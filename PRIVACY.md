# Privacy Guidelines

## Zero-PII Philosophy
- SemantIQ datasets must not contain personal data.
- Do not include names, emails, phone numbers, or identifiers.

## ModelAnswers Storage
- Store minimal text and usage metadata.
- Avoid retaining raw provider objects; use sanitized payloads.

## Human Ratings
- Use anonymized rater IDs.
- Do not store demographics or sensitive attributes.

## Prohibited Data
- No health data, SSNs, credit cards, or private communications.

## Model Outputs
- Filter large or risky content before logging or releasing.
- Mask PII patterns using built-in sanitizers.

## Contributor Best Practices
- Validate datasets for PII before publishing.
- Use `docs/file_formats.md` as reference for safe structures.
