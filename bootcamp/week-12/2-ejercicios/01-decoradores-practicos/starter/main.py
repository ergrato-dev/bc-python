"""
Ejercicio 01: Decoradores Prácticos
===================================

Aprende a crear decoradores útiles para aplicaciones reales.

Instrucciones:
1. Lee cada sección
2. Descomenta el código
3. Ejecuta para verificar
"""

import functools
import time
import random
from typing import Callable, ParamSpec, TypeVar, Any

P = ParamSpec("P")
R = TypeVar("R")


# ============================================
# PASO 1: Decorador Timer
# ============================================
print("=== PASO 1: Timer ===")

# El decorador timer mide el tiempo de ejecución de una función.
# Usa time.perf_counter() para mayor precisión.
# @functools.wraps preserva el nombre y docstring de la función original.

# Descomenta las siguientes líneas:

# def timer(func: Callable[P, R]) -> Callable[P, R]:
#     """Mide el tiempo de ejecución de una función."""
#     @functools.wraps(func)
#     def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
#         start = time.perf_counter()
#         result = func(*args, **kwargs)
#         elapsed = time.perf_counter() - start
#         print(f"⏱️ {func.__name__} executed in {elapsed:.4f}s")
#         return result
#     return wrapper
#
#
# @timer
# def slow_sum(n: int) -> int:
#     """Suma números del 1 al n."""
#     return sum(range(n + 1))
#
#
# result = slow_sum(1_000_000)
# print(f"Result: {result}")

print()


# ============================================
# PASO 2: Decorador Debug
# ============================================
print("=== PASO 2: Debug ===")

# El decorador debug muestra los argumentos y el resultado
# de cada llamada a la función. Útil para depuración.

# Descomenta las siguientes líneas:

# def debug(func: Callable[P, R]) -> Callable[P, R]:
#     """Muestra argumentos y resultado de la función."""
#     @functools.wraps(func)
#     def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
#         # Formatear argumentos
#         args_repr = [repr(a) for a in args]
#         kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
#         signature = ", ".join(args_repr + kwargs_repr)
#
#         print(f"🔍 Calling {func.__name__}({signature})")
#         result = func(*args, **kwargs)
#         print(f"🔍 {func.__name__} returned {result!r}")
#
#         return result
#     return wrapper
#
#
# @debug
# def greet(name: str, greeting: str = "Hello") -> str:
#     """Saluda a una persona."""
#     return f"{greeting}, {name}!"
#
#
# greet("Alice", greeting="Hi")

print()


# ============================================
# PASO 3: Decorador Retry
# ============================================
print("=== PASO 3: Retry ===")

# El decorador retry reintenta la función si falla.
# Es un decorador CON ARGUMENTOS, por eso tiene una función extra.
# Estructura: retry(args) -> decorator -> wrapper

# Descomenta las siguientes líneas:

# def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
#     """
#     Reintenta la función si falla.
#
#     Args:
#         max_attempts: Número máximo de intentos
#         delay: Segundos entre intentos
#         exceptions: Tupla de excepciones a capturar
#     """
#     def decorator(func: Callable[P, R]) -> Callable[P, R]:
#         @functools.wraps(func)
#         def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
#             last_exception = None
#
#             for attempt in range(1, max_attempts + 1):
#                 try:
#                     return func(*args, **kwargs)
#                 except exceptions as e:
#                     last_exception = e
#                     print(f"⚠️ Attempt {attempt} failed: {e}")
#                     if attempt < max_attempts:
#                         time.sleep(delay)
#
#             raise last_exception
#         return wrapper
#     return decorator
#
#
# @retry(max_attempts=3, delay=0.2, exceptions=(ConnectionError,))
# def unstable_api() -> str:
#     """Simula una API inestable."""
#     if random.random() < 0.6:
#         raise ConnectionError("Network error")
#     return "Data received"
#
#
# try:
#     result = unstable_api()
#     print(f"✅ {result}")
# except ConnectionError as e:
#     print(f"❌ Failed after all attempts: {e}")

print()


# ============================================
# PASO 4: Decorador Validate Types
# ============================================
print("=== PASO 4: Validate Types ===")

# Este decorador valida los tipos de los argumentos
# usando inspect para obtener información de la firma.

# Descomenta las siguientes líneas:

