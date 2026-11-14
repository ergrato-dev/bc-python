"""Tests de la semana 32: validación cruzada de un modelo ajustado, con un pipeline.

Qué: comprueban core/validation.py (el orden de las medidas, la preparación de las
entradas, los pliegues al azar y por tiempo, el ajuste y la medida en cada pliegue) y el
comando `ajustar`.
Para qué: la validación cruzada solo sirve si cada pliegue es un examen honrado. Si la
preparación se ajusta con todas las medidas, si los pliegues por tiempo dejan ver el futuro,
o si la regularización se elige con los mismos pliegues con los que se mide, el resultado
sale mejor de lo que es, y nada falla.
Impacto: validation.py no se reexporta en core: la CLI arranca sin cargar scikit-learn.
"""

import hashlib
import math
import re
from dataclasses import FrozenInstanceError
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from sklearn.exceptions import NotFittedError
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GridSearchCV, KFold, TimeSeriesSplit
from sklearn.utils.validation import check_is_fitted
from test_learning import level_of
from typer.testing import CliRunner

import observatorio.core
from observatorio import cli
from observatorio.core import validation
from observatorio.core.learning import SEED
from observatorio.core.validation import (
    INPUTS,
    STRENGTHS,
    CrossValidation,
    folds,
    ordered,
    prepare,
    validate,
)

runner = CliRunner()


def frame_of(rows: list[tuple[str, float]]) -> pd.DataFrame:
    """Una instantánea de una carga: la posición es el orden de llegada."""
    values = [value for _, value in rows]
    return pd.DataFrame(
        {
            "carga": 1,
            "posicion": range(len(rows)),
            "etiqueta": [label for label, _ in rows],
            "valor": values,
            "nivel": [level_of(value) for value in values],
        }
    )


def signal(size: int = 120) -> pd.DataFrame:
    """La etiqueta decide el valor (Norte, bajo; Sur, medio; Centro, alto), con ruido. Las
    etiquetas se turnan: cada pliegue, al azar o por tiempo, tiene de las tres."""
    rng = np.random.default_rng(1)
    centers = {"Norte": 5.0, "Sur": 30.0, "Centro": 70.0}
    labels = list(centers)
    rows = []
    for position in range(size):
        label = labels[position % 3]
        rows.append((label, float(round(rng.normal(centers[label], 2.0), 1))))
    return frame_of(rows)


def noise(size: int = 120) -> pd.DataFrame:
    """Valores al azar y etiquetas al azar: no hay nada que aprender."""
    rng = np.random.default_rng(2)
    labels = rng.choice(["Norte", "Sur", "Centro"], size=size).tolist()
    values = rng.uniform(0, 80, size=size).round(1).tolist()
    return frame_of(list(zip(labels, values, strict=True)))


def result(model: tuple[float, ...], baseline: tuple[float, ...], higher: bool) -> CrossValidation:
    return CrossValidation("tarea", "métrica", higher, model, baseline, {})


def write(tmp_path: Path, frame: pd.DataFrame) -> Path:
    path = tmp_path / "instantanea.csv"
    frame.to_csv(path, index=False, lineterminator="\n")
    return path


# --- CrossValidation ---


def test_beats_when_higher_is_better() -> None:
    assert result((0.9, 0.4), (0.5, 0.5), True).beats == (True, False)


def test_beats_when_lower_is_better() -> None:
    assert result((3.0, 9.0), (5.0, 5.0), False).beats == (True, False)


@pytest.mark.parametrize("higher", [True, False])
def test_a_tie_is_not_a_win(higher: bool) -> None:
    assert result((0.5,), (0.5,), higher).beats == (False,)


def test_improves_only_when_it_wins_every_fold() -> None:
    assert result((0.9, 0.8, 0.7), (0.5, 0.5, 0.5), True).improves
    assert not result((0.9, 0.8, 0.4), (0.5, 0.5, 0.5), True).improves


def test_cross_validation_is_frozen() -> None:
    with pytest.raises(FrozenInstanceError):
        result((0.5,), (0.5,), True).metric = "otra"  # type: ignore[misc]


# --- ordered ---


