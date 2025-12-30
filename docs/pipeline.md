# Semantiq Automated Pipeline

The Semantiq Pipeline enables automated, reproducible, and efficient execution of benchmarks across multiple providers, models, and parameter configurations. It is designed to be the backbone for research experiments, CI/CD integration, and the Web UI.

## Core Concepts

*   **Matrix Runs:** Automatically generate runs for all combinations of configured benchmarks, providers, models, and parameters.
*   **Determinism:** Runs are fingerprinted based on the exact configuration (dataset hash, prompt version, parameters).
*   **Caching:** Results are cached by fingerprint to save costs and time. Re-running the same configuration (if inputs haven't changed) yields the cached result immediately.
*   **Failure Isolation:** A failure in one run combination does not abort the entire pipeline.
*   **Result Registry:** All runs are indexed in a central registry for easy access by CLI and UI.

## Pipeline Configuration (YAML)

Pipelines are defined in a YAML configuration file.

```yaml
# pipeline/run_matrix.yaml

benchmarks:
  - code_writer_v1

providers:
  - openai
  - dummy

models:
  openai:
    - gpt-4o
    - gpt-3.5-turbo
  dummy:
    - fast-test-model

parameters:
  temperature: [0.0, 0.7]
  max_tokens: [1024]
  # Matrix expansion: 2 models * 2 temps = 4 runs per benchmark

run_options:
  parallelism: false # Set to true to enable parallel execution (careful with rate limits)
  max_workers: 4
  fail_fast: false   # If true, stops on first error
  cache_policy: use  # 'use' (default), 'refresh' (force re-run), 'disable' (no cache)

output_options:
  base_dir: runs
```

## CLI Usage

### Run a Pipeline
```bash
semantiq pipeline run pipeline/run_matrix.yaml
```

**Options:**
*   `--dry-run`: Prints the run combinations and cache status without executing models.

### List Runs
View all indexed benchmark runs with their status and scores.
```bash
semantiq pipeline list-runs
```

### Pipeline Status
Check the overall status of the pipeline (alias for list-runs for now).
```bash
semantiq pipeline status
```

## Caching Strategy

The system calculates a SHA256 fingerprint for every run based on:
1.  Benchmark ID & Version
2.  Dataset Hash (content integrity)
3.  Prompt Template Version
4.  Provider & Model Name
5.  Canonicalized Run Parameters (sorted keys)

**Cache Location:** `.cache/runs/<fingerprint>/`

*   **Hit:** If `result.json` exists in the fingerprint directory, it is returned immediately.
*   **Miss:** The benchmark is executed, and the result is saved to both the run directory (timestamped) and the cache directory.

## Data Flow

1.  **Config Loader:** Reads YAML, validates schema via Pydantic.
2.  **Matrix Generator:** Explodes parameters into individual `RunConfig` objects.
3.  **Runner Engine:**
    *   Iterates through configs.
    *   Computes Fingerprint.
    *   Checks Cache.
    *   Executes `PipelineEngine.run_benchmark` if needed.
    *   Saves artifacts.
4.  **Registry:** Scans output directories and updates `index.json`.

## Directory Structure

```
runs/
├── 2025-01-12T10-00-00_code_writer_v1/  # Individual Run Artifacts
│   ├── result.json
│   └── RUN_METADATA.json
└── index.json                           # Central Registry Index

.cache/
└── runs/
    └── <sha256_fingerprint>/            # Cached Result
        └── result.json
```
