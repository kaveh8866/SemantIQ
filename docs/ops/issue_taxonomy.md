# Issue Taxonomy & Triage System

Standardized labels and triage rules ensure that methodological concerns are treated with the same rigor as code bugs.

## Label Taxonomy

| Label Category | Label Name | Description | Triage Priority |
| :--- | :--- | :--- | :--- |
| **Integrity** | `benchmark-integrity` | Claims that a benchmark is flawed, biased, or contaminated. | **Critical** (24h) |
| **Methodology** | `methodology-question` | Questions about *why* a metric is calculated a certain way. | Medium (3-5 days) |
| **Code** | `scoring-regression` | Bug report: Scores changed without dataset/model changes. | High (48h) |
| **Docs** | `documentation-gap` | Missing or unclear instructions. | Low (Best Effort) |
| **Ethics** | `ethical-concern` | Report of harmful content or misuse. | **Critical** (Immediate) |
| **Misuse** | `false-comparison-claim` | Reports of users misrepresenting SemantIQ results (e.g., "marketing hype"). | Medium |

## Triage Process

1.  **Ingestion**: Community Moderator applies initial labels.
2.  **Routing**:
    - `benchmark-integrity` -> Assigned to **Benchmark Steward**.
    - `scoring-regression` -> Assigned to **Core Maintainer**.
    - `ethical-concern` -> Assigned to **Project Lead** + **Safety Team**.
3.  **Resolution**:
    - **Code Fix**: Standard PR flow.
    - **Benchmark Review**: Requires a "Governance Simulation" style review. If a benchmark is found flawed, it is *deprecated* in the next version, not silently patched.

## Expected Response Times
- **Critical**: Initial response within 24 hours.
- **High**: Initial response within 48 hours.
- **Medium/Low**: As resources allow.

## Policy: Code vs. Methodology
- **Code Fix**: "The ICC calculation throws a ZeroDivisionError." -> Fix immediately.
- **Methodology Fix**: "I think ICC is the wrong metric here." -> Requires Research Liaison review and proposal process.
