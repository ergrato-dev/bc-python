"""Ejercicio 01: listas y tuplas.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python lists_lab.py
"""

print("Ejercicio 01 · Listas y tuplas")

# ============================================
# PASO 1: crear una lista, medirla y leer por posición
# ============================================
# Los índices empiezan en 0; los negativos cuentan desde el final; [a:b] es un trozo.
# Descomenta las siguientes líneas:
# readings = [12.5, 8.0, 55.1, 61.0]
# print("Lecturas:", readings, "| cuántas:", len(readings))
# print("Primera:", readings[0], "| última:", readings[-1], "| del medio:", readings[1:3])

# ============================================
# PASO 2: cambiar la lista en su sitio
# ============================================
# Una lista es mutable: estos métodos la cambian a ella, no crean otra.
# Descomenta las siguientes líneas:
# readings[1] = 9.5
# readings.append(48.9)
# readings.insert(0, 3.2)
# last = readings.pop()
# readings.remove(55.1)
# print("Tras cambiar:", readings, "| pop sacó:", last)

# ============================================
# PASO 3: sorted crea una lista nueva; sort cambia la lista y devuelve None
# ============================================
# Descomenta las siguientes líneas:
# ordered = sorted(readings)
# print("sorted:", ordered, "| original:", readings)
# result = readings.sort(reverse=True)
# print("sort:", readings, "| sort devolvió:", result)

# ============================================
# PASO 4: dos nombres para una lista frente a una copia
# ============================================
# = no copia: le da otro nombre al MISMO objeto. .copy() crea un objeto nuevo.
# Descomenta las siguientes líneas:
# alias = readings
# snapshot = readings.copy()
# alias.append(0.0)
# print("readings:", readings)
# print("snapshot:", snapshot)
# print("alias is readings:", alias is readings, "| snapshot is readings:", snapshot is readings)

# ============================================
# PASO 5: tuplas y desempaquetado
# ============================================
# Una tupla es una secuencia inmutable: un registro con partes fijas.
# Descomenta las siguientes líneas:
# station = ("Norte", 12.5, "µg/m³")
# label, value, unit = station
# print(f"{label}: {value} {unit} | campos: {len(station)}")
# first, *rest = [3, 1, 4, 1, 5]
# print("first:", first, "| rest:", rest)
# low, high = 10.0, 50.0
# low, high = high, low
# print("intercambio:", low, high)

# ============================================
# PASO 6: una lista de tuplas, ordenada por el valor
# ============================================
# key dice por qué ordenar: aquí, por la segunda parte de cada tupla.
# Descomenta las siguientes líneas:
# records = [("Norte", 12.5), ("Sur", 8.0), ("Oriente", 55.1)]
# for label, value in sorted(records, key=lambda record: record[1], reverse=True):
#     print(f"  {label:<8}{value:>6.1f}")
# print("Máximo:", max(records, key=lambda record: record[1]))
