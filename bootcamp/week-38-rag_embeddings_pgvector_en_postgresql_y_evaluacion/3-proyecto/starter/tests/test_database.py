"""Tests de la semana 19: guardar y consultar medidas en PostgreSQL.

Necesitan un PostgreSQL de verdad: `docker compose up -d --wait db`. Las fixtures
`engine`, `session` y `db_env` viven en db_fixtures.py, y tu conftest.py las importa para
que lleguen a todos los archivos de tests/ (paso 3).
"""

import configparser
from datetime import datetime
from pathlib import Path

import pytest
from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from db_fixtures import ROOT, TEST_URL, alembic_config
from psycopg import errors
from sqlalchemy import Engine, event, inspect, make_url, text
from sqlalchemy.exc import DataError, IntegrityError, OperationalError, ProgrammingError
from sqlalchemy.orm import Session
from typer.testing import CliRunner

from observatorio import cli
from observatorio.core import (
    Base,
    LabelStats,
    Load,
    Measurement,
    Reading,
    Series,
    delete_load,
    label_stats,
    list_loads,
    load_series,
    make_engine,
    save_series,
)
from observatorio.settings import Settings

runner = CliRunner()

NORTE_SUR = Series(
    [Measurement("Norte", 12.5), Measurement("Sur", None), Measurement("Norte", 7.5)]
)


def count_queries(session: Session) -> list[str]:
    """Una lista que se llena con cada SQL que la sesión envía a PostgreSQL."""
    statements: list[str] = []
    connection = session.connection()

    def remember(*args: object) -> None:
        statements.append(str(args[2]))

    event.listen(connection, "before_cursor_execute", remember)
    return statements


# --- Los modelos ----------------------------------------------------------------------


def test_the_models_declare_three_tables() -> None:
    # La tercera, notes, la declara rag.py (semana 38), y migrations/env.py lo importa.
    import observatorio.core.rag  # noqa: F401

    assert set(Base.metadata.tables) == {"loads", "readings", "notes"}


def test_readings_columns_and_nulls() -> None:
    columns = Base.metadata.tables["readings"].columns
    assert [column.name for column in columns] == ["id", "load_id", "position", "label", "value"]
    assert columns["value"].nullable is True
    assert columns["label"].nullable is False
    assert columns["position"].nullable is False


def test_loads_created_at_is_set_by_the_server() -> None:
    created_at = Base.metadata.tables["loads"].columns["created_at"]
    assert created_at.server_default is not None
    assert created_at.nullable is False


def test_constraints_have_fixed_names() -> None:
    readings = Base.metadata.tables["readings"]
    names = {constraint.name for constraint in readings.constraints}
    assert {"pk_readings", "fk_readings_load_id_loads", "uq_readings_load_id_position"} <= names
    assert {index.name for index in readings.indexes} == {"ix_readings_load_id"}


def test_deleting_a_load_cascades_in_the_database() -> None:
    (foreign_key,) = Base.metadata.tables["readings"].foreign_keys
    assert foreign_key.ondelete == "CASCADE"


# --- make_engine ----------------------------------------------------------------------


def test_make_engine_uses_psycopg_3() -> None:
    engine = make_engine("postgresql+psycopg://usuario:clave@localhost/base")
    assert engine.dialect.driver == "psycopg"


def test_make_engine_hides_the_password() -> None:
    engine = make_engine("postgresql+psycopg://usuario:clave@localhost/base")
    assert "clave" not in repr(engine)
    assert "clave" not in str(engine.url)


def test_make_engine_echo() -> None:
    url = "postgresql+psycopg://usuario:clave@localhost/base"
    assert make_engine(url).echo is False
    assert make_engine(url, echo=True).echo is True


def test_make_engine_does_not_connect_yet() -> None:
    # create_engine no abre ninguna conexión: la primera se abre al usarlo.
    engine = make_engine("postgresql+psycopg://usuario:clave@127.0.0.1:1/base")
    with pytest.raises(OperationalError):
        engine.connect()


# --- save_series y load_series ---------------------------------------------------------


