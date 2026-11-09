"""Ejercicio 01 · Arrays y dtypes: crear arrays, leer su forma y su tipo, y ver sus vistas.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import numpy as np

print("Ejercicio 01 · Arrays y dtypes")


# ============================================
# PASO 1: Crear arrays
# ============================================
# Descomenta las siguientes líneas:
# readings = np.array([12.5, 8.0, 55.1, 61.0])
# print("de una lista:", readings)
# print("ceros:      ", np.zeros(3))
# print("lleno de 7: ", np.full(3, 7.0))
# print("arange:     ", np.arange(0, 10, 3))
# print("linspace:   ", np.linspace(0, 1, 5))
# squares = np.fromiter((n * n for n in range(5)), dtype=np.int64, count=5)
# print("fromiter:   ", squares)


# ============================================
# PASO 2: Forma, tamaño y memoria
# ============================================
# Descomenta las siguientes líneas:
# grid = np.arange(12).reshape(3, 4)
# print(grid)
# print(f"ndim {grid.ndim} · shape {grid.shape} · size {grid.size}")
# print(f"dtype {grid.dtype} · itemsize {grid.itemsize} · nbytes {grid.nbytes}")
# print(f"strides {grid.strides}")


# ============================================
# PASO 3: Un solo tipo para todos
# ============================================
# Descomenta las siguientes líneas:
# print(np.array([1, 2, 3]).dtype, np.array([1, 2.5]).dtype, np.array([True, False]).dtype)
# print(np.array(["Norte", "Sur"]).dtype, np.array(["Norte", 1]))
# print(np.array([1, None]).dtype)
# print(np.array([1.7, -1.7]).astype(np.int64))
# print(np.array(["12.5", "8"]).astype(np.float64) * 2)


# ============================================
# PASO 4: Enteros que dan la vuelta
# ============================================
# Descomenta las siguientes líneas:
# small = np.array([100, 120], dtype=np.int8)
# print("int8 + 10:", small + 10)
# print(f"límites de int8: {np.iinfo(np.int8).min} a {np.iinfo(np.int8).max}")
# print(f"límites de int64: {np.iinfo(np.int64).max:,}".replace(",", " "))
# try:
#     np.array([200], dtype=np.int8)
# except OverflowError as problem:
#     print("OverflowError:", problem)


# ============================================
# PASO 5: Coma flotante
# ============================================
# Descomenta las siguientes líneas:
# print(0.1 + 0.2 == 0.3, np.isclose(0.1 + 0.2, 0.3))
# print(f"float32: {float(np.float32(0.1)):.17f}")
# print(f"float64: {float(np.float64(0.1)):.17f}")
# print(f"épsilon de float64: {np.finfo(np.float64).eps}")
# print(np.array([1.0, -1.0, 0.0]) / 0)


# ============================================
# PASO 6: Vistas y copias
# ============================================
# Descomenta las siguientes líneas:
# flat = np.arange(6)
# view = flat.reshape(2, 3)
# view[0, 0] = 99
# print("flat tras cambiar la vista:", flat)
# print("¿comparten memoria?", np.shares_memory(flat, view), view.base is flat)
# copy = flat.reshape(2, 3).copy()
# copy[0, 0] = -1
# print("flat tras cambiar la copia:", flat)
# print("¿comparten memoria?", np.shares_memory(flat, copy))
# print(f"traspuesta: shape {view.T.shape} · strides {view.T.strides} · {view.T.flags.c_contiguous}")
