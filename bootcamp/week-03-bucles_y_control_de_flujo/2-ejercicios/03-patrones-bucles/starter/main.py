"""
Ejercicio 03: Patrones de Bucles
================================
Aprende break, continue, else en bucles y patrones de iteración.

Instrucciones:
- Lee cada sección y descomenta el código correspondiente
- Ejecuta el archivo después de cada paso para ver los resultados
- Asegúrate de entender cada patrón antes de continuar
"""

# ============================================
# PASO 1: Break - Salir del bucle
# ============================================
print("--- Paso 1: Break ---")

# break termina el bucle inmediatamente
# Descomenta las siguientes líneas:

# print("Números hasta encontrar el 5:")
# for i in range(10):
#     if i == 5:
#         print(f"¡Encontrado {i}! Saliendo...")
#         break
#     print(i, end=" ")
# print("\nBucle terminado\n")
#
# # Break en búsqueda
# numbers: list[int] = [10, 20, 30, 40, 50]
# target: int = 30
#
# print(f"Buscando {target} en {numbers}:")
# for i, num in enumerate(numbers):
#     print(f"  Revisando índice {i}: {num}")
#     if num == target:
#         print(f"  ✅ Encontrado en índice {i}")
#         break
# print()


# ============================================
# PASO 2: Continue - Saltar iteración
# ============================================
print("--- Paso 2: Continue ---")

# continue salta el resto de la iteración actual
# Descomenta las siguientes líneas:

# print("Números del 0 al 9, saltando el 5:")
# for i in range(10):
#     if i == 5:
#         continue  # Salta el 5
#     print(i, end=" ")
# print("\n")
#
# # Continue para filtrar valores
# print("Solo números pares:")
# for i in range(10):
#     if i % 2 != 0:  # Si es impar
#         continue    # Salta
#     print(i, end=" ")
# print("\n")


# ============================================
# PASO 3: Else en bucles
# ============================================
print("--- Paso 3: Else en bucles ---")

# else se ejecuta si el bucle termina SIN break
# Descomenta las siguientes líneas:

# # Caso 1: Bucle completo (else SE ejecuta)
# print("Buscar 99 en [1, 2, 3, 4, 5]:")
# for num in [1, 2, 3, 4, 5]:
#     if num == 99:
#         print("Encontrado!")
#         break
# else:
#     print("  No encontrado (else ejecutado)")
# print()
#
# # Caso 2: Break ejecutado (else NO se ejecuta)
# print("Buscar 3 en [1, 2, 3, 4, 5]:")
# for num in [1, 2, 3, 4, 5]:
#     if num == 3:
#         print("  ✅ Encontrado! (break ejecutado)")
#         break
# else:
#     print("  No encontrado")
# print()


# ============================================
# PASO 4: Patrón Búsqueda
# ============================================
print("--- Paso 4: Búsqueda ---")

# Buscar el primer elemento que cumple una condición
# Descomenta las siguientes líneas:

# def find_first_negative(numbers: list[int]) -> int | None:
#     """Encuentra el primer número negativo."""
#     for num in numbers:
#         if num < 0:
#             return num  # Encontrado, retornar inmediatamente
#     return None  # No encontrado
#
# def find_index(items: list[str], target: str) -> int:
#     """Encuentra el índice de un elemento, -1 si no existe."""
#     for i, item in enumerate(items):
#         if item == target:
#             return i
#     return -1
#
# # Probar búsqueda
# nums1 = [5, 3, -2, 8, -1]
# nums2 = [1, 2, 3, 4, 5]
#
# print(f"Primer negativo en {nums1}: {find_first_negative(nums1)}")
# print(f"Primer negativo en {nums2}: {find_first_negative(nums2)}")
#
# colors = ["rojo", "verde", "azul"]
# print(f"Índice de 'verde' en {colors}: {find_index(colors, 'verde')}")
# print(f"Índice de 'negro' en {colors}: {find_index(colors, 'negro')}")
# print()


# ============================================
# PASO 5: Patrón Filtrado
# ============================================
print("--- Paso 5: Filtrado ---")

# Seleccionar elementos que cumplen una condición
# Descomenta las siguientes líneas:

# def filter_even(numbers: list[int]) -> list[int]:
#     """Filtra solo números pares."""
#     result: list[int] = []
#     for num in numbers:
#         if num % 2 == 0:
#             result.append(num)
#     return result
#
# def filter_long_words(words: list[str], min_length: int) -> list[str]:
#     """Filtra palabras con longitud mínima."""
#     result: list[str] = []
#     for word in words:
#         if len(word) >= min_length:
#             result.append(word)
#     return result
#
# # Probar filtrado
# nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# print(f"Pares en {nums}: {filter_even(nums)}")
#
# words = ["sol", "luna", "estrella", "mar", "cielo"]
# print(f"Palabras con 4+ letras: {filter_long_words(words, 4)}")
# print()


