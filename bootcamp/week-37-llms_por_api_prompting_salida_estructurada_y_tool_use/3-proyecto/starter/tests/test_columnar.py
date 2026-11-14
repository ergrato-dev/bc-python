"""Tests de la semana 26: Polars, Parquet y DuckDB.

Qué: comprueban core/columnar.py con tablas pequeñas escritas a mano, comparan con
Hypothesis el resumen de Polars con el de pandas y el de DuckDB, y prueban los comandos
`exportar` y `sql`.
Para qué: Polars, Parquet y DuckDB deciden en silencio si un dato que falta es null o NaN,
en qué orden salen los grupos y qué tipo tiene cada columna; estos tests lo dejan escrito.
Impacto: columnar.py no se reexporta: la CLI sigue arrancando sin Polars ni DuckDB.
"""

import io
import math
import subprocess
import sys
import tempfile
from pathlib import Path

import duckdb
import polars as pl
import pytest
from hypothesis import given
from hypothesis import strategies as st
from typer.testing import CliRunner

from observatorio import cli
from observatorio.core import Measurement, Series, frames, summaries
from observatorio.core.columnar import frame_of, query, summary

runner = CliRunner()

# Las medidas válidas de medidas.txt.
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

# Las columnas del resumen y sus tipos: count y missing son UInt32 en Polars.
SUMMARY_SCHEMA = {
    "label": pl.String,
    "count": pl.UInt32,
    "missing": pl.UInt32,
    "mean": pl.Float64,
    "minimum": pl.Float64,
    "maximum": pl.Float64,
}

LABELS = ["Norte", "Sur", "Centro"]
VALUES = st.floats(min_value=-1e6, max_value=1e6, allow_nan=False)
MEASUREMENTS = st.lists(st.builds(Measurement, st.sampled_from(LABELS), st.none() | VALUES))

Row = tuple[object, ...]


def summary_rows(series: Series) -> list[Row]:
    """El resumen de Polars de una serie, como lista de tuplas."""
    return summary(frame_of(series).lazy()).collect().rows()


def same_rows(rows: list[Row], expected: list[Row]) -> bool:
    """Las mismas filas, con los float comparados con tolerancia: cada biblioteca suma a su modo."""
    return len(rows) == len(expected) and all(
        len(row) == len(other)
        and all(
            math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)
            if isinstance(a, float) and isinstance(b, float)
            else a == b
            for a, b in zip(row, other, strict=True)
        )
        for row, other in zip(rows, expected, strict=True)
    )


def parquet_of(tmp_path: Path, series: Series, name: str = "medidas.parquet") -> Path:
    """Guarda la serie en tmp_path/name con Polars y devuelve la ruta."""
    path = tmp_path / name
    frame_of(series).write_parquet(path)
    return path


def write(tmp_path: Path, text: str, name: str = "medidas.txt") -> Path:
    """Guarda text en tmp_path/name y devuelve la ruta."""
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def cells(stdout: str) -> list[list[str]]:
    """Las celdas de las filas de datos de una tabla de Rich, sin la cabecera."""
    return [
        [cell.strip() for cell in line.strip("│").split("│")]
        for line in stdout.splitlines()
        if line.startswith("│")
    ]


def header(stdout: str) -> list[str]:
    """Los nombres de las columnas de una tabla de Rich."""
    line = next(line for line in stdout.splitlines() if line.startswith("┃"))
    return [cell.strip() for cell in line.strip("┃").split("┃")]


# --- frame_of ---


def test_frame_of_has_label_and_value_with_their_types() -> None:
    frame = frame_of(SERIES)
    assert frame.schema == pl.Schema({"label": pl.String, "value": pl.Float64})
    assert frame.row(0) == ("Norte", 12.5)
    assert frame.height == 7


def test_frame_of_a_missing_value_is_null_not_nan() -> None:
    value = frame_of(SERIES)["value"]
    assert value.null_count() == 1
    assert value.is_nan().sum() == 0
    assert value[2] is None


def test_frame_of_an_empty_series_keeps_the_types() -> None:
    frame = frame_of(Series([]))
    assert frame.height == 0
    assert frame.schema == pl.Schema({"label": pl.String, "value": pl.Float64})


def test_frame_of_a_series_without_values_keeps_the_types() -> None:
    frame = frame_of(Series([Measurement("A", None)]))
    assert frame.schema["value"] == pl.Float64


@given(MEASUREMENTS)
def test_frame_of_agrees_with_the_pandas_frame(measurements: list[Measurement]) -> None:
    series = Series(measurements)
    pandas = frames.frame_of(series)
    frame = frame_of(series)
    assert frame["label"].to_list() == pandas["label"].to_list()
    # pandas pone NaN y Polars null: los dos son "falta".
    assert frame["value"].to_list() == [
        None if math.isnan(value) else value for value in pandas["value"]
    ]


