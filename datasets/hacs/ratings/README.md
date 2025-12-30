# HACS Ratings Data

This directory contains human evaluation data for the Human-AI Comparative Score (HACS) benchmark.

## Structure
- `ratings.csv`: The main dataset file (git-lfs recommended for large files).
- `schema.json`: JSON Schema definition for validation.
- `example_ratings.csv`: Template file for raters.

## Privacy & Ethics
- **Anonymity**: `rater_id` must be a pseudonymous hash or random string. Do NOT use real names.
- **Content**: Ratings text (`notes`) must not contain PII.
- **License**: All data in this directory is CC-BY 4.0.

## Validation
To validate a ratings file against the schema:
```bash
bench research validate-hacs --ratings path/to/ratings.csv
```
