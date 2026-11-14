"""Validación cruzada de un modelo ajustado, con todo el preprocesado dentro del pipeline.

Qué: validate prepara las entradas (la etiqueta en one-hot y la posición escalada) dentro de
un Pipeline, elige la fuerza de la regularización con GridSearchCV y mide el resultado en
varios pliegues, cada uno frente a un modelo Dummy medido en los mismos pliegues.
Para qué: un solo reparto da un número que cambia con la semilla; varios pliegues dicen si
la mejora se repite o fue suerte. El ajuste va dentro de cada pliegue (validación anidada):
si eligiera la regularización mirando los pliegues con los que se mide, la medida saldría
optimista.
Impacto: importa pandas y scikit-learn: core/__init__.py no lo reexporta, y la CLI lo
importa solo en `validar`.
"""

from dataclasses import dataclass
from typing import Literal

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.model_selection import GridSearchCV, KFold, TimeSeriesSplit, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from observatorio.core.learning import SEED, known

# El orden en el tiempo: la carga y, dentro de ella, la posición de cada medida.
ORDER = ["carga", "posicion"]
INPUTS = ["etiqueta", "posicion"]
# Los valores que se prueban para alpha (Ridge) y C (logística), de diez en diez. Van al
# revés: alpha alto regulariza mucho; C alto, poco.
STRENGTHS = [0.01, 0.1, 1.0, 10.0, 100.0]


@dataclass(frozen=True)
class CrossValidation:
    """Una métrica en cada pliegue: la del modelo ajustado y la de la referencia."""

    task: str
    metric: str
    higher_is_better: bool
    model: tuple[float, ...]
    baseline: tuple[float, ...]
    params: dict[str, float]

    @property
    def beats(self) -> tuple[bool, ...]:
        """Si el modelo es mejor que la referencia en cada pliegue. Empatar no es ganar."""
        pairs = zip(self.model, self.baseline, strict=True)
        if self.higher_is_better:
            return tuple(model > baseline for model, baseline in pairs)
        return tuple(model < baseline for model, baseline in pairs)

    @property
    def improves(self) -> bool:
        """Solo si gana en todos los pliegues: una mejora que no se repite puede ser suerte."""
        return all(self.beats)


def ordered(frame: pd.DataFrame) -> pd.DataFrame:
    """Las medidas con valor, en el orden en que llegaron: carga y posición."""
    missing = set(ORDER) - set(frame.columns)
    if missing:
        raise ValueError(f"a la instantánea le faltan las columnas {', '.join(sorted(missing))}")
    return known(frame).sort_values(ORDER, kind="stable")


def prepare() -> ColumnTransformer:
    """La etiqueta en one-hot y la posición escalada. Sin ajustar: cada pliegue lo ajusta
    con su entrenamiento, y una etiqueta que no vio da una fila de ceros, no un error."""
    return ColumnTransformer(
        [
            ("etiqueta", OneHotEncoder(handle_unknown="ignore"), ["etiqueta"]),
            ("posicion", StandardScaler(), ["posicion"]),
        ]
    )


def folds(n_splits: int, by_time: bool) -> KFold | TimeSeriesSplit:
    """Pliegues al azar, con la semilla, o por tiempo: cada prueba, después de su
    entrenamiento."""
    if by_time:
        return TimeSeriesSplit(n_splits=n_splits)
    return KFold(n_splits=n_splits, shuffle=True, random_state=SEED)


def validate(
    frame: pd.DataFrame,
    target: Literal["valor", "nivel"],
    n_splits: int = 5,
    by_time: bool = False,
) -> CrossValidation:
    """Ajusta y mide el modelo del valor (Ridge, con MAE) o del nivel (logística, con
    exactitud equilibrada) en cada pliegue, junto a su referencia."""
    rows = ordered(frame)
    if target == "valor":
        task, metric, scoring = "regresión del valor", "MAE", "neg_mean_absolute_error"
        model, grid = Ridge(), {"model__alpha": STRENGTHS}
        baseline: DummyRegressor | DummyClassifier = DummyRegressor(strategy="mean")
    else:
        task, metric = "clasificación del nivel", "exactitud equilibrada"
        scoring = "balanced_accuracy"
        model, grid = LogisticRegression(), {"model__C": STRENGTHS}
        baseline = DummyClassifier(strategy="most_frequent")
    x, y = rows[INPUTS], rows[target]
    pipeline = Pipeline([("prepare", prepare()), ("model", model)])
    search = GridSearchCV(pipeline, grid, scoring=scoring, cv=folds(n_splits, by_time))
    # Validación anidada: en cada pliegue, GridSearchCV elige con su entrenamiento.
    tuned = cross_val_score(search, x, y, scoring=scoring, cv=folds(n_splits, by_time))
    guessed = cross_val_score(baseline, x, y, scoring=scoring, cv=folds(n_splits, by_time))
    # scikit-learn da los errores en negativo, para que más sea siempre mejor: aquí, en positivo.
    sign = -1 if target == "valor" else 1
    params = search.fit(x, y).best_params_
    return CrossValidation(
        task,
        metric,
        target != "valor",
        tuple(float(sign * score) for score in tuned),
        tuple(float(sign * score) for score in guessed),
        {name.removeprefix("model__"): value for name, value in params.items()},
    )
