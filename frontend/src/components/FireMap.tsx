"use client";

import { useEffect, useState } from "react";
import { MapContainer, TileLayer, GeoJSON, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { fetchRiskGeoJSON, type RiskGeoJSON } from "@/lib/api";
import L from "leaflet";

function FitMapToGeoJSON({ geojson }: { geojson: RiskGeoJSON }) {
  const map = useMap();

  useEffect(() => {
    if (geojson.features.length > 0) {
      const layer = L.geoJSON(geojson);
      map.fitBounds(layer.getBounds().pad(0.1));
    }
  }, [geojson, map]);

  return null;
}

const RISK_OPACITY: Record<string, number> = {
  EXTREME: 0.65,
  HIGH: 0.55,
  ELEVATED: 0.45,
  MODERATE: 0.35,
  LOW: 0.25,
};

export default function FireMap() {
  const [geojson, setGeojson] = useState<RiskGeoJSON | null>(null);

  useEffect(() => {
    fetchRiskGeoJSON().then(setGeojson);
  }, []);

  return (
    <div className="relative h-full w-full border border-zinc-800 bg-zinc-900">
      <div className="absolute left-3 top-3 z-[1000] flex items-center gap-2 border border-zinc-800 bg-zinc-900/90 px-3 py-1.5 text-[10px] font-medium uppercase tracking-wider text-zinc-400 backdrop-blur-sm">
        Risk Grid Overlay
      </div>
      <div className="absolute right-3 top-3 z-[1000] flex flex-col gap-1 border border-zinc-800 bg-zinc-900/90 px-3 py-2 text-[10px] font-medium tracking-wider text-zinc-400 backdrop-blur-sm">
        <div className="mb-1 text-zinc-500">LEGEND</div>
        {[
          { label: "EXTREME", color: "#dc2626" },
          { label: "HIGH", color: "#f97316" },
          { label: "ELEVATED", color: "#eab308" },
          { label: "MODERATE", color: "#65a30d" },
          { label: "LOW", color: "#22c55e" },
        ].map(({ label, color }) => (
          <div key={label} className="flex items-center gap-2">
            <span
              className="inline-block h-2.5 w-2.5"
              style={{ backgroundColor: color }}
            />
            <span>{label}</span>
          </div>
        ))}
      </div>
      <MapContainer
        center={[40.0, -118.0]}
        zoom={5}
        className="h-full w-full"
        zoomControl={true}
        attributionControl={true}
      >
        <TileLayer
          url="https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}"
          attribution='Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ'
        />
        {geojson && (
          <>
            <FitMapToGeoJSON geojson={geojson} />
            <GeoJSON
              key={JSON.stringify(geojson.features.map((f) => f.properties.risk_category))}
              data={geojson}
              style={(feature) => ({
                fillColor: feature?.properties.color ?? "#666",
                fillOpacity: RISK_OPACITY[feature?.properties.risk_category] ?? 0.3,
                color: feature?.properties.color ?? "#666",
                weight: 1,
                opacity: 0.7,
              })}
              onEachFeature={(feature, layer) => {
                const p = feature.properties;
                layer.bindPopup(
                  `<div style="font-family:monospace;font-size:12px;color:#e4e4e7;background:#18181b;padding:8px;border:1px solid #27272a;">
                    <div style="font-weight:bold;margin-bottom:4px;">${p.region_name}</div>
                    <div>Risk: <span style="color:${p.color};font-weight:bold;">${p.risk_category}</span></div>
                    <div>Score: ${p.risk_score}%</div>
                  </div>`,
                  { className: "dark-popup" }
                );
              }}
            />
          </>
        )}
      </MapContainer>
    </div>
  );
}
