# Governance Simulation: Adding a New Benchmark

**Objective**: Prove that the governance process is robust, fair, and ensures quality before public adoption.

## Scenario
**Contributor**: "AliceResearcher" (External)
**Proposal**: Add a new SMF category: "Irony Detection Benchmark (IDB)"
**Target**: `benchmarks/smf/categories/idb/`

---

## 1. Proposal Phase (GitHub Issue)
**Action**: Alice opens an Issue using the "New Benchmark Proposal" template.

**Issue Content**:
> **Title**: [Proposal] Add Irony Detection Benchmark (IDB) to SMF
> **Description**: I propose adding a dataset of 50 irony-laden social media comments to test LLM subtlety.
> **Methodology**: Human-annotated dataset from SemEval 2018.
> **License**: CC-BY-SA 4.0.

**Governance Check**:
- [x] Is it multimodal? (No, text-only -> Fits SMF)
- [x] Is the license compatible? (CC-BY-SA 4.0 is compatible with our goals, but requires attribution)
- [x] Is it ethical? (No PII in data? -> Needs verification)

**Decision**: *Proceed to PR.*

---

## 2. Review Phase (Pull Request)
**Action**: Alice submits PR #42 adding `datasets/smf/idb.yaml` and `benchmarks/smf/categories/idb/`.

**CI Checks**:
- [x] `pytest` passes.
- [x] `validate-smf` command runs successfully on new file.
- [x] Schema validation passes.

**Human Review (Maintainer)**:
> **Reviewer**: "The dataset looks good, but please ensure all PII is scrubbed. Also, `question_guidelines.md` is missing."

**Alice's Response**:
> "Added guidelines. Verified scrubbing."

---

## 3. Decision Phase
**Action**: Core Maintainer performs final review.

**Decision Record**:
- **Integrity**: Verified (hashes match).
- **Quality**: Verified (guidelines clear).
- **Ethics**: Verified (PII removed).

**Outcome**: **Merge**

---

## 4. Release Impact
1.  **Version Bump**: SMF version bumped from v1.0 -> v1.1.
2.  **Changelog**: Entry added: "- Added Irony Detection Benchmark (IDB) by @AliceResearcher".
3.  **Data Manifest**: Updated with new file hashes.

This simulation confirms the process defined in `GOVERNANCE.md` and `CONTRIBUTING.md` is actionable.
