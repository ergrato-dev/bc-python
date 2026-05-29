# DataFrames y Expresiones

## Objetivos

- Crear DataFrames desde dicts, listas y archivos
- Seleccionar, filtrar y transformar columnas con expresiones
- Usar `pl.col()`, `pl.when()`, `pl.lit()` y expresiones encadenadas
- Aplicar operaciones de strings y fechas

---

## 1. Crear DataFrames

```python
import polars as pl
from datetime import date

# Desde dict
df = pl.DataFrame({
    "project_id":  ["reel-2025", "reel-2025", "spot-bc-01", "spot-bc-01"],
    "employee":    ["Ana", "Luis", "Ana", "Carlos"],
    "hours":       [8.0, 6.5, 4.0, 7.5],
    "date":        [date(2025, 1, 13), date(2025, 1, 14), date(2025, 1, 13), date(2025, 1, 14)],
    "billable":    [True, True, False, True],
})

# Desde CSV
df = pl.read_csv("timesheets.csv", try_parse_dates=True)

# Schema explícito
df = pl.read_csv("timesheets.csv", schema={
    "project_id": pl.Utf8,
    "employee":   pl.Utf8,
    "hours":      pl.Float64,
    "date":       pl.Date,
})

# Ver estructura
print(df.schema)
print(df.shape)   # (rows, cols)
print(df.head(3))
print(df.describe())
```

---

## 2. `select()` — elegir columnas

```python
# Selección básica
df.select("project_id", "hours")
df.select(["project_id", "hours"])

# Con expresiones — transformar al seleccionar
df.select(
    pl.col("project_id"),
    pl.col("hours").round(1).alias("hours_rounded"),
    (pl.col("hours") * 150.0).alias("revenue_usd"),
)

# Todos los numéricos
df.select(pl.col(pl.NUMERIC_DTYPES))

# Excluir columnas
df.select(pl.exclude("billable", "date"))
```

---

## 3. `filter()` — filtrar filas

```python
# Condición simple
df.filter(pl.col("hours") > 6)

# Y lógico
df.filter(
    (pl.col("hours") > 6) & (pl.col("billable") == True)
)

# O lógico
df.filter(
    (pl.col("project_id") == "reel-2025") |
    (pl.col("hours") > 7)
)

# Valores nulos
df.filter(pl.col("hours").is_not_null())
df.filter(pl.col("hours").is_null())

# `is_in` — equivalente a SQL IN
df.filter(pl.col("employee").is_in(["Ana", "Luis"]))

# Filtrado por fecha
df.filter(pl.col("date") >= date(2025, 1, 14))
```

---

## 4. `with_columns()` — añadir / modificar columnas

```python
df = df.with_columns(
    # Columna calculada
    (pl.col("hours") * 150.0).alias("revenue_usd"),

    # Modificar columna existente
    pl.col("employee").str.to_uppercase(),

    # Múltiples en una llamada
    pl.col("hours").round(0).alias("hours_int"),
    pl.lit("draft").alias("status"),   # pl.lit(): valor constante
)
```

`with_columns()` es **inmutable** — retorna un nuevo DataFrame. El original no cambia.

---

## 5. `pl.col()` — la expresión fundamental

```python
# Referencia a columna
pl.col("hours")

# Múltiples columnas
pl.col("hours", "revenue_usd")

# Por tipo
pl.col(pl.Float64)
pl.col(pl.Utf8)

# Wildcard — todas las columnas
pl.col("*")

# Excluir
pl.exclude("date")

# Renombrar
pl.col("hours").alias("hrs")

# Encadenamiento
pl.col("hours").round(1).cast(pl.Float32).alias("hours_f32")
```

---

## 6. `pl.when().then().otherwise()` — condicional

```python
# Equivalente a SQL CASE WHEN
df = df.with_columns(
    pl.when(pl.col("hours") > 8)
    .then(pl.lit("overtime"))
    .when(pl.col("hours") >= 6)
    .then(pl.lit("full"))
    .otherwise(pl.lit("partial"))
    .alias("shift_type")
)

# Con expresiones en then/otherwise
df = df.with_columns(
    pl.when(pl.col("billable"))
    .then(pl.col("hours") * 150.0)
    .otherwise(pl.lit(0.0))
    .alias("billable_revenue")
)

# Múltiples condiciones encadenadas
df = df.with_columns(
    pl.when(pl.col("hours").is_null())
    .then(pl.lit(0.0))
    .otherwise(pl.col("hours"))
    .alias("hours_safe")
)
```

---

## 7. Operaciones de strings

```python
df.with_columns(
    pl.col("employee").str.to_uppercase().alias("emp_upper"),
    pl.col("project_id").str.replace("-", "_").alias("project_slug"),
    pl.col("project_id").str.starts_with("reel").alias("is_reel"),
    pl.col("employee").str.len_chars().alias("name_len"),
    pl.col("project_id").str.split("-").alias("id_parts"),  # → List[Utf8]
)

# Extraer con regex
df.with_columns(
    pl.col("project_id").str.extract(r"(\d{4})$", 1).alias("year")
)
```

---

## 8. Operaciones de fechas

```python
df.with_columns(
    pl.col("date").dt.year().alias("year"),
    pl.col("date").dt.month().alias("month"),
    pl.col("date").dt.week().alias("week"),
    pl.col("date").dt.weekday().alias("weekday"),  # 0=Mon … 6=Sun
    pl.col("date").dt.strftime("%Y-%m").alias("month_label"),
)

# Filtrar por rango de fechas
df.filter(
    pl.col("date").is_between(date(2025, 1, 1), date(2025, 1, 31))
)

# Diferencia entre fechas
df.with_columns(
    (pl.col("due_date") - pl.col("start_date")).dt.total_days().alias("days_to_deadline")
)
```

---

## 9. `sort()`, `unique()`, `drop_nulls()`

```python
# Ordenar
df.sort("hours", descending=True)
df.sort(["project_id", "date"])

# Únicos
df.unique(subset=["employee"])          # por columnas específicas
df.unique()                              # todas las columnas

# Nulos
df.drop_nulls()                          # elimina filas con cualquier null
df.drop_nulls(subset=["hours"])          # solo si hours es null
df.fill_null(0)                          # reemplaza nulls por 0
df.fill_null(strategy="forward")         # fill forward
```

---

## ✅ Resumen

| Operación | Método |
|-----------|--------|
| Seleccionar columnas | `select(...)` |
| Filtrar filas | `filter(pl.col(...))` |
| Añadir/modificar columnas | `with_columns(...)` |
| Condicional | `pl.when().then().otherwise()` |
| Valor constante | `pl.lit(value)` |
| Strings | `pl.col(...).str.*` |
| Fechas | `pl.col(...).dt.*` |
| Ordenar | `sort(col, descending=)` |

---

## Recursos Adicionales

- [Polars — Expressions](https://docs.pola.rs/user-guide/expressions/)
- [Polars — String functions](https://docs.pola.rs/api/python/stable/reference/expressions/string.html)
