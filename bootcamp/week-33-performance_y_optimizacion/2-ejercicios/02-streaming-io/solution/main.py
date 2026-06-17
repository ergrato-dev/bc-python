"""
Ejercicio 02: Streaming I/O — SOLUCIÓN
"""
from __future__ import annotations

import hashlib
import json
import tracemalloc
from pathlib import Path
from typing import Iterator

CATEGORIES = ["documental", "publicidad", "entrevista", "institucional", "deportes"]


def checksum_streaming(path: Path, chunk_size: int = 4 * 1024 * 1024) -> str:
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            sha.update(chunk)
    return sha.hexdigest()


def iter_jsonl(path: Path, encoding: str = "utf-8") -> Iterator[dict[str, object]]:
    with open(path, encoding=encoding) as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def count_by_category(path: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in iter_jsonl(path):
        cat = str(record.get("category", "unknown"))
        counts[cat] = counts.get(cat, 0) + 1
    return counts


def load_full(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def generate_test_jsonl(path: Path, n: int = 1000) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for i in range(n):
            record = {
                "id": i,
                "title": f"Asset {i:04d} de Studio BC",
                "category": CATEGORIES[i % len(CATEGORIES)],
                "tags": [f"tag{j}" for j in range(5)],
                "duration_s": (i % 300) + 30,
            }
            f.write(json.dumps(record) + "\n")


if __name__ == "__main__":
    test_file = Path("test_assets.jsonl")
    generate_test_jsonl(test_file, n=10_000)
    print(f"Archivo generado: {test_file} ({test_file.stat().st_size / 1024:.1f} KB)\n")

    sha = checksum_streaming(test_file)
    print(f"SHA-256 (streaming): {sha[:16]}...")

    first_5 = []
    for record in iter_jsonl(test_file):
        first_5.append(record)
        if len(first_5) >= 5:
            break
    print(f"Primeros 5 records: {[r['id'] for r in first_5]}")

    counts = count_by_category(test_file)
    print(f"\nConteo por categoría: {counts}")
    assert len(counts) == len(CATEGORIES)

    print("\n=== Comparación de memoria ===")
    for label, fn in [
        ("load_full (lista)", lambda p: load_full(p)),
        ("iter_jsonl (streaming)", lambda p: sum(1 for _ in iter_jsonl(p))),
    ]:
        tracemalloc.start()
        result = fn(test_file)
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"{label}: peak = {peak / 1024:.1f} KB  (result={result if isinstance(result, int) else len(result)})")

    test_file.unlink(missing_ok=True)
    print("\nOK — Ejercicio 02 completado")
