"""Ejercicio 04 · Vectorizar con NumPy: bucles, funciones de Python y arrays.

Ejecuta `uv run python main.py` después de cada paso. Los tiempos son de tu máquina:
compáralos con los del README por su orden de magnitud y por cuál gana, no por el último
decimal.
"""

import random
import timeit
from collections import deque
from collections.abc import Callable

import numpy as np

# Un millón de valores, siempre los mismos: como una columna de medidas grande.
rng = random.Random(22)
VALUES = [rng.uniform(0, 80) for _ in range(1_000_000)]


def best(function: Callable[[], object], number: int = 3) -> float:
    """Milisegundos por llamada: el mínimo de 5 repeticiones de `number` llamadas."""
    return min(timeit.repeat(function, number=number, repeat=5)) / number * 1000


print("Ejercicio 04 · Vectorizar")


# ============================================
# PASO 1: Sumar un millón de valores
# ============================================
# Descomenta las siguientes líneas:
# def loop_sum(values: list[float]) -> float:
#     total = 0.0
#     for value in values:
#         total += value
#     return total
#
#
# array = np.array(VALUES)
# print(f"dtype {array.dtype} · shape {array.shape} · {array.nbytes / 1e6:.0f} MB")
# print(f"bucle   {best(lambda: loop_sum(VALUES)):6.1f} ms")
# print(f"sum()   {best(lambda: sum(VALUES)):6.1f} ms")
# print(f"np.sum  {best(lambda: np.sum(array)):6.1f} ms")


# ============================================
# PASO 2: Una operación por elemento
# ============================================
# Descomenta las siguientes líneas:
# mean = sum(VALUES) / len(VALUES)
# spread = (sum((value - mean) ** 2 for value in VALUES) / len(VALUES)) ** 0.5
# print(f"lista   {best(lambda: [(value - mean) / spread for value in VALUES]):6.1f} ms")
# print(f"array   {best(lambda: (array - array.mean()) / array.std()):6.1f} ms")
# scores = (array - array.mean()) / array.std()
# print(f"primera puntuación: {scores[0]:.4f} · {(VALUES[0] - mean) / spread:.4f}")


# ============================================
# PASO 3: El precio de entrar y salir
# ============================================
# Descomenta las siguientes líneas:
# print(f"np.array(lista) {best(lambda: np.array(VALUES)):6.1f} ms")
# print(f"array.tolist()  {best(lambda: array.tolist()):6.1f} ms")
# print(f"sum() de lista  {best(lambda: sum(VALUES)):6.1f} ms")
# print(f"convertir y np.sum {best(lambda: np.sum(np.array(VALUES))):6.1f} ms")


# ============================================
# PASO 4: Contar y filtrar sin bucle
# ============================================
# Descomenta las siguientes líneas:
# print(f"bucle   {best(lambda: sum(value > 50 for value in VALUES)):6.1f} ms")
# print(f"máscara {best(lambda: np.count_nonzero(array > 50)):6.1f} ms")
# high = array[array > 50]
# print(f"altos: {high.size} · el primero {high[0]:.2f} · {(array > 50)[:4]}")


# ============================================
# PASO 5: La media móvil
# ============================================
# Descomenta las siguientes líneas:
# def moving_average(values: list[float], window: int) -> list[float]:
#     """La de tu Observatorio: suma el que entra y resta el que sale."""
#     recent: deque[float] = deque(maxlen=window)
#     total, averages = 0.0, []
#     for value in values:
#         if len(recent) == window:
#             total -= recent[0]
#         recent.append(value)
#         total += value
#         if len(recent) == window:
#             averages.append(total / window)
#     return averages
#
#
# def moving_average_np(values: np.ndarray, window: int) -> np.ndarray:
#     """Con sumas acumuladas: la suma de un tramo es la resta de dos acumuladas."""
#     sums = np.cumsum(np.concatenate(([0.0], values)))
#     return (sums[window:] - sums[:-window]) / window
#
#
# print(f"deque   {best(lambda: moving_average(VALUES, 3)):6.1f} ms")
# print(f"cumsum  {best(lambda: moving_average_np(array, 3)):6.1f} ms")
# same = np.allclose(moving_average_np(array, 3), moving_average(VALUES, 3))
# print(f"iguales: {same} · {len(moving_average(VALUES[:5], 3))} medias de 5 valores")


# ============================================
# PASO 6: Con pocos datos
# ============================================
# Descomenta las siguientes líneas:
# few = VALUES[:10]
# few_array = np.array(few)
# print(f"10 valores · sum() {best(lambda: sum(few), 10_000) * 1000:5.2f} µs")
# print(f"10 valores · np.sum {best(lambda: np.sum(few_array), 10_000) * 1000:5.2f} µs")
# both = best(lambda: np.sum(np.array(few)), 10_000)
# print(f"10 valores · convertir y np.sum {both * 1000:5.2f} µs")
