# SemantIQ Benchmarks v0.2

This document describes the benchmark suite structure and how to contribute new prompts via YAML files.

## Modules
- SMF Core: foundational semantic tasks across meaning, context, narrative, reasoning, stability, structure, robustness, evidence, precision, ethics.
- Extended Metrics: decision transparency, safety, energy/token efficiency, documentation, weakness analysis.
- WIF Scale: knowledge illusion and confidence control tasks.
- CBF Framework: cognitive bias resistance and calibration tasks.
- Human-Specific: human insight, values, empathy, audience adaptation, judgment.

## Data Layout
- Location: `src/semantiq/data/benchmarks/`
- Files:
  - `01_smf_core.yaml`
  - `02_extended_metrics.yaml`
  - `03_wif_illusion.yaml`
  - `04_cbf_bias.yaml`
  - `05_human_specific.yaml`
- Golden examples: `src/semantiq/data/examples/golden_responses.yaml`

## YAML Schema
Each item must follow:
```yaml
- id: "MODULE-CODE"
  module: "module_name"
  prompt: "Prompt text with optional placeholders"
  dimensions: ["metric_a", "metric_b"]
  meta:
    name: "Descriptive name"
    difficulty: "basic|intermediate|advanced"
    tags: ["tag1", "tag2"]
    variables: ["PLACEHOLDER_A", "PLACEHOLDER_B"]
```

## Seeding
- Seed into the database:
  - `semantiq seed` (reads all YAML files)
  - `semantiq seed --force` (updates text if it changed)
- Validate data:
  - `semantiq validate-data` (detect duplicate IDs)

## Contribution Guide
- Add new prompts to the corresponding YAML file.
- Ensure unique `id` per prompt across the entire suite.
- Prefer short, precise dimensions (e.g., `clarity`, `consistency`).
- Use `meta.variables` for placeholders required at runtime.
- Run validation before opening a PR: `semantiq validate-data`.
