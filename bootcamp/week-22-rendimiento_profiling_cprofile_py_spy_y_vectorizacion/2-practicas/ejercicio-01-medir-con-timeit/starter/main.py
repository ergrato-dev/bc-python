"""Ejercicio 01 · Medir con perf_counter y timeit: ruido, repeticiones y cómo crece.

Ejecuta `uv run python main.py` después de cada paso. Los tiempos son de tu máquina:
compáralos con los del README por su orden de magnitud y por cuál gana, no por el último
decimal.
"""

import statistics
import time
import timeit
from collections import deque
from functools import partial

# 10 000 etiquetas distintas, como las de un archivo grande, y 1 000 que buscar en ellas.
LABELS = [f"estación-{number}" for number in range(10_000)]
WANTED = [f"estación-{number}" for number in range(0, 20_000, 20)]


def count_known(wanted: list[str], known: list[str] | set[str]) -> int:
    """Cuántas de wanted están en known. Con una lista, cada `in` la recorre entera."""
    return sum(label in known for label in wanted)


print("Ejercicio 01 · Medir")


# ============================================
# PASO 1: Una sola medida con perf_counter
# ============================================
# Descomenta las siguientes líneas:
# for attempt in range(3):
#     start = time.perf_counter()
#     found = count_known(WANTED, LABELS)
#     print(f"intento {attempt + 1}: {time.perf_counter() - start:.4f} s · {found} encontradas")


# ============================================
# PASO 2: Repetir y quedarse con el mínimo
# ============================================
# Descomenta las siguientes líneas:
# times = timeit.repeat(lambda: count_known(WANTED, LABELS), number=5, repeat=7)
# per_call = [total / 5 for total in times]
# print(f"lista · mínimo {min(per_call):.4f} s · mediana {statistics.median(per_call):.4f} s")
# print(f"lista · máximo {max(per_call):.4f} s")


# ============================================
# PASO 3: La misma pregunta a un set
# ============================================
# Descomenta las siguientes líneas:
# known = set(LABELS)
# per_call_set = min(timeit.repeat(lambda: count_known(WANTED, known), number=5, repeat=7)) / 5
# print(f"set · mínimo {per_call_set:.6f} s · {min(per_call) / per_call_set:.0f} veces más rápido")
# build = min(timeit.repeat(lambda: set(LABELS), number=5, repeat=7)) / 5
# print(f"crear el set: {build:.6f} s")


# ============================================
# PASO 4: timeit elige cuántas veces
# ============================================
# Descomenta las siguientes líneas:
# timer = timeit.Timer(lambda: "-".join(LABELS))
# loops, total = timer.autorange()
# print(f"join: {loops} vueltas en {total:.2f} s · {total / loops * 1e6:.0f} µs por vuelta")


# ============================================
# PASO 5: Cómo crece con el tamaño
# ============================================
# Descomenta las siguientes líneas:
# def insert_front(n: int) -> None:
#     items: list[int] = []
#     for number in range(n):
#         items.insert(0, number)
#
#
# def append_left(n: int) -> None:
#     items: deque[int] = deque()
#     for number in range(n):
#         items.appendleft(number)
#
#
# for n in (10_000, 20_000, 40_000):
#     list_time = min(timeit.repeat(partial(insert_front, n), number=1, repeat=5))
#     deque_time = min(timeit.repeat(partial(append_left, n), number=1, repeat=5))
#     print(f"n={n:>6} · list.insert(0) {list_time:.4f} s · deque.appendleft {deque_time:.4f} s")


# ============================================
# PASO 6: Tiempo de reloj y tiempo de CPU
# ============================================
# Descomenta las siguientes líneas:
# wall, cpu = time.perf_counter(), time.process_time()
# time.sleep(0.5)
# count_known(WANTED, LABELS)
# print(f"reloj: {time.perf_counter() - wall:.2f} s · CPU: {time.process_time() - cpu:.2f} s")
