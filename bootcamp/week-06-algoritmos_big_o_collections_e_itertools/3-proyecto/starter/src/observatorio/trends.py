"""Tendencias del Observatorio: frecuencias, mediana, media móvil y saltos.

Qué: funciones puras sobre los registros y sus valores, en el orden en que llegan.
Para qué: las medias por etiqueta de la semana 5 no dicen cómo evolucionan las medidas;
la media móvil suaviza el ruido y el mayor salto señala el cambio más brusco.
Impacto: cada función recorre los datos una sola vez (O(n)), salvo la mediana, que
ordena (O(n log n)). En la semana 25, pandas hace lo mismo con value_counts(),
median(), rolling(3).mean() y diff().
"""

from collections import Counter, deque
from itertools import pairwise

from observatorio.groups import Record


def values_of(records: list[Record]) -> list[float]:
    """Los valores de los registros, en orden, sin los None."""
    raise NotImplementedError("Paso 5: implementa values_of")


def most_common_labels(records: list[Record], n: int) -> list[tuple[str, int]]:
    """Las n etiquetas con más registros y cuántos tienen, de más a menos.

    Cuenta también los registros sin dato: miden cuántas veces llegó la etiqueta.
    Con conteos iguales, va primero la etiqueta que apareció antes.
    """
    raise NotImplementedError("Paso 5: implementa most_common_labels")


def median(values: list[float]) -> float:
    """El valor del medio de values ordenados; con un número par, la media de los dos del medio.

    No cambia values. Lanza ValueError si values está vacía: no hay mediana de nada.
    Ejemplo: median([8.0, 61.0, 12.5]) da 12.5; median([8.0, 61.0, 12.5, 9.5]) da 11.0.
    """
    raise NotImplementedError("Paso 6: implementa median")


def moving_average(values: list[float], window: int) -> list[float]:
    """La media de cada tramo de `window` valores seguidos, en orden.

    Con 5 valores y window 3 da 3 medias: la de los valores 1-3, la de 2-4 y la de 3-5.
    Si hay menos valores que window, da una lista vacía.
    Lanza ValueError si window es menor que 1.
    Recorre values una sola vez: suma el valor que entra y resta el que sale.
    """
    raise NotImplementedError("Paso 7: implementa moving_average")


def jumps(values: list[float]) -> list[float]:
    """La diferencia entre cada valor y el anterior: jumps([10.0, 15.0, 12.0]) da [5.0, -3.0]."""
    raise NotImplementedError("Paso 8: implementa jumps")


def largest_jump(values: list[float]) -> float:
    """El salto más grande en valor absoluto, con su signo; 0.0 si hay menos de dos valores.

    Ejemplo: con saltos [5.0, -8.0, 3.0] da -8.0. Con dos iguales en tamaño, el primero.
    """
    raise NotImplementedError("Paso 8: implementa largest_jump")
