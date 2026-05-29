"""
Ejercicio 01 — DataFrames Básico
Studio BC: exploración de datos de timesheets.
"""

import polars as pl

# ─────────────────────────────────────────────
# PASO 1 — Cargar y explorar
# ─────────────────────────────────────────────

# TODO: lee timesheets.csv con try_parse_dates=True
# df = pl.read_csv("timesheets.csv", try_parse_dates=True)
# print("Schema:", df.schema)
# print("Shape:", df.shape)
# print(df.head(3))
# print(df.describe())


# ─────────────────────────────────────────────
# PASO 2 — Selección con columna calculada
# ─────────────────────────────────────────────

# TODO: selecciona project_id, employee, hours
# añade revenue_usd = hours * 120
# selected = df.select(
#     pl.col("project_id"),
#     pl.col("employee"),
#     pl.col("hours"),
#     (pl.col("hours") * 120.0).alias("revenue_usd"),
# )
# print(selected)


# ─────────────────────────────────────────────
# PASO 3 — Filtrado
# ─────────────────────────────────────────────

# TODO: filtra hours > 6 AND billable == True
# filtered = df.filter(...)
# print(f"Filas con hours > 6 y billable: {len(filtered)}")


# ─────────────────────────────────────────────
# PASO 4 — Sort y unique
# ─────────────────────────────────────────────

# TODO: ordena por hours descendente
# sorted_df = df.sort("hours", descending=True)
# print(sorted_df.select("employee", "hours").head(5))

# TODO: obtén valores únicos de employee
# employees = df["employee"].unique().sort()
# print("Empleados:", employees.to_list())


if __name__ == "__main__":
    print("── Paso 1: explorar ──")
    # TODO: descomenta los pasos
