"""Funciones que fabrican y envuelven funciones: closures, decoradores y functools.

Qué: un filtro que recuerda su límite (above), dos decoradores (skip_missing y rounded)
y una función que se comporta distinto según el tipo de lo que recibe (describe).
Para qué: escribir una vez el comportamiento común (saltar los None, redondear,
filtrar) y aplicarlo a cualquier función, sin repetirlo dentro de cada una.
Impacto: el modelo no importa este módulo; este módulo importa el modelo.
"""

from collections.abc import Callable
from functools import singledispatch, wraps

from observatorio.core.model import Measurement, Scale, Series


def above(limit: float) -> Callable[[Measurement], bool]:
    """Un filtro para Series.where: True si la medida tiene valor y es mayor que limit.

    La función devuelta es una closure: recuerda limit después de que above termine.
    """

    def is_above(measurement: Measurement) -> bool:
        return measurement.value is not None and measurement.value > limit

    return is_above


def skip_missing(func: Callable[[float], float]) -> Callable[[float | None], float | None]:
    """Decorador: la función acepta también None y entonces devuelve None sin llamarla."""

    @wraps(func)
    def wrapper(value: float | None) -> float | None:
        if value is None:
            return None
        return func(value)

    return wrapper


def rounded[**P](digits: int) -> Callable[[Callable[P, float]], Callable[P, float]]:
    """Decorador con argumento: redondea a digits decimales lo que devuelve la función.

    Ejemplo: @rounded(1) encima de una función que devuelve 12.345 hace que devuelva 12.3.
    """

    def decorator(func: Callable[P, float]) -> Callable[P, float]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> float:
            return round(func(*args, **kwargs), digits)

        return wrapper

    return decorator


@singledispatch
def describe(item: object) -> str:
    """Una frase que describe una medida, una serie o una escala.

    Cada tipo registra su versión con @describe.register; con otro tipo, TypeError.
    """
    raise TypeError(f"describe no acepta {type(item).__name__}")


@describe.register
def _(item: Measurement) -> str:
    text = "sin dato" if item.value is None else str(item.value).replace(".", ",")
    return f"{item.label}: {text}"


@describe.register
def _(item: Series) -> str:
    return f"medidas: {len(item)} · etiquetas: {len(item.labels())}"


@describe.register
def _(item: Scale) -> str:
    return f"{item.unit} entre {item.low:g} y {item.high:g}"
