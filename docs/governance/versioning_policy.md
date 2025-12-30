# Versioning Policy

We use **Semantic Versioning (SemVer 2.0.0)**, but we distinguish between **Code Versioning** and **Benchmark Versioning**.

## 1. Code Versioning
Refers to the CLI, Web UI, and Analysis Pipeline.
- **MAJOR (1.0.0)**: Breaking changes to the CLI API or JSON output format.
- **MINOR (0.1.0)**: New features (e.g., new visualization type, new command).
- **PATCH (0.0.1)**: Bug fixes that do not alter benchmark logic.

## 2. Benchmark Versioning
Refers to the content of `datasets/`, `prompts/`, and evaluation logic.
Each domain (SMF, HACS, Vision) has its own version, tracked in `datasets/<domain>/metadata.json`.

- **MAJOR (v2.0)**:
  - Methodology change (e.g., changing from boolean scoring to scalar scoring).
  - Removal of a sub-category.
  - Scores are **NOT** comparable across Major versions.
- **MINOR (v1.1)**:
  - Addition of new prompts/questions.
  - Clarification of existing prompts (without changing semantic meaning).
  - Scores **ARE** generally comparable, but v1.1 is harder/more comprehensive.
- **PATCH**:
  - Typo fixes in metadata (not in prompts).

## 3. Reproducibility
- **Snapshotting**: Every release is tagged in git.
- **Availability**: We guarantee that all versions of benchmark data will remain available in the repository history.
- **Reporting**: Benchmark reports MUST include the specific version hash or tag used.
