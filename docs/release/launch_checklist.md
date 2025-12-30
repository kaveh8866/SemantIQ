# Release Readiness Checklist

## 1. Code Integrity & CI
- [x] **CI Pipeline**: All tests passed (pytest 48/48 passed).
- [ ] **Linting**: Code style verified.
- [ ] **Dependencies**: `requirements.txt` is up-to-date and pinned where necessary.
- [ ] **Security**: No hardcoded secrets in codebase.

## 2. Versioning & Tags
- [ ] **Code Release Tag**: `v0.1.0` (SemVer compliant).
- [ ] **Benchmark Tags**:
    - [ ] SMF: `benchmarks-smf-v1.0`
    - [ ] HACS: `benchmarks-hacs-hib-1.0`
    - [ ] Vision: `benchmarks-vision-v0.1`
- [ ] **Changelog**: `CHANGELOG.md` updated for v0.1.0 release.

## 3. Data Integrity
- [ ] **Dataset Hashes**: `data_manifest.json` verified against actual files.
- [ ] **Prompt Templates**: All templates verified in `prompts/`.
- [ ] **Reference Data**: `datasets/` structure is consistent.

## 4. Documentation & Governance
- [ ] **README.md**: Root README polished and accurate.
- [ ] **License**: `LICENSE` file (Apache 2.0) present.
- [ ] **Notice**: `NOTICE` file present.
- [ ] **Citation**: `CITATION.cff` valid and up-to-date.
- [ ] **Ethics**: `docs/governance/ethics_statement.md` visible and linked.
- [ ] **Contributing**: `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` present.
- [ ] **Security**: `SECURITY.md` contact info active.

## 5. User Interface
- [ ] **Build**: `webapp/dist` builds successfully.
- [ ] **Functionality**: `bench ui serve` launches correctly.
- [ ] **No API Keys**: UI code free of bundled keys.

## 6. Public Release
- [ ] **GitHub Repo**: Public visibility enabled (if applicable).
- [ ] **Zenodo**: Repository connected for DOI generation.
- [ ] **GitHub Pages**: Documentation site live.
- [ ] **Announcement**: Release notes drafted.
