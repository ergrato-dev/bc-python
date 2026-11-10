"""Tests de la semana 24: las medidas como DataFrame de pandas y el comando `filtrar`.

Qué: comprueban core/frames.py con tablas pequeñas escritas a mano, comparan con Hypothesis
lo nuevo (pandas) con lo que ya tenías (Scale.level, Series.where, most_common, la lectura
de archivos), y prueban la CLI.
Para qué: pandas.testing compara dos DataFrames entero (valores, tipos de columna e índice);
un `==` entre tablas da otra tabla, no un sí o un no.
Impacto: el último test impide que pandas se cargue al arrancar la CLI, como NumPy en la
semana 23.
"""

import math
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd
import pytest
from hypothesis import given
from hypothesis import strategies as st
from typer.testing import CliRunner

from observatorio import cli
from observatorio.core import Measurement, Scale, Series, open_file
from observatorio.core.frames import (
    by_value,
    frame_of,
    label_counts,
    select,
    with_levels,
    write_frame,
)

runner = CliRunner()

SCALE = Scale("unidad", 10, 50)

SERIES = Series(
    [
        Measurement("Norte", 12.5),
        Measurement("Sur", 8.0),
        Measurement("Centro", None),
        Measurement("Norte", 48.9),
    ]
)

VALUES = st.floats(min_value=-1e6, max_value=1e6, allow_nan=False)
MEASUREMENTS = st.lists(
    st.builds(
        Measurement,
        st.sampled_from(["Norte", "Sur", "Centro"]),
        st.none() | VALUES,
    )
)


def table(labels: list[str], values: list[float], positions: list[int]) -> pd.DataFrame:
    """El DataFrame que debe salir: table(["A"], [1.0], [1]); math.nan si falta el valor."""
    return pd.DataFrame(
        {"label": pd.Series(labels, dtype="str"), "value": pd.Series(values, dtype="float64")}
    ).set_axis(pd.Index(positions, name="position"))


def frame_rows(stdout: str) -> list[str]:
    """Las filas de datos que escribe `filtrar`, con un espacio entre columnas: ["1 A 2.0 bajo"]."""
    return [" ".join(line.split()) for line in stdout.splitlines()[2:-1]]


def write(tmp_path: Path, text: str) -> Path:
    """Guarda text en medidas.txt dentro de tmp_path y devuelve la ruta."""
    path = tmp_path / "medidas.txt"
    path.write_text(text, encoding="utf-8")
    return path


# --- frame_of ---


def test_frame_of_has_one_row_per_measurement_in_order() -> None:
    expected = table(["Norte", "Sur", "Centro", "Norte"], [12.5, 8.0, math.nan, 48.9], [1, 2, 3, 4])
    pd.testing.assert_frame_equal(frame_of(SERIES), expected, check_index_type=False)


def test_frame_of_column_types() -> None:
    frame = frame_of(SERIES)
    assert list(frame.columns) == ["label", "value"]
    assert frame["label"].dtype == "str"
    assert frame["value"].dtype == "float64"


def test_frame_of_index_is_the_position_from_1() -> None:
    index = frame_of(SERIES).index
    assert isinstance(index, pd.RangeIndex)
    assert (index.start, index.stop, index.name) == (1, 5, "position")


def test_frame_of_an_empty_series_keeps_the_columns_and_types() -> None:
    frame = frame_of(Series())
    assert frame.empty
    assert frame.dtypes.to_dict() == {"label": "str", "value": "float64"}


def test_frame_of_puts_nan_where_the_value_is_missing() -> None:
    assert frame_of(SERIES)["value"].isna().tolist() == [False, False, True, False]


@given(MEASUREMENTS)
def test_frame_of_keeps_every_measurement(measurements: list[Measurement]) -> None:
    frame = frame_of(Series(measurements))
    rebuilt = [
        Measurement(label, None if math.isnan(value) else value)
        for label, value in frame.itertuples(index=False)
    ]
    assert rebuilt == measurements


# --- with_levels ---


