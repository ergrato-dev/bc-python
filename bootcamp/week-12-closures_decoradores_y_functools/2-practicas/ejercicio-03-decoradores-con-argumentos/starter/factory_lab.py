"""Ejercicio 03: decoradores con argumentos.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python factory_lab.py
"""

import functools
from collections.abc import Callable, Iterator
from dataclasses import dataclass

print("Ejercicio 03 · Decoradores con argumentos")

# ============================================
# PASO 1: una fábrica de decoradores
# ============================================
# Descomenta las siguientes líneas:
# def repeat(times: int) -> Callable[[Callable[[str], None]], Callable[[str], None]]:
#     def decorator(func: Callable[[str], None]) -> Callable[[str], None]:
#         @functools.wraps(func)
#         def wrapper(text: str) -> None:
#             for _ in range(times):
#                 func(text)
#
#         return wrapper
#
#     return decorator
#
#
# @repeat(3)
# def beep(text: str) -> None:
#     print("   ", text)
#
#
# beep("alerta")
# twice = repeat(2)
# print("repeat(2) es un decorador:", twice.__name__)
# twice(print)("a mano")

# ============================================
# PASO 2: olvidar los paréntesis
# ============================================
# Descomenta las siguientes líneas:
# @repeat  # type: ignore[arg-type]
# def broken(text: str) -> None:
#     print("   ", text)
#
#
# print("Sin paréntesis, broken es:", broken.__name__)  # type: ignore[attr-defined]
# print("Y llamarla no imprime nada; devuelve:", broken("alerta").__name__)  # type: ignore[arg-type, attr-defined]

# ============================================
# PASO 3: un registro de funciones
# ============================================
# Descomenta las siguientes líneas:
# PARSERS: dict[str, Callable[[str], float]] = {}
#
#
# def parser(suffix: str) -> Callable[[Callable[[str], float]], Callable[[str], float]]:
#     def decorator(func: Callable[[str], float]) -> Callable[[str], float]:
#         PARSERS[suffix] = func
#         return func
#
#     return decorator
#
#
# @parser(".txt")
# def parse_comma(text: str) -> float:
#     return float(text.replace(",", "."))
#
#
# @parser(".csv")
# def parse_point(text: str) -> float:
#     return float(text)
#
#
# print("Registrados:", {suffix: func.__name__ for suffix, func in PARSERS.items()})
# for suffix, raw in [(".txt", "12,5"), (".csv", "55.1")]:
#     print(f"  {raw} con {suffix}: {PARSERS[suffix](raw)}")

# ============================================
# PASO 4: decoradores que ya usabas
# ============================================
# Descomenta las siguientes líneas:
# @dataclass(frozen=True)
# class WithAt:
#     label: str
#
#
# class ByHand:
#     label: str
#
#
# ByHand = dataclass(frozen=True)(ByHand)  # type: ignore[misc]
# print("Con @:", WithAt("Norte"), "· a mano:", ByHand("Norte"))  # type: ignore[call-arg]
# print("dataclass(frozen=True) devuelve:", type(dataclass(frozen=True)).__name__)
# print("property, classmethod y staticmethod son clases:", property, classmethod, staticmethod)

# ============================================
# PASO 5: reintentar una función que falla
# ============================================
# Descomenta las siguientes líneas:
# def retry[**P, R](times: int, error: type[Exception]) -> Callable[[Callable[P, R]], Callable[P, R]]:
#     def decorator(func: Callable[P, R]) -> Callable[P, R]:
#         @functools.wraps(func)
#         def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
#             for attempt in range(1, times + 1):
#                 try:
#                     return func(*args, **kwargs)
#                 except error as problem:
#                     print(f"    intento {attempt} de {times}: {problem}")
#             raise RuntimeError(f"{func.__name__} falló {times} veces")
#
#         return wrapper
#
#     return decorator
#
#
# answers: Iterator[float | Exception] = iter([ConnectionError("sin red"), ConnectionError("sin red"), 21.5])
#
#
# @retry(3, ConnectionError)
# def read_sensor() -> float:
#     answer = next(answers)
#     if isinstance(answer, Exception):
#         raise answer
#     return answer
#
#
# print("Lectura:", read_sensor())
# try:
#     read_sensor()
# except StopIteration:
#     print("Sin más respuestas: StopIteration no es ConnectionError y no se reintenta")