def test_ordered_sorts_by_load_and_position() -> None:
    frame = signal(6)
    frame["carga"] = [2, 1, 2, 1, 1, 2]
    rows = ordered(frame.iloc[::-1])
    assert list(zip(rows["carga"], rows["posicion"], strict=True)) == [
        (1, 1),
        (1, 3),
        (1, 4),
        (2, 0),
        (2, 2),
        (2, 5),
    ]


def test_ordered_drops_the_measures_without_value() -> None:
    frame = pd.concat([signal(), frame_of([("Norte", math.nan)])], ignore_index=True)
    assert len(ordered(frame)) == 120


def test_ordered_names_the_missing_columns() -> None:
    with pytest.raises(ValueError, match="faltan las columnas carga, posicion"):
        ordered(signal().drop(columns=["carga", "posicion"]))


def test_ordered_keeps_the_checks_of_known() -> None:
    with pytest.raises(ValueError, match="dos niveles"):
        ordered(frame_of([("Norte", 30.0)] * 10))


# --- prepare ---


def test_prepare_has_one_column_per_label_and_the_position() -> None:
    prepared = prepare().fit(signal()[INPUTS])
    assert list(prepared.get_feature_names_out()) == [
        "etiqueta__etiqueta_Centro",
        "etiqueta__etiqueta_Norte",
        "etiqueta__etiqueta_Sur",
        "posicion__posicion",
    ]


def test_prepare_scales_the_position_with_the_data_it_is_fitted_on() -> None:
    train = signal()[INPUTS].iloc[:60]
    position = prepare().fit(train).transform(train)[:, -1]
    assert position.mean() == pytest.approx(0.0, abs=1e-9)
    assert position.std() == pytest.approx(1.0)


def test_prepare_does_not_learn_from_rows_it_was_not_fitted_on() -> None:
    inputs = signal()[INPUTS]
    prepared = prepare().fit(inputs.iloc[:60])
    # La posición 90 está lejos de las 60 primeras: escalada con ellas, mucho más que 1.
    assert prepared.transform(inputs.iloc[[90]])[0, -1] > 2


def test_prepare_ignores_a_label_it_never_saw() -> None:
    prepared = prepare().fit(signal()[INPUTS])
    unseen = pd.DataFrame({"etiqueta": ["Oeste"], "posicion": [0]})
    assert prepared.transform(unseen)[0, :3].tolist() == [0.0, 0.0, 0.0]


def test_prepare_uses_only_the_label_and_the_position() -> None:
    prepared = prepare().fit(signal())
    assert not any("valor" in name or "nivel" in name for name in prepared.get_feature_names_out())


def test_prepare_comes_unfitted() -> None:
    with pytest.raises(NotFittedError):
        check_is_fitted(prepare())


# --- folds ---


def test_random_folds_are_shuffled_with_the_seed() -> None:
    splitter = folds(5, by_time=False)
    assert isinstance(splitter, KFold)
    assert splitter.shuffle
    assert splitter.random_state == SEED


@pytest.mark.parametrize("n_splits", [2, 5, 10])
@pytest.mark.parametrize("by_time", [True, False])
def test_folds_number(n_splits: int, by_time: bool) -> None:
    assert folds(n_splits, by_time).get_n_splits() == n_splits


def test_time_folds_always_test_after_training() -> None:
    splitter = folds(4, by_time=True)
    assert isinstance(splitter, TimeSeriesSplit)
    for train, test in splitter.split(np.zeros(100)):
        assert train.max() < test.min()


@settings(max_examples=30, deadline=None)
@given(st.integers(min_value=2, max_value=10), st.integers(min_value=20, max_value=200))
def test_random_folds_test_every_row_once(n_splits: int, size: int) -> None:
    tested = [index for _, test in folds(n_splits, False).split(np.zeros(size)) for index in test]
    assert sorted(tested) == list(range(size))


# --- validate: el valor ---


def test_validate_value_names_its_task_and_metric() -> None:
    validated = validate(signal(), "valor", 3)
    assert (validated.task, validated.metric) == ("regresión del valor", "MAE")
    assert not validated.higher_is_better


def test_validate_value_one_score_per_fold() -> None:
    validated = validate(signal(), "valor", 4)
    assert len(validated.model) == len(validated.baseline) == 4


def test_validate_value_errors_are_positive() -> None:
    validated = validate(noise(), "valor", 3)
    assert all(score > 0 for score in validated.model + validated.baseline)


