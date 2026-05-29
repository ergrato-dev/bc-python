"""
Ejercicio 03 — concurrent.futures
Studio BC: paralelizar validación y checksum de assets con código síncrono legacy.
"""

import asyncio
import hashlib
import os
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed

ASSETS = [
    "video_01.mp4",
    "video_02.mp4",
    "image_01.png",
    "audio_01.wav",
    "audio_02.wav",
    "thumbnail.jpg",
    "credits.mp4",
    "intro.mp4",
]


# ─────────────────────────────────────────────
# Funciones síncronas (código "legacy")
# ─────────────────────────────────────────────

def validate_asset_sync(name: str) -> dict[str, object]:
    """Simula validación I/O-bound (ej: descarga y metadata check)."""
    time.sleep(0.8)   # simula red
    return {"name": name, "valid": True, "size_mb": len(name) * 10}


def compute_checksum(data: bytes) -> str:
    """CPU-bound: calcula SHA-256 de un bloque de datos."""
    result = hashlib.sha256(data).digest()
    # simula trabajo CPU adicional
    for _ in range(500_000):
        result = hashlib.sha256(result).digest()
    return result.hex()[:16]


# ─────────────────────────────────────────────
# PASO 1 — secuencial (punto de partida)
# ─────────────────────────────────────────────

def run_sequential() -> None:
    start = time.perf_counter()
    results = [validate_asset_sync(a) for a in ASSETS]
    elapsed = time.perf_counter() - start
    print(f"\n── Secuencial: {len(results)} assets en {elapsed:.2f}s ──")


# ─────────────────────────────────────────────
# PASO 1 — ThreadPoolExecutor con map()
# ─────────────────────────────────────────────

# TODO: implementa run_thread_map() usando ThreadPoolExecutor(max_workers=4)
# y executor.map(validate_asset_sync, ASSETS).
# Mide el tiempo e imprime cuántos assets se validaron.

# def run_thread_map() -> None:
#     start = time.perf_counter()
#     with ThreadPoolExecutor(max_workers=4) as executor:
#         results = list(executor.map(...))
#     elapsed = time.perf_counter() - start
#     print(f"\n── ThreadPool map: {len(results)} assets en {elapsed:.2f}s ──")


# ─────────────────────────────────────────────
# PASO 2 — submit() + as_completed
# ─────────────────────────────────────────────

# TODO: implementa run_thread_submit() usando submit() y as_completed().
# Imprime cada resultado en el orden en que termina, no en el orden de input.
# Maneja posibles excepciones con future.result() en un try/except.

# def run_thread_submit() -> None:
#     with ThreadPoolExecutor(max_workers=4) as executor:
#         future_to_asset = {
#             executor.submit(validate_asset_sync, a): a
#             for a in ASSETS
#         }
#         for future in as_completed(future_to_asset):
#             asset = future_to_asset[future]
#             try:
#                 result = future.result()
#                 print(f"  ✅ {result}")
#             except Exception as e:
#                 print(f"  ❌ {asset}: {e}")


# ─────────────────────────────────────────────
# PASO 3 — ProcessPoolExecutor para CPU-bound
# ─────────────────────────────────────────────

# Bloques de datos para calcular checksums (simula frames de video)
CHUNKS: list[bytes] = [os.urandom(512) for _ in range(os.cpu_count() or 4)]


# TODO: implementa run_process_pool() usando ProcessPoolExecutor(max_workers=...).
# Usa executor.map(compute_checksum, CHUNKS) y compara el tiempo
# con una versión secuencial: [compute_checksum(c) for c in CHUNKS].

# def run_process_pool() -> None:
#     print("\n── CPU-bound: checksum secuencial ──")
#     start = time.perf_counter()
#     seq_results = [compute_checksum(c) for c in CHUNKS]
#     print(f"  secuencial: {time.perf_counter() - start:.2f}s")

#     print("\n── CPU-bound: ProcessPoolExecutor ──")
#     start = time.perf_counter()
#     with ProcessPoolExecutor() as executor:
#         par_results = list(executor.map(compute_checksum, CHUNKS))
#     print(f"  paralelo ({os.cpu_count()} cores): {time.perf_counter() - start:.2f}s")

#     assert seq_results == par_results


# ─────────────────────────────────────────────
# PASO 4 — integrar en async con run_in_executor
# ─────────────────────────────────────────────

# TODO: implementa la corutina process_project(project_assets).
# Debe:
# 1. Validar todos los assets con ThreadPoolExecutor via run_in_executor (I/O)
# 2. Calcular checksum de os.urandom(512) con ProcessPoolExecutor (CPU)
# 3. Retornar {"validated": N, "checksum": "..."}
# Usa: loop = asyncio.get_running_loop()
#      result = await loop.run_in_executor(pool, func, arg)

# async def process_project(project_assets: list[str]) -> dict[str, object]:
#     loop = asyncio.get_running_loop()
#     ...


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    run_sequential()

    # Descomenta según avances:
    # run_thread_map()
    # run_thread_submit()
    # run_process_pool()
    # asyncio.run(process_project(ASSETS[:4]))
