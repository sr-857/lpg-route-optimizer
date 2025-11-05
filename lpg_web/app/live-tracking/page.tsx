"use client";
import dynamic from "next/dynamic";

const MapboxBase = dynamic(() => import("@/components/maps/MapboxBase"), { ssr: false });

export default function Page() {
  return (
    <div className="space-y-4">
      <h1 className="text-lg font-semibold">Live Tracking</h1>
      <div className="grid grid-cols-1 lg:grid-cols-[320px,1fr] gap-6">
        <aside className="card p-3">
          <div className="text-sm text-textLabel mb-2">Active Vehicles</div>
          <ul className="space-y-2 text-sm">
            {Array.from({ length: 8 }).map((_, i) => (
              <li key={i} className="flex items-center justify-between">
                <span>TRK-{100 + i}</span>
                <span className="text-green-600">On Route</span>
              </li>
            ))}
          </ul>
          <button className="mt-4 w-full border rounded-lg px-3 py-2">Recalculate Route</button>
        </aside>
        <div className="card p-2" style={{ height: 520 }}>
          <MapboxBase />
        </div>
      </div>
    </div>
  );
}
