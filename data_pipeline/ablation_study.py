import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, average_precision_score
import warnings
warnings.filterwarnings('ignore')

def run_ablation_study():
    print("Loading dataset for Ablation Study...")
    df = pd.read_csv("data/ml_features.csv")
    df['target_fire_risk'] = (df['fires_last_24h'] > 0).astype(int)
    
    # Geospatial Split
    train_df = df[df['grid_lat'] >= 36]
    test_df = df[df['grid_lat'] < 36]
    
    y_train = train_df['target_fire_risk']
    y_test = test_df['target_fire_risk']
    
    if y_test.sum() == 0:
        print("Error: No positive cases in the test set. Cannot run evaluation.")
        return

    # Define Feature Sets
    feature_sets = {
        "Model A: Spatial Only (Lat/Lon)": ['grid_lat', 'grid_lon'],
        "Model B: Weather Only": ['temperature_c', 'humidity_percent', 'precipitation_mm', 'wind_speed_kmh'],
        "Model C: Spatial + Weather (Full Model)": ['grid_lat', 'grid_lon', 'temperature_c', 'humidity_percent', 'precipitation_mm', 'wind_speed_kmh']
    }
    
    results = []
    
    print("\nRunning Ablation Experiments using HistGradientBoosting...\n")
    
    for name, features in feature_sets.items():
        X_train = train_df[features]
        X_test = test_df[features]
        
        model = HistGradientBoostingClassifier(max_iter=100, learning_rate=0.05, max_leaf_nodes=15, class_weight='balanced', random_state=42)
        model.fit(X_train, y_train)
        
        y_prob = model.predict_proba(X_test)[:, 1]
        
        roc_auc = roc_auc_score(y_test, y_prob)
        pr_auc = average_precision_score(y_test, y_prob)
        
        results.append({
            "Experiment": name,
            "ROC-AUC": f"{roc_auc:.3f}",
            "PR-AUC": f"{pr_auc:.3f}"
        })
        
    # Print Markdown Table
    print("| Experiment | ROC-AUC | PR-AUC |")
    print("|---|---|---|")
    for r in results:
        print(f"| {r['Experiment']} | {r['ROC-AUC']} | {r['PR-AUC']} |")

if __name__ == "__main__":
    run_ablation_study()
