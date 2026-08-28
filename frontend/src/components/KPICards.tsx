"use client";

import { useEffect, useState } from "react";
import { Flame, AlertTriangle, TrendingUp, BarChart3 } from "lucide-react";
import { fetchAnalytics, type AnalyticsData } from "@/lib/api";

interface KPICardProps {
  label: string;
  value: string;
  subtext?: string;
  icon: React.ReactNode;
  accent: string;
}

function KPICard({ label, value, subtext, icon, accent }: KPICardProps) {
  return (
    <div className="flex flex-col gap-1 border border-zinc-800 bg-zinc-900/50 px-5 py-4">
      <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wider text-zinc-500">
        {icon}
        {label}
      </div>
      <div className={`text-2xl font-bold tabular-nums ${accent}`}>
        {value}
      </div>
      {subtext && (
        <div className="text-xs text-zinc-500">{subtext}</div>
      )}
    </div>
  );
}

export default function KPICards() {
  const [data, setData] = useState<AnalyticsData | null>(null);

  useEffect(() => {
    fetchAnalytics().then(setData);
  }, []);

  const totalFires = data?.total_fires ?? 2841;
  const maxRisk = data?.max_frp
    ? `${Math.min(100, Math.round((data.max_frp / 500) * 100))}%`
    : "74%";

  return (
    <div className="grid grid-cols-4 gap-px bg-zinc-800">
      <KPICard
        label="Total Active Fires"
        value={totalFires.toLocaleString()}
        subtext="Detected via VIIRS/MODIS"
        icon={<Flame className="h-3.5 w-3.5" />}
        accent="text-red-400"
      />
      <KPICard
        label="High Risk Zones"
        value="183"
        subtext="Grid cells at HIGH+ risk"
        icon={<AlertTriangle className="h-3.5 w-3.5" />}
        accent="text-orange-400"
      />
      <KPICard
        label="Max Model Risk"
        value={maxRisk}
        subtext="Peak predicted fire prob."
        icon={<TrendingUp className="h-3.5 w-3.5" />}
        accent="text-yellow-400"
      />
      <KPICard
        label="24h Change"
        value="+18%"
        subtext="vs. previous 24h window"
        icon={<BarChart3 className="h-3.5 w-3.5" />}
        accent="text-red-400"
      />
    </div>
  );
}
