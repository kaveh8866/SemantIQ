# Security Guidelines

## API Keys
- Store API keys in environment variables.
- Never hardcode or commit keys.
- Keys are sanitized in logs and not printed.

## Confidential Benchmarks
- Do not include sensitive or proprietary content in benchmarks.
- Use `--unsafe-allow` only for controlled internal testing.

## Open Source Security
- Report vulnerabilities via the Security Contact.
- Avoid dependencies with known CVEs; update regularly.

## Threat Model
- Data leakage via logs
- Misconfiguration of providers
- Ingestion of PII in prompts
- Exposure of model raw responses

## Controls
- Central logging with sanitization
- Config validation for safe ranges and required keys
- Benchmark safety checks before runs

## Security Contact / Disclosure
- Email: security@semantiq.org
- Use responsible disclosure; do not publicly post exploits before fix.
