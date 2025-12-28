# SemantIQ-M-Benchmarks

## Project Vision
SemantIQ-M-Benchmarks is an open-source LLM Benchmark Framework designed to provide a modular, secure, and reproducible environment for evaluating Large Language Models. It aims to streamline the process of running benchmarks, analyzing results, and comparing model performance through a unified CLI and Web UI.

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
    git clone <repo-url>
    cd SemantIQ-M-Benchmarks
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
    - Copy `webapp/.env.local.example` to `webapp/.env.local` for frontend config.

### Running the Project
*   (Instructions to be added as components are built)
