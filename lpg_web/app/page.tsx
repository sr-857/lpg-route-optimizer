import { Gauge, Truck, TrendingUp, Wallet } from "lucide-react";
import dynamic from "next/dynamic";

const MapboxBase = dynamic(() => import("@/components/maps/MapboxBase"), { ssr: false });

function MetricCard({ title, value, sub }: { title: string; value: string; sub?: string }) {
  return (
    <div className="card hover-card p-4">
      <div className="text-textLabel text-xs">{title}</div>
      <div className="text-2xl font-semibold mt-1">{value}</div>
      {sub && <div className="text-xs text-textLabel mt-1">{sub}</div>}
    </div>
  );
}

export default function Page() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">Today’s Overview</h1>
        <div className="flex gap-2">
          <input type="date" className="border rounded-lg px-2 py-1 text-sm" />
          <button className="px-3 py-1 rounded-lg bg-primary text-white text-sm">Refresh</button>
        </div>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard title="Total Deliveries" value="128" sub="+6 vs yesterday" />
        <MetricCard title="Active Vehicles" value="12" sub="• On track" />
        <MetricCard title="Avg Route Efficiency" value="87%" sub="Progress vs baseline" />
        <MetricCard title="Fuel Cost (₹)" value="42,350" sub="-3% vs yesterday" />
      </div>
      <div className="card p-2" style={{ height: 420 }}>
        <MapboxBase />
      </div>
      <div className="card p-0 overflow-auto">
        <table className="w-full text-sm">
          <thead className="bg-gray-50">
            <tr>
              <th className="text-left p-3">Vehicle ID</th>
              <th className="text-left p-3">Driver</th>
              <th className="text-left p-3">Route ID</th>
              <th className="text-left p-3">Status</th>
              <th className="text-left p-3">ETA</th>
              <th className="text-left p-3">Delay reason</th>
            </tr>
          </thead>
          <tbody>
            {Array.from({ length: 8 }).map((_, i) => (
              <tr key={i} className="border-t">
                <td className="p-3">TRK-{100 + i}</td>
                <td className="p-3">Driver {i + 1}</td>
                <td className="p-3">R-{200 + i}</td>
                <td className="p-3">On Route</td>
                <td className="p-3">{12 + i}:30</td>
                <td className="p-3">—</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