def test_with_levels_adds_the_level_of_each_value() -> None:
    assert with_levels(frame_of(SERIES), SCALE)["level"].tolist() == [
        "medio",
        "bajo",
        "sin dato",
        "medio",
    ]


@pytest.mark.parametrize(
    ("value", "level"), [(9.99, "bajo"), (10.0, "medio"), (49.99, "medio"), (50.0, "alto")]
)
def test_with_levels_borders_like_classify(value: float, level: str) -> None:
    frame = frame_of(Series([Measurement("A", value)]))
    assert with_levels(frame, SCALE)["level"].tolist() == [level]


def test_with_levels_level_is_text() -> None:
    assert with_levels(frame_of(SERIES), SCALE)["level"].dtype == "str"


def test_with_levels_does_not_change_the_frame() -> None:
    frame = frame_of(SERIES)
    with_levels(frame, SCALE)
    assert list(frame.columns) == ["label", "value"]


@given(MEASUREMENTS)
def test_with_levels_agrees_with_scale_level(measurements: list[Measurement]) -> None:
    levels = with_levels(frame_of(Series(measurements)), SCALE)["level"].tolist()
    assert levels == [SCALE.level(m.value) for m in measurements]


# --- select ---


def test_select_without_filters_keeps_every_row() -> None:
    frame = frame_of(SERIES)
    pd.testing.assert_frame_equal(select(frame), frame)


def test_select_by_label_keeps_the_positions() -> None:
    expected = table(["Norte", "Norte"], [12.5, 48.9], [1, 4])
    pd.testing.assert_frame_equal(select(frame_of(SERIES), labels=["Norte"]), expected)


def test_select_by_several_labels() -> None:
    chosen = select(frame_of(SERIES), labels={"Sur", "Centro"})
    assert chosen.index.tolist() == [2, 3]


def test_select_unknown_label_is_empty() -> None:
    assert select(frame_of(SERIES), labels=["Oeste"]).empty


def test_select_low_and_high_are_included() -> None:
    chosen = select(frame_of(SERIES), low=8.0, high=12.5)
    assert chosen["value"].tolist() == [12.5, 8.0]


def test_select_only_low() -> None:
    assert select(frame_of(SERIES), low=12.5)["value"].tolist() == [12.5, 48.9]


def test_select_only_high() -> None:
    assert select(frame_of(SERIES), high=12.5)["value"].tolist() == [12.5, 8.0]


def test_select_by_value_drops_missing_values() -> None:
    assert 3 not in select(frame_of(SERIES), low=-1e9).index


def test_select_label_and_value_at_once() -> None:
    chosen = select(frame_of(SERIES), labels=["Norte", "Sur"], low=10.0)
    assert chosen.index.tolist() == [1, 4]


def test_select_keeps_the_level_column() -> None:
    chosen = select(with_levels(frame_of(SERIES), SCALE), labels=["Sur"])
    assert chosen["level"].tolist() == ["bajo"]


def test_changing_a_selection_does_not_change_the_frame() -> None:
    # Copy-on-write, por defecto desde pandas 3.0: la selección se comporta como una copia.
    frame = frame_of(SERIES)
    chosen = select(frame, labels=["Norte"])
    chosen.loc[1, "value"] = 0.0
    assert frame.loc[1, "value"] == 12.5


@given(MEASUREMENTS, st.sets(st.sampled_from(["Norte", "Sur", "Centro"]), min_size=1))
def test_select_by_label_agrees_with_series_where(
    measurements: list[Measurement], labels: set[str]
) -> None:
    series = Series(measurements)
    chosen = select(frame_of(series), labels=labels)
    pd.testing.assert_frame_equal(
        chosen.reset_index(drop=True),
        frame_of(series.where(lambda m: m.label in labels)).reset_index(drop=True),
        check_index_type=False,
    )


# --- by_value ---


def test_by_value_from_highest_to_lowest_and_missing_last() -> None:
    assert by_value(frame_of(SERIES)).index.tolist() == [4, 1, 2, 3]


