import pandas as pd
import requests
import json
import time
from config import PATHS, SPRING_SYNC_URL, SPRING_FETCH_URL
from reddit_scraper import scrape_reddit
from data_processor import run_processor

def sync_dataframe_to_spring(df, source_name="Data"):
    print(f"\n--- Syncing {source_name} to Spring Boot ---")
    
    # Ensure correct columns for Java DTO
    payload_list = []
    
    for _, row in df.iterrows():
        # Handle NaN/Nulls
        txt = str(row.get('text_content', '')) if pd.notna(row.get('text_content')) else ""
        
        item = {
            "txt_content": txt,
            "timestamp": str(row.get('timestamp')),
            "category": str(row.get('category', 'General')),
            "age": int(row.get('age', 25)),
            "gender": str(row.get('gender', 'OTHER')).upper(),
            "region_clean": str(row.get('region_clean', 'Global')),
            "season": str(row.get('season', 'Core')),
            "clean_text": "",
            "topic_id": 0,
            "segment_id": 0,
            "topic_name": "Pending"
        }
        payload_list.append(item)

    # Send in batches
    BATCH_SIZE = 500
    for i in range(0, len(payload_list), BATCH_SIZE):
        batch = payload_list[i:i+BATCH_SIZE]
        try:
            resp = requests.post(SPRING_SYNC_URL, json=batch, headers={"Content-Type": "application/json"})
            if resp.status_code in [200, 201]:
                print(f"   Batch {i//BATCH_SIZE + 1}: ✅ Sent {len(batch)} rows")
            else:
                print(f"   Batch {i//BATCH_SIZE + 1}: ❌ Failed ({resp.status_code})")
        except Exception as e:
            print(f"   ❌ Connection Error: {e}")
            return False
            
    return True

def run_full_pipeline():
    print("="*50)
    print("🚀 STARTING AUTOMATED DATA PIPELINE")
    print("="*50)

    # 1. LOAD & SYNC HISTORICAL CSV (Run once or if DB is empty)
    # Uncomment this if you want to re-upload the CSV every time
    # print("\n[Phase 1] Loading Historical CSV...")
    # if os.path.exists(PATHS['raw_csv']):
    #     df_csv = pd.read_csv(PATHS['raw_csv'])
    #     # Ensure columns match expectations
    #     if 'region' in df_csv.columns: df_csv['region_clean'] = df_csv['region']
    #     sync_dataframe_to_spring(df_csv, "Historical CSV")

    # 2. SCRAPE & SYNC REDDIT (Live Data)
    print("\n[Phase 2] Scraping Reddit...")
    df_reddit = scrape_reddit(limit=10) # Adjust limit as needed
    if not df_reddit.empty:
        sync_dataframe_to_spring(df_reddit, "Reddit Live Data")
    else:
        print("⚠️ No Reddit data fetched. Skipping sync.")

    # 3. FETCH ALL FROM DB & PROCESS (Update Dashboard)
    print("\n[Phase 3] Fetching Combined Data from MongoDB...")
    try:
        resp = requests.get(SPRING_FETCH_URL)
        if resp.status_code == 200:
            data = resp.json()
            df_full = pd.DataFrame(data)
            
            print(f"✅ Downloaded {len(df_full)} rows from MongoDB.")
            
            # Map Java DTO fields back to Python logic expected by data_processor
            # Java sends 'txt_content', processor might expect 'text_content'
            if 'txt_content' in df_full.columns:
                df_full['text_content'] = df_full['txt_content']
            if 'region_clean' in df_full.columns:
                df_full['region'] = df_full['region_clean']

            # Save to raw_dataset.csv so data_processor can read it
            df_full.to_csv(PATHS['raw_csv'], index=False)
            print(f"💾 Saved combined dataset to {PATHS['raw_csv']}")
            
            # 4. RUN PROCESSOR
            print("\n[Phase 4] Running Rule-Based Processor...")
            run_processor() # From data_processor.py
            
        else:
            print(f"❌ Failed to fetch from Spring Boot: {resp.status_code}")

    except Exception as e:
        print(f"❌ Pipeline Error: {e}")

if __name__ == "__main__":
    # In a real app, you might run this on a schedule (e.g., while True: ... time.sleep(3600))
    run_full_pipeline()