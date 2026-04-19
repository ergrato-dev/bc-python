"""
Ejercicio 01: Comprehensions Básicos
====================================
Practica list, dict y set comprehensions.

Instrucciones:
1. Lee cada sección
2. Descomenta el código indicado
3. Ejecuta para verificar resultados
"""

# ============================================
# PASO 1: List Comprehension Básico
# ============================================
print("=== PASO 1: List Comprehension Básico ===")

# Un list comprehension crea una lista aplicando una expresión
# a cada elemento de un iterable.

# Descomenta las siguientes líneas:
# squares = [x ** 2 for x in range(10)]
# print(f"Cuadrados: {squares}")

print()

# ============================================
# PASO 2: Transformación de Strings
# ============================================
print("=== PASO 2: Transformación de Strings ===")

# Puedes aplicar métodos a cada elemento.

languages = ["python", "javascript", "rust", "go"]

# Descomenta las siguientes líneas:
# upper_langs = [lang.upper() for lang in languages]
# print(f"Mayúsculas: {upper_langs}")
#
# lengths = [len(lang) for lang in languages]
# print(f"Longitudes: {lengths}")

print()

# ============================================
# PASO 3: Filtrado con if
# ============================================
print("=== PASO 3: Filtrado con if ===")

# El 'if' al FINAL filtra elementos (los excluye si no cumplen).
# Sintaxis: [expresion for x in iterable if condicion]

# Descomenta las siguientes líneas:
# evens = [n for n in range(20) if n % 2 == 0]
# print(f"Pares: {evens}")
#
# long_words = [lang for lang in languages if len(lang) > 4]
# print(f"Palabras largas: {long_words}")

print()

# ============================================
# PASO 4: Transformar y Filtrar
# ============================================
print("=== PASO 4: Transformar y Filtrar ===")

# Puedes combinar transformación Y filtro.
# Primero filtra, luego transforma.

# Descomenta las siguientes líneas:
# odd_squares = [n ** 2 for n in range(10) if n % 2 != 0]
# print(f"Cuadrados de impares: {odd_squares}")

print()

# ============================================
# PASO 5: Expresión Condicional (if-else)
# ============================================
print("=== PASO 5: Expresión Condicional (if-else) ===")

# if-else al INICIO transforma TODOS los elementos.
# Sintaxis: [valor_true if cond else valor_false for x in iterable]
# ¡Nota la diferencia con el filtro!

numbers = [1, 2, 3, 4, 5]
scores = [85, 42, 91, 55, 78, 38]

# Descomenta las siguientes líneas:
# labels = ["par" if n % 2 == 0 else "impar" for n in numbers]
# print(f"Etiquetas: {labels}")
#
# pass_fail = ["PASS" if s >= 60 else "FAIL" for s in scores]
# print(f"Aprobados: {pass_fail}")

print()

# ============================================
# PASO 6: Dict Comprehension
# ============================================
print("=== PASO 6: Dict Comprehension ===")

# Dict comprehension crea diccionarios con {clave: valor for ...}

words = ["python", "es", "genial"]

# Descomenta las siguientes líneas:
# squares_dict = {n: n ** 2 for n in range(1, 6)}
# print(f"Cuadrados dict: {squares_dict}")
#
# word_lengths = {word: len(word) for word in words}
# print(f"Longitud palabras: {word_lengths}")

print()

# ============================================
# PASO 7: Dict con Filtro
# ============================================
print("=== PASO 7: Dict con Filtro ===")

# También puedes filtrar en dict comprehensions.

grades = {"Ana": 85, "Bob": 42, "Carlos": 91, "Diana": 55, "Eva": 78}
original = {"a": 1, "b": 2, "c": 3}

# Descomenta las siguientes líneas:
# passing = {name: score for name, score in grades.items() if score >= 60}
# print(f"Aprobados: {passing}")
#
# # Invertir diccionario (intercambiar claves y valores)
# inverted = {v: k for k, v in original.items()}
# print(f"Invertido: {inverted}")

print()

# ============================================
# PASO 8: Set Comprehension
# ============================================
print("=== PASO 8: Set Comprehension ===")

# Set comprehension crea conjuntos (valores únicos).
# Usa llaves {} pero SIN clave:valor.

text = "hello"
sentence = "Python es un lenguaje increible"

# Descomenta las siguientes líneas:
# unique_letters = {char for char in text}
# print(f"Letras únicas: {unique_letters}")
#
# vowels = {char.lower() for char in sentence if char.lower() in "aeiou"}
# print(f"Vocales: {vowels}")

print()

# ============================================
# PASO 9: Comprehension Anidado
# ============================================
print("=== PASO 9: Comprehension Anidado ===")

# Puedes anidar bucles for en un comprehension.
# Se lee de izquierda a derecha (for externo primero).

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
letters = ["A", "B"]
numbers_list = [1, 2]

# Descomenta las siguientes líneas:
# # Aplanar matriz (convertir lista de listas en lista simple)
# flat = [num for row in matrix for num in row]
# print(f"Aplanado: {flat}")
#
# # Producto cartesiano
# combos = [(letter, num) for letter in letters for num in numbers_list]
# print(f"Combinaciones: {combos}")

print()

# ============================================
# PASO 10: Caso Práctico
# ============================================
print("=== PASO 10: Caso Práctico ===")

# Aplicar IVA a productos caros (precio > 500)

products = {
    "Laptop": 1000,
    "Mouse": 25,
    "Keyboard": 75,
    "Phone": 800,
    "Cable": 10
}
iva = 0.21

# Descomenta las siguientes líneas:
# # Filtrar productos caros y aplicar IVA
# expensive_with_tax = {
#     name: round(price * (1 + iva), 2)
#     for name, price in products.items()
#     if price > 500
# }
# print(f"Productos caros: {expensive_with_tax}")


# ============================================
# ¡FELICIDADES! 🎉
# ============================================
# Has completado el ejercicio de comprehensions.
# Ahora dominas:
# - List comprehensions con transformaciones y filtros
# - Expresiones condicionales (if-else)
# - Dict comprehensions
# - Set comprehensions
# - Comprehensions anidados
