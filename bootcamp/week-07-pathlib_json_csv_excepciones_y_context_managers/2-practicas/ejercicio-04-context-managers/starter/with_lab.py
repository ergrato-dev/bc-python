"""Ejercicio 04: context managers.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python with_lab.py
"""

import time
from collections.abc import Iterator
from contextlib import contextmanager, suppress
from pathlib import Path

print("Ejercicio 04 · Context managers")

OUT = Path(__file__).parent / "salida"
OUT.mkdir(exist_ok=True)

# ============================================
# PASO 1: with cierra también cuando hay un error
# ============================================
# El archivo se cierra al salir del bloque, salga como salga.
# Descomenta las siguientes líneas:
# path = OUT / "a-medias.txt"
# try:
#     with path.open("w", encoding="utf-8") as file:
#         file.write("Norte;12,5\n")
#         print("Dentro, ¿cerrado?", file.closed)
#         raise ValueError("algo falló a mitad")
# except ValueError as error:
#     print("Capturado:", error)
# print("Fuera, ¿cerrado?", file.closed)
# print("Se guardó:", path.read_text(encoding="utf-8").splitlines())

# ============================================
# PASO 2: un context manager propio
# ============================================
# Lo de antes del yield es la entrada; lo del finally, la salida, pase lo que pase.
# Descomenta las siguientes líneas:
# @contextmanager
# def announce(name: str) -> Iterator[str]:
#     print(f"  entra en {name}")
#     try:
#         yield name.upper()
#     finally:
#         print(f"  sale de {name}")
#
#
# with announce("lectura") as label:
#     print("  cuerpo con", label)
# try:
#     with announce("escritura"):
#         raise OSError("disco lleno")
# except OSError as error:
#     print("  capturado fuera:", error)

# ============================================
# PASO 3: un cronómetro
# ============================================
# El mismo patrón mide lo que tarda el cuerpo del with.
# Descomenta las siguientes líneas:
# @contextmanager
# def timer(name: str) -> Iterator[None]:
#     start = time.perf_counter()
#     try:
#         yield
#     finally:
#         print(f"  {name}: {(time.perf_counter() - start) * 1000:.1f} ms")
#
#
# with timer("ordenar un millón"):
#     sorted(range(1_000_000), reverse=True)
# with timer("sumar un millón"):
#     sum(range(1_000_000))

# ============================================
# PASO 4: dos archivos en un with, y suppress
# ============================================
# Lee de uno y escribe en otro; suppress ignora un error concreto a propósito.
# Descomenta las siguientes líneas:
# source = OUT / "origen.txt"
# target = OUT / "destino.txt"
# source.write_text("norte;12,5\nsur;8\n", encoding="utf-8")
# with (
#     source.open(encoding="utf-8") as reader,
#     target.open("w", encoding="utf-8") as writer,
# ):
#     for line in reader:
#         writer.write(line.capitalize())
# print("Destino:", target.read_text(encoding="utf-8").splitlines())
# with suppress(FileNotFoundError):
#     (OUT / "temporal.tmp").unlink()
#     print("Esta línea no se escribe")
# print("Siguió sin error")
