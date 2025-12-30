# Operational Roles & Responsibilities

To ensure the long-term integrity and sustainability of SemantIQ-M-Benchmarks, we define clear roles for maintainers and contributors.

## 1. Core Maintainers (Code + Infra)
**Scope**: Repository health, CLI functionality, CI/CD, release engineering, and security.
- **Responsibilities**:
    - Review and merge PRs related to core infrastructure (non-benchmark logic).
    - Manage releases and version tags.
    - Maintain the documentation website and operational tools.
    - Ensure security patches are applied.
- **Decision Boundary**: Can veto code changes that break architecture, but *cannot* unilaterally change benchmark datasets without Steward approval.

## 2. Benchmark Stewards (Domain Specific)
**Scope**: Methodological integrity of specific domains (SMF, HACS, Vision).
- **Roles**:
    - **SMF Steward**: Focus on reasoning and semantic maturity protocols.
    - **HACS Steward**: Focus on human-AI symmetry and rater reliability.
    - **Vision Steward**: Focus on multimodal generation and evaluation.
- **Responsibilities**:
    - Review new benchmark proposals (e.g., new SMF categories).
    - Validate changes to scoring logic.
    - Decide on deprecation of obsolete prompts.
    - Audit `data_manifest.json` changes.
- **Decision Boundary**: Final authority on *methodology* and *dataset content*.

## 3. Release Managers
**Scope**: Coordination of the release cycle.
- **Responsibilities**:
    - Assemble the changelog.
    - Verify release readiness (Checklist).
    - Mint DOIs and publish to Zenodo.
    - Communicate releases to the public.
- **Rotation**: Rotates among Core Maintainers per release.

## 4. Community Moderators
**Scope**: Health of public discussions (GitHub Issues, Discussions, Discord).
- **Responsibilities**:
    - Enforce the Code of Conduct.
    - Triage incoming issues (labeling).
    - Guide new contributors to the right docs.

## 5. Research Liaisons
**Scope**: Bridging the gap between academic research and the repo.
- **Responsibilities**:
    - Monitor citations and usage in papers.
    - Solicit feedback from independent researchers.
    - Translate academic findings into potential benchmark improvements.

## Succession & Rotation
- **Bus Factor**: We aim for at least 2 people capable of fulfilling each Core and Steward role.
- **Emeritus**: Past maintainers can move to an advisory "Emeritus" role.
