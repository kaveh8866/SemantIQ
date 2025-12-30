# External Integration & Ecosystem

## Principles for the Ecosystem
We want a thriving ecosystem of tools built *on top* of SemantIQ, while preserving the integrity of the underlying measurements.

### 1. Wrappers & SDKs
- **Official**: The `semantiq` CLI and Python package.
- **Community**:
    - **Language Bindings**: (e.g., Node.js wrapper for CLI).
    - **Framework Plugins**: (e.g., HuggingFace Evaluation Harness integration).
- **Requirement**: Must not alter the prompt text or scoring logic without explicit documentation.

### 2. Dashboards & Visualization
- **Scope**: Tools that ingest `results.json` and create charts.
- **Guideline**: Do not aggregate scores into a single "Intelligence Number" without context. Show the breakdown.

### 3. Academic Forks
- **Encouraged**: Researchers often need to modify protocols.
- **Guideline**: Please change the package name or clearly label the fork to avoid confusion with the canonical benchmark.
- **Merge Back**: If the modification is generalizable, please PR it back!

## Branding & Attribution
- **Logo Usage**: Permitted for linking to the project.
- **Name**: "SemantIQ" is the project name.
- **Attribution**: "Results generated using SemantIQ-M-Benchmarks vX.Y".
