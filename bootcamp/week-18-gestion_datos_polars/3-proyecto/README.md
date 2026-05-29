# Proyecto Semana 18 — Studio BC KPI Dashboard

## Descripción

Construir un pipeline de análisis de datos para Studio BC que procese timesheets, proyectos y tarifas para generar un reporte de KPIs: horas trabajadas, rentabilidad por proyecto, variación presupuesto vs real, y tendencias por semana.

---

## Requerimientos

### Pipeline (Lazy API)

El pipeline debe usar `scan_csv()` y un único `collect()` al final:

```python
# Estructura esperada
result = (
    pl.scan_csv("data/timesheets.csv", ...)
    .join(pl.scan_csv("data/rates.csv"), ...)
    .with_columns(...)
    .group_by(...)
    .agg(...)
    .join(pl.scan_csv("data/projects.csv"), ...)
    .with_columns(...)
    .collect()
)
```

### KPIs a calcular

| KPI | Descripción |
|-----|-------------|
| `total_hours` | Suma de horas por proyecto |
| `billable_hours` | Horas donde `billable=True` |
| `billable_pct` | `billable_hours / total_hours * 100` |
| `total_cost_usd` | `sum(hours * hourly_rate)` |
| `budget_usd` | Del CSV de proyectos |
| `margin_usd` | `budget_usd - total_cost_usd` |
| `margin_pct` | `margin_usd / budget_usd * 100` |
| `team_size` | Empleados únicos por proyecto |

### Tendencia semanal

DataFrame separado con `(project_id, week, total_hours)` usando `group_by("project_id", week)`.

### Salida

1. `output/kpi_report.parquet` — reporte principal
2. `output/weekly_trend.parquet` — tendencia semanal
3. `output/kpi_report.json` — reporte principal en JSON
4. Consola: tabla Rich con el resumen de KPIs

---

## Estructura del proyecto

```
starter/
├── src/
│   ├── pipeline.py     — función build_kpi_pipeline() con Lazy API
│   ├── reporter.py     — función print_kpi_table() con Rich
│   └── __init__.py
├── data/
│   ├── timesheets.csv
│   ├── projects.csv
│   └── rates.csv
├── output/             # generado al ejecutar
├── main.py
└── pyproject.toml
```

---

## Rúbrica (30 pts)

| Criterio | Puntos |
|----------|--------|
| Pipeline usa Lazy API (`scan_csv` + único `collect()`) | 8 |
| KPIs calculados correctamente (todos los 8 campos) | 12 |
| Escritura de Parquet y JSON en `output/` | 5 |
| Reporte Rich con tabla de KPIs en consola | 3 |
| mypy --strict pasa sin errores | 2 |

## Bonus (+5 pts)

Añadir un análisis de tendencia: detectar proyectos donde las horas reales superaron el 90% del presupuesto y mostrarlos en un panel de alerta en Rich.

---

## Ejecutar

```bash
cd starter
uv run python main.py
```

Resultado esperado:
```
── Studio BC KPI Report ──
project_id   | hours | cost_usd | budget | margin | margin_pct
reel-2025    | 25.5  | 2805.0   | 8000   | 5195.0 | 64.9%
spot-bc-01   | 16.0  | 1760.0   | 2500   |  740.0 | 29.6%
short-film   | 17.5  | 2145.0   | 5000   | 2855.0 | 57.1%

Saved: output/kpi_report.parquet · output/kpi_report.json
```
