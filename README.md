# SemantIQ

## Project Vision
SemantIQ is an open-source platform for semantic-cognitive benchmarking for Models (LLMs), Multi-Modal and Text-to-Image Models, and Human Levels. It is designed to provide a modular, secure, and reproducible environment for evaluating AI systems. It aims to streamline the process of running benchmarks, analyzing results, and comparing model performance through a unified CLI and Web UI.

## Components Overview
- **CLI Tool**: A powerful command-line interface for managing benchmarks, datasets, and models.
- **Auto Benchmark Pipeline**: An automated pipeline for executing benchmarks consistently.
- **Web-App (UI)**: A modern web interface for visualizing results and managing the system.
- **API Abstraction Layer (Model Adapter)**: A flexible adapter system to connect with various LLM APIs (OpenAI, OpenRouter, etc.).

## Local Setup

### Prerequisites
- Python ≥ 3.11
- Node.js ≥ 18
- Git ≥ 2.40

### Installation
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/kaveh8866/SemantIQ.git
    cd SemantIQ
    ```

2.  **Backend Setup**:
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    
    pip install -e .[dev]
    ```

3.  **Frontend Setup**:
    ```bash
    cd webapp
    npm install
    ```

4.  **Environment Configuration**:
    - Copy `.env.example` to `.env` and fill in your API keys.

### Running the Project
- **CLI**: `semantiq --help`
- **Web UI**: `semantiq ui serve`
