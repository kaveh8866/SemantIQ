# SemantIQ Architecture

## Module Overview (ASCII)
```
semantiq/
  benchmarks/   -> load benchmark definitions
  models/       -> provider interfaces & implementations (OpenAI, Grok, mock)
  runner/       -> orchestrate benchmark runs
  storage/      -> JSONL read/write for answers, evaluations, ratings
  evaluation/   -> LLM-as-a-Judge evaluator and pipeline
  dashboard/    -> FastAPI + Jinja web UI for monitoring
  human_rater/  -> FastAPI + Jinja human rating interface
  schemas/      -> pydantic models for all entities
  cli.py        -> Typer CLI entrypoint
  api/          -> FastAPI REST API (runs, benchmarks, results)
  db/           -> SQLModel models and async engine (PostgreSQL)
  storage/      -> Storage interface with PostgresStorage
  worker.py     -> arq worker processing benchmark runs asynchronously
```

## Lifecycle of a Benchmark Run
- Load config and benchmarks
- Iterate models and prompts
- Generate answers via provider
- Persist `ModelAnswer` to JSONL
- Evaluate answers (LLM judge) to `EvaluationResult`
- Human rating UI writes `HumanRating`
- Dashboard reads JSONL files and visualizes metrics
 
## Cloud Flow (Phase 1)
- Client calls `POST /runs` on API
- API creates `RunDB` (status pending) and enqueues job in Redis
- arq worker pulls job, runs benchmarks, writes answers to DB, marks run completed
- Clients poll `GET /runs/{id}` or `GET /runs/{id}/results`
 
## Environment Variables
- `DATABASE_URL`: PostgreSQL DSN (e.g., `postgresql+asyncpg://user:pass@host:5432/db`)
- `REDIS_URL`: Redis DSN (e.g., `redis://localhost:6379`)
- `SEMANTIQ_API_KEY`: API key for basic authentication

## Extensibility
- Add providers by implementing `BaseModelProvider`
- Add storage backends (SQLite/PostgreSQL) alongside JSONL
- Extend evaluator strategies (prompt variants, multi-judge ensembles)
