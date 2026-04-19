"""
Ejercicio 03: Tuplas y Estructuras
==================================

Aprende a usar tuplas, unpacking y estructuras de datos anidadas.

Instrucciones:
1. Lee cada sección
2. Descomenta el código
3. Ejecuta y observa los resultados
"""


# ============================================
# PASO 1: Crear Tuplas
# ============================================
print("--- Paso 1: Crear Tuplas ---")

# Las tuplas son secuencias inmutables ordenadas

# Descomenta las siguientes líneas:
# # Crear tupla con paréntesis
# point: tuple[int, int] = (10, 20)
# print(f"Punto: {point}")
# print(f"Tipo: {type(point)}")
#
# # Sin paréntesis (también válido)
# coordinates = 3, 4, 5
# print(f"Coordenadas: {coordinates}")
# print(f"Tipo: {type(coordinates)}")
#
# # Tupla vacía
# empty: tuple = ()
# print(f"Tupla vacía: {empty}, longitud: {len(empty)}")
#
# # ⚠️ Tupla de un elemento (coma obligatoria)
# single_tuple = (42,)
# not_a_tuple = (42)  # Solo un int entre paréntesis
#
# print(f"\n(42,) tipo: {type(single_tuple)}")  # tuple
# print(f"(42) tipo: {type(not_a_tuple)}")      # int
#
# # Crear tupla desde otros iterables
# from_list = tuple([1, 2, 3])
# from_string = tuple("abc")
# from_range = tuple(range(5))
#
# print(f"\nDesde lista: {from_list}")
# print(f"Desde string: {from_string}")
# print(f"Desde range: {from_range}")

print()


# ============================================
# PASO 2: Inmutabilidad
# ============================================
print("--- Paso 2: Inmutabilidad ---")

# Las tuplas NO pueden modificarse después de crearse

# Descomenta las siguientes líneas:
# colors: tuple[str, str, str] = ("red", "green", "blue")
# print(f"Tupla: {colors}")
#
# # ❌ ERROR: No se pueden modificar elementos
# # colors[0] = "yellow"  # TypeError
#
# # ❌ ERROR: No se pueden agregar elementos
# # colors.append("yellow")  # AttributeError
#
# # ❌ ERROR: No se pueden eliminar elementos
# # del colors[0]  # TypeError
#
# # ✅ Pero sí se puede reasignar la variable
# colors = ("yellow", "purple", "orange")
# print(f"Nueva tupla: {colors}")
#
# # ⚠️ Tuplas con objetos mutables
# data: tuple[str, list[int]] = ("scores", [85, 90, 78])
# print(f"\nTupla con lista: {data}")
#
# # No se puede cambiar qué objeto está en la tupla
# # data[1] = [100, 100, 100]  # Error
#
# # Pero SÍ se puede modificar el objeto mutable interno
# data[1].append(95)
# data[1][0] = 100
# print(f"Después de modificar la lista interna: {data}")

print()


# ============================================
# PASO 3: Acceso y Métodos
# ============================================
print("--- Paso 3: Acceso y Métodos ---")

# Las tuplas soportan indexing, slicing y tienen 2 métodos

# Descomenta las siguientes líneas:
# person: tuple[str, int, str] = ("Alice", 30, "NYC")
# print(f"Persona: {person}")
#
# # Indexing
# print(f"\nperson[0] = {person[0]}")  # "Alice"
# print(f"person[1] = {person[1]}")    # 30
# print(f"person[-1] = {person[-1]}")  # "NYC"
#
# # Slicing
# print(f"\nperson[0:2] = {person[0:2]}")  # ('Alice', 30)
# print(f"person[1:] = {person[1:]}")      # (30, 'NYC')
#
# # Iteración
# print("\nIterando:")
# for item in person:
#     print(f"  {item}")
#
# # Verificar existencia
# print(f"\n'Alice' in person: {'Alice' in person}")
# print(f"25 in person: {25 in person}")
#
# # Métodos: count() e index()
# numbers: tuple[int, ...] = (1, 2, 3, 2, 4, 2, 5)
# print(f"\nTupla: {numbers}")
# print(f"count(2) = {numbers.count(2)}")  # 3
# print(f"index(2) = {numbers.index(2)}")  # 1 (primera ocurrencia)
# print(f"index(2, 2) = {numbers.index(2, 2)}")  # 3 (busca desde índice 2)

