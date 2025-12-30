# Community Adoption: Researchers

## How to Use SemantIQ Responsibly
As a researcher, you are the primary audience for SemantIQ. We provide the tools to dissect model behavior, not just rank it.

### Valid Usage
- **Diagnostic Analysis**: "Model A scores lower on SMF 'Negation' than Model B, suggesting a specific deficit in logical processing."
- **Longitudinal Studies**: "Tracking the evolution of 'Vision' scores across training checkpoints."
- **Inter-Rater Reliability**: Using HACS protocols to validate human evaluation steps in your own study.

### Invalid Usage / Claims
- **General Intelligence Claims**: "Model X has a higher SemantIQ score, therefore it is smarter." (SemantIQ measures specific tasks, not 'g' factor).
- **Cross-Version Comparison**: Comparing scores from SMF v1.0 with SMF v2.0 directly without normalization.

## Citing Results
Always cite the specific version of the benchmark used.

> "We evaluated using SemantIQ-M-Benchmarks (v0.1.0) with the SMF dataset (v1.0) [1]."

## Contributing Improvements
If you find a flaw in our methodology:
1.  **Open an Issue** with the `methodology-question` label.
2.  **Propose a Change**: Submit a PR with a new dataset category or metric.
3.  **Do Not Bias**: Do not submit prompts that your own model was specifically trained on (contamination).
