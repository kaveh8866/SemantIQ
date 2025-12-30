# Community Adoption: Industry & Developers

## Integrating SemantIQ into MLOps
SemantIQ is designed to be a "unit test for cognition" in your model development pipeline.

### Recommended Workflow
1.  **Pre-Training**: Use small subsets of SMF to monitor capability acquisition during training runs.
2.  **Fine-Tuning**: Run the full HACS suite to ensure RLHF hasn't degraded cognitive symmetry or introduced bias.
3.  **Release Gate**: Use the CLI `validate` commands as a CI/CD gate before deploying a new model version.

### Marketing Guidelines
If you use SemantIQ scores in your model card or marketing materials:
- **Be Specific**: Don't say "SemantIQ Score: 90%". Say "SemantIQ SMF-v1.0 (Reasoning): 90%".
- **Link to Reproducibility**: Provide the `data_manifest.json` hash or the exact command used to generate the score.
- **No Cherry-Picking**: If you report SMF scores, report the aggregate or the full breakdown. Do not selectively hide low scores in specific categories.

### Commercial Use
- The codebase is **Apache 2.0** (commercial friendly).
- The datasets are **CC-BY 4.0** (attribution required).
- You **can** use SemantIQ to evaluate internal models.
- You **cannot** claim endorsement by the SemantIQ team.
