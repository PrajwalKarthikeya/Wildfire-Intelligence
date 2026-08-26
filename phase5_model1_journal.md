# Phase 5 Journey Journal: Training the ML Baseline (Model 1)

With our pristine California dataset in hand, it was time to teach a machine to predict fire risk based on weather and location.

---

## 🧑‍🏫 Layman's Terms

Imagine asking someone to predict if a forest fire is going to happen today, but they've only been alive for 24 hours. They know today's temperature and wind speed, but they lack years of historical context.

That is essentially what we did here. We used **Logistic Regression** (a very basic algorithm that draws straight lines to separate data) to establish a "Baseline." 
A baseline is our worst-case scenario. It answers: *"How good is the absolute dumbest model we can build?"*

**The Result:** It was terrible! 
Our model missed all 6 fires in Southern California (False Negatives) and incorrectly panicked and predicted fires in 10 places where there were none (False Positives).

Why did it fail?
1. **The Dataset is Tiny**: We only gave it 1 day of data. It saw exactly 21 fires total. That's not enough to learn complex weather patterns.
2. **Straight Lines Don't Work for Nature**: Logistic regression tries to draw a straight line between "safe" and "fire". But wildfires are complicated. A high temperature only causes a fire if the humidity is low *and* the wind is high. Logistic regression struggles to understand these combined conditions.

But this is a **huge success for our project methodology**. We now have a mathematical baseline to beat. In our next step, we will use a much smarter model (Random Forest) to blow these results out of the water.

---

## 👩‍💻 Technical Terms

### Step 1: Mitigating Data Leakage
Before training, we dropped `fires_last_24h`, `avg_frp`, and `max_frp` from our feature matrix `X`. If we left them in, the model would simply learn "if there is a fire currently burning, predict a fire," which is mathematically trivial and useless for predictive forecasting. Our independent variables were strictly spatial (`grid_lat`, `grid_lon`) and meteorological (`temperature_c`, `humidity_percent`, `wind_speed_kmh`, `precipitation_mm`).

### Step 2: Geospatial Splitting (No Random Splits!)
As outlined in our Phase 0 architecture, randomly splitting spatiotemporal data causes severe data leakage (e.g., training on cell A and testing on adjacent cell B on the same day leaks the regional weather state).
Since we are using a single-day MVP snapshot, we implemented a strict **spatial split**:
*   **Train Set**: Northern/Central California (`latitude >= 36`) - 286 cells
*   **Test Set**: Southern California (`latitude < 36`) - 154 cells

### Step 3: Training the Baseline (Logistic Regression)
We trained `sklearn.linear_model.LogisticRegression` using `class_weight='balanced'` to aggressively penalize errors on the minority class (fires). 

### Step 4: Evaluation Metrics
The model generalized very poorly to Southern California:
*   **Precision**: `0.000`
*   **Recall**: `0.000`
*   **F1 Score**: `0.000`
*   **ROC-AUC**: `0.663`
*   **Confusion Matrix**: 
    *   True Negatives: 138 (Correctly identified safe zones)
    *   False Positives: 10 (Cried wolf)
    *   False Negatives: 6 (Completely missed actual fires)
    *   True Positives: 0 (Failed to predict a single fire)

While ROC-AUC shows it learned *slight* probabilistic separation (`0.663 > 0.5`), the strict linear decision boundary failed to capture the non-linear interaction terms between wind, humidity, and temperature. 

This sets a perfect, defensible baseline for us to benchmark our upcoming Random Forest model against.
