### Phase 10: Alert Panel Update

**Copy and paste this into Open Code to add the Phase 10 Alerts feature:**

***

We need to add a "Live Alerts" panel to our dashboard. 

The backend has just exposed a new endpoint: `GET http://127.0.0.1:8001/alerts`

This endpoint returns an array of JSON objects that look exactly like this:
```json
{
    "id": "alert-34.5--118.0",
    "severity": "EXTREME",
    "title": "⚠ EXTREME RISK ALERT",
    "message": "Critical fire risk (84%) detected at coordinates 34.5, -118.0.",
    "reasons": "• 7 active fire detections\n• Dangerously low humidity (12%)",
    "timestamp": "2026-08-25 17:54:00"
}
```

Please update the React dashboard UI to include an **"Active Alerts" sidebar** or a **notification drawer** on the right side of the screen.

**Styling Requirements:**
1. Stick to the dark military/satellite aesthetic.
2. If `severity === "EXTREME"`, give the alert card a subtle pulsing red border or a red warning icon. 
3. Display the `title`, `message`, and `timestamp`.
4. Render the `reasons` string exactly as formatted (it contains literal `\n` characters, so render them as separate lines or bullet points).

Ensure the frontend fetches this endpoint periodically (or alongside the other data) and dynamically renders the alert cards!
