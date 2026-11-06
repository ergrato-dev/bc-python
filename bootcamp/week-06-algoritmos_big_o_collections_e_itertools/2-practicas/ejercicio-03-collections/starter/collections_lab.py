"""Ejercicio 03: el módulo collections.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python collections_lab.py
"""

import timeit
from collections import Counter, defaultdict, deque, namedtuple

print("Ejercicio 03 · collections")

# ============================================
# PASO 1: Counter, un diccionario que cuenta
# ============================================
# Counter(iterable) cuenta cada elemento; una clave que no está vale 0, sin KeyError.
# Descomenta las siguientes líneas:
# levels = ["alto", "bajo", "alto", "medio", "alto", "bajo"]
# counts = Counter(levels)
# print("Conteo:", counts)
# print("Los 2 más comunes:", counts.most_common(2))
# print("¿Cuántos 'sin dato'?", counts["sin dato"])
# counts.update(["bajo", "sin dato"])
# print("Tras update:", counts)
# print("Total:", counts.total())

# ============================================
# PASO 2: defaultdict, un diccionario con valor por defecto
# ============================================
# defaultdict(list) crea una lista vacía la primera vez que lees una clave que no está.
# Descomenta las siguientes líneas:
# records = [("Norte", 12.5), ("Sur", 8.0), ("Norte", 48.9), ("Sur", 9.5), ("Este", 30.0)]
# groups: defaultdict[str, list[float]] = defaultdict(list)
# for label, value in records:
#     groups[label].append(value)
# print("Grupos:", dict(groups))
# print("¿Oeste?", "Oeste" in groups)
# print("groups['Oeste']:", groups["Oeste"])
# print("¿Oeste ahora?", "Oeste" in groups)

# ============================================
# PASO 3: deque, una cola con dos extremos rápidos
# ============================================
# popleft en un deque es O(1); pop(0) en una lista mueve todos los demás: O(n).
# Descomenta las siguientes líneas:
# queue = deque(["Norte", "Sur"])
# queue.append("Este")
# queue.appendleft("Oeste")
# print("Cola:", list(queue))
# first = queue.popleft()
# print("Sale:", first, "| queda:", list(queue))
#
# n = 100_000
# list_time = timeit.timeit("values.pop(0)", setup=f"values = list(range({n}))", number=n)
# deque_time = timeit.timeit(
#     "values.popleft()", setup=f"from collections import deque; values = deque(range({n}))", number=n
# )
# print(f"Vaciar {n:,} por la izquierda | lista: {list_time * 1000:.0f} ms | deque: {deque_time * 1000:.1f} ms")

# ============================================
# PASO 4: deque con maxlen, los últimos N
# ============================================
# Con maxlen, al añadir con el deque lleno se cae el elemento del otro extremo.
# Descomenta las siguientes líneas:
# last_three: deque[float] = deque(maxlen=3)
# for value in [10.0, 20.0, 30.0, 40.0, 50.0]:
#     last_three.append(value)
#     average = sum(last_three) / len(last_three)
#     print(f"  entra {value:>4} -> {list(last_three)} media {average:.1f}")

# ============================================
# PASO 5: namedtuple, una tupla con nombres
# ============================================
# Sigue siendo una tupla (inmutable, se desempaqueta), pero sus partes tienen nombre.
# Descomenta las siguientes líneas:
# Reading = namedtuple("Reading", ["label", "value"])
# reading = Reading("Norte", 12.5)
# print(reading, "| etiqueta:", reading.label, "| valor:", reading.value)
# label, value = reading
# print("Desempaquetada:", label, value, "| ¿es tupla?", isinstance(reading, tuple))
# print("Cambiada:", reading._replace(value=13.0), "| original:", reading)
