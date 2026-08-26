# Phase 1 Journey Journal: The Data Pipeline

Welcome to our project diary! In Phase 1, we successfully built the foundation of our Wildfire Intelligence system: **The Data Pipeline**.

Without data, our machine learning models and shiny dashboards are useless. Let's break down exactly what we accomplished.

---

## 🧑‍🏫 Layman's Terms (The "What did we do?" version)

Imagine trying to predict where the next big fire is going to happen, but you have no idea where current fires are burning. 

NASA has satellites orbiting the Earth right now, taking pictures and detecting intense heat signatures (fires!). However, they provide this data in a massive, messy, raw spreadsheet format.

In Phase 1, we built an automated "messenger" (our Python script) that:
1. Knocks on NASA's digital door using a secret password (the `MAP_KEY`).
2. Asks for the last 24 hours of fire detections across the entire globe.
3. Takes NASA's messy spreadsheet and carefully organizes it. It throws away invalid data, combines dates and times into a single readable clock, and translates confusing satellite codes into a standard language we can understand.
4. Gives every single fire its own unique ID.
5. Saves this clean, organized list into a neat file on our computer so we can use it later.

We basically built a vacuum cleaner that sucks up raw space data and spits out a pristine list of global fires!

---

## 👩‍💻 Technical Terms (The "How did we do it?" version)

From an engineering perspective, Phase 1 focused on building a robust ETL (Extract, Transform, Load) pipeline using Python.

### Step 1: Authentication & Security
*   **Action**: Registered for the NASA FIRMS API and obtained a `MAP_KEY`.
*   **Security**: Stored the key in a local `.env` file and immediately added it to `.gitignore`. This ensures we never leak credentials to GitHub.

### Step 2: Data Extraction (Ingestion)
*   **Action**: Wrote `fetch_fires.py` using the `requests` library to interface with the FIRMS API.
*   **Details**: We hit the `/api/area/csv` endpoint for the `VIIRS_SNPP_NRT` (Suomi-NPP) sensor, requesting a 1-day global bounding box. The API returns CSV data in the response body.
*   **Parsing**: We used `io.StringIO` to read the raw HTTP response directly into a `pandas.DataFrame` in memory, avoiding unnecessary disk writes for the raw file.

### Step 3: Understanding the Data (Exploratory Data Analysis)
*   **Action**: Analyzed the raw VIIRS schema.
*   **Findings**: We identified key features:
    *   `latitude` / `longitude`: Spatial coordinates.
    *   `acq_date` / `acq_time`: Temporal data, split into a string date and an integer time (e.g., `1342` for 13:42).
    *   `frp` (Fire Radiative Power): The radiant energy of the fire, crucial for determining intensity rather than just presence.
    *   `confidence`: A string value (`'l'`, `'n'`, `'h'`) for VIIRS, which differs from MODIS (which uses a 0-100 percentage).

### Step 4: Data Transformation & Normalization (Cleaning)
*   **Action**: Built the `clean_and_normalize(df)` function to standardize the schema.
*   **Transformations applied**:
    1.  **Dropped NaNs**: Removed rows missing critical spatial/temporal features.
    2.  **Spatial filtering**: Bounded latitude `[-90, 90]` and longitude `[-180, 180]` to prevent geographic anomalies.
    3.  **Temporal joining**: Zero-padded the `acq_time` integer to 4 characters, concatenated it with `acq_date`, and parsed it into a true Pandas `datetime64` object.
    4.  **Schema Normalization**: Mapped VIIRS-specific columns (like `bright_ti4`) to generic names (`brightness`). Translated VIIRS string confidence (`'l', 'n', 'h'`) into a 0-100 integer scale (`30, 70, 100`) so it will be compatible if we ever ingest MODIS data.
    5.  **Unique Keys**: Generated a deterministic `fire_id` using an MD5 hash of the coordinates, timestamp, and satellite. This allows us to deduplicate safely.

### The Result
We converted a raw, multi-format CSV stream into a clean, normalized schema:
`[fire_id, latitude, longitude, timestamp, satellite, brightness, frp, confidence, daynight]`

The clean data is saved locally to `data/clean_fires.csv`, perfectly setting the stage for Phase 2: PostgreSQL Database integration.