def test_save_series_assigns_an_id(session: Session) -> None:
    load = save_series(session, "norte.txt", NORTE_SUR)
    assert isinstance(load.id, int)
    assert load.source == "norte.txt"


def test_save_series_keeps_the_order(session: Session) -> None:
    load = save_series(session, "norte.txt", NORTE_SUR)
    assert [reading.position for reading in load.readings] == [0, 1, 2]
    assert [reading.label for reading in load.readings] == ["Norte", "Sur", "Norte"]


def test_save_series_stores_missing_values_as_null(session: Session) -> None:
    save_series(session, "norte.txt", NORTE_SUR)
    nulls = session.execute(text("SELECT count(*) FROM readings WHERE value IS NULL"))
    assert nulls.scalar_one() == 1


def test_save_series_sets_created_at_with_time_zone(session: Session) -> None:
    load = save_series(session, "norte.txt", NORTE_SUR)
    session.refresh(load)
    assert isinstance(load.created_at, datetime)
    assert load.created_at.tzinfo is not None


def test_save_series_with_an_empty_series(session: Session) -> None:
    load = save_series(session, "vacio.txt", Series())
    assert load.readings == []
    assert load_series(session, load.id) == Series()


def test_save_series_does_not_commit(session: Session, monkeypatch: pytest.MonkeyPatch) -> None:
    def no_commit() -> None:
        raise AssertionError("save_series no debe hacer commit: lo decide quien abre la sesión")

    monkeypatch.setattr(session, "commit", no_commit)
    save_series(session, "norte.txt", NORTE_SUR)


def test_load_series_round_trip(session: Session) -> None:
    load = save_series(session, "norte.txt", NORTE_SUR)
    session.expire_all()
    assert load_series(session, load.id) == NORTE_SUR


def test_load_series_of_a_missing_load(session: Session) -> None:
    assert load_series(session, 999_999) is None


def test_two_loads_do_not_mix(session: Session) -> None:
    first = save_series(session, "a.txt", Series([Measurement("A", 1.0)]))
    second = save_series(session, "b.txt", Series([Measurement("B", 2.0)]))
    assert load_series(session, first.id) == Series([Measurement("A", 1.0)])
    assert load_series(session, second.id) == Series([Measurement("B", 2.0)])


# --- list_loads -----------------------------------------------------------------------


def test_list_loads_empty(session: Session) -> None:
    assert list_loads(session) == []


def test_list_loads_counts_measurements(session: Session) -> None:
    first = save_series(session, "a.txt", NORTE_SUR)
    second = save_series(session, "b.txt", Series())
    loads = list_loads(session)
    assert [(info.id, info.source, info.measurements) for info in loads] == [
        (first.id, "a.txt", 3),
        (second.id, "b.txt", 0),
    ]


def test_list_loads_is_one_query(session: Session) -> None:
    for name in ["a.txt", "b.txt", "c.txt"]:
        save_series(session, name, NORTE_SUR)
    statements = count_queries(session)
    list_loads(session)
    assert len(statements) == 1
    assert "GROUP BY" in statements[0]


# --- label_stats ----------------------------------------------------------------------


def test_label_stats_groups_by_label(session: Session) -> None:
    save_series(session, "a.txt", NORTE_SUR)
    assert label_stats(session) == [
        LabelStats("Norte", 2, 2, 10.0),
        LabelStats("Sur", 1, 0, None),
    ]


def test_label_stats_of_all_loads(session: Session) -> None:
    save_series(session, "a.txt", NORTE_SUR)
    save_series(session, "b.txt", Series([Measurement("Norte", 40.0), Measurement("Este", 3.0)]))
    assert label_stats(session) == [
        LabelStats("Este", 1, 1, 3.0),
        LabelStats("Norte", 3, 3, 20.0),
        LabelStats("Sur", 1, 0, None),
    ]


def test_label_stats_of_one_load(session: Session) -> None:
    save_series(session, "a.txt", NORTE_SUR)
    second = save_series(session, "b.txt", Series([Measurement("Norte", 40.0)]))
    assert label_stats(session, second.id) == [LabelStats("Norte", 1, 1, 40.0)]


