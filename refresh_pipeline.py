import time
import subprocess
import os
import datetime

def run_script(script_name):
    print(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] Running {script_name}...")
    try:
        # Run the script and stream the output
        result = subprocess.run(
            ["python", os.path.join("data_pipeline", script_name)],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ {script_name} completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_name}:")
        print(e.stderr)
        return False

def run_full_pipeline():
    print(f"\n{'='*50}")
    print(f"🚀 INITIATING LIVE DATA REFRESH: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")
    
    # 1. Fetch live detections from NASA FIRMS and normalize
    if not run_script("fetch_fires.py"): return
    
    # 2. Insert new detections into the PostgreSQL/SQLite database
    if not run_script("load_data.py"): return
    
    # 3. Re-aggregate features and fetch live weather from Open-Meteo
    if not run_script("ml_dataset_builder.py"): return
    
    # 4. Run ML inference to update the risk probabilities
    # (For the MVP, retraining the HistGradientBoosting model on the fly takes <1 second)
    if not run_script("train_model3.py"): return
    
    # 5. Regenerate the GeoJSON map layer for the frontend
    if not run_script("generate_map_data.py"): return
    
    print(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] 🎉 Pipeline Refresh Complete! The dashboard is now up to date.")

if __name__ == "__main__":
    # Run once immediately
    run_full_pipeline()
    
    # Then loop every 15 minutes
    REFRESH_INTERVAL_SECONDS = 15 * 60
    
    while True:
        print(f"\nSleeping for 15 minutes. Next refresh at {(datetime.datetime.now() + datetime.timedelta(seconds=REFRESH_INTERVAL_SECONDS)).strftime('%H:%M:%S')}...")
        time.sleep(REFRESH_INTERVAL_SECONDS)
        run_full_pipeline()
