"""Ejercicio 02: scope, el valor por defecto mutable, funciones como valores y recursión.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python scope_lab.py
"""

print("Ejercicio 02 · Scope y funciones como valores")

# ============================================
# PASO 1: lo que nace dentro de una función, se queda dentro
# ============================================
# total es local: existe mientras dura la llamada. UNIT es global: se puede leer desde dentro.
# Descomenta las siguientes líneas:
# UNIT = "µg/m³"
#
#
# def label_total(values: list[float]) -> str:
#     total = 0.0
#     for value in values:
#         total += value
#     return f"{total} {UNIT}"
#
#
# print("Total:", label_total([1.5, 2.5]))
# print("¿Existe total fuera?", "total" in globals())

# ============================================
# PASO 2: asignar dentro crea una variable local
# ============================================
# visits += 1 asigna, así que visits es local en TODA la función, también antes de asignar.
# Descomenta las siguientes líneas:
# visits = 0
#
#
# def add_visit() -> None:
#     visits += 1
#
#
# add_visit()

# ============================================
# PASO 3: el valor por defecto se crea una sola vez
# ============================================
# readings=[] se evalúa al definir la función, no en cada llamada: la lista se comparte.
# Descomenta las siguientes líneas:
# def add_reading(value: float, readings: list[float] = []) -> list[float]:
#     readings.append(value)
#     return readings
#
#
# def add_reading_safe(value: float, readings: list[float] | None = None) -> list[float]:
#     if readings is None:
#         readings = []
#     readings.append(value)
#     return readings
#
#
# print("Con []:  ", add_reading(1.0), add_reading(2.0))
# print("Con None:", add_reading_safe(1.0), add_reading_safe(2.0))

# ============================================
# PASO 4: una función es un valor más
# ============================================
# Se puede guardar en una variable y pasar a otra función, sin paréntesis (sin llamarla).
# Descomenta las siguientes líneas:
# def apply(function, texts: list[str]) -> str:
#     result = ""
#     for text in texts:
#         result += function(text) + " "
#     return result
#
#
# def initial(text: str) -> str:
#     return text[0]
#
#
# words = ["norte", "sur", "centro"]
# print("upper:  ", apply(str.upper, words))
# print("initial:", apply(initial, words))
# shout = str.upper
# print("shout:  ", shout("hola"))

# ============================================
# PASO 5: key= y lambda
# ============================================
# sorted, max y min aceptan key: una función que dice POR QUÉ comparar.
# Descomenta las siguientes líneas:
# stations = ["Occidente", "Sur", "Norte"]
# print("Orden alfabético:", sorted(stations))
# print("Por longitud:    ", sorted(stations, key=len))
# print("La más larga:    ", max(stations, key=len))
# texts = ["12,5", "8", "55,1"]
# print("Como texto: ", sorted(texts))
# print("Como número:", sorted(texts, key=lambda text: float(text.replace(",", "."))))

# ============================================
# PASO 6: una función que se llama a sí misma
# ============================================
# Recursión: un caso base que termina y un caso que se acerca a él.
# Descomenta las siguientes líneas:
# def factorial(n: int) -> int:
#     if n <= 1:
#         return 1
#     return n * factorial(n - 1)
#
#
# def digits_sum(n: int) -> int:
#     if n < 10:
#         return n
#     return n % 10 + digits_sum(n // 10)
#
#
# print("5! =", factorial(5), "| suma de dígitos de 2026:", digits_sum(2026))
