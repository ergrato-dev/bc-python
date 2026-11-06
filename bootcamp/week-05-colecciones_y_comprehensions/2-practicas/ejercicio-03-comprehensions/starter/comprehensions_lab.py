"""Ejercicio 03: list, dict y set comprehensions, y expresiones generadoras.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python comprehensions_lab.py
"""

print("Ejercicio 03 · Comprehensions")

# ============================================
# PASO 1: el mismo filtro, con bucle y con comprehension
# ============================================
# [expresión for elemento in iterable if condición]: crear, recorrer, filtrar y añadir en una línea.
# Descomenta las siguientes líneas:
# texts = ["12,5", "8", "55,1", "NA", "61"]
# values = []
# for text in texts:
#     if text != "NA":
#         values.append(float(text.replace(",", ".")))
# print("Con bucle:        ", values)
# same = [float(text.replace(",", ".")) for text in texts if text != "NA"]
# print("Con comprehension:", same)

# ============================================
# PASO 2: transformar todos, o elegir entre dos valores
# ============================================
# El if del final FILTRA; un "a if c else b" al principio ELIGE el valor y no quita nada.
# Descomenta las siguientes líneas:
# squares = [n * n for n in range(1, 6)]
# print("Cuadrados:", squares)
# levels = ["alto" if value >= 50 else "normal" for value in same]
# print("Niveles:", levels)

# ============================================
# PASO 3: dict comprehension
# ============================================
# {clave: valor for ...}: construye un diccionario.
# Descomenta las siguientes líneas:
# labels = ["Norte", "Sur", "Este"]
# lengths = {label: len(label) for label in labels}
# print("Longitudes:", lengths)
# readings = {"Norte": 12.5, "Sur": 8.0, "Este": 55.1}
# high = {label: value for label, value in readings.items() if value >= 50}
# print("Altas:", high)

# ============================================
# PASO 4: set comprehension
# ============================================
# {expresión for ...} sin dos puntos: un conjunto, sin repetidos.
# Descomenta las siguientes líneas:
# words = "el aire del norte y el aire del sur".split()
# print("Palabras:", len(words), "| distintas:", sorted({word for word in words}))
# print("Iniciales:", sorted({word[0] for word in words}))

# ============================================
# PASO 5: expresiones generadoras
# ============================================
# Entre paréntesis, no crea la lista: da los valores de uno en uno, y solo una vez.
# Descomenta las siguientes líneas:
# print("Cuántas altas:", sum(1 for value in same if value >= 50))
# print("¿Alguna > 60?", any(value > 60 for value in same), "| ¿todas > 5?", all(value > 5 for value in same))
# gen = (n * n for n in range(3))
# print("Generador:", gen)
# print("Primera vuelta:", list(gen), "| segunda:", list(gen))

# ============================================
# PASO 6: comprehensions anidadas
# ============================================
# Los for se leen en el mismo orden que si fueran bucles anidados.
# Descomenta las siguientes líneas:
# grid = [[1, 2, 3], [4, 5, 6]]
# flat = [n for row in grid for n in row]
# print("Aplanada:", flat)
# columns = [[row[i] for row in grid] for i in range(3)]
# print("Columnas:", columns)
