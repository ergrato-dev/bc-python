"""
Ejercicio 03: Polimorfismo
==========================
Practica polimorfismo con herencia y Duck Typing.

Instrucciones:
1. Lee cada sección comentada
2. Descomenta el código paso a paso
3. Ejecuta para ver los resultados
"""

import math


# ============================================
# PASO 1: Clase Base Shape
# ============================================
print("=== Paso 1: Clase Base Shape ===")

# Shape define la interfaz que todas las formas deben implementar
# Los métodos lanzan NotImplementedError para forzar override
# Descomenta las siguientes líneas:

# class Shape:
#     """Clase base abstracta para formas geométricas."""
#
#     def area(self) -> float:
#         """Calcula el área de la forma."""
#         raise NotImplementedError("Subclasses must implement area()")
#
#     def perimeter(self) -> float:
#         """Calcula el perímetro de la forma."""
#         raise NotImplementedError("Subclasses must implement perimeter()")
#
#     def describe(self) -> str:
#         """Describe la forma con su área y perímetro."""
#         name = type(self).__name__
#         return f"{name}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"
#
# print("Shape base class defined")

print()


# ============================================
# PASO 2: Circle
# ============================================
print("=== Paso 2: Circle ===")

# Circle implementa area() y perimeter() para un círculo
# Usa math.pi para precisión
# Descomenta las siguientes líneas:

# class Circle(Shape):
#     """Círculo definido por su radio."""
#
#     def __init__(self, radius: float) -> None:
#         self.radius = radius
#
#     def area(self) -> float:
#         """Área = π * r²"""
#         return math.pi * self.radius ** 2
#
#     def perimeter(self) -> float:
#         """Perímetro (circunferencia) = 2 * π * r"""
#         return 2 * math.pi * self.radius
#
# # Probar Circle
# circle = Circle(5)
# print(f"Circle with radius 5:")
# print(f"  Area: {circle.area():.2f}")
# print(f"  Perimeter: {circle.perimeter():.2f}")
# print(f"  {circle.describe()}")

print()


# ============================================
# PASO 3: Rectangle
# ============================================
print("=== Paso 3: Rectangle ===")

# Rectangle tiene width y height
# Descomenta las siguientes líneas:

# class Rectangle(Shape):
#     """Rectángulo definido por ancho y alto."""
#
#     def __init__(self, width: float, height: float) -> None:
#         self.width = width
#         self.height = height
#
#     def area(self) -> float:
#         """Área = ancho * alto"""
#         return self.width * self.height
#
#     def perimeter(self) -> float:
#         """Perímetro = 2 * (ancho + alto)"""
#         return 2 * (self.width + self.height)
#
# # Probar Rectangle
# rect = Rectangle(4, 6)
# print(f"Rectangle 4x6:")
# print(f"  Area: {rect.area():.2f}")
# print(f"  Perimeter: {rect.perimeter():.2f}")
# print(f"  {rect.describe()}")

print()


# ============================================
# PASO 4: Triangle
# ============================================
print("=== Paso 4: Triangle ===")

# Triangle usa la fórmula de Herón para calcular el área
# Necesita los tres lados: a, b, c
# Descomenta las siguientes líneas:

# class Triangle(Shape):
#     """Triángulo definido por sus tres lados."""
#
#     def __init__(self, a: float, b: float, c: float) -> None:
#         self.a = a
#         self.b = b
#         self.c = c
#
#     def area(self) -> float:
#         """Área usando la fórmula de Herón."""
#         # s = semiperímetro
#         s = self.perimeter() / 2
#         # Área = √(s(s-a)(s-b)(s-c))
#         return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
#
#     def perimeter(self) -> float:
#         """Perímetro = suma de los tres lados"""
#         return self.a + self.b + self.c
#
# # Probar Triangle (triángulo 3-4-5, rectángulo)
# triangle = Triangle(3, 4, 5)
# print(f"Triangle with sides 3, 4, 5:")
# print(f"  Area: {triangle.area():.2f}")
# print(f"  Perimeter: {triangle.perimeter():.2f}")
# print(f"  {triangle.describe()}")

print()


# ============================================
# PASO 5: Funciones Polimórficas
# ============================================
print("=== Paso 5: Funciones Polimórficas ===")

# Funciones que trabajan con CUALQUIER Shape
# El polimorfismo permite código genérico y reutilizable
# Descomenta las siguientes líneas:

# def print_shape_info(shape: Shape) -> None:
#     """Imprime información de cualquier forma geométrica."""
#     print(shape.describe())
#
#
# def total_area(shapes: list[Shape]) -> float:
#     """Calcula el área total de una lista de formas."""
#     return sum(shape.area() for shape in shapes)
#
#
# def total_perimeter(shapes: list[Shape]) -> float:
#     """Calcula el perímetro total de una lista de formas."""
#     return sum(shape.perimeter() for shape in shapes)
#
#
# def largest_shape(shapes: list[Shape]) -> Shape:
#     """Encuentra la forma con mayor área."""
#     return max(shapes, key=lambda s: s.area())
#
#
# def smallest_shape(shapes: list[Shape]) -> Shape:
#     """Encuentra la forma con menor área."""
#     return min(shapes, key=lambda s: s.area())
#
# print("Polymorphic functions defined")

