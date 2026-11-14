"""Tests de la semana 29: extraer de PostgreSQL, transformar y guardar una instantánea.

Qué: comprueban core/etl.py contra el PostgreSQL de pruebas (la fixture `session` de la
semana 19), con tablas cuyo contenido se escribe a mano, y el comando `extraer`.
Para qué: un análisis vale lo que valen sus datos. Si la extracción pierde el orden, cambia
un tipo o trata un "sin dato" como cero, el notebook calcula con buena cara sobre datos
equivocados, y nadie lo ve en un gráfico.
Impacto: etl.py no se reexporta en core: la CLI arranca sin cargar pandas.
"""

import hashlib
import math
from pathlib import Path

import pandas as pd
import pytest
from hypothesis import given
from hypothesis import strategies as st
from sqlalchemy import update
from sqlalchemy.orm import Session
from typer.testing import CliRunner

from observatorio import cli
from observatorio.core import Scale, Series, save_series
from observatorio.core.database import Reading
from observatorio.core.etl import SNAPSHOT_COLUMNS, TYPES, extract, transform, write_snapshot

runner = CliRunner()

NAN = math.nan
SCALE = Scale("unidad", 10.0, 50.0)
# La instantánea de una carga con Norte 12,5, Sur sin dato y Norte 7,5, byte a byte.
SNAPSHOT = "carga,posicion,etiqueta,valor,nivel\n1,0,Norte,12.5,medio\n1,1,Sur,,sin dato\n"


def save(session: Session, *lines: str) -> int:
    """Guarda una carga con esas líneas y devuelve su número."""
    return save_series(session, "prueba.txt", Series.from_lines(list(lines))).id


def values(frame: pd.DataFrame, column: str) -> list[object]:
    """Los valores de una columna como lista, con None en lugar de NaN para poder comparar."""
    return [
        None if isinstance(value, float) and math.isnan(value) else value for value in frame[column]
    ]


def frame_of(rows: list[tuple[int, int, str, float]]) -> pd.DataFrame:
    """Una tabla como la que devuelve extract, con esas filas."""
    columns = ["load_id", "position", "label", "value"]
    return pd.DataFrame(rows, columns=columns).astype(TYPES)


# --- extract --------------------------------------------------------------------------


def test_extract_columns_and_types(session: Session) -> None:
    save(session, "Norte;12,5")
    frame = extract(session.connection())
    assert list(frame.columns) == ["load_id", "position", "label", "value"]
    assert frame.dtypes.astype(str).to_dict() == {
        "load_id": "int64",
        "position": "int64",
        "label": "str",
        "value": "float64",
    }


def test_extract_keeps_the_saved_order(session: Session) -> None:
    first = save(session, "Norte;12,5", "Sur;NA", "Norte;7,5")
    second = save(session, "Este;3")
    frame = extract(session.connection())
    assert values(frame, "load_id") == [first, first, first, second]
    assert values(frame, "position") == [0, 1, 2, 0]
    assert values(frame, "label") == ["Norte", "Sur", "Norte", "Este"]
    assert values(frame, "value") == [12.5, None, 7.5, 3.0]


def test_extract_orders_even_after_an_update(session: Session) -> None:
    # Sin ORDER BY, PostgreSQL devuelve las filas como estén guardadas en disco, y un
    # UPDATE escribe una copia nueva de la fila al final: la primera medida saldría la última.
    save(session, "Norte;12,5", "Sur;NA", "Norte;7,5")
    session.execute(update(Reading).where(Reading.position == 0).values(value=13.0))
    frame = extract(session.connection())
    assert values(frame, "position") == [0, 1, 2]
    assert values(frame, "value") == [13.0, None, 7.5]


def test_extract_one_load(session: Session) -> None:
    save(session, "Norte;12,5")
    second = save(session, "Este;3", "Oeste;4")
    frame = extract(session.connection(), second)
    assert values(frame, "label") == ["Este", "Oeste"]
    assert set(frame["load_id"]) == {second}


