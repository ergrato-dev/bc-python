"""Ejercicio 03 · El GIL y free-threading: el mismo programa con GIL y sin él.

Ejecuta cada paso de dos formas y compara:

    uv run python main.py                      # Python 3.14 normal, con GIL
    uv run --python 3.14.10t python main.py    # Python 3.14 free-threaded, sin GIL

Como en el ejercicio 02, cada paso es una función con @step, y el bloque final las
ejecuta dentro del guardián: los subintérpretes del paso 5 también importan este archivo.
"""

import sys
import sysconfig
import threading
import time
from collections.abc import Callable
from concurrent.futures import InterpreterPoolExecutor, ThreadPoolExecutor

STEPS: list[Callable[[], None]] = []
SIZES = [10_000_000] * 4


def step(function: Callable[[], None]) -> Callable[[], None]:
    """Apunta un paso para ejecutarlo al final, dentro del guardián."""
    STEPS.append(function)
    return function


def crunch(size: int) -> int:
    """Suma cuadrados en un bucle de Python: CPU pura, sin esperas."""
    total = 0
    for number in range(size):
        total += number * number
    return total


def timed(label: str, run: Callable[[], object]) -> None:
    start = time.perf_counter()
    run()
    print(f"{label}: {time.perf_counter() - start:.2f} s")


# ============================================
# PASO 1: ¿Qué Python estás usando?
# ============================================
# Descomenta las siguientes líneas:
# @step
# def which_python() -> None:
#     # Py_GIL_DISABLED vale 1 si este Python se compiló sin GIL (el build "t").
#     free_threaded = sysconfig.get_config_var("Py_GIL_DISABLED") == 1
#     print(f"Python {sys.version.split()[0]} · free-threaded: {free_threaded}")
#     print(f"GIL activo: {sys._is_gil_enabled()}")


# ============================================
# PASO 2: Hilos que calculan
# ============================================
# Descomenta las siguientes líneas:
# @step
# def threads_that_compute() -> None:
#     timed("1 hilo, 4 tareas", lambda: [crunch(size) for size in SIZES])
#     with ThreadPoolExecutor(max_workers=4) as pool:
#         timed("4 hilos, 4 tareas", lambda: list(pool.map(crunch, SIZES)))


# ============================================
# PASO 3: Una carrera que el GIL esconde
# ============================================
# Descomenta las siguientes líneas:
# hits = 0
#
#
# def add_many() -> None:
#     global hits
#     for _ in range(200_000):
#         hits += 1  # leer, sumar y escribir: tres pasos, no uno
#
#
# @step
# def hidden_race() -> None:
#     global hits
#     hits = 0
#     threads = [threading.Thread(target=add_many) for _ in range(4)]
#     for thread in threads:
#         thread.start()
#     for thread in threads:
#         thread.join()
#     print(f"hits += 1 sin Lock: esperado 800000 · obtenido {hits}")


# ============================================
# PASO 4: El Lock, con GIL y sin él
# ============================================
# Descomenta las siguientes líneas:
# lock = threading.Lock()
#
#
# def add_many_safely() -> None:
#     global hits
#     for _ in range(200_000):
#         with lock:
#             hits += 1
#
#
# @step
# def race_with_lock() -> None:
#     global hits
#     hits = 0
#     threads = [threading.Thread(target=add_many_safely) for _ in range(4)]
#     start = time.perf_counter()
#     for thread in threads:
#         thread.start()
#     for thread in threads:
#         thread.join()
#     elapsed = time.perf_counter() - start
#     print(f"hits += 1 con Lock: esperado 800000 · obtenido {hits} · {elapsed:.2f} s")


# ============================================
# PASO 5: Subintérpretes, un GIL para cada uno
# ============================================
# Descomenta las siguientes líneas:
# @step
# def subinterpreters() -> None:
#     with InterpreterPoolExecutor(max_workers=4) as pool:
#         timed("4 subintérpretes, 4 tareas", lambda: list(pool.map(crunch, SIZES)))


if __name__ == "__main__":
    print("Ejercicio 03 · El GIL y free-threading")
    for run_step in STEPS:
        run_step()
