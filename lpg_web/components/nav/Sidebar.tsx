"use client";
import Link from "next/link";
import { Gauge, Map, Navigation2, Activity, Settings, LifeBuoy } from "lucide-react";
import { usePathname } from "next/navigation";

const items = [
  { href: "/", label: "Dashboard", icon: Gauge },
  { href: "/route-planner", label: "Route Planner", icon: Navigation2 },
  { href: "/live-tracking", label: "Live Tracking", icon: Map },
  { href: "/analytics", label: "Analytics", icon: Activity },
  { href: "/admin", label: "Admin Panel", icon: Settings },
  { href: "/support", label: "Support", icon: LifeBuoy },
];

export function Sidebar() {
  const pathname = usePathname();
  return (
    <aside className="h-[calc(100vh-56px)] sticky top-14 border-r border-neutral-800 bg-black text-white dark:bg-black">
      <nav className="flex flex-col p-3 gap-1 w-[260px]">
        {items.map(({ href, label, icon: Icon }) => {
          const active = pathname === href;
          return (
            <Link
              key={href}
              href={href}
              className={`flex items-center gap-2 px-3 py-2 rounded-xl text-sm text-white hover:bg-neutral-800 ${
                active ? "bg-neutral-800" : ""
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{label}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
