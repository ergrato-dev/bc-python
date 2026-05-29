# Lazy API y Optimización

## Objetivos

- Entender la diferencia entre `DataFrame` (eager) y `LazyFrame` (lazy)
- Usar `scan_csv()` y `scan_parquet()` para leer sin cargar en memoria
- Visualizar el query plan antes de ejecutar
- Aplicar `collect()` y streaming para datasets grandes

---

## 1. Eager vs Lazy

```python
import polars as pl

# EAGER — ejecuta cada operación inmediatamente
df = pl.read_csv("timesheets.csv")        # carga todo en RAM
df = df.filter(pl.col("hours") > 6)      # opera en RAM
df = df.group_by("project_id").agg(...)  # opera en RAM

# LAZY — construye un plan, ejecuta todo de una vez al final
lf = pl.scan_csv("timesheets.csv")        # NO lee el archivo
lf = lf.filter(pl.col("hours") > 6)      # NO filtra aún
lf = lf.group_by("project_id").agg(...)  # NO agrupa aún

result = lf.collect()   # aquí se ejecuta todo, de forma optimizada
```

La Lazy API permite a Polars:
1. **Predicate pushdown** — aplicar filtros antes de leer columnas innecesarias
2. **Projection pushdown** — leer solo las columnas usadas desde Parquet
3. **Query reordering** — reordenar operaciones para mayor eficiencia

---

## 2. `scan_*` — leer sin cargar en memoria

```python
import polars as pl

# scan_csv — compatible con glob
lf = pl.scan_csv("data/timesheets_*.csv")

# scan_parquet — especialmente eficiente (columnar)
lf = pl.scan_parquet("data/monthly/*.parquet")

# scan_json / scan_ndjson
lf = pl.scan_ndjson("data/events.ndjson")

# Encadenar transformaciones
result = (
    pl.scan_parquet("data/timesheets.parquet")
    .filter(pl.col("date") >= date(2025, 1, 1))
    .select(["project_id", "employee", "hours"])
    .group_by("project_id")
    .agg(pl.col("hours").sum())
    .sort("hours", descending=True)
    .collect()
)
```

---

## 3. Visualizar el query plan

```python
lf = (
    pl.scan_csv("timesheets.csv")
    .filter(pl.col("hours") > 6)
    .group_by("project_id")
    .agg(pl.col("hours").sum())
)

# Plan lógico (lo que pediste)
print(lf.explain())

# Plan físico (lo que Polars ejecutará, con optimizaciones)
print(lf.explain(optimized=True))
```

Salida típica con predicate pushdown:
```
 AGGREGATE
  [col("hours").sum()]
  BY [col("project_id")]
    CSV SCAN [timesheets.csv]
    PROJECT */5 COLUMNS
    SELECTION: [(col("hours")) > (6)]   ← el filtro se empujó al scan
```

---

## 4. `LazyFrame.collect()` vs `fetch()`

```python
# collect() — ejecuta todo el plan sobre todos los datos
result: pl.DataFrame = lf.collect()

# fetch(n) — ejecuta el plan sobre los primeros n registros
# Útil para probar el pipeline sin cargar todos los datos
sample: pl.DataFrame = lf.fetch(100)

# collect() con streaming para datasets muy grandes
result = lf.collect(streaming=True)
# streaming=True procesa en chunks — menor uso de RAM, más lento
```

---

## 5. `from_dataframe()` / `lazy()` — convertir entre eager y lazy

```python
import polars as pl

# DataFrame → LazyFrame
df = pl.read_csv("timesheets.csv")
lf = df.lazy()

# LazyFrame → DataFrame
result = lf.filter(pl.col("hours") > 6).collect()

# Patrón recomendado:
# - scan_* para leer
# - transformaciones en lazy
# - collect() solo al final
```

---

## 6. Pipeline de producción con Lazy API

```python
from datetime import date
import polars as pl
from pathlib import Path

def build_kpi_report(
    timesheets_path: str,
    projects_path: str,
    output_path: str,
    since: date = date(2025, 1, 1),
) -> pl.DataFrame:
    """
    Pipeline completo con Lazy API:
    1. scan ambos CSVs sin cargar en memoria
    2. filtrar, transformar, unir y agregar
    3. collect() una sola vez al final
    """
    timesheets = (
        pl.scan_csv(timesheets_path, try_parse_dates=True)
        .filter(pl.col("date") >= since)                  # predicate pushdown
        .select(["project_id", "employee", "hours", "billable"])
    )

    projects = pl.scan_csv(projects_path)

    result = (
        timesheets
        .group_by("project_id")
        .agg(
            pl.col("hours").sum().alias("total_hours"),
            pl.col("hours")
            .filter(pl.col("billable"))
            .sum()
            .alias("billable_hours"),
            pl.col("employee").n_unique().alias("team_size"),
        )
        .join(projects, on="project_id", how="left")
        .with_columns(
            (pl.col("billable_hours") / pl.col("total_hours") * 100)
            .round(1)
            .alias("billable_pct"),
        )
        .sort("total_hours", descending=True)
        .collect()   # ← un único collect al final
    )

    result.write_parquet(output_path)
    return result
```

---

## 7. Cuándo usar Lazy vs Eager

```
¿Qué API usar?
│
├─ ¿Dataset > RAM disponible? → Lazy + collect(streaming=True)
│
├─ ¿Múltiples archivos (glob)? → scan_* (Lazy)
│
├─ ¿Pipeline con filtros y selecciones antes de agrupar? → Lazy (predicate pushdown)
│
├─ ¿Exploración interactiva (Jupyter)? → Eager (más directo)
│
└─ ¿Dataset pequeño (< 100k filas)? → Eager (suficiente)
```

---

## ✅ Resumen

| Concepto | API |
|---------|-----|
| Crear LazyFrame | `pl.scan_csv()` / `df.lazy()` |
| Ejecutar | `.collect()` |
| Muestra rápida | `.fetch(n)` |
| Ver plan | `.explain()` / `.explain(optimized=True)` |
| Streaming | `.collect(streaming=True)` |
| Ventajas | predicate pushdown, projection pushdown, paralelismo |

---

## Recursos Adicionales

- [Polars — Lazy API](https://docs.pola.rs/user-guide/lazy/)
- [Polars — Query optimization](https://docs.pola.rs/user-guide/lazy/query_plan/)
