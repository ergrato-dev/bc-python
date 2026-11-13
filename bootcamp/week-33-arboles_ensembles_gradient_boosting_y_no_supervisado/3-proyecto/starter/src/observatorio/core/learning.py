"""Un modelo predictivo de la instantánea, juzgado contra una referencia que no sabe nada.

Qué: split separa las medidas con valor en entrenamiento y prueba, regress predice el valor
con una regresión lineal y classify el nivel con una regresión logística; las dos usan solo
la etiqueta, y cada métrica se compara con la de un modelo Dummy que ignora las entradas.
Para qué: un modelo solo aporta si predice mejor que no saber nada. La media de todo (para
el valor) o el nivel más frecuente (para el nivel) son ese "no saber nada": si tu modelo no
los mejora en medidas que no vio al entrenar, no ha aprendido nada útil de tus datos.
Impacto: importa pandas y scikit-learn: core/__init__.py no lo reexporta, y la CLI lo
importa solo en `modelo`.
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    mean_absolute_error,
    r2_score,
    root_mean_squared_error,
)
from sklearn.model_selection import train_test_split

COLUMNS = {"etiqueta", "valor", "nivel"}
# La semilla por defecto: el mismo reparto en cada ejecución, y en los tests.
SEED = 31


@dataclass(frozen=True)
class Score:
    """Una métrica en las medidas de prueba: la del modelo y la de la referencia."""

    name: str
    model: float
    baseline: float
    higher_is_better: bool

    @property
    def improves(self) -> bool:
        """Si el modelo es mejor que la referencia en esta métrica. Empatar no es mejorar."""
        if self.higher_is_better:
            return self.model > self.baseline
        return self.model < self.baseline


@dataclass(frozen=True)
class Evaluation:
    """Un modelo evaluado: la primera métrica es la que decide."""

    task: str
    train_size: int
    test_size: int
    scores: tuple[Score, ...]

    @property
    def improves(self) -> bool:
        return self.scores[0].improves


def known(frame: pd.DataFrame) -> pd.DataFrame:
    """Las medidas con valor: sin él no hay nada que predecir ni que comparar.

    Lanza ValueError si faltan columnas, o si algún nivel tiene menos de dos medidas: el
    reparto estratificado necesita al menos una en entrenamiento y otra en prueba.
    """
    missing = COLUMNS - set(frame.columns)
    if missing:
        raise ValueError(f"a la instantánea le faltan las columnas {', '.join(sorted(missing))}")
    rows = frame[frame["valor"].notna()]
    counts = rows["nivel"].value_counts()
    if len(counts) < 2 or counts.min() < 2:
        raise ValueError("hacen falta dos niveles, cada uno con al menos dos medidas con valor")
    return rows


def features(frame: pd.DataFrame) -> pd.DataFrame:
    """Las entradas del modelo: una columna 0/1 por etiqueta. Nunca el valor ni el nivel:
    son lo que se predice."""
    return pd.get_dummies(frame["etiqueta"], dtype="float64")


def split(
    frame: pd.DataFrame, test_size: float = 0.25, seed: int = SEED
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Entrenamiento y prueba, con la misma proporción de cada nivel en las dos partes."""
    rows = known(frame)
    train, test = train_test_split(
        rows, test_size=test_size, random_state=seed, stratify=rows["nivel"]
    )
    return train, test


def regress(frame: pd.DataFrame, test_size: float = 0.25, seed: int = SEED) -> Evaluation:
    """Predice el valor de cada medida de prueba; la referencia predice siempre la media."""
    train, test = split(frame, test_size, seed)
    x = features(known(frame))
    x_train, x_test = x.loc[train.index], x.loc[test.index]
    y_train, y_test = train["valor"], test["valor"]
    model = LinearRegression().fit(x_train, y_train)
    baseline = DummyRegressor(strategy="mean").fit(x_train, y_train)
    predicted, guessed = model.predict(x_test), baseline.predict(x_test)
    scores = (
        Score(
            "MAE",
            mean_absolute_error(y_test, predicted),
            mean_absolute_error(y_test, guessed),
            False,
        ),
        Score(
            "RMSE",
            root_mean_squared_error(y_test, predicted),
            root_mean_squared_error(y_test, guessed),
            False,
        ),
        Score("R²", r2_score(y_test, predicted), r2_score(y_test, guessed), True),
    )
    return Evaluation("regresión del valor", len(train), len(test), scores)


def classify(frame: pd.DataFrame, test_size: float = 0.25, seed: int = SEED) -> Evaluation:
    """Predice el nivel de cada medida de prueba; la referencia predice el más frecuente."""
    train, test = split(frame, test_size, seed)
    x = features(known(frame))
    x_train, x_test = x.loc[train.index], x.loc[test.index]
    y_train, y_test = train["nivel"].to_numpy(), test["nivel"].to_numpy()
    model = LogisticRegression().fit(x_train, y_train)
    baseline = DummyClassifier(strategy="most_frequent").fit(x_train, y_train)
    predicted: np.ndarray = model.predict(x_test)
    guessed: np.ndarray = baseline.predict(x_test)
    scores = (
        # Equilibrada primero: la exactitud premia acertar siempre el nivel más frecuente.
        Score(
            "exactitud equilibrada",
            balanced_accuracy_score(y_test, predicted),
            balanced_accuracy_score(y_test, guessed),
            True,
        ),
        Score(
            "exactitud",
            accuracy_score(y_test, predicted),
            accuracy_score(y_test, guessed),
            True,
        ),
        Score(
            "F1 macro",
            f1_score(y_test, predicted, average="macro", zero_division=0),
            f1_score(y_test, guessed, average="macro", zero_division=0),
            True,
        ),
    )
    return Evaluation("clasificación del nivel", len(train), len(test), scores)
