"""
Ejercicio 02: While y Validación
================================
Aprende el bucle while, validación de entrada y menús interactivos.

Instrucciones:
- Lee cada sección y descomenta el código correspondiente
- Los pasos 3-8 son INTERACTIVOS (requieren entrada del usuario)
- Ejecuta un paso a la vez para practicar cada concepto
"""

# ============================================
# PASO 1: While básico
# ============================================
print("--- Paso 1: While básico ---")

# El bucle while repite mientras la condición sea True
# Descomenta las siguientes líneas:

# count: int = 1
#
# while count <= 5:
#     print(f"Iteración {count}")
#     count += 1  # ¡Importante! Sin esto, bucle infinito
#
# print("Fin del bucle\n")


# ============================================
# PASO 2: Cuenta regresiva
# ============================================
print("--- Paso 2: Cuenta regresiva ---")

# Usar while para contar hacia atrás
# Descomenta las siguientes líneas:

# def countdown(n: int) -> None:
#     """Cuenta regresiva desde n hasta 1."""
#     while n > 0:
#         print(n, end=" ")
#         n -= 1
#     print("¡Despegue! 🚀")
#
# countdown(10)
# print()


# ============================================
# PASO 3: Validación de entrada numérica
# ============================================
print("--- Paso 3: Validación numérica ---")

# Solicitar un número positivo hasta que sea válido
# ⚠️ INTERACTIVO: Descomenta y ejecuta para probar

# def get_positive_number() -> int:
#     """Solicita un número positivo al usuario."""
#     number: int = -1
#
#     while number <= 0:
#         try:
#             number = int(input("Ingresa un número positivo: "))
#             if number <= 0:
#                 print("❌ Debe ser mayor que cero.")
#         except ValueError:
#             print("❌ Eso no es un número válido.")
#
#     return number
#
# result = get_positive_number()
# print(f"✅ Número válido: {result}\n")


# ============================================
# PASO 4: Validación con límite de intentos
# ============================================
print("--- Paso 4: Límite de intentos ---")

# Simular login con máximo 3 intentos
# ⚠️ INTERACTIVO: La contraseña correcta es "python123"

# def login_simulation() -> bool:
#     """Simula un login con intentos limitados."""
#     correct_password: str = "python123"
#     max_attempts: int = 3
#     attempts: int = 0
#
#     while attempts < max_attempts:
#         password = input(f"Contraseña ({max_attempts - attempts} intentos): ")
#         attempts += 1
#
#         if password == correct_password:
#             print("✅ ¡Acceso concedido!")
#             return True
#         else:
#             print("❌ Contraseña incorrecta.")
#
#     print("🚫 Demasiados intentos fallidos.")
#     return False
#
# login_simulation()
# print()


# ============================================
# PASO 5: Validación con flag (bandera)
# ============================================
print("--- Paso 5: Validación con flag ---")

# Usar una variable booleana para controlar el bucle
# ⚠️ INTERACTIVO: Ingresa "si" o "no"

# def get_yes_no() -> str:
#     """Solicita respuesta si/no al usuario."""
#     valid: bool = False
#     response: str = ""
#
#     while not valid:
#         response = input("¿Continuar? (si/no): ").lower().strip()
#
#         if response in ["si", "sí", "no"]:
#             valid = True
#         else:
#             print("❌ Por favor, ingresa 'si' o 'no'.")
#
#     return response
#
# answer = get_yes_no()
# print(f"✅ Respondiste: {answer}\n")


# ============================================
# PASO 6: While True con break
# ============================================
print("--- Paso 6: While True con break ---")

# Bucle infinito controlado con break
# ⚠️ INTERACTIVO: Escribe "salir" para terminar

# def command_processor() -> None:
#     """Procesa comandos hasta recibir 'salir'."""
#     print("Procesador de comandos (escribe 'salir' para terminar)")
#
#     while True:
#         command = input(">>> ").strip().lower()
#
#         if command == "salir":
#             print("👋 ¡Hasta luego!")
#             break
#         elif command == "":
#             continue  # Ignorar entrada vacía
#         elif command == "ayuda":
#             print("Comandos: ayuda, hola, fecha, salir")
#         elif command == "hola":
#             print("¡Hola! 👋")
#         elif command == "fecha":
#             from datetime import date
#             print(f"Hoy es: {date.today()}")
#         else:
#             print(f"Comando desconocido: '{command}'")
#
# command_processor()
# print()


# ============================================
# PASO 7: Acumulador con while
# ============================================
print("--- Paso 7: Acumulador ---")

# Sumar números hasta que el usuario termine
# ⚠️ INTERACTIVO: Ingresa números, enter vacío para terminar

# def sum_numbers() -> int:
#     """Suma números ingresados por el usuario."""
#     total: int = 0
#     count: int = 0
#
#     print("Ingresa números (enter vacío para terminar):")
#
#     while True:
#         user_input = input(f"  Número {count + 1}: ").strip()
#
#         if user_input == "":
#             break
#
#         try:
#             number = int(user_input)
#             total += number
#             count += 1
#             print(f"    Suma parcial: {total}")
#         except ValueError:
#             print("    ❌ No es un número válido, ignorado.")
#
#     return total
#
# final_sum = sum_numbers()
# print(f"✅ Suma total: {final_sum}\n")


# ============================================
# PASO 8: Menú interactivo
# ============================================
print("--- Paso 8: Menú interactivo ---")

# Crear un menú con opciones
# ⚠️ INTERACTIVO: Selecciona opciones 1-4

# def calculator_menu() -> None:
#     """Calculadora con menú interactivo."""
#     option: str = ""
#
#     while option != "4":
#         print("\n╔════════════════════════╗")
#         print("║   🧮 CALCULADORA      ║")
#         print("╠════════════════════════╣")
#         print("║ 1. Sumar              ║")
#         print("║ 2. Restar             ║")
#         print("║ 3. Multiplicar        ║")
#         print("║ 4. Salir              ║")
#         print("╚════════════════════════╝")
#
#         option = input("Elige una opción: ").strip()
#
#         if option in ["1", "2", "3"]:
#             try:
#                 a = float(input("  Primer número: "))
#                 b = float(input("  Segundo número: "))
#
#                 match option:
#                     case "1":
#                         print(f"  ✅ {a} + {b} = {a + b}")
#                     case "2":
#                         print(f"  ✅ {a} - {b} = {a - b}")
#                     case "3":
#                         print(f"  ✅ {a} × {b} = {a * b}")
#             except ValueError:
#                 print("  ❌ Números inválidos.")
#         elif option == "4":
#             print("👋 ¡Hasta luego!")
#         else:
#             print("❌ Opción no válida.")
#
# calculator_menu()


# ============================================
# RESUMEN
# ============================================
print("\n" + "=" * 50)
print("¡Ejercicio completado!")
print("=" * 50)
print("""
Conceptos aprendidos:
✅ while condición: repite mientras sea True
✅ Siempre actualizar la variable de control
✅ try/except para manejar errores de entrada
✅ Límite de intentos con contador
✅ Flag (bandera) booleana para control
✅ while True + break para bucles controlados
✅ Acumulador con entrada de usuario
✅ Menú interactivo con match
""")
