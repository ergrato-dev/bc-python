"""La serie como tabla de pandas: seleccionar, ordenar, contar y escribir sin bucles.

Este módulo importa pandas, que tarda en cargarse: core/__init__.py no lo reexporta, y la
CLI lo importa solo dentro del comando que lo usa.
"""

from collections.abc import Collection
from pathlib import Path

import pandas as pd

from observatorio.core.model import Scale, Series

# Las columnas de medidas.csv, en español, y las del DataFrame, en inglés.
FILE_COLUMNS = {"etiqueta": "label", "valor": "value"}


def frame_of(series: Series) -> pd.DataFrame:
    """Una fila por medida, con label (str) y value (float64, NaN si falta); índice desde 1."""
    return pd.DataFrame(
        {
            "label": pd.Series([m.label for m in series], dtype="str"),
            "value": pd.Series([m.value for m in series], dtype="float64"),
        }
    ).set_axis(pd.RangeIndex(1, len(series) + 1, name="position"))


def with_levels(frame: pd.DataFrame, scale: Scale) -> pd.DataFrame:
    """Una copia con la columna level, como Scale.level pero sin bucle de Python."""
    # right=False: cada intervalo incluye su borde izquierdo, así un valor igual a low ya es
    # "medio" y uno igual a high, "alto", como en classify.
    levels = pd.cut(
        frame["value"],
        bins=[float("-inf"), scale.low, scale.high, float("inf")],
        labels=["bajo", "medio", "alto"],
        right=False,
    )
    return frame.assign(level=levels.astype("str").where(levels.notna(), "sin dato"))


def select(
    frame: pd.DataFrame,
    *,
    labels: Collection[str] = (),
    low: float | None = None,
    high: float | None = None,
) -> pd.DataFrame:
    """Las filas con alguna de labels (todas si no hay) y value entre low y high, incluidos."""
    keep = pd.Series(True, index=frame.index)
    if labels:
        keep &= frame["label"].isin(labels)
    # Un NaN comparado con cualquier número da False: filtrar por valor quita las sin dato.
    if low is not None:
        keep &= frame["value"] >= low
    if high is not None:
        keep &= frame["value"] <= high
    return frame.loc[keep]


def by_value(frame: pd.DataFrame) -> pd.DataFrame:
    """Las filas de mayor a menor valor, las sin dato al final y los empates en su orden."""
    # kind="stable": el quicksort por defecto desordena los empates a partir de unas decenas.
    return frame.sort_values("value", ascending=False, na_position="last", kind="stable")


def label_counts(frame: pd.DataFrame) -> dict[str, int]:
    """Cuántas medidas hay de cada etiqueta, de la más frecuente a la menos."""
    # value_counts deja los empates en el orden en que aparece cada etiqueta, como
    # Counter.most_common: lo vigila un test con Hypothesis.
    counts = frame["label"].value_counts()
    return {str(label): int(count) for label, count in counts.items()}


def write_frame(frame: pd.DataFrame, path: Path) -> None:
    """Escribe label y value como medidas.csv: etiqueta;valor, coma decimal y NA si falta."""
    frame[list(FILE_COLUMNS.values())].rename(
        columns={new: old for old, new in FILE_COLUMNS.items()}
    ).to_csv(path, sep=";", decimal=",", na_rep="NA", index=False)
