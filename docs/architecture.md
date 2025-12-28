# System Architecture

## Overview
The system consists of three main layers:
1.  **Frontend**: A Vue.js/Vite web application for user interaction.
2.  **CLI/Backend**: A Python-based CLI tool and pipeline engine.
3.  **Data/Storage**: Local file system based storage for datasets, prompts, and results.

## Directory Structure
- `cli/`: Command Line Interface logic (Typer/Click).
- `benchmarks/`: Benchmark definitions and logic.
- `datasets/`: Storage for benchmark datasets.
- `prompts/`: Prompt templates.
- `adapters/`: Model adapters for different LLM providers.
- `pipeline/`: Core execution engine.
- `webapp/`: Frontend application.
- `docs/`: Documentation.

## Data Flow
1.  User initiates a benchmark via CLI or Web UI.
2.  **Pipeline** loads the specified benchmark configuration and dataset.
3.  **Model Adapter** communicates with the target LLM API.
4.  Results are collected and stored in `benchmarks/results/` (or similar).
5.  Web UI reads the results for visualization.

## Security
- API Keys are managed via `.env` files and never committed to version control.
- Input validation via Pydantic models.
