# Release Process

This document outlines how we ship new versions of SemantIQ-M-Benchmarks.

## 1. Release Cadence
- **Code**: Ad-hoc, triggered by feature completion or bug fixes.
- **Benchmarks**: Quarterly updates (target: Jan, Apr, Jul, Oct).

## 2. Release Checklist

### Pre-Release
1. [ ] **Code Freeze**: No new features merged 48h before release.
2. [ ] **Regression Testing**: Run full test suite (`pytest`).
3. [ ] **Benchmark Verification**: Run the reference models (e.g., GPT-4, Stable Diffusion) against the new benchmark set to ensure sanity.
4. [ ] **Documentation Update**: Update `CHANGELOG.md` and version numbers.

### Release Day
1. [ ] **Tagging**: Create a git tag (e.g., `v0.2.0`).
2. [ ] **Build**: Build CLI and Web UI artifacts.
3. [ ] **Publish**: Push to PyPI (CLI) and GitHub Releases.
4. [ ] **Announcement**: Post in Discussions/Discord/Socials.

## 3. Hotfixes
Critical bugs (e.g., crashing CLI, security flaw) allow for an immediate **PATCH** release, bypassing the quarterly cycle.
