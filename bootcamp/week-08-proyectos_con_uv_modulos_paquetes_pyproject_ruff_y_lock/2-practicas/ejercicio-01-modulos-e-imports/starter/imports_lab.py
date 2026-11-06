"""Ejercicio 01: módulos e imports.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python imports_lab.py
"""

import sys

print("Ejercicio 01 · Módulos e imports")

# ============================================
# PASO 1: import y el caché de módulos
# ============================================
# import ejecuta units.py una vez y guarda el módulo en sys.modules.
# Descomenta las siguientes líneas:
# import units
#
# print("10 millas:", units.miles_to_km(10), "km")
# print("Constante:", units.KM_PER_MILE)
# import units
#
# print("¿En el caché?", "units" in sys.modules)

# ============================================
# PASO 2: from ... import y los alias
# ============================================
# from copia nombres sueltos a este archivo; as les pone otro nombre.
# Descomenta las siguientes líneas:
# from units import celsius_to_fahrenheit as c_to_f
# from units import miles_to_km
#
# print("Maratón:", round(miles_to_km(26.2188), 1), "km")
# print("25 °C:", c_to_f(25), "°F")
# print("¿Mismo objeto?", miles_to_km is units.miles_to_km)
# print("Nombres de units:", [name for name in dir(units) if not name.startswith("_")])

# ============================================
# PASO 3: __name__
# ============================================
# Dentro de un módulo importado, __name__ es su nombre; en el archivo que ejecutas, "__main__".
# Descomenta las siguientes líneas:
# print("Aquí __name__ vale:", repr(__name__))
# print("Y en units:", repr(units.__name__))

# ============================================
# PASO 4: dónde busca Python
# ============================================
# sys.path es la lista de carpetas donde import busca; la primera, la del script.
# Descomenta las siguientes líneas:
# from pathlib import Path
#
# print("Primera carpeta:", Path(sys.path[0]).name)
# print("Carpeta de trabajo:", Path.cwd().name)
# print("units viene de:", Path(units.__file__).name)
# for folder in sys.path[1:]:
#     if folder.endswith("lib/python3.14"):
#         print("La biblioteca estándar:", Path(folder).name)

# ============================================
# PASO 5: un archivo que tapa la biblioteca estándar
# ============================================
# La carpeta del script va antes que la biblioteca estándar en sys.path.
# Descomenta las siguientes líneas:
# import statistics
#
# print("Mediana:", statistics.median([8, 12.5, 30.7]))
