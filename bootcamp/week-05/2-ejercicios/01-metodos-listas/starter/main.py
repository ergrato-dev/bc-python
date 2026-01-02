"""
Ejercicio 01: Métodos de Listas
===============================

Aprende a usar los métodos más importantes de las listas en Python.

Instrucciones:
1. Lee cada sección
2. Descomenta el código
3. Ejecuta y observa los resultados
"""


# ============================================
# PASO 1: append() - Agregar al final
# ============================================
print("--- Paso 1: append() ---")

# append() agrega UN elemento al final de la lista
# Modifica la lista original y retorna None

# Descomenta las siguientes líneas:
# fruits: list[str] = ["apple", "banana"]
# print(f"Original: {fruits}")
#
# # Agregar un elemento
# fruits.append("orange")
# print(f"Después de append('orange'): {fruits}")
#
# # Agregar otro
# fruits.append("mango")
# print(f"Después de append('mango'): {fruits}")
#
# # ⚠️ Cuidado: append con lista agrega la lista como un elemento
# fruits.append(["kiwi", "grape"])
# print(f"Después de append(['kiwi', 'grape']): {fruits}")
# print(f"Último elemento: {fruits[-1]}")  # Es una lista!

print()


# ============================================
# PASO 2: extend() - Agregar múltiples elementos
# ============================================
print("--- Paso 2: extend() ---")

# extend() agrega CADA elemento de un iterable
# A diferencia de append, "desempaqueta" el iterable

# Descomenta las siguientes líneas:
# colors: list[str] = ["red", "blue"]
# print(f"Original: {colors}")
#
# # Extender con otra lista
# colors.extend(["green", "yellow"])
# print(f"Después de extend(['green', 'yellow']): {colors}")
#
# # Extender con una tupla
# colors.extend(("orange", "purple"))
# print(f"Después de extend(('orange', 'purple')): {colors}")
#
# # ⚠️ Extender con string (cada caracter es un elemento)
# colors.extend("RGB")
# print(f"Después de extend('RGB'): {colors}")

print()


# ============================================
# PASO 3: insert() - Insertar en posición
# ============================================
print("--- Paso 3: insert() ---")

# insert(index, item) inserta un elemento en una posición específica
# Los elementos existentes se desplazan a la derecha

# Descomenta las siguientes líneas:
# numbers: list[int] = [1, 2, 4, 5]
# print(f"Original: {numbers}")
#
# # Insertar 3 en la posición 2
# numbers.insert(2, 3)
# print(f"Después de insert(2, 3): {numbers}")
#
# # Insertar al inicio (posición 0)
# numbers.insert(0, 0)
# print(f"Después de insert(0, 0): {numbers}")
#
# # Insertar con índice negativo
# numbers.insert(-1, 99)  # Antes del último
# print(f"Después de insert(-1, 99): {numbers}")
#
# # Índice mayor que la longitud: agrega al final
# numbers.insert(100, 100)
# print(f"Después de insert(100, 100): {numbers}")

print()


# ============================================
# PASO 4: remove() - Eliminar por valor
# ============================================
print("--- Paso 4: remove() ---")

# remove(item) elimina la PRIMERA ocurrencia de un valor
# Genera ValueError si el elemento no existe

# Descomenta las siguientes líneas:
# letters: list[str] = ["a", "b", "c", "b", "d", "b"]
# print(f"Original: {letters}")
#
# # Eliminar primera 'b'
# letters.remove("b")
# print(f"Después de remove('b'): {letters}")
#
# # Eliminar otra 'b'
# letters.remove("b")
# print(f"Después de remove('b') otra vez: {letters}")
#
# # Verificar antes de eliminar para evitar error
# if "z" in letters:
#     letters.remove("z")
# else:
#     print("'z' no está en la lista")
#
# # Eliminar todas las ocurrencias de 'b'
# while "b" in letters:
#     letters.remove("b")
# print(f"Después de eliminar todas las 'b': {letters}")

print()


# ============================================
# PASO 5: pop() - Eliminar y retornar
# ============================================
print("--- Paso 5: pop() ---")

# pop([index]) elimina y RETORNA el elemento en la posición dada
# Sin índice, elimina el último (como una pila/stack)