def test_label_stats_empty(session: Session) -> None:
    assert label_stats(session) == []


def test_label_stats_is_one_query(session: Session) -> None:
    save_series(session, "a.txt", NORTE_SUR)
    statements = count_queries(session)
    label_stats(session)
    assert len(statements) == 1
    assert "avg" in statements[0].lower()


# --- delete_load ----------------------------------------------------------------------


def test_delete_load_removes_its_readings(session: Session) -> None:
    load = save_series(session, "a.txt", NORTE_SUR)
    other = save_series(session, "b.txt", Series([Measurement("Este", 3.0)]))
    assert delete_load(session, load.id) is True
    assert load_series(session, load.id) is None
    remaining = session.execute(text("SELECT count(*) FROM readings")).scalar_one()
    assert remaining == 1
    assert load_series(session, other.id) == Series([Measurement("Este", 3.0)])


def test_delete_load_of_a_missing_load(session: Session) -> None:
    assert delete_load(session, 999_999) is False


def test_delete_with_sql_also_cascades(session: Session) -> None:
    load = save_series(session, "a.txt", NORTE_SUR)
    session.execute(text("DELETE FROM loads WHERE id = :id"), {"id": load.id})
    remaining = session.execute(text("SELECT count(*) FROM readings")).scalar_one()
    assert remaining == 0


# --- Las restricciones las comprueba PostgreSQL ---------------------------------------


def test_two_readings_cannot_share_a_position(session: Session) -> None:
    load = save_series(session, "a.txt", NORTE_SUR)
    session.add(Reading(load_id=load.id, position=0, label="Otra", value=1.0))
    with pytest.raises(IntegrityError) as caught:
        session.flush()
    assert isinstance(caught.value.orig, errors.UniqueViolation)


def test_a_reading_needs_an_existing_load(session: Session) -> None:
    session.add(Reading(load_id=999_999, position=0, label="Norte", value=1.0))
    with pytest.raises(IntegrityError) as caught:
        session.flush()
    assert isinstance(caught.value.orig, errors.ForeignKeyViolation)


def test_a_label_has_at_most_100_characters(session: Session) -> None:
    session.add(Load(source="a.txt", readings=[Reading(position=0, label="x" * 101)]))
    with pytest.raises(DataError) as caught:
        session.flush()
    assert isinstance(caught.value.orig, errors.StringDataRightTruncation)


def test_parameters_are_never_sql(session: Session) -> None:
    # Una etiqueta con SQL dentro se guarda como texto: nunca se ejecuta.
    evil = "x'); DROP TABLE readings; --"
    load = save_series(session, "a.txt", Series([Measurement(evil, 1.0)]))
    assert load_series(session, load.id) == Series([Measurement(evil, 1.0)])
    assert inspect(session.connection()).has_table("readings")


# --- Las migraciones ------------------------------------------------------------------


def test_the_migrations_match_the_models(engine: Engine) -> None:
    # Lo mismo que `alembic check`: si cambias un modelo sin migración, falla aquí.
    with engine.connect() as connection:
        differences = compare_metadata(MigrationContext.configure(connection), Base.metadata)
    assert differences == []


def test_there_is_one_head_and_it_is_0002(engine: Engine) -> None:
    with engine.connect() as connection:
        script = ScriptDirectory.from_config(alembic_config(connection))
    assert script.get_heads() == ["0002"]


def test_the_database_is_at_head(engine: Engine) -> None:
    with engine.connect() as connection:
        assert MigrationContext.configure(connection).get_current_revision() == "0002"


def test_downgrade_and_upgrade_again(engine: Engine) -> None:
    # Todo dentro de una transacción que se deshace: en PostgreSQL, CREATE y DROP TABLE
    # también son transaccionales.
    with engine.connect() as connection:
        transaction = connection.begin()
        command.downgrade(alembic_config(connection), "base")
        assert not inspect(connection).has_table("readings")
        assert not inspect(connection).has_table("loads")
        assert not inspect(connection).has_table("notes")
        command.upgrade(alembic_config(connection), "head")
        assert inspect(connection).has_table("readings")
        transaction.rollback()


