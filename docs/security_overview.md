# Security Overview

## Logging
- Central logger with sanitization
- Optional JSON output via `SEMANTIQ_LOG_FORMAT=json`

## Config Validation
- Warns on missing keys and unsafe ranges

## Benchmark Safety
- Static regex checks for risky content

## Provider Integration
- No API keys in logs
- Responses sanitized before storage
