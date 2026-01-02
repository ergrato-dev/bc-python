"""
Ejercicio 01: CRUD de Diccionarios
==================================
Practica las operaciones fundamentales: Create, Read, Update, Delete.

Instrucciones:
1. Lee cada sección para entender el concepto
2. Descomenta el código paso a paso
3. Ejecuta el archivo para ver los resultados
4. Experimenta modificando los valores
"""

# ============================================
# PASO 1: Crear Diccionarios
# ============================================
print("=== PASO 1: Crear Diccionarios ===")

# Existen múltiples formas de crear diccionarios en Python.
# La más común es la forma literal con llaves {}.

# Descomenta las siguientes líneas:

# # Forma literal (más común y recomendada)
# person_literal: dict[str, str | int] = {
#     "name": "Alice",
#     "age": 30,
#     "city": "Madrid"
# }
# print(f"Literal: {person_literal}")
#
# # Constructor dict() con argumentos nombrados
# person_constructor: dict[str, str | int] = dict(name="Bob", age=25)
# print(f"Constructor: {person_constructor}")
#
# # Desde lista de tuplas (útil al convertir datos)
# pairs: list[tuple[str, int]] = [("a", 1), ("b", 2), ("c", 3)]
# from_tuples: dict[str, int] = dict(pairs)
# print(f"Desde tuplas: {from_tuples}")
#
# # fromkeys() para crear con valor por defecto
# coordinates: dict[str, int] = dict.fromkeys(["x", "y", "z"], 0)
# print(f"fromkeys: {coordinates}")

print()

# ============================================
# PASO 2: Leer/Acceder Valores
# ============================================
print("=== PASO 2: Leer/Acceder ===")

# Hay dos formas principales de acceder a valores:
# - Corchetes []: lanza KeyError si la clave no existe
# - get(): retorna None (o valor por defecto) si no existe

# Descomenta las siguientes líneas:

# # Diccionario de ejemplo
# user: dict[str, str | int] = {
#     "name": "Alice",
#     "age": 30,
#     "city": "Madrid"
# }
#
# # Acceso con corchetes (clave debe existir)
# name: str = user["name"]
# age: int = user["age"]
# print(f"Nombre: {name}")
# print(f"Edad: {age}")
#
# # Acceso con get() - seguro para claves que pueden no existir
# country: str = user.get("country", "Unknown")
# print(f"País (corchetes fallaría): {country}")
#
# # get() sin valor por defecto retorna None
# email: str | None = user.get("email")
# print(f"Email: {email}")

print()

# ============================================
# PASO 3: Agregar y Actualizar
# ============================================
print("=== PASO 3: Agregar y Actualizar ===")

# Agregar: asignar a una clave que no existe
# Actualizar: asignar a una clave existente
# La sintaxis es la misma en ambos casos

# Descomenta las siguientes líneas:

# # Empezamos con un diccionario básico
# profile: dict[str, str | int] = {
#     "name": "Alice",
#     "age": 30
# }
#
# # Agregar nueva clave
# profile["email"] = "alice@example.com"
# print(f"Después de agregar email: {profile}")
#
# # Actualizar valor existente
# profile["age"] = 31
# print(f"Después de actualizar edad: {profile}")
#
# # Agregar múltiples claves con update()
# profile.update({
#     "city": "Madrid",
#     "country": "Spain"
# })
# print(f"Después de update(): {profile}")

print()

# ============================================
# PASO 4: Eliminar Elementos
# ============================================
print("=== PASO 4: Eliminar ===")

# Python ofrece varias formas de eliminar elementos:
# - del: elimina por clave (lanza KeyError si no existe)
# - pop(): elimina y retorna el valor
# - clear(): elimina todos los elementos

# Descomenta las siguientes líneas:

# # Diccionario de trabajo
# data: dict[str, str | int] = {
#     "name": "Alice",
#     "age": 31,
#     "email": "alice@example.com",
#     "city": "Madrid",
#     "country": "Spain"
# }
#
# # del - elimina por clave
# del data["city"]
# print(f"Después de del: {data}")
#
# # pop() - elimina y retorna el valor
# removed_email: str = data.pop("email")
# print(f"Valor eliminado con pop: {removed_email}")
#
# # pop() con valor por defecto (no lanza error si no existe)
# removed_phone: str = data.pop("phone", "N/A")
# print(f"Pop con default: {removed_phone}")
#
# # clear() - vacía todo el diccionario
# data.clear()
# print(f"Después de clear: {data}")

print()

# ============================================
# PASO 5: Verificar Existencia
# ============================================
print("=== PASO 5: Verificar Existencia ===")

# Usa el operador 'in' para verificar si una clave existe.
# Esto es más eficiente que intentar acceder y manejar excepciones.

# Descomenta las siguientes líneas:

# # Diccionario de producto
# product: dict[str, str | int | float] = {
#     "name": "Laptop",
#     "price": 999.99,
#     "stock": 50
# }
#
# # Verificar si clave existe
# if "name" in product:
#     print("✓ El producto tiene nombre")
#
# # Verificar si clave NO existe
# if "discount" not in product:
#     print("✗ El producto NO tiene descuento")
#
# # Patrón común: verificar antes de acceder
# if "stock" in product:
#     stock: int = product["stock"]
#     print(f"Stock: {stock}")
# else:
#     print("Stock no disponible")

# ============================================
# DESAFÍO EXTRA (Opcional)
# ============================================
# Crea un mini sistema de inventario:
# 1. Crea un diccionario con 3 productos (nombre -> cantidad)
# 2. Agrega un nuevo producto
# 3. Actualiza la cantidad de un producto existente
# 4. Elimina un producto
# 5. Verifica si un producto específico existe

# Tu código aquí:
# inventory: dict[str, int] = {}
