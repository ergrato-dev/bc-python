"""Tests de la semana 31: un modelo de la instantánea, juzgado contra una referencia.

Qué: comprueban core/learning.py (las medidas que se usan, las entradas del modelo, el
reparto en entrenamiento y prueba, la regresión del valor y la clasificación del nivel) y
el comando `modelo`.
Para qué: un error en un modelo no rompe nada: da un número que parece bueno. Si se cuela el
valor entre las entradas, si una medida está a la vez en entrenamiento y en prueba, o si la
referencia no es la que dice, el modelo "mejora" sin haber aprendido nada.
Impacto: learning.py no se reexporta en core: la CLI arranca sin cargar scikit-learn.
"""

import hashlib
import math
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from sklearn.metrics import mean_absolute_error
from typer.testing import CliRunner

import observatorio.core
from observatorio import cli
from observatorio.core.learning import (
    SEED,
    Evaluation,
    Score,
    classify,
    features,
    known,
    regress,
    split,
)

runner = CliRunner()


def level_of(value: float) -> str:
    """Los niveles de la semana 2, con los umbrales del starter: 10 y 50."""
    if math.isnan(value):
        return "sin dato"
    return "bajo" if value < 10 else "medio" if value < 50 else "alto"


def frame_of(rows: list[tuple[str, float]]) -> pd.DataFrame:
    values = [value for _, value in rows]
    return pd.DataFrame(
        {
            "etiqueta": [label for label, _ in rows],
            "valor": values,
            "nivel": [level_of(value) for value in values],
        }
    )


def signal() -> pd.DataFrame:
    """La etiqueta decide el valor: Norte, bajo; Sur, medio; Centro, alto. Con ruido, y
    con algunas medidas sin valor. Un modelo que solo ve la etiqueta puede acertar."""
    rng = np.random.default_rng(1)
    centers = {"Norte": 5.0, "Sur": 30.0, "Centro": 70.0}
    rows = [
        (label, float(round(rng.normal(center, 2.0), 1)))
        for label, center in centers.items()
        for _ in range(40)
    ]
    rows += [("Norte", math.nan), ("Sur", math.nan), ("Centro", math.nan)]
    return frame_of(rows)


def write(tmp_path: Path, frame: pd.DataFrame) -> Path:
    path = tmp_path / "instantanea.csv"
    frame.to_csv(path, index=False, lineterminator="\n")
    return path


# --- Score y Evaluation ---------------------------------------------------------------


def test_score_higher_is_better() -> None:
    assert Score("exactitud", 0.8, 0.5, True).improves
    assert not Score("exactitud", 0.4, 0.5, True).improves


def test_score_lower_is_better() -> None:
    assert Score("MAE", 2.0, 3.0, False).improves
    assert not Score("MAE", 4.0, 3.0, False).improves


@pytest.mark.parametrize("higher_is_better", [True, False])
def test_a_tie_is_not_an_improvement(higher_is_better: bool) -> None:
    assert not Score("x", 0.5, 0.5, higher_is_better).improves


def test_the_first_score_decides() -> None:
    better = Score("MAE", 1.0, 2.0, False)
    worse = Score("R²", 0.1, 0.2, True)
    assert Evaluation("t", 3, 1, (better, worse)).improves
    assert not Evaluation("t", 3, 1, (worse, better)).improves


def test_score_and_evaluation_are_frozen() -> None:
    score = Score("MAE", 1.0, 2.0, False)
    with pytest.raises(AttributeError):
        score.model = 0.0  # type: ignore[misc]


# --- known ----------------------------------------------------------------------------


def test_known_drops_the_measures_without_value() -> None:
    rows = known(signal())
    assert len(rows) == 120
    assert rows["valor"].notna().all()
    assert "sin dato" not in set(rows["nivel"])


def test_known_names_the_missing_columns() -> None:
    frame = signal().drop(columns=["nivel", "valor"])
    with pytest.raises(ValueError, match="faltan las columnas nivel, valor"):
        known(frame)


def test_known_needs_two_levels() -> None:
    frame = frame_of([("Norte", 20.0), ("Sur", 30.0), ("Sur", math.nan)])
    with pytest.raises(ValueError, match="dos niveles"):
        known(frame)


def test_known_needs_two_measures_of_each_level() -> None:
    frame = frame_of([("Norte", 20.0), ("Sur", 30.0), ("Centro", 70.0)])
    with pytest.raises(ValueError, match="al menos dos medidas"):
        known(frame)


# --- features -------------------------------------------------------------------------


def test_features_has_one_column_per_label_in_order() -> None:
    assert list(features(signal()).columns) == ["Centro", "Norte", "Sur"]


def test_features_are_zeros_and_ones() -> None:
    x = features(signal())
    assert set(np.unique(x.to_numpy())) == {0.0, 1.0}
    assert (x.sum(axis=1) == 1).all()
    assert (x.dtypes == "float64").all()


def test_features_never_include_what_is_predicted() -> None:
    columns = set(features(signal()).columns)
    assert not columns & {"valor", "nivel"}


