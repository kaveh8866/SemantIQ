# System Architecture

## Overview
SemantIQ-M-Benchmarks is a modular, model-agnostic framework designed for evaluating Large Language Models (LLMs). The system is built on a clean separation of concerns, ensuring reproducibility, security, and extensibility.

## Core Principles
1.  **Separation of Concerns**: The CLI, benchmark logic, and model interaction are decoupled.
2.  **Model-Agnostic Design**: Benchmarks do not contain provider-specific code. All model interactions go through the Adapter layer.
3.  **Benchmark Isolation**: Each benchmark is self-contained with its own logic and data requirements.
4.  **Reproducibility**: All runs are versioned, and configurations are deterministic.
5.  **Security by Default**: API keys are never hard-coded; input data is validated.

## Directory Structure & Module Responsibilities

- **`cli/`**: The entry point for the user. Handles command-line arguments, subcommands (`init`, `run`, `list`, `report`), and renders output using `rich`. It orchestrates calls to the `pipeline` but contains no business logic.
- **`pipeline/`**: The execution engine. It orchestrates the loading of benchmarks, initialization of adapters, execution of tests, and storage of results.
- **`benchmarks/`**: Contains the definitions of individual benchmarks. Each benchmark is a class implementing a standard interface.
- **`datasets/`**: Stores static and versioned data used by benchmarks.
- **`prompts/`**: Contains prompt templates. This allows for versioning and modification of prompts without changing benchmark code.
- **`adapters/`**: The Abstraction Layer for LLM providers. It defines a `BaseModelAdapter` interface that all specific providers (OpenAI, Anthropic, Local, etc.) must implement.
- **`webapp/`**: The Vue.js/Vite frontend for visualizing results and managing the system (future integration).
- **`docs/`**: Project documentation.

## Data Flow

1.  **Initialization**: User runs `semantiq run <benchmark_name> --model <provider>`.
2.  **Configuration**: CLI loads configuration from environment variables (`.env`) and flags.
3.  **Pipeline Setup**: The `Pipeline` module initializes the requested `Benchmark` class and the appropriate `ModelAdapter`.
4.  **Execution**:
    *   The Benchmark requests a prompt template from `prompts/`.
    *   The Benchmark loads data from `datasets/`.
    *   The Benchmark constructs the final prompt.
    *   The Pipeline sends the prompt to the `ModelAdapter`.
    *   The `ModelAdapter` calls the external API (or local model) and returns a standardized `ModelResponse`.
5.  **Scoring & Storage**: The Benchmark evaluates the response. Results are saved to disk (JSON/SQLite).
6.  **Reporting**: CLI displays a summary via `rich`.

## Risk Assessment & Mitigation

| Risk | Description | Mitigation Strategy |
| :--- | :--- | :--- |
| **Prompt Injection** | Malicious inputs in datasets affecting model behavior. | **Template Sandboxing**: Use Jinja2 auto-escaping. **Input Validation**: Strict schema validation for dataset entries. **System Instructions**: Robust system prompts enforcing role and output format. |
| **Prompt Leakage** | Inadvertent exposure of system prompts or benchmark answers in model outputs. | **Strict Separation**: Prompts are stored in `prompts/`, not code. Output validation in Pipeline to detect leakage. |
| **Benchmark Overfitting** | Models trained on benchmark data (contamination). | **Dynamic Datasets**: Support for private/local datasets in `datasets/` that are not public. Versioning of datasets. **Hash Verification**: Datasets are hashed to detect modification. |
| **API Abuse** | Excessive costs or rate limits due to loops or malformed requests. | **Budget Limits**: Pipeline can enforce token limits. **Retry Logic**: Centralized in `adapters` with exponential backoff. |
| **Reproducibility Issues** | Different results for the same input due to model non-determinism. | **Config Locking**: Recording temperature, seed, and model version for every run. **Artifact Versioning**: Saving exact prompt/data versions used. **Deterministic Scoring**: Use exact match or verifiable heuristics where possible. |
| **Security (Keys)** | Leaking API keys in code or logs. | **Environment Variables**: Keys loaded *only* from `.env`. **Log Sanitization**: Pipeline logs are scrubbed of sensitive patterns. |

## Data Models (Schema)

SemantIQ uses strict Pydantic models to ensure data integrity and reproducibility.

### Benchmark Spec (`BenchmarkSpec`)
Defines the configuration for a benchmark run.
- `id`: Unique identifier (e.g., "code_writer_v1")
- `version`: Semantic version
- `dataset_path`: Path to the input dataset
- `dataset_hash`: SHA256 hash for verification
- `prompt_template_path`: Directory containing Jinja2 templates
- `scoring`: Configuration for the scoring mechanism

### Test Case (`TestCase`)
Represents a single unit of work.
- `case_id`: Unique ID within the dataset
- `input`: The primary input (e.g., instruction)
- `expected`: The ground truth (optional)
- `constraints`: List of specific constraints
- `metadata`: Tags, difficulty, etc.

### Run Result (`BenchmarkRunResult`)
The complete artifact of a benchmark execution.
- `run_id`: Timestamped unique ID
- `spec`: The full spec used for the run
- `model_info`: Provider and model name
- `cases`: List of `CaseResult` (input, output, score, latency)
- `summary`: Aggregated metrics (mean score, duration)

## Security Implementation
- **API Keys**: Managed via `.env` files (using `python-dotenv` pattern, though currently relying on `os.environ`).
- **Input Validation**: All internal data structures use Pydantic for runtime type checking.
