const API_BASE = "http://127.0.0.1:8001";

export interface AnalyticsData {
  total_fires: number;
  max_frp: number;
}

export interface FireHistoryEntry {
  hour: string;
  fire_count: number;
}

export interface AlertData {
  id: string;
  severity: "EXTREME" | "HIGH" | "ELEVATED" | "MODERATE" | "LOW";
  title: string;
  message: string;
  reasons: string;
  timestamp: string;
}

export interface RiskGeoJSON {
  type: "FeatureCollection";
  features: Array<{
    type: "Feature";
    geometry: {
      type: "Polygon";
      coordinates: number[][][];
    };
    properties: {
      risk_category: "LOW" | "MODERATE" | "ELEVATED" | "HIGH" | "EXTREME";
      color: string;
      region_name: string;
      risk_score: number;
    };
  }>;
}

const MOCK_ANALYTICS: AnalyticsData = {
  total_fires: 2841,
  max_frp: 403.9,
};

const MOCK_HISTORY: FireHistoryEntry[] = Array.from({ length: 24 }, (_, i) => {
  const base = 8500 + Math.sin(i / 3) * 2000;
  const noise = Math.floor(Math.random() * 400 - 200);
  const hour = new Date();
  hour.setHours(hour.getHours() - (23 - i), 0, 0, 0);
  return {
    hour: hour.toISOString().slice(0, 16).replace("T", " ") + ":00",
    fire_count: Math.max(0, Math.floor(base + noise)),
  };
});

function generateRiskGrid(): RiskGeoJSON {
  const categories: Array<{
    risk: RiskGeoJSON["features"][0]["properties"]["risk_category"];
    color: string;
    weight: number;
  }> = [
    { risk: "EXTREME", color: "#dc2626", weight: 5 },
    { risk: "HIGH", color: "#f97316", weight: 10 },
    { risk: "ELEVATED", color: "#eab308", weight: 15 },
    { risk: "MODERATE", color: "#65a30d", weight: 12 },
    { risk: "LOW", color: "#22c55e", weight: 8 },
  ];

  const riskScores: Record<string, number> = {
    EXTREME: 92,
    HIGH: 78,
    ELEVATED: 62,
    MODERATE: 45,
    LOW: 22,
  };

  const regions: Array<{ name: string; lat: number; lng: number }> = [
    { name: "Northern California", lat: 40.5, lng: -122.5 },
    { name: "Southern California", lat: 34.0, lng: -118.5 },
    { name: "Central Oregon", lat: 44.0, lng: -121.0 },
    { name: "Western Montana", lat: 46.8, lng: -114.0 },
    { name: "Northern Nevada", lat: 40.8, lng: -117.5 },
    { name: "Eastern Washington", lat: 47.5, lng: -118.0 },
    { name: "Southern Utah", lat: 38.2, lng: -112.5 },
    { name: "Northern Arizona", lat: 35.5, lng: -111.5 },
    { name: "Western Colorado", lat: 39.0, lng: -108.5 },
    { name: "Central Idaho", lat: 44.5, lng: -115.0 },
    { name: "Southeast Oregon", lat: 42.5, lng: -118.0 },
    { name: "Northern New Mexico", lat: 36.5, lng: -106.0 },
    { name: "Eastern California", lat: 37.5, lng: -118.0 },
    { name: "Southwest Wyoming", lat: 41.5, lng: -108.0 },
    { name: "Western Montana", lat: 47.5, lng: -115.5 },
    { name: "Southern Colorado", lat: 37.5, lng: -105.5 },
    { name: "Northwest Arizona", lat: 35.0, lng: -114.0 },
    { name: "Central California", lat: 36.5, lng: -119.5 },
    { name: "Eastern Oregon", lat: 43.5, lng: -117.5 },
    { name: "Northern California", lat: 41.5, lng: -121.5 },
    { name: "Western Nevada", lat: 39.5, lng: -120.0 },
    { name: "Southern Idaho", lat: 42.0, lng: -114.5 },
    { name: "Northeast California", lat: 41.0, lng: -120.5 },
    { name: "Southeast Arizona", lat: 33.0, lng: -110.5 },
    { name: "Central Montana", lat: 47.0, lng: -110.5 },
  ];

  const features: RiskGeoJSON["features"] = [];

  let idx = 0;
  for (const region of regions) {
    const totalWeight = categories.reduce((s, c) => s + c.weight, 0);
    let rand = Math.random() * totalWeight;
    let selected = categories[0];
    for (const cat of categories) {
      rand -= cat.weight;
      if (rand <= 0) {
        selected = cat;
        break;
      }
    }

    const offset = 0.8;
    const lat = region.lat + (Math.random() - 0.5) * 2;
    const lng = region.lng + (Math.random() - 0.5) * 2;
    const coords: number[][][] = [
      [
        [lng - offset, lat - offset],
        [lng + offset, lat - offset],
        [lng + offset, lat + offset],
        [lng - offset, lat + offset],
        [lng - offset, lat - offset],
      ],
    ];

    features.push({
      type: "Feature",
      geometry: { type: "Polygon", coordinates: coords },
      properties: {
        risk_category: selected.risk,
        color: selected.color,
        region_name: region.name,
        risk_score: riskScores[selected.risk] + Math.floor(Math.random() * 10 - 5),
      },
    });
    idx++;
  }

  return { type: "FeatureCollection", features };
}

