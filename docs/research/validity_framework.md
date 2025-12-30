# Validity Framework

## 1. Construct Validity
*Does the test measure what it claims to measure?*

### Hypotheses
- **H_CV1**: High scores on SMF "Logical Consistency" should correlate with high scores on HACS "Clarity".
- **H_CV2**: Models with higher parameter counts (within the same family) should generally score higher (monotonicity check).

## 2. Convergent Validity
*Do scores correlate with other established measures?*

### Hypotheses
- **H_ConV1**: SMF-Vision scores should correlate positively with CLIP-Score or other automated image quality metrics.
- **H_ConV2**: HACS ratings should correlate with established leaderboards (e.g., LMSYS Chatbot Arena) for the subset of overlapping models.

## 3. Discriminant Validity
*Are unrelated constructs actually uncorrelated?*

### Hypotheses
- **H_DV1**: "Creativity" scores should be distinct from "Safety" scores (low correlation expected).
- **H_DV2**: "Image Quality" (Vision) should be distinct from "Text Alignment" (SMF).

## 4. Face Validity
*Does it look right to experts?*
- **Process**: Subject Matter Experts (SMEs) review a random sample of 20 prompts and scoring criteria.
- **Checklist**:
  - [ ] Are prompts unambiguous?
  - [ ] Are scoring rubrics clear?
  - [ ] Is the difficulty level appropriate?
