"""Tests de la semana 25: resúmenes por etiqueta, dos archivos a la vez y series de tiempo.

Qué: comprueban core/summaries.py con tablas pequeñas escritas a mano, comparan con
Hypothesis lo nuevo (groupby, resample) con lo que ya tenías (Series.means,
values_by_label), y prueban los comandos `resumir` y `evolucion`.
Para qué: groupby, merge y resample deciden en silencio el orden de las filas, qué pasa
con los NaN y qué grupos salen aunque estén vacíos; estos tests lo dejan escrito.
Impacto: summaries.py, como frames.py, no se reexporta: la CLI sigue arrancando sin pandas.
"""

import math
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import pytest
from hypothesis import given
from hypothesis import strategies as st
from typer.testing import CliRunner

from observatorio import cli
from observatorio.core import Measurement, Series
from observatorio.core.frames import frame_of
from observatorio.core.summaries import compare, duration, evolution, summary, timed

runner = CliRunner()

NAN = math.nan

# Las medidas válidas de medidas.txt: con START y una cada hora, van de las 8:00 a las 14:00.
SERIES = Series(
    [
        Measurement("Norte", 12.5),
        Measurement("Sur", 8.0),
        Measurement("Centro", None),
        Measurement("Oriente", 55.1),
        Measurement("Occidente", 61.0),
        Measurement("Norte", 48.9),
        Measurement("Sur", 9.5),
    ]
)
TEXT = "Norte;12,5\nSur;8\nCentro;NA\nOriente;55,1\nOccidente;61\nNorte;48,9\nSur;9,5\n"
START = datetime(2026, 11, 1, 8)
HOUR = timedelta(hours=1)

LABELS = ["Norte", "Sur", "Centro"]
VALUES = st.floats(min_value=-1e6, max_value=1e6, allow_nan=False)
MEASUREMENTS = st.lists(st.builds(Measurement, st.sampled_from(LABELS), st.none() | VALUES))


def summary_table(rows: dict[str, tuple[int, int, float, float, float]]) -> pd.DataFrame:
    """El resumen que debe salir: {"A": (count, missing, mean, minimum, maximum)}."""
    return (
        pd.DataFrame(
            list(rows.values()),
            columns=["count", "missing", "mean", "minimum", "maximum"],
            index=pd.Index(list(rows), dtype="str", name="label"),
        )
        .astype("float64")
        .astype({"count": "int64", "missing": "int64"})
    )


def means_table(means: dict[str, float]) -> pd.DataFrame:
    """Un resumen con solo la columna mean, lo único que usa compare: {"A": 1.0}."""
    return pd.DataFrame(
        {"mean": list(means.values())}, index=pd.Index(list(means), dtype="str", name="label")
    )


def data_rows(stdout: str) -> list[str]:
    """Las filas de datos de una tabla de pandas, con un espacio entre columnas."""
    return [" ".join(line.split()) for line in stdout.splitlines()[2:-1]]


def write(tmp_path: Path, text: str, name: str = "medidas.txt") -> Path:
    """Guarda text en tmp_path/name y devuelve la ruta."""
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


# --- summary ---


def test_summary_has_one_row_per_label_in_order_of_appearance() -> None:
    expected = summary_table(
        {
            "Norte": (2, 0, 30.7, 12.5, 48.9),
            "Sur": (2, 0, 8.75, 8.0, 9.5),
            "Centro": (0, 1, NAN, NAN, NAN),
            "Oriente": (1, 0, 55.1, 55.1, 55.1),
            "Occidente": (1, 0, 61.0, 61.0, 61.0),
        }
    )
    pd.testing.assert_frame_equal(summary(frame_of(SERIES)), expected)


def test_summary_counts_values_and_missing_apart() -> None:
    series = Series([Measurement("A", 1.0), Measurement("A", None), Measurement("A", 3.0)])
    pd.testing.assert_frame_equal(
        summary(frame_of(series)), summary_table({"A": (2, 1, 2.0, 1.0, 3.0)})
    )


def test_summary_of_an_empty_frame_keeps_the_columns_and_types() -> None:
    pd.testing.assert_frame_equal(summary(frame_of(Series([]))), summary_table({}))


def test_summary_does_not_change_the_frame() -> None:
    frame = frame_of(SERIES)
    before = frame.copy()
    summary(frame)
    pd.testing.assert_frame_equal(frame, before)


@given(MEASUREMENTS)
def test_summary_means_agree_with_series_means(measurements: list[Measurement]) -> None:
    series = Series(measurements)
    table = summary(frame_of(series))
    # Como diccionarios: means ordena por el primer valor de cada etiqueta, y summary, por
    # la primera vez que aparece, tenga valor o no.
    assert table["mean"].dropna().to_dict() == pytest.approx(series.means())


