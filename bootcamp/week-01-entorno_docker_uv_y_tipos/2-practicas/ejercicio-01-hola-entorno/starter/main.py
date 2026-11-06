"""Ejercicio 01: tu primer programa ejecutado con uv.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python main.py
"""

import platform

print("Ejercicio 01 · Hola, entorno")

# ============================================
# PASO 3: una función que saluda
# ============================================
# `def` crea la función; `name: str` dice que espera un texto y `-> str` que
# devuelve otro. strip() quita los espacios de los lados.
# Descomenta las siguientes líneas:
# def greet(name: str) -> str:
#     name = name.strip()
#     if name == "":
#         return "Hola, mundo"
#     return f"Hola, {name}"
#
#
# print(greet("Ana"))
# print(greet("   "))

# ============================================
# PASO 4: la versión del intérprete
# ============================================
# platform.python_version() devuelve la versión de Python que ejecuta este
# archivo. Si no es 3.14.10, uv no está usando la versión fijada.
# Descomenta las siguientes líneas:
# def python_summary() -> str:
#     return f"Python {platform.python_version()}"
#
#
# print(python_summary())
