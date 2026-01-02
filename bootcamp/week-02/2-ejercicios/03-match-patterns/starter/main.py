"""
Ejercicio 03: Match Patterns
============================

Objetivo: Dominar el pattern matching básico de Python 3.10+.

Instrucciones:
1. Lee cada sección
2. Descomenta el código indicado
3. Ejecuta y verifica los resultados

Nota: Requiere Python 3.10 o superior.
"""

# ============================================
# PASO 1: Match Básico con Strings
# ============================================
print("=== MATCH BÁSICO ===")

# La sintaxis básica de match/case con strings
# Descomenta las siguientes líneas:

# def handle_command(command: str) -> str:
#     """Procesa un comando y retorna la respuesta."""
#     match command.lower():
#         case "start":
#             return "Iniciando sistema..."
#         case "stop":
#             return "Deteniendo sistema..."
#         case "pause":
#             return "Sistema pausado"
#         case "help":
#             return "Comandos: start, stop, pause, help"
#         case _:  # Wildcard - coincide con cualquier cosa
#             return f"Comando desconocido: {command}"
#
# # Tests
# print(handle_command("start"))
# print(handle_command("STOP"))
# print(handle_command("help"))
# print(handle_command("exit"))

print()

# ============================================
# PASO 2: Match con Números
# ============================================
print("=== MATCH CON NÚMEROS ===")

# Match funciona igual con valores numéricos
# Descomenta las siguientes líneas:

# def http_status(code: int) -> str:
#     """Retorna el mensaje para un código HTTP."""
#     match code:
#         case 200:
#             return "✅ OK"
#         case 201:
#             return "✅ Created"
#         case 400:
#             return "⚠️ Bad Request"
#         case 404:
#             return "⚠️ Not Found"
#         case 500:
#             return "❌ Internal Server Error"
#         case _:
#             return f"❓ Unknown: {code}"
#
# # Tests
# print(f"HTTP 200: {http_status(200)}")
# print(f"HTTP 404: {http_status(404)}")
# print(f"HTTP 418: {http_status(418)}")

print()

# ============================================
# PASO 3: Patrones Combinados con OR (|)
# ============================================
print("=== PATRONES COMBINADOS ===")

# Usar | para combinar múltiples patrones en un case
# Descomenta las siguientes líneas:

# def get_day_type(day: str) -> str:
#     """Clasifica el día de la semana."""
#     match day.lower():
#         case "monday":
#             return "😩 Inicio de semana"
#         case "tuesday" | "wednesday" | "thursday":
#             return "📅 Entre semana"
#         case "friday":
#             return "🎉 ¡Viernes!"
#         case "saturday" | "sunday":
#             return "🏖️ Fin de semana"
#         case _:
#             return "❓ Día no válido"
#
# # Tests
# print(f"Monday: {get_day_type('Monday')}")
# print(f"Wednesday: {get_day_type('Wednesday')}")
# print(f"Friday: {get_day_type('Friday')}")
# print(f"Sunday: {get_day_type('Sunday')}")
# print(f"Funday: {get_day_type('Funday')}")

# OR con números
# def http_category(code: int) -> str:
#     """Categoriza códigos HTTP."""
#     match code:
#         case 200 | 201 | 204:
#             return "✅ Success"
#         case 400 | 401 | 403 | 404:
#             return "⚠️ Client Error"
#         case 500 | 502 | 503:
#             return "❌ Server Error"
#         case _:
#             return "❓ Unknown"
#
# print(f"\nHTTP 200: {http_category(200)}")
# print(f"HTTP 404: {http_category(404)}")
# print(f"HTTP 500: {http_category(500)}")

print()

# ============================================
# PASO 4: Captura de Valores
# ============================================
print("=== CAPTURA DE VALORES ===")

# Puedes capturar el valor en una variable
# Descomenta las siguientes líneas:

# def describe_number(n: int) -> str:
#     """Describe un número capturando su valor."""
#     match n:
#         case 0:
#             return "Es cero"
#         case 1:
#             return "Es uno"
#         case 13:
#             return "¡Número de la suerte!"
#         case other:  # 'other' captura cualquier otro valor
#             return f"Es el número {other}"
#
# # Tests
# print(describe_number(0))
# print(describe_number(1))
# print(describe_number(13))
# print(describe_number(42))
# print(describe_number(100))

print()

# ============================================
# PASO 5: Guardas (Guards) con if
# ============================================
print("=== PATRONES CON GUARDAS ===")

# Las guardas añaden condiciones con if
# Descomenta las siguientes líneas:

# def classify_number(n: int) -> str:
#     """Clasifica un número usando guardas."""
#     match n:
#         case 0:
#             return "Cero"
#         case n if n < 0:
#             return f"Negativo: {n}"
#         case n if n > 100:
#             return f"Número grande: {n}"
#         case n if n % 2 == 0:
#             return f"Par: {n}"
#         case _:
#             return f"Impar: {n}"
#
# # Tests
# print(classify_number(0))
# print(classify_number(-5))
# print(classify_number(150))
# print(classify_number(42))
# print(classify_number(7))

print()

# ============================================
# PASO 6: Clasificador de Edad
# ============================================
print("=== CLASIFICADOR DE EDAD ===")

