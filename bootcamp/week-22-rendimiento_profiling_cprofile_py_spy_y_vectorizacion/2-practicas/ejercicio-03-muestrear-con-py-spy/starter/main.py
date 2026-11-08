"""Ejercicio 03 · Muestrear con py-spy: record, el gráfico de llamas, --idle y dump.

Este programa no se mide a sí mismo: lo mide py-spy desde fuera, sin tocar el código.
Ejecuta las órdenes del README después de cada paso.
"""

import os
import time
from pathlib import Path

# 200 000 líneas "etiqueta;valor", como un archivo grande ya leído.
LINES = [f"estación-{number % 50};{number % 97},5" for number in range(200_000)]


def parse_values(lines: list[str]) -> list[float]:
    """El valor de cada línea, con la coma decimal cambiada por un punto."""
    return [float(line.split(";")[1].replace(",", ".")) for line in lines]


def checksum(values: list[float]) -> float:
    """Un resumen de los valores que obliga a recorrerlos uno a uno."""
    total = 0.0
    for value in values:
        total = (total * 31 + value) % 1_000_003
    return total


def work(rounds: int) -> float:
    """Analiza las líneas y las resume `rounds` veces: unos segundos de CPU."""
    result = 0.0
    for _ in range(rounds):
        result = checksum(parse_values(LINES))
    return result


print("Ejercicio 03 · py-spy")


# ============================================
# PASO 1: Trabajo de CPU
# ============================================
# Descomenta las siguientes líneas:
# start = time.perf_counter()
# print(f"work: {work(40):.1f} · {time.perf_counter() - start:.2f} s")


# ============================================
# PASO 2: Una espera
# ============================================
# Descomenta las siguientes líneas:
# start = time.perf_counter()
# time.sleep(2)
# print(f"esperando: {time.perf_counter() - start:.2f} s")


# ============================================
# PASO 3: Un programa que no termina
# ============================================
# Descomenta las siguientes líneas:
# def wait_for(path: Path) -> None:
#     """Espera a que exista path, mirando cada décima de segundo."""
#     while not path.exists():
#         time.sleep(0.1)
#
#
# print(f"pid {os.getpid()}: esperando a listo.txt", flush=True)
# wait_for(Path("listo.txt"))
# print("listo")
