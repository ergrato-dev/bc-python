"""
Ejercicio 01: Bucle For Básico
==============================
Aprende la sintaxis del bucle for, range() y enumerate().

Instrucciones:
- Lee cada sección y descomenta el código correspondiente
- Ejecuta el archivo después de cada paso para ver los resultados
- Asegúrate de entender cada concepto antes de continuar
"""

# ============================================
# PASO 1: Iteración sobre string
# ============================================
print("--- Paso 1: Iteración sobre string ---")

# El bucle for recorre cada carácter del string
# Descomenta las siguientes líneas:

# word: str = "Python"
# for char in word:
#     print(char)
# print()  # Línea en blanco


# ============================================
# PASO 2: range() básico
# ============================================
print("--- Paso 2: range() básico ---")

# range(n) genera números del 0 al n-1
# Descomenta las siguientes líneas:

# for i in range(5):
#     print(f"Iteración {i}")
# print()


# ============================================
# PASO 3: range() con inicio y fin
# ============================================
print("--- Paso 3: range() con inicio y fin ---")

# range(start, stop) genera desde start hasta stop-1
# Descomenta las siguientes líneas:

# print("Números del 1 al 5:")
# for i in range(1, 6):
#     print(i, end=" ")
# print("\n")  # Nueva línea


# ============================================
# PASO 4: range() con paso
# ============================================
print("--- Paso 4: range() con paso ---")

# range(start, stop, step) permite definir el incremento
# Descomenta las siguientes líneas:

# print("Números pares del 0 al 10:")
# for i in range(0, 11, 2):
#     print(i, end=" ")
# print()
#
# print("Cuenta regresiva:")
# for i in range(5, 0, -1):
#     print(i, end=" ")
# print("¡Despegue! 🚀\n")


# ============================================
# PASO 5: enumerate()
# ============================================
print("--- Paso 5: enumerate() ---")

# enumerate() retorna (índice, valor) para cada elemento
# Descomenta las siguientes líneas:

# fruits: list[str] = ["manzana", "banana", "cereza", "durazno"]
#
# print("Lista de frutas:")
# for index, fruit in enumerate(fruits):
#     print(f"  {index}: {fruit}")
# print()
#
# # enumerate con start personalizado
# print("Lista numerada (empezando en 1):")
# for num, fruit in enumerate(fruits, start=1):
#     print(f"  {num}. {fruit}")
# print()


# ============================================
# PASO 6: Patrón Contador
# ============================================
print("--- Paso 6: Contador de vocales ---")

# El patrón contador suma 1 cada vez que se cumple una condición
# Descomenta las siguientes líneas:

# def count_vowels(text: str) -> int:
#     """Cuenta las vocales en un texto."""
#     vowels: str = "aeiouAEIOU"
#     count: int = 0
#
#     for char in text:
#         if char in vowels:
#             count += 1
#
#     return count
#
# # Probar la función
# print(f"Vocales en 'Python': {count_vowels('Python')}")
# print(f"Vocales en 'Programación': {count_vowels('Programación')}")
# print(f"Vocales en 'AEIOU': {count_vowels('AEIOU')}")
# print()


# ============================================
# PASO 7: Patrón Acumulador
# ============================================
print("--- Paso 7: Suma de dígitos ---")

# El patrón acumulador suma valores en cada iteración
# Descomenta las siguientes líneas:

# def sum_digits(number: int) -> int:
#     """Suma los dígitos de un número."""
#     total: int = 0
#
#     for digit in str(number):
#         total += int(digit)
#
#     return total
#
# # Probar la función
# print(f"Suma de dígitos de 12345: {sum_digits(12345)}")  # 1+2+3+4+5 = 15
# print(f"Suma de dígitos de 999: {sum_digits(999)}")      # 9+9+9 = 27
# print(f"Suma de dígitos de 100: {sum_digits(100)}")      # 1+0+0 = 1
# print()


# ============================================
# PASO 8: Construir strings
# ============================================
print("--- Paso 8: Invertir string ---")

# Construir un nuevo string carácter por carácter
# Descomenta las siguientes líneas:

# def reverse_string(text: str) -> str:
#     """Invierte un string."""
#     result: str = ""
#
#     for char in text:
#         result = char + result  # Agregar al inicio
#
#     return result
#
# # Probar la función
# print(f"'Python' invertido: '{reverse_string('Python')}'")
# print(f"'Hola Mundo' invertido: '{reverse_string('Hola Mundo')}'")
# print(f"'12345' invertido: '{reverse_string('12345')}'")
# print()


# ============================================
# RESUMEN
# ============================================
print("=" * 50)
print("¡Ejercicio completado!")
print("=" * 50)
print("""
Conceptos aprendidos:
✅ for variable in secuencia: itera sobre elementos
✅ range(n): genera 0 hasta n-1
✅ range(start, stop): desde start hasta stop-1
✅ range(start, stop, step): con incremento personalizado
✅ enumerate(): retorna (índice, valor)
✅ Patrón contador: count += 1
✅ Patrón acumulador: total += valor
✅ Construcción de strings: result = char + result
""")
