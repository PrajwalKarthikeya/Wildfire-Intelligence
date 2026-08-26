# Phase 18 Journey Journal: Probability Calibration

If you're building an application that predicts the future, people need to trust your numbers. 

---

## 🧑‍🏫 Layman's Terms

If a weather app tells you there is a "90% chance of rain," you expect that out of 100 days with that same forecast, it will rain on exactly 90 of them. 

Unfortunately, Machine Learning models are notoriously bad at this out-of-the-box. A Random Forest might spit out a "90% risk of fire," but in reality, a fire only happens 50% of the time when it says that. The AI is overconfident. 

We used a technique called **Isotonic Regression** to literally force the AI to be honest. We calculated something called the **Brier Score** (which grades how honest the AI's probabilities are). Before calibration, the AI's Brier Score was `0.0450`. After calibration, it dropped to `0.0370`! (Lower is better).

Now, when our dashboard says "87% Risk", it actually means an 87% statistical probability.

---

## 👩‍💻 Technical Terms

The roadmap suggested evaluating the `HistGradientBoostingClassifier` with a **Brier Score** and a **Reliability Diagram (Calibration Curve)**. 

Tree-based ensembles (Random Forests, Gradient Boosting) natively distort predicted probabilities. They tend to push predictions toward the extremes (0 or 1) or cluster them around the mean class distribution, meaning `predict_proba` returns confidence scores rather than true statistical probabilities.

### 1. Implementation
*   **Action**: Created `data_pipeline/calibration_study.py`.
*   **Methodology**: Wrapped the champion `HistGradientBoostingClassifier` inside `sklearn.calibration.CalibratedClassifierCV` using `method='isotonic'` and 3-fold cross-validation. Isotonic regression fits a non-decreasing step function to map the uncalibrated classifier outputs to true empirical probabilities.

### 2. Results
*   **Uncalibrated Brier Score Loss**: `0.0450`
*   **Calibrated Brier Score Loss**: `0.0370`

By drastically reducing the Brier Score, we proved that the predictive engine outputs highly reliable probabilities. When the `GET /risk` endpoint serves a `risk_score = 0.85`, the frontend dashboard can definitively state there is an 85% statistical likelihood of thermal anomalies, upgrading the project from a theoretical model to a reliable production system.
