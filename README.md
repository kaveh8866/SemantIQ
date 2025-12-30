# SemantIQ-M-Benchmarks

[![CI](https://github.com/kaveh8866/SemantIQ/actions/workflows/ci.yml/badge.svg)](https://github.com/kaveh8866/SemantIQ/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/pending.svg)](https://zenodo.org/badge/latestdoi/pending)

**SemantIQ-M-Benchmarks** is an open-source, reproducible framework for evaluating the cognitive and semantic capabilities of Multimodal AI models. It provides a unified CLI and Web UI to run rigorous benchmarks across Reasoning (SMF), Human-AI Symmetry (HACS), and Vision domains.

## 🚀 Key Features
- **SMF (Semantic Maturity Framework)**: Evaluate abstract reasoning, bias resilience, and knowledge boundaries.
- **HACS (Human-AI Cognitive Symmetry)**: Measure how well models align with human cognitive patterns.
- **Vision**: Test Text-to-Image generation for attribute binding, spatial reasoning, and consistency.
- **Reproducible**: Git-hashed datasets and deterministic scoring ensure your results are verifiable.
- **Privacy-First**: Run everything locally. Your data stays on your machine.

## 📦 Quick Start (Local)

### Prerequisites
- Python ≥ 3.11
- Node.js ≥ 18 (for Web UI)
- Git

### Installation
```bash
git clone https://github.com/kaveh8866/SemantIQ.git
cd SemantIQ

# Setup Backend
python -m venv venv
# Windows: .\venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -e .[dev]

# Setup Frontend (Optional)
cd webapp && npm install && cd ..
```

### Running a Benchmark
```bash
# Run the 'code_writer' benchmark using a dummy model (no API key needed)
semantiq pipeline run code_writer_v1 --provider dummy --model test-model
```

### Viewing Results
```bash
semantiq ui serve
# Open http://localhost:5173
```

## 📚 Documentation
- [**Governance & Ethics**](docs/governance/ethics_statement.md)
- [**Research Protocols**](docs/research/protocol_overview.md)
- [**Release & Versioning**](docs/release/versioning.md)

## 🤝 Contributing
We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) and our [Code of Conduct](CODE_OF_CONDUCT.md).

## 📜 License
This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.
Data artifacts are licensed under CC-BY 4.0.

## 🔗 Citation
If you use this framework, please cite:
```bibtex
@software{semantiq_benchmarks,
  author = {{SemantIQ Research Team}},
  title = {SemantIQ-M-Benchmarks: A Unified Framework for Multimodal AI Evaluation},
  year = {2025},
  url = {https://github.com/kaveh8866/SemantIQ},
  version = {0.1.0}
}
```
