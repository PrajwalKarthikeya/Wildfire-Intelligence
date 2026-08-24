from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json
import os
import sys

# Add parent directory to path so we can import the database engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_pipeline.database import engine

app = FastAPI(title="Wildfire Intelligence API", version="1.0.0")

# Enable CORS for the frontend (Phase 9)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "online", "service": "Wildfire Intelligence API"}

@app.get("/fires/latest")
def get_latest_fires(limit: int = 100):
    query = f"SELECT * FROM fire_detections ORDER BY timestamp DESC LIMIT {limit}"
    df = pd.read_sql(query, engine)
    df['timestamp'] = df['timestamp'].astype(str)
    df['created_at'] = df['created_at'].astype(str)
    return df.to_dict(orient="records")

@app.get("/fires/history")
def get_fire_history():
    query = """
    SELECT strftime('%Y-%m-%d %H:00:00', timestamp) as hour, count(id) as fire_count
    FROM fire_detections
    GROUP BY hour
    ORDER BY hour DESC
    LIMIT 24
    """
    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")

@app.get("/fires/clusters")
def get_fire_clusters():
    # Returns top spatial concentrations (simplified clustering for MVP API)
    query = """
    SELECT ROUND(latitude, 1) as cluster_lat, ROUND(longitude, 1) as cluster_lon, count(id) as total_detections, avg(frp) as avg_frp
    FROM fire_detections
    GROUP BY cluster_lat, cluster_lon
    ORDER BY total_detections DESC
    LIMIT 10
    """
    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")

@app.get("/risk")
def get_risk_grid():
    # Returns the precomputed GeoJSON generated in Phase 6
    try:
        with open("../data/risk_grid.geojson", "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        # Fallback if running from a different directory
        try:
            with open("data/risk_grid.geojson", "r") as f:
                data = json.load(f)
            return data
        except Exception as e2:
            raise HTTPException(status_code=500, detail="Risk map GeoJSON not found. Run Phase 6 first.")

@app.get("/risk/{lat}/{lon}")
def get_specific_risk(lat: float, lon: float):
    # Find the closest grid cell in our California ML predictions
    try:
        try:
            df = pd.read_csv("../data/california_risk_predictions.csv")
        except:
            df = pd.read_csv("data/california_risk_predictions.csv")
            
        df['dist'] = abs(df['grid_lat'] - lat) + abs(df['grid_lon'] - lon)
        closest = df.sort_values('dist').iloc[0]
        return closest.drop('dist').to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics")
def get_analytics():
    query = "SELECT count(id) as total_fires, avg(frp) as avg_frp, max(frp) as max_frp FROM fire_detections"
    df = pd.read_sql(query, engine)
    result = df.iloc[0].to_dict()
    
    # Handle NaNs
    for k, v in result.items():
        if pd.isna(v):
            result[k] = 0.0
            
    return result

@app.get("/alerts")
def get_alerts():
    # Phase 10: In-app alerts based on current ML predictions
    try:
        try:
            df = pd.read_csv("../data/california_risk_predictions.csv")
        except:
            df = pd.read_csv("data/california_risk_predictions.csv")
            
        # Filter for High/Extreme risk cells (Risk > 60%)
        high_risk = df[df['risk_score'] >= 0.6].copy()
        
        # Sort by highest risk first
        high_risk = high_risk.sort_values('risk_score', ascending=False)
        
        alerts = []
        for _, row in high_risk.iterrows():
            # Generate dynamic alert reason based on feature thresholds
            reasons = []
            if row['fires_last_24h'] > 0:
                reasons.append(f"• {int(row['fires_last_24h'])} active fire detections")
            if row['avg_frp'] > 50:
                reasons.append("• Extremely high Fire Radiative Power (FRP)")
            if row['wind_speed_kmh'] > 20:
                reasons.append(f"• Strong winds ({row['wind_speed_kmh']} km/h)")
            if row['humidity_percent'] < 30:
                reasons.append(f"• Dangerously low humidity ({int(row['humidity_percent'])}%)")
            
            if not reasons:
                reasons.append("• Combination of regional factors")
                
            risk_pct = int(row['risk_score'] * 100)
            severity = "EXTREME" if risk_pct >= 80 else "HIGH"
                
            alert = {
                "id": f"alert-{row['grid_lat']}-{row['grid_lon']}",
                "severity": severity,
                "title": f"⚠ {severity} RISK ALERT",
                "message": f"Critical fire risk ({risk_pct}%) detected at coordinates {row['grid_lat']}, {row['grid_lon']}.",
                "reasons": "\n".join(reasons),
                "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            alerts.append(alert)
            
        return alerts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate alerts: {str(e)}")
