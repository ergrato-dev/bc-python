# I/O — Formatos de Datos

## Objetivos

- Leer y escribir CSV con opciones avanzadas
- Trabajar con Excel usando `openpyxl`
- Usar Parquet para almacenamiento eficiente
- Leer y escribir JSON y NDJSON

---

## 1. CSV

```python
import polars as pl

# Lectura básica
df = pl.read_csv("timesheets.csv")

# Opciones de lectura
df = pl.read_csv(
    "timesheets.csv",
    separator=";",                    # delimitador alternativo
    has_header=True,
    skip_rows=2,                      # saltar filas iniciales
    n_rows=1000,                      # leer solo primeras N filas
    try_parse_dates=True,             # parsear fechas automáticamente
    null_values=["", "N/A", "null"],  # tratar como null
    schema={
        "project_id": pl.Utf8,
        "hours":      pl.Float64,
        "date":       pl.Date,
    },
    encoding="utf8-lossy",            # tolerar caracteres inválidos
)

# Escritura
df.write_csv("output/timesheets_clean.csv")
df.write_csv("output/timesheets_clean.csv", separator=";")

# Sin header
df.write_csv("output/data.csv", has_header=False)
```

---

## 2. Excel — `openpyxl`

Polars usa `openpyxl` para Excel. Debe estar instalado:

```toml
# pyproject.toml
dependencies = ["polars", "openpyxl"]
```

```python
import polars as pl

# Leer Excel
df = pl.read_excel("studio_report.xlsx")

# Hoja específica
df = pl.read_excel("studio_report.xlsx", sheet_name="Timesheets")

# Con opciones
df = pl.read_excel(
    "studio_report.xlsx",
    sheet_name="Timesheets",
    read_options={"header_row": 1},   # fila de encabezados (0-indexed)
)

# Escribir Excel
df.write_excel("output/report.xlsx")

# Múltiples hojas en un workbook
from openpyxl import Workbook

wb = Workbook()
ws_ts = wb.active
ws_ts.title = "Timesheets"
ws_proj = wb.create_sheet("Projects")

# Escribir cada DataFrame en su hoja
timesheets_df.write_excel(wb.active)    # forma directa no disponible con múltiples hojas
# Para múltiples hojas, usar write_excel con engine="openpyxl" vía XlsxWriter o BytesIO
```

### Escritura multi-hoja con BytesIO

```python
import io
from openpyxl import load_workbook
import polars as pl

def write_multi_sheet(sheets: dict[str, pl.DataFrame], path: str) -> None:
    """Escribe múltiples DataFrames en distintas hojas de un Excel."""
    buffers: dict[str, bytes] = {}
    for name, df in sheets.items():
        buf = io.BytesIO()
        df.write_excel(buf)
        buffers[name] = buf.getvalue()

    # Cargar el primero y agregar las demás hojas
    wb = load_workbook(io.BytesIO(next(iter(buffers.values()))))
    wb.active.title = next(iter(sheets.keys()))

    for name, data in list(buffers.items())[1:]:
        src = load_workbook(io.BytesIO(data)).active
        ws = wb.create_sheet(title=name)
        for row in src.iter_rows(values_only=True):
            ws.append(row)

    wb.save(path)
```

---

## 3. Parquet — el formato eficiente

Parquet es columnar y comprimido. Ideal para almacenar datasets procesados:

```python
import polars as pl

# Leer
df = pl.read_parquet("timesheets.parquet")

# Leer columnas específicas (Parquet es columnar — solo lee las que necesitas)
df = pl.read_parquet("timesheets.parquet", columns=["project_id", "hours", "date"])

# Escribir
df.write_parquet("output/timesheets.parquet")

# Con compresión
df.write_parquet("output/timesheets.parquet", compression="zstd")
# Opciones: "snappy" (default), "gzip", "lz4", "zstd", "uncompressed"

# Lazy con scan_parquet (no carga en memoria hasta collect())
lf = pl.scan_parquet("timesheets.parquet")
result = lf.filter(pl.col("hours") > 6).collect()
```

### Parquet vs CSV

| Aspecto | CSV | Parquet |
|---------|-----|---------|
| Legible por humanos | Sí | No |
| Tamaño | ~10× | Comprimido |
| Velocidad de lectura | Lenta | Rápida (columnar) |
| Tipos preservados | No | Sí |
| Recomendado para | Intercambio | Almacenamiento intermedio |

---

## 4. JSON y NDJSON

```python
import polars as pl

# JSON — array de objetos
df = pl.read_json("assets.json")
df.write_json("output/assets.json")

# NDJSON — un objeto por línea (Newline-Delimited JSON)
# Más eficiente para archivos grandes
df = pl.read_ndjson("events.ndjson")
df.write_ndjson("output/events.ndjson")

# Convertir a/desde dict de Python
data = df.to_dicts()          # list[dict[str, Any]]
df2 = pl.from_dicts(data)

# Convertir a JSON string
json_str: str = df.serialize(format="json")
```

---

## 5. Múltiples archivos — glob patterns

```python
# Leer todos los CSV de un directorio
df = pl.read_csv("data/timesheets_*.csv")

# Leer múltiples Parquet
df = pl.read_parquet("data/monthly/*.parquet")

# Con Lazy API (eficiente para muchos archivos)
lf = pl.scan_csv("data/timesheets_*.csv")
result = lf.filter(pl.col("hours") > 4).collect()
```

---

## 6. Escritura con schema y validación

```python
import polars as pl
from pathlib import Path

def save_report(df: pl.DataFrame, output_path: Path) -> None:
    """Valida el schema antes de escribir."""
    expected = {
        "project_id":  pl.Utf8,
        "total_hours": pl.Float64,
        "margin_usd":  pl.Float64,
        "margin_pct":  pl.Float64,
    }

    for col, dtype in expected.items():
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")
        if df[col].dtype != dtype:
            raise TypeError(f"Column {col}: expected {dtype}, got {df[col].dtype}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(output_path)
    print(f"Saved {len(df)} rows to {output_path}")
```

---

## ✅ Resumen

| Formato | Leer | Escribir | Cuándo |
|---------|------|---------|--------|
| CSV | `read_csv()` | `write_csv()` | Intercambio, datos de entrada |
| Excel | `read_excel()` | `write_excel()` | Reportes para usuarios finales |
| Parquet | `read_parquet()` | `write_parquet()` | Almacenamiento intermedio |
| JSON | `read_json()` | `write_json()` | APIs, configuración |
| NDJSON | `read_ndjson()` | `write_ndjson()` | Logs, streaming events |

---

## Recursos Adicionales

- [Polars — IO docs](https://docs.pola.rs/user-guide/io/)
- [openpyxl docs](https://openpyxl.readthedocs.io/)
- [Apache Parquet format](https://parquet.apache.org/)
