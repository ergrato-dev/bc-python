"""Ejercicio 04 · concurrent.futures: Future, map, as_completed, errores, esperas y cancelar.

Ejecuta `uv run python main.py` después de cada paso. Todo usa hilos y tareas que
duermen: los tiempos y el orden de la salida son los mismos en cualquier máquina.
"""

import os
import threading
import time
from concurrent.futures import (
    FIRST_COMPLETED,
    Future,
    ThreadPoolExecutor,
    as_completed,
    wait,
)

# Cada estación tarda lo que dice su número, en décimas de segundo.
DELAYS = {"Norte": 3, "Sur": 1, "Oriente": 2}


def read_station(station: str) -> str:
    """Una lectura falsa que tarda DELAYS[station] décimas. "Centro" no existe."""
    if station not in DELAYS:
        raise KeyError(f"estación desconocida: {station}")
    time.sleep(DELAYS[station] / 10)
    return f"{station};{DELAYS[station] * 10}"


print("Ejercicio 04 · concurrent.futures")


# ============================================
# PASO 1: submit y Future
# ============================================
# Descomenta las siguientes líneas:
# with ThreadPoolExecutor(max_workers=2) as pool:
#     future = pool.submit(read_station, "Norte")
#     print(f"recién enviada: done={future.done()} · {future}")
#     print(f"result(): {future.result()}")  # espera a que termine
#     print(f"después: done={future.done()}")


# ============================================
# PASO 2: map frente a as_completed
# ============================================
# Descomenta las siguientes líneas:
# with ThreadPoolExecutor(max_workers=3) as pool:
#     print(f"map: {list(pool.map(read_station, DELAYS))}")
#     futures = [pool.submit(read_station, station) for station in DELAYS]
#     print(f"as_completed: {[future.result() for future in as_completed(futures)]}")


# ============================================
# PASO 3: Errores dentro de una tarea
# ============================================
# Descomenta las siguientes líneas:
# stations = ["Sur", "Centro", "Norte"]
# with ThreadPoolExecutor(max_workers=3) as pool:
#     future = pool.submit(read_station, "Centro")
#     print(f"el error espera en el Future: {future.exception()!r}")
#     try:
#         for line in pool.map(read_station, stations):
#             print(f"map: {line}")
#     except KeyError as problem:
#         print(f"map se para en el primer error: {problem}")
#     names = {pool.submit(read_station, station): station for station in stations}
#     for finished in as_completed(names):
#         try:
#             print(f"as_completed: {finished.result()}")
#         except KeyError as problem:
#             print(f"as_completed sigue: {names[finished]} falló con {problem}")


# ============================================
# PASO 4: No esperar para siempre
# ============================================
# Descomenta las siguientes líneas:
# with ThreadPoolExecutor(max_workers=3) as pool:
#     slow = pool.submit(read_station, "Norte")
#     try:
#         slow.result(timeout=0.1)
#     except TimeoutError:
#         print(f"a los 0.1 s aún no: running={slow.running()}")
#     futures = [pool.submit(read_station, station) for station in DELAYS]
#     first, pending = wait(futures, return_when=FIRST_COMPLETED)
#     print(f"la primera: {[f.result() for f in first]} · pendientes: {len(pending)}")


# ============================================
# PASO 5: Cancelar lo que aún no empezó
# ============================================
# Descomenta las siguientes líneas:
# stations = ["Sur", "Norte", "Oriente"]
# pool = ThreadPoolExecutor(max_workers=1)
# futures = [pool.submit(read_station, station) for station in stations]
# time.sleep(0.05)  # la primera ya ha empezado; las otras esperan su turno
# print(f"cancelar la primera: {futures[0].cancel()} · la segunda: {futures[1].cancel()}")
# pool.shutdown(wait=True, cancel_futures=True)
# print(f"canceladas: {[future.cancelled() for future in futures]}")


# ============================================
# PASO 6: Avisos al terminar
# ============================================
# Descomenta las siguientes líneas:
# def announce(future: Future[str]) -> None:
#     # Lo ejecuta el hilo que terminó la tarea, no el principal.
#     print(f"terminó {future.result()} en {threading.current_thread().name}")
#
#
# with ThreadPoolExecutor(max_workers=1, thread_name_prefix="lector") as pool:
#     pool.submit(read_station, "Sur").add_done_callback(announce)
# print(f"y el principal es {threading.current_thread().name}")


# ============================================
# PASO 7: ¿Cuántos trabajadores por defecto?
# ============================================
# Descomenta las siguientes líneas:
# cpus = os.process_cpu_count() or 1
# with ThreadPoolExecutor() as pool:
#     print(f"núcleos: {cpus} · hilos por defecto: {pool._max_workers}")
#     print(f"min(32, núcleos + 4) = {min(32, cpus + 4)}")
