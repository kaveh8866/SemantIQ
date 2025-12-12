const BASE_URL = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000").replace(/\/+$/, "");
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || "dev-key";

async function get<T = any>(path: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "x-api-key": API_KEY },
    cache: "no-store"
  });
  if (!res.ok) {
    throw new Error(`${res.status}`);
  }
  return res.json() as Promise<T>;
}

export async function listRuns(): Promise<Array<{ run_id: number; status: string; created_at: string; model_name?: string; provider?: string }>> {
  return get("/runs");
}

export async function getRun(id: string | number): Promise<{ run_id: number; status: string; created_at: string }> {
  return get(`/runs/${id}`);
}

export async function getRunMetrics(id: string | number): Promise<{ run_id: number; averages: Record<string, number> }> {
  return get(`/runs/${id}/metrics`);
}

export async function listBenchmarks(): Promise<Array<{ id: string; module: string; prompt: string; dimensions: string[] }>> {
  return get("/benchmarks");
}
