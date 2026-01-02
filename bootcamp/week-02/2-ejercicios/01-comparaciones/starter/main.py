"""
Ejercicio 01: Comparaciones
===========================

Objetivo: Practicar operadores de comparación, identidad y pertenencia.

Instrucciones:
1. Lee cada sección
2. Descomenta el código indicado
3. Ejecuta y verifica los resultados
"""

# ============================================
# PASO 1: Comparaciones Numéricas Básicas
# ============================================
print("=== COMPARACIONES NUMÉRICAS ===")

# Los operadores de comparación retornan True o False
# Descomenta las siguientes líneas:

# x: int = 10
# y: int = 5
# z: int = 10
#
# print(f"{x} > {y}: {x > y}")      # Mayor que
# print(f"{x} < {y}: {x < y}")      # Menor que
# print(f"{x} == {z}: {x == z}")    # Igual a
# print(f"{x} != {y}: {x != y}")    # Diferente de
# print(f"{x} >= {z}: {x >= z}")    # Mayor o igual
# print(f"{y} <= {x}: {y <= x}")    # Menor o igual

# Comparación con floats
# pi: float = 3.14159
# print(f"3 < {pi}: {3 < pi}")
# print(f"3 == 3.0: {3 == 3.0}")    # int y float pueden compararse

print()

# ============================================
# PASO 2: Comparaciones de Strings
# ============================================
print("=== COMPARACIONES DE STRINGS ===")

# Los strings se comparan lexicográficamente (Unicode)
# Descomenta las siguientes líneas:

# word1: str = "apple"
# word2: str = "banana"
# word3: str = "Apple"
#
# print(f"'{word1}' < '{word2}': {word1 < word2}")   # 'a' < 'b'
# print(f"'{word3}' < '{word1}': {word3 < word1}")   # 'A' (65) < 'a' (97)
# print(f"'{word1}' == '{word1}': {word1 == word1}") # Exactamente igual
# print(f"'{word1}' == '{word3}': {word1 == word3}") # Case-sensitive

# Comparación de longitud (usa len())
# name1: str = "Ana"
# name2: str = "Alexander"
# print(f"len('{name1}') < len('{name2}'): {len(name1) < len(name2)}")

print()

# ============================================
# PASO 3: Igualdad vs Identidad
# ============================================
print("=== IGUALDAD VS IDENTIDAD ===")

# == compara VALORES, is compara IDENTIDAD (mismo objeto en memoria)
# Descomenta las siguientes líneas:

# list1: list[int] = [1, 2, 3]
# list2: list[int] = [1, 2, 3]
# list3: list[int] = list1  # list3 es un alias de list1
#
# # Comparación de valor
# print(f"list1 == list2: {list1 == list2}")  # True - mismo contenido
# print(f"list1 == list3: {list1 == list3}")  # True - mismo contenido
#
# # Comparación de identidad
# print(f"list1 is list2: {list1 is list2}")  # False - objetos diferentes
# print(f"list1 is list3: {list1 is list3}")  # True - mismo objeto
#
# # Verificar con id()
# print(f"id(list1): {id(list1)}")
# print(f"id(list2): {id(list2)}")
# print(f"id(list3): {id(list3)}")

# Caso especial: None
# value: int | None = None
# print(f"value is None: {value is None}")      # ✅ Forma correcta
# print(f"value == None: {value == None}")      # Funciona pero no pythónico

print()

# ============================================
# PASO 4: Operadores de Pertenencia
# ============================================
print("=== OPERADORES DE PERTENENCIA ===")

# in verifica si un elemento existe en una secuencia
# Descomenta las siguientes líneas:

# # Con listas
# fruits: list[str] = ["apple", "banana", "orange"]
# print(f"'apple' in fruits: {'apple' in fruits}")
# print(f"'grape' in fruits: {'grape' in fruits}")
# print(f"'grape' not in fruits: {'grape' not in fruits}")
#
# # Con strings (busca substring)
# message: str = "Hello, Python!"
# print(f"'Python' in message: {'Python' in message}")
# print(f"'Java' in message: {'Java' in message}")
#
# # Con diccionarios (busca en keys por defecto)
# user: dict[str, str | int] = {"name": "Ana", "age": 25}
# print(f"'name' in user: {'name' in user}")       # True - busca en keys
# print(f"'Ana' in user: {'Ana' in user}")         # False - 'Ana' no es key
# print(f"'Ana' in user.values(): {'Ana' in user.values()}")  # True

print()

# ============================================
# PASO 5: Comparaciones Encadenadas
# ============================================
print("=== COMPARACIONES ENCADENADAS ===")

# Python permite encadenar comparaciones de forma elegante
# Descomenta las siguientes líneas:

# age: int = 25
# temperature: float = 22.5
# score: int = 85
#
# # En lugar de: age >= 18 and age <= 65
# print(f"18 <= {age} <= 65: {18 <= age <= 65}")  # Forma pythónica
#
# # Múltiples encadenamientos
# print(f"20 < {temperature} < 30: {20 < temperature < 30}")
#
# # También con igualdad
# a, b, c = 1, 2, 3
# print(f"{a} < {b} < {c}: {a < b < c}")
# print(f"{a} <= {b} <= {c}: {a <= b <= c}")
#
# # Rango de calificación
# print(f"70 <= {score} < 90: {70 <= score < 90}")

print()

# ============================================
# DESAFÍO EXTRA
# ============================================
print("=== DESAFÍO EXTRA ===")

# Implementa una función que verifique si un año es bisiesto
# Reglas:
# - Divisible por 4 Y (no divisible por 100 O divisible por 400)
# Descomenta y completa:

# def is_leap_year(year: int) -> bool:
#     """Determina si un año es bisiesto."""
#     return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
#
# # Tests
# print(f"2024 es bisiesto: {is_leap_year(2024)}")  # True
# print(f"2023 es bisiesto: {is_leap_year(2023)}")  # False
# print(f"2000 es bisiesto: {is_leap_year(2000)}")  # True
# print(f"1900 es bisiesto: {is_leap_year(1900)}")  # False

print("\n✅ Ejercicio completado!")