# Descomenta las siguientes líneas:
# stack: list[str] = ["primero", "segundo", "tercero", "cuarto"]
# print(f"Original: {stack}")
#
# # Pop sin índice: elimina el último
# last = stack.pop()
# print(f"pop() retornó: '{last}'")
# print(f"Lista ahora: {stack}")
#
# # Pop con índice
# first = stack.pop(0)
# print(f"pop(0) retornó: '{first}'")
# print(f"Lista ahora: {stack}")
#
# # Pop con índice negativo
# item = stack.pop(-1)
# print(f"pop(-1) retornó: '{item}'")
# print(f"Lista ahora: {stack}")
#
# # Uso como stack (LIFO - Last In, First Out)
# print("\n--- Simulando Stack ---")
# stack_demo: list[int] = []
# stack_demo.append(1)  # Push
# stack_demo.append(2)  # Push
# stack_demo.append(3)  # Push
# print(f"Stack: {stack_demo}")
# print(f"Pop: {stack_demo.pop()}")  # 3
# print(f"Pop: {stack_demo.pop()}")  # 2
# print(f"Stack: {stack_demo}")

print()


# ============================================
# PASO 6: index() y count() - Búsqueda
# ============================================
print("--- Paso 6: index() y count() ---")

# index(item) retorna la posición de la primera ocurrencia
# count(item) retorna cuántas veces aparece un elemento

# Descomenta las siguientes líneas:
# data: list[int] = [10, 20, 30, 20, 40, 20, 50]
# print(f"Lista: {data}")
#
# # index() - encontrar posición
# pos = data.index(30)
# print(f"index(30) = {pos}")
#
# # index() con rango de búsqueda
# pos = data.index(20)  # Primera ocurrencia
# print(f"index(20) = {pos}")
#
# pos = data.index(20, 2)  # Buscar desde índice 2
# print(f"index(20, 2) = {pos}")
#
# pos = data.index(20, 4)  # Buscar desde índice 4
# print(f"index(20, 4) = {pos}")
#
# # count() - contar ocurrencias
# count = data.count(20)
# print(f"count(20) = {count}")
#
# count = data.count(99)  # Elemento que no existe
# print(f"count(99) = {count}")  # 0, no da error
#
# # Encontrar todas las posiciones de un elemento
# def find_all_positions(lst: list, item) -> list[int]:
#     """Encuentra todas las posiciones de un elemento."""
#     return [i for i, x in enumerate(lst) if x == item]
#
# positions = find_all_positions(data, 20)
# print(f"Todas las posiciones de 20: {positions}")

print()


# ============================================
# PASO 7: sort() - Ordenar in-place
# ============================================
print("--- Paso 7: sort() ---")

# sort() ordena la lista IN-PLACE (modifica la original)
# Retorna None, no una nueva lista

# Descomenta las siguientes líneas:
# numbers: list[int] = [64, 34, 25, 12, 22, 11, 90]
# print(f"Original: {numbers}")
#
# # Ordenar ascendente (por defecto)
# numbers.sort()
# print(f"Después de sort(): {numbers}")
#
# # Ordenar descendente
# numbers.sort(reverse=True)
# print(f"Después de sort(reverse=True): {numbers}")
#
# # Ordenar strings
# words: list[str] = ["banana", "Apple", "cherry", "date"]
# words.sort()
# print(f"\nStrings ordenados: {words}")  # Mayúsculas primero!
#
# # Ordenar ignorando mayúsculas
# words.sort(key=str.lower)
# print(f"Ordenados (ignorando caso): {words}")
#
# # Ordenar por longitud
# words.sort(key=len)
# print(f"Ordenados por longitud: {words}")
#
# # ⚠️ Importante: sort() retorna None
# result = numbers.sort()
# print(f"\nsort() retorna: {result}")  # None
#
# # Para obtener una lista ordenada sin modificar la original, usar sorted()
# original: list[int] = [3, 1, 4, 1, 5]
# sorted_copy = sorted(original)
# print(f"\nOriginal: {original}")
# print(f"sorted(): {sorted_copy}")

print()


# ============================================
# PASO 8: reverse() - Invertir in-place
# ============================================
print("--- Paso 8: reverse() ---")

# reverse() invierte el orden de los elementos IN-PLACE
# No ordena, solo invierte

