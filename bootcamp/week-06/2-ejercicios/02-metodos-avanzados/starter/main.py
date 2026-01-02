"""
Ejercicio 02: Métodos Avanzados de Diccionarios
===============================================
Domina los métodos más útiles: keys(), values(), items(),
setdefault(), update(), copy() y popitem().

Instrucciones:
1. Lee cada sección para entender el concepto
2. Descomenta el código paso a paso
3. Ejecuta el archivo para ver los resultados
4. Experimenta modificando los valores
"""

import copy  # Necesario para deepcopy

# ============================================
# PASO 1: Vistas - keys(), values(), items()
# ============================================
print("=== PASO 1: Vistas ===")

# Las vistas son objetos especiales que reflejan el estado
# actual del diccionario. Se actualizan automáticamente.

# Descomenta las siguientes líneas:

# # Diccionario de ejemplo
# user: dict[str, str | int] = {
#     "name": "Alice",
#     "age": 30,
#     "city": "Madrid"
# }
#
# # Obtener vistas
# keys = user.keys()
# values = user.values()
# items = user.items()
#
# print(f"Claves: {keys}")
# print(f"Valores: {values}")
# print(f"Items: {items}")
#
# # Convertir a lista para indexar
# keys_list: list[str] = list(keys)
# print(f"Lista de claves: {keys_list}")
#
# # Las vistas se actualizan automáticamente
# user["country"] = "Spain"
# print(f"Después de agregar: {keys}")  # Incluye 'country'

print()

# ============================================
# PASO 2: setdefault()
# ============================================
print("=== PASO 2: setdefault() ===")

# setdefault() es muy útil para:
# - Obtener un valor si existe
# - Crearlo con un valor por defecto si no existe
# Todo en una sola operación atómica

# Descomenta las siguientes líneas:

# # Diccionario inicial
# profile: dict[str, str | int] = {"name": "Alice"}
#
# # Si la clave existe, retorna el valor actual
# existing_name: str = profile.setdefault("name", "Unknown")
# print(f"Nombre existente: {existing_name}")
#
# # Si la clave no existe, la crea con el valor por defecto
# new_age: int = profile.setdefault("age", 0)
# print(f"Edad creada: {new_age}")
# print(f"Diccionario actualizado: {profile}")
#
# # Caso de uso común: contar palabras
# words: list[str] = ["hello", "world", "hello", "python"]
# word_count: dict[str, int] = {}
#
# for word in words:
#     # Si la palabra no existe, inicia en 0, luego suma 1
#     word_count[word] = word_count.setdefault(word, 0) + 1
#
# print(f"Conteo de palabras: {word_count}")

print()

# ============================================
# PASO 3: Combinar Diccionarios
# ============================================
print("=== PASO 3: Combinar Diccionarios ===")

# Python ofrece varias formas de combinar diccionarios:
# - update(): modifica el diccionario original
# - | (Python 3.9+): crea un nuevo diccionario
# - |= (Python 3.9+): actualiza in-place

# Descomenta las siguientes líneas:

# # Configuración por defecto y del usuario
# defaults: dict[str, str | int] = {
#     "theme": "dark",
#     "lang": "en",
#     "font_size": 12
# }
#
# user_settings: dict[str, str | int] = {
#     "theme": "light",
#     "font_size": 14
# }
#
# print(f"Defaults: {defaults}")
# print(f"User settings: {user_settings}")
#
# # Operador | crea nuevo diccionario (user_settings tiene prioridad)
# merged: dict[str, str | int] = defaults | user_settings
# print(f"Merged (|): {merged}")
#
# # Operador |= actualiza in-place
# config: dict[str, str | int] = defaults.copy()  # Copia para no modificar defaults
# config |= user_settings
# print(f"Después de |=: {config}")

print()

# ============================================
# PASO 4: Copias de Diccionarios
# ============================================
print("=== PASO 4: Copias ===")

# Es crucial entender la diferencia entre:
# - Copia superficial (shallow): objetos internos compartidos
# - Copia profunda (deep): todo es independiente

# Descomenta las siguientes líneas:

# # Diccionario con objeto anidado
# original: dict[str, dict[str, bool]] = {
#     "config": {"debug": True}
# }
#
# print(f"Original: {original}")
#
# # Copia superficial - ¡Cuidado!
# shallow: dict[str, dict[str, bool]] = original.copy()
# shallow["config"]["debug"] = False  # Modifica el objeto interno
#
# print(f"Shallow modificado debug: {shallow}")
# print(f"¿Original afectado? {original}")  # ¡Sí, también cambió!
#
# # Copia profunda - Totalmente independiente
# original["config"]["debug"] = False  # Reset
# deep: dict[str, dict[str, bool]] = copy.deepcopy(original)
# deep["config"]["debug"] = True  # No afecta original
#
# print(f"Después de deepcopy y modificar: Original={original}, Deep={deep}")

print()

# ============================================
# PASO 5: popitem()
# ============================================
print("=== PASO 5: popitem() ===")

# popitem() elimina y retorna el último par clave-valor insertado.
# Útil para procesar elementos en orden LIFO (último en entrar, primero en salir).

# Descomenta las siguientes líneas:

# # Cola de tareas (simulada)
# task_queue: dict[str, str] = {
#     "task1": "Write tests",
#     "task2": "Review code",
#     "task3": "Send email"
# }
#
# # Procesar tareas en orden inverso (LIFO)
# while task_queue:
#     task_id, description = task_queue.popitem()
#     print(f"Procesando: {(task_id, description)} - ✓")
#
# print(f"Cola vacía: {task_queue}")

# ============================================
# DESAFÍO EXTRA (Opcional)
# ============================================
# Crea un sistema de configuración que:
# 1. Tenga valores por defecto
# 2. Permita al usuario sobrescribir algunos valores
# 3. Use setdefault() para valores opcionales
# 4. Muestre las claves, valores e items por separado

# Tu código aquí:
# default_config: dict[str, str | int | bool] = {
#     "app_name": "MyApp",
#     "version": "1.0",
#     "debug": False,
#     "max_connections": 100
# }
