"""Ejercicio 02: paquetes.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python packages_lab.py
"""

print("Ejercicio 02 · Paquetes")

# ============================================
# PASO 1: importar módulos de un paquete
# ============================================
# El camino va con puntos: paquete.módulo.
# Descomenta las siguientes líneas:
# import meteo.convert
# from meteo.stats import mean
#
# print("30 °C:", meteo.convert.c_to_f(30), "°F")
# print("Media:", mean([20.0, 22.5, 19.0]))
# print("Nombre completo:", meteo.convert.__name__)
# print("¿meteo es un paquete?", hasattr(meteo, "__path__"))

# ============================================
# PASO 2: lo que reexporta el __init__.py
# ============================================
# Descomenta el PASO 2 de meteo/__init__.py y después estas líneas:
# from meteo import c_to_f
#
# print("Desde el paquete:", c_to_f(100))
# print("¿La misma función?", c_to_f is meteo.convert.c_to_f)

# ============================================
# PASO 3: __all__
# ============================================
# Descomenta el PASO 3 de meteo/__init__.py y después estas líneas:
# print("Nombres públicos de meteo:", sorted(n for n in vars(meteo) if not n.startswith("_")))
# print("Su __all__:", meteo.__all__)
