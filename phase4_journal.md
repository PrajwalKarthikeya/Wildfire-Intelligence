# Phase 4 Journey Journal: Building the ML Dataset

We can now look back at fires and analyze them (Phase 3), but the ultimate goal is to *predict* risk (Phase 5). To do that, we needed to build a proper Machine Learning dataset.

---

## 🧑‍🏫 Layman's Terms

A machine learning algorithm is like a student studying for an exam. You can't just give the student a list of fires and say "predict the next one." You have to give them a textbook filled with context.

In Phase 4, we built that textbook. We focused specifically on **California** to keep the project scoped perfectly.

1. **The Grid**: We sliced the state of California into 440 invisible grid boxes (each about 55km wide).
2. **The Fire Context**: We looked inside each of those 440 boxes and asked our database: *"How many fires happened here today, and how hot were they?"*
3. **The Weather Context**: We know fires don't happen in a vacuum. We built a bridge to a free weather service (Open-Meteo) and asked it for the exact temperature, humidity, wind speed, and rain happening inside *every single one* of our 440 grid boxes.

Now, instead of just raw fire data, we have a complete "profile" for every area in California. We can hand this profile to our ML model in Phase 5 and ask: *"Given this temperature, this humidity, and these recent fires... is this area at high risk tomorrow?"*

---

## 👩‍💻 Technical Terms

In Phase 4, we engineered the feature matrix (the independent variables, $X$) required for our supervised classification model.

### 1. Spatial Rasterization (The Grid)
*   **Action**: Created a uniform spatial grid bounding California (`Lat: 32.5 to 42.0`, `Lon: -124.5 to -114.0`).
*   **Implementation**: Used `numpy.arange` to generate 0.5-degree steps, then mapped them via a Pandas `MultiIndex.from_product` to create a Cartesian coordinate system of 440 cells. 
*   *Note: 0.5 degrees was chosen strategically over 0.1 degrees to minimize API rate-limiting during weather ingestion.*

### 2. Feature Engineering: Historical & Fire Metrics
*   **Action**: Mapped the Phase 2 database records into the grid.
*   **Transformations**: Grouped the raw coordinates into the 0.5-degree bins, then calculated:
    *   `fires_last_24h`: Count of active detections.
    *   `avg_frp` / `max_frp`: Radiant power aggregation.

### 3. Feature Engineering: Environmental Variables
*   **Action**: Ingested localized weather covariates.
*   **Implementation**: Used the Open-Meteo API. To avoid throttling, we constructed bulk API requests using string-concatenated coordinate lists (max 100 per request), chunking our 440 cells into 9 rapid, asynchronous-friendly batches.
*   **Features Extracted**: `temperature_c`, `humidity_percent`, `wind_speed_kmh`, `precipitation_mm`.

### The Result
We successfully merged the spatial, thermal, and meteorological data into a finalized target feature vector (`data/ml_features.csv`). 

```text
[grid_lat, grid_lon, fires_last_24h, avg_frp, max_frp, temperature_c, humidity_percent, precipitation_mm, wind_speed_kmh]
```
Of the 440 generated cells, 21 currently exhibit active fires. This provides exactly the labeled target distribution we need to proceed to Phase 5.
