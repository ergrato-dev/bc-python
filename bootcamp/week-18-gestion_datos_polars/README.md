# Semana 18: Gestión de Datos con Polars

> **Fase 2 — Python Profesional** · _Junior → Mid-level_

## Objetivos de Aprendizaje

Al finalizar esta semana, serás capaz de:

- Elegir entre **Polars** y Pandas según el caso y explicar las diferencias de rendimiento
- Crear, seleccionar, filtrar y transformar DataFrames con la API expresiva de Polars
- Aplicar agregaciones, `group_by` y todos los tipos de `join`
- Leer y escribir datos en CSV, Excel, Parquet y JSON
- Usar la **Lazy API** para optimizar pipelines de datos antes de ejecutarlos

---

## Contenidos

| # | Archivo | Tema |
|---|---------|------|
| 01 | [Polars vs Pandas](1-teoria/01-polars-vs-pandas.md) | API, performance, lazy vs eager, cuándo usar cada uno |
| 02 | [DataFrames y Expresiones](1-teoria/02-dataframes-expresiones.md) | `pl.col()`, `pl.when()`, `pl.lit()`, encadenamiento |
| 03 | [Agregaciones y Joins](1-teoria/03-agregaciones-joins.md) | `group_by`, `agg`, tipos de join, `pivot`, `unpivot` |
| 04 | [I/O: Formatos de datos](1-teoria/04-io-formatos.md) | CSV, Excel, Parquet, JSON, escritura con schema |
| 05 | [Lazy API y optimización](1-teoria/05-lazy-api-optimizacion.md) | `LazyFrame`, `scan_*`, query plan, `collect()`, streaming |

---

## Estructura de la Semana

```
week-18-gestion_datos_polars/
├── README.md
├── rubrica-evaluacion.md
├── 0-assets/               # SVGs de apoyo a la teoría
├── 1-teoria/               # 5 archivos .md
├── 2-ejercicios/
│   ├── 01-ejercicio-dataframes/
│   ├── 02-ejercicio-expresiones/
│   ├── 03-ejercicio-aggregaciones-joins/
│   └── 04-ejercicio-io/
├── 3-proyecto/
│   ├── README.md           # Studio BC KPI Dashboard
│   ├── starter/
│   └── solution/
├── 4-recursos/
└── 5-glosario/
```

---

## Distribución del Tiempo (6h)

| Bloque | Actividad | Tiempo |
|--------|-----------|--------|
| 1 | Teoría: Polars vs Pandas + DataFrames/Expresiones | 1.5h |
| 2 | Teoría: Agregaciones + I/O + Lazy API | 1.0h |
| 3 | Ejercicios guiados (4) | 2.0h |
| 4 | Proyecto semanal | 1.5h |

---

## Entregables

- [ ] Ejercicio 01: DataFrames, selección y filtrado básico
- [ ] Ejercicio 02: Expresiones encadenadas con `pl.col()` y `pl.when()`
- [ ] Ejercicio 03: Agregaciones y joins entre DataFrames de Studio BC
- [ ] Ejercicio 04: I/O — leer CSV/JSON, escribir Parquet
- [ ] Proyecto: KPI Dashboard — horas por proyecto, rentabilidad por cliente

---

## Navegación

← [Semana 17](../week-17-cli_profesional_typer_rich/README.md) · [Semana 19](../week-19-http_y_apis_httpx/README.md) →