# --- summary ---


def test_summary_is_lazy() -> None:
    assert isinstance(summary(frame_of(SERIES).lazy()), pl.LazyFrame)


def test_summary_has_one_row_per_label_in_order_of_appearance() -> None:
    assert summary_rows(SERIES) == [
        ("Norte", 2, 0, 30.7, 12.5, 48.9),
        ("Sur", 2, 0, 8.75, 8.0, 9.5),
        ("Centro", 0, 1, None, None, None),
        ("Oriente", 1, 0, 55.1, 55.1, 55.1),
        ("Occidente", 1, 0, 61.0, 61.0, 61.0),
    ]


def test_summary_has_the_columns_and_types() -> None:
    assert summary(frame_of(SERIES).lazy()).collect_schema() == pl.Schema(SUMMARY_SCHEMA)


def test_summary_counts_values_and_missing_apart() -> None:
    series = Series([Measurement("A", 1.0), Measurement("A", None), Measurement("A", 3.0)])
    assert summary_rows(series) == [("A", 2, 1, 2.0, 1.0, 3.0)]


def test_summary_of_an_empty_frame_keeps_the_columns_and_types() -> None:
    table = summary(frame_of(Series([])).lazy()).collect()
    assert table.height == 0
    assert table.schema == pl.Schema(SUMMARY_SCHEMA)


def test_summary_order_does_not_depend_on_the_size() -> None:
    # Con muchas filas, Polars reparte el trabajo entre hilos: maintain_order mantiene el orden.
    labels = [f"L{number:03}" for number in range(300)]
    series = Series([Measurement(label, 1.0) for label in labels * 20])
    assert [row[0] for row in summary_rows(series)] == labels


@given(MEASUREMENTS)
def test_summary_agrees_with_the_pandas_summary(measurements: list[Measurement]) -> None:
    series = Series(measurements)
    table = summaries.summary(frames.frame_of(series))
    # La misma tabla de pandas, con None donde pandas pone NaN.
    expected = [
        (label, *(None if isinstance(v, float) and math.isnan(v) else v for v in row))
        for label, row in zip(table.index, table.itertuples(index=False), strict=True)
    ]
    assert same_rows(summary_rows(series), expected)


# --- Parquet ---


def test_parquet_keeps_the_rows_and_the_types(tmp_path: Path) -> None:
    frame = pl.read_parquet(parquet_of(tmp_path, SERIES))
    assert frame.equals(frame_of(SERIES))
    assert frame.schema == frame_of(SERIES).schema


def test_parquet_keeps_null_as_null(tmp_path: Path) -> None:
    frame = pl.read_parquet(parquet_of(tmp_path, SERIES))
    assert frame["value"].null_count() == 1


def test_summary_of_a_parquet_file(tmp_path: Path) -> None:
    lazy = pl.scan_parquet(parquet_of(tmp_path, SERIES))
    assert summary(lazy).collect().rows() == summary_rows(SERIES)


@given(MEASUREMENTS)
def test_parquet_round_trip(measurements: list[Measurement]) -> None:
    # Sin tmp_path: Hypothesis repite el test muchas veces con la misma fixture.
    frame = frame_of(Series(measurements))
    buffer = io.BytesIO()
    frame.write_parquet(buffer)
    buffer.seek(0)
    assert pl.read_parquet(buffer).equals(frame)


# --- query ---


def test_query_sees_the_file_as_medidas(tmp_path: Path) -> None:
    columns, rows = query(parquet_of(tmp_path, SERIES), "SELECT * FROM medidas LIMIT 2")
    assert columns == ["label", "value"]
    assert rows == [("Norte", 12.5), ("Sur", 8.0)]


def test_query_missing_value_is_none(tmp_path: Path) -> None:
    sql = "SELECT value FROM medidas WHERE label = 'Centro'"
    assert query(parquet_of(tmp_path, SERIES), sql) == (["value"], [(None,)])


def test_query_group_by(tmp_path: Path) -> None:
    sql = "SELECT label, count(value) AS count FROM medidas GROUP BY label ORDER BY label"
    columns, rows = query(parquet_of(tmp_path, SERIES), sql)
    assert columns == ["label", "count"]
    assert rows == [("Centro", 0), ("Norte", 2), ("Occidente", 1), ("Oriente", 1), ("Sur", 2)]


