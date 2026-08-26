import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, average_precision_score, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

def run_evaluation():
    print("Loading ML dataset for comprehensive evaluation...")
    df = pd.read_csv("data/ml_features.csv")
    
    # Target Variable
    df['target_fire_risk'] = (df['fires_last_24h'] > 0).astype(int)
    
    # Features (No leakage)
    features = ['grid_lat', 'grid_lon', 'temperature_c', 'humidity_percent', 'precipitation_mm', 'wind_speed_kmh']
    
    # Geospatial Train/Test Split
    train_df = df[df['grid_lat'] >= 36]
    test_df = df[df['grid_lat'] < 36]
    
    X_train = train_df[features]
    y_train = train_df['target_fire_risk']
    
    X_test = test_df[features]
    y_test = test_df['target_fire_risk']
    
    # We must ensure there is at least one positive case in the test set to calculate ROC/PR curves
    if y_test.sum() == 0:
        print("Error: No positive cases in the test set. Cannot run evaluation.")
        return
        
    models = {
        "Logistic Regression": LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=5, class_weight='balanced', random_state=42),
        "HistGradientBoosting": HistGradientBoostingClassifier(max_iter=100, learning_rate=0.05, max_leaf_nodes=15, class_weight='balanced', random_state=42)
    }
    
    results = []
    
    print("\nTraining and evaluating models...\n")
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        roc_auc = roc_auc_score(y_test, y_prob)
        pr_auc = average_precision_score(y_test, y_prob)
        
        cm = confusion_matrix(y_test, y_pred)
        tn, fp, fn, tp = cm.ravel()
        
        results.append({
            "Model": name,
            "Precision": f"{precision:.3f}",
            "Recall": f"{recall:.3f}",
            "F1": f"{f1:.3f}",
            "ROC-AUC": f"{roc_auc:.3f}",
            "PR-AUC": f"{pr_auc:.3f}",
            "TP": tp,
            "FP": fp
        })
        
    # Generate Markdown Table
    print("| Model | Precision | Recall | F1 | ROC-AUC | PR-AUC | True Positives | False Positives |")
    print("|---|---|---|---|---|---|---|---|")
    for r in results:
        print(f"| {r['Model']} | {r['Precision']} | {r['Recall']} | {r['F1']} | {r['ROC-AUC']} | {r['PR-AUC']} | {r['TP']} | {r['FP']} |")

if __name__ == "__main__":
    run_evaluation()