def test_features_mark_the_label_of_each_row() -> None:
    frame = frame_of([("Sur", 30.0), ("Norte", 5.0)])
    assert features(frame).to_dict("list") == {"Norte": [0.0, 1.0], "Sur": [1.0, 0.0]}


# --- split ----------------------------------------------------------------------------


def test_split_sizes() -> None:
    train, test = split(signal(), test_size=0.25)
    assert (len(train), len(test)) == (90, 30)


def test_split_parts_are_disjoint_and_cover_every_known_row() -> None:
    train, test = split(signal())
    assert not set(train.index) & set(test.index)
    assert set(train.index) | set(test.index) == set(known(signal()).index)


def test_split_keeps_the_proportion_of_each_level() -> None:
    _, test = split(signal(), test_size=0.25)
    assert test["nivel"].value_counts().to_dict() == {"bajo": 10, "medio": 10, "alto": 10}


def test_split_is_the_same_with_the_same_seed() -> None:
    first, second = split(signal(), seed=7)[1], split(signal(), seed=7)[1]
    assert list(first.index) == list(second.index)


def test_split_changes_with_another_seed() -> None:
    assert list(split(signal(), seed=7)[1].index) != list(split(signal(), seed=8)[1].index)


def test_split_default_seed() -> None:
    assert SEED == 31
    assert list(split(signal())[1].index) == list(split(signal(), seed=31)[1].index)


@settings(max_examples=30, deadline=None)
@given(st.floats(min_value=0.1, max_value=0.5), st.integers(min_value=0, max_value=10_000))
def test_split_never_loses_or_repeats_a_row(test_size: float, seed: int) -> None:
    train, test = split(signal(), test_size, seed)
    assert len(train) + len(test) == 120
    assert len(test) == math.ceil(120 * test_size)
    assert sorted([*train.index, *test.index]) == sorted(known(signal()).index)


# --- regress --------------------------------------------------------------------------


def test_regress_scores_in_order() -> None:
    result = regress(signal())
    assert [s.name for s in result.scores] == ["MAE", "RMSE", "R²"]
    assert [s.higher_is_better for s in result.scores] == [False, False, True]


def test_regress_sizes() -> None:
    result = regress(signal())
    assert (result.task, result.train_size, result.test_size) == ("regresión del valor", 90, 30)


def test_regress_improves_when_the_label_decides_the_value() -> None:
    result = regress(signal())
    mae, _, r2 = result.scores
    assert result.improves
    assert mae.model < 2.5
    assert mae.baseline > 20
    assert r2.model > 0.95


def test_regress_baseline_predicts_the_mean_of_training() -> None:
    frame = signal()
    train, test = split(frame)
    by_hand = mean_absolute_error(test["valor"], np.full(len(test), train["valor"].mean()))
    assert regress(frame).scores[0].baseline == pytest.approx(by_hand)


def test_regress_model_learns_only_from_training() -> None:
    # Con solo la etiqueta, la regresión predice la media de cada una en el entrenamiento.
    frame = signal()
    train, test = split(frame)
    means = train.groupby("etiqueta")["valor"].mean()
    by_hand = mean_absolute_error(test["valor"], test["etiqueta"].map(means))
    assert regress(frame).scores[0].model == pytest.approx(by_hand)


def test_regress_baseline_r2_is_about_zero() -> None:
    assert regress(signal()).scores[2].baseline == pytest.approx(0, abs=0.1)


def test_regress_rmse_is_never_below_mae() -> None:
    mae, rmse, _ = regress(signal()).scores
    assert rmse.model >= mae.model
    assert rmse.baseline >= mae.baseline


def test_regress_uses_the_test_size_and_seed() -> None:
    assert regress(signal(), test_size=0.5).test_size == 60
    assert regress(signal(), seed=7) != regress(signal(), seed=8)


# --- classify -------------------------------------------------------------------------


def test_classify_scores_in_order() -> None:
    result = classify(signal())
    assert [s.name for s in result.scores] == ["exactitud equilibrada", "exactitud", "F1 macro"]
    assert all(s.higher_is_better for s in result.scores)


def test_classify_sizes() -> None:
    result = classify(signal())
    assert (result.task, result.train_size, result.test_size) == (
        "clasificación del nivel",
        90,
        30,
    )


def test_classify_improves_when_the_label_decides_the_level() -> None:
    result = classify(signal())
    assert result.improves
    assert [s.model for s in result.scores] == [1.0, 1.0, 1.0]


def test_classify_baseline_guesses_the_most_frequent_level() -> None:
    # 30 de cada nivel en la prueba: acertar siempre el mismo es acertar uno de cada tres.
    balanced, accuracy, f1 = classify(signal()).scores
    assert balanced.baseline == pytest.approx(1 / 3)
    assert accuracy.baseline == pytest.approx(1 / 3)
    assert f1.baseline == pytest.approx((2 * (1 / 3) / (1 + 1 / 3)) / 3)


