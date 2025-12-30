import os
import json
from typing import List, Dict, Any
from datetime import datetime
from benchmarks.schema import BenchmarkRunResult

class ResultRegistry:
    def __init__(self, base_dir: str = "."):
        self.base_dir = base_dir
        self.runs_dir = os.path.join(base_dir, "runs")
        self.index_path = os.path.join(self.runs_dir, "index.json")

    def update_index(self):
        """
        Scans the runs directory and rebuilds the index.
        """
        runs_index = []
        if not os.path.exists(self.runs_dir):
            return

        for entry in os.scandir(self.runs_dir):
            if entry.is_dir():
                result_path = os.path.join(entry.path, "result.json")
                if os.path.exists(result_path):
                    try:
                        with open(result_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            # Minimal metadata for index
                            runs_index.append({
                                "run_id": data.get("run_id"),
                                "timestamp": data.get("timestamp"),
                                "benchmark_id": data.get("spec", {}).get("id"),
                                "provider": data.get("model_info", {}).get("provider"),
                                "model": data.get("model_info", {}).get("model"),
                                "mean_score": data.get("summary", {}).get("mean_score"),
                                "status": "success" # Assumed if result.json exists
                            })
                    except Exception as e:
                        print(f"Error reading {result_path}: {e}")
        
        # Sort by timestamp descending
        runs_index.sort(key=lambda x: x["timestamp"], reverse=True)
        
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(runs_index, f, indent=2)

    def get_index(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.index_path):
            with open(self.index_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
