"""Las medidas como arrays de NumPy: la estadística de la serie entera, sin bucles.

Qué: convierte una Series en un array de float64 (NaN donde falta el dato) y calcula
sobre él el resumen, las puntuaciones z, las medidas atípicas, el histograma y la
media de cada etiqueta.
Para qué: cada operación recorre el array en C, de una vez; con 100 000 medidas es
mucho más rápido que el bucle equivalente en Python, y se escribe en una línea.
Impacto: importar NumPy cuesta alrededor de 0,1 s. Este módulo no se reexporta en
`observatorio.core`, y la CLI lo importa solo en `estadisticas`: `informe` no lo paga.
"""

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from observatorio.core.model import Series

# Un array de números de coma flotante de 64 bits, el tipo de casi todo lo que sigue.
Floats = NDArray[np.float64]
# Un array de enteros del tamaño de un índice: conteos y posiciones.
Counts = NDArray[np.intp]


@dataclass(frozen=True)
class Stats:
    """El resumen de los valores presentes de una serie, los que no son NaN."""

    count: int
    missing: int
    mean: float
    std: float
    minimum: float
    q1: float
    median: float
    q3: float
    maximum: float


def values_array(series: Series) -> Floats:
    """Los valores de la serie en un array, en orden; NaN donde falta el dato.

    Un array tiene un solo tipo: None no cabe en float64, NaN sí. Así la posición i del
    array sigue siendo la medida i de la serie.
    """
    return np.fromiter(
        (np.nan if measurement.value is None else measurement.value for measurement in series),
        dtype=np.float64,
        count=len(series),
    )


def labels_array(series: Series) -> NDArray[np.str_]:
    """Las etiquetas de la serie en un array de texto, en el mismo orden que values_array."""
    return np.array([measurement.label for measurement in series], dtype=np.str_)


def stats_of(values: Floats) -> Stats | None:
    """El resumen de los valores que no son NaN, o None si no hay ninguno.

    La desviación es la de la población (ddof=0), la misma que np.std por defecto.
    """
    present = values[~np.isnan(values)]
    if present.size == 0:
        return None
    q1, median, q3 = np.percentile(present, [25, 50, 75])
    return Stats(
        count=int(present.size),
        missing=int(values.size - present.size),
        mean=float(present.mean()),
        std=float(present.std()),
        minimum=float(present.min()),
        q1=float(q1),
        median=float(median),
        q3=float(q3),
        maximum=float(present.max()),
    )


def zscores(values: Floats) -> Floats:
    """A cuántas desviaciones de la media está cada valor: (valor - media) / desviación.

    NaN donde falta el dato. Si no hay valores o todos son iguales (desviación 0), todo
    NaN: ningún valor se aleja de la media, y dividir por 0 daría inf o NaN con un aviso.
    """
    present = values[~np.isnan(values)]
    std = present.std() if present.size else 0.0
    if std == 0:
        return np.full_like(values, np.nan)
    return (values - present.mean()) / std


def outliers(values: Floats, threshold: float) -> Counts:
    """Las posiciones de los valores con |z| > threshold, en orden.

    Una comparación con NaN da False: los datos que faltan nunca son atípicos.
    """
    return np.flatnonzero(np.abs(zscores(values)) > threshold)


def histogram(values: Floats, bins: int) -> tuple[Counts, Floats]:
    """Cuántos valores caen en cada uno de `bins` intervalos iguales, y sus bordes.

    Sin los NaN. Devuelve bins conteos y bins + 1 bordes; el último intervalo incluye
    su borde derecho, así que el máximo también cuenta.
    """
    counts, edges = np.histogram(values[~np.isnan(values)], bins=bins)
    return counts, edges


def group_means(labels: NDArray[np.str_], values: Floats) -> dict[str, float]:
    """La media de cada etiqueta, sin bucles: {"Norte": 30.7, "Sur": 8.75}.

    Mismo resultado que Series.means(): sin los NaN, y una etiqueta sin ningún valor no
    aparece. Las etiquetas salen ordenadas, porque np.unique las ordena.
    """
    present = ~np.isnan(values)
    names, codes = np.unique(labels[present], return_inverse=True)
    sums = np.bincount(codes, weights=values[present])
    counts = np.bincount(codes)
    return dict(zip(names.tolist(), (sums / counts).tolist(), strict=True))
