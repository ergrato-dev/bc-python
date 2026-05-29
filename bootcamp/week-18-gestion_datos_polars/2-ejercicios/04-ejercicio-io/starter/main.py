"""
Ejercicio 04 — I/O de Datos
Studio BC: leer y escribir en distintos formatos.
"""

import polars as pl
from pathlib import Path

output = Path("output")
output.mkdir(exist_ok=True)


# ─────────────────────────────────────────────
# PASO 1 — CSV con opciones avanzadas
# ─────────────────────────────────────────────

# TODO: lee data/timesheets.csv con:
# - null_values=[""]
# - try_parse_dates=True
# - schema_overrides={"hours": pl.Float32}
# df = pl.read_csv("data/timesheets.csv", ...)
# print(df.dtypes)
# print(df.head(3))


# ─────────────────────────────────────────────
# PASO 2 — Parquet
# ─────────────────────────────────────────────

# TODO: escribe df a output/timesheets.parquet con compression="zstd"
# df.write_parquet("output/timesheets.parquet", compression="zstd")

# TODO: lee el parquet de vuelta y verifica shape y dtypes
# df_back = pl.read_parquet("output/timesheets.parquet")
# assert df.shape == df_back.shape, "Shape mismatch!"
# print("Parquet OK — shape:", df_back.shape)


# ─────────────────────────────────────────────
# PASO 3 — JSON
# ─────────────────────────────────────────────

# TODO: genera summary = group_by("project_id").agg(total_hours, unique_employees)
# escríbelo a output/summary.json
# léelo de vuelta con pl.read_json()
# summary = ...
# summary.write_json("output/summary.json")
# summary_back = pl.read_json("output/summary.json")
# print(summary_back)


# ─────────────────────────────────────────────
# PASO 4 — scan_csv vs read_csv
# ─────────────────────────────────────────────

# TODO: implementa la misma transformación con scan_csv:
# lf = pl.scan_csv("data/timesheets.csv", try_parse_dates=True)
# result_lazy = (
#     lf
#     .filter(pl.col("hours") > 6)
#     .group_by("project_id")
#     .agg(pl.col("hours").sum())
#     .collect()
# )

# Compara con eager:
# result_eager = (
#     pl.read_csv("data/timesheets.csv", try_parse_dates=True)
#     .filter(pl.col("hours") > 6)
#     .group_by("project_id")
#     .agg(pl.col("hours").sum())
# )
# print("Resultados idénticos:", result_lazy.sort("project_id").equals(result_eager.sort("project_id")))


if __name__ == "__main__":
    print("── Paso 1: CSV ──")
    # descomenta los pasos