print()


# ============================================
# PASO 4: Tuple Unpacking Básico
# ============================================
print("--- Paso 4: Tuple Unpacking Básico ---")

# Unpacking extrae elementos de una tupla en variables

# Descomenta las siguientes líneas:
# # Unpacking básico
# point: tuple[int, int, int] = (10, 20, 30)
# x, y, z = point
#
# print(f"Tupla: {point}")
# print(f"x = {x}, y = {y}, z = {z}")
#
# # Funciona con cualquier iterable
# a, b, c = [1, 2, 3]  # Lista
# print(f"\nDesde lista: a={a}, b={b}, c={c}")
#
# first, second, third = "ABC"  # String
# print(f"Desde string: {first}, {second}, {third}")
#
# # Swap de variables (intercambio)
# m, n = 10, 20
# print(f"\nAntes: m={m}, n={n}")
#
# m, n = n, m  # Swap en una línea!
# print(f"Después de swap: m={m}, n={n}")
#
# # Unpacking en bucle
# students = [("Alice", 95), ("Bob", 87), ("Charlie", 92)]
# print("\nCalificaciones:")
# for name, grade in students:
#     print(f"  {name}: {grade}")

print()


# ============================================
# PASO 5: Extended Unpacking
# ============================================
print("--- Paso 5: Extended Unpacking ---")

# El operador * permite capturar múltiples elementos

# Descomenta las siguientes líneas:
# numbers: tuple[int, ...] = (1, 2, 3, 4, 5, 6, 7)
# print(f"Tupla: {numbers}")
#
# # Primero y el resto
# first, *rest = numbers
# print(f"\nfirst, *rest:")
# print(f"  first = {first}")
# print(f"  rest = {rest}")  # Lista!
#
# # Último y el resto
# *rest, last = numbers
# print(f"\n*rest, last:")
# print(f"  rest = {rest}")
# print(f"  last = {last}")
#
# # Primero, último y el medio
# first, *middle, last = numbers
# print(f"\nfirst, *middle, last:")
# print(f"  first = {first}")
# print(f"  middle = {middle}")
# print(f"  last = {last}")
#
# # Ignorar valores con _
# data = ("Alice", 30, "alice@email.com", "NYC", "Engineer")
# name, _, email, *_ = data
# print(f"\nSolo nombre y email:")
# print(f"  name = {name}")
# print(f"  email = {email}")
#
# # ⚠️ Solo puede haber UN * en el unpacking
# # a, *b, *c = numbers  # SyntaxError

print()


# ============================================
# PASO 6: Named Tuples
# ============================================
print("--- Paso 6: Named Tuples ---")

# Named tuples combinan tuplas con acceso por nombre

# Descomenta las siguientes líneas:
# from typing import NamedTuple
#
# # Definir Named Tuple con clase
# class Point(NamedTuple):
#     x: float
#     y: float
#
# class Person(NamedTuple):
#     name: str
#     age: int
#     city: str = "Unknown"  # Valor por defecto
#
# # Crear instancias
# p1 = Point(10.5, 20.3)
# p2 = Point(x=5.0, y=15.0)  # Con nombres
#
# print(f"Punto 1: {p1}")
# print(f"Punto 2: {p2}")
#
# # Acceso por nombre (más legible)
# print(f"\np1.x = {p1.x}")
# print(f"p1.y = {p1.y}")
#
# # También por índice
# print(f"p1[0] = {p1[0]}")
# print(f"p1[1] = {p1[1]}")
#
# # Crear personas
# alice = Person("Alice", 30, "NYC")
# bob = Person("Bob", 25)  # city = "Unknown"
#
# print(f"\nAlice: {alice}")
# print(f"  Nombre: {alice.name}")
# print(f"  Ciudad: {alice.city}")
#
# print(f"\nBob: {bob}")
# print(f"  Ciudad: {bob.city}")  # Valor por defecto
#
# # Unpacking sigue funcionando
# name, age, city = alice
# print(f"\nUnpacked: {name}, {age}, {city}")

