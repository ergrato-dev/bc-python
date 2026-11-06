"""Ejercicio 01: for, range, enumerate, zip y los patrones de bucle.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python loops_lab.py
"""

print("Ejercicio 01 · for y range")

# ============================================
# PASO 1: for recorre un texto letra a letra
# ============================================
# En cada vuelta, letter toma el siguiente carácter; el bucle acaba cuando no quedan.
# Descomenta las siguientes líneas:
# def count_vowels(text: str) -> int:
#     count = 0
#     for letter in text.casefold():
#         if letter in "aeiouáéíóú":
#             count += 1
#     return count
#
#
# print("Vocales en 'Murciélago':", count_vowels("Murciélago"))
# for letter in "abc":
#     print("  vuelta con", repr(letter))

# ============================================
# PASO 2: range genera los números, sin incluir el final
# ============================================
# range(fin), range(inicio, fin) y range(inicio, fin, paso). list() los muestra todos.
# Descomenta las siguientes líneas:
# print("range(5):", list(range(5)))
# print("range(1, 6):", list(range(1, 6)))
# print("range(10, 0, -3):", list(range(10, 0, -3)))
# print("range(5, 5):", list(range(5, 5)))

# ============================================
# PASO 3: el acumulador empieza antes del bucle
# ============================================
# total arranca en 0 (neutro de la suma) y product en 1 (neutro del producto).
# Descomenta las siguientes líneas:
# def sum_up_to(n: int) -> int:
#     total = 0
#     for number in range(1, n + 1):
#         total += number
#     return total
#
#
# def factorial(n: int) -> int:
#     product = 1
#     for number in range(2, n + 1):
#         product *= number
#     return product
#
#
# print("1 + 2 + ... + 100 =", sum_up_to(100))
# print("5! =", factorial(5), "y 0! =", factorial(0))

# ============================================
# PASO 4: enumerate numera y zip empareja
# ============================================
# enumerate da (posición, elemento); zip avanza por dos secuencias a la vez.
# Descomenta las siguientes líneas:
# stations = ["Norte", "Sur", "Centro"]
# readings = [12.5, 8.0, 55.1]
# for number, station in enumerate(stations, start=1):
#     print(f"  {number}. {station}")
# for station, reading in zip(stations, readings):
#     print(f"  {station:<8}{reading:>6.1f}")

# ============================================
# PASO 5: bucles anidados, una tabla
# ============================================
# Por cada fila, el bucle de dentro da todas sus vueltas: 3 filas x 5 columnas = 15 vueltas.
# Descomenta las siguientes líneas:
# for row in range(1, 4):
#     line = ""
#     for column in range(1, 6):
#         line += f"{row * column:>4}"
#     print(line)

# ============================================
# PASO 6: el máximo a mano, empezando por None
# ============================================
# Empezar en 0 fallaría con valores negativos: None significa "todavía no he visto ninguno".
# Descomenta las siguientes líneas:
# def largest(values: list[float]) -> float | None:
#     best = None
#     for value in values:
#         if best is None or value > best:
#             best = value
#     return best
#
#
# print("Mayor de [12.5, 8.0, 55.1]:", largest([12.5, 8.0, 55.1]))
# print("Mayor de [-3.0, -1.5]:", largest([-3.0, -1.5]))
# print("Mayor de []:", largest([]))
