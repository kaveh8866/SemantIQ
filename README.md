# SemantIQ – Semantic Intelligence Benchmarking Platform

SemantIQ is an open-source platform for semantic-cognitive benchmarking of Large Language Models (LLMs). It provides standardized schemas, a pluggable provider system, orchestration for benchmark runs, LLM-as-a-Judge evaluation, a Human Rater interface, and a simple dashboard.

Version: `0.1.0` (Phase 0)

## Goals
- Define core schemas for benchmarks, model configs, answers, and evaluation scores
- Provide a minimal CLI to orchestrate runs against configured models and benchmarks
- Persist results in JSONL (extensible to SQLite/PostgreSQL/Parquet later)
- Keep dependencies small and code simple, readable, and extendable

## Installation

PyPI (coming soon):

```bash
pip install semantiq
```

Local (editable) with all extras:

```bash
python -m pip install -e .[all]
```

## Quickstart

1) Prepare a YAML config:

```yaml
# config/config.yaml
models:
  openai:
    model_name: "gpt-4.1"
    temperature: 0.2
    max_tokens: 256
  gemini:
    model_name: "gemini-pro"
    temperature: 0.3
    max_tokens: 256
  grok:
    model_name: "grok-beta"
    temperature: 0.3
    max_tokens: 256
```

2) Prepare a benchmark file:

```yaml
# benchmarks/smf_example.yaml
- id: SMF-00
  module: smf
  prompt: "Explain the concept of semantic consistency in one paragraph."
  dimensions:
    - clarity
    - consistency
  meta:
    difficulty: basic
```

3) Run CLI commands:

```bash
semantiq run --benchmarks benchmarks/smf_example.yaml --provider openai --config config/config.yaml --output outputs/run1.jsonl
```

This command runs a provider against benchmarks and writes structured answers to JSONL.

Evaluate answers using LLM-as-a-Judge:

```bash
semantiq evaluate --input outputs/run1.jsonl --output outputs/scores.jsonl --provider openai --config config/config.yaml --benchmarks benchmarks/smf_example.yaml
```

Start the dashboard:

```bash
semantiq dashboard --answers-dir outputs/ --evals-dir outputs/
```

## Environment Variables
- `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `XAI_API_KEY` are referenced by name only; no secrets are hardcoded.

## Repository Layout

```text
src/
  semantiq/
    __init__.py
    cli.py
    schemas.py
    benchmarks/
      loader.py
    config/
      loader.py
      schemas.py
    models/
      base.py
    runner/
      run.py
    storage/
      jsonl.py
examples/
  config.toml
  benchmarks/
    example_benchmarks.json
tests/
  test_schemas.py
```

## Features
- Pluggable providers (OpenAI, Gemini, Grok; mocks for Phase 0 except OpenAI/Grok)
- Unified schemas for benchmarks, answers, and evaluations
- Runner orchestration with JSONL storage
- LLM-as-a-Judge evaluator for automated scoring
- Human Rater UI for collecting gold-standard scores
- Dashboard for inspecting runs and benchmark performance

## Providers
- OpenAI (real API)
- Grok (xAI, OpenAI-compatible API)
- Gemini (mock in Phase 0)
Configure via `config/config.yaml` and environment variables.

## Evaluators
- LLMEvaluator (LLM-as-a-Judge) assigns scores per criterion and writes them to JSONL.
- Criteria: clarity, consistency, depth, bias_risk, reflection, stability.
- Ensure the `openai` extra is installed: `python -m pip install -e .[providers]`
- Provide your API key via environment: `OPENAI_API_KEY=...`
- Reference the key in `config/config.yaml` using `${ENV.OPENAI_API_KEY}` under the relevant model key

Example:

```yaml
models:
  openai:
    model_name: "gpt-4.1"
    temperature: 0.2
    max_tokens: 256
    api_key: "${ENV.OPENAI_API_KEY}"
```

## Dashboard
- Minimal FastAPI + Jinja web UI to view runs and evaluation scores.
- Start: `semantiq dashboard --answers-dir outputs/ --evals-dir outputs/`

## Next Steps (Phase 1–3)
- Implement concrete provider clients (OpenAI, Gemini, Grok) with HTTP calls
- Load benchmarks from files with validation and richer metadata
- Run real requests and persist raw responses and usage metadata
- Add evaluation scoring interfaces and support human annotation workflows
- Extend storage to SQLite/PostgreSQL and add basic analytics queries
## Using Grok as a provider
- xAI Grok supports an OpenAI-compatible chat completions API
- Provide your API key via `GROK_API_KEY`; base URL defaults to `https://api.x.ai/v1` but can be overridden in config

Config snippet:

```yaml
models:
  grok:
    model_name: "grok-2-latest"
    temperature: 0.3
    max_tokens: 256
    api_key: "${ENV.GROK_API_KEY}"
    base_url: "https://api.x.ai/v1"
```

Run:

```bash
GROK_API_KEY=xxx semantiq run --provider grok --benchmarks benchmarks/smf_example.yaml --config config/config.yaml --output outputs/grok_run.jsonl
```

## Providers and environment variables

| Provider | Env Var          | Example Model     |
|----------|------------------|-------------------|
| openai   | OPENAI_API_KEY   | gpt-4.1           |
| gemini   | GEMINI_API_KEY   | gemini-1.5-pro    |
| grok     | GROK_API_KEY     | grok-2-latest     |