@given(MEASUREMENTS)
def test_summary_count_and_missing_add_up_to_the_measurements(
    measurements: list[Measurement],
) -> None:
    table = summary(frame_of(Series(measurements)))
    totals = (table["count"] + table["missing"]).to_dict()
    assert totals == Counter(m.label for m in measurements)
    with_values = table.loc[table["count"] > 0, "count"].to_dict()
    assert with_values == Counter(m.label for m in measurements if m.has_value)


# --- compare ---


def test_compare_known_values() -> None:
    table = compare(means_table({"A": 1.0, "B": 2.0}), means_table({"A": 1.5, "B": 1.0}))
    expected = pd.DataFrame(
        {"before": [1.0, 2.0], "after": [1.5, 1.0], "change": [0.5, -1.0]},
        index=pd.Index(["A", "B"], dtype="str", name="label"),
    )
    pd.testing.assert_frame_equal(table, expected)


def test_compare_keeps_labels_of_both_sorted() -> None:
    table = compare(means_table({"C": 1.0, "A": 2.0}), means_table({"B": 3.0, "A": 2.0}))
    assert list(table.index) == ["A", "B", "C"]


def test_compare_label_in_one_side_only_has_nan_on_the_other() -> None:
    table = compare(means_table({"A": 1.0}), means_table({"B": 2.0}))
    # Filas A y B; columnas before, after y change.
    assert table.isna().to_numpy().tolist() == [[False, True, True], [True, False, True]]


def test_compare_label_without_values_has_no_change() -> None:
    table = compare(means_table({"A": NAN}), means_table({"A": 2.0}))
    assert table["change"].isna().tolist() == [True]


def test_compare_rejects_a_repeated_label() -> None:
    repeated = pd.DataFrame(
        {"mean": [1.0, 2.0]}, index=pd.Index(["A", "A"], dtype="str", name="label")
    )
    with pytest.raises(pd.errors.MergeError):
        compare(repeated, means_table({"A": 1.0}))


def test_compare_of_two_empty_summaries_is_empty() -> None:
    empty = summary(frame_of(Series([])))
    table = compare(empty, empty)
    assert table.empty
    assert list(table.columns) == ["before", "after", "change"]


@given(MEASUREMENTS)
def test_compare_a_summary_with_itself_changes_nothing(measurements: list[Measurement]) -> None:
    table = summary(frame_of(Series(measurements)))
    changes = compare(table, table)
    assert sorted(changes.index) == sorted(table.index)
    assert (changes["change"].dropna() == 0).all()


# --- duration ---


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("1h", timedelta(hours=1)),
        ("15min", timedelta(minutes=15)),
        ("2h30min", timedelta(hours=2, minutes=30)),
        ("1D", timedelta(days=1)),
    ],
)
def test_duration_reads_pandas_durations(text: str, expected: timedelta) -> None:
    value = duration(text)
    assert value == expected
    assert type(value) is timedelta


@pytest.mark.parametrize("text", ["", "abc", "0h", "-1h", "1M"])
def test_duration_rejects_what_is_not_a_positive_duration(text: str) -> None:
    with pytest.raises(ValueError, match="no es una duración mayor que cero"):
        duration(text)


# --- timed ---


def test_timed_puts_one_measurement_every_step_from_start() -> None:
    frame = timed(frame_of(SERIES), START, HOUR)
    expected = pd.date_range("2026-11-01 08:00", "2026-11-01 14:00", freq="1h", name="time")
    pd.testing.assert_index_equal(frame.index, expected)


def test_timed_keeps_the_columns_and_values() -> None:
    frame = frame_of(SERIES)
    pd.testing.assert_frame_equal(
        timed(frame, START, HOUR).reset_index(drop=True), frame.reset_index(drop=True)
    )


def test_timed_does_not_change_the_frame() -> None:
    frame = frame_of(SERIES)
    timed(frame, START, HOUR)
    assert frame.index.name == "position"


def test_timed_of_an_empty_frame_is_empty() -> None:
    frame = timed(frame_of(Series([])), START, HOUR)
    assert frame.empty
    assert isinstance(frame.index, pd.DatetimeIndex)


# --- evolution ---


def test_evolution_known_values() -> None:
    table = evolution(timed(frame_of(SERIES), START, HOUR), timedelta(hours=3))
    expected = pd.DataFrame(
        {
            "Centro": [NAN, NAN, NAN],
            "Norte": [12.5, NAN, 48.9],
            "Occidente": [NAN, NAN, 61.0],
            "Oriente": [NAN, 55.1, NAN],
            "Sur": [NAN, 8.0, 9.5],
        },
        index=pd.date_range("2026-11-01 06:00", periods=3, freq="3h", name="time"),
    ).rename_axis(columns="label")
    expected.columns = expected.columns.astype("str")
    pd.testing.assert_frame_equal(table, expected)