def test_extract_a_missing_load_is_empty(session: Session) -> None:
    save(session, "Norte;12,5")
    assert extract(session.connection(), 999).empty


def test_extract_an_empty_database_keeps_the_types(session: Session) -> None:
    frame = extract(session.connection())
    assert frame.empty
    assert frame["value"].dtype == "float64"
    assert frame["load_id"].dtype == "int64"


def test_extract_a_load_without_values_keeps_float(session: Session) -> None:
    # Sin `dtype`, una columna llena de NULL llega como object.
    load = save(session, "Sur;NA", "Sur;NA")
    frame = extract(session.connection(), load)
    assert frame["value"].dtype == "float64"
    assert frame["value"].isna().all()


# --- transform ------------------------------------------------------------------------


def test_transform_columns_in_spanish() -> None:
    snapshot = transform(frame_of([(1, 0, "Norte", 12.5)]), SCALE)
    assert list(snapshot.columns) == list(SNAPSHOT_COLUMNS.values())
    assert list(snapshot.columns) == ["carga", "posicion", "etiqueta", "valor", "nivel"]


def test_transform_adds_the_level() -> None:
    rows = [
        (1, 0, "A", 9.9),
        (1, 1, "A", 10.0),
        (1, 2, "A", 49.9),
        (1, 3, "A", 50.0),
        (1, 4, "A", NAN),
    ]
    snapshot = transform(frame_of(rows), SCALE)
    assert values(snapshot, "nivel") == ["bajo", "medio", "medio", "alto", "sin dato"]


def test_transform_keeps_the_rest() -> None:
    snapshot = transform(frame_of([(3, 7, "Sur", NAN)]), SCALE)
    assert values(snapshot, "carga") == [3]
    assert values(snapshot, "posicion") == [7]
    assert values(snapshot, "etiqueta") == ["Sur"]
    assert values(snapshot, "valor") == [None]


def test_transform_does_not_change_its_input() -> None:
    frame = frame_of([(1, 0, "Norte", 12.5)])
    transform(frame, SCALE)
    assert list(frame.columns) == ["load_id", "position", "label", "value"]


# --- write_snapshot -------------------------------------------------------------------


def snapshot_of(*rows: tuple[int, int, str, float]) -> pd.DataFrame:
    return transform(frame_of(list(rows)), SCALE)


def test_write_snapshot_writes_csv(tmp_path: Path) -> None:
    path = tmp_path / "instantanea.csv"
    write_snapshot(snapshot_of((1, 0, "Norte", 12.5), (1, 1, "Sur", NAN)), path)
    # Sin índice, un "sin dato" como celda vacía y "\n" al final de cada línea.
    assert path.read_bytes() == SNAPSHOT.encode()


def test_write_snapshot_returns_the_sha256_of_the_file(tmp_path: Path) -> None:
    path = tmp_path / "instantanea.csv"
    digest = write_snapshot(snapshot_of((1, 0, "Norte", 12.5), (1, 1, "Sur", NAN)), path)
    assert digest == hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest == hashlib.sha256(SNAPSHOT.encode()).hexdigest()


def test_write_snapshot_same_data_same_digest(tmp_path: Path) -> None:
    snapshot = snapshot_of((1, 0, "Norte", 12.5))
    assert write_snapshot(snapshot, tmp_path / "a.csv") == write_snapshot(
        snapshot, tmp_path / "b.csv"
    )


def test_write_snapshot_one_change_changes_the_digest(tmp_path: Path) -> None:
    before = write_snapshot(snapshot_of((1, 0, "Norte", 12.5)), tmp_path / "a.csv")
    after = write_snapshot(snapshot_of((1, 0, "Norte", 12.6)), tmp_path / "b.csv")
    assert before != after


