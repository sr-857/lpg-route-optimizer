"use client";
import { useEffect, useRef } from "react";

export default function MapboxBase() {
  const ref = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const token = process.env.NEXT_PUBLIC_MAPBOX_TOKEN || process.env.MAPBOX_TOKEN;
    if (!token) return; // no-op if no token; page shows placeholder

    (async () => {
      const mapboxgl = (await import("mapbox-gl")).default;
      (mapboxgl as any).accessToken = token as string;
      const map = new mapboxgl.Map({
        container: ref.current!,
        style: "mapbox://styles/mapbox/streets-v12",
        center: [73.8567, 18.5204],
        zoom: 10,
      });
      return () => map.remove();
    })();
  }, []);

  return (
    <div className="w-full h-full relative">
      <div ref={ref} className="absolute inset-0 rounded-xl" />
      <div className="absolute inset-0 flex items-center justify-center text-textLabel">
        <div className="bg-white/70 backdrop-blur rounded-xl px-3 py-1 text-sm">
          Map placeholder — set MAPBOX token to render
        </div>
      </div>
    </div>
  );
}
