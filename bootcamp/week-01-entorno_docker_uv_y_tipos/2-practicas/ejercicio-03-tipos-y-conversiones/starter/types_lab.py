"""Ejercicio 03: tipos básicos de Python y conversiones explícitas."""

import math


def type_name(value: object) -> str:
    """Devuelve el nombre del tipo de value: "int", "float", "str", "bool" o "NoneType"."""
    raise NotImplementedError("Paso 2: implementa type_name")


def to_int(text: str) -> int:
    """Convierte un texto como " 42 " en el entero 42 (ignora espacios a los lados)."""
    raise NotImplementedError("Paso 3: implementa to_int")


def to_float(text: str) -> float:
    """Convierte "3.5" en 3.5. Acepta también la coma decimal: "3,5" da 3.5."""
    raise NotImplementedError("Paso 4: implementa to_float")


def floats_are_equal(a: float, b: float) -> bool:
    """True si a y b son iguales salvo el error de redondeo de los float."""
    raise NotImplementedError("Paso 5: implementa floats_are_equal")


def digits_of_power_of_two(exponent: int) -> int:
    """Cuántas cifras tiene 2 elevado a exponent. Ejemplo: 2**10 = 1024 tiene 4."""
    raise NotImplementedError("Paso 6: implementa digits_of_power_of_two")


def is_missing(value: object) -> bool:
    """True solo si value es None. 0, "" y False NO cuentan como dato faltante."""
    raise NotImplementedError("Paso 7: implementa is_missing")


if __name__ == "__main__":
    print(type_name(3), type_name(3.0), type_name("3"), type_name(True), type_name(None))
    print(to_int(" 42 "), to_float("3,5"))
    print(0.1 + 0.2 == 0.3, floats_are_equal(0.1 + 0.2, 0.3))
    print(digits_of_power_of_two(100))
    print(is_missing(None), is_missing(0))
    print(math.pi)