# Ejemplo práctico con guardas
# Descomenta las siguientes líneas:

# def classify_age(age: int) -> str:
#     """Clasifica una persona por su edad."""
#     match age:
#         case n if n < 0:
#             return "❌ Edad inválida"
#         case n if n < 3:
#             return "👶 Bebé"
#         case n if n < 13:
#             return "🧒 Niño"
#         case n if n < 18:
#             return "🧑 Adolescente"
#         case n if n < 65:
#             return "👨 Adulto"
#         case _:
#             return "👴 Adulto mayor"
#
# # Tests
# ages = [-1, 1, 8, 15, 30, 70]
# for age in ages:
#     print(f"Edad {age}: {classify_age(age)}")

print()

# ============================================
# PASO 7: Clasificador de Temperatura
# ============================================
print("=== CLASIFICADOR DE TEMPERATURA ===")

# Otro ejemplo práctico con guardas
# Descomenta las siguientes líneas:

# def classify_temperature(temp: float) -> str:
#     """Clasifica la temperatura en categorías."""
#     match temp:
#         case t if t < 0:
#             return "🥶 Congelante"
#         case t if t < 10:
#             return "❄️ Muy frío"
#         case t if t < 20:
#             return "🌤️ Fresco"
#         case t if t < 30:
#             return "☀️ Agradable"
#         case t if t < 40:
#             return "🔥 Caluroso"
#         case _:
#             return "🌡️ Extremo"
#
# # Tests
# temps = [-10, 5, 15, 25, 35, 45]
# for t in temps:
#     print(f"{t}°C: {classify_temperature(t)}")

print()

# ============================================
# PASO 8: Menú de Opciones
# ============================================
print("=== MENÚ DE OPCIONES ===")

# Ejemplo de menú interactivo
# Descomenta las siguientes líneas:

# def process_menu(option: str) -> str:
#     """Procesa la selección de un menú."""
#     match option.lower():
#         case "1" | "new" | "n":
#             return "📄 Creando nuevo archivo..."
#         case "2" | "open" | "o":
#             return "📂 Abriendo archivo..."
#         case "3" | "save" | "s":
#             return "💾 Guardando archivo..."
#         case "4" | "quit" | "q" | "exit":
#             return "👋 Saliendo del programa..."
#         case "help" | "h" | "?":
#             return "❓ Opciones: 1-new, 2-open, 3-save, 4-quit, help"
#         case _:
#             return "⚠️ Opción no válida. Escribe 'help'"
#
# # Tests
# options = ["1", "new", "save", "q", "help", "xyz"]
# for opt in options:
#     print(f"'{opt}': {process_menu(opt)}")

print()

# ============================================
# DESAFÍO EXTRA
# ============================================
print("=== DESAFÍO EXTRA ===")

# Implementa un conversor de calificaciones
# Descomenta y completa:

# def grade_to_description(score: int) -> str:
#     """
#     Convierte un puntaje numérico a descripción.
#
#     - score < 0 o > 100 -> "Puntaje inválido"
#     - score >= 90 -> "A - Excelente"
#     - score >= 80 -> "B - Muy bien"
#     - score >= 70 -> "C - Bien"
#     - score >= 60 -> "D - Suficiente"
#     - score < 60 -> "F - Reprobado"
#     """
#     match score:
#         case s if s < 0 or s > 100:
#             return "Puntaje inválido"
#         case s if s >= 90:
#             return "A - Excelente"
#         case s if s >= 80:
#             return "B - Muy bien"
#         case s if s >= 70:
#             return "C - Bien"
#         case s if s >= 60:
#             return "D - Suficiente"
#         case _:
#             return "F - Reprobado"
#
# # Tests
# scores = [-5, 95, 85, 75, 65, 45, 110]
# for score in scores:
#     print(f"Puntaje {score}: {grade_to_description(score)}")

print()

# ============================================
# DESAFÍO AVANZADO: Calculadora Simple
# ============================================
print("=== DESAFÍO AVANZADO ===")

# Implementa una calculadora que procese operaciones como strings
# Descomenta y completa:

# def simple_calc(operation: str, a: float, b: float) -> str:
#     """
#     Calculadora simple.
#     operation: "add", "sub", "mul", "div"
#     """
#     match operation.lower():
#         case "add" | "suma" | "+":
#             result = a + b
#             return f"{a} + {b} = {result}"
#         case "sub" | "resta" | "-":
#             result = a - b
#             return f"{a} - {b} = {result}"
#         case "mul" | "mult" | "*":
#             result = a * b
#             return f"{a} × {b} = {result}"
#         case "div" | "/" if b != 0:
#             result = a / b
#             return f"{a} ÷ {b} = {result}"
#         case "div" | "/" if b == 0:
#             return "Error: división por cero"
#         case _:
#             return f"Operación desconocida: {operation}"
#
# # Tests
# print(simple_calc("add", 5, 3))
# print(simple_calc("sub", 10, 4))
# print(simple_calc("mul", 6, 7))
# print(simple_calc("div", 15, 3))
# print(simple_calc("div", 10, 0))
# print(simple_calc("suma", 2, 2))
# print(simple_calc("pow", 2, 8))

print("\n✅ Ejercicio completado!")
