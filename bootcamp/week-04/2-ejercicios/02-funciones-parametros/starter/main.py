"""
Ejercicio 02: Funciones y Parámetros
====================================
Practica definición de funciones y diferentes tipos de parámetros.

Instrucciones:
1. Lee cada sección
2. Descomenta el código indicado
3. Ejecuta para verificar resultados
"""

import math

# ============================================
# PASO 1: Función Básica
# ============================================
print("=== PASO 1: Función Básica ===")

# Una función encapsula código reutilizable.
# Usa 'def' para definir, 'return' para devolver valor.

# Descomenta las siguientes líneas:
# def calculate_circle_area(radius: float) -> float:
#     """Calcula el área de un círculo dado su radio."""
#     return math.pi * radius ** 2
#
# area = calculate_circle_area(5)
# print(f"Área: {area:.2f}")

print()

# ============================================
# PASO 2: Type Hints y Docstrings
# ============================================
print("=== PASO 2: Type Hints y Docstrings ===")

# Type hints documentan tipos esperados.
# Docstrings explican qué hace la función.

# Descomenta las siguientes líneas:
# def create_greeting(name: str) -> str:
#     """Crea un mensaje de saludo.
#
#     Args:
#         name: El nombre de la persona a saludar.
#
#     Returns:
#         String con el saludo formateado.
#     """
#     return f"¡Hola, {name}!"
#
# print(create_greeting("Ana"))
# print(create_greeting("Bob"))

print()

# ============================================
# PASO 3: Valores por Defecto
# ============================================
print("=== PASO 3: Valores por Defecto ===")

# Los parámetros pueden tener valores por defecto.
# Estos van DESPUÉS de los parámetros sin default.

# Descomenta las siguientes líneas:
# def greet(name: str, greeting: str = "Hola") -> str:
#     """Saluda con un mensaje personalizable.
#
#     Args:
#         name: Nombre de la persona.
#         greeting: Saludo a usar (default: "Hola").
#
#     Returns:
#         Mensaje de saludo completo.
#     """
#     return f"{greeting}, {name}!"
#
# # Usar valor por defecto
# print(greet("Ana"))
#
# # Sobrescribir valor por defecto (posicional)
# print(greet("Bob", "Hi"))
#
# # Sobrescribir con keyword argument
# print(greet("Carlos", greeting="Buenos días"))

print()

# ============================================
# PASO 4: Múltiples Parámetros con Default
# ============================================
print("=== PASO 4: Múltiples Parámetros con Default ===")

# Puedes tener varios parámetros con valores por defecto.

# Descomenta las siguientes líneas:
# def create_user(
#     name: str,
#     age: int,
#     city: str = "Unknown",
#     active: bool = True
# ) -> dict:
#     """Crea un diccionario de usuario.
#
#     Args:
#         name: Nombre del usuario (requerido).
#         age: Edad del usuario (requerido).
#         city: Ciudad (default: "Unknown").
#         active: Estado activo (default: True).
#
#     Returns:
#         Diccionario con datos del usuario.
#     """
#     return {
#         "name": name,
#         "age": age,
#         "city": city,
#         "active": active
#     }
#
# # Solo parámetros requeridos
# print(create_user("Ana", 25))
#
# # Sobrescribir un default
# print(create_user("Bob", 30, "Madrid"))
#
# # Sobrescribir varios defaults con keywords
# print(create_user("Carlos", 35, city="Barcelona", active=False))

print()

# ============================================
# PASO 5: Keyword Arguments
# ============================================
print("=== PASO 5: Keyword Arguments ===")

# Los keyword arguments permiten pasar argumentos por nombre,
# sin importar el orden.

# Descomenta las siguientes líneas:
# def show_args(a: int, b: int, c: int) -> None:
#     """Muestra cómo se reciben los argumentos."""
#     print(f"{a} argumentos posicionales")
#     print(f"{b} argumentos keyword")
#     print(f"Mixto: pos1={a}, key1={c}")
#
# # Posicionales: por orden
# show_args(3, 2, "a")
#
# # También se puede llamar con keywords
# # show_args(a=3, b=2, c="a")
# # show_args(c="a", a=3, b=2)  # El orden no importa con keywords

print()

# ============================================
# PASO 6: Return Múltiple
# ============================================
print("=== PASO 6: Return Múltiple ===")

