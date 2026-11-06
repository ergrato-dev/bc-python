"""Ejercicio 04: generadores.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python generator_lab.py
"""

import itertools
import sys
from collections.abc import Generator, Iterable, Iterator

print("Ejercicio 04 · Generadores")

# ============================================
# PASO 1: yield pausa la función
# ============================================
# Descomenta las siguientes líneas:
# def countdown(start: int) -> Iterator[int]:
#     print("    empieza")
#     while start > 0:
#         print(f"    antes de dar {start}")
#         yield start
#         start -= 1
#     print("    termina")
#
#
# gen = countdown(2)
# print("Llamar no ejecuta nada:", type(gen).__name__)
# print("next:", next(gen))
# print("next:", next(gen))
# print("next con valor por defecto:", next(gen, "fin"))
# print("Con un for:", list(countdown(3)))

# ============================================
# PASO 2: memoria: lista frente a generador
# ============================================
# Descomenta las siguientes líneas:
# squares_list = [n * n for n in range(1_000_000)]
# squares_gen = (n * n for n in range(1_000_000))
# print(f"Lista: {sys.getsizeof(squares_list):,} bytes · generador: {sys.getsizeof(squares_gen)} bytes")
# print("Misma suma:", sum(squares_list) == sum(squares_gen))
# print("¿Y si sumo otra vez el generador?", sum(squares_gen))

# ============================================
# PASO 3: generadores infinitos e islice
# ============================================
# Descomenta las siguientes líneas:
# def readings_forever(start: float, step: float) -> Iterator[float]:
#     value = start
#     while True:
#         yield value
#         value += step
#
#
# print("Las 4 primeras:", list(itertools.islice(readings_forever(10.0, 2.5), 4)))
# print("Hasta pasar de 20:", list(itertools.takewhile(lambda v: v <= 20, readings_forever(10.0, 2.5))))
# print("En lotes de 2:", list(itertools.batched(itertools.islice(readings_forever(1.0, 1.0), 5), 2)))

# ============================================
# PASO 4: una tubería de generadores
# ============================================
# Cada etapa pide un valor a la anterior solo cuando la siguiente se lo pide a ella.
# Descomenta las siguientes líneas:
# RAW = ["Norte;12,5", "# nota", "Sur;NA", "Centro;8", "basura", "Este;55,1"]
#
#
# def read(lines: Iterable[str]) -> Iterator[str]:
#     for line in lines:
#         print(f"    lee {line!r}")
#         yield line
#
#
# def parse(lines: Iterable[str]) -> Iterator[float]:
#     for line in lines:
#         _, sep, text = line.partition(";")
#         if sep and text != "NA":
#             yield float(text.replace(",", "."))
#
#
# def above(values: Iterable[float], limit: float) -> Iterator[float]:
#     return (value for value in values if value > limit)
#
#
# pipeline = above(parse(read(RAW)), 10.0)
# print("Tubería creada; aún no se ha leído nada")
# print("Primer valor alto:", next(pipeline))
# print("El resto:", list(pipeline))

# ============================================
# PASO 5: yield from y el retorno de un generador
# ============================================
# Descomenta las siguientes líneas:
# def all_values(groups: dict[str, list[float]]) -> Iterator[float]:
#     for values in groups.values():
#         yield from values
#
#
# def numbered(lines: list[str]) -> Generator[str, None, str]:
#     yield from (f"{n}: {line}" for n, line in enumerate(lines, start=1))
#     return "sin más líneas"
#
#
# print("yield from:", list(all_values({"Norte": [12.5, 48.9], "Sur": [8.0]})))
# lines = numbered(["Norte;12,5", "Sur;8"])
# print(next(lines), "·", next(lines))
# try:
#     next(lines)
# except StopIteration as stop:
#     print("StopIteration con valor:", stop.value)
