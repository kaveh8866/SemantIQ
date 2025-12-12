from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from semantiq.benchmarks.loader import load_benchmarks
from semantiq.schemas.evaluation import EvaluationCriterion


def iter_benchmark_files(root: Path) -> Iterable[Path]:
    yield from sorted(root.glob("*.yaml"))


def main() -> int:
    root = Path("src/semantiq/data/benchmarks")
    if not root.exists():
        print(f"Benchmarks directory not found: {root}", file=sys.stderr)
        return 2

    allowed_dims = {c.value for c in EvaluationCriterion}
    files = list(iter_benchmark_files(root))

    id_to_files: dict[str, list[str]] = defaultdict(list)
    invalid_dims: list[tuple[str, str, list[str]]] = []
    per_file_counts: dict[str, int] = {}

    total = 0
    for fp in files:
        items = load_benchmarks(str(fp))
        per_file_counts[str(fp)] = len(items)
        total += len(items)
        for b in items:
            id_to_files[b.id].append(str(fp))
            bad = [d for d in (b.dimensions or []) if d not in allowed_dims]
            if bad:
                invalid_dims.append((b.id, str(fp), bad))

    duplicates = {bid: fps for bid, fps in id_to_files.items() if len(fps) > 1}

    print("Benchmark Validation Report")
    print("---------------------------")
    print(f"Files scanned: {len(files)}")
    print(f"Benchmarks loaded: {total}")
    print("Per-file counts:")
    for f, cnt in sorted(per_file_counts.items()):
        print(f"  {f}: {cnt}")

    print("")
    print(f"Duplicate IDs: {len(duplicates)}")
    if duplicates:
        for bid, fps in sorted(duplicates.items()):
            print(f"  {bid}:")
            for f in fps:
                print(f"    - {f}")

    print("")
    print(f"Invalid dimensions: {len(invalid_dims)}")
    if invalid_dims:
        print(f"Allowed: {sorted(allowed_dims)}")
        for bid, fp, bad in invalid_dims:
            print(f"  {bid} ({fp}): {bad}")

    errors = (1 if duplicates else 0) + (1 if invalid_dims else 0)
    if errors:
        print("\nValidation failed")
        return 1

    print("\nValidation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

