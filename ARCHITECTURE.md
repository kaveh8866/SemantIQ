# SemantIQ Architecture (Phase 0)

## Overview
SemantIQ defines a modular structure to benchmark LLMs and persist results in a unified format. Phase 0 provides scaffolding without real provider calls.

## Modules
- `semantiq.schemas`: Core pydantic models for benchmarks, models, answers, and evaluation scores
- `semantiq.config`: Config schemas and loader for TOML/YAML/JSON
- `semantiq.benchmarks`: Loader utilities to read benchmark definitions from files
- `semantiq.models`: Base abstraction for LLM provider clients
- `semantiq.runner`: Orchestration for executing benchmarks against configured models
- `semantiq.storage`: Writers for result persistence (JSONL in Phase 0)
- `semantiq.cli`: Typer-based CLI entrypoint

## Data Flow
1. CLI reads config file and resolves model configurations and benchmark file paths
2. Benchmarks are parsed into `BenchmarkDefinition` instances
3. Runner iterates models and benchmarks and produces `ModelAnswer` instances (dummy in Phase 0)
4. Storage writes `ModelAnswer` records to JSONL file

## Extensibility
- Provider clients implement `LLMClient` and can be registered via config
- Storage can be swapped to SQLite/PostgreSQL/Parquet without changing schemas
- Evaluation scores attach to `ModelAnswer` records for human/AI grading