import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function Landing() {
  return (
    <div className="container py-24">
      <div className="mx-auto max-w-3xl text-center">
        <h1 className="text-4xl font-bold">The Global Standard for Semantic Intelligence</h1>
        <p className="mt-4 text-gray-400">Benchmark, evaluate, and monitor language models with scientific rigor.</p>
        <div className="mt-8">
          <Link href="/dashboard">
            <Button size="lg">Go to Dashboard</Button>
          </Link>
        </div>
        <div className="mt-12 grid grid-cols-1 gap-6 md:grid-cols-3">
          <div className="rounded-lg border border-gray-800 p-6">
            <div className="text-xl font-semibold">Benchmarks</div>
            <div className="mt-2 text-sm text-gray-400">SMF, WIF, CBF and more.</div>
          </div>
          <div className="rounded-lg border border-gray-800 p-6">
            <div className="text-xl font-semibold">Analytics</div>
            <div className="mt-2 text-sm text-gray-400">Scores, trends, and insights.</div>
          </div>
          <div className="rounded-lg border border-gray-800 p-6">
            <div className="text-xl font-semibold">Research</div>
            <div className="mt-2 text-sm text-gray-400">Studies and reports.</div>
          </div>
        </div>
        <div className="mt-12 text-sm text-gray-500">Latest Benchmark: Claude 3.5 scored 0.89 in Reflexivity</div>
      </div>
    </div>
  );
}