# ============================================
# PASO 6: Patrón Transformación
# ============================================
print("--- Paso 6: Transformación ---")

# Aplicar una operación a cada elemento
# Descomenta las siguientes líneas:

# def square_all(numbers: list[int]) -> list[int]:
#     """Eleva al cuadrado cada número."""
#     result: list[int] = []
#     for num in numbers:
#         result.append(num ** 2)
#     return result
#
# def to_uppercase(words: list[str]) -> list[str]:
#     """Convierte todas las palabras a mayúsculas."""
#     result: list[str] = []
#     for word in words:
#         result.append(word.upper())
#     return result
#
# def add_prefix(items: list[str], prefix: str) -> list[str]:
#     """Agrega un prefijo a cada elemento."""
#     result: list[str] = []
#     for item in items:
#         result.append(prefix + item)
#     return result
#
# # Probar transformación
# nums = [1, 2, 3, 4, 5]
# print(f"Cuadrados de {nums}: {square_all(nums)}")
#
# words = ["hola", "mundo", "python"]
# print(f"Mayúsculas: {to_uppercase(words)}")
# print(f"Con prefijo 'pre_': {add_prefix(words, 'pre_')}")
# print()


# ============================================
# PASO 7: Patrón Max/Min
# ============================================
print("--- Paso 7: Max/Min ---")

# Encontrar el valor extremo manualmente
# Descomenta las siguientes líneas:

# def find_max(numbers: list[int]) -> int | None:
#     """Encuentra el valor máximo."""
#     if not numbers:
#         return None
#
#     max_val: int = numbers[0]
#     for num in numbers[1:]:
#         if num > max_val:
#             max_val = num
#     return max_val
#
# def find_min(numbers: list[int]) -> int | None:
#     """Encuentra el valor mínimo."""
#     if not numbers:
#         return None
#
#     min_val: int = numbers[0]
#     for num in numbers[1:]:
#         if num < min_val:
#             min_val = num
#     return min_val
#
# def find_longest(words: list[str]) -> str | None:
#     """Encuentra la palabra más larga."""
#     if not words:
#         return None
#
#     longest: str = words[0]
#     for word in words[1:]:
#         if len(word) > len(longest):
#             longest = word
#     return longest
#
# # Probar max/min
# nums = [3, 7, 2, 9, 1, 5]
# print(f"Máximo en {nums}: {find_max(nums)}")
# print(f"Mínimo en {nums}: {find_min(nums)}")
#
# words = ["sol", "estrella", "luna", "universo"]
# print(f"Palabra más larga: '{find_longest(words)}'")
# print()


# ============================================
# PASO 8: Combinando patrones
# ============================================
print("--- Paso 8: Combinando patrones ---")

# Combinar múltiples patrones en una función
# Descomenta las siguientes líneas:

# def analyze_numbers(numbers: list[int]) -> dict:
#     """Analiza una lista de números con múltiples patrones."""
#     if not numbers:
#         return {"error": "Lista vacía"}
#
#     # Inicializar variables para cada patrón
#     total: int = 0                    # Acumulador
#     count_positive: int = 0           # Contador
#     count_negative: int = 0           # Contador
#     max_val: int = numbers[0]         # Max
#     min_val: int = numbers[0]         # Min
#     positives: list[int] = []         # Filtrado
#
#     for num in numbers:
#         # Acumulador
#         total += num
#
#         # Contadores
#         if num > 0:
#             count_positive += 1
#             positives.append(num)      # Filtrado
#         elif num < 0:
#             count_negative += 1
#
#         # Max/Min
#         if num > max_val:
#             max_val = num
#         if num < min_val:
#             min_val = num
#
#     return {
#         "sum": total,
#         "average": total / len(numbers),
#         "count_positive": count_positive,
#         "count_negative": count_negative,
#         "max": max_val,
#         "min": min_val,
#         "positives": positives,
#     }
#
# # Probar análisis combinado
# test_numbers = [5, -3, 8, -1, 0, 12, -7, 3]
# result = analyze_numbers(test_numbers)
#
# print(f"Análisis de {test_numbers}:")
# for key, value in result.items():
#     print(f"  {key}: {value}")
# print()


# ============================================
# RESUMEN
# ============================================
print("=" * 50)
print("¡Ejercicio completado!")
print("=" * 50)
print("""
Conceptos aprendidos:
✅ break: termina el bucle completamente
✅ continue: salta a la siguiente iteración
✅ else: se ejecuta si NO hubo break
✅ Patrón búsqueda: return cuando encuentre
✅ Patrón filtrado: append si cumple condición
✅ Patrón transformación: append valor modificado
✅ Patrón max/min: comparar y actualizar
✅ Combinar patrones para análisis complejo
""")
