# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |
| 0.x     | :x:                |

## Reporting a Vulnerability
We take the security of our benchmarks and tools seriously.

### Responsible Disclosure
If you discover a security vulnerability (e.g., code execution exploit, sensitive data leak) or a major integrity flaw (e.g., prompt leakage that invalidates the benchmark), please do **NOT** open a public issue.

Instead, please report it via:
- Email: [INSERT SECURITY EMAIL]
- GitHub Security Advisory (if enabled)

We will acknowledge your report within 48 hours and provide a timeline for mitigation.

### Benchmark Integrity Issues
For non-security issues related to benchmark validity (e.g., "The model has memorized this prompt"), please open a standard GitHub Issue with the label `integrity`.

### Scope
- **In Scope**:
  - Vulnerabilities in the CLI or Web UI.
  - Leaks of private/held-out evaluation datasets.
  - Exploits allowing manipulation of benchmark scores.
- **Out of Scope**:
  - Attacks requiring physical access to the user's machine.
  - "Jailbreaks" of the AI models being tested (unless caused by our harness).
