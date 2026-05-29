# Queries Avanzadas

## Objetivos

- Usar `select()` con `where()`, `order_by()`, `limit()` y `offset()`
- Escribir joins entre tablas relacionadas
- Aggregar datos con `func.count()`, `func.sum()`, `group_by()`
- Combinar filtros con `and_()`, `or_()`, `not_()`

---

## 1. `select()` — la base de toda query

```python
from sqlmodel import select, Session
from sqlalchemy import func

# Select todos
stmt = select(Project)
projects = session.exec(stmt).all()

# Select uno
project = session.exec(select(Project).where(Project.id == 1)).first()

# Método abreviado para PK
project = session.get(Project, 1)
```

---

## 2. Filtros con `where()`

```python
# Filtro simple
stmt = select(Asset).where(Asset.project_id == project_id)

# Múltiples condiciones — AND implícito
stmt = (
    select(Asset)
    .where(Asset.project_id == project_id)
    .where(Asset.type == "video")
)

# AND explícito
from sqlalchemy import and_
stmt = select(Asset).where(
    and_(Asset.project_id == project_id, Asset.size_mb > 100)
)

# OR
from sqlalchemy import or_
stmt = select(Project).where(
    or_(Project.client == "Canal 9", Project.client == "Canal 7")
)

# IN
stmt = select(Project).where(Project.client.in_(["Canal 9", "Canal 7"]))  # type: ignore

# LIKE / ILIKE
stmt = select(Asset).where(Asset.name.contains("intro"))        # LIKE %intro%
stmt = select(Asset).where(Asset.name.startswith("reel"))       # LIKE reel%
stmt = select(Asset).where(Asset.name.ilike("%INTRO%"))         # case-insensitive

# IS NULL
stmt = select(Asset).where(Asset.project_id == None)            # noqa: E711

# NOT
from sqlalchemy import not_
stmt = select(Project).where(not_(Project.is_active))
```

---

## 3. Ordenamiento, límite y paginación

```python
# Orden ascendente / descendente
stmt = select(Project).order_by(Project.created_at.desc())

# Paginación con limit + offset
PAGE_SIZE = 20

def list_projects(session: Session, page: int = 0) -> list[Project]:
    return session.exec(
        select(Project)
        .order_by(Project.created_at.desc())
        .offset(page * PAGE_SIZE)
        .limit(PAGE_SIZE)
    ).all()
```

---

## 4. Joins

```python
# JOIN implícito vía FK
stmt = (
    select(Asset, Project)
    .join(Project, Asset.project_id == Project.id)
    .where(Project.client == "Canal 9")
)
results = session.exec(stmt).all()
for asset, project in results:
    print(f"{asset.name} → {project.name}")

# Seleccionar solo columnas de Asset pero filtrando por Project
stmt = (
    select(Asset)
    .join(Project)                          # SQLModel infiere la FK
    .where(Project.is_active == True)
)
assets = session.exec(stmt).all()

# LEFT OUTER JOIN — incluye assets sin proyecto
from sqlalchemy import outerjoin
stmt = select(Asset).join(Project, isouter=True)

# JOIN con tabla de asociación (many-to-many manual)
stmt = (
    select(Asset)
    .join(AssetTagLink, Asset.id == AssetTagLink.asset_id)
    .join(Tag, Tag.id == AssetTagLink.tag_id)
    .where(Tag.name == "hd")
)
```

---

## 5. Aggregaciones

```python
from sqlalchemy import func

# COUNT
total = session.exec(select(func.count(Project.id))).one()
print(f"Total proyectos: {total}")

# COUNT con filtro
active_count = session.exec(
    select(func.count(Project.id)).where(Project.is_active == True)
).one()

# SUM y AVG
total_budget = session.exec(select(func.sum(Project.budget))).one()
avg_budget   = session.exec(select(func.avg(Project.budget))).one()
max_size     = session.exec(select(func.max(Asset.size_mb))).one()
```

---

## 6. GROUP BY

```python
# Assets por proyecto — (project_id, count)
stmt = (
    select(Asset.project_id, func.count(Asset.id).label("asset_count"))
    .group_by(Asset.project_id)
    .order_by(func.count(Asset.id).desc())
)
rows = session.exec(stmt).all()
for project_id, count in rows:
    print(f"  proyecto {project_id}: {count} assets")

# GROUP BY con HAVING — solo proyectos con más de 5 assets
stmt = (
    select(Asset.project_id, func.count(Asset.id).label("n"))
    .group_by(Asset.project_id)
    .having(func.count(Asset.id) > 5)
)

# JOIN + GROUP BY — nombre del proyecto + conteo de assets
stmt = (
    select(Project.name, func.count(Asset.id).label("assets"))
    .join(Asset, isouter=True)
    .group_by(Project.id)
    .order_by(func.count(Asset.id).desc())
)
results = session.exec(stmt).all()
for name, count in results:
    print(f"  {name}: {count} assets")
```

---

## 7. Subqueries

```python
from sqlalchemy import select as sa_select

# Proyectos cuyo presupuesto supera el promedio
avg_stmt = sa_select(func.avg(Project.budget)).scalar_subquery()
stmt = select(Project).where(Project.budget > avg_stmt)
big_projects = session.exec(stmt).all()
```

---

## 8. Columnas calculadas con `label()`

```python
# Retornar datos transformados sin modelo completo
stmt = select(
    Project.name,
    Project.budget,
    (Project.budget * 0.19).label("iva"),
    (Project.budget * 1.19).label("total_con_iva"),
).where(Project.is_active == True)

rows = session.exec(stmt).all()
for name, budget, iva, total in rows:
    print(f"{name}: ${budget:.2f} + IVA ${iva:.2f} = ${total:.2f}")
```

---

## ✅ Resumen

| Operación | SQLModel |
|-----------|----------|
| Filtro | `.where(Model.field == value)` |
| OR / AND | `or_(...)` / `and_(...)` de `sqlalchemy` |
| IN | `.where(Model.field.in_([...]))` |
| Orden | `.order_by(Model.field.desc())` |
| Paginación | `.offset(n).limit(m)` |
| JOIN | `.join(OtherModel)` o `.join(OtherModel, isouter=True)` |
| COUNT | `func.count(Model.id)` |
| SUM / AVG | `func.sum(...)` / `func.avg(...)` |
| GROUP BY | `.group_by(Model.field)` |
| HAVING | `.having(func.count(...) > N)` |

---

## Recursos Adicionales

- [SQLModel — Where](https://sqlmodel.tiangolo.com/tutorial/where/)
- [SQLAlchemy — ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/)