def test_validate_value_improves_when_the_label_decides_the_value() -> None:
    validated = validate(signal(), "valor", 5)
    assert validated.improves
    assert all(score < 3 for score in validated.model)


def test_validate_value_does_not_improve_with_noise() -> None:
    assert not validate(noise(), "valor", 5).improves


def test_validate_value_baseline_is_the_mean_of_each_training_fold() -> None:
    rows = ordered(noise())
    values = rows["valor"].to_numpy()
    expected = [
        mean_absolute_error(values[test], np.full(len(test), values[train].mean()))
        for train, test in folds(3, False).split(values)
    ]
    assert validate(noise(), "valor", 3).baseline == pytest.approx(expected)


def test_validate_value_by_time_trains_only_with_the_past() -> None:
    rows = ordered(noise())
    values = rows["valor"].to_numpy()
    expected = [
        mean_absolute_error(values[test], np.full(len(test), values[: test[0]].mean()))
        for _, test in folds(3, True).split(values)
    ]
    assert validate(noise(), "valor", 3, by_time=True).baseline == pytest.approx(expected)


def test_validate_value_learns_from_the_position() -> None:
    rng = np.random.default_rng(3)
    labels = rng.choice(["Norte", "Sur"], size=90).tolist()
    trend = [float(position) * 0.5 for position in range(90)]
    assert validate(frame_of(list(zip(labels, trend, strict=True))), "valor", 3).improves


def test_validate_value_tunes_alpha() -> None:
    params = validate(signal(), "valor", 3).params
    assert list(params) == ["alpha"]
    assert params["alpha"] in STRENGTHS


def test_validate_value_regularizes_noise_as_much_as_it_can() -> None:
    # Sin nada que aprender, lo mejor es acercarse a la media: la regularización más fuerte.
    assert validate(noise(300), "valor", 5).params == {"alpha": 100.0}


# --- validate: el nivel ---


def test_validate_level_names_its_task_and_metric() -> None:
    validated = validate(signal(), "nivel", 3)
    assert (validated.task, validated.metric) == (
        "clasificación del nivel",
        "exactitud equilibrada",
    )
    assert validated.higher_is_better


def test_validate_level_improves_when_the_label_decides_the_level() -> None:
    validated = validate(signal(), "nivel", 5)
    assert validated.improves
    assert validated.model == pytest.approx((1.0,) * 5)


def test_validate_level_baseline_guesses_the_most_frequent_level() -> None:
    # Con los tres niveles en cada prueba, decir siempre uno acierta un tercio de media.
    assert validate(signal(), "nivel", 5).baseline == pytest.approx((1 / 3,) * 5)


def test_validate_level_does_not_see_the_value() -> None:
    assert not validate(noise(), "nivel", 5).improves


def test_validate_level_tunes_c() -> None:
    params = validate(signal(), "nivel", 3).params
    assert list(params) == ["C"]
    assert params["C"] in STRENGTHS


def test_validate_level_by_time_with_a_label_that_comes_late() -> None:
    frame = signal()
    frame.loc[frame.index[-10:], "etiqueta"] = "Oeste"
    assert len(validate(frame, "nivel", 3, by_time=True).model) == 3


def test_validate_tunes_inside_each_fold(monkeypatch: pytest.MonkeyPatch) -> None:
    fitted: list[int] = []

    class Counting(GridSearchCV):  # type: ignore[misc]
        def fit(self, x: object, y: object = None, **params: object) -> Counting:
            fitted.append(len(x))  # type: ignore[arg-type]
            return super().fit(x, y, **params)  # type: ignore[no-any-return]

    monkeypatch.setattr(validation, "GridSearchCV", Counting)
    validate(signal(), "valor", 4)
    # Una búsqueda con el entrenamiento de cada pliegue, y la última con todas las medidas.
    assert fitted == [90, 90, 90, 90, 120]


# --- el comando ajustar ---


