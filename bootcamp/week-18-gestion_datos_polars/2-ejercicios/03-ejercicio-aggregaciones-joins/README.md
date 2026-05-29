# Ejercicio 03 — Agregaciones y Joins

## Objetivos
- Calcular KPIs por proyecto con `group_by().agg()`
- Unir DataFrames con distintos tipos de join
- Usar `over()` para funciones de ventana

## Duración estimada
40 minutos

## Pasos

### Paso 1 — `group_by` simple
Calcula para cada `project_id`: total_hours, avg_hours, empleados únicos.

### Paso 2 — `group_by` por múltiples columnas
Agrupa por `project_id` y `employee`. Calcula: sum de hours, count de días.

### Paso 3 — Join con projects
Une el resultado del Paso 1 con `projects.csv` (left join por project_id).
Calcula `margin_usd = budget_usd - (total_hours * 110)`.

### Paso 4 — Función de ventana con `over()`
Añade `pct_of_project = hours / sum(hours over project_id) * 100` a cada fila.

## Ejecutar
```bash
cd starter
uv run python main.py
```
