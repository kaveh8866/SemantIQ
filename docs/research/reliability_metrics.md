# Reliability Metrics

## Inter-Rater Reliability (IRR)

### Intraclass Correlation Coefficient (ICC)
We use **ICC(2,k)** (Two-way random effects, absolute agreement, average of k raters).
- **Interpretation**:
  - < 0.5: Poor
  - 0.5 - 0.75: Moderate
  - 0.75 - 0.9: Good
  - > 0.9: Excellent

### Krippendorff's Alpha
Used for categorical data or when there are missing ratings.
- **Interpretation**: Alpha > 0.8 is generally required for reliable conclusions.

## Intra-Rater Reliability
(Optional)
- **Test-Retest**: A subset of prompts is re-evaluated by the same raters after a washout period (e.g., 1 week).
- **Metric**: Pearson correlation or simple percent agreement.

## Implementation Details
- Code location: `evaluation/reliability/`
- Dependencies: `numpy`, `pandas`, `scipy` (optional)
