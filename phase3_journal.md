# Phase 3 Journey Journal: Historical Analytics

With our data securely stored in our relational database (Phase 2), we could finally start extracting intelligence from it. In Phase 3, we built the analytical engine that will eventually power our frontend dashboard.

---

## 🧑‍🏫 Layman's Terms

We have 23,000 fire records sitting in our digital filing cabinet. But a giant list of fires doesn't help anyone make decisions. We need to summarize it, find patterns, and group things together.

In Phase 3, we built an automated "Data Analyst" that answers four critical questions:

1. **When are fires happening?** 
   Our script groups all the fires by the hour they happened. We can immediately see exactly when fire activity spiked during the day.
2. **How intense are they?** 
   It looks at the "FRP" (Fire Radiative Power), which measures how hot/intense the fire is burning. We calculate the average intensity, find the single most extreme fire of the day, and sum up the total thermal energy across the globe.
3. **Where are the busiest zones?**
   The Earth is huge. We placed an invisible "grid" over the entire planet (boxes roughly 11km x 11km). Our script counts the fires inside each box and ranks the top 5 worst hotspot zones. (It found massive hotspots in Texas and Russia!).
4. **Where are the massive continuous wildfires?**
   Instead of looking at arbitrary grid boxes, we used a Machine Learning algorithm called **DBSCAN**. We asked it: *"Find me groups of fires that are physically touching or extremely close to each other."* It successfully ignored all the isolated campfires and found **353 massive, contiguous wildfire clusters** across the globe. 

**How do we check this?** Right now, our Python script prints the results directly to our terminal window. Later on (in Phase 9), we will take these exact same calculations and hook them up to beautiful, interactive charts and maps on our React website!

---

## 👩‍💻 Technical Terms

We implemented the foundational analytics that will power the frontend dashboard components using `pandas` and `scikit-learn`.

### 1. Temporal Distribution (Fires Over Time)
*   **Action**: Loaded the dataset into Pandas via a SQL query.
*   **Aggregation**: Set the `timestamp` as a DatetimeIndex and used `.resample('h').size()` to bucket the detections into 1-hour intervals. 
*   **Why Pandas?**: Aggregating in Pandas makes our code database-agnostic, preventing SQL syntax breaks when we transition from SQLite to PostgreSQL (Supabase) in Phase 11.

### 2. Fire Intensity Metrics (FRP)
*   **Action**: Calculated summary statistics on the `frp` feature to derive intensity baselines.
*   **Results**: Identified a baseline global mean of `10.14 MW`, while pinpointing a severe anomaly maxing out at `403.93 MW`.

### 3. Geographic Concentration (Grid Cells)
*   **Action**: Spatial Binning.
*   **Implementation**: Rather than relying on heavy PostGIS extensions, we achieved a rapid ~11km x 11km spatial grid by rounding `latitude` and `longitude` to 1 decimal place (`0.1` degrees).
*   **Aggregation**: Used `groupby` to count the spatial density. The logic successfully identified grid `(32.9, -98.3)` as the densest cell with 367 simultaneous detections.

### 4. Contiguous Fire Clusters (Machine Learning: DBSCAN)
*   **Action**: Unsupervised Spatial Clustering.
*   **Implementation**: Used `sklearn.cluster.DBSCAN` to identify true contiguous fire events based on proximity, ignoring arbitrary grid boundaries.
*   **Hyperparameters**: 
    *   `metric='haversine'`: Essential for accurate distance calculations on a spherical globe.
    *   `eps=14/6371.0`: A strict 14km clustering radius, converted to radians for the Haversine formula.
    *   `min_samples=10`: Drops isolated anomalies (noise), ensuring we only flag substantial fire perimeters.
*   **Results**: Successfully resolved 23,000 disconnected points into **353 distinct wildfire clusters**, including a massive 1,039-detection mega-cluster in Northern Russia!

With our raw data now translated into spatial and temporal intelligence, Phase 3 is fully complete. Next up: building the predictive ML dataset (Phase 4).
