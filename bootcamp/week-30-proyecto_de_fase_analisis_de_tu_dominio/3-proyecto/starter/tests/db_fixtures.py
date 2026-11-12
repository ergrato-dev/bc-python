"""Fixtures para probar con PostgreSQL: una base de pruebas, sesiones y la CLI.

Qué: `engine` crea desde cero la base de OBSERVATORIO_TEST_DATABASE_URL (por defecto,
observatorio_test en 127.0.0.1) y le aplica las migraciones, una vez por sesión de pytest;
`session` abre una transacción que se deshace al terminar cada test; `db_env` prepara la
CLI contra esa base, con las tablas vacías.
Para qué: los tests usan el PostgreSQL de verdad, con sus tipos y restricciones, y aun
así cada test empieza limpio.
Impacto: no es un archivo de tests (no empieza por test_). Tu conftest.py importa sus
fixtures, y así sirven en test_database.py y en tus tests.
"""

import os
from collections.abc import Iterator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import Connection, Engine, create_engine, make_url, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from observatorio.core import make_engine

TEST_URL = os.environ.get(
    "OBSERVATORIO_TEST_DATABASE_URL",
    "postgresql+psycopg://observatorio:observatorio@127.0.0.1:5432/observatorio_test",
)
ROOT = Path(__file__).parent.parent


def alembic_config(connection: Connection) -> Config:
    """La configuración de alembic.ini, con una conexión ya abierta: env.py la usa."""
    config = Config(ROOT / "alembic.ini")
    config.attributes["connection"] = connection
    return config


@pytest.fixture(scope="session")
def engine() -> Iterator[Engine]:
    """Una base de pruebas vacía, con las migraciones aplicadas, para toda la sesión."""
    url = make_url(TEST_URL)
    # CREATE DATABASE no puede ir dentro de una transacción: AUTOCOMMIT, contra la base
    # `postgres`, que siempre existe.
    admin = create_engine(url.set(database="postgres"), isolation_level="AUTOCOMMIT")
    try:
        with admin.connect() as connection:
            # Un nombre de base no puede ir como parámetro (%s): va entre comillas dobles,
            # y sale de tu configuración, no de lo que escribe un usuario.
            connection.execute(text(f'DROP DATABASE IF EXISTS "{url.database}" WITH (FORCE)'))
            connection.execute(text(f'CREATE DATABASE "{url.database}"'))
    except OperationalError:
        pytest.fail(
            f"no hay PostgreSQL en {url.host}:{url.port}: arráncalo con "
            "`docker compose up -d --wait db`",
            pytrace=False,
        )
    finally:
        admin.dispose()
    engine = make_engine(TEST_URL)
    with engine.begin() as connection:
        command.upgrade(alembic_config(connection), "head")
    yield engine
    engine.dispose()


@pytest.fixture
def session(engine: Engine) -> Iterator[Session]:
    """Una sesión dentro de una transacción que se deshace al terminar el test.

    join_transaction_mode="create_savepoint": un session.commit() del código que se
    prueba solo confirma un SAVEPOINT; el rollback final lo deshace todo igualmente.
    """
    with engine.connect() as connection:
        transaction = connection.begin()
        session = Session(bind=connection, join_transaction_mode="create_savepoint")
        yield session
        session.close()
        transaction.rollback()


@pytest.fixture
def db_env(tmp_path: Path, engine: Engine, monkeypatch: pytest.MonkeyPatch) -> Iterator[Path]:
    """Una carpeta vacía, sin .env, con la CLI apuntando a la base de pruebas.

    Vacía las tablas y reinicia los números (la primera carga vuelve a ser la 1), y deja
    dos archivos: norte.txt (Norte 12,5, Sur sin dato, Norte 7,5) y este.csv (Este 3).
    Al terminar las vuelve a vaciar: la CLI confirma de verdad, y lo que guarde no debe
    llegar a los tests de `session`, que esperan las tablas vacías.
    """
    monkeypatch.chdir(tmp_path)
    for name in ["TOKEN", "TIMEOUT", "RETRIES"]:
        monkeypatch.delenv(f"OBSERVATORIO_{name}", raising=False)
    monkeypatch.setenv("OBSERVATORIO_DATABASE_URL", TEST_URL)
    with engine.begin() as connection:
        connection.execute(text("TRUNCATE loads, readings RESTART IDENTITY"))
    (tmp_path / "norte.txt").write_text("Norte;12,5\nSur;NA\nNorte;7,5\n", encoding="utf-8")
    (tmp_path / "este.csv").write_text("etiqueta;valor\nEste;3\n", encoding="utf-8")
    yield tmp_path
    with engine.begin() as connection:
        connection.execute(text("TRUNCATE loads, readings RESTART IDENTITY"))