def test_classify_balanced_accuracy_sees_through_an_unbalanced_level() -> None:
    # Nueve de cada diez medidas son de nivel medio, y la etiqueta no dice nada: la
    # exactitud de la referencia es alta, la equilibrada no.
    rng = np.random.default_rng(2)
    values = [30.0] * 180 + [5.0] * 10 + [70.0] * 10
    labels = rng.choice(["Norte", "Sur"], size=len(values))
    frame = frame_of(list(zip(labels.tolist(), values, strict=True)))
    balanced, accuracy, _ = classify(frame).scores
    assert accuracy.baseline == pytest.approx(0.9)
    assert balanced.baseline == pytest.approx(1 / 3)
    # F1 macro: la media de las tres clases, con el mismo peso; solo "medio" no es 0. El
    # modelo tampoco aprende nada, y dice siempre "medio" como la referencia.
    f1 = classify(frame).scores[2]
    assert f1.model == f1.baseline == pytest.approx((2 * 0.9 / 1.9) / 3)


def test_classify_does_not_see_the_value() -> None:
    # El valor decide el nivel, la etiqueta no dice nada. Con el valor entre las entradas,
    # el modelo acertaría siempre; sin él, no puede.
    rng = np.random.default_rng(3)
    values = rng.uniform(0, 80, 300).round(1)
    labels = rng.choice(["Norte", "Sur", "Centro"], size=300)
    frame = frame_of(list(zip(labels.tolist(), values.tolist(), strict=True)))
    assert classify(frame).scores[0].model < 0.6


def test_classify_and_regress_test_the_same_measures() -> None:
    assert classify(signal()).test_size == regress(signal()).test_size
    assert classify(signal(), test_size=0.4).test_size == 48


# --- el comando modelo ----------------------------------------------------------------


def test_modelo_prints_the_data_both_tables_and_both_verdicts(tmp_path: Path) -> None:
    path = write(tmp_path, signal())
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    result = runner.invoke(cli.app, ["modelo", str(path)])
    assert result.exit_code == 0, result.output
    assert f"instantanea.csv: 123 medidas · sha256: {digest}" in result.output
    assert "regresión del valor · 90 para entrenar, 30 para probar" in result.output
    assert "clasificación del nivel · 90 para entrenar, 30 para probar" in result.output
    assert "regresión del valor: el modelo mejora la referencia" in result.output
    assert "clasificación del nivel: el modelo mejora la referencia" in result.output


def test_modelo_shows_each_score_with_three_decimals(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["modelo", str(write(tmp_path, signal()))])
    accuracy = next(s for s in classify(signal()).scores if s.name == "exactitud")
    assert f"{accuracy.baseline:.3f}" in result.output
    for name in ["MAE", "RMSE", "R²", "exactitud equilibrada", "F1 macro"]:
        assert name in result.output


def test_modelo_says_when_it_does_not_improve(tmp_path: Path) -> None:
    rng = np.random.default_rng(4)
    values = [30.0] * 60 + [5.0] * 4 + [70.0] * 4
    labels = rng.choice(["Norte", "Sur"], size=len(values))
    frame = frame_of(list(zip(labels.tolist(), values, strict=True)))
    result = runner.invoke(cli.app, ["modelo", str(write(tmp_path, frame))])
    assert "clasificación del nivel: el modelo no mejora la referencia" in result.output
    assert re.search(r"exactitud equilibrada .*│ no +│", result.output)


def test_modelo_passes_the_test_size_and_seed(tmp_path: Path) -> None:
    path = str(write(tmp_path, signal()))
    result = runner.invoke(cli.app, ["modelo", path, "--prueba", "0.5", "--semilla", "7"])
    assert "60 para entrenar, 60 para probar" in result.output
    assert f"{regress(signal(), 0.5, 7).scores[0].model:.3f}" in result.output


def test_modelo_checks_the_digest(tmp_path: Path) -> None:
    path = write(tmp_path, signal())
    result = runner.invoke(cli.app, ["modelo", str(path), "--huella", "0000"])
    assert result.exit_code == 1
    assert "no 0000" in result.output


def test_modelo_without_the_level_column(tmp_path: Path) -> None:
    path = write(tmp_path, signal().drop(columns=["nivel"]))
    result = runner.invoke(cli.app, ["modelo", str(path)])
    assert result.exit_code == 1
    assert "faltan las columnas nivel" in result.output


def test_modelo_without_the_file(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["modelo", str(tmp_path / "no.csv")])
    assert result.exit_code == 2
    assert "no se puede leer" in result.output


@pytest.mark.parametrize("value", ["0.05", "0.6"])
def test_modelo_rejects_a_test_size_out_of_range(tmp_path: Path, value: str) -> None:
    path = str(write(tmp_path, signal()))
    assert runner.invoke(cli.app, ["modelo", path, "--prueba", value]).exit_code == 2


def test_learning_is_not_reexported_in_core() -> None:
    assert "learning" not in observatorio.core.__all__
    assert not hasattr(observatorio.core, "regress")


def test_importing_the_cli_does_not_load_sklearn() -> None:
    # En otro proceso: en este, los tests de arriba ya han importado scikit-learn.
    code = "import sys, observatorio.cli; print('sklearn' in sys.modules)"
    result = subprocess.run(
        [sys.executable, "-c", code], check=False, capture_output=True, text=True
    )
    assert result.stdout == "False\n"
