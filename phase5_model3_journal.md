# Phase 5 Journey Journal: The Champion (Model 3)

We had a solid Random Forest (Model 2) that beat our baseline, but the roadmap challenged us to go one step further. It was time to unleash **HistGradientBoosting**.

---

## 🧑‍🏫 Layman's Terms

If a Random Forest is a committee of 100 experts all shouting their answers at the same time and taking a vote, **Gradient Boosting** is more like a relay race. 

The first expert makes a prediction. It's usually a bit flawed. They hand their mistakes to the second expert, who explicitly focuses on *fixing the mistakes* the first expert made. The second expert hands the new mistakes to the third expert, and so on. They learn from each other sequentially.

**The Result:** It is our absolute champion! 
It successfully found the hidden fire in Southern California, just like the Random Forest did. But more importantly, it drastically reduced its false alarms. The Random Forest panicked and falsely predicted 8 fires. Gradient Boosting stayed calm and only falsely predicted 3. 

It is the smartest model we've built, and it is officially the model we are using to power our final Dashboard!

---

## 👩‍💻 Technical Terms

### Step 1: Sequential Ensemble Architecture
We implemented `sklearn.ensemble.HistGradientBoostingClassifier`, which is scikit-learn's blazing-fast implementation of LightGBM. We configured it with `learning_rate=0.05` and `max_leaf_nodes=15` to heavily regularize the boosting process, preventing it from overfitting to the noise in our sparse 1-day dataset. We also utilized the native `class_weight='balanced'` parameter.

### Step 2: Evaluation Metrics (The Winner)
Gradient Boosting outperformed both the Logistic Regression baseline and the Random Forest across the board on the Southern California holdout set:
*   **ROC-AUC**: Jumped to `0.793` (Highest yet)
*   **Precision**: Doubled to `0.250`
*   **False Positives**: Dropped from `8` (Random Forest) down to `3`
*   **True Positives**: Held steady at `1`

By dramatically reducing the False Positive Rate without sacrificing Recall, the `HistGradientBoostingClassifier` proved it can construct far more precise, non-linear geospatial decision boundaries. 

We generated the final probabilistic predictions using this champion model and overwrote `data/california_risk_predictions.csv`. Phase 5 is fully complete, and we are ready for mapping!