# Python permite retornar múltiples valores como tupla.

# Descomenta las siguientes líneas:
# def get_statistics(numbers: list[int]) -> tuple[int, int, float]:
#     """Calcula estadísticas de una lista.
#
#     Args:
#         numbers: Lista de números.
#
#     Returns:
#         Tupla con (mínimo, máximo, promedio).
#     """
#     minimum = min(numbers)
#     maximum = max(numbers)
#     average = sum(numbers) / len(numbers)
#     return minimum, maximum, average
#
# data = [1, 5, 3, 9, 2, 7]
#
# # Desempaquetar resultados
# min_val, max_val, avg = get_statistics(data)
# print(f"Min: {min_val}, Max: {max_val}, Promedio: {avg}")
#
# # O como tupla
# stats = get_statistics(data)
# print(f"Estadísticas: {stats}")

print()

# ============================================
# PASO 7: Early Return
# ============================================
print("=== PASO 7: Early Return ===")

# Early return simplifica el código manejando casos especiales primero.

# Descomenta las siguientes líneas:
# def safe_divide(a: float, b: float) -> float | str:
#     """Divide a entre b de forma segura.
#
#     Args:
#         a: Dividendo.
#         b: Divisor.
#
#     Returns:
#         Resultado de la división o mensaje de error.
#     """
#     # Early return para caso especial
#     if b == 0:
#         return "Error: divisor es cero"
#
#     # Lógica principal
#     return a / b
#
# print(safe_divide(10, 0))
# print(f"Resultado: {safe_divide(10, 2)}")

print()

# ============================================
# PASO 8: Funciones que Llaman Funciones
# ============================================
print("=== PASO 8: Funciones que Llaman Funciones ===")

# Las funciones pueden llamar a otras funciones.

# Descomenta las siguientes líneas:
# def celsius_to_fahrenheit(celsius: float) -> float:
#     """Convierte Celsius a Fahrenheit."""
#     return (celsius * 9/5) + 32
#
# def fahrenheit_to_celsius(fahrenheit: float) -> float:
#     """Convierte Fahrenheit a Celsius."""
#     return (fahrenheit - 32) * 5/9
#
# def round_trip_conversion(celsius: float) -> float:
#     """Convierte C->F->C para verificar precisión."""
#     fahrenheit = celsius_to_fahrenheit(celsius)
#     back_to_celsius = fahrenheit_to_celsius(fahrenheit)
#     return back_to_celsius
#
# temp_c = 25
# temp_f = celsius_to_fahrenheit(temp_c)
# print(f"Celsius: {temp_c} -> Fahrenheit: {temp_f}")
#
# temp_back = fahrenheit_to_celsius(temp_f)
# print(f"Fahrenheit: {temp_f} -> Celsius: {temp_back}")
#
# print(f"Round trip: {round_trip_conversion(temp_c)}")

print()

# ============================================
# PASO 9: Caso Práctico - Calculadora
# ============================================
print("=== PASO 9: Caso Práctico - Calculadora ===")

# Crear funciones para una calculadora simple.

# Descomenta las siguientes líneas:
# def add(a: float, b: float) -> float:
#     """Suma dos números."""
#     return a + b
#
# def subtract(a: float, b: float) -> float:
#     """Resta b de a."""
#     return a - b
#
# def multiply(a: float, b: float) -> float:
#     """Multiplica dos números."""
#     return a * b
#
# def divide(a: float, b: float) -> float | str:
#     """Divide a entre b. Retorna error si b es 0."""
#     if b == 0:
#         return "Error: División por cero"
#     return a / b
#
# x, y = 10, 5
# print(f"{x} + {y} = {add(x, y)}")
# print(f"{x} - {y} = {subtract(x, y)}")
# print(f"{x} * {y} = {multiply(x, y)}")
# print(f"{x} / {y} = {divide(x, y)}")
# print(f"{x} / 0 = {divide(x, 0)}")


# ============================================
# ¡FELICIDADES! 🎉
# ============================================
# Has completado el ejercicio de funciones y parámetros.
# Ahora dominas:
# - Definición de funciones con def
# - Type hints y docstrings
# - Parámetros con valores por defecto
# - Keyword arguments
# - Return múltiple y early return
