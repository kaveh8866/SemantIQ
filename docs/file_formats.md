# SemantIQ Dataset File Formats

## Overview
- `benchmarks.jsonl`: one benchmark definition per line
- `model_answers.jsonl`: one model answer per line
- `ai_evaluations.jsonl`: one evaluation result per line (AI-sourced)
- `human_ratings.jsonl`: one human rating per line (optional)
- `metadata.json`: summary metadata for the dataset
- `config/models_used.yaml`: models/providers included
- `config/semantiq_version.txt`: SemantIQ version used for export

## Example Lines
- `benchmarks.jsonl`:
  `{ "id": "smf-001", "module": "SMF", "prompt_text": "Explain semantic similarity.", "dimensions": ["clarity", "consistency"], "meta": {"difficulty": "easy"} }`

- `model_answers.jsonl`:
  `{ "benchmark_id": "smf-001", "model_id": "gemini:gemini-pro", "model": "gemini-pro", "provider": "gemini", "answer_text": "...", "usage_meta": {"input_tokens": 12, "output_tokens": 18}, "timestamp": "2025-01-01T00:00:00Z" }`

- `ai_evaluations.jsonl`:
  `{ "benchmark_id": "smf-001", "model": "gemini-pro", "provider": "gemini", "scores": [ { "criterion": "clarity", "value": 0.8, "source": "ai" } ] }`

- `human_ratings.jsonl`:
  `{ "benchmark_id": "smf-001", "model": "gemini-pro", "provider": "gemini", "criterion": "clarity", "value": 0.9, "rater_id": "r1" }`

## Metadata
`metadata.json` includes:
- `name`, `version`, `created_at`, `semantiq_version`
- counts and lists: `benchmarks_count`, `answers_count`, `models`, `providers`, `criteria`
- booleans: `has_ai_evaluations`, `has_human_ratings`
- `license`

## Models Used
`config/models_used.yaml` lists models and providers found in answers.

## Parquet (Optional)
If exported with `--format parquet` or `--format both`, Parquet files appear alongside JSONL:
- `model_answers.parquet`, `ai_evaluations.parquet`, `human_ratings.parquet`
Install extras: `python -m pip install -e .[parquet]`.
