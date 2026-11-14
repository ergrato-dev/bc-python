"""Tests de la semana 33: árboles y ensembles frente al lineal y la referencia.

Qué: comprueban core/ensembles.py (el resultado de la competición, los cinco modelos y la
medida de cada uno con los mismos pliegues) y el comando `competir`.
Para qué: comparar modelos solo es justo si todos se miden con los mismos pliegues y la
misma preparación, y si "el mejor" se decide con la media pero solo "mejora" cuando gana a
la referencia en todos los pliegues. Un árbol sin límite de profundidad o un bosque sin
semilla dan números que no se repiten.
Impacto: ensembles.py no se reexporta en core: la CLI arranca sin cargar scikit-learn.
"""

import hashlib
import re
from dataclasses import FrozenInstanceError
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.base import is_classifier, is_regressor
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold, TimeSeriesSplit, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeRegressor
from test_validation import frame_of, noise, signal, write
from typer.testing import CliRunner

import observatorio.core
from observatorio import cli
from observatorio.core import ensembles
from observatorio.core.ensembles import (
    BASELINE,
    DEPTH,
    LEAF,
    TREES,
    Contest,
    candidates,
    compete,
)
from observatorio.core.learning import SEED
from observatorio.core.validation import INPUTS, ordered, prepare

runner = CliRunner()
NAMES = [BASELINE, "lineal", "árbol", "bosque", "boosting"]


def bump(size: int = 120) -> pd.DataFrame:
    """El valor depende de la posición, pero no en línea recta: alto en el tercio del
    medio y bajo en los otros dos. Una recta no puede dibujarlo; un árbol, sí."""
    rng = np.random.default_rng(3)
    labels = ["Norte", "Sur", "Centro"]
    rows = []
    for position in range(size):
        center = 60.0 if size // 3 <= position < 2 * size // 3 else 10.0
        rows.append((labels[position % 3], float(round(rng.normal(center, 2.0), 1))))
    return frame_of(rows)


def contest(higher: bool, **scores: tuple[float, ...]) -> Contest:
    return Contest("tarea", "métrica", higher, scores)


# --- Contest ---


def test_means_keep_the_order_of_the_scores() -> None:
    result = contest(False, referencia=(4.0, 6.0), lineal=(1.0, 2.0), árbol=(3.0, 3.0))
    assert result.means == {BASELINE: 5.0, "lineal": 1.5, "árbol": 3.0}
    assert list(result.means) == [BASELINE, "lineal", "árbol"]


def test_wins_when_lower_is_better() -> None:
    result = contest(False, referencia=(5.0, 5.0, 5.0), lineal=(4.0, 6.0, 1.0))
    assert result.wins == {"lineal": 2}


def test_wins_when_higher_is_better() -> None:
    result = contest(True, referencia=(0.5, 0.5, 0.5), lineal=(0.4, 0.6, 0.9))
    assert result.wins == {"lineal": 2}


@pytest.mark.parametrize("higher", [True, False])
def test_a_tie_is_not_a_win(higher: bool) -> None:
    assert contest(higher, referencia=(1.0,), lineal=(1.0,)).wins == {"lineal": 0}


def test_wins_leave_out_the_baseline() -> None:
    result = contest(True, referencia=(0.5,), lineal=(0.6,), bosque=(0.4,))
    assert result.wins == {"lineal": 1, "bosque": 0}


def test_best_when_lower_is_better() -> None:
    result = contest(False, referencia=(5.0,), lineal=(4.0,), bosque=(3.0,))
    assert result.best == "bosque"


def test_best_when_higher_is_better() -> None:
    result = contest(True, referencia=(0.5,), lineal=(0.9,), bosque=(0.7,))
    assert result.best == "lineal"


def test_best_in_a_tie_is_the_first() -> None:
    result = contest(True, referencia=(0.5,), lineal=(1.0,), bosque=(1.0,))
    assert result.best == "lineal"


