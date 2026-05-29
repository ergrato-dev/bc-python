# Semana 20: Bases de Datos con SQLModel

> **Fase 2 — Python Profesional** · _Junior → Mid-level_

## Objetivos de Aprendizaje

Al finalizar esta semana, serás capaz de:

- Definir modelos SQLModel y gestionarlos con sesiones SQLAlchemy
- Modelar relaciones uno-a-muchos y muchos-a-muchos con `Relationship`
- Escribir queries avanzadas: filtros, joins, aggregaciones con `select()`
- Gestionar esquemas evolutivos con migraciones Alembic
- Aplicar el patrón Repository para aislar el acceso a datos

---

## Contenidos

| # | Archivo | Tema |
|---|---------|------|
| 01 | [SQLModel — Fundamentos](1-teoria/01-sqlmodel-fundamentos.md) | Modelos, engine, sesiones, CRUD básico |
| 02 | [Relaciones](1-teoria/02-relaciones.md) | One-to-many, many-to-many, back_populates |
| 03 | [Queries Avanzadas](1-teoria/03-queries-avanzadas.md) | select(), where(), join(), func, group_by |
| 04 | [Migraciones con Alembic](1-teoria/04-migraciones-alembic.md) | alembic init, revision, upgrade, downgrade |
| 05 | [Patrones de Acceso a Datos](1-teoria/05-patrones-acceso-datos.md) | Repository, Unit of Work, sesiones en contexto |

---

## Estructura de la Semana

```
week-20-bases_de_datos_sqlmodel/
├── README.md
├── rubrica-evaluacion.md
├── 0-assets/               # SVGs de apoyo a la teoría
├── 1-teoria/               # 5 archivos .md
├── 2-ejercicios/
│   ├── 01-ejercicio-modelos-sesiones/
│   ├── 02-ejercicio-relaciones/
│   ├── 03-ejercicio-queries/
│   └── 04-ejercicio-migraciones/
├── 3-proyecto/
│   ├── README.md           # Studio BC Catalog DB
│   ├── starter/
│   └── solution/
├── 4-recursos/
└── 5-glosario/
```

---

## Distribución del Tiempo (6h)

| Bloque | Actividad | Tiempo |
|--------|-----------|--------|
| 1 | Teoría: fundamentos + relaciones | 1.5h |
| 2 | Teoría: queries + migraciones + patrones | 1.0h |
| 3 | Ejercicios guiados (4) | 2.0h |
| 4 | Proyecto semanal | 1.5h |

---

## Entregables

- [ ] Ejercicio 01: Modelos, engine, sesiones y CRUD básico
- [ ] Ejercicio 02: Relaciones one-to-many y many-to-many
- [ ] Ejercicio 03: Queries avanzadas con joins y aggregaciones
- [ ] Ejercicio 04: Migraciones con Alembic
- [ ] Proyecto: `studio-catalog-db` — base de datos del catálogo de Studio BC

---

## Navegación

← [Semana 19](../week-19-http_y_apis_httpx/README.md) · [Semana 21](../week-21-proyecto_fase_2/README.md) →
