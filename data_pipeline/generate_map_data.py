import pandas as pd
import json

def generate_risk_categories(score):
    percent = score * 100
    if percent < 20: return "LOW"
    elif percent < 40: return "MODERATE"
    elif percent < 60: return "ELEVATED"
    elif percent < 80: return "HIGH"
    else: return "EXTREME"

def get_color(category):
    return {
        "LOW": "#2ecc71",       # Green
        "MODERATE": "#f1c40f",  # Yellow
        "ELEVATED": "#e67e22",  # Orange
        "HIGH": "#e74c3c",      # Red
        "EXTREME": "#8e44ad"    # Purple
    }.get(category, "#bdc3c7")

def convert_to_geojson():
    print("Reading California risk predictions...")
    df = pd.read_csv("data/california_risk_predictions.csv")
    
    # 1. Convert Risk Scores
    df['risk_percent'] = (df['risk_score'] * 100).round(1)
    df['risk_category'] = df['risk_score'].apply(generate_risk_categories)
    
    # 2. Build GeoJSON Polygons for the Grid
    features = []
    
    # Our grid step was 0.5. The grid_lat/grid_lon are the centers.
    step = 0.5
    half = step / 2.0
    
    for _, row in df.iterrows():
        lat = row['grid_lat']
        lon = row['grid_lon']
        
        # Only plot elevated risk or higher to keep the map clean, OR plot everything
        # Let's plot everything but give lower opacity to LOW/MODERATE
        
        polygon = [
            [lon - half, lat - half],
            [lon + half, lat - half],
            [lon + half, lat + half],
            [lon - half, lat + half],
            [lon - half, lat - half] # Close the ring
        ]
        
        feature = {
            "type": "Feature",
            "properties": {
                "risk_percent": row['risk_percent'],
                "risk_category": row['risk_category'],
                "color": get_color(row['risk_category']),
                "fires_last_24h": row['fires_last_24h'],
                "temperature_c": row['temperature_c'],
                "humidity_percent": row['humidity_percent'],
                "wind_speed_kmh": row['wind_speed_kmh']
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [polygon]
            }
        }
        features.append(feature)
        
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    output_path = "data/risk_grid.geojson"
    with open(output_path, "w") as f:
        json.dump(geojson, f)
        
    print(f"Generated {len(features)} risk polygons and saved to {output_path}")

if __name__ == "__main__":
    convert_to_geojson()
