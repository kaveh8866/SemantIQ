# Preregistration Template

**Title**: [Study Title]
**Date**: [YYYY-MM-DD]
**Authors**: [Author Names]

## 1. Hypotheses
- **H1**: Model X will score higher than Model Y on the SMF-Vision benchmark.
- **H2**: There will be a positive correlation (>0.6) between HACS "Clarity" scores and SMF "Coherence" scores.

## 2. Design Plan
- **Study Type**: Observational / Experimental
- **Blinding**: Raters [will/will not] be blinded to the model identity.
- **Study Design**: Balanced incomplete block design (if applicable).

## 3. Sampling Plan
- **Models**: [List of Models]
- **Prompts**: [Number of prompts] randomly sampled from [Dataset Version].
- **Raters**: Minimum of [N] raters per prompt.
- **Stopping Rule**: Data collection will stop when [N] ratings are collected or by [Date].

## 4. Analysis Plan
- **Reliability**: We will calculate ICC(2,k) to assess inter-rater reliability.
- **Exclusion Criteria**: Ratings with completion times < [X] seconds will be excluded.
- **Statistical Tests**: [T-test / ANOVA / Correlation]

## 5. Scripts
- We will use the standard SemantIQ-M analysis pipeline: `bench research report`.
