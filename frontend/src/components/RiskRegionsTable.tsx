"use client";

import { useEffect, useState } from "react";
import { fetchRiskGeoJSON, type RiskGeoJSON } from "@/lib/api";

const RISK_COLORS: Record<string, string> = {
  EXTREME: "text-red-500",
  HIGH: "text-orange-400",
  ELEVATED: "text-yellow-400",
  MODERATE: "text-lime-500",
  LOW: "text-green-500",
};

const RISK_BG: Record<string, string> = {
  EXTREME: "bg-red-500/10",
  HIGH: "bg-orange-400/10",
  ELEVATED: "bg-yellow-400/10",
  MODERATE: "bg-lime-500/10",
  LOW: "bg-green-500/10",
};

export default function RiskRegionsTable() {
  const [geojson, setGeojson] = useState<RiskGeoJSON | null>(null);

  useEffect(() => {
    fetchRiskGeoJSON().then(setGeojson);
  }, []);

  const regions = (geojson?.features ?? [])
    .map((f) => ({
      name: f.properties.region_name,
      risk: f.properties.risk_category,
      score: f.properties.risk_score,
      color: f.properties.color,
    }))
    .sort((a, b) => {
      const order = { EXTREME: 5, HIGH: 4, ELEVATED: 3, MODERATE: 2, LOW: 1 };
      return (order[b.risk] ?? 0) - (order[a.risk] ?? 0);
    });

  return (
    <div className="flex h-full flex-col border border-zinc-800 bg-zinc-900/50 p-4">
      <div className="mb-4 text-xs font-medium uppercase tracking-wider text-zinc-500">
        High-Risk Regions
      </div>
      <div className="flex-1 overflow-y-auto">
        <table className="w-full text-left text-xs">
          <thead>
            <tr className="border-b border-zinc-800 text-zinc-500">
              <th className="pb-2 font-medium">Region</th>
              <th className="pb-2 font-medium">Risk</th>
              <th className="pb-2 text-right font-medium">Score</th>
            </tr>
          </thead>
          <tbody>
            {regions.map((r, i) => (
              <tr
                key={`${r.name}-${i}`}
                className="border-b border-zinc-800/50 hover:bg-zinc-800/30"
              >
                <td className="py-2 text-zinc-300">{r.name}</td>
                <td className="py-2">
                  <span
                    className={`inline-block px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-wider ${RISK_COLORS[r.risk] ?? "text-zinc-400"} ${RISK_BG[r.risk] ?? "bg-zinc-800"}`}
                  >
                    {r.risk}
                  </span>
                </td>
                <td className="py-2 text-right tabular-nums text-zinc-300">
                  {r.score}%
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