print()


# ============================================
# PASO 7: Tuplas en Funciones
# ============================================
print("--- Paso 7: Tuplas en Funciones ---")

# Las funciones pueden retornar múltiples valores como tupla

# Descomenta las siguientes líneas:
# def get_stats(numbers: list[float]) -> tuple[float, float, float]:
#     """
#     Calcula estadísticas básicas.
#
#     Returns:
#         tuple: (mínimo, máximo, promedio)
#     """
#     minimum = min(numbers)
#     maximum = max(numbers)
#     average = sum(numbers) / len(numbers)
#     return minimum, maximum, average
#
# # Usar la función
# data = [23.5, 18.0, 31.2, 27.8, 22.1]
# result = get_stats(data)
# print(f"Resultado como tupla: {result}")
#
# # Unpacking directo
# min_val, max_val, avg_val = get_stats(data)
# print(f"\nMínimo: {min_val}")
# print(f"Máximo: {max_val}")
# print(f"Promedio: {avg_val:.2f}")
#
# # Ignorar valores que no necesitas
# _, max_only, _ = get_stats(data)
# print(f"\nSolo máximo: {max_only}")
#
# # divmod() retorna tupla (cociente, residuo)
# quotient, remainder = divmod(17, 5)
# print(f"\n17 ÷ 5 = {quotient} con residuo {remainder}")

print()


# ============================================
# PASO 8: Estructuras Anidadas (Matrices)
# ============================================
print("--- Paso 8: Estructuras Anidadas ---")

# Listas de listas para representar matrices/grids

# Descomenta las siguientes líneas:
# # Matriz 3x3
# matrix: list[list[int]] = [
#     [1, 2, 3],
#     [4, 5, 6],
#     [7, 8, 9]
# ]
#
# print("Matriz:")
# for row in matrix:
#     print(f"  {row}")
#
# # Acceso: matrix[fila][columna]
# print(f"\nmatrix[0][0] = {matrix[0][0]}")  # 1
# print(f"matrix[1][1] = {matrix[1][1]}")  # 5
# print(f"matrix[2][2] = {matrix[2][2]}")  # 9
#
# # Modificar elemento
# matrix[1][1] = 99
# print(f"\nDespués de matrix[1][1] = 99:")
# for row in matrix:
#     print(f"  {row}")
#
# # Iterar todos los elementos
# print("\nTodos los elementos:")
# for i, row in enumerate(matrix):
#     for j, value in enumerate(row):
#         print(f"  [{i}][{j}] = {value}")
#
# # Obtener columna
# def get_column(mat: list[list[int]], col: int) -> list[int]:
#     return [row[col] for row in mat]
#
# matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# col_1 = get_column(matrix, 1)
# print(f"\nColumna 1: {col_1}")  # [2, 5, 8]

print()


# ============================================
# PASO 9: Listas de Tuplas
# ============================================
print("--- Paso 9: Listas de Tuplas ---")

# Combinar listas y tuplas para datos estructurados

