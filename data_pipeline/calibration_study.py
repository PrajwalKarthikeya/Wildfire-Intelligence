import pandas as pd
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.calibration import calibration_curve, CalibratedClassifierCV
from sklearn.metrics import brier_score_loss
import warnings
warnings.filterwarnings('ignore')

def run_calibration_study():
    print("Loading dataset for Probability Calibration...")
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
    
    if y_test.sum() == 0:
        print("Error: No positive cases in the test set. Cannot run evaluation.")
        return

    # Train Uncalibrated Champion Model
    print("\nTraining Uncalibrated Champion Model...")
    base_model = HistGradientBoostingClassifier(max_iter=100, learning_rate=0.05, max_leaf_nodes=15, class_weight='balanced', random_state=42)
    base_model.fit(X_train, y_train)
    
    y_prob_uncalibrated = base_model.predict_proba(X_test)[:, 1]
    brier_uncalibrated = brier_score_loss(y_test, y_prob_uncalibrated)
    
    # Train Calibrated Model (using Isotonic Regression to map outputs to true probabilities)
    print("Training Calibrated Model (Isotonic Regression)...")
    calibrated_model = CalibratedClassifierCV(base_model, method='isotonic', cv=3)
    calibrated_model.fit(X_train, y_train) 
    
    y_prob_calibrated = calibrated_model.predict_proba(X_test)[:, 1]
    brier_calibrated = brier_score_loss(y_test, y_prob_calibrated)
    
    print("\n--- Brier Score Loss (Lower is better) ---")
    print(f"Uncalibrated Model: {brier_uncalibrated:.4f}")
    print(f"Calibrated Model:   {brier_calibrated:.4f}")
    
    # Calculate Calibration Curve (Reliability Diagram data)
    fraction_of_positives, mean_predicted_value = calibration_curve(y_test, y_prob_uncalibrated, n_bins=5)
    
    print("\n--- Reliability Diagram (Uncalibrated) ---")
    print("If predicted probability is X, the actual fraction of true fires is Y. Ideally, X should equal Y.")
    print("| Predicted Probability (Bin Mean) | Actual True Fraction |")
    print("|---|---|")
    for pred, actual in zip(mean_predicted_value, fraction_of_positives):
        print(f"| {pred:.2%} | {actual:.2%} |")
        
    print("\nConclusion: Tree-based models often push probabilities to the extremes (0 or 1). Calibration forces the outputs to represent true statistical likelihoods.")

if __name__ == "__main__":
    run_calibration_study()
