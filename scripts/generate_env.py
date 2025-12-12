import json
import os
import subprocess

def terraform_outputs() -> dict:
    try:
        raw = subprocess.check_output(["terraform", "output", "-json"], cwd="infra/terraform")
        return json.loads(raw.decode("utf-8"))
    except Exception:
        return {}

def main() -> None:
    outs = terraform_outputs()
    db_url = outs.get("db_url", {}).get("value") or os.getenv("DATABASE_URL", "")
    redis_host = outs.get("redis_endpoint", {}).get("value") or os.getenv("REDIS_HOST", "")
    redis_url = f"redis://{redis_host}:6379" if redis_host and not redis_host.startswith("redis://") else (redis_host or "")
    content = []
    if db_url:
        content.append(f"DATABASE_URL={db_url}")
    if redis_url:
        content.append(f"REDIS_URL={redis_url}")
    api_url = os.getenv("NEXT_PUBLIC_API_URL", "https://api.semantiq.ai")
    api_key = os.getenv("SEMANTIQ_API_KEY", "")
    content.append(f"NEXT_PUBLIC_API_URL={api_url}")
    if api_key:
        content.append(f"NEXT_PUBLIC_API_KEY={api_key}")
        content.append(f"SEMANTIQ_API_KEY={api_key}")
    with open(".env.prod", "w", encoding="utf-8") as f:
        f.write("\n".join(content) + "\n")

if __name__ == "__main__":
    main()

