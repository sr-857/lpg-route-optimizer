"use client";
import { useMemo } from "react";
import dynamic from "next/dynamic";
import MapboxBase from "@/components/maps/MapboxBase";

const { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, LineChart, Line, PieChart, Pie, Cell } = require("recharts");

export default function Page() {
  const barData = useMemo(() => Array.from({ length: 8 }).map((_, i) => ({ name: `TRK-${i+101}`, mins: 35 + Math.round(Math.random()*50) })), []);
  const lineData = useMemo(() => Array.from({ length: 12 }).map((_, i) => ({ week: `W${i+1}`, fuel: 200 + Math.round(Math.random()*80) })), []);
  const pieData = [
    { name: 'On Time', value: 72, color: '#66BB6A' },
    { name: 'Late', value: 22, color: '#F59E0B' },
    { name: 'Missed', value: 6, color: '#EF4444' },
  ];

  const heatmapData = useMemo(() => ({
    type: "FeatureCollection",
    features: Array.from({ length: 60 }).map(() => ({
      type: "Feature",
      properties: {
        weight: Math.random(),
      },
      geometry: {
        type: "Point",
        coordinates: [
          73.7 + Math.random() * 0.5,
          18.4 + Math.random() * 0.4,
        ],
      },
    })),
  }), []);

  return (
    <div className="space-y-6">
      <h1 className="text-lg font-semibold">Analytics</h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="rounded-xl shadow-card bg-white p-4">
          <div className="text-sm text-textLabel mb-2">Average Delivery Time per Vehicle</div>
          <div style={{ width: '100%', height: 260 }}>
            <ResponsiveContainer>
              <BarChart data={barData}>
                <XAxis dataKey="name" hide />
                <YAxis />
                <Tooltip />
                <Bar dataKey="mins" fill="#007AFF" radius={[6,6,0,0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div className="rounded-xl shadow-card bg-white p-4">
          <div className="text-sm text-textLabel mb-2">Fuel Consumption Trend (Weekly)</div>
          <div style={{ width: '100%', height: 260 }}>
            <ResponsiveContainer>
              <LineChart data={lineData}>
                <XAxis dataKey="week" />
                <YAxis />
                <Tooltip />
                <Line dataKey="fuel" stroke="#007AFF" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div className="rounded-xl shadow-card bg-white p-4">
          <div className="text-sm text-textLabel mb-2">Delivery Status Breakdown</div>
          <div style={{ width: '100%', height: 260 }}>
            <ResponsiveContainer>
              <PieChart>
                <Pie data={pieData} dataKey="value" nameKey="name" innerRadius={60} outerRadius={90}>
                  {pieData.map((entry: any, index: number) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div className="rounded-xl shadow-card bg-white p-4">
          <div className="text-sm text-textLabel mb-2">Delivery Density Heatmap</div>
          <div className="h-[260px]">
            <MapboxBase heatmapData={heatmapData as any} />
          </div>
        </div>
      </div>
    </div>
  );
}
