"use client";
import { useState, type ChangeEvent } from "react";
import dynamic from "next/dynamic";

const MapboxBase = dynamic(() => import("@/components/maps/MapboxBase"), { ssr: false });

type Order = { id: number; lat: number; lon: number; demand: number; tw_start: number; tw_end: number; service_min: number }

export default function Page() {
  const [capacity, setCapacity] = useState(20);
  const [vehicles, setVehicles] = useState(3);
  const [mode, setMode] = useState("distance");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [depot, setDepot] = useState<[number, number] | null>(null);
  const [orders, setOrders] = useState<Order[] | null>(null);

  async function optimize() {
    setLoading(true);
    try {
      // Mock data around Pune for demo
      const d: [number, number] = [18.5204, 73.8567];
      const ords: Order[] = Array.from({ length: 15 }).map((_, i) => ({
        id: i + 1,
        lat: d[0] + (Math.random() - 0.5) * 0.18,
        lon: d[1] + (Math.random() - 0.5) * 0.18,
        demand: Math.random() < 0.7 ? 1 : 2,
        tw_start: 8 * 60,
        tw_end: 18 * 60,
        service_min: 10,
      }));
      const body = {
        depot: d,
        orders: ords,
        num_vehicles: vehicles,
        vehicle_capacity: capacity,
        speed_kmph: 30,
        mode,
      };
      const res = await fetch("/api/optimize", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
      const data = await res.json();
      setResult(data);
      setDepot(d);
      setOrders(ords);
    } finally {
      setLoading(false);
    }
  }

  async function downloadPdf() {
    if (!result || !depot || !orders) return;
    const res = await fetch('/api/route-plan/pdf', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ depot, orders, result }),
    });
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'route-plan.pdf';
    a.click();
    window.URL.revokeObjectURL(url);
  }

  async function sendToDriver() {
    if (!result || !depot || !orders) return;
    const res = await fetch('/api/route-plan/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ depot, orders, result }),
    });
    const data = await res.json();
    alert(`Dispatched (mock): ${data.dispatchId || 'ok'}`);
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-[380px,1fr] gap-6">
      <div className="card p-4 space-y-4">
        <h1 className="text-lg font-semibold">Route Planner</h1>
        <div className="space-y-2">
          <label className="text-sm text-textLabel">Vehicle Capacity</label>
          <input type="number" className="w-full border rounded-lg px-2 py-1" value={capacity} onChange={(e: ChangeEvent<HTMLInputElement>)=>setCapacity(parseInt(e.target.value||'0'))} />
        </div>
        <div className="space-y-2">
          <label className="text-sm text-textLabel">Number of Vehicles</label>
          <input type="number" className="w-full border rounded-lg px-2 py-1" value={vehicles} onChange={(e: ChangeEvent<HTMLInputElement>)=>setVehicles(parseInt(e.target.value||'0'))} />
        </div>
        <div className="space-y-2">
          <label className="text-sm text-textLabel">Optimization Mode</label>
          <select className="w-full border rounded-lg px-2 py-1" value={mode} onChange={(e)=>setMode(e.target.value)}>
            <option value="distance">Shortest Distance</option>
            <option value="fuel">Minimum Fuel Cost</option>
          </select>
        </div>
        <button onClick={optimize} disabled={loading} className="w-full py-2 rounded-lg bg-primary text-white">
          {loading ? 'Optimizing...' : 'Optimize Route'}
        </button>
        {result && (
          <div className="text-sm text-textLabel">
            <div>Total distance: <strong>{(result.total_distance_km||0).toFixed?.(1) ?? '—'} km</strong></div>
            <div>Total time: <strong>{(result.total_time_min||0).toFixed?.(0) ?? '—'} min</strong></div>
          </div>
        )}
        <div className="flex gap-2">
          <button onClick={downloadPdf} disabled={!result} className="flex-1 border rounded-lg px-3 py-2 disabled:opacity-50">Download Route Plan (PDF)</button>
          <button onClick={sendToDriver} disabled={!result} className="flex-1 border rounded-lg px-3 py-2 disabled:opacity-50">Send to Driver</button>
        </div>
      </div>
      <div className="card p-2" style={{ height: 520 }}>
        <MapboxBase />
      </div>
    </div>
  );
}
