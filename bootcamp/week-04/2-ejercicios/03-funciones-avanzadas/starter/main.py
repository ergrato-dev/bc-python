"""
Ejercicio 03: Funciones Avanzadas
=================================
Practica *args, **kwargs, scope y closures.

Instrucciones:
1. Lee cada sección
2. Descomenta el código indicado
3. Ejecuta para verificar resultados
"""

# ============================================
# PASO 1: *args Básico
# ============================================
print("=== PASO 1: *args Básico ===")

# *args permite recibir cualquier cantidad de argumentos posicionales.
# Dentro de la función, args es una TUPLA.

# Descomenta las siguientes líneas:
# def sum_all(*numbers: int) -> int:
#     """Suma cualquier cantidad de números.
#
#     Args:
#         *numbers: Números a sumar (cantidad variable).
#
#     Returns:
#         La suma de todos los números.
#     """
#     total = 0
#     for num in numbers:
#         total += num
#     return total
#
# print(f"Suma de 1, 2: {sum_all(1, 2)}")
# print(f"Suma de 1, 2, 3, 4, 5: {sum_all(1, 2, 3, 4, 5)}")
# print(f"Suma de ninguno: {sum_all()}")
#
# # Verificar tipo
# def show_type(*args):
#     print(f"Args es tipo: {type(args)}")
#
# show_type(1, 2, 3)

print()

# ============================================
# PASO 2: *args con Parámetros Regulares
# ============================================
print("=== PASO 2: *args con Parámetros Regulares ===")

# Puedes combinar parámetros regulares con *args.
# Los regulares van ANTES de *args.

# Descomenta las siguientes líneas:
# def log_messages(level: str, *messages: str) -> None:
#     """Registra mensajes con un nivel.
#
#     Args:
#         level: Nivel del log (INFO, WARNING, ERROR).
#         *messages: Mensajes a registrar.
#     """
#     for msg in messages:
#         print(f"[{level}] {msg}")
#
# log_messages("INFO", "Sistema iniciado")
# log_messages("WARNING", "Memoria baja", "Disco lleno")
# log_messages("ERROR", "Conexión perdida")

print()

# ============================================
# PASO 3: **kwargs Básico
# ============================================
print("=== PASO 3: **kwargs Básico ===")

# **kwargs permite recibir cualquier cantidad de argumentos keyword.
# Dentro de la función, kwargs es un DICCIONARIO.

# Descomenta las siguientes líneas:
# def print_info(**info) -> None:
#     """Imprime información como pares clave-valor.
#
#     Args:
#         **info: Pares clave-valor de información.
#     """
#     for key, value in info.items():
#         print(f"{key}: {value}")
#
# print_info(name="Ana", age=25, city="Madrid")
# print("---")
# print_info(role="developer")
#
# # Verificar tipo
# def show_kwargs_type(**kwargs):
#     print(f"Kwargs es tipo: {type(kwargs)}")
#
# show_kwargs_type(a=1, b=2)

print()

# ============================================
# PASO 4: Combinar *args y **kwargs
# ============================================
print("=== PASO 4: Combinar *args y **kwargs ===")

# Puedes usar ambos en la misma función.
# Orden: parámetros regulares, *args, **kwargs

# Descomenta las siguientes líneas:
# def flexible_log(level: str, *tags: str, **metadata) -> None:
#     """Log flexible con tags y metadata.
#
#     Args:
#         level: Nivel del log.
#         *tags: Tags para categorizar.
#         **metadata: Información adicional.
#     """
#     tag_str = ",".join(tags) if tags else "none"
#     meta_str = ", ".join(f"{k}: {v}" for k, v in metadata.items())
#     print(f"[{level}] {{tags: {tag_str}}}")
#     if meta_str:
#         print(f"[{level}] {{{meta_str}}}")
#
# flexible_log("INFO", "auth", "login")
# flexible_log("DEBUG", user_id=123, ip="192.168.1.1")

print()

# ============================================
# PASO 5: Desempaquetado en Llamadas
# ============================================
print("=== PASO 5: Desempaquetado en Llamadas ===")

# * desempaqueta lista/tupla en argumentos posicionales.
# ** desempaqueta diccionario en argumentos keyword.