def test_best_can_be_the_baseline() -> None:
    result = contest(False, referencia=(1.0,), lineal=(2.0,))
    assert result.best == BASELINE
    assert not result.improves


def test_improves_only_when_the_best_wins_every_fold() -> None:
    assert contest(False, referencia=(5.0, 5.0), lineal=(4.0, 4.0)).improves
    # La mejor media, pero pierde en un pliegue.
    assert not contest(False, referencia=(5.0, 5.0), lineal=(1.0, 6.0)).improves


def test_improves_looks_at_the_best_not_at_any_model() -> None:
    # lineal gana en todos los pliegues, pero bosque tiene mejor media y pierde en uno.
    result = contest(False, referencia=(5.0, 5.0), lineal=(4.0, 4.0), bosque=(0.0, 6.0))
    assert result.best == "bosque"
    assert not result.improves


def test_contest_is_frozen() -> None:
    result = contest(True, referencia=(0.5,))
    with pytest.raises(FrozenInstanceError):
        result.task = "otra"  # type: ignore[misc]


# --- candidates ---


@pytest.mark.parametrize("target", ["valor", "nivel"])
def test_candidates_go_from_simple_to_flexible(target: str) -> None:
    assert list(candidates(target)) == NAMES  # type: ignore[arg-type]


def test_candidates_are_a_line_a_tree_a_forest_and_a_boosting() -> None:
    regressors = candidates("valor")
    assert isinstance(regressors["árbol"], DecisionTreeRegressor)
    assert isinstance(regressors["boosting"], HistGradientBoostingRegressor)
    classifiers = candidates("nivel")
    assert isinstance(classifiers["lineal"], LogisticRegression)
    assert isinstance(classifiers["bosque"], RandomForestClassifier)


def test_candidates_for_the_value_are_regressors() -> None:
    assert all(is_regressor(model) for model in candidates("valor").values())


def test_candidates_for_the_level_are_classifiers() -> None:
    assert all(is_classifier(model) for model in candidates("nivel").values())


@pytest.mark.parametrize("target", ["valor", "nivel"])
def test_candidates_have_the_seed(target: str) -> None:
    models = candidates(target)  # type: ignore[arg-type]
    for name in ["árbol", "bosque", "boosting"]:
        assert models[name].get_params()["random_state"] == SEED


@pytest.mark.parametrize("target", ["valor", "nivel"])
def test_candidates_trees_are_limited(target: str) -> None:
    models = candidates(target)  # type: ignore[arg-type]
    assert models["árbol"].get_params()["max_depth"] == DEPTH
    assert models["bosque"].get_params()["min_samples_leaf"] == LEAF
    assert models["bosque"].get_params()["n_estimators"] == TREES


def test_candidates_baselines() -> None:
    assert candidates("valor")[BASELINE].get_params()["strategy"] == "mean"
    assert candidates("nivel")[BASELINE].get_params()["strategy"] == "most_frequent"


# --- compete ---


def test_compete_value_names_its_task_and_metric() -> None:
    result = compete(signal(), "valor", 3)
    assert (result.task, result.metric, result.higher_is_better) == (
        "regresión del valor",
        "MAE",
        False,
    )


def test_compete_level_names_its_task_and_metric() -> None:
    result = compete(signal(), "nivel", 3)
    assert (result.task, result.metric, result.higher_is_better) == (
        "clasificación del nivel",
        "exactitud equilibrada",
        True,
    )


def test_compete_one_score_per_fold_and_model() -> None:
    result = compete(noise(), "valor", 4)
    assert list(result.scores) == NAMES
    assert all(len(scores) == 4 for scores in result.scores.values())


def test_compete_value_errors_are_positive() -> None:
    assert all(
        score > 0 for scores in compete(noise(), "valor", 3).scores.values() for score in scores
    )


def test_compete_trees_draw_what_a_line_cannot() -> None:
    result = compete(bump(), "valor", 3)
    assert result.wins["lineal"] == 0
    assert result.best in {"árbol", "bosque", "boosting"}
    assert result.improves