# Descomenta las siguientes líneas:
# from typing import NamedTuple
#
# # Lista de coordenadas
# points: list[tuple[int, int]] = [
#     (0, 0),
#     (10, 20),
#     (30, 40),
#     (50, 60)
# ]
#
# print("Puntos:")
# for x, y in points:
#     print(f"  ({x}, {y})")
#
# # Encontrar punto más lejano del origen
# def distance_from_origin(point: tuple[int, int]) -> float:
#     x, y = point
#     return (x**2 + y**2)**0.5
#
# farthest = max(points, key=distance_from_origin)
# print(f"\nPunto más lejano: {farthest}")
#
# # Named tuple para estudiantes
# class Student(NamedTuple):
#     name: str
#     grade: float
#
# students: list[Student] = [
#     Student("Alice", 95.5),
#     Student("Bob", 87.0),
#     Student("Charlie", 92.3),
#     Student("Diana", 88.5)
# ]
#
# # Ordenar por calificación
# sorted_students = sorted(students, key=lambda s: s.grade, reverse=True)
# print("\nEstudiantes por calificación:")
# for student in sorted_students:
#     print(f"  {student.name}: {student.grade}")
#
# # Filtrar aprobados (>= 90)
# honors = [s for s in students if s.grade >= 90]
# print(f"\nEstudiantes de honor: {[s.name for s in honors]}")

print()


# ============================================
# PASO 10: Ejercicio Integrador
# ============================================
print("--- Paso 10: Ejercicio Integrador ---")

# Sistema de inventario con tuplas y estructuras

# Descomenta las siguientes líneas:
# from typing import NamedTuple
#
# class Product(NamedTuple):
#     """Representa un producto en inventario."""
#     id: int
#     name: str
#     price: float
#     quantity: int
#
# def manage_inventory() -> None:
#     """Gestiona un inventario de productos."""
#
#     # Inventario inicial
#     inventory: list[Product] = [
#         Product(1, "Laptop", 999.99, 10),
#         Product(2, "Mouse", 29.99, 50),
#         Product(3, "Keyboard", 79.99, 30),
#         Product(4, "Monitor", 299.99, 15),
#         Product(5, "Headphones", 149.99, 25),
#     ]
#
#     print("📦 INVENTARIO")
#     print("=" * 50)
#     for product in inventory:
#         print(f"  [{product.id}] {product.name}: ${product.price:.2f} x {product.quantity}")
#
#     # 1. Valor total del inventario
#     total_value = sum(p.price * p.quantity for p in inventory)
#     print(f"\n💰 Valor total: ${total_value:,.2f}")
#
#     # 2. Producto más caro
#     most_expensive = max(inventory, key=lambda p: p.price)
#     print(f"\n💎 Más caro: {most_expensive.name} (${most_expensive.price})")
#
#     # 3. Producto con más unidades
#     most_stock = max(inventory, key=lambda p: p.quantity)
#     print(f"📈 Mayor stock: {most_stock.name} ({most_stock.quantity} unidades)")
#
#     # 4. Productos con bajo stock (< 20)
#     low_stock = [p for p in inventory if p.quantity < 20]
#     print(f"\n⚠️ Stock bajo:")
#     for p in low_stock:
#         print(f"  - {p.name}: {p.quantity} unidades")
#
#     # 5. Estadísticas de precio
#     prices = [p.price for p in inventory]
#     min_price, max_price, avg_price = min(prices), max(prices), sum(prices) / len(prices)
#     print(f"\n📊 Estadísticas de precio:")
#     print(f"  Mínimo: ${min_price:.2f}")
#     print(f"  Máximo: ${max_price:.2f}")
#     print(f"  Promedio: ${avg_price:.2f}")
#
#     # 6. Crear matriz de resumen (ID x Valor)
#     summary: list[tuple[int, str, float]] = [
#         (p.id, p.name, p.price * p.quantity)
#         for p in inventory
#     ]
#
#     print(f"\n📋 Resumen por valor:")
#     sorted_summary = sorted(summary, key=lambda x: x[2], reverse=True)
#     for id, name, value in sorted_summary:
#         print(f"  {name}: ${value:,.2f}")
#
# manage_inventory()

print()
print("=" * 50)
print("🎉 ¡Ejercicio completado!")
print("=" * 50)
