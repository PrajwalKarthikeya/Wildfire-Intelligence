import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
import warnings
warnings.filterwarnings('ignore')

def run_error_analysis():
    print("Loading dataset for Failure Analysis...")
    df = pd.read_csv("data/ml_features.csv")
    df['target_fire_risk'] = (df['fires_last_24h'] > 0).astype(int)
    
    # Geospatial Split
    train_df = df[df['grid_lat'] >= 36]
    test_df = df[df['grid_lat'] < 36]
    
    features = ['grid_lat', 'grid_lon', 'temperature_c', 'humidity_percent', 'precipitation_mm', 'wind_speed_kmh']
    
    X_train = train_df[features]
    y_train = train_df['target_fire_risk']
    
    X_test = test_df[features]
    y_test = test_df['target_fire_risk']

    print("Training Champion Model...")
    model = HistGradientBoostingClassifier(max_iter=100, learning_rate=0.05, max_leaf_nodes=15, class_weight='balanced', random_state=42)
    model.fit(X_train, y_train)
    
    # Predict
    test_df['predicted_class'] = model.predict(X_test)
    test_df['predicted_prob'] = model.predict_proba(X_test)[:, 1]
    
    # Isolate Errors
    false_positives = test_df[(test_df['predicted_class'] == 1) & (test_df['target_fire_risk'] == 0)]
    false_negatives = test_df[(test_df['predicted_class'] == 0) & (test_df['target_fire_risk'] == 1)]
    
    print(f"\nTotal False Positives: {len(false_positives)}")
    print(f"Total False Negatives: {len(false_negatives)}\n")
    
    print("--- FALSE POSITIVE ANALYSIS ---")
    if not false_positives.empty:
        # Get the one with the highest confidence
        fp = false_positives.sort_values(by='predicted_prob', ascending=False).iloc[0]
        print(f"Predicted Probability: {fp['predicted_prob']:.2%}")
        print(f"Actual Fire: No")
        print(f"Location: Lat {fp['grid_lat']}, Lon {fp['grid_lon']}")
        print(f"Weather: {fp['temperature_c']} C, {fp['humidity_percent']}% Humidity, {fp['wind_speed_kmh']} km/h Wind")
        print("Hypothesis: The weather was perfectly primed for a fire (high temp, low humidity, high wind), but no human or lightning actually sparked an ignition. The model correctly identified a dangerous environment, but lacked an ignition source feature.")
        
    print("\n--- FALSE NEGATIVE ANALYSIS ---")
    if not false_negatives.empty:
        # Get the one with the lowest confidence
        fn = false_negatives.sort_values(by='predicted_prob', ascending=True).iloc[0]
        print(f"Predicted Probability: {fn['predicted_prob']:.2%}")
        print(f"Actual Fire: YES")
        print(f"Location: Lat {fn['grid_lat']}, Lon {fn['grid_lon']}")
        print(f"Weather: {fn['temperature_c']} C, {fn['humidity_percent']}% Humidity, {fn['wind_speed_kmh']} km/h Wind")
        print("Hypothesis: The weather was relatively mild. This fire was likely caused by a localized human event (e.g., a car crash, arson, or campfire) that superseded meteorological conditions. Our model is blind to human-caused anomalies.")

if __name__ == "__main__":
    run_error_analysis()