def test_compete_level_trees_draw_what_a_line_cannot() -> None:
    result = compete(bump(), "nivel", 3)
    assert result.best in {"árbol", "bosque", "boosting"}
    assert result.improves


def test_compete_every_model_learns_when_the_label_decides_the_value() -> None:
    result = compete(signal(), "valor", 3)
    assert all(wins == 3 for wins in result.wins.values())


def test_compete_does_not_improve_with_noise() -> None:
    assert not compete(noise(), "valor", 3).improves
    assert not compete(noise(), "nivel", 3).improves


def test_compete_baseline_is_the_mean_of_each_training_fold() -> None:
    rows = ordered(noise())
    expected = -cross_val_score(
        DummyRegressor(),
        rows[INPUTS],
        rows["valor"],
        scoring="neg_mean_absolute_error",
        cv=KFold(3, shuffle=True, random_state=SEED),
    )
    assert compete(noise(), "valor", 3).scores[BASELINE] == pytest.approx(tuple(expected))


def test_compete_uses_the_same_folds_and_preparation_for_every_model() -> None:
    rows = ordered(bump())
    for name, model in candidates("valor").items():
        pipeline = Pipeline([("prepare", prepare()), ("model", model)])
        expected = -cross_val_score(
            pipeline,
            rows[INPUTS],
            rows["valor"],
            scoring="neg_mean_absolute_error",
            cv=KFold(3, shuffle=True, random_state=SEED),
        )
        assert compete(bump(), "valor", 3).scores[name] == pytest.approx(tuple(expected))


def test_compete_by_time_trains_only_with_the_past() -> None:
    rows = ordered(bump())
    expected = -cross_val_score(
        DummyRegressor(),
        rows[INPUTS],
        rows["valor"],
        scoring="neg_mean_absolute_error",
        cv=TimeSeriesSplit(3),
    )
    result = compete(bump(), "valor", 3, by_time=True)
    assert result.scores[BASELINE] == pytest.approx(tuple(expected))


def test_compete_level_balances_the_levels() -> None:
    # Hay más medidas de nivel medio: la exactitud de "siempre medio" pasaría de 0,33; la
    # equilibrada da a cada nivel el mismo peso, y la referencia se queda en un tercio.
    assert compete(noise(), "nivel", 3).scores[BASELINE] == pytest.approx((1 / 3,) * 3)


def test_compete_level_does_not_see_the_value() -> None:
    # El nivel sale del valor: si el valor entrara como entrada, acertaría siempre.
    assert compete(noise(), "nivel", 3).means["árbol"] < 0.9


def test_compete_is_repeatable() -> None:
    assert compete(noise(), "valor", 3) == compete(noise(), "valor", 3)


# --- el comando competir ---


def test_competir_prints_the_data_both_tables_and_both_verdicts(tmp_path: Path) -> None:
    path = write(tmp_path, bump())
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    result = runner.invoke(cli.app, ["competir", str(path), "--pliegues", "3"])
    assert result.exit_code == 0, result.output
    assert f"instantanea.csv: 120 medidas · sha256: {digest} · pliegues al azar" in result.output
    assert "regresión del valor · MAE en cada pliegue" in result.output
    assert "clasificación del nivel · exactitud equilibrada en cada pliegue" in result.output
    best = compete(bump(), "valor", 3).best
    assert f"regresión del valor: el mejor es {best}, gana en 3 de 3 pliegues: mejora" in (
        result.output
    )


def test_competir_writes_one_row_per_model(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["competir", str(write(tmp_path, noise())), "--pliegues", "3"])
    for name in NAMES:
        assert len(re.findall(rf"│ {name} +│", result.output)) == 2
    # La referencia no compite consigo misma: su columna "Gana" va vacía.
    assert len(re.findall(r"│ referencia +│.*│ +│\n", result.output)) == 2