def test_by_value_keeps_ties_in_their_order() -> None:
    series = Series([Measurement("A", 5.0), Measurement("B", 9.0), Measurement("C", 5.0)])
    assert by_value(frame_of(series))["label"].tolist() == ["B", "A", "C"]


def test_by_value_keeps_ties_in_order_in_a_long_frame() -> None:
    series = Series([Measurement(f"M{i}", float(i % 3)) for i in range(100)])
    positions = by_value(frame_of(series)).index.tolist()
    assert positions == sorted(range(1, 101), key=lambda position: -((position - 1) % 3))


def test_by_value_does_not_change_the_frame() -> None:
    frame = frame_of(SERIES)
    by_value(frame)
    assert frame.index.tolist() == [1, 2, 3, 4]


# --- label_counts ---


def test_label_counts_known_values() -> None:
    assert label_counts(frame_of(SERIES)) == {"Norte": 2, "Sur": 1, "Centro": 1}


def test_label_counts_types_are_python() -> None:
    counts = label_counts(frame_of(SERIES))
    assert all(type(label) is str and type(n) is int for label, n in counts.items())


def test_label_counts_of_an_empty_frame_is_empty() -> None:
    assert label_counts(frame_of(Series())) == {}


@given(MEASUREMENTS)
def test_label_counts_agree_with_most_common(measurements: list[Measurement]) -> None:
    series = Series(measurements)
    expected = series.most_common(len(series))
    assert list(label_counts(frame_of(series)).items()) == expected


# --- write_frame ---


def test_write_frame_writes_like_medidas_csv(tmp_path: Path) -> None:
    path = tmp_path / "salida.csv"
    write_frame(with_levels(frame_of(SERIES), SCALE), path)
    assert path.read_text(encoding="utf-8") == (
        "etiqueta;valor\nNorte;12,5\nSur;8,0\nCentro;NA\nNorte;48,9\n"
    )


@given(MEASUREMENTS)
def test_write_frame_reads_back_the_same_series(measurements: list[Measurement]) -> None:
    # Sin tmp_path: Hypothesis repite el test con la misma fixture; una carpeta por ejemplo.
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "salida.csv"
        write_frame(frame_of(Series(measurements)), path)
        series, errors = Series.parse(open_file(path).lines())
    assert errors == []
    assert list(series) == measurements


# --- el comando filtrar ---


def test_filtrar_writes_every_measurement_with_its_level(tmp_path: Path) -> None:
    path = write(tmp_path, "Norte;12,34\nSur;8\nCentro;NA\nNorte;48,9\n")
    result = runner.invoke(cli.app, ["filtrar", str(path)])
    assert result.exit_code == 0
    assert frame_rows(result.stdout) == [
        "1 Norte 12.3 medio",
        "2 Sur 8.0 bajo",
        "3 Centro sin dato sin dato",
        "4 Norte 48.9 medio",
    ]
    assert result.stdout.split("\n")[0].split() == ["etiqueta", "valor", "nivel"]


def test_filtrar_ends_with_the_counts(tmp_path: Path) -> None:
    path = write(tmp_path, "Norte;12,5\nSur;8\nCentro;NA\nNorte;48,9\n")
    result = runner.invoke(cli.app, ["filtrar", str(path)])
    assert result.stdout.splitlines()[-1] == "4 de 4 medidas · Norte 2, Sur 1, Centro 1"


def test_filtrar_by_label_and_value(tmp_path: Path) -> None:
    path = write(tmp_path, "Norte;12,5\nSur;8\nCentro;20\nNorte;48,9\nSur;30\n")
    result = runner.invoke(
        cli.app, ["filtrar", "-e", "Norte", "-e", "Sur", "--desde", "10", str(path)]
    )
    assert [row.split()[0] for row in frame_rows(result.stdout)] == ["1", "4", "5"]
    assert result.stdout.splitlines()[-1] == "3 de 5 medidas · Norte 2, Sur 1"