# Descomenta las siguientes líneas:
# def add_three(a: int, b: int, c: int) -> int:
#     """Suma tres números."""
#     return a + b + c
#
# def greet(name: str, greeting: str = "Hello") -> str:
#     """Saluda a una persona."""
#     return f"{greeting}, {name}!"
#
# # Desempaquetar lista con *
# numbers = [1, 2, 3]
# print(f"Suma: {add_three(*numbers)}")
#
# # Desempaquetar dict con **
# config = {"name": "Alice", "greeting": "Hello"}
# print(f"Saludo: {greet(**config)}")

print()

# ============================================
# PASO 6: Scope - Variables Locales
# ============================================
print("=== PASO 6: Scope - Variables Locales ===")

# Las variables dentro de una función son LOCALES.
# No afectan variables del mismo nombre fuera.

# Descomenta las siguientes líneas:
# message = "global"
#
# def show_local():
#     message = "local"  # Esta es una variable LOCAL
#     print(f"Dentro: {message}")
#
# show_local()
# print(f"Fuera: {message}")  # La global no cambió

print()

# ============================================
# PASO 7: La Palabra global
# ============================================
print("=== PASO 7: La Palabra global ===")

# 'global' permite MODIFICAR una variable global desde una función.
# ⚠️ Usar con cuidado - puede hacer el código difícil de seguir.

# Descomenta las siguientes líneas:
# counter = 0
#
# def increment():
#     global counter
#     counter += 1
#
# print(f"Antes: {counter}")
# increment()
# increment()
# increment()
# print(f"Después de incrementar: {counter}")

print()

# ============================================
# PASO 8: Closure Básico
# ============================================
print("=== PASO 8: Closure Básico ===")

# Un closure es una función que "recuerda" variables
# del scope donde fue creada.

# Descomenta las siguientes líneas:
# def make_multiplier(factor: int):
#     """Crea una función que multiplica por factor.
#
#     Args:
#         factor: El multiplicador a usar.
#
#     Returns:
#         Función que multiplica su argumento por factor.
#     """
#     def multiplier(number: int) -> int:
#         return number * factor  # 'factor' viene del scope exterior
#     return multiplier
#
# # Crear funciones especializadas
# double = make_multiplier(2)
# triple = make_multiplier(3)
#
# print(f"Doble de 5: {double(5)}")
# print(f"Triple de 5: {triple(5)}")
# print(f"Doble de 10: {double(10)}")

print()

# ============================================
# PASO 9: Closure con Estado
# ============================================
print("=== PASO 9: Closure con Estado ===")

# Los closures pueden mantener estado entre llamadas.

# Descomenta las siguientes líneas:
# def create_counter():
#     """Crea un contador que recuerda su valor.
#
#     Returns:
#         Función que incrementa y retorna el contador.
#     """
#     count = 0
#
#     def increment() -> int:
#         nonlocal count  # Modifica variable del scope exterior
#         count += 1
#         return count
#
#     return increment
#
# # Crear contadores independientes
# counter1 = create_counter()
# counter2 = create_counter()
#
# print(f"Contador 1: {counter1()}")
# print(f"Contador 1: {counter1()}")
# print(f"Contador 1: {counter1()}")
# print(f"Contador 2: {counter2()}")  # Contador separado

print()

# ============================================
# PASO 10: Funciones como Objetos
# ============================================
print("=== PASO 10: Funciones como Objetos ===")

# Las funciones son objetos de primera clase.
# Puedes pasarlas como argumentos y guardarlas en variables.

# Descomenta las siguientes líneas:
# def add(a: int, b: int) -> int:
#     return a + b
#
# def multiply(a: int, b: int) -> int:
#     return a * b
#
# def apply_operation(func, x: int, y: int) -> int:
#     """Aplica una función a dos números.
#
#     Args:
#         func: Función que toma dos ints y retorna int.
#         x: Primer número.
#         y: Segundo número.
#
#     Returns:
#         Resultado de aplicar func(x, y).
#     """
#     return func(x, y)
#
# # Pasar funciones como argumentos
# print(f"Con add: {apply_operation(add, 10, 5)}")
# print(f"Con multiply: {apply_operation(multiply, 10, 5)}")
#
# # Funciones en lista
# operations = [add, multiply]
# results = [op(10, 5) for op in operations]
# print(f"Operaciones: {results}")


# ============================================
# ¡FELICIDADES! 🎉
# ============================================
# Has completado el ejercicio de funciones avanzadas.
# Ahora dominas:
# - *args para argumentos posicionales variables
# - **kwargs para argumentos keyword variables
# - Desempaquetado con * y **
# - Scope de variables y LEGB
# - Closures con estado
# - Funciones como objetos de primera clase
