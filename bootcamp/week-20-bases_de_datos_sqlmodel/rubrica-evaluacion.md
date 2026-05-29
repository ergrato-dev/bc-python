# Rúbrica de Evaluación — Semana 20: Bases de Datos con SQLModel

## Puntaje Total: 100 puntos · Mínimo para aprobar: 70 pts

---

## Conocimiento (30 pts)

| Indicador | Puntos |
|-----------|--------|
| Explica la diferencia entre `SQLModel` (tabla), `SQLModel` (solo Pydantic) y cuándo usar cada forma | 8 |
| Describe cómo funciona la sesión SQLAlchemy: qué es el Unit of Work y cuándo se hace flush/commit | 7 |
| Distingue `Relationship` (ORM) de `Field(foreign_key=...)` (columna) y el rol de `back_populates` | 8 |
| Explica para qué sirve Alembic y qué problema resuelven las migraciones frente a `create_all()` | 7 |

## Desempeño (40 pts)

| Indicador | Puntos |
|-----------|--------|
| Define modelos con herencia `SQLModel, table=True` y crea el engine + tablas correctamente | 10 |
| Implementa relaciones one-to-many y many-to-many con tabla de asociación | 10 |
| Escribe queries con `select()`, `where()`, `join()` y aggregaciones (`func.count`, `group_by`) | 10 |
| Crea y aplica una migración Alembic (nueva columna o tabla) sin pérdida de datos | 10 |

## Producto (30 pts)

| Indicador | Puntos |
|-----------|--------|
| `studio-catalog-db` tiene al menos 4 modelos relacionados (Client, Project, Asset, Tag) | 10 |
| Todas las operaciones CRUD pasan por el patrón Repository — ningún `session.exec()` suelto en `main` | 8 |
| Hay al menos una migración Alembic funcional en el historial | 7 |
| mypy --strict pasa sin errores | 5 |
