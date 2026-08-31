import pandas as pd
from database import SessionLocal, FireDetection

def load_csv_to_db(csv_path="data/clean_fires.csv"):
    print(f"Loading data from {csv_path} into the database...")
    try:
        df = pd.read_csv(csv_path)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        print("Clean data not found or is completely empty. Skipping database load.")
        return

    # Convert timestamp column back to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    session = SessionLocal()
    
    # We want to avoid inserting duplicates if we run this multiple times.
    # We can query existing IDs. 
    # For large datasets, bulk inserts are better, but this works for our MVP.
    existing_ids = {row[0] for row in session.query(FireDetection.id).all()}
    
    new_records = []
    for _, row in df.iterrows():
        if row['fire_id'] not in existing_ids:
            conf_val = row.get('confidence', 50.0)
            if isinstance(conf_val, str):
                conf_val = {'l': 30.0, 'n': 70.0, 'h': 100.0}.get(conf_val.lower(), 50.0)
            else:
                try:
                    conf_val = float(conf_val)
                except:
                    conf_val = 50.0

            fire = FireDetection(
                id=row['fire_id'],
                latitude=row['latitude'],
                longitude=row['longitude'],
                timestamp=row['timestamp'].to_pydatetime(),
                satellite=row.get('satellite', 'Unknown'),
                brightness=row.get('brightness', 0.0),
                frp=row.get('frp', 0.0),
                confidence=conf_val,
                daynight=row.get('daynight', 'U')
            )
            new_records.append(fire)
            
    if new_records:
        session.bulk_save_objects(new_records)
        session.commit()
        print(f"Successfully inserted {len(new_records)} new fire detections into the database.")
    else:
        print("No new records to insert. Database is up to date.")
        
    session.close()

if __name__ == "__main__":
    load_csv_to_db()
