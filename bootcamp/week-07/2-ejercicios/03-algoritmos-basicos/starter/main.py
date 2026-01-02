"""
Ejercicio 03: Algoritmos Básicos de Búsqueda y Ordenamiento
===========================================================
Aprende búsqueda lineal, binaria y ordenamiento con sorted/sort.

Instrucciones:
1. Lee cada sección
2. Descomenta el código indicado
3. Ejecuta el archivo para ver los resultados
"""

# ============================================
# PASO 1: Búsqueda Lineal
# ============================================
print("=== PASO 1: Búsqueda Lineal ===")

# La búsqueda lineal revisa cada elemento secuencialmente
# Descomenta las siguientes líneas:

# def linear_search(items: list[int], target: int) -> int:
#     """Busca un elemento y retorna su índice o -1."""
#     for index, item in enumerate(items):
#         if item == target:
#             return index
#     return -1
#
# numbers: list[int] = [64, 34, 25, 12, 22, 11, 90, 45]
# target = 22
#
# print(f"Lista: {numbers}")
# print(f"Buscando {target}...")
#
# result = linear_search(numbers, target)
# if result != -1:
#     print(f"✓ Encontrado en índice {result}")
# else:
#     print("✗ No encontrado")

print()

# ============================================
# PASO 2: Búsqueda Lineal (Todos los Índices)
# ============================================
print("=== PASO 2: Búsqueda Lineal (Todos los Índices) ===")

# Encontrar TODAS las posiciones donde aparece un elemento
# Descomenta las siguientes líneas:

# def find_all_indices(items: list[str], target: str) -> list[int]:
#     """Encuentra todos los índices donde aparece el elemento."""
#     return [i for i, item in enumerate(items) if item == target]
#
# words: list[str] = ["apple", "banana", "apple", "cherry", "apple"]
# target = "apple"
#
# print(f"Lista: {words}")
# indices = find_all_indices(words, target)
# print(f"Índices de '{target}': {indices}")

print()

# ============================================
# PASO 3: Búsqueda Binaria
# ============================================
print("=== PASO 3: Búsqueda Binaria ===")

# La búsqueda binaria divide el espacio a la mitad cada vez
# REQUIERE lista ordenada
# Descomenta las siguientes líneas:

# def binary_search(items: list[int], target: int) -> int:
#     """Búsqueda binaria en lista ORDENADA."""
#     left = 0
#     right = len(items) - 1
#
#     while left <= right:
#         mid = (left + right) // 2
#
#         if items[mid] == target:
#             return mid
#         elif items[mid] < target:
#             left = mid + 1
#         else:
#             right = mid - 1
#
#     return -1
#
# # Lista DEBE estar ordenada para búsqueda binaria
# sorted_numbers: list[int] = [11, 12, 22, 25, 34, 45, 64, 90]
# target = 25
#
# print(f"Lista ordenada: {sorted_numbers}")
# print(f"Buscando {target}...")
#
# result = binary_search(sorted_numbers, target)
# if result != -1:
#     print(f"✓ Encontrado en índice {result}")
# else:
#     print("✗ No encontrado")

print()

# ============================================
# PASO 4: Comparación de Búsquedas
# ============================================
print("=== PASO 4: Comparación de Búsquedas ===")

# Comparar eficiencia de búsqueda lineal vs binaria
# Descomenta las siguientes líneas:

# def linear_search_count(items: list[int], target: int) -> int:
#     """Retorna número de comparaciones en búsqueda lineal."""
#     count = 0
#     for item in items:
#         count += 1
#         if item == target:
#             break
#     return count
#
# def binary_search_count(items: list[int], target: int) -> int:
#     """Retorna número de comparaciones en búsqueda binaria."""
#     count = 0
#     left, right = 0, len(items) - 1
#
#     while left <= right:
#         count += 1
#         mid = (left + right) // 2
#         if items[mid] == target:
#             break
#         elif items[mid] < target:
#             left = mid + 1
#         else:
#             right = mid - 1
#
#     return count
#
# # Crear lista grande
# size = 1_000_000
# big_list = list(range(size))
# target = 750_000
#
# linear_count = linear_search_count(big_list, target)
# binary_count = binary_search_count(big_list, target)
#
# print(f"Buscando {target} en lista de {size:,} elementos:")
# print(f"  Búsqueda lineal: {linear_count} comparaciones")
# print(f"  Búsqueda binaria: {binary_count} comparaciones")
# print(f"  Binaria es {linear_count // binary_count}x más rápida")

print()

# ============================================
# PASO 5: sorted() Básico
# ============================================
print("=== PASO 5: sorted() Básico ===")

# sorted() retorna una NUEVA lista ordenada
# Descomenta las siguientes líneas:

# numbers: list[int] = [64, 34, 25, 12, 22, 11, 90]
#
# # sorted() no modifica el original
# sorted_asc = sorted(numbers)
# sorted_desc = sorted(numbers, reverse=True)
#
# print(f"Original: {numbers}")
# print(f"Ordenado ascendente: {sorted_asc}")
# print(f"Ordenado descendente: {sorted_desc}")
# print(f"Original sin cambios: {numbers}")

print()

# ============================================
# PASO 6: sorted() con key
# ============================================
print("=== PASO 6: sorted() con key ===")

# key permite especificar criterio de ordenamiento
# Descomenta las siguientes líneas:

# words: list[str] = ["Python", "is", "awesome", "and", "fun"]
# print(f"Palabras: {words}")
#
# # Ordenar por longitud
# by_length = sorted(words, key=len)
# print(f"Por longitud: {by_length}")
#
# # Ordenar alfabéticamente ignorando mayúsculas
# alphabetical = sorted(words, key=str.lower)
# print(f"Alfabético (ignorando mayúsculas): {alphabetical}")

print()

# ============================================
# PASO 7: Ordenar Diccionarios
# ============================================
print("=== PASO 7: Ordenar Diccionarios ===")

# Ordenar lista de diccionarios por diferentes campos
# Descomenta las siguientes líneas:

# students: list[dict[str, str | int]] = [
#     {"name": "Alice", "grade": 85, "age": 22},
#     {"name": "Bob", "grade": 92, "age": 20},
#     {"name": "Carol", "grade": 78, "age": 23},
#     {"name": "David", "grade": 92, "age": 21},
# ]
#
# print("Estudiantes:")
# for s in students:
#     print(f"  {s}")
#
# # Ordenar por calificación descendente
# by_grade = sorted(students, key=lambda s: s["grade"], reverse=True)
#
# print("\nPor calificación (descendente):")
# for s in by_grade:
#     print(f"  {s['name']}: {s['grade']}")

print()

# ============================================
# PASO 8: sort() In-Place
# ============================================
print("=== PASO 8: sort() In-Place ===")

# sort() modifica la lista original, retorna None
# Descomenta las siguientes líneas:

# numbers: list[int] = [5, 2, 8, 1, 9]
# print(f"Lista original: {numbers}")
#
# # sort() modifica la lista y retorna None
# result = numbers.sort()
#
# print(f"Después de sort(): {numbers}")
# print(f"sort() retorna: {result}")

print()

# ============================================
# ¡COMPLETADO!
# ============================================
print("=" * 50)
print("✅ ¡Ejercicio completado!")
print("Ahora conoces búsqueda lineal, binaria y ordenamiento.")
print("Continúa con el proyecto de la semana.")
print("=" * 50)
