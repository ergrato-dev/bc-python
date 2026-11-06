"""meteo: un paquete de ejemplo con dos módulos, convert y stats.

Una carpeta con un __init__.py es un paquete. Este archivo se ejecuta la primera vez
que se importa el paquete o cualquiera de sus módulos.
"""

print("  [cargando el paquete meteo]")

# ============================================
# PASO 2: el __init__.py reexporta
# ============================================
# Sube nombres de los módulos al paquete: `from meteo import c_to_f`.
# Descomenta las siguientes líneas:
# from meteo.convert import c_to_f
# from meteo.stats import mean

# ============================================
# PASO 3: __all__
# ============================================
# Los nombres que trae `from meteo import *`, y la lista oficial de la API.
# Descomenta las siguientes líneas:
# __all__ = ["c_to_f", "mean"]
