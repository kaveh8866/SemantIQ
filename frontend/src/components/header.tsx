 "use client";
 import { Button } from "@/components/ui/button";
 import { cn } from "@/lib/utils";
 import { Search } from "lucide-react";
 import Link from "next/link";

export function Header() {
  return (
    <header className={cn("flex h-14 items-center border-b border-gray-800 px-4")}>
      <div className="flex w-full items-center gap-4">
        <div className="hidden md:block">
          <Link href="/dashboard" className="text-sm text-gray-400">Dashboard</Link>
        </div>
        <div className="ml-auto flex items-center gap-2">
          <div className="flex items-center gap-2 rounded-md border border-gray-700 px-2">
            <Search size={16} />
            <input className="bg-transparent text-sm outline-none" placeholder="Search" />
          </div>
          <Button variant="ghost">Profile</Button>
        </div>
      </div>
    </header>
  );
}
