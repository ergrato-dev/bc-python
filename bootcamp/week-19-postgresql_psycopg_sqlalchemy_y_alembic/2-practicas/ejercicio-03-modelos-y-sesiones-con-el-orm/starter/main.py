"""Ejercicio 03 · Modelos y sesiones con el ORM de SQLAlchemy 2.

Antes de ejecutar, arranca el PostgreSQL de las prácticas: `docker compose up -d --wait`.
Cada ejecución borra y vuelve a crear las tablas: puedes repetir sin miedo.
"""

from sqlalchemy import ForeignKey, String, create_engine, event, func, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
    selectinload,
)
from sqlalchemy.orm.exc import DetachedInstanceError

URL = "postgresql+psycopg://practicas:practicas@127.0.0.1:5433/practicas"

print("Ejercicio 03 · Modelos y sesiones con el ORM")

engine = create_engine(URL)

# Cada SQL que el motor envía se apunta aquí: así se ve cuántas consultas cuesta algo.
sent: list[str] = []


@event.listens_for(engine, "before_cursor_execute")
def remember(conn: object, cursor: object, statement: str, *args: object) -> None:
    sent.append(statement)


class Base(DeclarativeBase):
    pass


# ============================================
# PASO 1: Dos modelos
# ============================================
# Descomenta las siguientes líneas:
# class Station(Base):
#     __tablename__ = "stations"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(50), unique=True)
#     altitude: Mapped[int | None]
#     readings: Mapped[list[Reading]] = relationship(
#         back_populates="station", cascade="all, delete-orphan"
#     )
#
#     def __repr__(self) -> str:
#         return f"Station({self.name!r})"
#
#
# class Reading(Base):
#     __tablename__ = "readings"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     station_id: Mapped[int] = mapped_column(ForeignKey("stations.id"))
#     value: Mapped[float | None]
#     station: Mapped[Station] = relationship(back_populates="readings")
#
#
# for column in Station.__table__.columns:
#     print(f"{column.name}: {column.type} · ¿admite NULL? {column.nullable}")
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)


# ============================================
# PASO 2: Guardar objetos
# ============================================
# Descomenta las siguientes líneas:
# with Session(engine) as session:
#     north = Station(name="Norte", altitude=2600, readings=[Reading(value=12.5)])
#     north.readings.append(Reading(value=7.5))
#     south = Station(name="Sur", altitude=1500)
#     south.readings += [Reading(value=30.0), Reading(value=None)]
#     session.add_all([north, south, Station(name="Este")])
#     print("antes del commit, id de Norte:", north.id)
#     session.commit()
#     print("después del commit, id de Norte:", north.id)


# ============================================
# PASO 3: Consultar objetos
# ============================================
# Descomenta las siguientes líneas:
# with Session(engine) as session:
#     stations = session.scalars(select(Station).order_by(Station.name)).all()
#     print("todas:", stations)
#     high = session.scalars(select(Station).where(Station.altitude > 2000)).one()
#     print("la alta:", high, high.altitude)
#     print("get(2):", session.get(Station, 2), "· get(99):", session.get(Station, 99))


# ============================================
# PASO 4: El mapa de identidad
# ============================================
# Descomenta las siguientes líneas:
# with Session(engine) as session:
#     sent.clear()
#     first = session.get(Station, 1)
#     second = session.get(Station, 1)
#     print("¿el mismo objeto?", first is second, "· consultas:", len(sent))


# ============================================
# PASO 5: La unidad de trabajo
# ============================================
# Descomenta las siguientes líneas:
# with Session(engine) as session:
#     north = session.scalars(select(Station).where(Station.name == "Norte")).one()
#     north.altitude = 2650
#     print("pendiente de guardar:", session.dirty)
#     sent.clear()
#     session.commit()
#     print("SQL del commit:", [statement.split()[0] for statement in sent])
#     sent.clear()
#     print("altitud:", north.altitude, "· consultas para leerla:", len(sent))


# ============================================
# PASO 6: Relaciones
# ============================================
# Descomenta las siguientes líneas:
# with Session(engine) as session:
#     south = session.scalars(select(Station).where(Station.name == "Sur")).one()
#     sent.clear()
#     print("medidas de Sur:", [reading.value for reading in south.readings])
#     print("consultas al tocar .readings:", len(sent))
#     reading = south.readings[0]
#     print("de la medida a su estación:", reading.station, reading.station is south)


# ============================================
# PASO 7: El problema N+1
# ============================================
# Descomenta las siguientes líneas:
# with Session(engine) as session:
#     sent.clear()
#     for station in session.scalars(select(Station).order_by(Station.id)):
#         print(f"{station.name}: {len(station.readings)} medidas")
#     print("consultas, sin selectinload:", len(sent))
# with Session(engine) as session:
#     sent.clear()
#     query = select(Station).options(selectinload(Station.readings)).order_by(Station.id)
#     for station in session.scalars(query):
#         len(station.readings)
#     print("consultas, con selectinload:", len(sent))


# ============================================
# PASO 8: Que cuente PostgreSQL
# ============================================
# Descomenta las siguientes líneas:
# summary = (
#     select(Station.name, func.count(Reading.id), func.avg(Reading.value))
#     .outerjoin(Station.readings)
#     .group_by(Station.name)
#     .order_by(Station.name)
# )
# with Session(engine) as session:
#     sent.clear()
#     for name, count, mean in session.execute(summary):
#         print(f"{name}: {count} medidas, media {mean}")
#     print("consultas:", len(sent))


# ============================================
# PASO 9: Borrar en cascada
# ============================================
# Descomenta las siguientes líneas:
# with Session(engine) as session:
#     south = session.scalars(select(Station).where(Station.name == "Sur")).one()
#     session.delete(south)
#     sent.clear()
#     session.commit()
#     print("SQL del borrado:", [statement.split()[0] for statement in sent])
#     left = session.scalar(select(func.count()).select_from(Reading))
#     print("medidas que quedan:", left)


# ============================================
# PASO 10: Un objeto fuera de su sesión
# ============================================
# Descomenta las siguientes líneas:
# with Session(engine) as session:
#     east = session.scalars(select(Station).where(Station.name == "Este")).one()
# print("fuera del with, el nombre:", east.name)
# try:
#     print(east.readings)
# except DetachedInstanceError as problem:
#     print("DetachedInstanceError:", str(problem).split(";")[1].split("(")[0].strip())
