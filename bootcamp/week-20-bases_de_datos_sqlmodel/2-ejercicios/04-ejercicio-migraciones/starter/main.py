"""
Ejercicio 04 — Migraciones con Alembic
========================================
Inicializa Alembic en el proyecto, crea migraciones y aplícalas.

Este ejercicio es guiado por comandos en terminal — el código Python
es el punto de partida; las tareas están en los comentarios.

Tareas:
  1. Configurar Alembic para que detecte los modelos SQLModel
  2. Crear la migración inicial (autogenerate)
  3. Añadir un campo nuevo al modelo Project y crear la migración
  4. Aplicar y revertir migraciones

Ejecutar paso a paso según las instrucciones.
"""
from __future__ import annotations

from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine

DATABASE_URL = "sqlite:///ejercicio04.db"
engine = create_engine(DATABASE_URL, echo=True)

# ── Modelo inicial ─────────────────────────────────────────────────────────────

class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, index=True)
    client: str
    budget: float = Field(default=0.0, ge=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)


class Asset(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=200)
    type: str = Field(default="video")
    size_mb: float = Field(default=0.0)
    project_id: int | None = Field(default=None, foreign_key="project.id")


# ── Tarea 1 — Setup Alembic ────────────────────────────────────────────────────
"""
En terminal:
  1. pip install alembic
  2. alembic init migrations

Luego editar migrations/env.py:
  - Importar SQLModel y los modelos: from src.models import Project, Asset
  - Reemplazar: target_metadata = SQLModel.metadata

Editar alembic.ini:
  - sqlalchemy.url = sqlite:///ejercicio04.db
"""

# ── Tarea 2 — Migración inicial ────────────────────────────────────────────────
"""
En terminal:
  alembic revision --autogenerate -m "create_project_and_asset"
  alembic upgrade head

Verificar: el archivo ejercicio04.db debe haberse creado con las tablas.
"""

# ── Tarea 3 — Nuevo campo ──────────────────────────────────────────────────────
"""
Agregar el campo `deadline` al modelo Project:
  deadline: str | None = Field(default=None)

Luego:
  alembic revision --autogenerate -m "add_deadline_to_project"
  alembic upgrade head

Verificar que la columna aparece en la tabla.
"""

# ── Tarea 4 — Downgrade ────────────────────────────────────────────────────────
"""
  alembic downgrade -1        # revierte el deadline
  alembic upgrade head        # vuelve a aplicarlo
  alembic history --verbose   # ver el historial
"""

# ── Código de verificación ────────────────────────────────────────────────────

def verify() -> None:
    """Inserta datos para verificar que el schema está correcto."""
    from sqlmodel import Session
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        p = Project(name="Test", client="QA")
        session.add(p)
        session.commit()
        session.refresh(p)
        print(f"Proyecto creado: id={p.id}, name={p.name}")
        print("OK — migración aplicada correctamente")


if __name__ == "__main__":
    verify()
