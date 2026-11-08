"""Ejercicio 04 · Cómo está la base de datos: revisión, columnas y filas de `stations`.

Ejecútalo después de cada `alembic upgrade` o `downgrade`: `uv run python main.py`.
Si la tabla existe y está vacía, añade dos estaciones, para que las migraciones
siguientes encuentren datos de verdad.
"""

from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine, inspect, text

from models import URL

engine = create_engine(URL)
with engine.begin() as conn:
    revision = MigrationContext.configure(conn).get_current_revision()
    print("revisión:", revision)
    if not inspect(conn).has_table("stations"):
        print("todavía no existe la tabla stations")
    else:
        columns = inspect(conn).get_columns("stations")
        print("columnas:", ", ".join(f"{c['name']} {c['type']}" for c in columns))
        if conn.execute(text("SELECT count(*) FROM stations")).scalar_one() == 0:
            conn.execute(text("INSERT INTO stations (name) VALUES ('Norte'), ('Sur')"))
        for row in conn.execute(text("SELECT * FROM stations ORDER BY id")):
            print("fila:", dict(row._mapping))
engine.dispose()
