"""Ejercicio 04 · Los modelos que Alembic compara con la base de datos.

Cada paso del README cambia este archivo y después crea una migración con Alembic.
"""

from sqlalchemy import MetaData, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

URL = "postgresql+psycopg://practicas:practicas@127.0.0.1:5433/migraciones"


class Base(DeclarativeBase):
    # Nombres fijos para restricciones e índices: una migración futura sabrá cuál borrar.
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


# ============================================
# PASO 2: El primer modelo
# ============================================
# Descomenta las siguientes líneas:
# class Station(Base):
#     __tablename__ = "stations"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(50), unique=True)

    # ============================================
    # PASO 4: Una columna que admite NULL
    # ============================================
    # Descomenta las siguientes líneas:
    # altitude: Mapped[int | None]

    # ============================================
    # PASO 5: Una columna que no admite NULL
    # ============================================
    # Descomenta las siguientes líneas:
    # region: Mapped[str] = mapped_column(String(50))
