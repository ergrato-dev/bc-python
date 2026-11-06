"""Ejercicio 02: while, break, continue y else en bucles.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python while_lab.py
"""

print("Ejercicio 02 · while, break y continue")

# ============================================
# PASO 1: while repite mientras la condición sea verdadera
# ============================================
# La condición se comprueba ANTES de cada vuelta. Si nada la cambia, el bucle no acaba nunca.
# Descomenta las siguientes líneas:
# seconds = 3
# while seconds > 0:
#     print("  quedan", seconds)
#     seconds -= 1
# print("  ¡ya! seconds vale", seconds)

# ============================================
# PASO 2: while cuando no sabes cuántas vueltas habrá
# ============================================
# Collatz: si n es par, n // 2; si es impar, 3 * n + 1. ¿Cuántos pasos hasta llegar a 1?
# Descomenta las siguientes líneas:
# def collatz_steps(n: int) -> int:
#     steps = 0
#     while n != 1:
#         n = n // 2 if n % 2 == 0 else 3 * n + 1
#         steps += 1
#     return steps
#
#
# print("Pasos de Collatz para 6:", collatz_steps(6), "y para 27:", collatz_steps(27))

# ============================================
# PASO 3: continue salta al principio de la siguiente vuelta
# ============================================
# Las medidas que faltan (None) no se suman ni se cuentan.
# Descomenta las siguientes líneas:
# def average_present(values: list[float | None]) -> float | None:
#     total = 0.0
#     count = 0
#     for value in values:
#         if value is None:
#             continue
#         total += value
#         count += 1
#     return total / count if count > 0 else None
#
#
# print("Promedio sin los None:", average_present([10.0, None, 20.0, None, 30.0]))
# print("Promedio de [None]:", average_present([None]))

# ============================================
# PASO 4: break termina el bucle en cuanto encuentras lo que buscas
# ============================================
# Después de break no se miran los valores que quedan.
# Descomenta las siguientes líneas:
# def first_over(values: list[float], limit: float) -> int | None:
#     position = None
#     for index, value in enumerate(values):
#         print(f"    miro la posición {index}: {value}")
#         if value > limit:
#             position = index
#             break
#     return position
#
#
# print("Primera por encima de 50:", first_over([12.5, 55.1, 61.0, 8.0], 50.0))

# ============================================
# PASO 5: else en un bucle, "terminé sin break"
# ============================================
# El else de un for se ejecuta solo si el bucle llegó al final sin break.
# Descomenta las siguientes líneas:
# def is_prime(n: int) -> bool:
#     if n < 2:
#         return False
#     for divisor in range(2, n):
#         if n % divisor == 0:
#             break
#     else:
#         return True
#     return False
#
#
# primes = ""
# for number in range(1, 31):
#     if is_prime(number):
#         primes += f"{number} "
# print("Primos hasta 30:", primes)

# ============================================
# PASO 6: while True con un centinela
# ============================================
# Lee números hasta que llegue "fin". La salida del bucle está dentro, en el break.
# Descomenta las siguientes líneas:
# total = 0.0
# count = 0
# while True:
#     text = input("número (o fin): ")
#     if text == "fin":
#         break
#     total += float(text)
#     count += 1
# print()
# print("Leídos:", count, "| suma:", total)
