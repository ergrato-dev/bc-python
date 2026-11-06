"""Ejercicio 03: iteradores.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python iterator_lab.py
"""

from collections.abc import Iterator

print("Ejercicio 03 · Iteradores")

# ============================================
# PASO 1: iter() y next() a mano
# ============================================
# Descomenta las siguientes líneas:
# values = [12.5, 8.0, 55.1]
# cursor = iter(values)
# print("Tipo:", type(cursor).__name__)
# print("next:", next(cursor), next(cursor), next(cursor))
# try:
#     next(cursor)
# except StopIteration:
#     print("StopIteration: no quedan valores")
# print("¿Con valor por defecto?", next(cursor, "fin"))

# ============================================
# PASO 2: lo que hace un for por dentro
# ============================================
# Este while hace lo mismo que `for value in values: print(...)`.
# Descomenta las siguientes líneas:
# cursor = iter(values)
# while True:
#     try:
#         value = next(cursor)
#     except StopIteration:
#         break
#     print("  a mano:", value)
# print("¿Una lista es su propio iterador?", iter(values) is values)
# print("¿Un iterador lo es?", iter(cursor) is cursor)

# ============================================
# PASO 3: un iterador escrito como clase
# ============================================
# Descomenta las siguientes líneas:
# class Countdown:
#     def __init__(self, start: int) -> None:
#         self.current = start
#
#     def __iter__(self) -> Countdown:
#         return self
#
#     def __next__(self) -> int:
#         if self.current <= 0:
#             raise StopIteration
#         self.current -= 1
#         return self.current + 1
#
#
# countdown = Countdown(3)
# print("Cuenta atrás:", list(countdown))
# print("Otra vez:", list(countdown))

# ============================================
# PASO 4: iterable frente a iterador
# ============================================
# Launch se puede recorrer muchas veces: cada iter() crea una Countdown nueva.
# Descomenta las siguientes líneas:
# class Launch:
#     def __init__(self, start: int) -> None:
#         self.start = start
#
#     def __iter__(self) -> Iterator[int]:
#         return Countdown(self.start)
#
#
# launch = Launch(3)
# print("Primera:", list(launch), "· segunda:", list(launch))
# print("Parejas:", [(a, b) for a in launch for b in launch if a > b])
# countdown = Countdown(3)
# print("Parejas con un iterador:", [(a, b) for a in countdown for b in countdown if a > b])

# ============================================
# PASO 5: los iteradores de la biblioteca estándar
# ============================================
# Descomenta las siguientes líneas:
# labels = ["Norte", "Sur", "Centro"]
# pairs = zip(labels, values)
# print("zip es:", type(pairs).__name__, "· ¿iterador?", isinstance(pairs, Iterator))
# print("Primera vuelta:", list(pairs))
# print("Segunda vuelta:", list(pairs))
# rounded = map(round, values)
# print("map:", next(rounded), "y luego", list(rounded))
# numbered = enumerate(labels, start=1)
# print("enumerate:", next(numbered), "· queda:", list(numbered))
# with open("medidas.txt", encoding="utf-8") as file:
#     print("¿Un archivo es un iterador?", isinstance(file, Iterator))
#     print("Primera línea:", next(file).rstrip())
#     print("Las demás:", [line.rstrip() for line in file])
