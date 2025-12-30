# Post-Launch Monitoring Plan

## 1. Issue Triage
- **Cadence**: Weekly review of new GitHub Issues.
- **Labels**:
    - `bug`: Critical failures in CLI/UI.
    - `benchmark-flaw`: Reports of errors in dataset questions/answers.
    - `feature-request`: New adapter or scorer ideas.

## 2. Benchmark Abuse Handling
If a model is found to be "gaming" the benchmark (hardcoded answers in training data):
1.  **Investigation**: Analyze the model's failure patterns on similar but unseen tasks.
2.  **Action**: If confirmed, we may mark the model as "Contaminated" in our internal reports and release a "v1.1" of the dataset with adversarial perturbations.

## 3. Release Cadence
- **Patch Releases (v0.1.x)**: As needed for bug fixes (weekly/bi-weekly).
- **Minor Releases (v0.2.0)**: New features or new benchmark categories (quarterly).
- **Major Releases (v1.0.0)**: Breaking changes to the core engine or scoring logic (annual).

## 4. Deprecation Policy
- Features will be marked `DeprecationWarning` for at least one minor version before removal.
- Old benchmark versions (e.g., `smf-v1.0`) remain available in the repo history/tags but are no longer the default in the CLI.
