"""Estadística inferencial con SciPy: ¿la diferencia entre dos etiquetas es real o es azar?

Qué: sample saca de una serie los valores de una etiqueta, y difference compara dos
muestras: la diferencia de medias con su intervalo de confianza (Welch), el tamaño del
efecto (d de Cohen) y los p-valores de Welch y de Mann-Whitney.
Para qué: dos medias distintas no bastan para decir que una etiqueta mide más que otra;
con pocas medidas, o muy dispersas, la diferencia puede ser ruido. El intervalo dice
cuánto puede valer la diferencia de verdad, y el p-valor, qué raro sería verla si no la hubiera.
Impacto: importar scipy.stats cuesta unos 0,4 s. No se reexporta en core, y la CLI lo
importa solo en `comparar`.
"""

from dataclasses import dataclass

import numpy as np
from scipy import stats

from observatorio.core.arrays import Floats, labels_array, values_array
from observatorio.core.model import Series


@dataclass(frozen=True)
class Comparison:
    """Dos muestras comparadas; difference, low y high son de la primera menos la segunda."""

    sizes: tuple[int, int]
    means: tuple[float, float]
    stds: tuple[float, float]
    difference: float
    low: float
    high: float
    effect: float
    p_welch: float
    p_ranks: float


def sample(series: Series, label: str) -> Floats:
    """Los valores de label en la serie, en orden y sin los que faltan."""
    values = values_array(series)
    # Anotado: indexar con una máscara de booleanos devuelve Any para mypy.
    chosen: Floats = values[(labels_array(series) == label) & ~np.isnan(values)]
    return chosen


def difference(first: Floats, second: Floats, confidence: float = 0.95) -> Comparison:
    """Compara dos muestras. Lanza ValueError si alguna tiene menos de 2 valores o no varía:
    sin dispersión no hay con qué medir el azar."""
    if first.size < 2 or second.size < 2:
        raise ValueError(
            f"cada muestra necesita al menos 2 valores (tienen {first.size} y {second.size})"
        )
    # min == max y no std == 0: la std de [0.1, 0.1, 0.1] sale 1,4e-17 por el redondeo.
    if first.min() == first.max() or second.min() == second.max():
        raise ValueError("las dos muestras tienen que variar: una tiene todos sus valores iguales")
    # ddof=1: la desviación de la muestra, que estima la de todas las medidas posibles.
    stds = float(first.std(ddof=1)), float(second.std(ddof=1))
    # equal_var=False es Welch: no supone que las dos etiquetas tengan la misma dispersión.
    welch = stats.ttest_ind(first, second, equal_var=False)
    interval = welch.confidence_interval(confidence)
    diff = float(first.mean() - second.mean())
    return Comparison(
        sizes=(int(first.size), int(second.size)),
        means=(float(first.mean()), float(second.mean())),
        stds=stds,
        difference=diff,
        low=float(interval.low),
        high=float(interval.high),
        # La diferencia medida en desviaciones: 0,2 es pequeña, 0,8 grande, sea cual sea la unidad.
        effect=diff / float(np.sqrt((stds[0] ** 2 + stds[1] ** 2) / 2)),
        p_welch=float(welch.pvalue),
        # Mann-Whitney compara los rangos, no las medias: no supone una campana, y un valor
        # extremo pesa como cualquier otro.
        p_ranks=float(stats.mannwhitneyu(first, second).pvalue),
    )