# Descomenta las siguientes líneas:
# items: list[str] = ["a", "b", "c", "d", "e"]
# print(f"Original: {items}")
#
# items.reverse()
# print(f"Después de reverse(): {items}")
#
# # Invertir de nuevo restaura el orden original
# items.reverse()
# print(f"Después de reverse() otra vez: {items}")
#
# # ⚠️ reverse() NO ordena, solo invierte
# mixed: list[int] = [3, 1, 4, 1, 5]
# mixed.reverse()
# print(f"\n[3, 1, 4, 1, 5] reversed: {mixed}")  # [5, 1, 4, 1, 3]
#
# # Para invertir sin modificar original, usar slicing
# original: list[int] = [1, 2, 3, 4, 5]
# reversed_copy = original[::-1]
# print(f"\nOriginal: {original}")
# print(f"Slicing [::-1]: {reversed_copy}")

print()


# ============================================
# PASO 9: copy() - Copia superficial
# ============================================
print("--- Paso 9: copy() ---")

# copy() crea una copia SUPERFICIAL de la lista
# La copia es independiente de la original (para elementos simples)

# Descomenta las siguientes líneas:
# original: list[int] = [1, 2, 3, 4, 5]
# copied = original.copy()
#
# print(f"Original: {original}")
# print(f"Copia: {copied}")
#
# # Modificar la copia no afecta la original
# copied.append(6)
# copied[0] = 99
# print(f"\nDespués de modificar la copia:")
# print(f"Original: {original}")
# print(f"Copia: {copied}")
#
# # ⚠️ Cuidado con listas anidadas (shallow copy)
# nested: list[list[int]] = [[1, 2], [3, 4]]
# shallow_copy = nested.copy()
#
# # Modificar elemento anidado AFECTA a ambas!
# shallow_copy[0][0] = 99
# print(f"\nDespués de modificar nested shallow copy:")
# print(f"Original: {nested}")
# print(f"Shallow copy: {shallow_copy}")
#
# # Para copia profunda, usar copy.deepcopy()
# import copy
# nested = [[1, 2], [3, 4]]
# deep_copy = copy.deepcopy(nested)
#
# deep_copy[0][0] = 99
# print(f"\nDespués de modificar deep copy:")
# print(f"Original: {nested}")
# print(f"Deep copy: {deep_copy}")

print()


# ============================================
# PASO 10: Ejercicio Integrador
# ============================================
print("--- Paso 10: Ejercicio Integrador ---")

# Gestión de lista de tareas (To-Do List)

# Descomenta las siguientes líneas:
# def manage_tasks() -> None:
#     """Simula gestión de tareas con métodos de lista."""
#     tasks: list[str] = []
#
#     # Agregar tareas
#     tasks.append("Revisar emails")
#     tasks.append("Reunión de equipo")
#     tasks.append("Escribir informe")
#     tasks.append("Llamar cliente")
#     print(f"Tareas iniciales: {tasks}")
#
#     # Insertar tarea urgente al inicio
#     tasks.insert(0, "🚨 Emergencia: Bug crítico")
#     print(f"Después de agregar urgente: {tasks}")
#
#     # Agregar varias tareas de una vez
#     tasks.extend(["Actualizar documentación", "Code review"])
#     print(f"Después de extend: {tasks}")
#
#     # Completar primera tarea (eliminar)
#     completed = tasks.pop(0)
#     print(f"\n✅ Completada: {completed}")
#     print(f"Tareas pendientes: {tasks}")
#
#     # Cancelar una tarea específica
#     if "Reunión de equipo" in tasks:
#         tasks.remove("Reunión de equipo")
#         print("❌ Cancelada: Reunión de equipo")
#
#     # Ordenar alfabéticamente
#     tasks.sort()
#     print(f"\nTareas ordenadas: {tasks}")
#
#     # Contar tareas
#     print(f"\n📊 Total de tareas pendientes: {len(tasks)}")
#
#     # Crear copia para "mañana"
#     tomorrow = tasks.copy()
#     tomorrow.append("Nueva tarea para mañana")
#     print(f"\nTareas de hoy: {tasks}")
#     print(f"Tareas de mañana: {tomorrow}")
#
# manage_tasks()

print()
print("=" * 50)
print("🎉 ¡Ejercicio completado!")
print("=" * 50)
