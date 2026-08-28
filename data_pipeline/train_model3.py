import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, average_precision_score, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

def train_hist_gradient_boosting():
    print("Loading ML dataset...")
    df = pd.read_csv("data/ml_features.csv")
    
    # 1. Target Variable
    df['target_fire_risk'] = (df['fires_last_24h'] > 0).astype(int)
    
    # 2. Features
    features = ['grid_lat', 'grid_lon', 'temperature_c', 'humidity_percent', 'precipitation_mm', 'wind_speed_kmh']
    
    # 3. Geospatial Train/Test Split
    train_df = df[df['grid_lat'] >= 36]
    test_df = df[df['grid_lat'] < 36]
    
    X_train = train_df[features]
    y_train = train_df['target_fire_risk']
    
    X_test = test_df[features]
    y_test = test_df['target_fire_risk']
    
    print(f"Training set: {len(X_train)} cells (Northern/Central CA)")
    print(f"Testing set: {len(X_test)} cells (Southern CA)")
    
    # 4. Train Model 3 (HistGradientBoosting)
    print("\nTraining Model 3: HistGradientBoosting...")
    # HistGradientBoosting doesn't natively support class_weight='balanced' like Random Forest.
    # We can handle class imbalance by setting class weights manually or adjusting learning parameters,
    # but let's try it natively with some regularization to prevent overfitting on our small dataset.
    model = HistGradientBoostingClassifier(
        max_iter=100, 
        learning_rate=0.05, 
        max_leaf_nodes=15, 
        random_state=42,
        class_weight='balanced' # wait, class_weight is supported in newer sklearn versions! Let's use it.
    )
    model.fit(X_train, y_train)
    
    # 5. Predictions
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    # 6. Evaluation
    print("\n--- Model 3 Evaluation (Southern CA Test Set) ---")
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
        print("Warning: No active fires in the test set to evaluate metrics. Outputting baseline zero-risk map.")
        
    print("\nOverwriting risk predictions for Phase 6 map generation with Model 3 (Winner!)...")
    df['risk_score'] = model.predict_proba(df[features])[:, 1]
    df.to_csv("data/california_risk_predictions.csv", index=False)

if __name__ == "__main__":
    train_hist_gradient_boosting()