def test_ajustar_prints_the_data_both_tables_and_both_verdicts(tmp_path: Path) -> None:
    path = write(tmp_path, signal())
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    result = runner.invoke(cli.app, ["ajustar", str(path), "--pliegues", "3"])
    assert result.exit_code == 0, result.output
    assert f"instantanea.csv: 120 medidas · sha256: {digest} · pliegues al azar" in result.output
    assert "regresión del valor · MAE en cada pliegue" in result.output
    assert "clasificación del nivel · exactitud equilibrada en cada pliegue" in result.output
    assert "gana en 3 de 3 pliegues: el modelo mejora la referencia" in result.output


def test_ajustar_writes_one_row_per_fold_and_the_mean(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["ajustar", str(write(tmp_path, signal())), "--pliegues", "4"])
    for number in range(1, 5):
        assert len(re.findall(rf"│ +{number} │", result.output)) == 2
    assert len(re.findall(r"│ +media │", result.output)) == 2


def test_ajustar_shows_each_score_with_three_decimals(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["ajustar", str(write(tmp_path, noise())), "--pliegues", "3"])
    validated = validate(noise(), "valor", 3)
    for score in validated.model + validated.baseline:
        assert f"{score:.3f}" in result.output
    mean = sum(validated.model) / 3
    assert re.search(rf"│ +media │ +{mean:.3f} │", result.output)


def test_ajustar_shows_the_chosen_strength(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["ajustar", str(write(tmp_path, signal())), "--pliegues", "3"])
    assert "regresión del valor: con alpha=0.01, gana en" in result.output
    assert "clasificación del nivel: con C=" in result.output


def test_ajustar_says_when_it_does_not_improve(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["ajustar", str(write(tmp_path, noise())), "--pliegues", "5"])
    validated = validate(noise(), "valor", 5)
    wins = sum(validated.beats)
    assert f"gana en {wins} de 5 pliegues: el modelo no mejora la referencia" in result.output
    assert re.search(r"│ +\d │ .*│ no +│", result.output)


def test_ajustar_by_time(tmp_path: Path) -> None:
    path = str(write(tmp_path, signal()))
    result = runner.invoke(cli.app, ["ajustar", path, "--pliegues", "3", "--tiempo"])
    assert "pliegues por tiempo" in result.output
    expected = validate(signal(), "valor", 3, by_time=True).baseline[0]
    assert f"{expected:.3f}" in result.output


def test_ajustar_passes_the_folds_and_the_order_to_both_models(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[tuple[str, int, bool]] = []

    def spy(frame: pd.DataFrame, target: str, n_splits: int, by_time: bool) -> CrossValidation:
        calls.append((target, n_splits, by_time))
        return result((1.0,), (0.5,), True)

    monkeypatch.setattr(validation, "validate", spy)
    path = str(write(tmp_path, signal()))
    runner.invoke(cli.app, ["ajustar", path, "--pliegues", "7", "--tiempo"])
    assert calls == [("valor", 7, True), ("nivel", 7, True)]


def test_ajustar_checks_the_digest(tmp_path: Path) -> None:
    path = write(tmp_path, signal())
    result = runner.invoke(cli.app, ["ajustar", str(path), "--huella", "0000"])
    assert result.exit_code == 1
    assert "no 0000" in result.output


def test_ajustar_without_the_position_column(tmp_path: Path) -> None:
    path = write(tmp_path, signal().drop(columns=["posicion"]))
    result = runner.invoke(cli.app, ["ajustar", str(path)])
    assert result.exit_code == 1
    assert "faltan las columnas posicion" in result.output


def test_ajustar_with_too_few_measures_for_the_folds(tmp_path: Path) -> None:
    path = write(tmp_path, signal(9))
    assert runner.invoke(cli.app, ["ajustar", str(path), "--pliegues", "10"]).exit_code == 1


def test_ajustar_without_the_file(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["ajustar", str(tmp_path / "no.csv")])
    assert result.exit_code == 2
    assert "no se puede leer" in result.output


@pytest.mark.parametrize("value", ["1", "11"])
def test_ajustar_rejects_a_number_of_folds_out_of_range(tmp_path: Path, value: str) -> None:
    path = str(write(tmp_path, signal()))
    result = runner.invoke(cli.app, ["ajustar", path, "--pliegues", value])
    assert result.exit_code == 2
    assert "not in the range 2<=x<=10" in result.output


def test_validation_is_not_reexported_in_core() -> None:
    assert "validation" not in observatorio.core.__all__
    assert not hasattr(observatorio.core, "validate")
