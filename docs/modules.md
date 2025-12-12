# Modules

- `semantiq.benchmarks`: File-based loaders for benchmark definitions (YAML/JSON/JSONL)
- `semantiq.models`: Provider base and implementations (OpenAI, Grok, mocks)
- `semantiq.runner`: Orchestrates model runs and produces answers
- `semantiq.storage`: JSONL readers/writers for answers, evaluations, human ratings
- `semantiq.evaluation`: Base evaluator, LLMEvaluator, pipeline
- `semantiq.dashboard`: Monitoring UI using FastAPI + Jinja
- `semantiq.human_rater`: Human rating UI using FastAPI + Jinja
- `semantiq.schemas`: Pydantic data models
- `semantiq.cli`: Typer-based CLI commands
