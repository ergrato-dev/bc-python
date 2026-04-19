"""
Módulo de calculadora para practicar testing.

Este módulo contiene funciones matemáticas básicas
que serán testeadas en los ejercicios.
"""


def add(a: float, b: float) -> float:
    """
    Suma dos números.

    Args:
        a: Primer número
        b: Segundo número

    Returns:
        La suma de a y b
    """
    return a + b


def subtract(a: float, b: float) -> float:
    """
    Resta b de a.

    Args:
        a: Número del cual restar
        b: Número a restar

    Returns:
        El resultado de a - b
    """
    return a - b


def multiply(a: float, b: float) -> float:
    """
    Multiplica dos números.

    Args:
        a: Primer factor
        b: Segundo factor

    Returns:
        El producto de a y b
    """
    return a * b


def divide(a: float, b: float) -> float:
    """
    Divide a entre b.

    Args:
        a: Dividendo
        b: Divisor

    Returns:
        El cociente de a / b

    Raises:
        ValueError: Si b es cero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(base: float, exponent: int) -> float:
    """
    Calcula base elevado a exponent.

    Args:
        base: La base
        exponent: El exponente

    Returns:
        base elevado a exponent
    """
    return base ** exponent


def is_even(n: int) -> bool:
    """
    Verifica si un número es par.

    Args:
        n: Número a verificar

    Returns:
        True si n es par, False si es impar
    """
    return n % 2 == 0
