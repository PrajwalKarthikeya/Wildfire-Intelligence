import pandas as pd
import numpy as np
import requests
import time
from database import engine

# California Bounding Box
LAT_MIN, LAT_MAX = 32.5, 42.0
LON_MIN, LON_MAX = -124.5, -114.0
GRID_STEP = 0.5  # 0.5 degree grid (~55km) to keep API calls reasonable for MVP

def get_california_fires():
    print("Extracting California fire data...")
    query = f"""
    SELECT latitude, longitude, frp 
    FROM fire_detections
    WHERE latitude BETWEEN {LAT_MIN} AND {LAT_MAX}
      AND longitude BETWEEN {LON_MIN} AND {LON_MAX}
    """
    df = pd.read_sql(query, engine)
    return df

def build_grid_features(fires_df):
    print(f"Building {GRID_STEP}° spatial grid for California...")
    
    # Create all possible grid cells for California
    lat_bins = np.arange(LAT_MIN, LAT_MAX + GRID_STEP, GRID_STEP)
    lon_bins = np.arange(LON_MIN, LON_MAX + GRID_STEP, GRID_STEP)
    
    # We use a multi-index to create a full grid, then reset to get combinations
    grid = pd.MultiIndex.from_product([lat_bins, lon_bins], names=['grid_lat', 'grid_lon']).to_frame(index=False)
    
    if not fires_df.empty:
        # Map fires to their closest grid cell
        fires_df['grid_lat'] = (fires_df['latitude'] / GRID_STEP).round() * GRID_STEP
        fires_df['grid_lon'] = (fires_df['longitude'] / GRID_STEP).round() * GRID_STEP
        
        # Aggregate fire features per grid cell
        fire_stats = fires_df.groupby(['grid_lat', 'grid_lon']).agg(
            fires_last_24h=('latitude', 'count'),
            avg_frp=('frp', 'mean'),
            max_frp=('frp', 'max')
        ).reset_index()
        
        # Merge stats onto the full grid (cells with no fires get 0)
        grid = pd.merge(grid, fire_stats, on=['grid_lat', 'grid_lon'], how='left')
    else:
        grid['fires_last_24h'] = 0
        grid['avg_frp'] = 0.0
        grid['max_frp'] = 0.0
        
    grid = grid.fillna(0)
    print(f"Total Grid Cells: {len(grid)}")
    print(f"Cells with active fires: {len(grid[grid['fires_last_24h'] > 0])}")
    return grid

def fetch_weather_features(grid_df):
    print("Fetching weather data from Open-Meteo...")
    
    # To avoid rate limits, we'll request weather ONLY for cells that are on land/relevant.
    # But for MVP, let's just fetch for all grid cells in batches.
    # Open-Meteo allows batching latitudes/longitudes in comma separated strings (max 100 per request)
    
    temps, hums, winds, precips = [], [], [], []
    
    batch_size = 50
    for i in range(0, len(grid_df), batch_size):
        batch = grid_df.iloc[i:i+batch_size]
        
        lats = ",".join(batch['grid_lat'].astype(str))
        lons = ",".join(batch['grid_lon'].astype(str))
        
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lats}&longitude={lons}&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                # If only 1 coordinate was requested, data['current'] is a dict. If multiple, it's a list of dicts.
                if isinstance(data, list):
                    for loc in data:
                        current = loc.get('current', {})
                        temps.append(current.get('temperature_2m', 0))
                        hums.append(current.get('relative_humidity_2m', 0))
                        precips.append(current.get('precipitation', 0))
                        winds.append(current.get('wind_speed_10m', 0))
                else:
                    # Single coordinate fallback
                    current = data.get('current', {})
                    temps.append(current.get('temperature_2m', 0))
                    hums.append(current.get('relative_humidity_2m', 0))
                    precips.append(current.get('precipitation', 0))
                    winds.append(current.get('wind_speed_10m', 0))
            else:
                print(f"Weather API Error: {response.status_code}")
                # Fill with defaults on error
                temps.extend([0] * len(batch))
                hums.extend([0] * len(batch))
                precips.extend([0] * len(batch))
                winds.extend([0] * len(batch))
        except Exception as e:
            print(f"Request failed: {e}")
            temps.extend([0] * len(batch))
            hums.extend([0] * len(batch))
            precips.extend([0] * len(batch))
            winds.extend([0] * len(batch))
            
        time.sleep(0.2)  # Gentle on the API
        
    grid_df['temperature_c'] = temps
    grid_df['humidity_percent'] = hums
    grid_df['precipitation_mm'] = precips
    grid_df['wind_speed_kmh'] = winds
    
    return grid_df

def build_dataset():
    fires_df = get_california_fires()
    grid_df = build_grid_features(fires_df)
    final_df = fetch_weather_features(grid_df)
    
    output_path = "data/ml_features.csv"
    final_df.to_csv(output_path, index=False)
    print(f"\nML Dataset successfully built and saved to {output_path}!")
    print("\n--- Final ML Feature Vector Sample ---")
    print(final_df[final_df['fires_last_24h'] > 0].head())

if __name__ == "__main__":
    build_dataset()
