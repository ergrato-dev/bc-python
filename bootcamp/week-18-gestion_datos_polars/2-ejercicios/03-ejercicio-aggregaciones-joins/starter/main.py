"""
Ejercicio 03 — Agregaciones y Joins
Studio BC: KPIs por proyecto y rentabilidad.
"""

import polars as pl

timesheets = pl.read_csv("data/timesheets.csv", try_parse_dates=True)
projects   = pl.read_csv("data/projects.csv",   try_parse_dates=True)
rates      = pl.read_csv("data/rates.csv")

# ─────────────────────────────────────────────
# PASO 1 — group_by simple
# ─────────────────────────────────────────────

# TODO: group_by("project_id") + agg total_hours, avg_hours, unique_employees
# summary = (
#     timesheets
#     .group_by("project_id")
#     .agg(
#         pl.col("hours").sum().alias("total_hours"),
#         pl.col("hours").mean().round(1).alias("avg_hours"),
#         pl.col("employee").n_unique().alias("unique_employees"),
#     )
#     .sort("total_hours", descending=True)
# )
# print(summary)


# ─────────────────────────────────────────────
# PASO 2 — group_by por múltiples columnas
# ─────────────────────────────────────────────

# TODO: group_by("project_id", "employee")
# .agg(sum de hours, count de registros como "days_worked")
# by_employee = (
#     timesheets
#     .group_by("project_id", "employee")
#     .agg(...)
#     .sort("project_id", "employee")
# )
# print(by_employee)


# ─────────────────────────────────────────────
# PASO 3 — Join y rentabilidad
# ─────────────────────────────────────────────

# TODO: une summary con projects (left join)
# calcula cost_usd = total_hours * 110 (tarifa media)
# calcula margin_usd = budget_usd - cost_usd
# calcula margin_pct = (margin_usd / budget_usd * 100).round(1)
# report = summary.join(projects, on="project_id", how="left").with_columns(...)
# print(report.select("project_id", "client", "budget_usd", "margin_usd", "margin_pct"))


# ─────────────────────────────────────────────
# PASO 4 — Función de ventana
# ─────────────────────────────────────────────

# TODO: añade pct_of_project a cada fila de timesheets
# windowed = timesheets.with_columns(
#     (pl.col("hours") / pl.col("hours").sum().over("project_id") * 100)
#     .round(1)
#     .alias("pct_of_project")
# )
# print(windowed.sort("project_id", "employee"))


if __name__ == "__main__":
    print("── Paso 1: group_by ──")
    # descomenta los pasos
