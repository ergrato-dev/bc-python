"""Tests de la semana 23: las medidas como arrays de NumPy y el comando `estadisticas`.

Qué: comprueban core/arrays.py con valores que se pueden calcular a mano, comparan con
Hypothesis lo nuevo (NumPy) con lo viejo (Python puro), y prueban la CLI.
Para qué: dos números de coma flotante calculados por caminos distintos casi nunca son
idénticos; np.testing y pytest.approx comparan con una tolerancia, y un NaN en el sitio
correcto también cuenta como acierto.
Impacto: los dos últimos tests impiden que NumPy se cargue al arrancar la CLI, la decisión
que mediste en la semana 22.
"""

import math
import subprocess
import sys
import warnings
from pathlib import Path

import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st
from typer.testing import CliRunner

from observatorio import cli
from observatorio.core import Measurement, Series, median
from observatorio.core.arrays import (
    Stats,
    group_means,
    histogram,
    labels_array,
    outliers,
    stats_of,
    values_array,
    zscores,
)

runner = CliRunner()

SERIES = Series(
    [
        Measurement("Norte", 12.5),
        Measurement("Sur", 8.0),
        Measurement("Centro", None),
        Measurement("Norte", 48.9),
    ]
)

# Valores que no desbordan ni pierden toda la precisión al restarlos: lo que mide un sensor.
VALUES = st.floats(min_value=-1e6, max_value=1e6, allow_nan=False)
MEASUREMENTS = st.lists(
    st.builds(
        Measurement,
        st.sampled_from(["Norte", "Sur", "Centro"]),
        st.none() | VALUES,
    )
)


def floats(*values: float) -> np.ndarray[tuple[int], np.dtype[np.float64]]:
    """Un array de float64 con estos valores: floats(1, math.nan, 3)."""
    return np.array(values, dtype=np.float64)


def stats_rows(stdout: str) -> dict[str, str]:
    """Las filas de la tabla de estadísticas: {"con valor": "3", "media": "4.0 unidad"...}."""
    cells = [line.strip("│ ").split(" │ ") for line in stdout.splitlines() if line.startswith("│")]
    return {name.strip(): value.strip() for name, value in cells}


def write(tmp_path: Path, text: str) -> Path:
    """Guarda text en medidas.txt dentro de tmp_path y devuelve la ruta."""
    path = tmp_path / "medidas.txt"
    path.write_text(text, encoding="utf-8")
    return path


# --- values_array y labels_array ---


def test_values_array_is_float64() -> None:
    assert values_array(SERIES).dtype == np.float64


def test_values_array_keeps_order_and_puts_nan_where_the_value_is_missing() -> None:
    np.testing.assert_array_equal(values_array(SERIES), floats(12.5, 8.0, math.nan, 48.9))


def test_values_array_of_an_empty_series_is_empty() -> None:
    assert values_array(Series()).shape == (0,)


def test_labels_array_keeps_order() -> None:
    assert labels_array(SERIES).tolist() == ["Norte", "Sur", "Centro", "Norte"]


def test_labels_array_is_text_even_when_empty() -> None:
    assert labels_array(Series()).dtype.kind == "U"


# --- stats_of ---


def test_stats_of_known_values() -> None:
    assert stats_of(floats(1, 2, 3, 4)) == Stats(
        count=4,
        missing=0,
        mean=2.5,
        std=math.sqrt(1.25),
        minimum=1.0,
        q1=1.75,
        median=2.5,
        q3=3.25,
        maximum=4.0,
    )


def test_stats_of_skips_nan_and_counts_them_as_missing() -> None:
    stats = stats_of(floats(math.nan, 10, math.nan, 20))
    assert stats is not None
    assert (stats.count, stats.missing, stats.mean) == (2, 2, 15.0)


def test_stats_of_only_nan_is_none() -> None:
    assert stats_of(floats(math.nan, math.nan)) is None


def test_stats_of_empty_is_none() -> None:
    assert stats_of(floats()) is None


def test_stats_of_a_single_value_has_no_spread() -> None:
    stats = stats_of(floats(7))
    assert stats is not None
    assert (stats.std, stats.q1, stats.q3) == (0.0, 7.0, 7.0)


