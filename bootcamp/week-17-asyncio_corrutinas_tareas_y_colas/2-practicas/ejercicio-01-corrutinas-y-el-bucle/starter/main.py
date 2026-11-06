"""Ejercicio 01 · Corrutinas y el bucle: async def, await, tareas, gather y no bloquear.

Ejecuta `uv run python main.py` después de cada paso. Los tiempos son de tu máquina:
compáralos con los del README por su orden de magnitud, no por el último decimal.
"""

import asyncio
import time

# Cuatro "descargas" falsas: cada una espera medio segundo, como una lectura de red.
STATIONS = ["Norte", "Sur", "Oriente", "Occidente"]
DELAY = 0.5


async def download(station: str) -> str:
    """Simula una lectura lenta: mientras espera, el bucle puede atender a otras tareas."""
    await asyncio.sleep(DELAY)
    return f"{station};{len(station) * 3.5:.1f}"


print("Ejercicio 01 · Corrutinas y el bucle")


# ============================================
# PASO 1: Una corrutina no se ejecuta sola
# ============================================
# Descomenta las siguientes líneas:
# pending = download("Norte")
# print(f"download('Norte') es {type(pending).__name__}")
# print(f"asyncio.run da {asyncio.run(pending)!r}")


# ============================================
# PASO 2: await, una detrás de otra
# ============================================
# Descomenta las siguientes líneas:
# async def one_by_one() -> list[str]:
#     return [await download(station) for station in STATIONS]
#
#
# start = time.perf_counter()
# lines = asyncio.run(one_by_one())
# print(f"con await: {time.perf_counter() - start:.1f} s · {lines[0]}")


# ============================================
# PASO 3: Tareas que esperan a la vez
# ============================================
# Descomenta las siguientes líneas:
# async def with_tasks() -> list[str]:
#     tasks = [asyncio.create_task(download(station)) for station in STATIONS]
#     print(f"tareas creadas: {len(asyncio.all_tasks())} (con la principal)")
#     return [await task for task in tasks]
#
#
# start = time.perf_counter()
# lines = asyncio.run(with_tasks())
# print(f"con tareas: {time.perf_counter() - start:.1f} s · {lines[-1]}")


# ============================================
# PASO 4: gather, los resultados en orden
# ============================================
# Descomenta las siguientes líneas:
# async def slow(name: str, seconds: float) -> str:
#     await asyncio.sleep(seconds)
#     print(f"  termina {name}")
#     return name
#
#
# async def gathered() -> list[str]:
#     jobs = [("lento", 0.3), ("medio", 0.2), ("rápido", 0.1)]
#     return await asyncio.gather(*(slow(name, seconds) for name, seconds in jobs))
#
#
# print(f"gather: {asyncio.run(gathered())}")


# ============================================
# PASO 5: Un solo hilo, turnos en cada await
# ============================================
# Descomenta las siguientes líneas:
# import threading
#
#
# async def worker(name: str) -> None:
#     for step in range(2):
#         print(f"  {name}{step} en {threading.current_thread().name}")
#         await asyncio.sleep(0)
#
#
# async def turns() -> None:
#     await asyncio.gather(worker("A"), worker("B"), worker("C"))
#
#
# asyncio.run(turns())


# ============================================
# PASO 6: time.sleep bloquea el bucle
# ============================================
# Descomenta las siguientes líneas:
# def read_slowly(station: str) -> str:
#     time.sleep(DELAY)  # Una función normal que bloquea, como leer un archivo grande.
#     return station
#
#
# async def blocking(station: str) -> str:
#     # Sin await: no cede el turno y el bucle entero se para medio segundo.
#     return read_slowly(station)
#
#
# async def all_blocking() -> list[str]:
#     return await asyncio.gather(*(blocking(station) for station in STATIONS))
#
#
# start = time.perf_counter()
# asyncio.run(all_blocking())
# print(f"con time.sleep: {time.perf_counter() - start:.1f} s")


# ============================================
# PASO 7: to_thread, lo que bloquea a otro hilo
# ============================================
# Descomenta las siguientes líneas:
# async def in_threads() -> list[str]:
#     return await asyncio.gather(*(asyncio.to_thread(read_slowly, s) for s in STATIONS))
#
#
# start = time.perf_counter()
# asyncio.run(in_threads())
# print(f"con to_thread: {time.perf_counter() - start:.1f} s")
