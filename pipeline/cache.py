import hashlib
import json
from typing import Any, Dict

def generate_run_fingerprint(
    benchmark_id: str,
    benchmark_version: str,
    dataset_hash: str,
    prompt_version: str,
    provider: str,
    model: str,
    run_params: Dict[str, Any]
) -> str:
    """
    Generates a deterministic hash for a run configuration.
    """
    # Sort keys for determinism
    canonical_params = json.dumps(run_params, sort_keys=True)
    
    payload = f"{benchmark_id}|{benchmark_version}|{dataset_hash}|{prompt_version}|{provider}|{model}|{canonical_params}"
    return hashlib.sha256(payload.encode()).hexdigest()
