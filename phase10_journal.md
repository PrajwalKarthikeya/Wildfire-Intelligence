# Phase 10 Journey Journal: In-App Alerts

A dashboard is great if someone is actively staring at it, but a true intelligence system needs to proactively warn you when things go wrong.

---

## 🧑‍🏫 Layman's Terms

Instead of forcing the user to click around the map trying to find dangerous areas, we built a security alarm.

Our backend now automatically scans the machine learning predictions. If it finds any zone where the risk of fire jumps dangerously high (above 60%), it automatically generates a text alert explaining exactly *why* the AI is worried.

For example, it won't just say "High Risk." It will say:
> "High Risk because there are 7 active fires burning right now, and the humidity just dropped to 12%."

We then updated Open Code with a prompt to build an "Alerts Sidebar" directly into our frontend dashboard so these warnings blink on the screen automatically!

---

## 👩‍💻 Technical Terms

Phase 10 focused on building an actionable notification layer on top of our probabilistic inference.

### Step 1: The Alert Generation Engine
*   **Action**: Authored a new `GET /alerts` endpoint in `backend/main.py`.
*   **Logic**: The endpoint reads the latest `california_risk_predictions.csv`. It filters out the noise by applying a hard threshold (`risk_score >= 0.6`).
*   **Dynamic Reason Extraction**: Rather than static text, the endpoint inspects the underlying feature vector of each high-risk cell. If `humidity_percent < 30`, it appends a specific warning about dry conditions. If `wind_speed_kmh > 20`, it flags the wind vector. This creates highly interpretable, explainable AI alerts.

### Step 2: Bridging to the UI
*   **Action**: Authored `open_code_prompt_alerts.md`.
*   **Implementation**: Instructed the Open Code assistant to query the new `/alerts` endpoint and dynamically render the JSON array into a dedicated notification sidebar, adhering strictly to the established dark-mode UI aesthetic.

Phase 10 is complete! We now have a fully functional, AI-driven, alerting intelligence platform.
