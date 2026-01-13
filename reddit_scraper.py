import praw
import pandas as pd
import numpy as np
import random
from datetime import datetime
from config import REDDIT_CONFIG, TARGET_SUBREDDITS

def scrape_reddit(limit=50):
    print(f"--- 🕵️‍♂️ Starting Reddit Scraper (Limit: {limit} posts per sub) ---")
    
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CONFIG["client_id"],
            client_secret=REDDIT_CONFIG["client_secret"],
            user_agent=REDDIT_CONFIG["user_agent"]
        )
        
        posts_data = []
        
        for sub_name in TARGET_SUBREDDITS:
            print(f"   Scanning r/{sub_name}...")
            subreddit = reddit.subreddit(sub_name)
            
            # Get New and Hot posts
            for post in subreddit.new(limit=limit):
                posts_data.append(process_post(post, sub_name))
            
            for post in subreddit.hot(limit=limit):
                posts_data.append(process_post(post, sub_name))
                
        # Convert to DataFrame
        df = pd.DataFrame(posts_data)
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['text_content'])
        
        print(f"✅ Scraped {len(df)} unique posts from Reddit.")
        return df

    except Exception as e:
        print(f"❌ Reddit Error: {e}")
        print("   (Did you put your API keys in config.py?)")
        return pd.DataFrame()

def process_post(post, source):
    # Combine title and body text
    full_text = f"{post.title} {post.selftext}"
    
    # Format timestamp for Java (YYYY-MM-DDTHH:MM:SS)
    ts = datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%dT%H:%M:%S')

    # --- SIMULATE DEMOGRAPHICS (Since Reddit is anonymous) ---
    # This ensures your dashboard filters work correctly with live data
    genders = ["MALE", "FEMALE", "OTHER"]
    regions = ["Europe", "North America", "Asia"]
    ages = range(18, 55)

    return {
        "text_content": full_text[:1000], # Limit length
        "timestamp": ts,
        "category": "Social Media", # Generic, will be retagged by processor
        "age": random.choice(ages),
        "gender": random.choice(genders),
        "region_clean": random.choice(regions),
        "season": "SS26" if datetime.now().month in [4,5,6,7,8] else "FW26",
        "clean_text": "", # Will be filled by processor
        "topic_id": 0,
        "segment_id": 0,
        "topic_name": f"r/{source}"
    }

if __name__ == "__main__":
    scrape_reddit(limit=5)