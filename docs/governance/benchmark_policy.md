# Benchmark Integrity Policy

This document defines what constitutes a valid benchmark run and outlines the rules against manipulation.

## 1. Definition of Manipulation
Any attempt to artificially inflate scores without improving the underlying model capability is considered manipulation.

### Prohibited Practices
- **Prompt Tuning**: Modifying the benchmark prompts to specifically trigger better responses from a single model (overfitting).
- **Hidden Hints**: Including "magic words" or encoded instructions in prompts that are not part of the semantic test.
- **Leakage**: Using the evaluation dataset (test set) during the model's training process (contamination).
- **Hard-coded Responses**: If a model is detected to output a pre-canned response for a specific benchmark prompt hash, it is disqualified.

## 2. Benchmark Lifecycle

### Phase 1: Experimental
New benchmarks start in the `experimental/` folder. They are not included in aggregate scores.

### Phase 2: Active
Validated benchmarks are moved to the main `datasets/` tree. Scores from these are "official".

### Phase 3: Deprecated
When a benchmark is deemed "solved" (e.g., all top models score >99%) or "flawed", it is moved to `deprecated/`.
- **Reasoning**: To prevent "score inflation" where new models look better simply because they ace easy, old tests.
- **Retention**: Deprecated benchmarks remain available for historical reproduction.

## 3. Public Overfitting & Saturation
If we detect that public models are overfitting to a specific benchmark version:
1. We will release a **v(N+1)** version with semantically equivalent but lexically distinct prompts.
2. The old version will be marked as "Compromised".
3. We encourage community contributions of "adversarial" prompt variations.
