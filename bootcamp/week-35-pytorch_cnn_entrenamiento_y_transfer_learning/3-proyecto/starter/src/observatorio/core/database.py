"""Guardar series en PostgreSQL y consultarlas, con SQLAlchemy 2.

Qué: dos tablas (`loads`, una por cada archivo guardado, y `readings`, una por medida)
declaradas como clases, y las funciones que guardan, leen, resumen y borran cargas.
Para qué: un archivo vive en una máquina y se lee entero cada vez; una base de datos la
comparten varios programas, y PostgreSQL agrupa y cuenta sin traer las filas a Python.
Impacto: el núcleo recibe la URL y la sesión como argumentos y no lee el entorno. Las
funciones no hacen commit: quien abre la sesión decide cuándo se confirma la transacción.
"""

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Engine,
    ForeignKey,
    MetaData,
    String,
    UniqueConstraint,
    create_engine,
    func,
    select,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

from observatorio.core.model import Measurement, Series


class Base(DeclarativeBase):
    """La base de los modelos: su `metadata` reúne las tablas, y Alembic la compara."""

    # Nombres fijos para índices y restricciones (pk_loads, fk_readings_load_id_loads...).
    # Sin ellos, PostgreSQL inventa uno, y una migración futura no sabría cuál borrar.
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


class Load(Base):
    """Una carga: las medidas de un archivo guardadas de una vez."""

    __tablename__ = "loads"

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(500))
    # server_default: la hora la pone PostgreSQL al insertar, con zona horaria.
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    # cascade: las medidas viajan con su carga; al borrar la carga, se borran con ella.
    readings: Mapped[list[Reading]] = relationship(
        back_populates="load", cascade="all, delete-orphan", order_by="Reading.position"
    )


class Reading(Base):
    """Una medida de una carga, en su posición dentro del archivo."""

    __tablename__ = "readings"
    # Dos medidas de una misma carga no pueden ocupar la misma posición.
    __table_args__ = (UniqueConstraint("load_id", "position"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    # ondelete="CASCADE": PostgreSQL borra las medidas aunque se borre la carga con SQL a mano.
    load_id: Mapped[int] = mapped_column(ForeignKey("loads.id", ondelete="CASCADE"), index=True)
    position: Mapped[int]
    label: Mapped[str] = mapped_column(String(100))
    # `float | None`: la columna admite NULL, que es "sin dato".
    value: Mapped[float | None]

    load: Mapped[Load] = relationship(back_populates="readings")


@dataclass(frozen=True, slots=True)
class LoadInfo:
    """Una fila de la lista de cargas: número, origen, fecha y cuántas medidas tiene."""

    id: int
    source: str
    created_at: datetime
    measurements: int


@dataclass(frozen=True, slots=True)
class LabelStats:
    """El resumen de una etiqueta: medidas, medidas con valor y media de los valores."""

    label: str
    measurements: int
    with_value: int
    mean: float | None


def make_engine(url: str, *, echo: bool = False) -> Engine:
    """El motor de una URL como postgresql+psycopg://usuario:clave@host:5432/base.

    pool_pre_ping: antes de reutilizar una conexión del pool, comprueba que sigue viva.
    echo=True escribe en el registro cada SQL que se envía.
    """
    return create_engine(url, echo=echo, pool_pre_ping=True)


def save_series(session: Session, source: str, series: Series) -> Load:
    """Añade una carga con las medidas de `series` y la devuelve con su `id` ya asignado."""
    load = Load(
        source=source,
        readings=[
            Reading(position=position, label=measurement.label, value=measurement.value)
            for position, measurement in enumerate(series)
        ],
    )
    session.add(load)
    # flush envía los INSERT sin confirmar la transacción: así PostgreSQL asigna el id.
    session.flush()
    return load


def load_series(session: Session, load_id: int) -> Series | None:
    """Las medidas de una carga, en su orden, o None si no existe."""
    load = session.get(Load, load_id)
    if load is None:
        return None
    return Series([Measurement(reading.label, reading.value) for reading in load.readings])


def list_loads(session: Session) -> list[LoadInfo]:
    """Todas las cargas, de la más antigua a la más nueva, con cuántas medidas tiene cada una."""
    # Una sola consulta con JOIN y GROUP BY: sin traer las medidas a Python (N+1).
    query = (
        select(Load.id, Load.source, Load.created_at, func.count(Reading.id))
        .outerjoin(Load.readings)
        .group_by(Load.id)
        .order_by(Load.id)
    )
    return [LoadInfo(*row) for row in session.execute(query)]


def label_stats(session: Session, load_id: int | None = None) -> list[LabelStats]:
    """Medidas, medidas con valor y media por etiqueta, de una carga o de todas."""
    # count(value) no cuenta los NULL, y avg los ignora: lo mismo que hace el Observatorio
    # con los "sin dato".
    query = (
        select(
            Reading.label,
            func.count(Reading.id),
            func.count(Reading.value),
            func.avg(Reading.value),
        )
        .group_by(Reading.label)
        .order_by(Reading.label)
    )
    if load_id is not None:
        query = query.where(Reading.load_id == load_id)
    return [LabelStats(*row) for row in session.execute(query)]


def delete_load(session: Session, load_id: int) -> bool:
    """Borra una carga y sus medidas; False si no existía."""
    load = session.get(Load, load_id)
    if load is None:
        return False
    session.delete(load)
    session.flush()
    return True
