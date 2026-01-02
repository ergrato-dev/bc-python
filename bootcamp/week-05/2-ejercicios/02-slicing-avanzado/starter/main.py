"""
Ejercicio 02: Slicing Avanzado
==============================

Aprende a usar slicing para extraer y manipular secuencias en Python.

Instrucciones:
1. Lee cada sección
2. Descomenta el código
3. Ejecuta y observa los resultados
"""


# ============================================
# PASO 1: Slicing Básico [start:stop]
# ============================================
print("--- Paso 1: Slicing Básico ---")

# La sintaxis básica es: sequence[start:stop]
# start está INCLUIDO, stop está EXCLUIDO

# Descomenta las siguientes líneas:
# numbers: list[int] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# print(f"Lista original: {numbers}")
# print(f"Índices:         0  1  2  3  4  5  6  7  8  9")
#
# # Extraer elementos del índice 2 al 5 (excluido)
# slice1 = numbers[2:5]
# print(f"\nnumbers[2:5] = {slice1}")  # [2, 3, 4]
#
# # Extraer del índice 0 al 3
# slice2 = numbers[0:3]
# print(f"numbers[0:3] = {slice2}")  # [0, 1, 2]
#
# # El índice stop NO está incluido
# slice3 = numbers[5:8]
# print(f"numbers[5:8] = {slice3}")  # [5, 6, 7] (no incluye 8)

print()


# ============================================
# PASO 2: Omitir start o stop
# ============================================
print("--- Paso 2: Omitir start o stop ---")

# Si omites start, comienza desde el inicio (índice 0)
# Si omites stop, continúa hasta el final

# Descomenta las siguientes líneas:
# letters: list[str] = ["a", "b", "c", "d", "e", "f"]
# print(f"Lista: {letters}")
#
# # Omitir start: desde el inicio
# first_three = letters[:3]
# print(f"\nletters[:3] = {first_three}")  # ['a', 'b', 'c']
#
# # Omitir stop: hasta el final
# from_index_3 = letters[3:]
# print(f"letters[3:] = {from_index_3}")  # ['d', 'e', 'f']
#
# # Omitir ambos: copia completa
# copy_all = letters[:]
# print(f"letters[:] = {copy_all}")  # ['a', 'b', 'c', 'd', 'e', 'f']
#
# # Es equivalente a:
# print(f"letters[0:len(letters)] = {letters[0:len(letters)]}")

print()


# ============================================
# PASO 3: Índices Negativos
# ============================================
print("--- Paso 3: Índices Negativos ---")

# Los índices negativos cuentan desde el final
# -1 es el último, -2 el penúltimo, etc.

# Descomenta las siguientes líneas:
# data: list[int] = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# print(f"Lista: {data}")
# print("Índices positivos:  0   1   2   3   4   5   6   7   8   9")
# print("Índices negativos: -10 -9  -8  -7  -6  -5  -4  -3  -2  -1")
#
# # Últimos 3 elementos
# last_three = data[-3:]
# print(f"\ndata[-3:] = {last_three}")  # [80, 90, 100]
#
# # Todo excepto los últimos 2
# without_last_two = data[:-2]
# print(f"data[:-2] = {without_last_two}")  # [10, 20, 30, 40, 50, 60, 70, 80]
#
# # Desde -6 hasta -2 (excluido)
# middle = data[-6:-2]
# print(f"data[-6:-2] = {middle}")  # [50, 60, 70, 80]
#
# # Combinando positivos y negativos
# combo = data[2:-2]
# print(f"data[2:-2] = {combo}")  # [30, 40, 50, 60, 70, 80]
#
# # Sin primer ni último elemento
# inner = data[1:-1]
# print(f"data[1:-1] = {inner}")  # [20, 30, 40, 50, 60, 70, 80, 90]

print()


# ============================================
# PASO 4: Slicing con Step
# ============================================
print("--- Paso 4: Slicing con Step ---")

# El tercer parámetro es el paso (step)
# sequence[start:stop:step]

# Descomenta las siguientes líneas:
# nums: list[int] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# print(f"Lista: {nums}")
#
# # Cada 2 elementos (step=2)
# every_two = nums[::2]
# print(f"\nnums[::2] = {every_two}")  # [0, 2, 4, 6, 8]
#
# # Cada 3 elementos
# every_three = nums[::3]
# print(f"nums[::3] = {every_three}")  # [0, 3, 6, 9]
#
# # Empezando desde índice 1, cada 2
# odd_indices = nums[1::2]
# print(f"nums[1::2] = {odd_indices}")  # [1, 3, 5, 7, 9]
#
# # Con rango específico y step
# range_step = nums[1:8:2]
# print(f"nums[1:8:2] = {range_step}")  # [1, 3, 5, 7]
#
# # Primeros 6 elementos, cada 2
# first_six_step = nums[:6:2]
# print(f"nums[:6:2] = {first_six_step}")  # [0, 2, 4]

print()


