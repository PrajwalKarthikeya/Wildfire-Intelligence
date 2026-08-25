# Prompt for Open Code

**Copy and paste the exact text below into Open Code to generate the frontend dashboard:**

***

You are building a production-grade, near-real-time "Wildfire Intelligence" dashboard.

### Tech Stack
*   Next.js (React)
*   Tailwind CSS (for styling)
*   Recharts (for the analytics charts)
*   React-Leaflet (for the interactive map)
*   Lucide React (for minimalist iconography)

### Design Aesthetic
*   **Vibe**: Military/Satellite Intelligence Platform.
*   **Colors**: Strictly Dark UI (slate/zinc/black backgrounds). Use high-contrast accents only for data (e.g., Red for Extreme risk, Orange for High, Yellow for Moderate, Green for Low).
*   **Style**: Minimalist, technical, flat. No rounded corners everywhere, no heavy drop shadows, no gradients, and absolutely no cheesy "AI powered 🔥" emojis. It must look like a serious, professional decision-support system used by a government agency.

### Layout / Wireframe
Please construct the UI exactly matching this layout structure:

1. **Header**: 
   *   Left: "🛰️ WILDFIRE INTELLIGENCE"
   *   Right: A blinking red dot indicating "● LIVE" status.

2. **Top Row (KPI Stats)**: 
   4 equal-width metric cards side-by-side:
   *   Total Active Fires (e.g., 2,841)
   *   High Risk Zones (e.g., 183)
   *   Max Model Risk (e.g., 74%)
   *   24h Change (e.g., +18%)

3. **Middle Row (The Map)**:
   *   A massive, full-width interactive map component (using React-Leaflet).
   *   The map should use a dark theme (like CARTO Dark Matter: `https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png`).
   *   It should render GeoJSON polygons representing risk grids (colored by severity).

4. **Bottom Row (Analytics)**:
   *   Split 50/50.
   *   Left side: A `Recharts` AreaChart showing "Fire Activity" (detections over the last 24 hours).
   *   Right side: A table or list showing "High-Risk Regions" (e.g., Northern California - 87%).

### Data Integration (API)
The UI should be built to fetch data from a local FastAPI backend running on `http://127.0.0.1:8001`. Please mock the API calls using `useEffect` or `react-query` but provide realistic fallback dummy data so the UI renders beautifully even if the backend is offline. 

The API endpoints you should expect to call are:
*   `GET http://127.0.0.1:8001/analytics` (Returns `{ total_fires: 2841, max_frp: 403.9 }`)
*   `GET http://127.0.0.1:8001/fires/history` (Returns array of `{ hour: "2026-08-25 06:00:00", fire_count: 8587 }` for Recharts)
*   `GET http://127.0.0.1:8001/risk` (Returns a GeoJSON FeatureCollection containing polygons with `properties.risk_category` ("LOW", "MODERATE", "ELEVATED", "HIGH", "EXTREME") and `properties.color` for Leaflet).

Please output the complete, functional Next.js/React component for this dashboard.