def test_evolution_periods_start_at_midnight_not_at_the_first_measurement() -> None:
    table = evolution(timed(frame_of(SERIES), START, HOUR), timedelta(hours=5))
    assert [str(time) for time in table.index] == ["2026-11-01 05:00:00", "2026-11-01 10:00:00"]


def test_evolution_keeps_periods_without_measurements() -> None:
    series = Series([Measurement("A", 1.0), Measurement("A", 3.0)])
    table = evolution(timed(frame_of(series), START, timedelta(hours=5)), HOUR)
    assert len(table) == 6
    assert table["A"].isna().tolist() == [False, True, True, True, True, False]


def test_evolution_labels_are_columns_in_alphabetical_order() -> None:
    table = evolution(timed(frame_of(SERIES), START, HOUR), timedelta(days=1))
    assert list(table.columns) == ["Centro", "Norte", "Occidente", "Oriente", "Sur"]


def test_evolution_of_an_empty_frame_is_empty() -> None:
    assert evolution(timed(frame_of(Series([])), START, HOUR), HOUR).empty


@given(MEASUREMENTS.filter(bool))
def test_evolution_in_one_period_gives_the_means_of_summary(
    measurements: list[Measurement],
) -> None:
    frame = frame_of(Series(measurements))
    # Medianoche y un minuto entre medidas: todas caen en el mismo día.
    table = evolution(timed(frame, datetime(2026, 11, 1), timedelta(minutes=1)), timedelta(days=1))
    means = summary(frame)["mean"]
    assert len(table) == 1
    pd.testing.assert_series_equal(
        table.iloc[0].sort_index(), means.sort_index(), check_names=False
    )


# --- resumir ---


def test_resumir_writes_one_row_per_label(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["resumir", str(write(tmp_path, TEXT))])
    assert result.exit_code == 0
    assert data_rows(result.stdout) == [
        "Norte 2 0 30.7 12.5 48.9",
        "Sur 2 0 8.8 8.0 9.5",
        "Centro 0 1 sin dato sin dato sin dato",
        "Oriente 1 0 55.1 55.1 55.1",
        "Occidente 1 0 61.0 61.0 61.0",
    ]


def test_resumir_has_the_columns_in_spanish(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["resumir", str(write(tmp_path, TEXT))])
    lines = result.stdout.splitlines()
    assert lines[0].split() == ["medidas", "faltan", "media", "mínimo", "máximo"]
    assert lines[1].strip() == "etiqueta"


def test_resumir_ends_with_the_totals(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["resumir", str(write(tmp_path, TEXT))])
    assert result.stdout.splitlines()[-1] == "5 etiquetas · 7 medidas"


def test_resumir_empty_file(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["resumir", str(write(tmp_path, ""))])
    assert result.exit_code == 0
    assert result.stdout == "ninguna medida\n0 etiquetas · 0 medidas\n"


def test_resumir_reports_invalid_lines_with_the_file_and_exits_1(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["resumir", str(write(tmp_path, "A;1\nmalo\n"))])
    assert result.exit_code == 1
    assert "error: medidas.txt: línea 2: 'malo'" in result.stderr
    assert result.stdout.splitlines()[-1] == "1 etiquetas · 1 medidas"


def test_resumir_missing_file_exits_2(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["resumir", str(tmp_path / "no.txt")])
    assert result.exit_code == 2
    assert result.stderr.startswith("error: ")


def test_resumir_contra_compares_the_means(tmp_path: Path) -> None:
    before = write(tmp_path, "A;1\nB;2\nB;4\n", "antes.txt")
    after = write(tmp_path, "A;1,5\nB;2\nC;7\n", "despues.txt")
    result = runner.invoke(cli.app, ["resumir", str(before), "--contra", str(after)])
    assert result.exit_code == 0
    assert result.stdout.splitlines()[0].split() == ["antes", "después", "cambio"]
    assert data_rows(result.stdout) == [
        "A 1.0 1.5 0.5",
        "B 3.0 2.0 -1.0",
        "C sin dato 7.0 sin dato",
    ]
    assert result.stdout.splitlines()[-1] == "2 de 3 etiquetas en los dos archivos"


def test_resumir_contra_reports_the_errors_of_the_other_file(tmp_path: Path) -> None:
    before = write(tmp_path, "A;1\n", "antes.txt")
    after = write(tmp_path, "A;2\nmalo\n", "despues.txt")
    result = runner.invoke(cli.app, ["resumir", str(before), "-c", str(after)])
    assert result.exit_code == 1
    assert "error: despues.txt: línea 2: 'malo'" in result.stderr
    assert data_rows(result.stdout) == ["A 1.0 2.0 1.0"]


