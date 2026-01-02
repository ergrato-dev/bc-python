"""
Ejercicio 02: Condicionales
===========================

Objetivo: Dominar estructuras if/elif/else y operador ternario.

Instrucciones:
1. Lee cada sección
2. Descomenta el código indicado
3. Ejecuta y verifica los resultados
"""

# ============================================
# PASO 1: Estructura if Básica
# ============================================
print("=== ESTRUCTURA IF BÁSICA ===")

# El if ejecuta un bloque solo si la condición es True
# Descomenta las siguientes líneas:

# age: int = 20
#
# if age >= 18:
#     print("Eres mayor de edad")
#     print("Puedes votar")
#
# # El programa continúa independientemente
# print("Verificación de edad completada")

# Verificar con input (opcional)
# user_age: int = int(input("Ingresa tu edad: "))
# if user_age >= 18:
#     print("Bienvenido al sistema")

print()

# ============================================
# PASO 2: Estructura if-else
# ============================================
print("=== ESTRUCTURA IF-ELSE ===")

# else se ejecuta cuando la condición del if es False
# Descomenta las siguientes líneas:

# temperature: float = 15.0
#
# if temperature > 25:
#     print("Hace calor, usa ropa ligera")
# else:
#     print("No hace tanto calor")
#
# # Ejemplo con validación
# password: str = "secret123"
# user_input: str = "secret123"  # Simula input del usuario
#
# if user_input == password:
#     print("✅ Acceso concedido")
# else:
#     print("❌ Contraseña incorrecta")

print()

# ============================================
# PASO 3: Estructura if-elif-else
# ============================================
print("=== IF-ELIF-ELSE ===")

# elif permite múltiples condiciones
# Descomenta las siguientes líneas:

# score: int = 85
#
# if score >= 90:
#     grade = "A - Excelente"
# elif score >= 80:
#     grade = "B - Muy bien"
# elif score >= 70:
#     grade = "C - Bien"
# elif score >= 60:
#     grade = "D - Suficiente"
# else:
#     grade = "F - Reprobado"
#
# print(f"Puntaje: {score}")
# print(f"Tu calificación es: {grade}")

# Clasificador de edad
# age: int = 25
#
# if age < 0:
#     category = "Edad inválida"
# elif age < 13:
#     category = "Niño"
# elif age < 18:
#     category = "Adolescente"
# elif age < 65:
#     category = "Adulto"
# else:
#     category = "Adulto mayor"
#
# print(f"Edad: {age} - Categoría: {category}")

print()

# ============================================
# PASO 4: Condiciones Compuestas
# ============================================
print("=== CONDICIONES COMPUESTAS ===")

# Combina condiciones con and, or, not
# Descomenta las siguientes líneas:

# age: int = 25
# has_license: bool = True
# has_car: bool = False
#
# # AND - ambas deben ser True
# if age >= 18 and has_license:
#     print("Puede conducir legalmente")
#
# # OR - al menos una debe ser True
# day: str = "Saturday"
# if day == "Saturday" or day == "Sunday":
#     print("Es fin de semana")
#
# # Forma más elegante con in
# if day in ["Saturday", "Sunday"]:
#     print("Es fin de semana (con in)")
#
# # NOT - invierte la condición
# is_raining: bool = False
# if not is_raining:
#     print("Buen día para salir")
#
# # Combinación compleja
# if age >= 18 and has_license and (has_car or day == "Saturday"):
#     print("Puede hacer un viaje")

print()

# ============================================
# PASO 5: Operador Ternario
# ============================================
print("=== OPERADOR TERNARIO ===")

# Sintaxis: valor_si_true if condición else valor_si_false
# Descomenta las siguientes líneas:

# age: int = 20
#
# # Forma tradicional
# if age >= 18:
#     status_traditional = "adulto"
# else:
#     status_traditional = "menor"
#
# # Forma ternaria (equivalente)
# status_ternary = "adulto" if age >= 18 else "menor"
#
# print(f"Estado (tradicional): {status_traditional}")
# print(f"Estado (ternario): {status_ternary}")
#
# # En f-strings
# count: int = 1
# print(f"Hay {count} {'item' if count == 1 else 'items'}")
#
# count = 5
# print(f"Hay {count} {'item' if count == 1 else 'items'}")
#
# # Valor absoluto con ternario
# number: int = -7
# absolute = number if number >= 0 else -number
# print(f"Valor absoluto de {number}: {absolute}")

print()

# ============================================
# PASO 6: Validaciones Prácticas
# ============================================
print("=== VALIDACIONES PRÁCTICAS ===")

# Patrones comunes de validación
# Descomenta las siguientes líneas:

# # Validar rango
# def validate_percentage(value: float) -> bool:
#     """Verifica si el valor está entre 0 y 100."""
#     return 0 <= value <= 100
#
# print(f"50 es porcentaje válido: {validate_percentage(50)}")
# print(f"150 es porcentaje válido: {validate_percentage(150)}")
#
# # Validar string no vacío
# def validate_name(name: str) -> str:
#     """Retorna el nombre o 'Anónimo' si está vacío."""
#     if name.strip():  # strip() quita espacios
#         return name.strip()
#     else:
#         return "Anónimo"
#
# print(f"Nombre: {validate_name('  Ana  ')}")
# print(f"Nombre: {validate_name('   ')}")
#
# # Validar opciones
# def validate_choice(choice: str, valid_options: list[str]) -> bool:
#     """Verifica si la elección está en las opciones válidas."""
#     return choice.lower() in [opt.lower() for opt in valid_options]
#
# options = ["rock", "paper", "scissors"]
# print(f"'Rock' es válido: {validate_choice('Rock', options)}")
# print(f"'fire' es válido: {validate_choice('fire', options)}")

print()

# ============================================
# DESAFÍO EXTRA
# ============================================
print("=== DESAFÍO EXTRA ===")

# Implementa un clasificador de triángulos
# Según sus lados: equilátero, isósceles, escaleno
# También valida que los lados formen un triángulo válido
# Descomenta y completa:

# def classify_triangle(a: float, b: float, c: float) -> str:
#     """
#     Clasifica un triángulo según sus lados.
#
#     Returns:
#         - "No es un triángulo válido" si no cumple la desigualdad triangular
#         - "Equilátero" si todos los lados son iguales
#         - "Isósceles" si dos lados son iguales
#         - "Escaleno" si todos los lados son diferentes
#     """
#     # Validar que sea un triángulo (desigualdad triangular)
#     if a + b <= c or b + c <= a or a + c <= b:
#         return "No es un triángulo válido"
#
#     # Clasificar
#     if a == b == c:
#         return "Equilátero"
#     elif a == b or b == c or a == c:
#         return "Isósceles"
#     else:
#         return "Escaleno"
#
# # Tests
# print(f"(3, 3, 3): {classify_triangle(3, 3, 3)}")      # Equilátero
# print(f"(3, 3, 4): {classify_triangle(3, 3, 4)}")      # Isósceles
# print(f"(3, 4, 5): {classify_triangle(3, 4, 5)}")      # Escaleno
# print(f"(1, 2, 10): {classify_triangle(1, 2, 10)}")    # No válido

print("\n✅ Ejercicio completado!")
