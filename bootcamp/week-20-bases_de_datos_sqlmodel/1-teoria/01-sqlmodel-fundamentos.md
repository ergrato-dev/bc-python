# SQLModel — Fundamentos

## Objetivos

- Entender qué es SQLModel y su relación con SQLAlchemy y Pydantic
- Crear modelos con `table=True` y modelos solo de validación
- Gestionar el ciclo de vida de la sesión (engine, Session, commit)
- Realizar CRUD básico: insertar, leer, actualizar, eliminar

---

## 1. SQLModel = SQLAlchemy + Pydantic

SQLModel unifica dos mundos:
- **Pydantic**: validación de datos, type hints, serialización JSON
- **SQLAlchemy**: ORM, generación de SQL, gestión de sesiones

```python
# Sin SQLModel — dos clases separadas
class ProjectDB(Base):       # SQLAlchemy
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String)

class ProjectSchema(BaseModel):   # Pydantic
    id: int
    name: str

# Con SQLModel — una sola clase
from sqlmodel import SQLModel, Field

class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
```

| Aspecto | SQLAlchemy puro | Pydantic puro | SQLModel |
|---------|----------------|---------------|----------|
| ORM / SQL | ✅ | ❌ | ✅ |
| Validación | ❌ | ✅ | ✅ |
| Type hints | Parcial | ✅ | ✅ |
| Una clase para todo | ❌ | ❌ | ✅ |

---

## 2. Modelos: `table=True` vs solo Pydantic

```python
from sqlmodel import SQLModel, Field
from datetime import datetime

# Modelo de tabla — se mapea a una tabla SQL
class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    client: str
    budget: float = Field(default=0.0, ge=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

# Modelo solo Pydantic — para requests/responses de API, sin tabla
class ProjectCreate(SQLModel):
    name: str
    client: str
    budget: float = 0.0

class ProjectRead(SQLModel):
    id: int
    name: str
    client: str
    budget: float
    created_at: datetime
```

El modelo sin `table=True` funciona como un schema Pydantic normal: validación, serialización, pero sin crear tabla.

---

## 3. Engine y creación de tablas

```python
from sqlmodel import SQLModel, create_engine

# SQLite (desarrollo)
engine = create_engine("sqlite:///studio.db", echo=True)

# PostgreSQL (producción)
# engine = create_engine("postgresql+psycopg2://user:pass@host/db")

# Crear todas las tablas definidas con table=True
SQLModel.metadata.create_all(engine)
```

`echo=True` imprime el SQL generado — útil para debug.

---

## 4. Sesión — el corazón del ORM

La sesión actúa como una caché en memoria que sincroniza objetos Python con la base de datos:

```python
from sqlmodel import Session

# Context manager — garantiza commit o rollback
with Session(engine) as session:
    project = Project(name="Spot Canal 9", client="Canal 9", budget=5000.0)
    session.add(project)
    session.commit()
    session.refresh(project)   # actualiza el objeto con datos del DB (ej: id generado)
    print(project.id)          # → 1
```

### Ciclo de vida de un objeto en la sesión

```
Transient → add() → Pending → commit() → Persistent → expunge() → Detached
                                   ↑                        ↓
                               refresh()              acceder atributo
                                                       → DetachedError
```

---

## 5. CRUD básico

### Create

```python
from sqlmodel import Session

def create_project(session: Session, data: ProjectCreate) -> Project:
    project = Project.model_validate(data)   # Pydantic → SQLModel
    session.add(project)
    session.commit()
    session.refresh(project)
    return project
```

### Read

```python
from sqlmodel import select

def get_project(session: Session, project_id: int) -> Project | None:
    return session.get(Project, project_id)   # by PK — más eficiente

def list_projects(session: Session) -> list[Project]:
    statement = select(Project).where(Project.is_active == True)
    return session.exec(statement).all()
```

### Update

```python
def update_project(
    session: Session,
    project_id: int,
    data: dict,
) -> Project | None:
    project = session.get(Project, project_id)
    if project is None:
        return None
    for key, value in data.items():
        setattr(project, key, value)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project
```

### Delete

```python
def delete_project(session: Session, project_id: int) -> bool:
    project = session.get(Project, project_id)
    if project is None:
        return False
    session.delete(project)
    session.commit()
    return True
```

---

## 6. Opciones de `Field()`

```python
from sqlmodel import Field

class Asset(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=200, index=True)      # índice para búsquedas rápidas
    size_mb: float = Field(ge=0.0)                     # ge=greater-than-or-equal
    type: str = Field(default="video")
    project_id: int | None = Field(default=None, foreign_key="project.id")

    # Columna con nombre distinto en la tabla SQL
    file_path: str = Field(sa_column_kwargs={"name": "file_path_on_disk"})
```

---

## ✅ Resumen

| Concepto | API |
|---------|-----|
| Modelo de tabla | `class M(SQLModel, table=True)` |
| Schema Pydantic | `class M(SQLModel)` — sin `table=True` |
| Engine SQLite | `create_engine("sqlite:///db.sqlite3")` |
| Crear tablas | `SQLModel.metadata.create_all(engine)` |
| Sesión | `with Session(engine) as session:` |
| Insertar | `session.add(obj); session.commit()` |
| Leer por PK | `session.get(Model, pk)` |
| Query | `session.exec(select(Model).where(...)).all()` |
| Actualizar | `setattr(obj, k, v); session.add(obj); session.commit()` |
| Eliminar | `session.delete(obj); session.commit()` |

---

## Recursos Adicionales

- [SQLModel — Documentación oficial](https://sqlmodel.tiangolo.com/)
- [SQLAlchemy — Session basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