# ============================================
# PASO 5: Step Negativo (Invertir)
# ============================================
print("--- Paso 5: Step Negativo ---")

# Con step negativo, se recorre de derecha a izquierda
# Ideal para invertir secuencias

# Descomenta las siguientes líneas:
# values: list[int] = [1, 2, 3, 4, 5]
# print(f"Lista: {values}")
#
# # Invertir completamente
# reversed_list = values[::-1]
# print(f"\nvalues[::-1] = {reversed_list}")  # [5, 4, 3, 2, 1]
#
# # Cada 2 elementos, invertido
# reverse_step = values[::-2]
# print(f"values[::-2] = {reverse_step}")  # [5, 3, 1]
#
# # Rango específico invertido
# # ⚠️ Con step negativo, start debe ser mayor que stop
# partial_reverse = values[4:1:-1]
# print(f"values[4:1:-1] = {partial_reverse}")  # [5, 4, 3]
#
# # Equivalente a values[4], values[3], values[2]
# # Se detiene ANTES de llegar al índice 1
#
# # ⚠️ Esto retorna lista vacía (no hay camino de 1 a 4 con step -1)
# empty = values[1:4:-1]
# print(f"values[1:4:-1] = {empty}")  # []

print()


# ============================================
# PASO 6: Slicing con Strings
# ============================================
print("--- Paso 6: Slicing con Strings ---")

# Slicing funciona igual con strings

# Descomenta las siguientes líneas:
# text: str = "Python Programming"
# print(f"String: '{text}'")
#
# # Primeros 6 caracteres
# first_word = text[:6]
# print(f"\ntext[:6] = '{first_word}'")  # 'Python'
#
# # Desde índice 7
# second_word = text[7:]
# print(f"text[7:] = '{second_word}'")  # 'Programming'
#
# # Invertir string
# reversed_text = text[::-1]
# print(f"text[::-1] = '{reversed_text}'")
#
# # Verificar palíndromo
# word = "radar"
# is_palindrome = word == word[::-1]
# print(f"\n'{word}' es palíndromo: {is_palindrome}")  # True
#
# word2 = "python"
# is_palindrome2 = word2 == word2[::-1]
# print(f"'{word2}' es palíndromo: {is_palindrome2}")  # False
#
# # ⚠️ Strings son inmutables, slicing retorna nuevo string
# # text[0] = "J"  # Error! No se puede modificar

print()


# ============================================
# PASO 7: Modificar Listas con Slicing
# ============================================
print("--- Paso 7: Modificar con Slicing ---")

# A diferencia de strings, las listas SÍ pueden modificarse con slicing

# Descomenta las siguientes líneas:
# numbers: list[int] = [0, 1, 2, 3, 4, 5]
# print(f"Original: {numbers}")
#
# # Reemplazar un rango
# numbers[1:4] = [10, 20, 30]
# print(f"numbers[1:4] = [10, 20, 30]: {numbers}")  # [0, 10, 20, 30, 4, 5]
#
# # Reemplazar con diferente cantidad de elementos
# numbers = [0, 1, 2, 3, 4, 5]
# numbers[1:4] = [99]  # 3 elementos reemplazados por 1
# print(f"numbers[1:4] = [99]: {numbers}")  # [0, 99, 4, 5]
#
# # Insertar elementos (slice vacío)
# numbers = [0, 1, 2, 3, 4, 5]
# numbers[2:2] = [100, 200, 300]  # Insertar en posición 2
# print(f"numbers[2:2] = [100,200,300]: {numbers}")
#
# # Eliminar elementos (asignar lista vacía)
# numbers = [0, 1, 2, 3, 4, 5]
# numbers[1:4] = []
# print(f"numbers[1:4] = []: {numbers}")  # [0, 4, 5]
#
# # Reemplazar con step (debe coincidir cantidad)
# numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# numbers[::2] = [10, 20, 30, 40, 50]  # 5 posiciones, 5 valores
# print(f"numbers[::2] = [10,20,30,40,50]: {numbers}")

print()


# ============================================
# PASO 8: Copiar con Slicing
# ============================================
print("--- Paso 8: Copiar con Slicing ---")

# Slicing crea una NUEVA secuencia, útil para copiar

# Descomenta las siguientes líneas:
# original: list[int] = [1, 2, 3, 4, 5]
#
# # ❌ INCORRECTO: Solo crea otra referencia
# not_a_copy = original
# not_a_copy[0] = 99
# print(f"Asignación directa:")
# print(f"  Original: {original}")  # [99, 2, 3, 4, 5] ¡También cambió!
# print(f"  'Copia': {not_a_copy}")
#
# # Restaurar
# original = [1, 2, 3, 4, 5]
#
# # ✅ CORRECTO: Slicing crea una nueva lista
# actual_copy = original[:]
# actual_copy[0] = 99
# print(f"\nSlicing [:]:")
# print(f"  Original: {original}")  # [1, 2, 3, 4, 5] Sin cambios
# print(f"  Copia: {actual_copy}")
#
# # ⚠️ Cuidado: Es copia superficial (como list.copy())
# nested: list[list[int]] = [[1, 2], [3, 4]]
# shallow = nested[:]
# shallow[0][0] = 99  # Modifica objeto anidado
# print(f"\nCopia superficial con anidados:")
# print(f"  Original: {nested}")  # [[99, 2], [3, 4]] ¡Afectado!
# print(f"  Copia: {shallow}")

