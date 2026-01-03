"""
Ejercicio 02: Generadores de Datos
==================================

Aprende a crear generadores eficientes para procesamiento de datos.

Instrucciones:
1. Lee cada sección
2. Descomenta el código
3. Ejecuta para verificar
"""

from typing import Iterator, Generator, Any
import sys


# ============================================
# PASO 1: Generador Básico con yield
# ============================================
print("=== PASO 1: Countdown ===")

# Un generador usa 'yield' en lugar de 'return'.
# Cada yield pausa la función y produce un valor.
# La función se reanuda en la siguiente llamada a next().

# Descomenta las siguientes líneas:

# def countdown(n: int) -> Iterator[int]:
#     """Genera cuenta regresiva desde n hasta 1."""
#     print(f"Starting countdown from {n}")
#     while n > 0:
#         yield n  # Produce valor y pausa
#         n -= 1
#     print("Countdown finished!")
#
#
# # Usar el generador en un for loop
# for num in countdown(5):
#     print(num, end=" ")
# print()
#
# # También podemos usar next() manualmente
# gen = countdown(3)
# print(f"Manual: {next(gen)}, {next(gen)}, {next(gen)}")

print()


# ============================================
# PASO 2: Generador de Fibonacci
# ============================================
print("=== PASO 2: Fibonacci ===")

# Los generadores pueden ser infinitos.
# Producen valores bajo demanda sin almacenar todo en memoria.

# Descomenta las siguientes líneas:

# def fibonacci() -> Iterator[int]:
#     """Genera secuencia infinita de Fibonacci."""
#     a, b = 0, 1
#     while True:  # Infinito
#         yield a
#         a, b = b, a + b
#
#
# # Tomar solo los primeros 10 números
# fib = fibonacci()
# first_10 = [next(fib) for _ in range(10)]
# print(f"First 10 Fibonacci: {first_10}")
#
# # Encontrar primer Fibonacci mayor a 1000
# fib = fibonacci()
# for num in fib:
#     if num > 1000:
#         print(f"First Fibonacci > 1000: {num}")
#         break

print()


# ============================================
# PASO 3: Expresiones Generadoras
# ============================================
print("=== PASO 3: Generator Expression ===")

# Las expresiones generadoras son como list comprehensions
# pero con paréntesis () en lugar de corchetes [].
# Producen valores bajo demanda, ahorrando memoria.

# Descomenta las siguientes líneas:

# # Comparar uso de memoria
# n = 1_000_000
#
# # List comprehension - crea lista completa en memoria
# squares_list = [x**2 for x in range(n)]
# list_size = sys.getsizeof(squares_list)
# print(f"List size: {list_size:,} bytes (~{list_size // 1024 // 1024} MB)")
#
# # Generator expression - casi no usa memoria
# squares_gen = (x**2 for x in range(n))
# gen_size = sys.getsizeof(squares_gen)
# print(f"Generator size: {gen_size} bytes")
#
# # Ambos funcionan igual en for loops
# # Pero el generador es más eficiente para datos grandes
#
# # Usar generador con funciones como sum(), max(), etc.
# small_gen = (x**2 for x in range(100))
# total = sum(small_gen)
# print(f"Sum of squares 0-99: {total}")
#
# # Generadores se agotan después de usarse
# gen = (x for x in range(3))
# print(f"First pass: {list(gen)}")   # [0, 1, 2]
# print(f"Second pass: {list(gen)}")  # [] - ya se agotó

print()


# ============================================
# PASO 4: yield from
# ============================================
print("=== PASO 4: Yield From ===")

# 'yield from' delega a otro iterador.
# Es más limpio que un for loop con yield.

# Descomenta las siguientes líneas:

# def flatten(nested: list) -> Iterator:
#     """Aplana lista anidada de cualquier profundidad."""
#     for item in nested:
#         if isinstance(item, list):
#             yield from flatten(item)  # Delega recursivamente
#         else:
#             yield item
#
#
# nested = [1, [2, 3, [4, 5]], 6, [7, [8, [9]]]]
# flat = list(flatten(nested))
# print(f"Nested: {nested}")
# print(f"Flat: {flat}")
#
#
# # Otro ejemplo: encadenar iterables
# def chain(*iterables) -> Iterator:
#     """Encadena múltiples iterables."""
#     for iterable in iterables:
#         yield from iterable
#
#
# result = list(chain([1, 2], "ab", (3, 4)))
# print(f"Chained: {result}")  # [1, 2, 'a', 'b', 3, 4]