def test_competir_shows_each_score_the_mean_and_the_wins(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["competir", str(write(tmp_path, noise())), "--pliegues", "3"])
    expected = compete(noise(), "valor", 3)
    scores = " +│ +".join(f"{score:.3f}" for score in expected.scores["bosque"])
    mean = expected.means["bosque"]
    wins = expected.wins["bosque"]
    assert re.search(rf"│ bosque +│ +{scores} +│ +{mean:.3f} +│ +{wins} de 3 │", result.output)


def test_competir_says_when_no_model_beats_the_mean_of_the_baseline(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fake(frame: pd.DataFrame, target: str, n_splits: int, by_time: bool) -> Contest:
        return contest(False, referencia=(1.0,), lineal=(2.0,))

    monkeypatch.setattr(ensembles, "compete", fake)
    result = runner.invoke(cli.app, ["competir", str(write(tmp_path, noise()))])
    assert "regresión del valor" not in result.output
    assert result.output.count("tarea: ningún modelo mejora la media de la referencia") == 2


def test_competir_says_when_the_best_does_not_improve(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["competir", str(write(tmp_path, noise())), "--pliegues", "3"])
    expected = compete(noise(), "nivel", 3)
    best = expected.best
    assert (
        f"clasificación del nivel: el mejor es {best}, gana en {expected.wins[best]} de 3"
        " pliegues: no mejora la referencia"
    ) in result.output


def test_competir_by_time(tmp_path: Path) -> None:
    path = str(write(tmp_path, signal()))
    result = runner.invoke(cli.app, ["competir", path, "--pliegues", "3", "--tiempo"])
    assert "pliegues por tiempo" in result.output
    expected = compete(signal(), "valor", 3, by_time=True).scores[BASELINE][0]
    assert f"{expected:.3f}" in result.output


def test_competir_passes_the_folds_and_the_order_to_both_tasks(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[tuple[str, int, bool]] = []

    def spy(frame: pd.DataFrame, target: str, n_splits: int, by_time: bool) -> Contest:
        calls.append((target, n_splits, by_time))
        return contest(True, referencia=(0.5,), lineal=(1.0,))

    monkeypatch.setattr(ensembles, "compete", spy)
    path = str(write(tmp_path, signal()))
    runner.invoke(cli.app, ["competir", path, "--pliegues", "7", "--tiempo"])
    assert calls == [("valor", 7, True), ("nivel", 7, True)]


def test_competir_checks_the_digest(tmp_path: Path) -> None:
    result = runner.invoke(
        cli.app, ["competir", str(write(tmp_path, signal())), "--huella", "0000"]
    )
    assert result.exit_code == 1
    assert "no 0000" in result.output


def test_competir_without_the_position_column(tmp_path: Path) -> None:
    path = write(tmp_path, signal().drop(columns=["posicion"]))
    result = runner.invoke(cli.app, ["competir", str(path)])
    assert result.exit_code == 1
    assert "faltan las columnas posicion" in result.output


def test_competir_with_too_few_measures_for_the_folds(tmp_path: Path) -> None:
    path = write(tmp_path, signal(9))
    assert runner.invoke(cli.app, ["competir", str(path), "--pliegues", "10"]).exit_code == 1


def test_competir_without_the_file(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["competir", str(tmp_path / "no.csv")])
    assert result.exit_code == 2
    assert "no se puede leer" in result.output


@pytest.mark.parametrize("value", ["1", "11"])
def test_competir_rejects_a_number_of_folds_out_of_range(tmp_path: Path, value: str) -> None:
    path = str(write(tmp_path, signal()))
    result = runner.invoke(cli.app, ["competir", path, "--pliegues", value])
    assert result.exit_code == 2
    assert "not in the range 2<=x<=10" in result.output


def test_ensembles_is_not_reexported_in_core() -> None:
    assert "ensembles" not in observatorio.core.__all__
    assert not hasattr(observatorio.core, "compete")
