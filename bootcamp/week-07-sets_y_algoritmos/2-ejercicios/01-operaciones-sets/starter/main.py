"""
Ejercicio 01: Operaciones con Sets
==================================
Aprende a crear sets y usar sus métodos básicos.

Instrucciones:
1. Lee cada sección
2. Descomenta el código indicado
3. Ejecuta el archivo para ver los resultados
"""

# ============================================
# PASO 1: Crear Sets
# ============================================
print("=== PASO 1: Crear Sets ===")

# Los sets se crean con llaves {} o con set()
# Descomenta las siguientes líneas:

# # Set literal con elementos
# fruits: set[str] = {"apple", "banana", "cherry"}
# print(f"Frutas: {fruits}")
#
# # Desde una lista (elimina duplicados)
# numbers_list: list[int] = [1, 2, 2, 3, 4, 4, 5]
# unique_numbers: set[int] = set(numbers_list)
# print(f"Números únicos: {unique_numbers}")
#
# # Set vacío (¡NO uses {} que crea dict!)
# empty_set: set[str] = set()
# print(f"Set vacío: {empty_set}")
# print(f"Tipo de set vacío: {type(empty_set)}")

print()

# ============================================
# PASO 2: Agregar Elementos
# ============================================
print("=== PASO 2: Agregar Elementos ===")

# add() agrega un elemento, update() agrega múltiples
# Descomenta las siguientes líneas:

# fruits: set[str] = {"apple", "banana", "cherry"}
#
# # Agregar un elemento con add()
# fruits.add("mango")
# print(f"Después de add('mango'): {fruits}")
#
# # Agregar elemento existente (no hace nada)
# fruits.add("apple")
# print(f"Después de add('apple'): {fruits}")
#
# # Agregar múltiples elementos con update()
# fruits.update(["grape", "kiwi"])
# print(f"Después de update: {fruits}")

print()

# ============================================
# PASO 3: Verificar Pertenencia
# ============================================
print("=== PASO 3: Verificar Pertenencia ===")

# El operador 'in' verifica si un elemento existe
# Descomenta las siguientes líneas:

# fruits: set[str] = {"apple", "banana", "cherry", "mango", "grape", "kiwi"}
#
# # Verificar pertenencia
# print(f"¿'apple' está en fruits? {'apple' in fruits}")
# print(f"¿'orange' está en fruits? {'orange' in fruits}")
# print(f"¿'orange' NO está en fruits? {'orange' not in fruits}")

print()

# ============================================
# PASO 4: Eliminar con remove()
# ============================================
print("=== PASO 4: Eliminar con remove() ===")

# remove() elimina un elemento, lanza KeyError si no existe
# Descomenta las siguientes líneas:

# fruits: set[str] = {"apple", "banana", "cherry", "mango", "grape", "kiwi"}
#
# # Eliminar elemento existente
# fruits.remove("banana")
# print(f"Después de remove('banana'): {fruits}")
#
# # Intentar eliminar elemento que no existe
# try:
#     fruits.remove("banana")  # Ya no existe
# except KeyError as e:
#     print(f"Error al eliminar 'banana' de nuevo: {e}")

print()

# ============================================
# PASO 5: Eliminar con discard()
# ============================================
print("=== PASO 5: Eliminar con discard() ===")

# discard() elimina un elemento sin lanzar error si no existe
# Descomenta las siguientes líneas:

# fruits: set[str] = {"apple", "cherry", "mango", "grape", "kiwi"}
#
# # Eliminar elemento existente
# fruits.discard("cherry")
# print(f"Después de discard('cherry'): {fruits}")
#
# # Eliminar elemento que no existe (sin error)
# fruits.discard("pineapple")
# print(f"Después de discard('pineapple'): {fruits}")

print()

# ============================================
# PASO 6: Eliminar con pop()
# ============================================
print("=== PASO 6: Eliminar con pop() ===")

# pop() elimina y retorna un elemento arbitrario
# Descomenta las siguientes líneas:

# fruits: set[str] = {"apple", "mango", "grape", "kiwi"}
#
# # pop() retorna el elemento eliminado
# removed = fruits.pop()
# print(f"Elemento eliminado con pop(): {removed}")
# print(f"Set después de pop(): {fruits}")

print()

# ============================================
# PASO 7: Copiar y Vaciar
# ============================================
print("=== PASO 7: Copiar y Vaciar ===")

# copy() crea una copia, clear() vacía el set
# Descomenta las siguientes líneas:

# fruits: set[str] = {"mango", "grape", "kiwi"}
#
# # Crear una copia
# fruits_copy: set[str] = fruits.copy()
# print(f"Copia: {fruits_copy}")
#
# # Vaciar el original
# fruits.clear()
# print(f"Original después de clear(): {fruits}")
# print(f"Copia sigue intacta: {fruits_copy}")

print()

# ============================================
# PASO 8: Eliminar Duplicados de una Lista
# ============================================
print("=== PASO 8: Eliminar Duplicados ===")

# Convertir a set y de vuelta a lista elimina duplicados
# Descomenta las siguientes líneas:

# languages: list[str] = ["python", "java", "python", "javascript", "java", "go"]
# print(f"Lista original: {languages}")
#
# # Convertir a set (elimina duplicados)
# unique_languages: set[str] = set(languages)
# print(f"Como set (únicos): {unique_languages}")
#
# # De vuelta a lista
# unique_list: list[str] = list(unique_languages)
# print(f"De vuelta a lista: {unique_list}")

print()

# ============================================
# ¡COMPLETADO!
# ============================================
print("=" * 50)
print("✅ ¡Ejercicio completado!")
print("Ahora sabes crear y manipular sets básicos.")
print("Continúa con el ejercicio 02-conjuntos-matematicos")
print("=" * 50)
