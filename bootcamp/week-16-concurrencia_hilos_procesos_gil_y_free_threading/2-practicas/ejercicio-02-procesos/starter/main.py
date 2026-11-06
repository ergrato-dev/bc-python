"""Ejercicio 02 · Procesos: CPU con hilos y con procesos, el guardián y el coste de pickle.

Ejecuta `uv run python main.py` después de cada paso. Los tiempos dependen de tu CPU:
fíjate en la proporción entre ellos, no en los segundos exactos.

Cada paso es una función marcada con @step; el bloque final las ejecuta en orden.
Así, cuando un proceso hijo importa este archivo, solo define funciones y no repite
los pasos (paso 4).
"""

import multiprocessing
import os
import pickle
import time
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

STEPS: list[Callable[[], None]] = []
LIMITS = [400_000] * 4


def step(function: Callable[[], None]) -> Callable[[], None]:
    """Apunta un paso para ejecutarlo al final, dentro del guardián."""
    STEPS.append(function)
    return function


def count_primes(limit: int) -> int:
    """Cuenta los primos menores que `limit` probando divisores: trabajo de CPU puro."""
    count = 0
    for number in range(2, limit):
        if all(number % divisor for divisor in range(2, int(number**0.5) + 1)):
            count += 1
    return count


def timed(label: str, run: Callable[[], object]) -> float:
    """Ejecuta `run`, escribe cuánto tardó y devuelve los segundos."""
    start = time.perf_counter()
    run()
    elapsed = time.perf_counter() - start
    print(f"{label}: {elapsed:.2f} s")
    return elapsed


# ============================================
# PASO 1: Trabajo de CPU, una tarea detrás de otra
# ============================================
# Descomenta las siguientes líneas:
# @step
# def sequential() -> None:
#     print(f"primos < 400 000: {count_primes(LIMITS[0])}")
#     timed("secuencial", lambda: [count_primes(limit) for limit in LIMITS])


# ============================================
# PASO 2: Con 4 hilos
# ============================================
# Descomenta las siguientes líneas:
# @step
# def with_threads() -> None:
#     with ThreadPoolExecutor(max_workers=4) as pool:
#         timed("4 hilos", lambda: list(pool.map(count_primes, LIMITS)))


# ============================================
# PASO 3: Con 4 procesos
# ============================================
# Descomenta las siguientes líneas:
# @step
# def with_processes() -> None:
#     print(f"núcleos disponibles: {os.process_cpu_count()}")
#     with ProcessPoolExecutor(max_workers=4) as pool:
#         timed("4 procesos", lambda: list(pool.map(count_primes, LIMITS)))


# ============================================
# PASO 4: Quién importa este archivo
# ============================================
# Descomenta las siguientes líneas:
# print(f"main.py cargado como {__name__}")


# ============================================
# PASO 5: Lo que no viaja a otro proceso
# ============================================
# Descomenta las siguientes líneas:
# @step
# def not_picklable() -> None:
#     with ProcessPoolExecutor(max_workers=2) as pool:
#         try:
#             print(list(pool.map(lambda limit: limit * 2, [1, 2])))
#         except pickle.PicklingError as problem:
#             print(f"{type(problem).__name__}: {problem}")


# ============================================
# PASO 6: Memoria separada
# ============================================
# Descomenta las siguientes líneas:
# seen: list[int] = []
#
#
# def remember(number: int) -> int:
#     time.sleep(0.1)  # así cada trabajador coge al menos una tarea
#     seen.append(number)
#     return os.getpid()
#
#
# @step
# def separate_memory() -> None:
#     with ThreadPoolExecutor(max_workers=2) as pool:
#         list(pool.map(remember, [1, 2, 3]))
#     print(f"hilos: seen = {sorted(seen)}")
#     seen.clear()
#     with ProcessPoolExecutor(max_workers=2) as pool:
#         pids = set(pool.map(remember, [1, 2, 3]))
#     print(f"procesos: seen = {seen} · hijos: {len(pids)} · ¿yo?: {os.getpid() in pids}")


# ============================================
# PASO 7: Muchas tareas pequeñas y chunksize
# ============================================
# Descomenta las siguientes líneas:
# @step
# def small_tasks() -> None:
#     small = [50] * 20_000
#     timed("20 000 tareas, secuencial", lambda: [count_primes(limit) for limit in small])
#     with ProcessPoolExecutor(max_workers=4) as pool:
#         timed("20 000 tareas, procesos", lambda: list(pool.map(count_primes, small)))
#         timed(
#             "20 000 tareas, chunksize=500",
#             lambda: list(pool.map(count_primes, small, chunksize=500)),
#         )


# ============================================
# PASO 8: Cómo nace un proceso
# ============================================
# Descomenta las siguientes líneas:
# @step
# def start_method() -> None:
#     print(f"método de arranque: {multiprocessing.get_start_method()}")
#     print(f"disponibles: {multiprocessing.get_all_start_methods()}")


if __name__ == "__main__":
    print("Ejercicio 02 · Procesos")
    for run_step in STEPS:
        run_step()
