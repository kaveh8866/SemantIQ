# Project Governance

## 1. Mission & Scope
The mission of **SemantIQ-M-Benchmarks** is to provide a unified, transparent, and reproducible framework for evaluating multimodal AI systems. We focus on:
- **Semantic Maturity Framework (SMF)**: Evaluating semantic capabilities of LLMs.
- **Human-AI Comparative Score (HACS)**: Assessing human-AI collaboration quality.
- **SemantIQ-Vision (T2I)**: Measuring semantic correctness in Text-to-Image generation.

Our goal is to foster open research, standardized evaluation, and ethical AI development.

## 2. Roles & Responsibilities

### Core Maintainers
Core Maintainers have administrative access to the repository and are responsible for the overall direction, release management, and final approval of significant changes.
- **Responsibilities**: Project roadmap, release tagging, security handling, conflict resolution.
- **Decision Power**: Consensus-seeking; in deadlocks, the Project Lead has the casting vote.

### Benchmark Editors
Experts in specific domains (Text, Vision, Human-AI) who curate and validate benchmark datasets.
- **Responsibilities**: Reviewing new prompts/datasets, ensuring benchmark integrity, maintaining domain-specific documentation.
- **Scope**: Can merge changes within their specific benchmark directories (e.g., `datasets/vision/`).

### Reviewers
Community members who actively review pull requests and issues.
- **Responsibilities**: Code review, reproducing benchmark runs, improving documentation.

## 3. Decision-Making Process
We operate on a **consensus-first** model.
1. **Proposal**: Significant changes (new benchmarks, API breaking changes) must start as an Issue or RFC (Request for Comments).
2. **Discussion**: Open discussion on GitHub.
3. **Consensus**: Maintainers aim for unanimous agreement.
4. **Escalation**: If no consensus is reached after reasonable debate, a vote among Core Maintainers is held.

## 4. Benchmark Management
Managing benchmarks is distinct from managing code.
- **Proposal**: New benchmarks are submitted via PR with a `rationale` and `validation report`.
- **Review**: Requires approval from at least one **Core Maintainer** AND one **Benchmark Editor**.
- **Deprecation**: Benchmarks that are "solved" (saturated) or found to be flawed are moved to `deprecated/` but never deleted to ensure reproducibility of historical results.
- **Protection**: Direct modification of existing prompt IDs (semantic change) is strictly forbidden. Fixes require a new version (e.g., `v1.1`).

## 5. Contact
For governance queries, contact the Core Maintainers via GitHub Issues.
