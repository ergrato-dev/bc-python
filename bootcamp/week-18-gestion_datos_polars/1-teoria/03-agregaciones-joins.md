# Agregaciones y Joins

## Objetivos

- Usar `group_by().agg()` con múltiples métricas
- Realizar todos los tipos de join entre DataFrames
- Aplicar `pivot` y `unpivot` para reformatear datos
- Usar expresiones de ventana (`over`)

---

## 1. `group_by().agg()` — agregaciones

```python
import polars as pl

timesheets = pl.DataFrame({
    "project_id": ["reel-2025", "reel-2025", "spot-bc-01", "spot-bc-01", "reel-2025"],
    "employee":   ["Ana", "Luis", "Ana", "Carlos", "Ana"],
    "hours":      [8.0, 6.5, 4.0, 7.5, 5.0],
    "billable":   [True, True, False, True, True],
})

# Agregación básica
summary = (
    timesheets
    .group_by("project_id")
    .agg(
        pl.col("hours").sum().alias("total_hours"),
        pl.col("hours").mean().alias("avg_hours"),
        pl.col("hours").max().alias("max_hours"),
        pl.col("employee").n_unique().alias("unique_employees"),
        pl.col("billable").filter(pl.col("billable")).len().alias("billable_count"),
    )
)
```

### Funciones de agregación comunes

```python
pl.col("hours").sum()
pl.col("hours").mean()
pl.col("hours").median()
pl.col("hours").std()
pl.col("hours").min()
pl.col("hours").max()
pl.col("hours").count()       # no-null count
pl.col("hours").len()         # total count including nulls
pl.col("employee").n_unique()
pl.col("employee").first()
pl.col("employee").last()
pl.col("hours").quantile(0.95)
```

### `group_by` con múltiples columnas

```python
(
    timesheets
    .group_by("project_id", "employee")
    .agg(
        pl.col("hours").sum(),
        pl.col("billable").all().alias("all_billable"),
    )
    .sort("project_id")
)
```

---

## 2. Expresiones de ventana — `over()`

`over()` aplica una función de ventana sin colapsar filas (similar a SQL `PARTITION BY`):

```python
# Añadir el total del proyecto como columna a cada fila
timesheets.with_columns(
    pl.col("hours").sum().over("project_id").alias("project_total_hours"),
    pl.col("hours").mean().over("project_id").alias("project_avg_hours"),
    (pl.col("hours") / pl.col("hours").sum().over("project_id")).alias("pct_of_project"),
)
# Todas las filas se mantienen — solo se añaden columnas calculadas por grupo
```

---

## 3. Joins

```python
projects = pl.DataFrame({
    "project_id": ["reel-2025", "spot-bc-01", "short-film"],
    "client":     ["Estudio Norte", "BC Media", "Canal 9"],
    "budget_usd": [8000.0, 2500.0, 5000.0],
})

hours = pl.DataFrame({
    "project_id": ["reel-2025", "reel-2025", "spot-bc-01"],
    "employee":   ["Ana", "Luis", "Carlos"],
    "hours":      [42.0, 18.0, 15.0],
})

# Inner join — solo filas con match en ambos
projects.join(hours, on="project_id", how="inner")

# Left join — todas las filas de projects, null si no hay match en hours
projects.join(hours, on="project_id", how="left")

# Right join — todas las filas de hours
projects.join(hours, on="project_id", how="right")

# Full outer join — todas las filas de ambos
projects.join(hours, on="project_id", how="full")

# Cross join — producto cartesiano
projects.join(hours, how="cross")

# Join por múltiples columnas
df1.join(df2, on=["project_id", "employee"], how="inner")

# Join con columnas de diferente nombre
df1.join(df2, left_on="project_id", right_on="proj_id", how="left")
```

### Joins y nulos (left join)

```python
result = projects.join(hours, on="project_id", how="left")
# short-film no tiene horas → employee y hours serán null

# Rellenar los nulls post-join
result.with_columns(
    pl.col("hours").fill_null(0.0),
    pl.col("employee").fill_null("—"),
)
```

---

## 4. `pivot` y `unpivot`

### `pivot` — de filas a columnas

```python
monthly = pl.DataFrame({
    "project_id": ["reel-2025", "reel-2025", "spot-bc-01", "spot-bc-01"],
    "month":      ["Jan", "Feb", "Jan", "Feb"],
    "hours":      [42.0, 38.0, 15.0, 20.0],
})

# Convertir meses en columnas
pivot = monthly.pivot(
    values="hours",
    index="project_id",
    on="month",
    aggregate_function="sum",
)
# project_id | Jan  | Feb
# reel-2025  | 42.0 | 38.0
# spot-bc-01 | 15.0 | 20.0
```

### `unpivot` — de columnas a filas (inverso de pivot)

```python
# Revertir el pivot anterior
pivot.unpivot(
    on=["Jan", "Feb"],
    index="project_id",
    variable_name="month",
    value_name="hours",
)
```

---

## 5. Concat — unir DataFrames

```python
# Vertical (mismo schema)
combined = pl.concat([df_q1, df_q2, df_q3])

# Horizontal (misma cantidad de filas)
pl.concat([df_names, df_hours], how="horizontal")

# Diagonal (diferentes schemas — rellena nulls)
pl.concat([df_2024, df_2025], how="diagonal")
```

---

## 6. Pipeline completo: reporte de rentabilidad

```python
projects = pl.read_csv("projects.csv")
timesheets = pl.read_csv("timesheets.csv")
rates = pl.read_csv("rates.csv")   # employee, hourly_rate_usd

# 1. Calcular horas y costo por proyecto
cost_by_project = (
    timesheets
    .join(rates, on="employee", how="left")
    .with_columns(
        (pl.col("hours") * pl.col("hourly_rate_usd")).alias("cost_usd")
    )
    .group_by("project_id")
    .agg(
        pl.col("hours").sum().alias("total_hours"),
        pl.col("cost_usd").sum().alias("total_cost_usd"),
    )
)

# 2. Unir con proyectos y calcular rentabilidad
report = (
    projects
    .join(cost_by_project, on="project_id", how="left")
    .with_columns(
        pl.col("total_cost_usd").fill_null(0.0),
        (pl.col("budget_usd") - pl.col("total_cost_usd")).alias("margin_usd"),
        (
            (pl.col("budget_usd") - pl.col("total_cost_usd"))
            / pl.col("budget_usd") * 100
        ).round(1).alias("margin_pct"),
    )
    .sort("margin_pct")
)
```

---

## ✅ Resumen

| Operación | Método |
|-----------|--------|
| Agrupar y agregar | `group_by(...).agg(...)` |
| Función de ventana | `pl.col(...).sum().over("group")` |
| Inner join | `.join(..., how="inner")` |
| Left join | `.join(..., how="left")` |
| Full outer join | `.join(..., how="full")` |
| Filas → columnas | `.pivot(values=, index=, on=)` |
| Columnas → filas | `.unpivot(on=, index=)` |
| Unir DataFrames | `pl.concat([df1, df2])` |

---

## Recursos Adicionales

- [Polars — Group by](https://docs.pola.rs/user-guide/transformations/group_by/)
- [Polars — Joins](https://docs.pola.rs/user-guide/transformations/joins/)
