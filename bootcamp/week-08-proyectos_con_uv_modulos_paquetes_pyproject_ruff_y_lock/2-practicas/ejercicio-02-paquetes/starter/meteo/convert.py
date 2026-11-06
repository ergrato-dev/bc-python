"""Conversión de temperaturas."""


def c_to_f(celsius: float) -> float:
    """Convierte grados Celsius a Fahrenheit."""
    return celsius * 9 / 5 + 32


def _round1(value: float) -> float:
    """Ayuda interna: el guion bajo dice "no la uses desde fuera"."""
    return round(value, 1)
