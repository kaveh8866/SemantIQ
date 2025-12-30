# Governance & Team Structure

This project follows a formal governance model to ensure the scientific integrity of its benchmarks. Detailed role descriptions can be found in [Roles & Responsibilities](docs/ops/roles_and_responsibilities.md).

## Current Maintainers (v1.0 Launch Team)

| Role | Responsibility | Current Assignee |
| :--- | :--- | :--- |
| **Project Lead** | Overall direction, release engineering, security. | @kaveh8866 |
| **SMF Steward** | Semantic maturity, logic puzzles, reasoning depth. | *Interim: @kaveh8866* (Open for nominations) |
| **HACS Steward** | Human-AI alignment, rater reliability protocols. | *Interim: @kaveh8866* (Open for nominations) |
| **Vision Steward** | Multimodal consistency, image generation metrics. | *Interim: @kaveh8866* (Open for nominations) |
| **Community Mod** | Triage, Code of Conduct enforcement. | *Open* |

## Decision Making Process

1.  **Consensus Seeking**: We aim for consensus on all major changes.
2.  **Steward Veto**: The Steward for a specific domain (e.g., Vision) has veto power over changes to that benchmark's methodology or dataset content.
3.  **Tie-Breaking**: The Project Lead has the final tie-breaking vote if consensus cannot be reached.

## Becoming a Maintainer

We actively seek researchers and developers to take over Steward roles.
**Path to Stewardship**:
1.  Contribute consistently to a specific domain (e.g., submit 3 accepted PRs to SMF).
2.  Demonstrate deep understanding of the methodology (e.g., participate in a methodology review).
3.  Be nominated by an existing maintainer.

## Meetings & Reviews

- **Quarterly Health Check**: Scheduled for April, July, October, January (Automated via GitHub Actions).
- **Ad-hoc Methodology Reviews**: Triggered by `benchmark-integrity` issues.

## Code of Conduct

All contributors and maintainers must adhere to the [Code of Conduct](CODE_OF_CONDUCT.md).