@given(st.lists(VALUES, min_size=1))
def test_stats_of_agrees_with_median_and_mean(values: list[float]) -> None:
    stats = stats_of(np.array(values))
    assert stats is not None
    assert stats.median == pytest.approx(median(values), abs=1e-6)
    assert stats.mean == pytest.approx(math.fsum(values) / len(values), abs=1e-6)
    assert stats.minimum <= stats.q1 <= stats.median <= stats.q3 <= stats.maximum


# --- zscores y outliers ---


def test_zscores_known_values() -> None:
    np.testing.assert_allclose(zscores(floats(2, 4, 6)), [-math.sqrt(1.5), 0, math.sqrt(1.5)])


def test_zscores_keep_nan_in_place_and_ignore_it() -> None:
    np.testing.assert_allclose(zscores(floats(0, math.nan, 2)), [-1, math.nan, 1])


@pytest.mark.parametrize(
    "values", [floats(5, 5, 5), floats(), floats(math.nan, math.nan)], ids=["equal", "empty", "nan"]
)
def test_zscores_without_spread_are_nan_and_do_not_warn(
    values: np.ndarray[tuple[int], np.dtype[np.float64]],
) -> None:
    # Un aviso convertido en error: dividir por 0 o promediar nada en NumPy solo avisa.
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        result = zscores(values)
    assert result.shape == values.shape
    assert np.isnan(result).all()


# Enteros: con floats, Hypothesis encuentra [0.0, 5e-324], cuya desviación es tan pequeña
# que dividir por ella da inf. Los datos de un sensor no son así.
@given(st.lists(st.integers(min_value=-1000, max_value=1000), min_size=2, unique=True))
def test_zscores_have_mean_zero_and_std_one(values: list[int]) -> None:
    z = zscores(np.array(values))
    assert z.mean() == pytest.approx(0, abs=1e-6)
    assert z.std() == pytest.approx(1)


def test_outliers_are_the_positions_beyond_the_threshold() -> None:
    values = floats(10, 10, 10, 10, 10, 10, 10, 10, 10, 100)
    assert outliers(values, 2.0).tolist() == [9]


def test_outliers_use_a_strict_threshold() -> None:
    # z de -1 y de +1: con umbral 1, ninguno lo supera.
    assert outliers(floats(0, 2), 1.0).tolist() == []


def test_outliers_never_include_missing_values() -> None:
    assert outliers(floats(0, math.nan, 2), 0.5).tolist() == [0, 2]


# --- histogram ---


def test_histogram_counts_each_bin_and_the_maximum_in_the_last() -> None:
    counts, edges = histogram(floats(0, 1, 2, 3, 4), 2)
    assert counts.tolist() == [2, 3]
    np.testing.assert_allclose(edges, [0, 2, 4])


def test_histogram_skips_nan() -> None:
    counts, _ = histogram(floats(1, math.nan, 3), 4)
    assert counts.sum() == 2


@given(st.lists(VALUES | st.just(math.nan)), st.integers(min_value=1, max_value=20))
def test_histogram_counts_every_present_value_once(values: list[float], bins: int) -> None:
    counts, edges = histogram(np.array(values, dtype=np.float64), bins)
    assert len(counts) == bins
    assert len(edges) == bins + 1
    assert counts.sum() == sum(not math.isnan(value) for value in values)


# --- group_means ---


def test_group_means_known_values() -> None:
    means = group_means(labels_array(SERIES), values_array(SERIES))
    assert means == {"Norte": pytest.approx(30.7), "Sur": 8.0}


def test_group_means_sorts_the_labels() -> None:
    assert list(group_means(labels_array(SERIES), values_array(SERIES))) == ["Norte", "Sur"]


def test_group_means_of_an_empty_series_is_empty() -> None:
    assert group_means(labels_array(Series()), values_array(Series())) == {}


@given(MEASUREMENTS)
def test_group_means_agree_with_series_means(measurements: list[Measurement]) -> None:
    series = Series(measurements)
    means = group_means(labels_array(series), values_array(series))
    expected = series.means()
    assert means.keys() == expected.keys()
    for label, mean in expected.items():
        assert means[label] == pytest.approx(mean, abs=1e-6)


