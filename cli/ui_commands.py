import os
import json
import typer
from typing import List, Optional, Dict, Any
from pathlib import Path
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = typer.Typer(name="ui", help="SemantIQ-M Web UI Commands")

# --- FastAPI App ---
fastapi_app = FastAPI(title="SemantIQ-M API")

# Allow CORS for dev (Vite runs on 5173, API on 8000)
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RunMetadata(BaseModel):
    provider: str
    model: str
    timestamp: str
    status: Optional[str] = "completed"

class CategoryScore(BaseModel):
    categoryId: str
    score: float
    label: str

class RunSummary(BaseModel):
    runId: str
    domain: str
    subject: str
    overallScore: float
    categories: List[Dict[str, Any]]
    metadata: RunMetadata

def load_run_summary(path: Path, domain: str) -> Optional[RunSummary]:
    if not path.exists():
        return None
    try:
        with open(path, "r") as f:
            data = json.load(f)
            
        # Normalize data based on domain schema
        # SMF/HACS/Vision schemas might differ slightly, but we aim for the Unified Schema
        
        run_id = data.get("run_id") or path.parent.name
        model = data.get("model", "unknown")
        provider = data.get("provider", "unknown")
        timestamp = data.get("timestamp", "")
        overall_score = data.get("overall_score", 0.0)
        
        categories = []
        cat_summaries = data.get("category_summaries", {})
        
        # Vision/HACS use dict for categories, SMF might too
        if isinstance(cat_summaries, dict):
            for cat_id, cat_data in cat_summaries.items():
                score = cat_data.get("mean_score") if isinstance(cat_data, dict) else cat_data
                categories.append({
                    "categoryId": cat_id,
                    "score": score,
                    "label": cat_id.upper() # or look up name
                })
        
        return RunSummary(
            runId=run_id,
            domain=domain.upper(),
            subject=model,
            overallScore=overall_score,
            categories=categories,
            metadata=RunMetadata(
                provider=provider,
                model=model,
                timestamp=timestamp,
                status="completed"
            )
        )
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return None

def scan_runs() -> List[RunSummary]:
    runs = []
    base_dir = Path("reports")
    
    domains = ["smf", "hacs", "vision"]
    
    for domain in domains:
        domain_runs_dir = base_dir / domain / "runs"
        if not domain_runs_dir.exists():
            continue
            
        for run_dir in domain_runs_dir.iterdir():
            if run_dir.is_dir():
                summary_path = run_dir / "overall_summary.json"
                summary = load_run_summary(summary_path, domain)
                if summary:
                    runs.append(summary)
    
    # Sort by timestamp desc
    runs.sort(key=lambda x: x.metadata.timestamp, reverse=True)
    return runs

@fastapi_app.get("/api/runs", response_model=List[RunSummary])
def get_runs():
    return scan_runs()

@fastapi_app.get("/api/runs/{run_id}")
def get_run_detail(run_id: str):
    # Find the run file
    base_dir = Path("reports")
    domains = ["smf", "hacs", "vision"]
    
    for domain in domains:
        summary_path = base_dir / domain / "runs" / run_id / "overall_summary.json"
        if summary_path.exists():
            with open(summary_path, "r") as f:
                data = json.load(f)
            # Inject domain info
            data["domain"] = domain.upper()
            data["runId"] = run_id
            
            # Normalize categories for the UI
            cats = []
            cat_summaries = data.get("category_summaries", {})
            if isinstance(cat_summaries, dict):
                for cat_id, cat_data in cat_summaries.items():
                    score = cat_data.get("mean_score") if isinstance(cat_data, dict) else cat_data
                    cats.append({
                        "categoryId": cat_id,
                        "score": score,
                        "label": cat_id.upper()
                    })
            data["categories"] = cats
            
            # Metadata normalization
            if "metadata" not in data:
                 data["metadata"] = {
                     "provider": data.get("provider"),
                     "model": data.get("model"),
                     "timestamp": data.get("timestamp"),
                     "status": "completed"
                 }
            
            return data
            
    raise HTTPException(status_code=404, detail="Run not found")

# Serve static files (React App)
# We assume the user has built the app to webapp/dist
static_dir = Path("webapp/dist")
if static_dir.exists():
    fastapi_app.mount("/", StaticFiles(directory="webapp/dist", html=True), name="static")
else:
    # Fallback for dev mode (or if not built)
    @fastapi_app.get("/")
    def read_root():
        return {"message": "SemantIQ-M API running. Webapp not built. Run 'npm run build' in webapp/."}


# --- Typer Commands ---

@app.command("serve")
def serve(
    host: str = "127.0.0.1",
    port: int = 8000,
    dev: bool = False
):
    """
    Start the Web UI server.
    """
    print(f"Starting SemantIQ-M UI at http://{host}:{port}")
    if not Path("webapp/dist").exists() and not dev:
        print("Warning: webapp/dist not found. Only API will be available.")
        print("Run 'bench ui build' to build the frontend.")
        
    uvicorn.run(fastapi_app, host=host, port=port)

@app.command("build")
def build():
    """
    Build the React frontend (requires npm).
    """
    print("Building Web UI...")
    import subprocess
    try:
        subprocess.run(["npm", "install"], cwd="webapp", check=True, shell=True)
        subprocess.run(["npm", "run", "build"], cwd="webapp", check=True, shell=True)
        print("Build complete. Output in webapp/dist")
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
