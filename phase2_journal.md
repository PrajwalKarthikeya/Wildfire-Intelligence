# Phase 2 Journey Journal: The Database

Our vacuum cleaner (Phase 1) collected a ton of data, but vacuum bags fill up, and it's hard to search through them. We needed a permanent home for our data so we can eventually start recognizing historical patterns. 

Enter Phase 2: **The Database**.

---

## 🧑‍🏫 Layman's Terms

Imagine you're trying to figure out which neighborhood is most likely to have a house fire. You can't just look at *today's* fires; you need to look at fires from last week, last month, and last year to see a pattern. 

In Phase 1, we got the data, but it was just living in a temporary spreadsheet. If we wanted to look at yesterday's fires, we'd have to go find yesterday's spreadsheet.

In Phase 2, we built a digital filing cabinet (a relational database). 
1. We designed specific "drawers" (tables) for exactly what we need: one for actual fire detections, one for our future risk predictions, and one to keep track of our AI models.
2. We made sure every single piece of information from our clean NASA spreadsheet was carefully filed into the right drawer.
3. We set it up so that when we deploy our app to the internet, we can just flip a switch to move our filing cabinet from our local computer to the cloud (Supabase) without rewriting any code.

Now our app has a memory! It remembers every fire it has ever seen.

---

## 👩‍💻 Technical Terms

In Phase 2, we established the persistence layer of our architecture. We chose an Object-Relational Mapping (ORM) approach using **SQLAlchemy** to abstract away raw SQL, allowing us to interact with our database using Python objects and easily swap out our SQL dialect later.

### Step 1: Defining the Data Models
*   **Action**: Created `database.py` and defined our database schema using SQLAlchemy's `declarative_base`.
*   **Schemas Defined**:
    *   `FireDetection`: The core table storing `latitude`, `longitude`, `timestamp`, `frp` (Fire Radiative Power), and `confidence`. We set `id` (the MD5 hash from Phase 1) as the primary key to ensure idempotency.
    *   `RiskPrediction`: A table prepared for Phase 6 to store ML outputs (`risk_score`, `risk_level`, `model_version`) mapped to geographic cells.
    *   `ModelRun`: A table to track model training metadata, ensuring reproducibility (MLOps best practices).

### Step 2: Database Initialization
*   **Action**: Used `create_engine` to connect to our database.
*   **Strategic Decision**: We configured the `DATABASE_URL` via environment variables, defaulting to a local SQLite database (`sqlite:///data/wildfire.db`). This allows for frictionless local development without requiring a local PostgreSQL server. When we move to production (Phase 11), we simply inject a Supabase PostgreSQL connection string into `.env`, and SQLAlchemy seamlessly handles the transition.

### Step 3: Data Ingestion
*   **Action**: Wrote `load_data.py` to bridge Phase 1 and Phase 2.
*   **Details**: 
    1. Read the normalized `clean_fires.csv` using Pandas.
    2. Parsed timestamps back into Python `datetime` objects.
    3. Queried the database for existing `fire_id`s to prevent Duplicate Key constraints. (We encountered a bug with pandas `dtype` evaluation of strings, but successfully mitigated it with safe type casting during ingestion).
    4. Performed a `bulk_save_objects()` insertion, committing all ~23,000 global detections into the SQLite database in a single transaction for high performance.

### The Result
We now have a persistent, structured, queryable datastore (`data/wildfire.db`) containing 22,970 historical fire records, fully decoupled from the raw data pipeline. We are ready to start running spatial and historical analytics on this database in Phase 3.
