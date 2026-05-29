# Polars vs Pandas

## Objetivos

- Entender por qué Polars es más rápido que Pandas
- Conocer las diferencias de API más importantes
- Decidir cuándo usar Polars vs Pandas

---

## 1. Por qué Polars es más rápido

Polars está construido sobre **Apache Arrow** y escrito en Rust. Las diferencias clave:

| Aspecto | Pandas | Polars |
|---------|--------|--------|
| Memoria | NumPy arrays (por columna) | Apache Arrow (columnar, contiguo) |
| GIL | Afectado (Python loops) | Evadido (Rust, multi-thread) |
| Paralelismo | No (por defecto) | Sí (automático en columnas) |
| Evaluación | Eager (inmediata) | Eager + **Lazy** (optimizada) |
| Tipos nulos | `NaN` (float) o `pd.NA` | `null` nativo en todos los tipos |
| Índice | Sí (Index object) | **No** (sin índice, más simple) |

```python
# Pandas — operación en columnas: ~0.8s en 10M filas
import pandas as pd
df = pd.read_csv("timesheets.csv")
result = df.groupby("project_id")["hours"].sum()

# Polars — misma operación: ~0.1s (8× más rápido)
import polars as pl
result = pl.read_csv("timesheets.csv").group_by("project_id").agg(pl.col("hours").sum())
```

---

## 2. Diferencias de API principales

```python
import polars as pl
import pandas as pd

# ── Selección de columnas ──
df_pd["name"]               # pandas: Series
df_pd[["name", "hours"]]    # pandas: DataFrame

df_pl["name"]               # polars: Series
df_pl.select("name")        # polars: DataFrame
df_pl.select(["name", "hours"])

# ── Filtrado ──
df_pd[df_pd["hours"] > 8]                     # pandas: boolean indexing
df_pl.filter(pl.col("hours") > 8)             # polars: expresión

# ── Nueva columna ──
df_pd["overtime"] = df_pd["hours"] - 8        # pandas: mutación in-place
df_pl = df_pl.with_columns(
    (pl.col("hours") - 8).alias("overtime")   # polars: inmutable, retorna nuevo DF
)

# ── Renombrar ──
df_pd.rename(columns={"hours": "hrs"})
df_pl.rename({"hours": "hrs"})

# ── Nulos ──
df_pd.fillna(0)
df_pl.fill_null(0)
```

---

## 3. Sin índice — un diseño más simple

Pandas indexa filas con un `Index` que complica muchas operaciones (`reset_index`, `set_index`, `merge` por índice). Polars elimina este concepto: las filas se identifican solo por posición o por valores de columnas.

```python
# Pandas — el índice se convierte en problema frecuente
df = pd.read_csv("timesheets.csv")
result = df.groupby("project_id")["hours"].sum()
# result ahora tiene project_id como INDEX, no como columna
result.reset_index()   # necesario para seguir operando

# Polars — group_by siempre retorna DataFrame "plano"
result = (
    pl.read_csv("timesheets.csv")
    .group_by("project_id")
    .agg(pl.col("hours").sum())
)
# project_id es una columna normal, no hay índice
```

---

## 4. Tipos de datos

```python
import polars as pl

df = pl.DataFrame({
    "project_id": ["reel-2025", "spot-bc-01"],
    "hours":      [42.5, 18.0],
    "date":       ["2025-01-15", "2025-01-16"],
    "paid":       [True, False],
})

# Polars infiere tipos automáticamente
print(df.dtypes)
# [Utf8, Float64, Utf8, Boolean]

# Cast explícito
df = df.with_columns(
    pl.col("date").str.to_date("%Y-%m-%d"),
    pl.col("hours").cast(pl.Float32),
)

# Tipos comunes
# pl.Int8/16/32/64, pl.UInt8/16/32/64
# pl.Float32/64
# pl.Boolean
# pl.Utf8 (= String)
# pl.Date, pl.Datetime, pl.Duration
# pl.List(pl.Int64)   — columna de listas
# pl.Struct(...)      — columna de structs
```

---

## 5. Cuándo usar cada uno

```
¿Qué biblioteca usar?
│
├─ ¿Dataset > 1 GB o necesitas máximo rendimiento? → Polars
│
├─ ¿Codebase existente en Pandas (sklearn, statsmodels, seaborn)? → Pandas
│   (o usa pl.DataFrame.to_pandas() para interoperar)
│
├─ ¿Necesitas operaciones de series de tiempo complejas? → Pandas (más maduro)
│
├─ ¿Pipeline de datos desde fuentes CSV/Parquet hasta reporte? → Polars + Lazy API
│
└─ ¿Jupyter + exploración visual rápida? → Pandas (mejor integración con matplotlib)
```

Polars tiene un método `to_pandas()` y puede leer DataFrames de Pandas con `pl.from_pandas()`.

---

## Recursos Adicionales

- [Polars docs](https://docs.pola.rs/)
- [Polars vs Pandas — user guide](https://docs.pola.rs/user-guide/migration/pandas/)
- [Apache Arrow](https://arrow.apache.org/)
