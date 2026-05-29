"""
Ejercicio 02 — Expresiones Encadenadas
Studio BC: transformaciones de datos con pl.when() y encadenamiento.
"""

import polars as pl

df = pl.read_csv("timesheets.csv", try_parse_dates=True)

# ─────────────────────────────────────────────
# PASO 1 — pl.when() para clasificación
# ─────────────────────────────────────────────

# TODO: añade shift_type con pl.when().then().otherwise()
# step1 = df.with_columns(
#     pl.when(pl.col("hours") > 8).then(pl.lit("overtime"))
#     .when(pl.col("hours") >= 6).then(pl.lit("full"))
#     .otherwise(pl.lit("partial"))
#     .alias("shift_type")
# )
# print(step1.select("employee", "hours", "shift_type"))


# ─────────────────────────────────────────────
# PASO 2 — Transformaciones de strings
# ─────────────────────────────────────────────

# TODO: añade employee_upper y project_short
# step2 = df.with_columns(
#     pl.col("employee").str.to_uppercase().alias("employee_upper"),
#     pl.col("project_id").str.slice(0, 4).alias("project_short"),
# )
# print(step2.select("employee", "employee_upper", "project_id", "project_short").head(4))


# ─────────────────────────────────────────────
# PASO 3 — Transformaciones de fechas
# ─────────────────────────────────────────────

# TODO: añade week_number, month y weekday (0=Lunes)
# step3 = df.with_columns(
#     pl.col("date").dt.week().alias("week_number"),
#     pl.col("date").dt.month().alias("month"),
#     pl.col("date").dt.weekday().alias("weekday"),
# )
# print(step3.select("date", "week_number", "month", "weekday").head(5))


# ─────────────────────────────────────────────
# PASO 4 — Pipeline completo en un with_columns
# ─────────────────────────────────────────────

# TODO: combina todo en un único with_columns() + añade billable_revenue
# full = df.with_columns(
#     # shift_type
#     # employee_upper
#     # project_short
#     # week_number, month, weekday
#     # billable_revenue: hours * 120 si billable, else 0
# )
# print(full)


if __name__ == "__main__":
    print("── Paso 1: clasificación ──")
    # descomenta los pasos
