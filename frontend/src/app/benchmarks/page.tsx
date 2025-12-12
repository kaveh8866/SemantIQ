import { listBenchmarks } from "@/lib/api";

export default async function BenchmarksPage() {
  const items = await listBenchmarks().catch(() => []);
  return (
    <div className="space-y-4">
      <div className="text-xl font-semibold">Benchmarks</div>
      <div className="rounded-lg border border-gray-800">
        <table className="min-w-full text-sm">
          <thead className="bg-background-lighter">
            <tr>
              <th className="px-4 py-2 text-left">ID</th>
              <th className="px-4 py-2 text-left">Module</th>
              <th className="px-4 py-2 text-left">Dimensions</th>
            </tr>
          </thead>
          <tbody>
            {Array.isArray(items) && items.map((b: any) => (
              <tr key={b.id} className="border-t border-gray-800">
                <td className="px-4 py-2">{b.id}</td>
                <td className="px-4 py-2">{b.module}</td>
                <td className="px-4 py-2">{Array.isArray(b.dimensions) ? b.dimensions.join(", ") : "-"}</td>
              </tr>
            ))}
            {!Array.isArray(items) && (
              <tr>
                <td className="px-4 py-2" colSpan={3}>No data</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
