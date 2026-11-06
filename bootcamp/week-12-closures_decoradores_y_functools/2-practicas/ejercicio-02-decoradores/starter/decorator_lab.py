"""Ejercicio 02: decoradores.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python decorator_lab.py
"""

import functools
from collections.abc import Callable

print("Ejercicio 02 · Decoradores")

# ============================================
# PASO 1: un decorador escrito a mano
# ============================================
# Descomenta las siguientes líneas:
# def announce(func: Callable[[float], float]) -> Callable[[float], float]:
#     def wrapper(value: float) -> float:
#         print(f"    llamo a {func.__name__}({value})")
#         return func(value)
#
#     return wrapper
#
#
# def to_fahrenheit(celsius: float) -> float:
#     """Grados Celsius a Fahrenheit."""
#     return celsius * 9 / 5 + 32
#
#
# print("Sin decorar:", to_fahrenheit(10.0))
# announced = announce(to_fahrenheit)
# print("Decorada a mano:", announced(10.0))

# ============================================
# PASO 2: la sintaxis @ y lo que se pierde
# ============================================
# Descomenta las siguientes líneas:
# @announce
# def to_kelvin(celsius: float) -> float:
#     """Grados Celsius a Kelvin."""
#     return celsius + 273.15
#
#
# print("Con @:", to_kelvin(10.0))
# print("¿Cómo se llama?", to_kelvin.__name__, "· ¿y su docstring?", to_kelvin.__doc__)

# ============================================
# PASO 3: functools.wraps
# ============================================
# Descomenta las siguientes líneas:
# def announce_wrapped(func: Callable[[float], float]) -> Callable[[float], float]:
#     @functools.wraps(func)
#     def wrapper(value: float) -> float:
#         print(f"    llamo a {func.__name__}({value})")
#         return func(value)
#
#     return wrapper
#
#
# @announce_wrapped
# def to_rankine(celsius: float) -> float:
#     """Grados Celsius a Rankine."""
#     return (celsius + 273.15) * 9 / 5
#
#
# print("Con wraps:", to_rankine.__name__, "·", to_rankine.__doc__)
# print("La original sigue dentro:", round(to_rankine.__wrapped__(0.0), 2))  # type: ignore[attr-defined]

# ============================================
# PASO 4: un decorador para cualquier función
# ============================================
# Descomenta las siguientes líneas:
# def counted[**P, R](func: Callable[P, R]) -> Callable[P, R]:
#     calls = 0
#
#     @functools.wraps(func)
#     def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
#         nonlocal calls
#         calls += 1
#         print(f"    {func.__name__}: llamada {calls}")
#         return func(*args, **kwargs)
#
#     return wrapper
#
#
# @counted
# def mean(values: list[float]) -> float:
#     return sum(values) / len(values)
#
#
# @counted
# def label_of(label: str, *, upper: bool = False) -> str:
#     return label.upper() if upper else label
#
#
# print("Media:", mean([10.0, 20.0]))
# print("Media:", mean([1.0, 2.0, 3.0]))
# print("Etiqueta:", label_of("Norte", upper=True))

# ============================================
# PASO 5: apilar decoradores
# ============================================
# Descomenta las siguientes líneas:
# def bold(func: Callable[[], str]) -> Callable[[], str]:
#     @functools.wraps(func)
#     def wrapper() -> str:
#         return f"<b>{func()}</b>"
#
#     return wrapper
#
#
# def italic(func: Callable[[], str]) -> Callable[[], str]:
#     @functools.wraps(func)
#     def wrapper() -> str:
#         return f"<i>{func()}</i>"
#
#     return wrapper
#
#
# @bold
# @italic
# def title() -> str:
#     return "Observatorio"
#
#
# @italic
# @bold
# def subtitle() -> str:
#     return "capa 11"
#
#
# print("bold encima de italic:", title())
# print("italic encima de bold:", subtitle())
