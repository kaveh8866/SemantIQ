# Long-Term Benchmark Health Monitoring

Benchmarks decay over time due to model capabilities improving and data contamination. We monitor health to know when to evolve.

## Health Indicators

### 1. Saturation Risk (The Ceiling Effect)
- **Signal**: When top-tier models consistently score >90% on a specific category.
- **Diagnosis**: The task is no longer discriminative.
- **Action**: Move category to "Solved/Legacy" and introduce a harder tier (e.g., SMF-Advanced).

### 2. Score Compression
- **Signal**: When the standard deviation of scores across a diverse set of models drops below 5%.
- **Diagnosis**: The benchmark fails to distinguish between mediocre and good models.
- **Action**: Review scoring granularity or prompt difficulty.

### 3. Prompt Memorization (Contamination)
- **Signal**: A model answers a "trick" question with the "correct" answer from the benchmark key, even when the question is slightly perturbed to require a different answer.
- **Action**: Immediate rotation of prompts.
- **Prevention**: Use "Canary Strings" (GUIDs) in datasets to search for them in training corpora (future feature).

## Lifecycle States

1.  **Active**: Default state. Recommended for evaluation.
2.  **At-Risk**: Showing signs of saturation. Warning issued in CLI.
3.  **Deprecated**: No longer recommended. Kept for historical reproducibility.
4.  **Retired**: Removed from default distribution.

## Rotation Schedule
- **Minor Rotation**: Every 6 months (add new prompts).
- **Major Overhaul**: Every 12-18 months (redefine categories).
