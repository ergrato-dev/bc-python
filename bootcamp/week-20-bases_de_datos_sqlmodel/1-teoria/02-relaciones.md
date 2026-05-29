# Relaciones

## Objetivos

- Implementar relaciones uno-a-muchos con `Relationship` y `back_populates`
- Implementar relaciones muchos-a-muchos con tabla de asociación
- Entender carga lazy vs eager y cuándo usar cada una
- Navegar relaciones sin caer en el problema N+1

---

## 1. One-to-Many — un proyecto tiene muchos assets

```python
from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship

class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    client: str

    # "Un proyecto tiene muchos assets"
    assets: list["Asset"] = Relationship(back_populates="project")


class Asset(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    project_id: int | None = Field(default=None, foreign_key="project.id")

    # "Un asset pertenece a un proyecto"
    project: Project | None = Relationship(back_populates="assets")
```

### Usar la relación

```python
from sqlmodel import Session, select

with Session(engine) as session:
    project = Project(name="Spot Canal 9", client="Canal 9")
    session.add(project)
    session.commit()
    session.refresh(project)

    asset = Asset(name="intro.mp4", project_id=project.id)
    session.add(asset)
    session.commit()

    # Navegar la relación (carga lazy — hace una query extra)
    session.refresh(project)
    print(project.assets)   # [Asset(name="intro.mp4")]
```

### Regla `back_populates`

| Lado | `Relationship(back_populates=...)` apunta a |
|------|---------------------------------------------|
| `Project.assets` | `"project"` (atributo en Asset) |
| `Asset.project` | `"assets"` (atributo en Project) |

Los nombres deben coincidir exactamente.

---

## 2. Many-to-Many — un asset puede tener muchas etiquetas

Muchos-a-muchos requiere una tabla de asociación (link table):

```python
from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship

# Tabla de asociación — sin campos extra
class AssetTagLink(SQLModel, table=True):
    asset_id: int | None = Field(
        default=None, foreign_key="asset.id", primary_key=True
    )
    tag_id: int | None = Field(
        default=None, foreign_key="tag.id", primary_key=True
    )


class Tag(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)

    assets: list["Asset"] = Relationship(
        back_populates="tags", link_model=AssetTagLink
    )


class Asset(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    project_id: int | None = Field(default=None, foreign_key="project.id")

    tags: list[Tag] = Relationship(
        back_populates="assets", link_model=AssetTagLink
    )
```

### Crear y navegar

```python
with Session(engine) as session:
    tag_music = Tag(name="music")
    tag_hd = Tag(name="hd")
    asset = Asset(name="jingle.mp3")

    asset.tags = [tag_music, tag_hd]
    session.add(asset)
    session.commit()
    session.refresh(asset)

    print([t.name for t in asset.tags])  # ["music", "hd"]
```

---

## 3. Many-to-Many con campos extra en la tabla de asociación

Cuando la tabla de asociación tiene datos propios (ej: fecha de asignación):

```python
from datetime import datetime

class ProjectClientLink(SQLModel, table=True):
    """Un cliente puede participar en varios proyectos y viceversa."""
    project_id: int | None = Field(
        default=None, foreign_key="project.id", primary_key=True
    )
    client_id: int | None = Field(
        default=None, foreign_key="client.id", primary_key=True
    )
    role: str = "sponsor"
    joined_at: datetime = Field(default_factory=datetime.utcnow)
```

En este caso se gestiona la tabla de asociación directamente como un modelo más.

---

## 4. Self-referential — un asset puede derivar de otro

```python
class Asset(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    parent_id: int | None = Field(default=None, foreign_key="asset.id")

    # SQLAlchemy necesita remote_side para auto-referencia
    children: list["Asset"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "Asset.id == Asset.parent_id",
            "foreign_keys": "[Asset.parent_id]",
        }
    )
```

---

## 5. Lazy vs Eager loading

Por defecto SQLModel usa **lazy loading**: los objetos relacionados se cargan al acceder al atributo (query extra).

```python
# Lazy — 1 query para el proyecto + 1 query por acceso a .assets
project = session.get(Project, 1)
print(project.assets)   # ← dispara SELECT * FROM asset WHERE project_id=1

# Eager (selectin) — 2 queries pero en el mismo bloque
from sqlalchemy.orm import selectinload
from sqlmodel import select

statement = (
    select(Project)
    .where(Project.id == 1)
    .options(selectinload(Project.assets))  # type: ignore
)
project = session.exec(statement).first()
# project.assets ya está cargado — sin queries extra
```

### Cuándo usar cada uno

| Caso | Recomendación |
|------|---------------|
| Acceso ocasional a la relación | Lazy (default) |
| Siempre necesitas los relacionados | Eager (`selectinload`) |
| Muchos niveles de anidación | `joinedload` |
| Bucle sobre muchos objetos | Eager — evita N+1 |

---

## 6. El problema N+1

```python
# MALO — 1 query para proyectos + 1 query por cada proyecto para sus assets
projects = session.exec(select(Project)).all()
for p in projects:
    print(p.assets)   # N queries adicionales

# BUENO — 2 queries total
from sqlalchemy.orm import selectinload
stmt = select(Project).options(selectinload(Project.assets))  # type: ignore
projects = session.exec(stmt).all()
for p in projects:
    print(p.assets)   # ya cargados
```

---

## ✅ Resumen

| Tipo | Implementación |
|------|----------------|
| One-to-Many | `FK` en el "muchos" + `Relationship(back_populates=...)` en ambos lados |
| Many-to-Many | Tabla de asociación + `Relationship(link_model=LinkTable)` en ambos lados |
| M2M con campos extra | Link table como modelo independiente, gestión manual |
| Eager loading | `.options(selectinload(Model.relation))` |

---

## Recursos Adicionales

- [SQLModel — Relationships](https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/)
- [SQLAlchemy — Relationship loading](https://docs.sqlalchemy.org/en/20/orm/loading_relationships.html)
