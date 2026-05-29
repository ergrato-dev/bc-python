# Rúbrica de Evaluación — Semana 18: Gestión de Datos con Polars

## Puntaje Total: 100 puntos · Mínimo para aprobar: 70 pts

---

## Conocimiento (30 pts)

| Indicador | Puntos |
|-----------|--------|
| Explica la diferencia entre `DataFrame` (eager) y `LazyFrame` (lazy) y cuándo usar cada uno | 8 |
| Describe por qué Polars es más rápido que Pandas para datasets grandes (GIL, Arrow, paralelismo) | 8 |
| Distingue `group_by().agg()` de `select()` con expresiones de ventana | 7 |
| Explica qué ocurre internamente con `scan_csv().filter().collect()` (query plan) | 7 |

## Desempeño (40 pts)

| Indicador | Puntos |
|-----------|--------|
| Usa `pl.col()`, `pl.when().then().otherwise()` y expresiones encadenadas correctamente | 10 |
| Realiza `group_by` + `agg` con múltiples métricas sobre datos de Studio BC | 10 |
| Ejecuta joins entre DataFrames distintos (proyectos, horas, empleados) correctamente | 10 |
| Lee desde CSV/JSON y escribe Parquet con schema explícito | 10 |

## Producto (30 pts)

| Indicador | Puntos |
|-----------|--------|
| KPI Dashboard calcula correctamente: horas por proyecto, rentabilidad, variación presupuesto | 12 |
| El pipeline usa Lazy API con `scan_csv` y un único `collect()` al final | 8 |
| Salida del reporte usa Rich (tabla + panel) o escribe Parquet/JSON válido | 6 |
| Código pasa `mypy --strict` sin errores | 4 |