def test_resumir_contra_missing_file_exits_2(tmp_path: Path) -> None:
    before = write(tmp_path, "A;1\n")
    result = runner.invoke(cli.app, ["resumir", str(before), "-c", str(tmp_path / "no.txt")])
    assert result.exit_code == 2
    assert result.stderr.startswith("error: ")


# --- evolucion ---


def test_evolucion_writes_one_row_per_period(tmp_path: Path) -> None:
    args = ["evolucion", str(write(tmp_path, TEXT)), "--inicio", "2026-11-01T08:00:00"]
    result = runner.invoke(cli.app, [*args, "--periodo", "3h"])
    assert result.exit_code == 0
    assert result.stdout.splitlines()[0].split() == [
        "etiqueta", "Centro", "Norte", "Occidente", "Oriente", "Sur"
    ]  # fmt: skip
    assert data_rows(result.stdout) == [
        "2026-11-01 06:00:00 sin dato 12.5 sin dato sin dato sin dato",
        "2026-11-01 09:00:00 sin dato sin dato sin dato 55.1 8.0",
        "2026-11-01 12:00:00 sin dato 48.9 61.0 sin dato 9.5",
    ]
    assert result.stdout.splitlines()[-1] == "3 periodos · 7 medidas"


def test_evolucion_one_day_and_one_hour_by_default(tmp_path: Path) -> None:
    path = write(tmp_path, "A;1\nA;3\n")
    result = runner.invoke(cli.app, ["evolucion", str(path), "--inicio", "2026-11-01"])
    assert data_rows(result.stdout) == ["2026-11-01 2.0"]


def test_evolucion_cada(tmp_path: Path) -> None:
    path = write(tmp_path, "A;1\nA;3\n")
    args = ["evolucion", str(path), "--inicio", "2026-11-01T23:00:00", "--cada", "1D"]
    result = runner.invoke(cli.app, args)
    assert data_rows(result.stdout) == ["2026-11-01 1.0", "2026-11-02 3.0"]


def test_evolucion_writes_at_most_filas_periods(tmp_path: Path) -> None:
    path = write(tmp_path, "".join(f"A;{i}\n" for i in range(25)))
    args = ["evolucion", str(path), "--inicio", "2026-11-01", "--cada", "1D"]
    lines = runner.invoke(cli.app, args).stdout.splitlines()
    assert len(lines) == 2 + 20 + 2
    assert lines[-2:] == ["… y 5 más (usa --filas para verlos)", "25 periodos · 25 medidas"]


def test_evolucion_filas_option(tmp_path: Path) -> None:
    path = write(tmp_path, "A;1\nA;2\nA;3\n")
    args = ["evolucion", str(path), "--inicio", "2026-11-01", "--cada", "1D", "-n", "2"]
    result = runner.invoke(cli.app, args)
    assert data_rows(result.stdout)[:-1] == ["2026-11-01 1.0", "2026-11-02 2.0"]
    assert "… y 1 más" in result.stdout


@pytest.mark.parametrize("option", ["--cada", "--periodo"])
def test_evolucion_rejects_a_duration_that_is_not_positive(tmp_path: Path, option: str) -> None:
    path = write(tmp_path, "A;1\n")
    args = ["evolucion", str(path), "--inicio", "2026-11-01", option, "0h"]
    result = runner.invoke(cli.app, args)
    assert result.exit_code == 2
    assert result.stderr == "error: no es una duración mayor que cero: '0h'\n"


def test_evolucion_needs_inicio(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["evolucion", str(write(tmp_path, "A;1\n"))])
    assert result.exit_code == 2
    assert "Missing option '--inicio'" in result.output


def test_evolucion_empty_file(tmp_path: Path) -> None:
    path = write(tmp_path, "")
    result = runner.invoke(cli.app, ["evolucion", str(path), "--inicio", "2026-11-01"])
    assert result.stdout == "ninguna medida\n0 periodos · 0 medidas\n"


def test_evolucion_reports_invalid_lines_and_exits_1(tmp_path: Path) -> None:
    path = write(tmp_path, "A;1\nmalo\nA;3\n")
    result = runner.invoke(cli.app, ["evolucion", str(path), "--inicio", "2026-11-01"])
    assert result.exit_code == 1
    assert "error: medidas.txt: línea 2: 'malo'" in result.stderr
    assert data_rows(result.stdout) == ["2026-11-01 2.0"]


# --- pandas solo cuando hace falta ---


def test_summaries_is_not_reexported_from_core() -> None:
    import observatorio.core

    assert "summaries" not in observatorio.core.__all__
    assert not hasattr(observatorio.core, "summary")
