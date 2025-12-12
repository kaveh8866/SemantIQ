const BASE_URL = ""; // use server-side proxy

async function get<T = any>(path: string): Promise<T> {
  const res = await fetch(`/api/proxy${path}`, {
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

export async function playgroundRun(payload: {
  models: Array<{ provider: string; model_name: string; temperature?: number; max_tokens?: number; api_key?: string }>;
  benchmarks_data?: Array<{ id: string; module: string; prompt_text: string; dimensions?: string[] }>;
  benchmarks_path?: string;
}): Promise<{ runs: number[] }> {
  const res = await fetch(`/api/proxy/playground/run`, {
    method: "POST",
    headers: {
      "content-type": "application/json"
    },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    throw new Error(`${res.status}`);
  }
  return res.json() as Promise<{ runs: number[] }>;
}

export async function getRunResults(id: string | number): Promise<{ count: number; answers: Array<{ id: number; benchmark_id: string; answer_text: string }> }> {
  return get(`/runs/${id}/results`);
}