print()


# ============================================
# PASO 6: Usar Polimorfismo
# ============================================
print("=== Paso 6: Polimorfismo en Acción ===")

# Crear lista mixta de formas y usar funciones polimórficas
# Cada forma usa SU implementación de area() y perimeter()
# Descomenta las siguientes líneas:

# # Crear varias formas
# shapes: list[Shape] = [
#     Circle(5),
#     Rectangle(4, 6),
#     Triangle(3, 4, 5),
#     Circle(3),
#     Rectangle(10, 2)
# ]
#
# # Mostrar información de cada forma
# print("All shapes:")
# for shape in shapes:
#     print_shape_info(shape)
#
# print()
#
# # Calcular totales
# print(f"Total area: {total_area(shapes):.2f}")
# print(f"Total perimeter: {total_perimeter(shapes):.2f}")
#
# print()
#
# # Encontrar extremos
# largest = largest_shape(shapes)
# smallest = smallest_shape(shapes)
# print(f"Largest shape: {largest.describe()}")
# print(f"Smallest shape: {smallest.describe()}")

print()


# ============================================
# PASO 7: Duck Typing
# ============================================
print("=== Paso 7: Duck Typing ===")

# Square NO hereda de Shape pero tiene los mismos métodos
# Python usa Duck Typing: "si hace cuac, es un pato"
# Descomenta las siguientes líneas:

# class Square:
#     """Square NO hereda de Shape pero tiene los mismos métodos."""
#
#     def __init__(self, side: float) -> None:
#         self.side = side
#
#     def area(self) -> float:
#         """Área = lado²"""
#         return self.side ** 2
#
#     def perimeter(self) -> float:
#         """Perímetro = 4 * lado"""
#         return 4 * self.side
#
#     def describe(self) -> str:
#         """Descripción del cuadrado."""
#         return f"Square: area={self.area():.2f}, perimeter={self.perimeter():.2f}"
#
#
# # Crear un Square
# square = Square(5)
#
# # ¡Las funciones polimórficas funcionan aunque Square no hereda de Shape!
# print("Square (no hereda de Shape):")
# print_shape_info(square)  # Duck typing en acción
#
# print()
#
# # Incluso funciona en listas mixtas
# mixed_shapes = [Circle(3), Rectangle(2, 4), square]
# print(f"Total area (including Square): {total_area(mixed_shapes):.2f}")

print()


# ============================================
# PASO 8: Protocol para Type Safety
# ============================================
print("=== Paso 8: Protocol ===")

# Protocol define una "interfaz" sin requerir herencia
# Permite type hints con Duck Typing
# Descomenta las siguientes líneas:

# from typing import Protocol
#
#
# class ShapeLike(Protocol):
#     """Protocolo que define qué significa ser 'como una forma'."""
#
#     def area(self) -> float: ...
#     def perimeter(self) -> float: ...
#     def describe(self) -> str: ...
#
#
# def print_shape_info_typed(shape: ShapeLike) -> None:
#     """Versión type-safe usando Protocol."""
#     print(shape.describe())
#
#
# def total_area_typed(shapes: list[ShapeLike]) -> float:
#     """Versión type-safe usando Protocol."""
#     return sum(s.area() for s in shapes)
#
#
# # Funciona con Circle (que hereda de Shape)
# print("Using Protocol:")
# print_shape_info_typed(Circle(3))
#
# # También funciona con Square (que NO hereda de Shape)
# print_shape_info_typed(Square(4))
#
# print()
#
# # Lista mixta con Protocol
# all_shapes: list[ShapeLike] = [
#     Circle(2),
#     Rectangle(3, 4),
#     Square(5)
# ]
#
# print(f"Total area (with Protocol): {total_area_typed(all_shapes):.2f}")


print()


# ============================================
# BONUS: Comparación de Enfoques
# ============================================
print("=== Bonus: Comparación ===")

# Compara los tres enfoques: Herencia, Duck Typing, Protocol
# Descomenta las siguientes líneas:

# print("Comparación de enfoques para polimorfismo:")
# print()
# print("1. HERENCIA (Circle, Rectangle, Triangle)")
# print("   ✓ Explícito - relación clara entre clases")
# print("   ✓ IDE y type checkers entienden la jerarquía")
# print("   ✗ Menos flexible - requiere modificar código existente")
# print()
# print("2. DUCK TYPING (Square)")
# print("   ✓ Muy flexible - no requiere herencia")
# print("   ✓ Permite integrar clases de terceros")
# print("   ✗ Sin verificación de tipos en tiempo de desarrollo")
# print()
# print("3. PROTOCOL (ShapeLike)")
# print("   ✓ Combina flexibilidad de Duck Typing con type hints")
# print("   ✓ Type checkers pueden verificar")
# print("   ✗ Requiere Python 3.8+ y más código")


print("\n✅ Ejercicio completado!")
