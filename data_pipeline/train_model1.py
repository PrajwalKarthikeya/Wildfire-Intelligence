import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, average_precision_score, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

def train_logistic_regression():
    print("Loading ML dataset...")
    df = pd.read_csv("data/ml_features.csv")
    
    # 1. Define Target Variable
    # For our MVP snapshot, we define risk as whether the cell has active fires.
    df['target_fire_risk'] = (df['fires_last_24h'] > 0).astype(int)
    
    # 2. Define Features
    # CRITICAL: We must drop 'fires_last_24h', 'avg_frp', 'max_frp' to prevent data leakage!
    features = ['grid_lat', 'grid_lon', 'temperature_c', 'humidity_percent', 'precipitation_mm', 'wind_speed_kmh']
    
    # 3. Geospatial Train/Test Split
    # Since we only have a single time snapshot for the MVP, a random split would cause spatial leakage.
    # We follow the roadmap's strict advice: "DO NOT randomly split your data."
    # We will train on Northern/Central California (Lat >= 36) and test on Southern California (Lat < 36).
    train_df = df[df['grid_lat'] >= 36]
    test_df = df[df['grid_lat'] < 36]
    
    X_train = train_df[features]
    y_train = train_df['target_fire_risk']
    
    X_test = test_df[features]
    y_test = test_df['target_fire_risk']
    
    print(f"Training set: {len(X_train)} cells (Northern/Central CA)")
    print(f"Testing set: {len(X_test)} cells (Southern CA)")
    print(f"Total active fire cells in dataset: {df['target_fire_risk'].sum()}")
    
    # 4. Train Model 1 (Logistic Regression Baseline)
    print("\nTraining Model 1: Logistic Regression...")
    # class_weight='balanced' is critical because fire datasets are heavily imbalanced (mostly 0s)
    model = LogisticRegression(class_weight='balanced', max_iter=1000)
    model.fit(X_train, y_train)
    
    # 5. Predictions & Probabilities
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    # 6. Evaluation Metrics
    print("\n--- Model 1 Evaluation (Southern CA Test Set) ---")
    
    # If the test set has no positive samples, roc_auc will fail.
    # Let's ensure there are fires in the test set.
    if y_test.sum() > 0:
        print(f"Precision: {precision_score(y_test, y_pred):.3f}")
        print(f"Recall:    {recall_score(y_test, y_pred):.3f}")
        print(f"F1 Score:  {f1_score(y_test, y_pred):.3f}")
        print(f"ROC-AUC:   {roc_auc_score(y_test, y_prob):.3f}")
        print(f"PR-AUC:    {average_precision_score(y_test, y_prob):.3f}")
        
        print("\nConfusion Matrix:")
        cm = confusion_matrix(y_test, y_pred)
        print(f"True Negatives: {cm[0][0]} | False Positives: {cm[0][1]}")
        print(f"False Negatives: {cm[1][0]} | True Positives: {cm[1][1]}")
    else:
        print("Warning: No active fires in the test set (Southern CA) to evaluate.")
        print(f"Predictions made: {y_pred.sum()} positive flags.")

if __name__ == "__main__":
    train_logistic_regression()
