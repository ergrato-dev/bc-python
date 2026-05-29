# Proyecto Semanal — Studio BC Catalog DB

## Contexto

Studio BC necesita una base de datos para gestionar su catálogo de producción:
clientes, proyectos, assets multimedia y etiquetas de clasificación.

---

## Objetivo

Construir `studio-catalog-db`: una base de datos SQLite con SQLModel que permita
gestionar el catálogo completo con operaciones CRUD, queries avanzadas y migraciones Alembic.

---

## Estructura

```
starter/
├── src/
│   ├── __init__.py
│   ├── database.py       # engine, get_session
│   ├── models.py         # Client, Project, Asset, Tag, AssetTagLink
│   └── repositories/
│       ├── __init__.py
│       ├── base.py       # BaseRepository genérico
│       ├── client.py     # ClientRepository
│       ├── project.py    # ProjectRepository
│       └── asset.py      # AssetRepository
├── migrations/
│   ├── env.py
│   └── versions/
├── tests/
│   └── test_repositories.py
├── main.py               # CLI de demostración con Rich
├── seed.py               # Poblar la DB con datos de prueba
├── alembic.ini
└── pyproject.toml
```

---

## Tareas

### 1. `src/models.py` — Modelos con relaciones

```python
class Client(SQLModel, table=True):
    id, name, email, country, created_at
    projects: list["Project"] = Relationship(back_populates="client_rel")

class Project(SQLModel, table=True):
    id, name, budget, status, created_at, is_active
    client_id (FK → client.id)
    client_rel: Client = Relationship(back_populates="projects")
    assets: list["Asset"] = Relationship(back_populates="project")

class AssetTagLink(SQLModel, table=True):
    asset_id (PK, FK), tag_id (PK, FK)

class Tag(SQLModel, table=True):
    id, name (unique)
    assets: list["Asset"] = Relationship(link_model=AssetTagLink)

class Asset(SQLModel, table=True):
    id, name, type, size_mb, storage_path
    project_id (FK → project.id)
    project: Project = Relationship(back_populates="assets")
    tags: list[Tag] = Relationship(link_model=AssetTagLink)
```

### 2. `src/repositories/base.py` — CRUD genérico

```python
class BaseRepository(Generic[T]):
    def get(self, session, id) -> T | None
    def list(self, session) -> list[T]
    def create(self, session, obj) -> T
    def delete(self, session, id) -> bool
```

### 3. `src/repositories/project.py` — Queries específicas

```python
class ProjectRepository(BaseRepository[Project]):
    def list_by_client(self, session, client_id) -> list[Project]
    def total_budget(self, session) -> float
    def asset_count_per_project(self, session) -> list[tuple[str, int]]
    def kpis(self, session) -> dict
```

### 4. `src/repositories/asset.py`

```python
class AssetRepository(BaseRepository[Asset]):
    def list_by_project(self, session, project_id) -> list[Asset]
    def add_tag(self, session, asset_id, tag_name) -> Asset
    def find_by_tag(self, session, tag_name) -> list[Asset]
    def total_size_by_project(self, session, project_id) -> float
```

### 5. `seed.py` — Datos de prueba

- 3 clientes
- 5 proyectos distribuidos entre los clientes
- 10 assets con tags variados

### 6. `main.py` — CLI con Rich

```
$ python main.py projects        # tabla de proyectos con presupuesto
$ python main.py assets --project-id 1   # assets del proyecto 1
$ python main.py kpis            # KPIs del catálogo
```

### 7. Alembic

- Migración inicial con todos los modelos
- Una migración adicional: añadir campo `notes` a Project

---

## Criterios de Aceptación

- [ ] `mypy --strict src/` pasa sin errores
- [ ] Todos los repositorios heredan de `BaseRepository`
- [ ] No hay `session.exec()` ni `session.get()` fuera de los repositorios
- [ ] `seed.py` pobla la DB sin errores
- [ ] `main.py kpis` muestra total/promedio/máx de presupuesto
- [ ] Hay al menos 2 migraciones en `migrations/versions/`
