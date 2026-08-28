"use client";

import { useEffect, useState, useCallback } from "react";
import { AlertTriangle, Bell } from "lucide-react";
import { fetchAlerts, type AlertData } from "@/lib/api";

const SEVERITY_STYLES: Record<
  string,
  { border: string; icon: string; badge: string; badgeBg: string }
> = {
  EXTREME: {
    border: "border border-red-600 animate-pulse-border",
    icon: "text-red-500",
    badge: "text-red-400",
    badgeBg: "bg-red-500/10",
  },
  HIGH: {
    border: "border border-orange-500/60",
    icon: "text-orange-400",
    badge: "text-orange-400",
    badgeBg: "bg-orange-400/10",
  },
  ELEVATED: {
    border: "border border-yellow-500/40",
    icon: "text-yellow-400",
    badge: "text-yellow-400",
    badgeBg: "bg-yellow-400/10",
  },
  MODERATE: {
    border: "border border-lime-500/30",
    icon: "text-lime-400",
    badge: "text-lime-400",
    badgeBg: "bg-lime-400/10",
  },
  LOW: {
    border: "border border-green-500/20",
    icon: "text-green-500",
    badge: "text-green-500",
    badgeBg: "bg-green-500/10",
  },
};

function AlertCard({ alert }: { alert: AlertData }) {
  const style = SEVERITY_STYLES[alert.severity] ?? SEVERITY_STYLES.LOW;
  const reasonLines = alert.reasons.split("\n").filter(Boolean);

  return (
    <div className={`bg-zinc-900/80 p-3 ${style.border}`}>
      <div className="mb-2 flex items-start justify-between gap-2">
        <div className="flex items-center gap-2">
          <AlertTriangle className={`h-3.5 w-3.5 shrink-0 ${style.icon}`} />
          <span
            className={`text-[10px] font-semibold uppercase tracking-wider ${style.badge} ${style.badgeBg} px-1.5 py-0.5`}
          >
            {alert.severity}
          </span>
        </div>
        <span className="shrink-0 text-[10px] text-zinc-600 tabular-nums">
          {alert.timestamp?.slice(11, 16)}
        </span>
      </div>
      <p className="mb-1 text-xs font-medium text-zinc-300">{alert.message}</p>
      {reasonLines.length > 0 && (
        <ul className="mt-1.5 space-y-0.5">
          {reasonLines.map((line, i) => (
            <li
              key={i}
              className="flex items-start gap-1.5 text-[11px] text-zinc-500"
            >
              <span className="mt-1 inline-block h-1 w-1 shrink-0 rounded-full bg-zinc-600" />
              {line}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default function AlertPanel() {
  const [alerts, setAlerts] = useState<AlertData[]>([]);

  const load = useCallback(() => {
    fetchAlerts().then(setAlerts);
  }, []);

  useEffect(() => {
    load();
    const interval = setInterval(load, 30_000);
    return () => clearInterval(interval);
  }, [load]);

  const extremeCount = alerts.filter((a) => a.severity === "EXTREME").length;

  return (
    <div className="flex h-full flex-col border border-zinc-800 bg-zinc-950">
      <div className="flex items-center justify-between border-b border-zinc-800 px-4 py-3">
        <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wider text-zinc-500">
          <Bell className="h-3.5 w-3.5" />
          Active Alerts
        </div>
        <div className="flex items-center gap-2">
          {extremeCount > 0 && (
            <span className="text-[10px] font-semibold text-red-400">
              {extremeCount} EXTREME
            </span>
          )}
          <span className="text-[10px] text-zinc-600">
            {alerts.length} total
          </span>
        </div>
      </div>
      <div className="flex-1 space-y-px overflow-y-auto p-px">
        {alerts.length === 0 ? (
          <div className="flex h-full items-center justify-center text-xs text-zinc-600">
            No active alerts
          </div>
        ) : (
          alerts.map((alert) => (
            <AlertCard key={alert.id} alert={alert} />
          ))
        )}
      </div>
    </div>
  );
}