print()


# ============================================
# PASO 5: Pipeline de Generadores
# ============================================
print("=== PASO 5: Pipeline ===")

# Los generadores se pueden encadenar para crear pipelines
# de procesamiento eficientes. Cada paso procesa un elemento
# a la vez, sin cargar todo en memoria.

# Descomenta las siguientes líneas:

# def generate_numbers(n: int) -> Iterator[int]:
#     """Genera números del 0 al n-1."""
#     for i in range(n):
#         yield i
#
#
# def filter_even(numbers: Iterator[int]) -> Iterator[int]:
#     """Filtra solo números pares."""
#     for n in numbers:
#         if n % 2 == 0:
#             yield n
#
#
# def square(numbers: Iterator[int]) -> Iterator[int]:
#     """Eleva al cuadrado cada número."""
#     for n in numbers:
#         yield n ** 2
#
#
# def take(n: int, iterable: Iterator) -> Iterator:
#     """Toma los primeros n elementos."""
#     for i, item in enumerate(iterable):
#         if i >= n:
#             break
#         yield item
#
#
# # Pipeline: genera -> filtra -> transforma -> limita
# pipeline = take(
#     5,
#     square(
#         filter_even(
#             generate_numbers(100)
#         )
#     )
# )
#
# # Solo procesa lo necesario (lazy evaluation)
# result = list(pipeline)
# print(f"Pipeline result: {result}")  # [0, 4, 16, 36, 64]
#
# # Versión más legible con variables
# numbers = generate_numbers(1000)
# evens = filter_even(numbers)
# squared = square(evens)
# first_10 = take(10, squared)
# print(f"First 10 even squares: {list(first_10)}")

print()


# ============================================
# PASO 6: Generador con send()
# ============================================
print("=== PASO 6: Send ===")

# Los generadores pueden recibir valores con send().
# El valor enviado se asigna al resultado de yield.

# Descomenta las siguientes líneas:

# def accumulator() -> Generator[int, int, None]:
#     """
#     Acumulador que recibe valores con send().
#
#     Generator[YieldType, SendType, ReturnType]
#     """
#     total = 0
#     while True:
#         # yield produce total y recibe nuevo valor
#         received = yield total
#         if received is not None:
#             total += received
#
#
# # Usar el acumulador
# acc = accumulator()
#
# # Inicializar (primer next() es obligatorio)
# print(f"Initial: {next(acc)}")
#
# # Enviar valores
# print(f"After send(10): {acc.send(10)}")
# print(f"After send(5): {acc.send(5)}")
# print(f"After send(3): {acc.send(3)}")
#
#
# # Ejemplo práctico: running average
# def running_average() -> Generator[float, float, None]:
#     """Calcula promedio acumulativo."""
#     total = 0.0
#     count = 0
#     average = 0.0
#
#     while True:
#         value = yield average
#         if value is not None:
#             total += value
#             count += 1
#             average = total / count
#
#
# avg = running_average()
# next(avg)  # Inicializar
# print(f"\nRunning average:")
# for val in [10, 20, 30, 40, 50]:
#     result = avg.send(val)
#     print(f"  Added {val}, average = {result}")

print()


# ============================================
# RESUMEN
# ============================================
print("=" * 50)
print("RESUMEN DE GENERADORES")
print("=" * 50)
print("""
✅ yield           - Produce valor y pausa
✅ yield from      - Delega a otro iterador
✅ (x for x in ...) - Expresión generadora
✅ next(gen)       - Obtiene siguiente valor
✅ gen.send(val)   - Envía valor al generador

Ventajas:
- Memoria eficiente (lazy evaluation)
- Ideal para datos grandes
- Pipelines de procesamiento
- Secuencias infinitas
""")
