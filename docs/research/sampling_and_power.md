# Sampling and Power Analysis

## Sample Size Recommendations

### 1. Number of Raters (HACS)
To achieve an ICC > 0.7 (acceptable reliability):
- **Minimum**: 3 raters per item.
- **Recommended**: 5+ raters per item.
- **Gold Standard**: 10+ raters for high-stakes evaluation.

### 2. Number of Items (Prompts)
- **Pilot Studies**: 30-50 prompts.
- **Full Benchmarks**: 100+ prompts to detect small effect sizes (Cohen's d ~ 0.3).
- **Vision**: 500+ prompts recommended due to higher variance in image generation.

### 3. Number of Subjects (Models/Humans)
- Compare at least 3 models to establish a relative baseline.
- Include at least one "human baseline" or "oracle" reference if possible.

## Statistical Power
- For pairwise comparisons (t-tests), with N=100 items and alpha=0.05, we have 80% power to detect medium effects.
- **Balanced Design**: Ensure all models are evaluated on the *same* set of prompts.

## Handling Missing Data
- **Listwise Deletion**: If a rater misses >20% of items, exclude the rater.
- **Imputation**: Do not impute missing ratings; use robust metrics like Krippendorff's alpha that handle missingness naturally.
