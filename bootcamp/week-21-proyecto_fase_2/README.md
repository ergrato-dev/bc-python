# Semana 21: Proyecto Integrador Fase 2

> **Fase 2 — Python Profesional** · _Junior → Mid-level_ · **Semana de cierre de fase**

## Objetivo

Integrar las seis tecnologías de la Fase 2 en una sola aplicación de producción:

| Semana | Tecnología | Rol en el proyecto |
|--------|------------|--------------------|
| 15 | Python moderno (type hints, protocols) | Interfaces y contratos entre capas |
| 16 | AsyncIO | Llamadas concurrentes a APIs externas |
| 17 | Typer + Rich | CLI con subcomandos y salida visual |
| 18 | Polars | Reportes y análisis de datos |
| 19 | httpx + tenacity | Integración con APIs externas resiliente |
| 20 | SQLModel + Alembic | Persistencia y migraciones |

---

## Entregable: `studio-bc-manager`

CLI de gestión de producción para Studio BC que permite:

- Gestionar clientes, proyectos y assets desde la terminal
- Consultar tipos de cambio en tiempo real (httpx async)
- Generar reportes de producción con Polars
- Persistir todo en SQLite con SQLModel
- Exportar reportes a CSV / Parquet

---

## Contenidos

| # | Archivo | Tema |
|---|---------|------|
| 01 | [Arquitectura en Capas](1-teoria/01-arquitectura-capas.md) | CLI → Servicios → Repositorios → DB/APIs |
| 02 | [Integración de Componentes](1-teoria/02-integracion-componentes.md) | Config, DI, manejo de errores entre capas |
| 03 | [Testing de Integración](1-teoria/03-testing-integracion.md) | Fixtures, fakes, DB en memoria |

---

## Estructura de la Semana

```
week-21-proyecto_fase_2/
├── README.md
├── rubrica-evaluacion.md
├── 0-assets/               # SVGs de arquitectura
├── 1-teoria/               # 3 archivos .md
├── 2-checkpoints/          # Hitos guiados de construcción
│   ├── 01-checkpoint-db-cli/
│   └── 02-checkpoint-servicios-reportes/
├── 3-proyecto/
│   ├── README.md
│   └── starter/            # studio-bc-manager
├── 4-recursos/
└── 5-glosario/
```

---

## Distribución del Tiempo (6h)

| Bloque | Actividad | Tiempo |
|--------|-----------|--------|
| 1 | Leer teoría de arquitectura (3 archivos) | 1.0h |
| 2 | Checkpoint 01: DB + CLI skeleton | 1.5h |
| 3 | Checkpoint 02: Servicios + Reportes | 1.5h |
| 4 | Proyecto completo + pulido | 2.0h |

---

## Entregables

- [ ] Checkpoint 01: `projects list` y `clients list` funcionales sobre SQLite
- [ ] Checkpoint 02: `report generate` produce tabla Rich + exporta CSV con Polars
- [ ] Proyecto: `studio-bc-manager` con todos los subcomandos implementados
- [ ] Al menos una llamada async a API externa integrada (tipo de cambio)
- [ ] Tests de integración con DB en memoria — mínimo 5 tests

---

## Navegación

← [Semana 20](../week-20-bases_de_datos_sqlmodel/README.md) · [Semana 22](../week-22-automatizacion_sistema_archivos/README.md) →