# --- el comando estadisticas ---


def test_estadisticas_writes_the_summary(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["estadisticas", str(write(tmp_path, "A;2\nB;4\nA;6\n"))])
    assert result.exit_code == 0
    assert stats_rows(result.stdout) == {
        "con valor": "3",
        "sin dato": "0",
        "media": "4.0 unidad",
        "desviación": "1.6 unidad",
        "mínimo": "2.0 unidad",
        "Q1": "3.0 unidad",
        "mediana": "4.0 unidad",
        "Q3": "5.0 unidad",
        "máximo": "6.0 unidad",
    }


def test_estadisticas_writes_one_line_per_bin(tmp_path: Path) -> None:
    path = write(tmp_path, "A;0\nA;1\nA;2\nA;3\nA;4\n")
    result = runner.invoke(cli.app, ["estadisticas", "-i", "2", str(path)])
    assert "histograma (2 intervalos):" in result.stdout
    assert "   0.0 –    2.0  " + "█" * 20 + " " * 10 + " 2" in result.stdout
    assert "   2.0 –    4.0  " + "█" * 30 + " 3" in result.stdout


def test_estadisticas_lists_the_outliers(tmp_path: Path) -> None:
    path = write(tmp_path, "A;10\n" * 9 + "Pico;100\n")
    result = runner.invoke(cli.app, ["estadisticas", str(path)])
    assert "atípicas (|z| > 2): Pico 100.0 (z +3.0)" in result.stdout


def test_estadisticas_threshold_option(tmp_path: Path) -> None:
    path = write(tmp_path, "A;0\nB;2\n")
    result = runner.invoke(cli.app, ["estadisticas", "-u", "0.5", str(path)])
    assert "atípicas (|z| > 0.5): A 0.0 (z -1.0), B 2.0 (z +1.0)" in result.stdout


def test_estadisticas_without_outliers_says_none(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["estadisticas", str(write(tmp_path, "A;1\nB;2\n"))])
    assert "atípicas (|z| > 2): ninguna" in result.stdout


def test_estadisticas_writes_the_mean_of_each_label(tmp_path: Path) -> None:
    path = write(tmp_path, "Sur;8\nNorte;12,5\nSur;NA\nNorte;48,9\n")
    result = runner.invoke(cli.app, ["estadisticas", str(path)])
    assert "media por etiqueta: Norte 30.7, Sur 8.0" in result.stdout


def test_estadisticas_without_values(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["estadisticas", str(write(tmp_path, "A;NA\n"))])
    assert result.exit_code == 0
    assert result.stdout == "ninguna medida con valor\n"


def test_estadisticas_reports_invalid_lines_and_exits_1(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["estadisticas", str(write(tmp_path, "A;1\nmalo\nB;3\n"))])
    assert result.exit_code == 1
    assert "error: línea 2: 'malo'" in result.stderr
    assert stats_rows(result.stdout)["con valor"] == "2"


def test_estadisticas_missing_file_exits_2(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["estadisticas", str(tmp_path / "no.txt")])
    assert result.exit_code == 2
    assert result.stderr.startswith("error: ")


@pytest.mark.parametrize(
    ("option", "name"), [(["-i", "0"], "--intervalos"), (["-u", "-1"], "--umbral")]
)
def test_estadisticas_rejects_impossible_options(
    tmp_path: Path, option: list[str], name: str
) -> None:
    result = runner.invoke(cli.app, ["estadisticas", *option, str(write(tmp_path, "A;1\n"))])
    assert result.exit_code == 2
    assert f"Invalid value for '{name}'" in result.output


# --- NumPy solo cuando hace falta ---


@pytest.mark.parametrize("module", ["observatorio.core", "observatorio.cli"])
def test_importing_does_not_load_numpy(module: str) -> None:
    # En otro proceso: en este, los tests de arriba ya han importado NumPy.
    code = f"import sys, {module}; print('numpy' in sys.modules)"
    result = subprocess.run(
        [sys.executable, "-c", code], check=False, capture_output=True, text=True
    )
    assert result.stdout == "False\n"
