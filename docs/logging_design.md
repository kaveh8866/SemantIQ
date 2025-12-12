# Logging Design

## Goals
- Useful diagnostics without leaking sensitive data
- Simple integration across modules

## Components
- `get_logger(name, json_mode=None)` returns a sanitized logger
- `_SanitizingFilter` masks API keys and PII patterns

## Usage
- Prefer INFO for operational events
- Use DEBUG only for short, sanitized snippets
- Avoid dumping full prompts or answers
