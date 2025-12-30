# Versioning & Tagging Strategy

## 1. Repository Tagging Policy
We use strict version tagging to ensure reproducibility of benchmark results.

### Codebase Versioning (SemVer)
- **Tag Format**: `vX.Y.Z` (e.g., `v0.1.0`)
- **Scope**: CLI tools, scoring engine, web application, and core libraries.
- **Rules**:
    - **Major (X)**: Breaking changes to CLI or API.
    - **Minor (Y)**: New features (e.g., new scorer type) without breaking existing workflows.
    - **Patch (Z)**: Bug fixes and internal improvements.

### Benchmark Versioning (Domain-Specific)
Benchmarks evolve independently of the code. We use specific tags for each domain to allow pinning specific dataset versions.

- **SMF (Semantic Maturity Framework)**
    - Tag: `benchmarks-smf-vA.B` (e.g., `benchmarks-smf-v1.0`)
    - Scope: `datasets/smf/`, `benchmarks/smf/`

- **HACS (Human-AI Cognitive Symmetry)**
    - Tag: `benchmarks-hacs-hib-X.Y` (e.g., `benchmarks-hacs-hib-1.0`)
    - Scope: `datasets/hacs/`, `benchmarks/hacs/`

- **Vision (SemantIQ Vision)**
    - Tag: `benchmarks-vision-vX.Y` (e.g., `benchmarks-vision-v0.1`)
    - Scope: `datasets/vision/`, `benchmarks/vision/`

## 2. Immutable Releases
- **No Force-Push**: Tags once pushed are immutable. If a mistake is made, a new patch version must be released.
- **Silent Changes Forbidden**: Any change to scoring logic or datasets requires a version bump.

## 3. Changelog Policy
We maintain a `CHANGELOG.md` at the root and within each domain directory.

### Format
- **Human-Readable**: Summary of what changed (Added, Changed, Deprecated, Removed, Fixed).
- **Machine-Readable**: `data_manifest.json` tracks SHA256 hashes of all critical data files for every release.

### Example Entry
```markdown
## [0.1.0] - 2025-01-15
### Added
- Initial public release of SemantIQ-M-Benchmarks.
- SMF v1.0 dataset integration.
- HACS v1.0 rater protocols.
- Vision v0.1 T2I rendering pipeline.
```
