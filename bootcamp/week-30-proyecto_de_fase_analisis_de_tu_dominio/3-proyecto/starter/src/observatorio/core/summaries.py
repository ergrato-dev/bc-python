"""Resúmenes con pandas: por etiqueta, de dos archivos a la vez y por periodos de tiempo.

Trabaja sobre las tablas de frames.py. Como frames, importa pandas: core/__init__.py no lo
reexporta, y la CLI lo importa solo dentro de los comandos que lo usan.
"""

from datetime import datetime, timedelta

import pandas as pd


def summary(frame: pd.DataFrame) -> pd.DataFrame:
    """Una fila por etiqueta, en el orden en que aparece: count, missing, mean, minimum, maximum.

    count son los valores que hay y missing los que faltan; una etiqueta sin ningún valor
    tiene count 0 y NaN en mean, minimum y maximum.
    """
    # sort=False: las etiquetas salen en el orden en que aparecen, como en Series.means.
    # Cada columna nueva es (columna de partida, función): count="count" no basta.
    table = frame.groupby("label", sort=False).agg(
        count=("value", "count"),
        size=("value", "size"),
        mean=("value", "mean"),
        minimum=("value", "min"),
        maximum=("value", "max"),
    )
    # size cuenta las filas y count solo los valores: la resta son los NaN de cada etiqueta.
    # La tabla es nueva, de agg: cambiarla aquí no toca la de nadie.
    table.insert(1, "missing", table.pop("size") - table["count"])
    return table


def compare(before: pd.DataFrame, after: pd.DataFrame) -> pd.DataFrame:
    """Las medias de dos resúmenes por etiqueta (before, after) y su diferencia (change).

    Salen todas las etiquetas de los dos, por orden alfabético: la que solo está en uno
    tiene NaN en el otro y en change.
    """
    # validate: cada etiqueta está una sola vez en cada resumen; si no, merge lanza
    # MergeError en lugar de multiplicar filas en silencio.
    joined = pd.merge(
        before["mean"].rename("before"),
        after["mean"].rename("after"),
        on="label",
        how="outer",
        validate="one_to_one",
    )
    return joined.assign(change=joined["after"] - joined["before"])


def duration(text: str) -> timedelta:
    """Una duración escrita como en pandas ("1h", "90min", "1D") como timedelta.

    Lanza ValueError si el texto no es una duración o si no es mayor que cero.
    """
    problem = ValueError(f"no es una duración mayor que cero: {text!r}")
    try:
        value = pd.Timedelta(text)
    except ValueError as error:
        raise problem from error
    # Un texto vacío da NaT ("not a time") en lugar de un error: también se rechaza.
    if pd.isna(value) or value <= pd.Timedelta(0):
        raise problem
    return value.to_pytimedelta()


def timed(frame: pd.DataFrame, start: datetime, every: timedelta) -> pd.DataFrame:
    """Una copia con índice de tiempo (time): la primera medida en start y otra cada every."""
    return frame.set_axis(pd.date_range(start, periods=len(frame), freq=every, name="time"))


def evolution(frame: pd.DataFrame, period: timedelta) -> pd.DataFrame:
    """La media de cada etiqueta en cada periodo: una fila por periodo, una columna por etiqueta.

    frame necesita índice de tiempo (timed). Cada fila es el inicio de su periodo, contado
    desde la medianoche del primer día; un periodo sin valores de una etiqueta queda en NaN.
    """
    # pivot pasa cada etiqueta a una columna (por orden alfabético); resample agrupa las
    # filas por periodos, incluidos los que no tienen ninguna medida.
    return frame.pivot(columns="label", values="value").resample(period).mean()
