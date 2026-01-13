import os
from os.path import abspath, dirname, join

# --- DIRECTORY CONFIGURATION ---
BASE_DIR = dirname(abspath(__file__))
DATA_DIR = join(BASE_DIR, "data")

# --- FILE PATHS ---
PATHS = {
    "raw_csv": join(DATA_DIR, "raw_dataset.csv"), 
    "processed_csv": join(DATA_DIR, "processed_data.csv")
}

# --- EXTERNAL SERVICES ---
SPRING_SYNC_URL = "http://localhost:8080/segments/"      # POST (Save data)
SPRING_FETCH_URL = "http://localhost:8080/segments/all"  # GET (Fetch all data)

# --- REDDIT API CONFIGURATION ---
# You must get these from https://www.reddit.com/prefs/apps
REDDIT_CONFIG = {
    "client_id": "YOUR_CLIENT_ID",         # REPLACE THIS
    "client_secret": "YOUR_CLIENT_SECRET", # REPLACE THIS
    "user_agent": "TrendSense_App/1.0"
}

# Target Subreddits for Fashion
TARGET_SUBREDDITS = ["streetwear", "femalefashionadvice", "malefashionadvice", "sneakers", "frugalmalefashion"]

# --- CLIENT TAXONOMY ---
PRODUCT_HIERARCHY = {
    "Clothing": ["T-shirt", "Shirt", "Hoodie", "Pants", "Jeans", "Dress", "Activewear", "Top"],
    "Footwear": ["Sneaker", "Boot", "Sandal", "Heel", "Flats"],
    "Accessories": ["Watch", "Bag", "Jewelry", "Eyewear"]
}

# --- KEYWORD MAPPING ---
TAXONOMY = {
    "Clothing": {
        "keywords": [],
        "sub_categories": {
            "T-shirt": ["t-shirt", "tee", "polo", "tshirt"],
            "Shirt": ["shirt", "button-down", "flannel", "blouse", "collar"],
            "Hoodie": ["hoodie", "sweatshirt", "sweater", "pullover", "jumper"],
            "Pants": ["pant", "trouser", "chino", "cargo", "jogger", "slacks"],
            "Jeans": ["jean", "denim", "jeggings"],
            "Dress": ["dress", "gown", "frock", "skirt", "maxi", "midi", "mini"],
            "Activewear": ["activewear", "gym", "yoga", "fitness", "legging", "sport bra", "tracksuit"],
            "Top": ["top", "tank", "camisole", "crop", "bodysuit"]
        }
    }
}

# --- ATTRIBUTES ---
ATTRIBUTES = {
    "Color": ["Red", "Blue", "Green", "Yellow", "Black", "White", "Pink", "Purple", "Orange", "Grey", "Beige", "Brown", "Navy", "Teal", "Gold", "Silver", "Neon", "Cream", "Khaki", "Burgundy", "Charcoal"],
    "Fabric": ["Linen", "Denim", "Cotton", "Silk", "Wool", "Leather", "Mesh", "Velvet", "Polyester", "Satin", "Suede", "Chiffon", "Knitted", "Lace", "Cashmere", "Spandex"],
    "Style": ["Oversized", "Slim", "Combat", "Retro", "Layered", "Cropped", "Fitted", "Vintage", "Boho", "Minimalist", "Streetwear", "Casual", "Formal", "Baggy", "Chic", "Sporty", "Elegant", "Printed", "Striped"]
}