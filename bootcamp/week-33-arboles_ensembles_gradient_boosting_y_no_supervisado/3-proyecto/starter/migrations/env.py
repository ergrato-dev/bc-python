"""Alembic: con qué base de datos y con qué modelos se ejecutan las migraciones.

Qué: lee la URL de Settings (OBSERVATORIO_DATABASE_URL) y compara con Base.metadata.
Para qué: `alembic revision --autogenerate` saca de los modelos lo que falta en la base,
y `alembic upgrade head` lo aplica, siempre con la misma URL que usa la CLI.
Impacto: los tests pasan su propia conexión en config.attributes["connection"]; así
migran la base de pruebas sin tocar tu .env ni el registro de pytest.
"""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import Connection

from observatorio.core.database import Base, make_engine
from observatorio.settings import Settings

config = context.config
connection: Connection | None = config.attributes.get("connection")

# El registro de alembic.ini, solo desde la terminal: en los tests lo configura pytest.
if config.config_file_name is not None and connection is None:
    fileConfig(config.config_file_name, disable_existing_loggers=False)


def database_url() -> str:
    """La URL de OBSERVATORIO_DATABASE_URL; sin ella no hay nada que migrar."""
    url = Settings().database_url
    if url is None:
        raise SystemExit("error: falta OBSERVATORIO_DATABASE_URL (en el entorno o en .env)")
    return url.get_secret_value()


def run_migrations(connection: Connection) -> None:
    """Aplica las migraciones pendientes en una transacción de esa conexión."""
    context.configure(connection=connection, target_metadata=Base.metadata)
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    # `alembic upgrade head --sql`: escribe el SQL en pantalla en lugar de ejecutarlo.
    context.configure(url=database_url(), target_metadata=Base.metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
elif connection is not None:
    run_migrations(connection)
else:
    with make_engine(database_url()).connect() as new_connection:
        run_migrations(new_connection)
