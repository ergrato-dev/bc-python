"""Ejercicio 02 · Índices, vistas y máscaras: elegir partes de un array sin bucles.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import numpy as np

# Las medidas de tres días en cuatro estaciones: una fila por día, una columna por estación.
STATIONS = np.array(["Norte", "Sur", "Este", "Oeste"])
WEEK = np.array(
    [
        [12.5, 8.0, 55.1, 61.0],
        [48.9, 9.5, 40.2, 33.3],
        [20.0, 71.4, 5.5, 18.8],
    ]
)

print("Ejercicio 02 · Índices, vistas y máscaras")


# ============================================
# PASO 1: Índices y cortes
# ============================================
# Descomenta las siguientes líneas:
# first_day = WEEK[0]
# print("primer día:   ", first_day)
# print("último valor: ", first_day[-1], "· del 1 al 2:", first_day[1:3], "· salteados:", first_day[::2])
# print("día 1, Este:  ", WEEK[1, 2])
# print("columna Sur:  ", WEEK[:, 1])
# print("bloque:\n", WEEK[1:, :2])


# ============================================
# PASO 2: Un corte es una vista
# ============================================
# Descomenta las siguientes líneas:
# week = WEEK.copy()
# north = week[:, 0]
# north[:] = 0
# print("tras poner a 0 la vista:\n", week)
# safe = WEEK[:, 0].copy()
# safe[:] = -1
# print("WEEK sigue igual:", WEEK[:, 0])


# ============================================
# PASO 3: Índices con una lista: una copia
# ============================================
# Descomenta las siguientes líneas:
# chosen = WEEK[0, [3, 0, 0]]
# print("elegidos:", chosen)
# chosen[:] = 0
# print("WEEK[0] sigue igual:", WEEK[0])
# print("filas 2 y 0:\n", WEEK[[2, 0]])
# print("una por día:", WEEK[[0, 1, 2], [3, 0, 1]])


# ============================================
# PASO 4: Máscaras
# ============================================
# Descomenta las siguientes líneas:
# high = WEEK > 50
# print(high)
# print("altos:", WEEK[high], "· cuántos:", np.count_nonzero(high))
# middle = (WEEK >= 10) & (WEEK <= 50)
# print("medios:", WEEK[middle])
# print("ni altos ni medios:", WEEK[~(high | middle)])
# try:
#     WEEK[(WEEK >= 10) and (WEEK <= 50)]
# except ValueError as problem:
#     print("ValueError:", problem)


# ============================================
# PASO 5: Cambiar lo que cumple una condición
# ============================================
# Descomenta las siguientes líneas:
# capped = WEEK.copy()
# capped[capped > 60] = 60
# print("con tope 60:\n", capped)
# print(np.where(WEEK[0] > 50, "alto", "no alto"))
# print("posiciones de los altos del día 0:", np.flatnonzero(WEEK[0] > 50))
# print("días con algún alto:", (WEEK > 50).any(axis=1))


# ============================================
# PASO 6: Ordenar y elegir los mayores
# ============================================
# Descomenta las siguientes líneas:
# day = WEEK[1]
# print("ordenados:", np.sort(day), "· posiciones:", np.argsort(day))
# order = np.argsort(day)[::-1]
# print("de mayor a menor:", STATIONS[order], day[order])
# row, column = np.unravel_index(WEEK.argmax(), WEEK.shape)
# print(f"el mayor: {WEEK.max()} el día {row} en {STATIONS[column]}")
# best = WEEK.argmax(axis=1)
# print("la estación más alta de cada día:", STATIONS[best])
