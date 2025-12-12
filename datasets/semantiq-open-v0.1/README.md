# SemantIQ Open Benchmark Dataset v0.1

## Summary
This dataset bundles model answers, AI evaluations, and optional human ratings across SemantIQ benchmarks. It is intended for research, benchmarking, and evaluator calibration in Phase 0.

## Intended Use
Academic and open-source analysis of semantic-cognitive performance of LLMs. Not for diagnostic or psychological use.

## Dataset Structure
- `benchmarks.jsonl`: BenchmarkDefinition entries
- `model_answers.jsonl`: ModelAnswer entries
- `ai_evaluations.jsonl`: EvaluationResult entries (scores source='ai')
- `human_ratings.jsonl`: HumanRating entries (if present)
- `metadata.json`: summary metadata
- `config/models_used.yaml`: models and providers included
- `config/semantiq_version.txt`: exporter SemantIQ version

## Benchmarks Description
Phase 0 includes semantic-cognitive prompts (e.g., SMF, HACS, WIF, CBF). Prompts are high-level and non-sensitive.

## Models Included
Example: GPT-4.1, Gemini 1.5 Pro, Grok-2 (actual set depends on runs).

## Scoring Dimensions
`clarity`, `consistency`, `depth`, `bias_risk`, `reflection`, `stability`.

## How to Load the Dataset
Python:

```python
import json
answers = [json.loads(l) for l in open('model_answers.jsonl')]
evals = [json.loads(l) for l in open('ai_evaluations.jsonl')]
```

Pandas:

```python
import pandas as pd
answers_df = pd.read_json('model_answers.jsonl', lines=True)
evals_df = pd.read_json('ai_evaluations.jsonl', lines=True)
```

SemantIQ SDK:

```python
from semantiq.storage.jsonl import read_answers_jsonl
from semantiq.storage.eval_jsonl import read_evaluation_results
answers = read_answers_jsonl('model_answers.jsonl')
evals = read_evaluation_results('ai_evaluations.jsonl')
```

## License
Code: MIT. Dataset: CC BY 4.0.

## Limitations & Ethical Considerations
Not a psychological test or diagnostic instrument. Focused on semantic/intellectual evaluation in constrained contexts.

## Citation
```
@dataset{semantiq_open_v0_1,
  title = {SemantIQ Open Benchmark Dataset v0.1},
  version = {0.1.0},
  author = {{SemantIQ Contributors}},
  year = {2025}
}
```
