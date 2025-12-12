import { notFound } from "next/navigation";
import { getRun, getRunMetrics } from "@/lib/api";
import { ScoresRadar } from "@/components/charts/radar";
import { Card, CardTitle, CardValue } from "@/components/ui/card";

export default async function RunDetail({ params }: { params: { id: string } }) {
  const data = await getRun(params.id).catch(() => null);
  if (!data) notFound();
  const metrics = await getRunMetrics(params.id).catch(() => ({ averages: {} }));
  const items = Object.entries(metrics.averages || {}).map(([k, v]) => ({ criterion: k, score: Number(v) }));
  return (
    <div className="space-y-6">
      <div className="text-xl font-semibold">Run #{params.id}</div>
      <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
        <Card>
          <CardTitle>Status</CardTitle>
          <CardValue>{data.status}</CardValue>
        </Card>
        <Card>
          <CardTitle>Timestamp</CardTitle>
          <CardValue>{new Date(data.created_at).toLocaleString()}</CardValue>
        </Card>
        <Card>
          <CardTitle>Cost</CardTitle>
          <CardValue>–</CardValue>
        </Card>
      </div>
      <Card>
        <CardTitle>Semantic Scores</CardTitle>
        <ScoresRadar data={items} />
      </Card>
      <Card>
        <CardTitle>Details</CardTitle>
        <div className="text-sm text-gray-400">Answers and judge reasoning will appear here.</div>
      </Card>
    </div>
  );
}
