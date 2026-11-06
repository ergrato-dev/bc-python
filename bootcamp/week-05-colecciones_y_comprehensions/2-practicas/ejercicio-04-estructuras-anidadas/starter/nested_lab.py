"""Ejercicio 04: estructuras anidadas, copias y elegir la colección.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python nested_lab.py
"""

import copy
import time

print("Ejercicio 04 · Estructuras anidadas")

# ============================================
# PASO 1: la trampa de [[0] * 3] * 3
# ============================================
# * repite la REFERENCIA a la misma lista interior; la comprehension crea una nueva por vuelta.
# Descomenta las siguientes líneas:
# grid = [[0] * 3] * 3
# grid[0][0] = 9
# print("Con *:            ", grid)
# grid = [[0] * 3 for _ in range(3)]
# grid[0][0] = 9
# print("Con comprehension:", grid)

# ============================================
# PASO 2: copia superficial y copia profunda
# ============================================
# .copy() copia el diccionario, pero las listas de dentro siguen compartidas.
# Descomenta las siguientes líneas:
# stations = {"Norte": [12.5, 48.9], "Sur": [8.0]}
# shallow = stations.copy()
# deep = copy.deepcopy(stations)
# stations["Norte"].append(99.0)
# print("original:", stations)
# print("copy():  ", shallow)
# print("deepcopy:", deep)

# ============================================
# PASO 3: no cambies una lista mientras la recorres
# ============================================
# remove desplaza los elementos y el for se salta el siguiente.
# Descomenta las siguientes líneas:
# values = [5, 60, 70, 8, 90]
# for value in values:
#     if value >= 50:
#         values.remove(value)
# print("Quitando dentro del for:", values)
# values = [5, 60, 70, 8, 90]
# values = [value for value in values if value < 50]
# print("Con comprehension:      ", values)

# ============================================
# PASO 4: una lista de diccionarios, como la que da un JSON
# ============================================
# Cada [] baja un nivel: la lista por posición, el diccionario por clave.
# Descomenta las siguientes líneas:
# measurements = [
#     {"label": "Norte", "values": [12.5, 48.9], "unit": "µg/m³"},
#     {"label": "Sur", "values": [8.0, 9.5], "unit": "µg/m³"},
#     {"label": "Centro", "values": [], "unit": "µg/m³"},
# ]
# for item in measurements:
#     values = item["values"]
#     text = f"{max(values):.1f} {item['unit']}" if values else "sin dato"
#     print(f"  {item['label']:<7} máximo {text}")
# print("Segunda lectura del Norte:", measurements[0]["values"][1])

# ============================================
# PASO 5: buscar en una lista frente a buscar en un set
# ============================================
# in recorre la lista elemento a elemento; en un set va directo al sitio.
# Descomenta las siguientes líneas:
# labels_list = [f"estación-{n}" for n in range(200_000)]
# labels_set = set(labels_list)
# start = time.perf_counter()
# for _ in range(200):
#     found = "estación-199999" in labels_list
# list_time = time.perf_counter() - start
# start = time.perf_counter()
# for _ in range(200):
#     found = "estación-199999" in labels_set
# set_time = time.perf_counter() - start
# print(f"list: {list_time * 1000:.1f} ms | set: {set_time * 1000:.3f} ms | ¿encontrada? {found}")
# print(f"El set fue unas {list_time / set_time:,.0f} veces más rápido")