LABELS = st.text(st.characters(codec="utf-8", exclude_categories=["Cs", "Cc"]), min_size=1)
VALUES = st.floats(allow_nan=False, allow_infinity=False) | st.just(NAN)


@given(st.lists(st.tuples(LABELS, VALUES), max_size=20))
def test_snapshot_reads_back_the_same(
    tmp_path_factory: pytest.TempPathFactory, rows: list[tuple[str, float]]
) -> None:
    # Con cualquier etiqueta (comas, comillas, "NA") y cualquier valor, el CSV devuelve lo
    # mismo si se lee como el notebook: sin convertir "NA" ni "null" en "sin dato".
    path = tmp_path_factory.mktemp("snapshot") / "instantanea.csv"
    snapshot = snapshot_of(
        *((1, position, label, value) for position, (label, value) in enumerate(rows))
    )
    write_snapshot(snapshot, path)
    back = pd.read_csv(
        path, keep_default_na=False, na_values={"valor": [""]}, dtype={"etiqueta": "str"}
    )
    assert values(back, "etiqueta") == values(snapshot, "etiqueta")
    assert values(back, "valor") == values(snapshot, "valor")


# --- extraer --------------------------------------------------------------------------


def test_extraer_all_loads(db_env: Path) -> None:
    runner.invoke(cli.app, ["guardar", "norte.txt", "este.csv"])
    result = runner.invoke(cli.app, ["extraer", "instantanea.csv"])
    assert result.exit_code == 0
    assert result.stdout.splitlines()[0] == "instantanea.csv: 4 medidas · cargas: 2"
    lines = (db_env / "instantanea.csv").read_text(encoding="utf-8").splitlines()
    assert lines == [
        "carga,posicion,etiqueta,valor,nivel",
        "1,0,Norte,12.5,medio",
        "1,1,Sur,,sin dato",
        "1,2,Norte,7.5,bajo",
        "2,0,Este,3.0,bajo",
    ]


def test_extraer_writes_the_digest_of_the_file(db_env: Path) -> None:
    runner.invoke(cli.app, ["guardar", "norte.txt"])
    result = runner.invoke(cli.app, ["extraer", "instantanea.csv"])
    digest = hashlib.sha256((db_env / "instantanea.csv").read_bytes()).hexdigest()
    assert result.stdout.splitlines()[1] == f"sha256: {digest}"


def test_extraer_one_load(db_env: Path) -> None:
    runner.invoke(cli.app, ["guardar", "norte.txt", "este.csv"])
    result = runner.invoke(cli.app, ["extraer", "solo.csv", "--carga", "2"])
    assert result.exit_code == 0
    assert result.stdout.splitlines()[0] == "solo.csv: 1 medidas · cargas: 1"
    assert (db_env / "solo.csv").read_text(encoding="utf-8").splitlines()[1:] == [
        "2,0,Este,3.0,bajo"
    ]


def test_extraer_a_missing_load(db_env: Path) -> None:
    runner.invoke(cli.app, ["guardar", "norte.txt"])
    result = runner.invoke(cli.app, ["extraer", "x.csv", "-c", "99"])
    assert result.exit_code == 1
    assert result.stderr == "error: no existe la carga 99\n"
    assert not (db_env / "x.csv").exists()


def test_extraer_without_measurements(db_env: Path) -> None:
    result = runner.invoke(cli.app, ["extraer", "x.csv"])
    assert result.exit_code == 1
    assert (
        result.stderr
        == "error: no hay medidas que extraer: guarda una carga con `observatorio guardar`\n"
    )
    assert not (db_env / "x.csv").exists()


def test_extraer_cannot_write(db_env: Path) -> None:
    runner.invoke(cli.app, ["guardar", "norte.txt"])
    result = runner.invoke(cli.app, ["extraer", "no/existe/x.csv"])
    assert result.exit_code == 2
    assert result.stderr.startswith("error: no se puede escribir no/existe/x.csv: ")
