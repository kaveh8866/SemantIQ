# Benchmarks Module

This module contains the logic for individual benchmarks.

## Structure
Each benchmark should be a self-contained class that implements the standard `Benchmark` interface.
It defines:
- The input data schema.
- The evaluation logic.
- The scoring metrics.

## Isolation
Benchmarks must NOT contain model-specific code. They interact with models solely through the `adapters` layer.