print()


# ============================================
# PASO 9: Casos de Uso Comunes
# ============================================
print("--- Paso 9: Casos de Uso Comunes ---")

# Patrones útiles que usarás frecuentemente

# Descomenta las siguientes líneas:
# data: list[int] = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# print(f"Lista: {data}")
#
# # 1. Obtener primeros N elementos
# n = 3
# first_n = data[:n]
# print(f"\nPrimeros {n}: {first_n}")
#
# # 2. Obtener últimos N elementos
# last_n = data[-n:]
# print(f"Últimos {n}: {last_n}")
#
# # 3. Dividir en mitades
# mid = len(data) // 2
# first_half = data[:mid]
# second_half = data[mid:]
# print(f"\nPrimera mitad: {first_half}")
# print(f"Segunda mitad: {second_half}")
#
# # 4. Elementos en índices pares/impares
# even_indices = data[::2]   # 0, 2, 4, 6, 8
# odd_indices = data[1::2]   # 1, 3, 5, 7, 9
# print(f"\nÍndices pares: {even_indices}")
# print(f"Índices impares: {odd_indices}")
#
# # 5. Rotar lista
# def rotate_left(lst: list, n: int) -> list:
#     """Rota n posiciones a la izquierda."""
#     n = n % len(lst)
#     return lst[n:] + lst[:n]
#
# def rotate_right(lst: list, n: int) -> list:
#     """Rota n posiciones a la derecha."""
#     n = n % len(lst)
#     return lst[-n:] + lst[:-n]
#
# sample = [1, 2, 3, 4, 5]
# print(f"\nOriginal: {sample}")
# print(f"Rotado izquierda 2: {rotate_left(sample, 2)}")
# print(f"Rotado derecha 2: {rotate_right(sample, 2)}")

print()


# ============================================
# PASO 10: Ejercicio Integrador
# ============================================
print("--- Paso 10: Ejercicio Integrador ---")

# Manipulación de datos de ventas semanales

# Descomenta las siguientes líneas:
# def analyze_sales() -> None:
#     """Analiza datos de ventas usando slicing."""
#
#     # Ventas diarias de 2 semanas (14 días)
#     sales: list[float] = [
#         120.5, 95.0, 200.3, 150.0, 180.5, 220.0, 175.5,  # Semana 1
#         110.0, 130.5, 190.0, 160.5, 200.0, 250.0, 195.0  # Semana 2
#     ]
#
#     print(f"Ventas de 14 días: {sales}")
#
#     # 1. Separar por semanas
#     week1 = sales[:7]
#     week2 = sales[7:]
#     print(f"\nSemana 1: {week1}")
#     print(f"Semana 2: {week2}")
#
#     # 2. Promedios semanales
#     avg_week1 = sum(week1) / len(week1)
#     avg_week2 = sum(week2) / len(week2)
#     print(f"\nPromedio Semana 1: ${avg_week1:.2f}")
#     print(f"Promedio Semana 2: ${avg_week2:.2f}")
#
#     # 3. Ventas de fines de semana (días 5,6 y 12,13 → índices 5,6,12,13)
#     # En lugar de índices específicos, usamos días 6,7 de cada semana
#     weekend1 = week1[-2:]  # Últimos 2 días de semana 1
#     weekend2 = week2[-2:]  # Últimos 2 días de semana 2
#     print(f"\nFin de semana 1: {weekend1}")
#     print(f"Fin de semana 2: {weekend2}")
#
#     # 4. Mejores 5 días (ordenar y tomar últimos 5)
#     sorted_sales = sorted(sales)
#     best_5 = sorted_sales[-5:]
#     print(f"\nMejores 5 ventas: {best_5}")
#
#     # 5. Días alternos (para muestreo)
#     alternate_days = sales[::2]
#     print(f"\nDías alternos: {alternate_days}")
#
#     # 6. Invertir para ver más recientes primero
#     recent_first = sales[::-1]
#     print(f"\nMás recientes primero: {recent_first[:5]}...")
#
#     # 7. Comparar primeros vs últimos 3 días
#     first_3 = sales[:3]
#     last_3 = sales[-3:]
#     trend = "📈 Mejorando" if sum(last_3) > sum(first_3) else "📉 Empeorando"
#     print(f"\nPrimeros 3: {first_3} = ${sum(first_3):.2f}")
#     print(f"Últimos 3: {last_3} = ${sum(last_3):.2f}")
#     print(f"Tendencia: {trend}")
#
# analyze_sales()

print()
print("=" * 50)
print("🎉 ¡Ejercicio completado!")
print("=" * 50)
