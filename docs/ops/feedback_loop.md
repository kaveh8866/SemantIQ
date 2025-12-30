# Feedback → Benchmark Evolution Loop

To ensure the benchmark remains relevant without succumbing to "grade inflation" or overfitting, we follow a structured evolution loop.

## 1. Signal Collection
We collect signals from:
- **GitHub Issues**: `methodology-question`, `benchmark-integrity`.
- **Discussion Forums**: Qualitative feedback on prompt quality.
- **Citation Analysis**: How researchers are modifying the benchmark in their own work.
- **Automated Health Checks**: See [Benchmark Health](benchmark_health.md).

## 2. Signal Classification
Incoming feedback is classified by the **Benchmark Steward**:

| Class | Description | Action |
| :--- | :--- | :--- |
| **Noise** | "My model failed this, so the test is wrong." | Close with explanation. |
| **Usability** | "The CLI is hard to use." | Route to Core Maintainer (UX improvement). |
| **Ambiguity** | "This prompt has two valid answers." | Candidate for **Revision** or **Removal**. |
| **Saturation** | "All models score >95% on this category." | Candidate for **Deprecation** or **Hardening**. |
| **Methodological Risk** | "The metric assumes a normal distribution but data is skewed." | Requires **Audit**. |

## 3. Evolution Actions

### A. Hotfixing (Prohibited)
**Rule**: We DO NOT modify benchmark datasets in-place for released versions.
- *Exception*: Security leaks or PII. In this case, the specific item is redacted/removed, and a patch version is issued immediately.

### B. Prompt Rotation (Versioning)
If prompts are memorized or ambiguous:
1.  Develop replacement prompts.
2.  Validate them using HACS protocols.
3.  Include them in the *next minor version* (e.g., SMF v1.1).

### C. Deprecation
If a category is no longer discriminative (Saturation):
1.  Mark as `deprecated` in metadata.
2.  Move to `legacy/` folder in the next major release.
3.  Remove from default run configurations.

## 4. The Cycle
1.  **Release v1.0** -> Collect Feedback (3 months).
2.  **Review** -> Identify saturated/broken items.
3.  **Develop v1.1** -> Add new items, deprecate old ones.
4.  **Release v1.1** -> Reset the loop.
