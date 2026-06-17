"""
Ejercicio 02: Streaming I/O
============================
Procesa un archivo JSONL (JSON Lines) grande sin cargarlo completo en memoria.
Compara uso de RAM: carga completa vs streaming.

Ejecutar: python main.py
"""
from __future__ import annotations

import hashlib
import json
import tracemalloc
from pathlib import Path
from typing import Iterator


# ── Funciones a implementar ───────────────────────────────────────────────────

def checksum_streaming(path: Path, chunk_size: int = 4 * 1024 * 1024) -> str:
    """
    Calcula SHA-256 de un archivo sin cargarlo completo en memoria.

    TODO:
    - sha = hashlib.sha256()
    - Abrir en "rb", leer en chunks de chunk_size
    - sha.update(chunk) hasta que chunk esté vacío
    - retornar sha.hexdigest()
    """
    raise NotImplementedError


def iter_jsonl(path: Path, encoding: str = "utf-8") -> Iterator[dict[str, object]]:
    """
    Generador que itera registros de un archivo JSONL sin cargarlo en memoria.

    TODO:
    - Abrir path con open(path, encoding=encoding)
    - Para cada línea: stripped, si no vacía → yield json.loads(line)
    """
    raise NotImplementedError


def count_by_category(path: Path) -> dict[str, int]:
    """
    Cuenta registros por categoría leyendo el JSONL en streaming.

    TODO:
    - Inicializar counts: dict[str, int] = {}
    - Usar iter_jsonl() para iterar
    - counts[record["category"]] = counts.get(..., 0) + 1
    - retornar counts
    """
    raise NotImplementedError


def load_full(path: Path) -> list[dict[str, object]]:
    """Carga completa (referencia para comparar memoria)."""
    return json.loads(path.read_text(encoding="utf-8"))


# ── Generador de datos de prueba ──────────────────────────────────────────────

CATEGORIES = ["documental", "publicidad", "entrevista", "institucional", "deportes"]

MOCK_RECORDS = [
    {"id": i, "title": f"Asset {i:04d}", "category": CATEGORIES[i % len(CATEGORIES)]}
    for i in range(50)
]


def generate_test_jsonl(path: Path, n: int = 1000) -> None:
    """Genera un archivo JSONL con N registros de assets."""
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

    # Test: checksum en streaming
    try:
        sha = checksum_streaming(test_file)
        print(f"SHA-256 (streaming): {sha[:16]}...")
    except NotImplementedError:
        sha = hashlib.sha256(test_file.read_bytes()).hexdigest()
        print(f"SHA-256 (fallback):  {sha[:16]}...")

    # Test: iter_jsonl
    try:
        first_5 = []
        for record in iter_jsonl(test_file):
            first_5.append(record)
            if len(first_5) >= 5:
                break
        print(f"Primeros 5 records: {[r['id'] for r in first_5]}")
    except NotImplementedError:
        print("iter_jsonl: NotImplementedError (pendiente)")

    # Test: count_by_category
    try:
        counts = count_by_category(test_file)
        print(f"\nConteo por categoría: {counts}")
        assert len(counts) == len(CATEGORIES)
    except NotImplementedError:
        print("count_by_category: NotImplementedError (pendiente)")

    # Comparar memoria: streaming vs carga completa
    print("\n=== Comparación de memoria ===")
    for fn_name, fn in [("load_full", load_full), ("iter_count", lambda p: sum(1 for _ in (iter_jsonl(p) if True else [])))]:
        try:
            tracemalloc.start()
            result = fn(test_file)
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            print(f"{fn_name}: peak = {peak / 1024:.1f} KB")
        except NotImplementedError:
            tracemalloc.stop()
            print(f"{fn_name}: NotImplementedError (pendiente)")

    test_file.unlink(missing_ok=True)
    print("\nOK — Ejercicio 02 completado")