def test_query_of_an_empty_file(tmp_path: Path) -> None:
    path = parquet_of(tmp_path, Series([]))
    assert query(path, "SELECT count(*) AS n FROM medidas") == (["n"], [(0,)])


@pytest.mark.parametrize(
    "sql",
    [
        "SELECT * FROM '{folder}/otro.csv'",
        "SELECT * FROM read_parquet('{folder}/otro.parquet')",
        "COPY medidas TO '{folder}/copia.csv'",
    ],
)
def test_query_cannot_touch_other_files(tmp_path: Path, sql: str) -> None:
    path = parquet_of(tmp_path, SERIES)
    write(tmp_path, "secreto\n", "otro.csv")
    parquet_of(tmp_path, SERIES, "otro.parquet")
    with pytest.raises(duckdb.PermissionException):
        query(path, sql.format(folder=tmp_path))
    assert not (tmp_path / "copia.csv").exists()


def test_query_cannot_turn_the_files_back_on(tmp_path: Path) -> None:
    with pytest.raises(duckdb.InvalidInputException):
        query(parquet_of(tmp_path, SERIES), "SET enable_external_access = true")


def test_query_with_bad_sql_raises_a_duckdb_error(tmp_path: Path) -> None:
    with pytest.raises(duckdb.ParserException):
        query(parquet_of(tmp_path, SERIES), "SELEC 1")


def test_query_of_a_missing_file_raises_a_duckdb_error(tmp_path: Path) -> None:
    with pytest.raises(duckdb.IOException):
        query(tmp_path / "no.parquet", "SELECT 1")


def test_query_of_a_file_that_is_not_parquet_raises_a_duckdb_error(tmp_path: Path) -> None:
    with pytest.raises(duckdb.Error):
        query(write(tmp_path, TEXT), "SELECT 1")


@given(MEASUREMENTS)
def test_query_agrees_with_the_polars_summary(measurements: list[Measurement]) -> None:
    series = Series(measurements)
    frame = frame_of(series)
    sql = (
        "SELECT label, count(value), count(*) - count(value), avg(value), min(value), max(value)"
        " FROM medidas GROUP BY label ORDER BY min(rowid)"
    )
    # Un archivo por ejemplo: query lee de disco, y Hypothesis no admite tmp_path.
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "m.parquet"
        frame.write_parquet(path)
        _, rows = query(path, sql)
    assert same_rows(rows, summary_rows(series))


# --- exportar ---


def test_exportar_writes_a_parquet_file_with_the_measurements(tmp_path: Path) -> None:
    salida = tmp_path / "medidas.parquet"
    result = runner.invoke(cli.app, ["exportar", str(write(tmp_path, TEXT)), str(salida)])
    assert result.exit_code == 0
    assert pl.read_parquet(salida).equals(frame_of(SERIES))


def test_exportar_writes_the_summary_of_the_file(tmp_path: Path) -> None:
    salida = tmp_path / "medidas.parquet"
    result = runner.invoke(cli.app, ["exportar", str(write(tmp_path, TEXT)), str(salida)])
    assert cells(result.stdout) == [
        ["Norte", "2", "0", "30.7", "12.5", "48.9"],
        ["Sur", "2", "0", "8.8", "8.0", "9.5"],
        ["Centro", "0", "1", "sin dato", "sin dato", "sin dato"],
        ["Oriente", "1", "0", "55.1", "55.1", "55.1"],
        ["Occidente", "1", "0", "61.0", "61.0", "61.0"],
    ]


def test_exportar_has_the_columns_in_spanish(tmp_path: Path) -> None:
    salida = tmp_path / "medidas.parquet"
    result = runner.invoke(cli.app, ["exportar", str(write(tmp_path, TEXT)), str(salida)])
    assert header(result.stdout) == ["etiqueta", "medidas", "faltan", "media", "mínimo", "máximo"]


def test_exportar_ends_with_the_file_and_its_size(tmp_path: Path) -> None:
    salida = tmp_path / "medidas.parquet"
    result = runner.invoke(cli.app, ["exportar", str(write(tmp_path, TEXT)), str(salida)])
    size = salida.stat().st_size
    assert result.stdout.splitlines()[-1] == f"7 medidas en medidas.parquet · {size} bytes"


def test_exportar_empty_file(tmp_path: Path) -> None:
    salida = tmp_path / "vacio.parquet"
    result = runner.invoke(cli.app, ["exportar", str(write(tmp_path, "")), str(salida)])
    assert result.exit_code == 0
    assert result.stdout.splitlines()[0] == "ninguna medida"
    assert pl.read_parquet(salida).schema == frame_of(SERIES).schema


