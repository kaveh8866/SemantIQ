# Advanced Usage: Studies and Matrix Runs

## Study Configuration
Define parameter matrices to create multiple runs systematically.

Example `study_config.yaml`:
```yaml
name: "Bias Resistance Study"
description: "Compare GPT-4 and Claude across temperatures"
created_by: "researcher@example.com"
benchmarks_path: "benchmarks/bias.yaml"
providers: ["openai", "gemini"]
models: ["gpt-4.1", "gemini-pro"]
temperatures: [0.1, 0.5, 0.9]
max_tokens: [128, 256]
repeats: 2
```

## Orchestrator
- Expands the matrix and enqueues each run to the worker queue.
- Tracks the study status until completion.

## Analyst Agent
- Pulls aggregated scores from the database.
- Uses an LLM to craft an executive summary (Markdown).
- Configurable via the model name passed to the agent.

## Reporting
- Generates Markdown reports; optional PDF with WeasyPrint.
- Includes executive summary and average scorecards.

## Scheduling
- Periodic tasks can be registered to run specific benchmarks at intervals (via arq cron).

