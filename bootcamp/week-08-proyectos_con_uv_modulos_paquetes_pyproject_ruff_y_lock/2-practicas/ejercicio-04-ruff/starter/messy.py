"""Ejercicio 04: un archivo que funciona... casi. ruff encuentra lo que falla.

Ejecuta:
    uv run python messy.py
    uv run ruff check
"""
import os
import sys, json
from typing import List, Optional


def add_reading(value: float, readings: list[float] = []) -> list[float]:
    readings.append(value)
    return readings


def describe(value: Optional[float]) -> str:
    if value == None:
        return 'sin dato'
    doubled = value*2
    return "valor: %s" % value


def mean(values: List[float]) -> float:
    total = 0
    for i in range(len(values)):
        total += values[i]
    return total/len(values)


print(f"Ejercicio 04 · ruff")
print("primera lectura:", add_reading(8.0))
print("segunda lectura:", add_reading(12.5))
print(describe(None), "|", describe(30.7))
print("media:", round(mean([8.0, 12.5, 30.7]), 1))
