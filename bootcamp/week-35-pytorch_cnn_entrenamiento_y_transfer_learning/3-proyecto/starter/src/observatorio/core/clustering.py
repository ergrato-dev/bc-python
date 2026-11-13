"""Grupos de etiquetas que se parecen, sin decirle al modelo cuáles son.

Qué: profiles resume cada etiqueta (media, mediana y desviación de sus valores) y cluster
reparte esos perfiles en k grupos con KMeans, después de escalarlos, y mide con la
silueta lo separados que quedan.
Para qué: es aprendizaje no supervisado: no hay una respuesta que acertar. KMeans siempre
devuelve k grupos, también con datos sin estructura; la silueta dice si merecen ese nombre.
Impacto: importa pandas y scikit-learn: core/__init__.py no lo reexporta, y la CLI lo
importa solo en `agrupar`.
"""

from dataclasses import dataclass

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from observatorio.core.learning import SEED

# Desde qué silueta se habla de grupos separados: de -1 (mal repartidos) a 1 (muy separados).
SEPARATED = 0.5


@dataclass(frozen=True)
class Clustering:
    """El grupo de cada etiqueta, numerado desde 1 por orden alfabético, y la silueta."""

    groups: dict[str, int]
    silhouette: float

    @property
    def separated(self) -> bool:
        """Si la silueta llega a SEPARATED: por debajo, los grupos se solapan."""
        return self.silhouette >= SEPARATED


def profiles(frame: pd.DataFrame) -> pd.DataFrame:
    """Una fila por etiqueta, en orden alfabético: la media, la mediana y la desviación de
    sus valores, sin las medidas que no lo tienen. Con una sola medida no hay desviación: 0."""
    table = (
        frame.dropna(subset=["valor"])
        .groupby("etiqueta")
        .agg(media=("valor", "mean"), mediana=("valor", "median"), desviacion=("valor", "std"))
    )
    return table.fillna({"desviacion": 0.0})


def cluster(frame: pd.DataFrame, k: int = 2) -> Clustering:
    """Reparte las etiquetas en k grupos con KMeans sobre sus perfiles escalados."""
    table = profiles(frame)
    if not 2 <= k < len(table):
        raise ValueError(f"con {len(table)} etiquetas, los grupos van de 2 a {len(table) - 1}")
    # Escalar: si no, la columna con números más grandes decidiría sola las distancias.
    pipeline = make_pipeline(StandardScaler(), KMeans(k, n_init=10, random_state=SEED))
    found = pipeline.fit_predict(table)
    silhouette = float(silhouette_score(pipeline[:-1].transform(table), found))
    # KMeans numera los grupos al azar: aquí, por orden de aparición, para que no cambien.
    numbers: dict[int, int] = {}
    for group in found:
        numbers.setdefault(int(group), len(numbers) + 1)
    groups = {str(label): numbers[int(group)] for label, group in zip(table.index, found)}
    return Clustering(groups, silhouette)
