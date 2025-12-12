import type { PropsWithChildren } from "react";
import { cn } from "@/lib/utils";

export function Card({ className, children }: PropsWithChildren<{ className?: string }>) {
  return <div className={cn("rounded-lg border border-gray-800 bg-background-lighter p-4", className)}>{children}</div>;
}

export function CardTitle({ children }: PropsWithChildren<{}>) {
  return <div className="mb-2 text-sm text-gray-400">{children}</div>;
}

export function CardValue({ children }: PropsWithChildren<{}>) {
  return <div className="text-2xl font-semibold">{children}</div>;
}
