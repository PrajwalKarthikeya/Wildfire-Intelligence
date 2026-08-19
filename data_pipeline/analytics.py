import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from database import engine

def analyze_fires():
    print("Loading data from database...")
    df = pd.read_sql("SELECT latitude, longitude, timestamp, frp FROM fire_detections", engine)
    
    if df.empty:
        print("No data found in database.")
        return

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    print("\n--- 1. Fires Over Time (Grouped by Hour) ---")
    fires_over_time = df.set_index('timestamp').resample('h').size()
    print(fires_over_time.head(3))
    print("...")
    
    print("\n--- 2. Fire Intensity (FRP) ---")
    print(f"Average FRP: {df['frp'].mean():.2f} MW")
    print(f"Maximum FRP: {df['frp'].max():.2f} MW")
    print(f"Total FRP:   {df['frp'].sum():.2f} MW")

    print("\n--- 3. Geographic Concentration ---")
    # Round to 1 decimal place (approx 11km x 11km grid)
    df['grid_lat'] = df['latitude'].round(1)
    df['grid_lon'] = df['longitude'].round(1)
    grid_concentration = df.groupby(['grid_lat', 'grid_lon']).size().reset_index(name='fire_count')
    grid_concentration = grid_concentration.sort_values(by='fire_count', ascending=False)
    print("Top 5 Fire Hotspot Grids (0.1 degree cells):")
    print(grid_concentration.head(5).to_string(index=False))
    
    print("\n--- 4. Fire Clusters (DBSCAN) ---")
    print("Running DBSCAN clustering algorithm on coordinates...")
    # Convert lat/lon to radians for Haversine metric
    coords = np.radians(df[['latitude', 'longitude']])
    
    # eps is in radians: 14km / 6371km (Earth radius)
    db = DBSCAN(eps=14/6371.0, min_samples=10, algorithm='ball_tree', metric='haversine').fit(coords)
    df['cluster'] = db.labels_
    
    # Filter out noise (cluster == -1)
    clusters = df[df['cluster'] != -1]
    num_clusters = clusters['cluster'].nunique()
    print(f"Total distinct fire clusters found globally: {num_clusters}")
    
    if num_clusters > 0:
        largest_cluster_id = clusters['cluster'].value_counts().idxmax()
        largest = clusters[clusters['cluster'] == largest_cluster_id]
        
        print("\nDetails of the Largest Cluster:")
        print(f"  Cluster ID: {largest_cluster_id}")
        print(f"  Total Detections: {len(largest)}")
        print(f"  Average FRP: {largest['frp'].mean():.2f} MW")
        print(f"  Center Lat/Lon: {largest['latitude'].mean():.4f}, {largest['longitude'].mean():.4f}")
        print(f"  Time Window: {largest['timestamp'].min()} to {largest['timestamp'].max()}")

if __name__ == "__main__":
    analyze_fires()
