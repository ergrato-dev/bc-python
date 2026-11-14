"""Árboles y ensembles frente al modelo lineal y la referencia, en los mismos pliegues.

Qué: compete mide cinco modelos (la referencia, el lineal, un árbol, un bosque y un
gradient boosting) con la misma preparación y los mismos pliegues de validation, y dice
cuál tiene la mejor media y en cuántos pliegues gana cada uno a la referencia.
Para qué: un modelo más flexible no es mejor por serlo; solo lo es si gana, pliegue a
pliegue, con tus datos.
Impacto: importa pandas y scikit-learn: core/__init__.py no lo reexporta, y la CLI lo
importa solo en `competir`.
"""

from dataclasses import dataclass
from statistics import mean
from typing import Literal

import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import (
    HistGradientBoostingClassifier,
    HistGradientBoostingRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

from observatorio.core.learning import SEED
from observatorio.core.validation import INPUTS, folds, ordered, prepare

BASELINE = "referencia"
# Profundidad del árbol y hojas mínimas del bosque: sin límite, los dos memorizan el ruido.
DEPTH = 4
LEAF = 5
TREES = 100


@dataclass(frozen=True)
class Contest:
    """La métrica de cada modelo en cada pliegue; la referencia, con su nombre."""

    task: str
    metric: str
    higher_is_better: bool
    scores: dict[str, tuple[float, ...]]

    @property
    def means(self) -> dict[str, float]:
        """La media de los pliegues de cada modelo, en el orden de scores."""
        return {name: mean(values) for name, values in self.scores.items()}

    @property
    def wins(self) -> dict[str, int]:
        """En cuántos pliegues gana cada modelo a la referencia. Empatar no es ganar."""
        baseline = self.scores[BASELINE]
        sign = 1 if self.higher_is_better else -1
        return {
            name: sum(
                sign * (score - other) > 0 for score, other in zip(values, baseline, strict=True)
            )
            for name, values in self.scores.items()
            if name != BASELINE
        }

    @property
    def best(self) -> str:
        """El modelo con la mejor media; en un empate, el primero (el más sencillo)."""
        means = self.means
        pick = max if self.higher_is_better else min
        return pick(means, key=means.__getitem__)

    @property
    def improves(self) -> bool:
        """Si el mejor no es la referencia y le gana en todos los pliegues."""
        best = self.best
        return best != BASELINE and self.wins[best] == len(self.scores[BASELINE])


def candidates(target: Literal["valor", "nivel"]) -> dict[str, BaseEstimator]:
    """Los cinco modelos, de más sencillo a más flexible, con la semilla fija."""
    if target == "valor":
        return {
            BASELINE: DummyRegressor(strategy="mean"),
            "lineal": Ridge(),
            "árbol": DecisionTreeRegressor(max_depth=DEPTH, random_state=SEED),
            "bosque": RandomForestRegressor(TREES, min_samples_leaf=LEAF, random_state=SEED),
            "boosting": HistGradientBoostingRegressor(random_state=SEED),
        }
    return {
        BASELINE: DummyClassifier(strategy="most_frequent"),
        "lineal": LogisticRegression(),
        "árbol": DecisionTreeClassifier(max_depth=DEPTH, random_state=SEED),
        "bosque": RandomForestClassifier(TREES, min_samples_leaf=LEAF, random_state=SEED),
        "boosting": HistGradientBoostingClassifier(random_state=SEED),
    }


def compete(
    frame: pd.DataFrame,
    target: Literal["valor", "nivel"],
    n_splits: int = 5,
    by_time: bool = False,
) -> Contest:
    """Mide los cinco modelos del valor (MAE) o del nivel (exactitud equilibrada) con los
    mismos pliegues y la misma preparación."""
    rows = ordered(frame)
    x, y = rows[INPUTS], rows[target]
    if target == "valor":
        task, metric, scoring = "regresión del valor", "MAE", "neg_mean_absolute_error"
    else:
        task, metric = "clasificación del nivel", "exactitud equilibrada"
        scoring = "balanced_accuracy"
    sign = -1 if target == "valor" else 1
    scores = {}
    for name, model in candidates(target).items():
        pipeline = Pipeline([("prepare", prepare()), ("model", model)])
        values = cross_val_score(pipeline, x, y, scoring=scoring, cv=folds(n_splits, by_time))
        scores[name] = tuple(float(sign * value) for value in values)
    return Contest(task, metric, target != "valor", scores)
