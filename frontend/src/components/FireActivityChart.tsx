"use client";

import { useEffect, useState } from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { fetchFireHistory, type FireHistoryEntry } from "@/lib/api";

function CustomTooltip({
  active,
  payload,
  label,
}: {
  active?: boolean;
  payload?: Array<{ value: number }>;
  label?: string;
}) {
  if (!active || !payload?.length) return null;
  return (
    <div className="border border-zinc-800 bg-zinc-900 px-3 py-2 text-xs">
      <div className="text-zinc-500">{label}</div>
      <div className="font-semibold text-red-400">
        {payload[0].value.toLocaleString()} detections
      </div>
    </div>
  );
}

export default function FireActivityChart() {
  const [data, setData] = useState<FireHistoryEntry[]>([]);

  useEffect(() => {
    fetchFireHistory().then(setData);
  }, []);

  return (
    <div className="flex h-full flex-col border border-zinc-800 bg-zinc-900/50 p-4">
      <div className="mb-2 text-xs font-medium uppercase tracking-wider text-zinc-500">
        Fire Activity — 24h
      </div>
      <div className="min-h-0 flex-1">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart
            data={data}
            margin={{ top: 10, right: 30, left: 0, bottom: 30 }}
          >
            <defs>
              <linearGradient id="fireGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#dc2626" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#dc2626" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="#27272a"
              vertical={false}
            />
            <XAxis
              dataKey="hour"
              tick={{ fill: "#9ca3af", fontSize: 11 }}
              tickFormatter={(v: string) => v?.slice(11, 16) ?? ""}
              stroke="#3f3f46"
              tickLine={false}
              axisLine={false}
            />
            <YAxis
              tick={{ fill: "#9ca3af", fontSize: 11 }}
              stroke="#3f3f46"
              tickLine={false}
              axisLine={false}
            />
            <Tooltip content={<CustomTooltip />} />
            <Area
              type="monotone"
              dataKey="fire_count"
              stroke="#ef4444"
              strokeWidth={1.5}
              fill="url(#fireGradient)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
