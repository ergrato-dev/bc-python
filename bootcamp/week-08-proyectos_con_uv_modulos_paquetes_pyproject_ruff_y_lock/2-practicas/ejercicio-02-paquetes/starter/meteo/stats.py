"""Estadísticas sencillas de temperaturas."""

# Import relativo: el punto es "el paquete en el que estoy", aquí meteo.
from .convert import _round1, c_to_f


def mean(values: list[float]) -> float:
    """La media, con un decimal."""
    return _round1(sum(values) / len(values))


def mean_f(values: list[float]) -> float:
    """La media en Fahrenheit."""
    return _round1(c_to_f(sum(values) / len(values)))


if __name__ == "__main__":
    print("Prueba rápida de stats:", mean([20.0, 22.5, 19.0]))
