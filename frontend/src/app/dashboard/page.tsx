import { Card, CardTitle, CardValue } from "@/components/ui/card";
import { ScoreTrend } from "@/components/charts/line";
import { listRuns } from "@/lib/api";

export default async function Dashboard() {
  const runs = await listRuns().catch(() => []);
  const totalRuns = Array.isArray(runs) ? runs.length : 0;
  const modelsEvaluated = Array.isArray(runs) ? new Set(runs.map((r: any) => r.model_name)).size : 0;
  const chartData = [
    { date: "2025-01-01", gpt4: 0.82, gemini: 0.78 },
    { date: "2025-02-01", gpt4: 0.85, gemini: 0.8 },
    { date: "2025-03-01", gpt4: 0.84, gemini: 0.81 },
    { date: "2025-04-01", gpt4: 0.86, gemini: 0.83 }
  ];
  const recent = Array.isArray(runs) ? runs.slice(-5).reverse() : [];
  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
      <Card>
        <CardTitle>Global SemantIQ Score</CardTitle>
        <CardValue>0.84</CardValue>
      </Card>
      <Card>
        <CardTitle>Total Benchmarks Run</CardTitle>
        <CardValue>{totalRuns}</CardValue>
      </Card>
      <Card>
        <CardTitle>Models Evaluated</CardTitle>
        <CardValue>{modelsEvaluated}</CardValue>
      </Card>
      <div className="lg:col-span-2">
        <Card>
          <CardTitle>Score Development over Time</CardTitle>
          <ScoreTrend data={chartData} />
        </Card>
      </div>
      <Card>
        <CardTitle>Recent Activity</CardTitle>
        <div className="mt-2 space-y-2">
          {recent.map((r: any) => (
            <div key={r.run_id} className="flex items-center justify-between">
              <div className="text-sm">{r.model_name || "unknown"} · {r.provider || "-"}</div>
              <div className="text-xs text-gray-500">{new Date(r.created_at).toLocaleString()}</div>
            </div>
          ))}
          {recent.length === 0 && <div className="text-sm text-gray-500">No recent runs</div>}
        </div>
      </Card>
    </div>
  );
}
