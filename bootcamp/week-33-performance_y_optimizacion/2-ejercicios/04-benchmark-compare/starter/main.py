"""
Ejercicio 04: Benchmark de Implementaciones
=============================================
Compara el tiempo de ejecución de dos implementaciones
del mismo pipeline usando timeit y una función de benchmark manual.

Ejecutar: python main.py
"""
from __future__ import annotations

import hashlib
import json
import time
import timeit
from pathlib import Path
from typing import Any


# ── Dos implementaciones del mismo proceso ────────────────────────────────────

def process_v1(records: list[dict[str, Any]]) -> list[str]:
    """V1: Concatena tags uno por uno con un loop."""
    result = []
    for record in records:
        tag_str = ""
        for tag in record.get("tags", []):
            tag_str += tag + ","
        result.append(tag_str.rstrip(","))
    return result


def process_v2(records: list[dict[str, Any]]) -> list[str]:
    """V2: Usa join + list comprehension."""
    return [",".join(record.get("tags", [])) for record in records]


def checksum_v1(data: bytes) -> str:
    """V1: Pasar datos completos a sha256."""
    return hashlib.sha256(data).hexdigest()


def checksum_v2(data: bytes, chunk_size: int = 65536) -> str:
    """V2: Streaming por chunks (para archivos grandes)."""
    sha = hashlib.sha256()
    offset = 0
    while offset < len(data):
        sha.update(data[offset: offset + chunk_size])
        offset += chunk_size
    return sha.hexdigest()


# ── Función de benchmark a implementar ───────────────────────────────────────

def run_benchmark(
    label_a: str,
    fn_a,
    label_b: str,
    fn_b,
    args: tuple,
    n: int = 100,
) -> dict[str, float]:
    """
    Benchmarca fn_a(*args) y fn_b(*args) con n repeticiones cada uno.
    Retorna {label_a: time_a, label_b: time_b, "speedup": max/min}.

    TODO:
    - timeit.timeit(lambda: fn_a(*args), number=n) → time_a
    - timeit.timeit(lambda: fn_b(*args), number=n) → time_b
    - speedup = max(time_a, time_b) / min(time_a, time_b)
    - retornar dict con los tres valores
    """
    raise NotImplementedError


def print_benchmark_table(results: dict[str, float]) -> None:
    """
    Imprime una tabla comparativa de los resultados del benchmark.

    TODO: formatear e imprimir los resultados de forma legible,
    indicando cuál implementación es más rápida y el speedup.
    """
    raise NotImplementedError


# ── Datos de prueba ───────────────────────────────────────────────────────────

SAMPLE_RECORDS = [
    {"id": i, "tags": [f"tag{j}" for j in range(10)]}
    for i in range(1000)
]
SAMPLE_DATA = b"x" * 10_000_000  # 10 MB


if __name__ == "__main__":
    print("=== Benchmark: process_v1 vs process_v2 ===\n")
    try:
        results = run_benchmark(
            "process_v1 (string concat)", process_v1,
            "process_v2 (join+listcomp)", process_v2,
            args=(SAMPLE_RECORDS,), n=50,
        )
        print_benchmark_table(results)
    except NotImplementedError:
        # Fallback manual
        t1 = timeit.timeit(lambda: process_v1(SAMPLE_RECORDS), number=50)
        t2 = timeit.timeit(lambda: process_v2(SAMPLE_RECORDS), number=50)
        print(f"  process_v1: {t1:.4f}s")
        print(f"  process_v2: {t2:.4f}s")
        print(f"  Speedup: {t1/t2:.1f}× (v2 es más rápida)" if t2 < t1 else f"  Speedup: {t2/t1:.1f}× (v1 es más rápida)")

    print("\n=== Benchmark: checksum_v1 vs checksum_v2 ===\n")
    try:
        results = run_benchmark(
            "checksum_v1 (one-shot)", checksum_v1,
            "checksum_v2 (streaming)", checksum_v2,
            args=(SAMPLE_DATA,), n=20,
        )
        print_benchmark_table(results)
    except NotImplementedError:
        t1 = timeit.timeit(lambda: checksum_v1(SAMPLE_DATA), number=20)
        t2 = timeit.timeit(lambda: checksum_v2(SAMPLE_DATA), number=20)
        print(f"  checksum_v1: {t1:.4f}s")
        print(f"  checksum_v2: {t2:.4f}s")

    # Verificar que ambas versiones producen el mismo resultado
    assert process_v1(SAMPLE_RECORDS[:5]) == process_v2(SAMPLE_RECORDS[:5])
    assert checksum_v1(SAMPLE_DATA[:100]) == checksum_v2(SAMPLE_DATA[:100])
    print("\nOK — Ejercicio 04 completado")
