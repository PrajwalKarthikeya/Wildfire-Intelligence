"use client";

import { Radio } from "lucide-react";

export default function Header() {
  return (
    <header className="flex items-center justify-between border-b border-zinc-800 bg-zinc-950 px-6 py-3">
      <div className="flex items-center gap-3">
        <span className="text-lg font-semibold tracking-tight text-zinc-100">
          SATELLITE WILDFIRE INTELLIGENCE
        </span>
      </div>
      <div className="flex items-center gap-2 text-xs font-medium tracking-wider text-zinc-400">
        <span className="relative flex h-2 w-2">
          <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-red-500 opacity-75" />
          <span className="relative inline-flex h-2 w-2 rounded-full bg-red-500" />
        </span>
        LIVE
      </div>
    </header>
  );
}
