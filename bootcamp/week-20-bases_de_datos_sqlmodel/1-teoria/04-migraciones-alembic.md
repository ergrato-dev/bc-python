# Migraciones con Alembic

## Objetivos

- Entender por qué `create_all()` no es suficiente en producción
- Inicializar Alembic en un proyecto SQLModel
- Crear y aplicar revisiones de migración
- Hacer downgrade cuando una migración sale mal

---

## 1. El problema de `create_all()`

`SQLModel.metadata.create_all(engine)` crea tablas si no existen — pero **no modifica** tablas existentes:

```
create_all():
  ✅ Tabla nueva → la crea
  ❌ Columna nueva en tabla existente → la ignora
  ❌ Columna renombrada → la ignora
  ❌ Índice añadido → lo ignora
  ❌ Tipo de dato cambiado → lo ignora
```

En producción necesitás **migraciones**: scripts versionados que describen cada cambio de esquema.

---

## 2. Instalación y setup

```bash
pip install alembic

# Dentro del directorio del proyecto
alembic init migrations
```

Estructura generada:

```
proyecto/
├── migrations/
│   ├── env.py          # configuración del entorno Alembic
│   ├── script.py.mako  # plantilla para nuevas migraciones
│   └── versions/       # archivos de migración generados
├── alembic.ini         # configuración principal
└── src/
    └── models.py
```

---

## 3. Configurar `env.py`

Editar `migrations/env.py` para que Alembic conozca tus modelos:

```python
# migrations/env.py
from sqlmodel import SQLModel
from src.models import Project, Asset, Tag   # importar TODOS los modelos

# Reemplazar: target_metadata = None
target_metadata = SQLModel.metadata
```

Y en `alembic.ini`, configurar la URL de la base de datos:

```ini
# alembic.ini
sqlalchemy.url = sqlite:///studio.db
```

O desde variable de entorno (mejor práctica):

```python
# migrations/env.py
import os
config.set_main_option("sqlalchemy.url", os.environ["DATABASE_URL"])
```

---

## 4. Crear una migración

```bash
# Autogenerar basándose en los modelos (detecta diferencias)
alembic revision --autogenerate -m "create_projects_and_assets"

# Migración vacía (para cambios manuales)
alembic revision -m "add_index_to_asset_name"
```

Archivo generado en `migrations/versions/`:

```python
"""create_projects_and_assets

Revision ID: a1b2c3d4e5f6
Revises:
Create Date: 2025-01-15 10:30:00
"""
from alembic import op
import sqlalchemy as sa

revision = "a1b2c3d4e5f6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "project",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("client", sa.String(), nullable=False),
        sa.Column("budget", sa.Float(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="1"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_project_name", "project", ["name"])

    op.create_table(
        "asset",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("size_mb", sa.Float(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("asset")
    op.drop_table("project")
```

---

## 5. Aplicar migraciones

```bash
# Ver estado actual
alembic current

# Ver historial
alembic history --verbose

# Aplicar todas las migraciones pendientes
alembic upgrade head

# Aplicar hasta una revisión específica
alembic upgrade a1b2c3d4e5f6

# Avanzar N pasos
alembic upgrade +2
```

---

## 6. Downgrade (revertir)

```bash
# Revertir la última migración
alembic downgrade -1

# Revertir hasta una revisión específica
alembic downgrade a1b2c3d4e5f6

# Revertir todo (estado inicial)
alembic downgrade base
```

---

## 7. Ejemplo: añadir columna a tabla existente

```python
# src/models.py — se agrega el campo
class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    client: str
    budget: float = 0.0
    deadline: str | None = None   # ← NUEVO
```

```bash
alembic revision --autogenerate -m "add_deadline_to_project"
```

Migración generada:

```python
def upgrade() -> None:
    op.add_column(
        "project",
        sa.Column("deadline", sa.String(), nullable=True),
    )

def downgrade() -> None:
    op.drop_column("project", "deadline")
```

```bash
alembic upgrade head
```

---

## 8. Operaciones comunes en migraciones manuales

```python
# Renombrar columna
op.alter_column("asset", "file_path", new_column_name="storage_path")

# Cambiar tipo de dato
op.alter_column("project", "budget", type_=sa.Numeric(precision=12, scale=2))

# Crear índice
op.create_index("ix_asset_name", "asset", ["name"])
op.drop_index("ix_asset_name", "asset")

# Crear FK
op.create_foreign_key(
    "fk_asset_project",
    "asset", "project",
    ["project_id"], ["id"],
)

# Migración de datos (junto con cambio de esquema)
def upgrade() -> None:
    op.add_column("project", sa.Column("slug", sa.String(), nullable=True))
    # Poblar con datos
    op.execute("UPDATE project SET slug = lower(replace(name, ' ', '-'))")
    op.alter_column("project", "slug", nullable=False)
```

---

## ✅ Resumen

| Comando | Descripción |
|---------|-------------|
| `alembic init migrations` | Inicializar Alembic |
| `alembic revision --autogenerate -m "msg"` | Crear migración desde modelos |
| `alembic upgrade head` | Aplicar todas las pendientes |
| `alembic downgrade -1` | Revertir la última |
| `alembic current` | Ver versión actual |
| `alembic history` | Ver historial |

---

## Recursos Adicionales

- [Alembic — Documentación](https://alembic.sqlalchemy.org/en/latest/)
- [Alembic — Auto-generating migrations](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)
