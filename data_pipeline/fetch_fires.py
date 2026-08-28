import os
import requests
import pandas as pd
import hashlib
from io import StringIO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

FIRMS_MAP_KEY = os.getenv("FIRMS_MAP_KEY")
BASE_URL = "https://firms.modaps.eosdis.nasa.gov/api/area/csv"

def fetch_active_fires(source="VIIRS_SNPP_NRT", area="world", day_range=1):
    """
    Fetches active fire data from NASA FIRMS.
    """
    if not FIRMS_MAP_KEY:
        raise ValueError("FIRMS_MAP_KEY not found in environment variables.")

    url = f"{BASE_URL}/{FIRMS_MAP_KEY}/{source}/{area}/{day_range}"
    
    print(f"Fetching data from FIRMS API: {source} (Area: {area}, Days: {day_range})...", flush=True)
    response = requests.get(url, timeout=30)
    
    if response.status_code != 200:
        print(f"Error: NASA API returned {response.status_code}")
        print(response.text)
        response.raise_for_status()

    # Parse CSV content into Pandas DataFrame
    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data)
    
    return df

def clean_and_normalize(df):
    """
    Step 4: Clean the data and normalize the schema.
    Handles duplicates, missing values, timestamps, and sensor differences.
    """
    if df.empty:
        return pd.DataFrame()

    print(f"Initial raw detections: {len(df)}")

    # 1. Drop rows missing crucial coordinates or time info
    df = df.dropna(subset=['latitude', 'longitude', 'acq_date', 'acq_time'])

    # 2. Filter invalid coordinates
    df = df[(df['latitude'] >= -90) & (df['latitude'] <= 90)]
    df = df[(df['longitude'] >= -180) & (df['longitude'] <= 180)]

    # 3. Handle Timestamps (Convert acq_date and acq_time into a single datetime)
    # acq_time is typically an integer like 1342 (13:42) or 5 (00:05). zfill pads it to 4 chars.
    df['acq_time_str'] = df['acq_time'].astype(str).str.zfill(4)
    df['timestamp'] = pd.to_datetime(df['acq_date'] + ' ' + df['acq_time_str'], format='%Y-%m-%d %H%M')

    # 4. Handle Sensor Differences (Brightness & Confidence)
    # VIIRS uses bright_ti4, MODIS uses brightness. Normalize to 'brightness'
    if 'bright_ti4' in df.columns:
        df['brightness'] = df['bright_ti4']
    elif 'brightness' not in df.columns:
        df['brightness'] = None

    # VIIRS confidence is string (l, n, h). MODIS is 0-100. Normalize to 0-100 scale.
    if 'confidence' in df.columns:
        if df['confidence'].dtype == 'O' or df['confidence'].dtype == str:  # Object/String type
            conf_map = {'l': 30, 'n': 70, 'h': 100}
            df['confidence'] = df['confidence'].str.lower().map(conf_map).fillna(50)
        else:
            df['confidence'] = df['confidence'].fillna(50)

    # Fill missing FRP with 0 (assuming very low power if not measured, though usually it is present)
    if 'frp' in df.columns:
        df['frp'] = df['frp'].fillna(0.0)

    # Fill missing daynight with 'D' as default or map it
    if 'daynight' in df.columns:
        df['daynight'] = df['daynight'].fillna('U')

    # Assign satellite if missing
    if 'satellite' not in df.columns:
        df['satellite'] = 'Unknown'

    # 5. Create a unified schema
    normalized_cols = ['latitude', 'longitude', 'timestamp', 'satellite', 'brightness', 'frp', 'confidence', 'daynight']
    # Select only the columns that exist in the dataframe to avoid errors
    available_cols = [col for col in normalized_cols if col in df.columns]
    
    clean_df = df[available_cols].copy()

    # 6. Generate unique fire_id based on location and time
    def generate_id(row):
        unique_str = f"{row['latitude']}-{row['longitude']}-{row['timestamp']}-{row.get('satellite', '')}"
        return hashlib.md5(unique_str.encode()).hexdigest()
        
    clean_df.insert(0, 'fire_id', clean_df.apply(generate_id, axis=1))

    # 7. Remove Duplicates
    clean_df = clean_df.drop_duplicates(subset=['fire_id'])
    
    print(f"Cleaned and normalized detections: {len(clean_df)}")
    return clean_df

if __name__ == "__main__":
    try:
        fire_df = fetch_active_fires(source="VIIRS_SNPP_NRT", area="world", day_range=1)
        
        # Step 3 & 4: Clean and Normalize Data
        clean_df = clean_and_normalize(fire_df)
        
        # Save locally
        output_path = "data/clean_fires.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        clean_df.to_csv(output_path, index=False)
        print(f"Saved to {output_path}")
        
        print("\n--- Normalized Data Sample ---")
        print(clean_df.head())
        print("------------------------------\n")
        
    except Exception as e:
        print(f"Pipeline failed: {e}")
        import sys
        sys.exit(1)
