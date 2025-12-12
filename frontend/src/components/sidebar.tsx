 "use client";
 import Link from "next/link";
 import { cn } from "@/lib/utils";
 import { Badge } from "@/components/ui/badge";

export function Sidebar() {
  return (
    <aside className={cn("flex h-screen w-64 flex-col border-r border-gray-800 bg-background-lighter p-4")}>
      <div className="mb-6 flex items-center gap-2">
        <div className="h-3 w-3 rounded-full bg-electric" />
        <span className="text-sm font-semibold">SemantIQ</span>
        <Badge className="ml-auto">v0.2</Badge>
      </div>
      <nav className="flex flex-col gap-2">
        <Link className="rounded-md px-3 py-2 hover:bg-gray-800" href="/dashboard">Dashboard</Link>
        <Link className="rounded-md px-3 py-2 hover:bg-gray-800" href="/runs">Runs</Link>
        <Link className="rounded-md px-3 py-2 hover:bg-gray-800" href="/benchmarks">Benchmarks</Link>
        <Link className="rounded-md px-3 py-2 hover:bg-gray-800" href="/settings">Settings</Link>
      </nav>
    </aside>
  );
}
