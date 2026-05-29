"""
Ejercicio 01 — AsyncIO Básico
Studio BC: verificar assets antes de iniciar edición.
"""

import asyncio
import time

# Assets del proyecto con su delay simulado (segundos)
ASSETS: list[tuple[str, float]] = [
    ("video_raw_01.mp4", 2.0),
    ("audio_bg.wav", 1.0),
    ("logo_overlay.png", 0.5),
    ("audio_02.wav", 1.5),
]


# ─────────────────────────────────────────────
# PASO 1 — función síncrona (punto de partida)
# ─────────────────────────────────────────────

def check_asset_sync(name: str, delay: float) -> str:
    """Simula verificación síncrona bloqueante."""
    time.sleep(delay)
    return f"✅ {name} OK ({delay}s)"


def run_sequential() -> None:
    start = time.perf_counter()
    results = [check_asset_sync(name, delay) for name, delay in ASSETS]
    elapsed = time.perf_counter() - start
    print("\n── Secuencial ──")
    for r in results:
        print(f"  {r}")
    print(f"  Tiempo total: {elapsed:.2f}s\n")


# ─────────────────────────────────────────────
# PASO 2 — convertir a corutina async
# ─────────────────────────────────────────────

# TODO: convierte check_asset_sync en una corutina async.
# Usa `await asyncio.sleep(delay)` en lugar de `time.sleep(delay)`.
# Nombra la función `check_asset`.

# async def check_asset(name: str, delay: float) -> str:
#     ...


# TODO: implementa run_with_tasks() usando asyncio.create_task()
# Crea una tarea por cada asset, luego await cada tarea.
# Mide el tiempo total con time.perf_counter().

# async def run_with_tasks() -> None:
#     start = time.perf_counter()
#     ...


# ─────────────────────────────────────────────
# PASO 3 — usar asyncio.gather()
# ─────────────────────────────────────────────

# TODO: implementa run_with_gather() usando asyncio.gather(*corutinas).
# El resultado debe ser una lista en el mismo orden que ASSETS.

# async def run_with_gather() -> None:
#     start = time.perf_counter()
#     ...


# ─────────────────────────────────────────────
# PASO 4 — manejo de errores con return_exceptions
# ─────────────────────────────────────────────

# TODO: crea check_asset_failable(name, delay) — igual que check_asset
# pero lanza ValueError(f"{name} corrupted") si name == "audio_02.wav".

# async def check_asset_failable(name: str, delay: float) -> str:
#     ...


# TODO: implementa run_with_errors() usando gather(..., return_exceptions=True).
# Para cada resultado: si es Exception, imprime "⚠ {r}", si no, imprime "  {r}".

# async def run_with_errors() -> None:
#     ...


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # Paso 1 (ejecutar siempre para comparar)
    run_sequential()

    # Descomenta según avances:
    # asyncio.run(run_with_tasks())
    # asyncio.run(run_with_gather())
    # asyncio.run(run_with_errors())
