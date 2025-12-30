# Contributing Guidelines

Thank you for your interest in contributing to SemantIQ-M-Benchmarks! We welcome contributions from the community to make multimodal AI evaluation more robust and transparent.

## Contribution Types

### 1. Code Contributions
Improvements to the CLI, analysis pipelines, or web UI.
- **Requirements**:
  - Python code must be typed (Type hints).
  - New features require unit tests (`pytest`).
  - Follow the existing project structure.
- **Process**: Fork -> Branch -> PR -> CI Checks -> Review -> Merge.

### 2. Benchmark Contributions (SMF / HACS / Vision)
New prompts, datasets, or evaluation criteria.
- **Strict Rules**:
  - **No Model-Specific Optimization**: Prompts must not be tuned for a specific model (e.g., "Midjourney style").
  - **No "Performance Hacking"**: Do not submit prompts designed solely to lower scores of specific competitors without semantic justification.
  - **Language**: Prompts/Questions can be natural language; rationale/metadata MUST be English.
- **Artifacts Required**:
  - **Rationale**: Why is this test case important?
  - **Risk Analysis**: Could this prompt generate harmful content?
  - **Test Coverage**: How is it scored?

### 3. Documentation
Improvements to guides, policy documents, or inline comments.
- **Language**: English only.

## Review Process
- **Code**: Requires 1 review from a Maintainer.
- **Benchmarks**: Requires 2 reviews (1 Maintainer + 1 Domain Editor). We scrutinize benchmarks for bias, ambiguity, and difficulty.

## Development Setup
```bash
# Clone repository
git clone https://github.com/your-org/semantiq-m-benchmarks
cd semantiq-m-benchmarks

# Install dependencies
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install -e .

# Run tests
pytest
```

## License Agreement
By contributing, you agree that your contributions will be licensed under the project's licenses:
- **Code**: Apache License 2.0
- **Benchmarks/Data**: Creative Commons Attribution 4.0 (CC-BY 4.0)
