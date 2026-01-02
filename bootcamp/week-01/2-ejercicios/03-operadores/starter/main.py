"""
Ejercicio 03: Operadores

Instrucciones:
1. Lee cada sección y su explicación
2. Descomenta el código de cada paso
3. Ejecuta el programa para ver los resultados
4. Avanza al siguiente paso

Comando para ejecutar:
docker run -it --rm -v $(pwd):/app -w /app python:3.13-slim python starter/main.py
"""

# ============================================
# PASO 1: Operadores aritméticos básicos
# ============================================
print("--- Paso 1: Operadores aritméticos básicos ---")

# Los operadores básicos: + - * /
# Descomenta las siguientes líneas:
# a: int = 10
# b: int = 3
#
# print(f"a = {a}, b = {b}")
# print(f"{a} + {b} = {a + b}")
# print(f"{a} - {b} = {a - b}")
# print(f"{a} * {b} = {a * b}")
# print(f"{a} / {b} = {a / b}")  # Siempre retorna float

print()


# ============================================
# PASO 2: División entera, módulo y potencia
# ============================================
print("--- Paso 2: División entera, módulo y potencia ---")

# // división entera (trunca decimales)
# %  módulo (resto de la división)
# ** potencia
# Descomenta las siguientes líneas:
# print(f"10 // 3 = {10 // 3} (división entera)")
# print(f"10 % 3 = {10 % 3} (resto/módulo)")
# print(f"2 ** 8 = {2 ** 8} (potencia)")

print()


# ============================================
# PASO 3: Operadores de comparación
# ============================================
print("--- Paso 3: Operadores de comparación ---")

# Comparan valores y retornan True o False
# == igual, != diferente
# > mayor, < menor
# >= mayor o igual, <= menor o igual
# Descomenta las siguientes líneas:
# x: int = 10
# y: int = 5
#
# print(f"x = {x}, y = {y}")
# print(f"{x} == {y}: {x == y}")
# print(f"{x} != {y}: {x != y}")
# print(f"{x} > {y}: {x > y}")
# print(f"{x} < {y}: {x < y}")
# print(f"{x} >= {x}: {x >= x}")
# print(f"{x} <= {y}: {x <= y}")

print()


# ============================================
# PASO 4: Operadores lógicos
# ============================================
print("--- Paso 4: Operadores lógicos ---")

# and: True si AMBOS son True
# or:  True si AL MENOS UNO es True
# not: invierte el valor
# Descomenta las siguientes líneas:
# print(f"True and True: {True and True}")
# print(f"True and False: {True and False}")
# print(f"True or False: {True or False}")
# print(f"False or False: {False or False}")
# print(f"not True: {not True}")
# print(f"not False: {not False}")

print()


# ============================================
# PASO 5: Operadores de asignación
# ============================================
print("--- Paso 5: Operadores de asignación ---")

# Atajos para modificar variables
# +=  suma y asigna
# -=  resta y asigna
# *=  multiplica y asigna
# //= divide (entero) y asigna
# Descomenta las siguientes líneas:
# puntos: int = 100
# print(f"Valor inicial: {puntos}")
#
# puntos += 10  # puntos = puntos + 10
# print(f"Después de += 10: {puntos}")
#
# puntos -= 20  # puntos = puntos - 20
# print(f"Después de -= 20: {puntos}")
#
# puntos *= 2   # puntos = puntos * 2
# print(f"Después de *= 2: {puntos}")
#
# puntos //= 3  # puntos = puntos // 3
# print(f"Después de //= 3: {puntos}")

print()


# ============================================
# PASO 6: Aplicación - Convertir minutos
# ============================================
print("--- Paso 6: Aplicación - Convertir minutos ---")

# Problema práctico: convertir minutos totales a horas y minutos
# Usamos // para obtener las horas y % para los minutos restantes
# Descomenta las siguientes líneas:
# def convertir_minutos(minutos_totales: int) -> None:
#     """Convierte minutos totales a formato horas:minutos"""
#     horas: int = minutos_totales // 60
#     minutos: int = minutos_totales % 60
#     print(f"{minutos_totales} minutos = {horas} horas y {minutos} minutos")
#
# convertir_minutos(150)
# convertir_minutos(200)
# convertir_minutos(45)


# ============================================
# ¡FELICIDADES!
# ============================================
# Has completado el ejercicio de operadores.
# Ahora dominas:
# - Operadores aritméticos (+, -, *, /, //, %, **)
# - Operadores de comparación (==, !=, >, <, >=, <=)
# - Operadores lógicos (and, or, not)
# - Operadores de asignación (+=, -=, *=, etc.)
