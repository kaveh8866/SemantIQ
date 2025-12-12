import Link from "next/link";
import { listRuns, getRunMetrics } from "@/lib/api";
import { Badge } from "@/components/ui/badge";

function formatStatus(s: string) {
  const map: Record<string, string> = {
    running: "border-yellow-600",
    completed: "border-green-600",
    failed: "border-red-600",
    pending: "border-gray-600"
  };
  return map[s] || "border-gray-600";
}

export default async function RunsPage() {
  const runs = await listRuns().catch(() => []);
  const averages = await Promise.all(
    (Array.isArray(runs) ? runs : []).map(async (r: any) => {
      try {
        const m = await getRunMetrics(r.run_id);
        const vals = Object.values(m.averages || {});
        if (!vals.length) return null;
        const sum = vals.reduce((a, b) => a + Number(b), 0);
        return sum / vals.length;
      } catch {
        return null;
      }
    })
  );
  return (
    <div className="space-y-4">
      <div className="text-xl font-semibold">Benchmark Runs</div>
      <div className="overflow-x-auto rounded-lg border border-gray-800">
        <table className="min-w-full text-sm">
          <thead className="bg-background-lighter">
            <tr>
              <th className="px-4 py-2 text-left">ID</th>
              <th className="px-4 py-2 text-left">Model</th>
              <th className="px-4 py-2 text-left">Provider</th>
              <th className="px-4 py-2 text-left">Timestamp</th>
              <th className="px-4 py-2 text-left">Status</th>
              <th className="px-4 py-2 text-left">Avg Score</th>
            </tr>
          </thead>
          <tbody>
            {Array.isArray(runs) && runs.map((r: any, i: number) => (
              <tr key={r.run_id} className="border-t border-gray-800">
                <td className="px-4 py-2">
                  <Link className="text-electric" href={`/runs/${r.run_id}`}>{r.run_id}</Link>
                </td>
                <td className="px-4 py-2">{r.model_name || "-"}</td>
                <td className="px-4 py-2">{r.provider || "-"}</td>
                <td className="px-4 py-2">{new Date(r.created_at).toLocaleString()}</td>
                <td className="px-4 py-2">
                  <Badge className={formatStatus(r.status)}>{r.status}</Badge>
                </td>
                <td className="px-4 py-2">{averages[i] != null ? averages[i].toFixed(2) : "–"}</td>
              </tr>
            ))}
            {!Array.isArray(runs) && (
              <tr>
                <td className="px-4 py-2" colSpan={6}>No data</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
