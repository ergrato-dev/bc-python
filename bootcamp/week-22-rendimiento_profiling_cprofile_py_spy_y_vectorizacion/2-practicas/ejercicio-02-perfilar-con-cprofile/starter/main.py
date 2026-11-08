"""Ejercicio 02 · Perfilar con cProfile: encontrar dónde se va el tiempo y arreglarlo.

Ejecuta `uv run python main.py` después de cada paso. Los tiempos son de tu máquina:
compáralos con los del README por su orden de magnitud, no por el último decimal.
"""

import cProfile
import io
import pstats
import random
import time
from collections import defaultdict

Record = tuple[str, float]


def make_records(count: int, labels: int) -> list[Record]:
    """count registros (etiqueta, valor) con `labels` etiquetas distintas, siempre los mismos."""
    rng = random.Random(22)
    return [(f"estación-{rng.randrange(labels)}", rng.uniform(0, 80)) for _ in range(count)]


def unique_labels(records: list[Record]) -> list[str]:
    """Las etiquetas distintas, en el orden en que aparecen."""
    seen: list[str] = []
    for label, _ in records:
        if label not in seen:
            seen.append(label)
    return seen


def values_of(records: list[Record], label: str) -> list[float]:
    """Los valores de una etiqueta: recorre todos los registros."""
    return [value for name, value in records if name == label]


def median(values: list[float]) -> float:
    """El valor del medio de los valores ordenados (o la media de los dos del medio)."""
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def report(records: list[Record]) -> dict[str, float]:
    """La mediana de cada etiqueta, en el orden en que aparecen."""
    return {label: median(values_of(records, label)) for label in unique_labels(records)}


RECORDS = make_records(20_000, 2_000)

print("Ejercicio 02 · Perfilar")


# ============================================
# PASO 1: Cuánto tarda
# ============================================
# Descomenta las siguientes líneas:
# start = time.perf_counter()
# medians = report(RECORDS)
# print(f"report: {time.perf_counter() - start:.2f} s · {len(medians)} etiquetas")


# ============================================
# PASO 2: Perfilar con cProfile, por tiempo acumulado
# ============================================
# Descomenta las siguientes líneas:
# profiler = cProfile.Profile()
# start = time.perf_counter()
# profiler.runcall(report, RECORDS)
# print(f"report con cProfile: {time.perf_counter() - start:.2f} s")
#
#
# def show(sort: str, limit: int) -> None:
#     """Las `limit` funciones con más tiempo según `sort`, sin rutas largas."""
#     text = io.StringIO()
#     stats = pstats.Stats(profiler, stream=text).strip_dirs().sort_stats(sort)
#     stats.print_stats(limit)
#     lines = text.getvalue().splitlines()
#     start = next(i for i, line in enumerate(lines) if "ncalls" in line)
#     print("\n".join(lines[start : start + limit + 1]))
#
#
# show("cumulative", 6)


# ============================================
# PASO 3: Por tiempo propio
# ============================================
# Descomenta las siguientes líneas:
# print("---")
# show("tottime", 5)


# ============================================
# PASO 4: Quién la llama
# ============================================
# Descomenta las siguientes líneas:
# print("---")
# text = io.StringIO()
# pstats.Stats(profiler, stream=text).strip_dirs().print_callers("values_of")
# print("\n".join(line for line in text.getvalue().splitlines() if "values_of" in line))


# ============================================
# PASO 5: Agrupar una vez
# ============================================
# Descomenta las siguientes líneas:
# def report_grouped(records: list[Record]) -> dict[str, float]:
#     """Lo mismo que report, recorriendo los registros una sola vez."""
#     groups: defaultdict[str, list[float]] = defaultdict(list)
#     for label, value in records:
#         groups[label].append(value)
#     return {label: median(values) for label, values in groups.items()}
#
#
# start = time.perf_counter()
# grouped = report_grouped(RECORDS)
# print(f"report_grouped: {time.perf_counter() - start:.3f} s · igual: {grouped == medians}")


# ============================================
# PASO 6: Perfilar otra vez
# ============================================
# Descomenta las siguientes líneas:
# profiler = cProfile.Profile()
# profiler.runcall(report_grouped, RECORDS)
# print("---")
# show("tottime", 4)
