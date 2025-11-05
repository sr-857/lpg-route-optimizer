"use client";
import { Bell, Search, SunMoon, User } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

export function TopNav() {
  const [q, setQ] = useState("");
  return (
    <header className="w-full border-b bg-white dark:bg-neutral-900">
      <div className="mx-auto max-w-[1400px] px-4 h-14 flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <Link href="/" className="font-semibold text-textTitle dark:text-white">LPG RouteX</Link>
        </div>
        <div className="flex-1 max-w-xl hidden md:flex items-center bg-white dark:bg-neutral-800 rounded-xl border px-3 py-1">
          <Search className="w-4 h-4 text-textLabel" />
          <input
            className="flex-1 bg-transparent outline-none px-2 text-sm"
            placeholder="Search vehicles, routes, orders..."
            value={q}
            onChange={(e) => setQ(e.target.value)}
          />
        </div>
        <div className="flex items-center gap-3">
          <button className="relative p-2 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-800">
            <Bell className="w-5 h-5" />
            <span className="absolute -top-1 -right-1 bg-primary text-white text-[10px] rounded-full px-1">3</span>
          </button>
          <button className="p-2 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-800" aria-label="Toggle theme">
            <SunMoon className="w-5 h-5" />
          </button>
          <div className="relative">
            <button className="flex items-center gap-2 px-2 py-1 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-800">
              <User className="w-5 h-5" />
              <span className="hidden sm:inline text-sm">Admin</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