# import inspect
#
# def validate_types(**expected_types):
#     """
#     Valida tipos de argumentos.
#
#     Usage:
#         @validate_types(x=int, y=str)
#         def func(x, y): ...
#     """
#     def decorator(func: Callable) -> Callable:
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs) -> Any:
#             # Vincular argumentos a parámetros
#             sig = inspect.signature(func)
#             bound = sig.bind(*args, **kwargs)
#             bound.apply_defaults()
#
#             # Validar cada tipo especificado
#             for param, expected in expected_types.items():
#                 if param in bound.arguments:
#                     value = bound.arguments[param]
#                     if not isinstance(value, expected):
#                         raise TypeError(
#                             f"{param} must be {expected.__name__}, "
#                             f"got {type(value).__name__}"
#                         )
#
#             return func(*args, **kwargs)
#         return wrapper
#     return decorator
#
#
# @validate_types(x=int, y=int)
# def multiply(x: int, y: int) -> int:
#     """Multiplica dos números."""
#     return x * y
#
#
# # Prueba válida
# print(f"multiply(3, 4) = {multiply(3, 4)}")
#
# # Prueba inválida
# try:
#     multiply(3, "4")
# except TypeError as e:
#     print(f"❌ TypeError: {e}")

print()


# ============================================
# PASO 5: Decorador Cache con TTL
# ============================================
print("=== PASO 5: Cache TTL ===")

# Cache que expira después de cierto tiempo.
# Almacena resultados con timestamp para verificar expiración.

# Descomenta las siguientes líneas:

# def cache_with_ttl(seconds: float = 60):
#     """
#     Cachea resultados por tiempo limitado (TTL).
#
#     Args:
#         seconds: Tiempo de vida del cache en segundos
#     """
#     def decorator(func: Callable[P, R]) -> Callable[P, R]:
#         cache: dict[tuple, tuple[R, float]] = {}
#
#         @functools.wraps(func)
#         def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
#             # Crear clave del cache
#             key = (args, tuple(sorted(kwargs.items())))
#             current_time = time.time()
#
#             # Verificar si existe en cache y no expiró
#             if key in cache:
#                 result, timestamp = cache[key]
#                 if current_time - timestamp < seconds:
#                     print(f"📦 Cache hit for {func.__name__}")
#                     return result
#
#             # Calcular y guardar en cache
#             print(f"🔄 Computing {func.__name__}...")
#             result = func(*args, **kwargs)
#             cache[key] = (result, current_time)
#             return result
#
#         # Método para limpiar cache manualmente
#         wrapper.clear_cache = lambda: cache.clear()
#
#         return wrapper
#     return decorator
#
#
# @cache_with_ttl(seconds=2)
# def expensive_computation(n: int) -> int:
#     """Simula operación costosa."""
#     time.sleep(0.5)
#     return n * n
#
#
# print(f"First call: {expensive_computation(2)}")
# print(f"Second call (cached): {expensive_computation(2)}")
# print("Waiting for TTL to expire...")
# time.sleep(2.5)
# print(f"After TTL: {expensive_computation(2)}")

print()


# ============================================
# PASO 6: Múltiples Decoradores
# ============================================
print("=== PASO 6: Multiple Decorators ===")

# Los decoradores se aplican de abajo hacia arriba.
# @a
# @b
# def f(): ...
# Es equivalente a: f = a(b(f))

# Descomenta las siguientes líneas (requiere los decoradores anteriores):

# def simple_timer(func: Callable[P, R]) -> Callable[P, R]:
#     """Timer simplificado para demostración."""
#     @functools.wraps(func)
#     def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
#         start = time.perf_counter()
#         result = func(*args, **kwargs)
#         elapsed = time.perf_counter() - start
#         print(f"⏱️ {func.__name__} took {elapsed:.4f}s")
#         return result
#     return wrapper
#
#
# def simple_debug(func: Callable[P, R]) -> Callable[P, R]:
#     """Debug simplificado para demostración."""
#     @functools.wraps(func)
#     def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
#         print(f"🔍 Calling {func.__name__}")
#         result = func(*args, **kwargs)
#         print(f"🔍 {func.__name__} finished")
#         return result
#     return wrapper
#
#
# @simple_timer
# @simple_debug
# def process_data(items: int) -> list[int]:
#     """Procesa datos con múltiples decoradores."""
#     time.sleep(0.1)
#     return [i * 2 for i in range(items)]
#
#
# result = process_data(5)
# print(f"Result: {result}")

print()


# ============================================
# RESUMEN
# ============================================
print("=" * 50)
print("RESUMEN DE DECORADORES")
print("=" * 50)
print("""
✅ @timer          - Mide tiempo de ejecución
✅ @debug          - Muestra args y resultado
✅ @retry(n)       - Reintenta n veces si falla
✅ @validate_types - Valida tipos de argumentos
✅ @cache_with_ttl - Cache con tiempo de vida

Recuerda:
- Siempre usa @functools.wraps
- Decoradores con args: decorator(args) -> wrapper
- Se aplican de abajo hacia arriba
""")
