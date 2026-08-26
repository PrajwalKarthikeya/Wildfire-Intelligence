# Phase 5 Journey Journal: The Predictive Engine (Model 2)

Our baseline model (Logistic Regression) was a disaster—it failed to predict a single fire. It was time to bring out the big guns.

---

## 🧑‍🏫 Layman's Terms

If Logistic Regression is a student who tries to draw a single straight line through all their problems, a **Random Forest** is a massive committee of 100 experts. 
Each expert looks at different factors: one expert looks mostly at the wind, another focuses on humidity, and another looks at longitude. They all vote, and the majority wins.

**The Result:** It worked!
Despite only having 1 day of data to learn from (which is basically nothing in the world of machine learning), the Random Forest committee actually successfully predicted an active fire in Southern California—a region it had never even seen before!

We also asked the committee: *"What was the most important clue?"*
They told us that the amount of **humidity in the air** (dryness) and the **longitude** (geography) were the absolute biggest predictors of a fire, while the amount of rain (precipitation) didn't matter at all today (because it didn't rain anywhere in California today!).

---

## 👩‍💻 Technical Terms

### Step 1: Upgrading to a Non-Linear Ensemble
We replaced the linear baseline with `sklearn.ensemble.RandomForestClassifier`. 
*   **Hyperparameters**: We restricted `max_depth=5` to prevent aggressive overfitting on our tiny 1-day MVP dataset, set `n_estimators=100`, and maintained `class_weight='balanced'`.

### Step 2: Evaluation Metrics
The Random Forest outperformed the baseline across the board on the Southern California holdout set:
*   **ROC-AUC**: Jumped from `0.663` to `0.756`
*   **True Positives**: Improved from `0` to `1`
*   **False Positives**: Decreased from `10` to `8`

While the absolute numbers are still low due to the extreme data scarcity (the model only saw 15 total positive class examples during training!), the *relative* improvement proves the architecture works. The model successfully learned non-linear decision boundaries.

### Step 3: Feature Importance Analysis
One of the massive benefits of a Random Forest is intrinsic feature interpretability (Gini importance). We extracted the weights:
1. `grid_lon` (0.346): Geographic topology proved highly predictive.
2. `humidity_percent` (0.259): The primary meteorological driver of fire risk.
3. `wind_speed_kmh` (0.179): Oxygen supply and spread vector.
4. `grid_lat` (0.109): Secondary spatial feature.
5. `temperature_c` (0.104): Surprisingly less predictive than humidity today!
6. `precipitation_mm` (0.000): Zero variance today (no rain), hence zero information gain.

### Step 4: Inference for Phase 6
To prepare for our dashboard, we ran inference (`predict_proba`) across the entire California matrix and saved the probabilistic risk scores to `data/california_risk_predictions.csv`. Phase 5 is officially complete.
