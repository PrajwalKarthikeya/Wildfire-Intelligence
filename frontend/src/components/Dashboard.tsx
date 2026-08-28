"use client";

import dynamic from "next/dynamic";
import Header from "@/components/Header";
import KPICards from "@/components/KPICards";
import FireActivityChart from "@/components/FireActivityChart";
import RiskRegionsTable from "@/components/RiskRegionsTable";
import AlertPanel from "@/components/AlertPanel";

const FireMap = dynamic(() => import("@/components/FireMap"), {
  ssr: false,
  loading: () => (
    <div className="flex h-full w-full items-center justify-center border border-zinc-800 bg-zinc-900">
      <div className="text-xs uppercase tracking-wider text-zinc-600">
        Loading map...
      </div>
    </div>
  ),
});

export default function Dashboard() {
  return (
    <div className="flex h-screen flex-col overflow-hidden bg-zinc-950">
      <Header />
      <div className="flex min-h-0 flex-1 gap-px bg-zinc-800">
        <div className="flex min-h-0 min-w-0 flex-1 flex-col gap-px">
          <KPICards />
          <div className="min-h-0 flex-1">
            <FireMap />
          </div>
          <div className="grid h-72 grid-cols-2 gap-px">
            <FireActivityChart />
            <RiskRegionsTable />
          </div>
        </div>
        <div className="w-80 shrink-0">
          <AlertPanel />
        </div>
      </div>
    </div>
  );
}