## Evaluations (LLM-as-a-Judge)
- SemantIQ supports evaluating model answers using an LLM judge.
- Prepare answers JSONL from a prior run and a judge model configuration.

Run:

```bash
OPENAI_API_KEY=xxx semantiq evaluate --input outputs/run1.jsonl --output outputs/scores.jsonl --provider openai --config config/config.yaml --benchmarks benchmarks/smf_example.yaml
```

Notes:
- Judge prompts request strict JSON with a list of scores.
- Criteria default to `clarity`, `consistency`, `depth` if benchmark dimensions are absent.

## JSONL Storage
- Answers: one `ModelAnswer` per line
- Evaluations: one `EvaluationResult` per line
- Human ratings: one `HumanRating` per line
The SemantIQ Dashboard is a simple web UI to inspect model runs and evaluation scores.

Install extras:

```bash
python -m pip install -e .[dashboard]
```

Start:

```bash
semantiq dashboard --answers-dir outputs/ --evals-dir outputs/
```

On the main page you see a list of model runs and an overview of their average SemantIQ scores.

## Dataset Export (SemantIQ Open v0.1)
- Bundles benchmarks, model answers, AI evaluations, and optional human ratings into a reusable dataset folder.
- Command: `semantiq export-dataset BENCHMARKS OUT_DIR [--answers ...] [--evaluations ...] [--human_ratings ...]`

Example:

```bash
# Export minimal dataset with benchmarks only
semantiq export-dataset examples/benchmarks/example_benchmarks.json datasets/semantiq-open-v0.1

# Export with answers and AI evaluations
semantiq run examples/benchmarks/example_benchmarks.json gemini examples/config.yaml outputs/run_gemini.jsonl
semantiq evaluate outputs/run_gemini.jsonl outputs/scores_gemini.jsonl --provider gemini --config examples/config.yaml --benchmarks examples/benchmarks/example_benchmarks.json
semantiq export-dataset examples/benchmarks/example_benchmarks.json datasets/semantiq-open-v0.1 --answers outputs/run_gemini.jsonl --evaluations outputs/scores_gemini.jsonl
```

Dataset layout:
- `benchmarks.jsonl` — benchmark definitions
- `model_answers.jsonl` — model answers
- `ai_evaluations.jsonl` — AI judge scores
- `human_ratings.jsonl` — human ratings (if provided)
- `metadata.json` — summary metadata
- `config/models_used.yaml`, `config/semantiq_version.txt`

Loading snippets:

```python
import json
answers = [json.loads(l) for l in open('datasets/semantiq-open-v0.1/model_answers.jsonl')]
evals = [json.loads(l) for l in open('datasets/semantiq-open-v0.1/ai_evaluations.jsonl')]
```

## Human Rater
The Human Rating Interface allows humans to rate model answers along SemantIQ dimensions. Ratings are stored as JSONL and can be used as gold-standard data or to calibrate the LLM-based evaluator.

Install:

```bash
python -m pip install -e .[human_rater]
```

Start:

```bash
semantiq human-rater --answers outputs/run1.jsonl --ratings outputs/human_ratings.jsonl --benchmarks benchmarks/smf_example.yaml
```

Rating format:

- Score scale: 0.0–1.0 per criterion
- Criteria: `clarity`, `consistency`, `depth`, `bias_risk`, `reflection`, `stability`
- Output stored as one `HumanRating` per criterion in `outputs/human_ratings.jsonl`

Integration notes:
- `HumanRating` aligns with `EvaluationScore` via `benchmark_id`, `model`, `provider`, and optional `answer_id` for future merging and correlation analyses.
## Development
- Editable install: `python -m pip install -e .[all]`
- Run tests: `pytest -q`
- Lint/format: `ruff`, `black`

## Versioning
- Semantic Versioning (`MAJOR.MINOR.PATCH`)
- Current: `v0.1.0` (Phase 0)
- See `CHANGELOG.md` for release notes

## License
- MIT License (see `LICENSE`)

## Citation (Template)
```
@software{semantiq_2025,
  title = {SemantIQ: Semantic Intelligence Benchmarking Platform},
  version = {0.1.0},
  author = {{SemantIQ Contributors}},
  year = {2025},
  url = {https://github.com/semantiq/semantiq}
}
```
## Security & Privacy
- Centralized logging with sanitization; avoids printing API keys or PII patterns.
- Config validation warns about unsafe parameter ranges or missing keys.
- Benchmark safety checks flag risky content; use `--unsafe-allow` for controlled runs.

## Responsible Use of SemantIQ
- SemantIQ does not evaluate humans psychologically; it evaluates semantic clarity and reasoning consistency in dialog contexts only.
- Use datasets responsibly and avoid collecting or releasing PII.
 
## Cloud Stack (Phase 1)
- Components: FastAPI (`src/semantiq/api/main.py`), Redis queue, arq worker (`src/semantiq/worker.py`), PostgreSQL (`src/semantiq/db`).
- Env vars: `DATABASE_URL`, `REDIS_URL`, `SEMANTIQ_API_KEY`.
- Compose: `docker-compose.cloud.yaml`.

Spin up:
```bash
docker compose -f docker-compose.cloud.yaml up --build
```

API:
```bash
curl -H "X-API-Key: dev-key" -X POST http://localhost:8000/runs -d '{"model_config":{"provider":"gemini","model_name":"gemini-pro"}}' -H "Content-Type: application/json"
```
