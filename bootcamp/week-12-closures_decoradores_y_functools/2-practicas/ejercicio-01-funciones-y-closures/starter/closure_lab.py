"""Ejercicio 01: funciones y closures.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python closure_lab.py
"""

from collections.abc import Callable

print("Ejercicio 01 · Funciones y closures")

READINGS = [("Norte", 12.5), ("Sur", 8.0), ("Centro", 55.1), ("Este", 48.9)]

# ============================================
# PASO 1: una función es un objeto
# ============================================
# Descomenta las siguientes líneas:
# def to_fahrenheit(celsius: float) -> float:
#     """Grados Celsius a Fahrenheit."""
#     return celsius * 9 / 5 + 32
#
#
# convert = to_fahrenheit
# print("Otro nombre, la misma función:", convert is to_fahrenheit, convert(10.0))
# print("Tiene atributos:", to_fahrenheit.__name__, "·", to_fahrenheit.__doc__)
# print("Su tipo:", type(to_fahrenheit).__name__)
# conversions = {"F": to_fahrenheit, "K": lambda celsius: celsius + 273.15}
# for unit, function in conversions.items():
#     print(f"  10 °C en {unit}: {function(10.0):.2f}")

# ============================================
# PASO 2: funciones que reciben funciones
# ============================================
# Descomenta las siguientes líneas:
# def value_of(reading: tuple[str, float]) -> float:
#     return reading[1]
#
#
# def apply_to_values(function: Callable[[float], float], values: list[float]) -> list[float]:
#     return [function(value) for value in values]
#
#
# print("Ordenadas por valor:", [label for label, _ in sorted(READINGS, key=value_of)])
# print("La más alta:", max(READINGS, key=value_of))
# print("Dobles:", apply_to_values(lambda v: v * 2, [1.0, 2.5]))
# print("Con map:", list(map(abs, [-1.5, 2.0, -3.0])))

# ============================================
# PASO 3: el alcance de una variable (LEGB)
# ============================================
# Descomenta las siguientes líneas:
# limit = 50.0
#
#
# def is_high(value: float) -> bool:
#     return value > limit
#
#
# def change_limit() -> None:
#     limit = 10.0
#     print("  Dentro, otra variable:", limit)
#
#
# def broken_counter() -> None:
#     total = 0
#
#     def add() -> None:
#         total += 1  # noqa: F823, F841
#
#     add()
#
#
# print("Lee la global:", is_high(55.1))
# change_limit()
# print("La global no cambia:", limit)
# try:
#     broken_counter()
# except UnboundLocalError as error:
#     print("UnboundLocalError:", error)

# ============================================
# PASO 4: closures y nonlocal
# ============================================
# Descomenta las siguientes líneas:
# def make_threshold(limit: float) -> Callable[[float], bool]:
#     def is_above(value: float) -> bool:
#         return value > limit
#
#     return is_above
#
#
# def make_counter() -> Callable[[], int]:
#     count = 0
#
#     def increment() -> int:
#         nonlocal count
#         count += 1
#         return count
#
#     return increment
#
#
# above_50 = make_threshold(50.0)
# above_10 = make_threshold(10.0)
# print("¿55,1 > 50?", above_50(55.1), "· ¿8 > 10?", above_10(8.0))
# print("Lo que recuerda above_50:", above_50.__closure__[0].cell_contents)  # type: ignore[index]
# counter = make_counter()
# other = make_counter()
# print("Contador:", counter(), counter(), counter(), "· otro:", other())

# ============================================
# PASO 5: la trampa de las closures en un bucle
# ============================================
# Descomenta las siguientes líneas:
# late = [lambda value: value > limit for limit in (10.0, 30.0, 50.0)]  # noqa: B023
# print("Tarde, ¿20 supera cada límite?", [check(20.0) for check in late])
# early = [lambda value, limit=limit: value > limit for limit in (10.0, 30.0, 50.0)]
# print("Con valor por defecto:", [check(20.0) for check in early])
# factory = [make_threshold(limit) for limit in (10.0, 30.0, 50.0)]
# print("Con una fábrica:", [check(20.0) for check in factory])