def test_filtrar_hasta(tmp_path: Path) -> None:
    path = write(tmp_path, "A;5\nB;15\nC;25\n")
    result = runner.invoke(cli.app, ["filtrar", "--hasta", "15", str(path)])
    assert [row.split()[1] for row in frame_rows(result.stdout)] == ["A", "B"]


def test_filtrar_writes_at_most_filas_rows(tmp_path: Path) -> None:
    path = write(tmp_path, "".join(f"A;{i}\n" for i in range(25)))
    result = runner.invoke(cli.app, ["filtrar", str(path)])
    lines = result.stdout.splitlines()
    assert len(lines) == 2 + 20 + 2
    assert lines[-2:] == ["… y 5 más (usa --filas para verlas)", "25 de 25 medidas · A 25"]


def test_filtrar_filas_option(tmp_path: Path) -> None:
    path = write(tmp_path, "A;5\nB;15\nC;25\n")
    result = runner.invoke(cli.app, ["filtrar", "-n", "2", "--ordenar", str(path)])
    assert [row.split()[1] for row in frame_rows(result.stdout)[:-1]] == ["C", "B"]
    assert "… y 1 más" in result.stdout


def test_filtrar_rejects_zero_filas(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["filtrar", "-n", "0", str(write(tmp_path, "A;1\n"))])
    assert result.exit_code == 2
    assert "Invalid value for '--filas'" in result.output


def test_filtrar_ordenar(tmp_path: Path) -> None:
    path = write(tmp_path, "A;5\nB;NA\nC;25\nD;15\n")
    result = runner.invoke(cli.app, ["filtrar", "--ordenar", str(path)])
    assert [row.split()[1] for row in frame_rows(result.stdout)] == ["C", "D", "A", "B"]


def test_filtrar_without_matches(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["filtrar", "--desde", "100", str(write(tmp_path, "A;5\n"))])
    assert result.exit_code == 0
    assert result.stdout == "ninguna medida cumple el filtro\n0 de 1 medidas\n"


def test_filtrar_salida_writes_every_chosen_row(tmp_path: Path) -> None:
    output = tmp_path / "elegidas.csv"
    path = write(tmp_path, "A;5\nB;15,5\nC;25\n")
    result = runner.invoke(
        cli.app, ["filtrar", "--desde", "10", "-n", "1", "-o", str(output), str(path)]
    )
    assert result.exit_code == 0
    assert result.stdout.endswith(f"guardadas en {output}\n")
    assert output.read_text(encoding="utf-8") == "etiqueta;valor\nB;15,5\nC;25,0\n"


def test_filtrar_salida_that_cannot_be_written_exits_2(tmp_path: Path) -> None:
    output = tmp_path / "no-existe" / "elegidas.csv"
    result = runner.invoke(cli.app, ["filtrar", "-o", str(output), str(write(tmp_path, "A;5\n"))])
    assert result.exit_code == 2
    assert result.stderr.startswith(f"error: no se pudo guardar {output}: ")


def test_filtrar_reports_invalid_lines_and_exits_1(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["filtrar", str(write(tmp_path, "A;1\nmalo\nB;3\n"))])
    assert result.exit_code == 1
    assert "error: línea 2: 'malo'" in result.stderr
    assert result.stdout.splitlines()[-1] == "2 de 2 medidas · A 1, B 1"


def test_filtrar_missing_file_exits_2(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["filtrar", str(tmp_path / "no.txt")])
    assert result.exit_code == 2
    assert result.stderr.startswith("error: ")


# --- pandas solo cuando hace falta ---


def test_frames_is_not_reexported_from_core() -> None:
    import observatorio.core

    assert "frames" not in observatorio.core.__all__
    assert not hasattr(observatorio.core, "frame_of")


def test_importing_the_cli_does_not_load_pandas() -> None:
    # En otro proceso: en este, los tests de arriba ya han importado pandas.
    code = "import sys, observatorio.cli; print('pandas' in sys.modules)"
    result = subprocess.run(
        [sys.executable, "-c", code], check=False, capture_output=True, text=True
    )
    assert result.stdout == "False\n"