def test_exportar_reports_invalid_lines_writes_the_rest_and_exits_1(tmp_path: Path) -> None:
    salida = tmp_path / "medidas.parquet"
    result = runner.invoke(cli.app, ["exportar", str(write(tmp_path, "A;1\nmalo\n")), str(salida)])
    assert result.exit_code == 1
    assert "error: medidas.txt: línea 2: 'malo'" in result.stderr
    assert pl.read_parquet(salida).rows() == [("A", 1.0)]


def test_exportar_missing_file_exits_2(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["exportar", str(tmp_path / "no.txt"), str(tmp_path / "s")])
    assert result.exit_code == 2
    assert result.stderr.startswith("error: ")


def test_exportar_cannot_write_exits_2(tmp_path: Path) -> None:
    salida = tmp_path / "no" / "existe.parquet"
    result = runner.invoke(cli.app, ["exportar", str(write(tmp_path, TEXT)), str(salida)])
    assert result.exit_code == 2
    assert result.stderr.startswith(f"error: no se puede escribir {salida}")


# --- sql ---


def test_sql_writes_the_rows(tmp_path: Path) -> None:
    path = parquet_of(tmp_path, SERIES)
    query_text = "SELECT label, avg(value) AS mean FROM medidas GROUP BY label ORDER BY label"
    result = runner.invoke(cli.app, ["sql", str(path), query_text])
    assert result.exit_code == 0
    assert header(result.stdout) == ["etiqueta", "media"]
    assert cells(result.stdout) == [
        ["Centro", "sin dato"],
        ["Norte", "30.7"],
        ["Occidente", "61.0"],
        ["Oriente", "55.1"],
        ["Sur", "8.8"],
    ]
    assert result.stdout.splitlines()[-1] == "5 filas"


def test_sql_keeps_the_names_that_are_not_in_names(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["sql", str(parquet_of(tmp_path, SERIES)), "SELECT 1 AS uno"])
    assert header(result.stdout) == ["uno"]
    assert cells(result.stdout) == [["1"]]


def test_sql_writes_at_most_filas_rows(tmp_path: Path) -> None:
    path = parquet_of(tmp_path, SERIES)
    result = runner.invoke(cli.app, ["sql", str(path), "SELECT * FROM medidas", "--filas", "2"])
    assert len(cells(result.stdout)) == 2
    assert result.stdout.splitlines()[-2:] == [
        "… y 5 más (usa --filas para verlas)",
        "7 filas",
    ]


def test_sql_writes_rows_by_default(tmp_path: Path) -> None:
    series = Series([Measurement("A", float(number)) for number in range(cli.ROWS + 1)])
    result = runner.invoke(cli.app, ["sql", str(parquet_of(tmp_path, series)), "FROM medidas"])
    assert len(cells(result.stdout)) == cli.ROWS


def test_sql_bad_query_exits_2(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["sql", str(parquet_of(tmp_path, SERIES)), "SELEC 1"])
    assert result.exit_code == 2
    assert result.stderr.startswith("error: Parser Error")


def test_sql_cannot_read_other_files_and_exits_2(tmp_path: Path) -> None:
    other = write(tmp_path, TEXT)
    sql = f"SELECT * FROM read_csv('{other}')"
    result = runner.invoke(cli.app, ["sql", str(parquet_of(tmp_path, SERIES)), sql])
    assert result.exit_code == 2
    assert result.stderr.startswith("error: Permission Error")


def test_sql_missing_file_exits_2(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["sql", str(tmp_path / "no.parquet"), "SELECT 1"])
    assert result.exit_code == 2
    assert result.stderr.startswith("error: IO Error")


def test_exportar_and_sql_agree(tmp_path: Path) -> None:
    salida = tmp_path / "medidas.parquet"
    runner.invoke(cli.app, ["exportar", str(write(tmp_path, TEXT)), str(salida)])
    result = runner.invoke(cli.app, ["sql", str(salida), "SELECT count(value) AS n FROM medidas"])
    assert cells(result.stdout) == [["6"]]


# --- Polars y DuckDB solo cuando hace falta ---


def test_columnar_is_not_reexported_from_core() -> None:
    import observatorio.core

    assert "columnar" not in observatorio.core.__all__
    assert not hasattr(observatorio.core, "query")


def test_importing_the_cli_does_not_load_polars_or_duckdb() -> None:
    # En otro proceso: en este, los tests de arriba ya han importado los dos.
    code = "import sys, observatorio.cli; print('polars' in sys.modules, 'duckdb' in sys.modules)"
    result = subprocess.run(
        [sys.executable, "-c", code], check=False, capture_output=True, text=True
    )
    assert result.stdout == "False False\n"