def test_alembic_ini_has_no_database_url() -> None:
    # alembic.ini va a Git: la URL, con su contraseña, llega por OBSERVATORIO_DATABASE_URL.
    parser = configparser.ConfigParser(interpolation=None)
    parser.read(ROOT / "alembic.ini", encoding="utf-8")
    assert "sqlalchemy.url" not in parser["alembic"]


# --- Settings -------------------------------------------------------------------------


@pytest.fixture
def clean_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Una carpeta de trabajo vacía, sin .env, y sin variables OBSERVATORIO_* de tu máquina."""
    monkeypatch.chdir(tmp_path)
    for name in ["TOKEN", "TIMEOUT", "RETRIES", "DATABASE_URL"]:
        monkeypatch.delenv(f"OBSERVATORIO_{name}", raising=False)
    return tmp_path


def test_settings_database_url_defaults_to_none(clean_env: Path) -> None:
    assert Settings().database_url is None


def test_settings_database_url_is_secret(clean_env: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OBSERVATORIO_DATABASE_URL", "postgresql+psycopg://u:clave@h/base")
    settings = Settings()
    assert settings.database_url is not None
    assert settings.database_url.get_secret_value() == "postgresql+psycopg://u:clave@h/base"
    assert "clave" not in repr(settings)


def test_settings_database_url_from_dotenv(clean_env: Path) -> None:
    (clean_env / ".env").write_text(
        "OBSERVATORIO_DATABASE_URL=postgresql+psycopg://u:clave@h/base\n", encoding="utf-8"
    )
    settings = Settings()
    assert settings.database_url is not None
    assert settings.database_url.get_secret_value().endswith("@h/base")


# --- La CLI ---------------------------------------------------------------------------


def test_guardar_saves_each_file(db_env: Path, engine: Engine) -> None:
    result = runner.invoke(cli.app, ["guardar", "norte.txt", "este.csv"])
    assert result.exit_code == 0, result.output
    assert result.stdout.splitlines() == [
        "carga 1: norte.txt, 3 medidas",
        "carga 2: este.csv, 1 medidas",
    ]
    with Session(engine) as session:
        assert load_series(session, 1) == NORTE_SUR


def test_guardar_keeps_going_after_a_bad_file(db_env: Path, engine: Engine) -> None:
    result = runner.invoke(cli.app, ["guardar", "norte.txt", "falta.txt", "este.csv"])
    assert result.exit_code == 1
    assert "error: no existe el archivo falta.txt" in result.stderr
    assert "carga 2: este.csv, 1 medidas" in result.stdout
    with Session(engine) as session:
        assert [info.source for info in list_loads(session)] == ["norte.txt", "este.csv"]


def test_guardar_commits_for_real(db_env: Path, engine: Engine) -> None:
    runner.invoke(cli.app, ["guardar", "norte.txt"])
    # Otra conexión, otra sesión: lo ve porque la CLI hizo commit.
    with engine.connect() as connection:
        assert connection.execute(text("SELECT count(*) FROM readings")).scalar_one() == 3


def test_cargas_without_loads(db_env: Path) -> None:
    result = runner.invoke(cli.app, ["cargas"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "no hay cargas: guarda una con `observatorio guardar`"


def test_cargas_lists_the_loads(db_env: Path) -> None:
    runner.invoke(cli.app, ["guardar", "norte.txt", "este.csv"])
    result = runner.invoke(cli.app, ["cargas"])
    assert result.exit_code == 0
    rows = [line for line in result.stdout.splitlines() if line.startswith("│")]
    cells = [[cell.strip() for cell in row.strip("│").split("│")] for row in rows]
    assert [(cell[0], cell[1], cell[3]) for cell in cells] == [
        ("1", "norte.txt", "3"),
        ("2", "este.csv", "1"),
    ]
    assert all(datetime.strptime(cell[2], "%Y-%m-%d %H:%M") for cell in cells)


def test_consultar_all_loads(db_env: Path) -> None:
    runner.invoke(cli.app, ["guardar", "norte.txt", "este.csv"])
    result = runner.invoke(cli.app, ["consultar"])
    assert result.exit_code == 0
    assert "│ Este     │       1 │         1 │  3.0 unidad │" in result.stdout
    assert "│ Norte    │       2 │         2 │ 10.0 unidad │" in result.stdout
    assert "│ Sur      │       1 │         0 │    sin dato │" in result.stdout


def test_consultar_one_load(db_env: Path) -> None:
    runner.invoke(cli.app, ["guardar", "norte.txt", "este.csv"])
    result = runner.invoke(cli.app, ["consultar", "--carga", "2"])
    assert result.exit_code == 0
    assert "Este" in result.stdout
    assert "Norte" not in result.stdout


def test_consultar_a_missing_load(db_env: Path) -> None:
    result = runner.invoke(cli.app, ["consultar", "-c", "99"])
    assert result.exit_code == 1
    assert result.stderr == "error: no existe la carga 99\n"


def test_borrar_a_load(db_env: Path) -> None:
    runner.invoke(cli.app, ["guardar", "norte.txt", "este.csv"])
    result = runner.invoke(cli.app, ["borrar", "1"])
    assert result.exit_code == 0
    assert result.stdout == "carga 1 borrada\n"
    remaining = runner.invoke(cli.app, ["cargas"])
    assert "norte.txt" not in remaining.stdout
    assert "este.csv" in remaining.stdout


def test_borrar_a_missing_load(db_env: Path) -> None:
    result = runner.invoke(cli.app, ["borrar", "99"])
    assert result.exit_code == 1
    assert result.stderr == "error: no existe la carga 99\n"


def test_cli_without_database_url(clean_env: Path) -> None:
    result = runner.invoke(cli.app, ["cargas"])
    assert result.exit_code == 2
    assert result.stderr == "error: falta OBSERVATORIO_DATABASE_URL (en el entorno o en .env)\n"


def test_cli_with_an_invalid_url(clean_env: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OBSERVATORIO_DATABASE_URL", "no es una url")
    result = runner.invoke(cli.app, ["cargas"])
    assert result.exit_code == 2
    assert "no es una URL de base de datos válida" in result.stderr


def test_cli_when_postgres_is_not_there(clean_env: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    url = make_url(TEST_URL).set(port=1)
    monkeypatch.setenv("OBSERVATORIO_DATABASE_URL", url.render_as_string(hide_password=False))
    result = runner.invoke(cli.app, ["cargas"])
    assert result.exit_code == 2
    assert result.stderr == f"error: no se pudo conectar con PostgreSQL en {url.host}:1\n"
    assert url.password is not None
    assert url.password not in result.output


def test_cli_without_tables(
    clean_env: Path, engine: Engine, monkeypatch: pytest.MonkeyPatch
) -> None:
    # La base `postgres` existe siempre y no tiene las tablas del Observatorio.
    url = make_url(TEST_URL).set(database="postgres")
    monkeypatch.setenv("OBSERVATORIO_DATABASE_URL", url.render_as_string(hide_password=False))
    result = runner.invoke(cli.app, ["cargas"])
    assert result.exit_code == 2
    assert result.stderr == "error: faltan las tablas: ejecuta `uv run alembic upgrade head`\n"


def test_cli_other_database_errors_are_not_hidden(
    db_env: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def broken(session: Session) -> list[object]:
        raise ProgrammingError("SELECT", {}, Exception("otro problema"))

    monkeypatch.setattr(cli, "list_loads", broken)
    result = runner.invoke(cli.app, ["cargas"])
    assert isinstance(result.exception, ProgrammingError)


def test_help_lists_the_database_commands() -> None:
    result = runner.invoke(cli.app, ["--help"])
    for name in ["guardar", "cargas", "consultar", "borrar"]:
        assert name in result.stdout
