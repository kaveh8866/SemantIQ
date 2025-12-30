export type BenchmarkDomain = "SMF" | "HACS" | "VISION";

export interface CategoryScore {
  categoryId: string;
  score: number;
  label: string;
}

export interface RunMetadata {
  provider: string;
  model: string;
  timestamp: string;
  status?: "completed" | "failed" | "running";
}

export interface RunSummary {
  runId: string;
  domain: BenchmarkDomain;
  subject: string; // Model name or "Human"
  overallScore: number;
  categories: CategoryScore[];
  metadata: RunMetadata;
}

// SMF Specifics
export interface SMFRunDetail extends RunSummary {
  domain: "SMF";
  // Add more specific fields if needed
}

// HACS Specifics
export interface HACSRunDetail extends RunSummary {
  domain: "HACS";
  moduleScores: Record<string, number>;
}

// Vision Specifics
export interface VisionRunDetail extends RunSummary {
  domain: "VISION";
  promptScores?: Record<string, any>;
  violationRate?: number;
}
