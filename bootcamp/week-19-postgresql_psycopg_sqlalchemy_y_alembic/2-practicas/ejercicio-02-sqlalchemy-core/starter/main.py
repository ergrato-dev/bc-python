"""Ejercicio 02 · SQLAlchemy Core: el motor, las conexiones, las tablas y las consultas.

Antes de ejecutar, arranca el PostgreSQL de las prácticas: `docker compose up -d --wait`.
Cada ejecución borra y vuelve a crear las tablas: puedes repetir sin miedo.
"""

import logging
import sys

from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    delete,
    func,
    insert,
    select,
    text,
    update,
)
from sqlalchemy.schema import CreateTable

# `+psycopg`: el driver de SQLAlchemy es psycopg 3, el del ejercicio 01.
URL = "postgresql+psycopg://practicas:practicas@127.0.0.1:5433/practicas"

print("Ejercicio 02 · SQLAlchemy Core")

engine = create_engine(URL)

metadata = MetaData()
stations = Table(
    "stations",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False, unique=True),
    Column("altitude", Integer),
)
readings = Table(
    "readings",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("station_id", ForeignKey("stations.id"), nullable=False),
    Column("value", Float),
)
metadata.drop_all(engine)


# ============================================
# PASO 1: El motor no es una conexión
# ============================================
# Descomenta las siguientes líneas:
# print("motor:", engine)
# print("driver:", engine.dialect.name, "+", engine.dialect.driver)
# print("pool:", engine.pool.status())


# ============================================
# PASO 2: Una conexión y text()
# ============================================
# Descomenta las siguientes líneas:
# with engine.connect() as conn:
#     total = conn.execute(text("SELECT :a + :b"), {"a": 2, "b": 3}).scalar_one()
#     print("2 + 3 =", total)
#     conn.execute(text("CREATE TABLE notes (body text)"))
#     conn.execute(text("INSERT INTO notes VALUES ('sin commit')"))
# with engine.connect() as conn:
#     exists = conn.execute(text("SELECT to_regclass('notes') IS NOT NULL")).scalar_one()
#     print("¿existe notes sin commit?", exists)
# print("pool:", engine.pool.status())


# ============================================
# PASO 3: begin() confirma solo
# ============================================
# Descomenta las siguientes líneas:
# with engine.begin() as conn:
#     conn.execute(text("CREATE TABLE notes (body text)"))
#     notes = [{"body": "a"}, {"body": "b"}]
#     conn.execute(text("INSERT INTO notes VALUES (:body)"), notes)
# with engine.connect() as conn:
#     print("notas:", conn.execute(text("SELECT count(*) FROM notes")).scalar_one())
# try:
#     with engine.begin() as conn:
#         conn.execute(text("INSERT INTO notes VALUES ('c')"))
#         raise RuntimeError("algo falla a mitad")
# except RuntimeError as problem:
#     print("RuntimeError:", problem)
# with engine.begin() as conn:
#     print("notas:", conn.execute(text("SELECT count(*) FROM notes")).scalar_one())
#     conn.execute(text("DROP TABLE notes"))


# ============================================
# PASO 4: Tablas como objetos de Python
# ============================================
# Descomenta las siguientes líneas:
# print(CreateTable(readings).compile(engine))
# metadata.create_all(engine)
# print("tablas:", sorted(metadata.tables))


# ============================================
# PASO 5: insert()
# ============================================
# Descomenta las siguientes líneas:
# with engine.begin() as conn:
#     new: list[dict[str, object]] = [
#         {"name": "Norte", "altitude": 2600},
#         {"name": "Sur", "altitude": 1500},
#         {"name": "Este", "altitude": None},
#     ]
#     ids = conn.execute(insert(stations).returning(stations.c.id), new).scalars().all()
#     print("ids:", ids)
#     values = [(1, 12.5), (1, 7.5), (2, 30.0), (2, None), (1, 20.0)]
#     measured = [{"station_id": station, "value": value} for station, value in values]
#     conn.execute(insert(readings), measured)


# ============================================
# PASO 6: select()
# ============================================
# Descomenta las siguientes líneas:
# query = (
#     select(stations.c.name, stations.c.altitude)
#     .where(stations.c.altitude > 2000)
#     .order_by(stations.c.name)
# )
# print("SQL:", query)
# with engine.connect() as conn:
#     for row in conn.execute(query):
#         print("fila:", row, "· nombre:", row.name, "· como dict:", row._mapping)
#     by_id = select(stations.c.name).order_by(stations.c.id)
#     names = conn.execute(by_id).scalars().all()
#     print("solo nombres:", names)


# ============================================
# PASO 7: JOIN y GROUP BY
# ============================================
# Descomenta las siguientes líneas:
# summary = (
#     select(
#         stations.c.name,
#         func.count(readings.c.id).label("measurements"),
#         func.count(readings.c.value).label("with_value"),
#         func.avg(readings.c.value).label("mean"),
#     )
#     .select_from(stations)
#     .outerjoin(readings)
#     .group_by(stations.c.name)
#     .order_by(stations.c.name)
# )
# print("SQL:", summary.compile(engine))
# with engine.connect() as conn:
#     for row in conn.execute(summary):
#         counts = f"{row.measurements} medidas, {row.with_value} con valor"
#         print(f"{row.name}: {counts}, media {row.mean}")


# ============================================
# PASO 8: update() y delete()
# ============================================
# Descomenta las siguientes líneas:
# with engine.begin() as conn:
#     changed = conn.execute(
#         update(stations).where(stations.c.altitude.is_(None)).values(altitude=0)
#     )
#     print("actualizadas:", changed.rowcount)
#     removed = conn.execute(delete(readings).where(readings.c.value.is_(None)))
#     print("borradas:", removed.rowcount)
#     left = conn.execute(select(func.count()).select_from(readings)).scalar_one()
#     print("medidas que quedan:", left)


# ============================================
# PASO 9: Ver el SQL que se envía
# ============================================
# Descomenta las siguientes líneas:
# logging.basicConfig(stream=sys.stdout, format="LOG %(message)s")
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
# with engine.connect() as conn:
#     conn.execute(select(stations.c.name).where(stations.c.id == 2)).scalar_one()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


# ============================================
# PASO 10: El pool de conexiones
# ============================================
# Descomenta las siguientes líneas:
# first = engine.connect()
# second = engine.connect()
# print("pool:", engine.pool.status())
# first.close()
# second.close()
# print("pool:", engine.pool.status())
# engine.dispose()
# print("después de dispose:", engine.pool.status())
