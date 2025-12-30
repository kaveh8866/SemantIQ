# SemantIQ-M Unified Web UI

The official visualization and analysis frontend for the SemantIQ-M Benchmark Suite.

## Overview
This Web UI provides a unified view across three benchmark domains:
1. **SMF (Text)**: Semantic Alignment & Safety.
2. **HACS (Human-AI)**: Human-in-the-loop collaboration.
3. **Vision (T2I)**: Text-to-Image semantic correctness.

It is designed as a **read-only, local-first** application to ensure privacy and reproducibility.

## Getting Started

### Prerequisites
- Node.js (v18+)
- Python (v3.10+) for the CLI

### Running Locally
You can launch the UI directly from the SemantIQ CLI:

```bash
# Serve the UI (starts API + Static File Server)
bench ui serve

# Build the frontend (if needed)
bench ui build
```

Access the UI at: http://127.0.0.1:8000

### Development Mode
For active frontend development (hot-reloading):

1. Start the API server:
   ```bash
   bench ui serve --dev
   ```
2. In a separate terminal, start Vite:
   ```bash
   cd webapp
   npm run dev
   ```
   Access at: http://localhost:5173 (Requests will be proxied to the API)

## Architecture

### Data Loading
The UI does not have a database. It reads JSON artifacts directly from the `reports/` directory:
- `reports/smf/runs/<id>/overall_summary.json`
- `reports/hacs/runs/<id>/overall_summary.json`
- `reports/vision/runs/<id>/overall_summary.json`

### Tech Stack
- **Framework**: React + Vite + TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Icons**: Lucide React
- **Backend**: FastAPI (Python) - serves static files and provides a read-only API over the file system.

## Privacy & Security
- **Local Execution**: All data remains on your machine. No telemetry is sent to SemantIQ.
- **Read-Only**: The UI cannot execute new runs or modify existing data.
- **No External Calls**: The application does not fetch resources from the public internet (fonts/icons are bundled or standard).

## Limitations
- **Image Hosting**: In this version, Vision benchmark images are stored locally.
- **Scalability**: Designed for single-user analysis, not for hosting thousands of concurrent runs.
