"""
Ejercicio 02 — gather, TaskGroup y timeout
Studio BC: descarga masiva de assets con mirrors y progreso en tiempo real.
"""

import asyncio
import time

# Assets con (nombre, delay_en_segundos)
ASSETS: list[tuple[str, float]] = [
    ("intro_reel.mp4", 1.5),
    ("logo_hd.png", 0.8),
    ("soundtrack.wav", 2.0),
    ("thumbnail.jpg", 0.4),
    ("credits.mp4", 3.0),
]

# Mirrors para el paso 1 (el mismo asset disponible en 3 servidores)
MIRRORS: list[tuple[str, float]] = [
    ("cdn-us.example.com", 3.0),
    ("cdn-eu.example.com", 1.2),
    ("cdn-sa.example.com", 2.5),
]


async def download(name: str, delay: float, source: str = "cdn") -> str:
    """Simula descarga de un asset."""
    await asyncio.sleep(delay)
    return f"✅ {name} desde {source} ({delay}s)"


# ─────────────────────────────────────────────
# PASO 1 — asyncio.wait(FIRST_COMPLETED)
# ─────────────────────────────────────────────

# TODO: implementa fastest_mirror(asset_name) que:
# 1. Crea un task por cada mirror en MIRRORS
# 2. Usa asyncio.wait(..., return_when=asyncio.FIRST_COMPLETED)
# 3. Imprime el resultado del primero en terminar
# 4. Cancela los tasks pendientes
# 5. Retorna el resultado del ganador

# async def fastest_mirror(asset_name: str) -> str:
#     tasks = {
#         asyncio.create_task(
#             download(asset_name, delay, server), name=server
#         )
#         for server, delay in MIRRORS
#     }
#     ...


# ─────────────────────────────────────────────
# PASO 2 — gather → TaskGroup
# ─────────────────────────────────────────────

async def download_batch_gather(assets: list[tuple[str, float]]) -> list[str]:
    """Versión con gather — ya implementada."""
    results = await asyncio.gather(
        *[download(name, delay) for name, delay in assets]
    )
    return list(results)


# TODO: implementa download_batch_taskgroup() usando async with asyncio.TaskGroup() as tg:
# Crea los tasks con tg.create_task() y recoge los resultados con task.result().

# async def download_batch_taskgroup(assets: list[tuple[str, float]]) -> list[str]:
#     ...


# ─────────────────────────────────────────────
# PASO 3 — timeout global
# ─────────────────────────────────────────────

ASSETS_WITH_SLOW: list[tuple[str, float]] = [
    *ASSETS[:3],
    ("4k_master.mp4", 8.0),   # este tardará demasiado
]

# TODO: implementa download_with_timeout(assets, timeout_secs).
# Envuelve la llamada a gather con `async with asyncio.timeout(timeout_secs):`.
# Captura TimeoutError e imprime un mensaje claro.

# async def download_with_timeout(
#     assets: list[tuple[str, float]], timeout_secs: float
# ) -> list[str]:
#     ...


# ─────────────────────────────────────────────
# PASO 4 — progreso con as_completed
# ─────────────────────────────────────────────

# TODO: implementa download_with_progress(assets) usando asyncio.as_completed().
# Imprime cada resultado con su tiempo desde el inicio, en orden de finalización:
#   [0.4s] thumbnail.jpg OK
#   [0.8s] logo_hd.png OK
#   ...

# async def download_with_progress(assets: list[tuple[str, float]]) -> None:
#     start = time.perf_counter()
#     ...


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────

async def main() -> None:
    print("── Paso 2: gather vs TaskGroup ──")
    r1 = await download_batch_gather(ASSETS)
    print(f"gather: {len(r1)} assets")

    # Descomenta según avances:
    # print("\n── Paso 1: fastest mirror ──")
    # winner = await fastest_mirror("promo_edit.mp4")
    # print(f"ganador: {winner}")

    # print("\n── Paso 2: TaskGroup ──")
    # r2 = await download_batch_taskgroup(ASSETS)
    # assert r1 == list(r2), "gather y TaskGroup deben dar el mismo resultado"
    # print("✅ resultados idénticos")

    # print("\n── Paso 3: timeout ──")
    # await download_with_timeout(ASSETS_WITH_SLOW, timeout_secs=5.0)

    # print("\n── Paso 4: progreso ──")
    # await download_with_progress(ASSETS)


if __name__ == "__main__":
    asyncio.run(main())
