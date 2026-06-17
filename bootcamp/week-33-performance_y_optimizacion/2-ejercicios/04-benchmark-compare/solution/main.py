"""
Ejercicio 04: Benchmark de Implementaciones — SOLUCIÓN
"""
from __future__ import annotations

import hashlib
import timeit
from typing import Any


def process_v1(records: list[dict[str, Any]]) -> list[str]:
    result = []
    for record in records:
        tag_str = ""
        for tag in record.get("tags", []):
            tag_str += tag + ","
        result.append(tag_str.rstrip(","))
    return result


def process_v2(records: list[dict[str, Any]]) -> list[str]:
    return [",".join(record.get("tags", [])) for record in records]


def checksum_v1(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def checksum_v2(data: bytes, chunk_size: int = 65536) -> str:
    sha = hashlib.sha256()
    offset = 0
    while offset < len(data):
        sha.update(data[offset: offset + chunk_size])
        offset += chunk_size
    return sha.hexdigest()


def run_benchmark(
    label_a: str,
    fn_a,
    label_b: str,
    fn_b,
    args: tuple,
    n: int = 100,
) -> dict[str, float]:
    time_a = timeit.timeit(lambda: fn_a(*args), number=n)
    time_b = timeit.timeit(lambda: fn_b(*args), number=n)
    faster = label_a if time_a < time_b else label_b
    speedup = max(time_a, time_b) / min(time_a, time_b)
    return {label_a: time_a, label_b: time_b, "speedup": speedup, "faster": faster}


def print_benchmark_table(results: dict[str, float]) -> None:
    speedup = results.pop("speedup")
    faster = results.pop("faster")
    for label, t in results.items():
        marker = " ◀ más rápida" if label == faster else ""
        print(f"  {label}: {t:.4f}s{marker}")
    print(f"  Speedup: {speedup:.1f}×")


SAMPLE_RECORDS = [
    {"id": i, "tags": [f"tag{j}" for j in range(10)]}
    for i in range(1000)
]
SAMPLE_DATA = b"x" * 10_000_000


if __name__ == "__main__":
    print("=== Benchmark: process_v1 vs process_v2 ===\n")
    results = run_benchmark(
        "process_v1 (string concat)", process_v1,
        "process_v2 (join+listcomp)", process_v2,
        args=(SAMPLE_RECORDS,), n=50,
    )
    print_benchmark_table(results)

    print("\n=== Benchmark: checksum_v1 vs checksum_v2 ===\n")
    results = run_benchmark(
        "checksum_v1 (one-shot)", checksum_v1,
        "checksum_v2 (streaming)", checksum_v2,
        args=(SAMPLE_DATA,), n=20,
    )
    print_benchmark_table(results)

    assert process_v1(SAMPLE_RECORDS[:5]) == process_v2(SAMPLE_RECORDS[:5])
    assert checksum_v1(SAMPLE_DATA[:100]) == checksum_v2(SAMPLE_DATA[:100])
    print("\nOK — Ejercicio 04 completado")
