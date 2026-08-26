# Phase 8 Journey Journal: The Live Heartbeat

Up until now, our data pipeline, database, machine learning model, and backend API were just individual puzzle pieces that we were running manually. In Phase 8, we connected them all together and gave the system a pulse.

---

## 🧑‍🏫 Layman's Terms

Imagine you build a beautiful clock, but you have to manually turn the gears with your finger every time you want to know what time it is. That's essentially what our project was up to this point.

In Phase 8, we built the automated motor for our clock. 

We wrote a "Heartbeat" script that wakes up exactly once every 15 minutes and performs the following sequence completely on its own:
1. Reaches out to NASA to ask if there are any brand new fires right now.
2. Carefully files those new fires into our database.
3. Checks the Open-Meteo weather service for any sudden drops in humidity or spikes in wind.
4. Feeds all that new data into our Gradient Boosting AI model.
5. Re-draws the entire California risk map.

Now, our API and our Dashboard are truly "Near-Real-Time." You don't have to push any buttons. The system just thinks and updates itself indefinitely. 

---

## 👩‍💻 Technical Terms

The roadmap advised against overengineering this. While enterprise systems might use Kafka, Airflow, or Kubernetes CronJobs for this, our MVP required a lightweight, robust orchestration approach.

### Step 1: Sequential Process Orchestration
*   **Action**: Created `refresh_pipeline.py`.
*   **Implementation**: Used Python's `subprocess` module to orchestrate the execution of our modular scripts sequentially. By strictly ordering the operations, we guarantee data consistency:
    `Extraction (fetch) -> Persistence (load) -> Feature Engineering (builder) -> Inference (model) -> Spatial Serialization (map)`
*   **Error Handling**: If a NASA API rate limit is hit or Open-Meteo times out, the `subprocess.run()` error handler catches the exception, halting the sequence safely without corrupting downstream artifacts (like the GeoJSON).

### Step 2: The Daemon Loop
*   **Action**: Implemented an infinite execution loop with `time.sleep(900)` (15 minutes).
*   **Why 15 Minutes?**: FIRMS global NRT data is generally updated within a 3-hour latency window. However, FIRMS US/Canada Real-Time (RT) and Ultra-Real-Time (URT) services can populate much faster (within 60 minutes or less of overpass). A 15-minute polling interval ensures we capture the URT anomalies for California as soon as NASA publishes them, while remaining well beneath the 5,000 requests/10-minute API throttling threshold.

### The Result
The system is now fully automated. We have transitioned from static analytical scripts into a true **continuous intelligence pipeline**. Phase 8 is complete, and the stage is set for the final major piece of the architecture: The Next.js React Dashboard (Phase 9).
