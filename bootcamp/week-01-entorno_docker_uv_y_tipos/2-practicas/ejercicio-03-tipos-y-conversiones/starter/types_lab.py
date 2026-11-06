"""Ejercicio 03: tipos básicos de Python y conversiones explícitas.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python types_lab.py
"""

import math

print("Ejercicio 03 · Tipos y conversiones")

# ============================================
# PASO 2: el nombre de cada tipo
# ============================================
# type(x) da la clase del valor; .__name__, su nombre como texto.
# Descomenta las siguientes líneas:
# def type_name(value: object) -> str:
#     return type(value).__name__
#
#
# print("Tipos:", type_name(3), type_name(3.0), type_name("3"), type_name(True), type_name(None))

# ============================================
# PASO 3: de texto a int
# ============================================
# int() ignora los espacios de los lados, pero no acepta decimales.
# Descomenta las siguientes líneas:
# def to_int(text: str) -> int:
#     return int(text)
#
#
# print("Entero:", to_int(" 42 "))
# print("Con decimales:", to_int("4.5"))

# ============================================
# PASO 4: de texto a float, con coma decimal
# ============================================
# float("3,5") falla: se cambia la coma por punto antes de convertir.
# Descomenta las siguientes líneas:
# def to_float(text: str) -> float:
#     return float(text.strip().replace(",", "."))
#
#
# print("Decimal:", to_float("3,5"), to_float(" 2.25 "))

# ============================================
# PASO 5: comparar float
# ============================================
# Un float es una aproximación binaria: == puede fallar con valores "iguales".
# math.isclose compara con una tolerancia.
# Descomenta las siguientes líneas:
# def floats_are_equal(a: float, b: float) -> bool:
#     return math.isclose(a, b)
#
#
# print("0.1 + 0.2 == 0.3:", 0.1 + 0.2 == 0.3)
# print("isclose:", floats_are_equal(0.1 + 0.2, 0.3))
# print("Con 17 decimales:", f"{0.1 + 0.2:.17f}")

# ============================================
# PASO 6: int sin límite
# ============================================
# ** es la potencia. len(str(n)) cuenta las cifras de n.
# Descomenta las siguientes líneas:
# def digits_of_power_of_two(exponent: int) -> int:
#     return len(str(2**exponent))
#
#
# print("Cifras de 2**10:", digits_of_power_of_two(10))
# print("Cifras de 2**1000:", digits_of_power_of_two(1000))

# ============================================
# PASO 7: None no es 0 ni ""
# ============================================
# `not value` es True para 0 y "": no sirve para saber si falta el dato.
# Descomenta las siguientes líneas:
# def is_missing(value: object) -> bool:
#     return value is None
#
#
# print("Faltan:", is_missing(None), is_missing(0), is_missing(""), is_missing(0.0))
# print("Con not:", not None, not 0, not "", not 0.0)