const MOCK_RISK: RiskGeoJSON = generateRiskGrid();

export async function fetchAnalytics(): Promise<AnalyticsData> {
  try {
    const res = await fetch(`${API_BASE}/analytics`, { signal: AbortSignal.timeout(3000) });
    if (!res.ok) throw new Error("API error");
    return await res.json();
  } catch {
    return MOCK_ANALYTICS;
  }
}

export async function fetchFireHistory(): Promise<FireHistoryEntry[]> {
  try {
    const res = await fetch(`${API_BASE}/fires/history`, { signal: AbortSignal.timeout(3000) });
    if (!res.ok) throw new Error("API error");
    return await res.json();
  } catch {
    return MOCK_HISTORY;
  }
}

export async function fetchRiskGeoJSON(): Promise<RiskGeoJSON> {
  try {
    const res = await fetch(`${API_BASE}/risk`, { signal: AbortSignal.timeout(3000) });
    if (!res.ok) throw new Error("API error");
    return await res.json();
  } catch {
    return MOCK_RISK;
  }
}

const MOCK_ALERTS: AlertData[] = [
  {
    id: "alert-34.5--118.0",
    severity: "EXTREME",
    title: "EXTREME RISK ALERT",
    message:
      "Critical fire risk (84%) detected at coordinates 34.5, -118.0.",
    reasons: "7 active fire detections\nDangerously low humidity (12%)",
    timestamp: "2026-08-25 17:54:00",
  },
  {
    id: "alert-40.5--122.5",
    severity: "EXTREME",
    title: "EXTREME RISK ALERT",
    message:
      "Critical fire risk (91%) detected at coordinates 40.5, -122.5.",
    reasons: "12 active fire detections\nWind gusts exceeding 45 mph\nDry lightning forecast within 6 hours",
    timestamp: "2026-08-25 17:48:00",
  },
  {
    id: "alert-44.0--121.0",
    severity: "HIGH",
    title: "HIGH RISK WARNING",
    message:
      "Elevated fire risk (72%) detected at coordinates 44.0, -121.0.",
    reasons: "3 active fire detections\nRelative humidity below 20%",
    timestamp: "2026-08-25 17:41:00",
  },
  {
    id: "alert-38.2--112.5",
    severity: "HIGH",
    title: "HIGH RISK WARNING",
    message:
      "Elevated fire risk (68%) detected at coordinates 38.2, -112.5.",
    reasons: "5 active fire detections\nDrought index at extreme levels",
    timestamp: "2026-08-25 17:35:00",
  },
  {
    id: "alert-46.8--114.0",
    severity: "ELEVATED",
    title: "ELEVATED RISK NOTICE",
    message:
      "Moderate-high fire risk (55%) detected at coordinates 46.8, -114.0.",
    reasons: "2 active fire detections\nVegetation moisture content critically low",
    timestamp: "2026-08-25 17:22:00",
  },
  {
    id: "alert-39.0--108.5",
    severity: "ELEVATED",
    title: "ELEVATED RISK NOTICE",
    message:
      "Moderate-high fire risk (51%) detected at coordinates 39.0, -108.5.",
    reasons: "1 active fire detection\nTemperature anomaly detected via satellite",
    timestamp: "2026-08-25 17:10:00",
  },
];

export async function fetchAlerts(): Promise<AlertData[]> {
  try {
    const res = await fetch(`${API_BASE}/alerts`, { signal: AbortSignal.timeout(3000) });
    if (!res.ok) throw new Error("API error");
    return await res.json();
  } catch {
    return MOCK_ALERTS;
  }
}
