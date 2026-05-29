# Patrones de Acceso a Datos

## Objetivos

- Implementar el patrón Repository para aislar queries del dominio
- Entender el Unit of Work y por qué la sesión lo implementa
- Gestionar sesiones con dependency injection (FastAPI / CLI)
- Evitar anti-patrones comunes: sesiones globales, lazy loading fuera de contexto

---

## 1. Por qué aislar el acceso a datos

Sin patrón, el código de negocio mezcla SQL con lógica:

```python
# MALO — lógica de negocio + SQL mezclados
def process_project(project_id: int) -> None:
    with Session(engine) as session:
        project = session.get(Project, project_id)
        assets = session.exec(
            select(Asset).where(Asset.project_id == project_id)
        ).all()
        total_size = sum(a.size_mb for a in assets)
        project.is_active = total_size < 50_000
        session.commit()
```

El patrón Repository separa responsabilidades:

```python
# BUENO — el repositorio maneja SQL, el servicio maneja lógica
class ProjectRepository:
    def get(self, session: Session, project_id: int) -> Project | None:
        return session.get(Project, project_id)

    def list_active(self, session: Session) -> list[Project]:
        return session.exec(select(Project).where(Project.is_active)).all()

class AssetRepository:
    def total_size_by_project(self, session: Session, project_id: int) -> float:
        result = session.exec(
            select(func.sum(Asset.size_mb)).where(Asset.project_id == project_id)
        ).one()
        return result or 0.0

def process_project(
    session: Session,
    project_repo: ProjectRepository,
    asset_repo: AssetRepository,
    project_id: int,
) -> None:
    project = project_repo.get(session, project_id)
    if project is None:
        return
    total_size = asset_repo.total_size_by_project(session, project_id)
    project.is_active = total_size < 50_000
    session.commit()
```

---

## 2. Repository — implementación completa

```python
from __future__ import annotations
from typing import Generic, TypeVar
from sqlmodel import SQLModel, Session, select

ModelT = TypeVar("ModelT", bound=SQLModel)


class BaseRepository(Generic[ModelT]):
    """CRUD genérico reutilizable."""

    def __init__(self, model: type[ModelT]) -> None:
        self.model = model

    def get(self, session: Session, id: int) -> ModelT | None:
        return session.get(self.model, id)

    def list(self, session: Session) -> list[ModelT]:
        return session.exec(select(self.model)).all()

    def create(self, session: Session, obj: ModelT) -> ModelT:
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    def delete(self, session: Session, id: int) -> bool:
        obj = self.get(session, id)
        if obj is None:
            return False
        session.delete(obj)
        session.commit()
        return True


class ProjectRepository(BaseRepository[Project]):
    """Queries específicas de Project."""

    def __init__(self) -> None:
        super().__init__(Project)

    def list_by_client(self, session: Session, client: str) -> list[Project]:
        return session.exec(
            select(Project).where(Project.client == client)
        ).all()

    def total_budget(self, session: Session) -> float:
        from sqlalchemy import func
        result = session.exec(select(func.sum(Project.budget))).one()
        return float(result or 0)


class AssetRepository(BaseRepository[Asset]):
    def __init__(self) -> None:
        super().__init__(Asset)

    def list_by_project(self, session: Session, project_id: int) -> list[Asset]:
        return session.exec(
            select(Asset)
            .where(Asset.project_id == project_id)
            .order_by(Asset.name)
        ).all()


# Instancias globales (sin estado — thread-safe)
project_repo = ProjectRepository()
asset_repo   = AssetRepository()
```

---

## 3. Unit of Work — la sesión como transacción

SQLAlchemy's `Session` implementa el patrón Unit of Work automáticamente: agrupa todas las operaciones en una transacción hasta el `commit()`.

```python
with Session(engine) as session:
    # Todas estas operaciones son parte de la misma transacción
    project = Project(name="Spot", client="Canal 9")
    session.add(project)

    asset1 = Asset(name="intro.mp4")
    asset2 = Asset(name="main.mp4")
    session.add(asset1)
    session.add(asset2)

    # Un solo commit para todo
    session.commit()

# Si algo falla antes del commit → rollback automático al salir del with
```

### Transacciones explícitas

```python
from sqlalchemy.exc import SQLAlchemyError

with Session(engine) as session:
    try:
        # operación 1
        # operación 2
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise
```

---

## 4. Gestión de sesiones — generador de dependencia

Patrón para inyectar la sesión en funciones (compatible con FastAPI y CLIs):

```python
from collections.abc import Generator
from sqlmodel import Session, create_engine

engine = create_engine("sqlite:///studio.db")

def get_session() -> Generator[Session, None, None]:
    """Generador que provee una sesión por request/operación."""
    with Session(engine) as session:
        yield session

# En FastAPI
from fastapi import Depends
from typing import Annotated

SessionDep = Annotated[Session, Depends(get_session)]

@app.get("/projects")
def list_projects(session: SessionDep) -> list[Project]:
    return project_repo.list(session)

# En CLI / scripts
def main() -> None:
    for session in get_session():
        projects = project_repo.list(session)
        for p in projects:
            print(p.name)
```

---

## 5. Anti-patrones comunes

### Sesión global (evitar)

```python
# MALO — la sesión global no es thread-safe y acumula objetos
global_session = Session(engine)

def get_project(id: int) -> Project | None:
    return global_session.get(Project, id)
```

### Acceso a atributos lazy fuera de sesión

```python
# MALO — DetachedInstanceError
with Session(engine) as session:
    project = session.get(Project, 1)
# Sesión cerrada aquí

print(project.assets)  # ← DetachedInstanceError: acceso lazy fuera de sesión

# BUENO — cargar antes de cerrar la sesión
with Session(engine) as session:
    project = session.get(Project, 1)
    assets = list(project.assets)  # carga dentro de la sesión

print(assets)  # OK
```

### Commit en bucle (evitar)

```python
# MALO — un commit por insert
for asset_data in asset_list:
    asset = Asset(**asset_data)
    session.add(asset)
    session.commit()   # ← muy lento

# BUENO — un solo commit al final
for asset_data in asset_list:
    session.add(Asset(**asset_data))
session.commit()   # ← una sola transacción
```

---

## ✅ Resumen

| Patrón | Propósito |
|--------|-----------|
| Repository | Aislar queries — el dominio no conoce SQL |
| Unit of Work | Agrupar cambios en una transacción (`Session`) |
| Dependency Injection | Inyectar sesión por operación — no global |
| Eager loading | Cargar relaciones dentro de la sesión |

---

## Recursos Adicionales

- [Martin Fowler — Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)
- [Martin Fowler — Unit of Work](https://martinfowler.com/eaaCatalog/unitOfWork.html)
- [SQLModel — Session](https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/)
