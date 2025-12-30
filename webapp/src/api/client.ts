import { RunSummary } from './types';

// In a real build, we might fetch from a backend API or load a static JSON manifest.
// For the "ui serve" command, we assume an API at /api

const API_BASE = '/api';

export async function fetchRuns(): Promise<RunSummary[]> {
  const response = await fetch(`${API_BASE}/runs`);
  if (!response.ok) {
    throw new Error('Failed to fetch runs');
  }
  return response.json();
}

export async function fetchRunDetail(runId: string): Promise<any> {
  const response = await fetch(`${API_BASE}/runs/${runId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch run detail');
  }
  return response.json();
}
