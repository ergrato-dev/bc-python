"""Ejercicio 01 · Ganchos de Git con pre-commit.

El programa es pequeño a propósito: lo importante no es lo que calcula, sino lo que
los ganchos le hacen antes de cada commit. Los pasos 3 y 4 le añaden errores que un
gancho detecta, o arregla solo.
"""

READINGS = [12.5, 30.0, 7.5]


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


print("Ejercicio 01 · Ganchos de Git con pre-commit")
print("media:", mean(READINGS))

# ============================================
# PASO 3: Código que ruff arregla solo
# ============================================
# Un import que nadie usa y un formato descuidado: ruff check quita el import y
# ruff format reescribe la función.
# Descomenta las siguientes líneas:
# import math
# def  double( value:float )->float :
#     return value*2
# print("doble:", double(21.0))

# ============================================
# PASO 4: Un error que solo ve mypy
# ============================================
# El programa funciona, pero la función promete un str y devuelve un float.
# Descomenta las siguientes líneas:
# def label(value: float) -> str:
#     return value
# print("etiqueta:", label(12.5))
