"""Ejercicio 03 · Dar forma: de tabla larga a ancha y vuelta, con pivot, melt y crosstab.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import pandas as pd

print("Ejercicio 03 · Dar forma")

# Formato largo: una fila por medida, con su día, su estación y su valor.
long = pd.DataFrame(
    {
        "day": ["lun", "lun", "lun", "mar", "mar", "mié"],
        "station": ["Norte", "Sur", "Este", "Norte", "Sur", "Norte"],
        "value": [12.5, 8.0, 61.0, 48.9, 9.5, 20.0],
    }
)


# ============================================
# PASO 1: pivot, de largo a ancho
# ============================================
# Descomenta las siguientes líneas:
# wide = long.pivot(index="day", columns="station", values="value")
# print(wide)
# print("forma: larga", long.shape, "· ancha", wide.shape)
# print("media de cada estación:", wide.mean().round(2).to_dict())
# print("media de cada día:", wide.mean(axis="columns").round(2).to_dict())


# ============================================
# PASO 2: Dos valores en la misma celda
# ============================================
# Descomenta las siguientes líneas:
# repeated = pd.concat([long, pd.DataFrame({"day": ["lun"], "station": ["Norte"], "value": [14.5]})])
# try:
#     repeated.pivot(index="day", columns="station", values="value")
# except ValueError as problem:
#     print("ValueError:", problem)
# table = repeated.pivot_table(index="day", columns="station", values="value", aggfunc="mean")
# print(table.loc["lun"].to_dict())
# counts = repeated.pivot_table(index="day", columns="station", values="value", aggfunc="count", fill_value=0)
# print(counts)


# ============================================
# PASO 3: melt, de ancho a largo
# ============================================
# Descomenta las siguientes líneas:
# back = wide.reset_index().melt(id_vars="day", var_name="station", value_name="value")
# print(back.head(4))
# print("filas:", len(back), "· con valor:", back["value"].notna().sum())
# again = back.dropna().sort_values(["day", "station"]).reset_index(drop=True)
# print("¿vuelta completa?", again.equals(long.sort_values(["day", "station"]).reset_index(drop=True)))


# ============================================
# PASO 4: stack y unstack
# ============================================
# Descomenta las siguientes líneas:
# stacked = wide.stack()
# print(stacked.head(4))
# print("índice:", stacked.index.names, "· filas:", len(stacked), "· con valor:", len(stacked.dropna()))
# print(stacked.unstack("day"))


# ============================================
# PASO 5: Tablas de conteo con crosstab
# ============================================
# Descomenta las siguientes líneas:
# long["level"] = pd.cut(long["value"], bins=[0, 10, 50, 100], labels=["bajo", "medio", "alto"], right=False)
# print(pd.crosstab(long["station"], long["level"]))
# print(pd.crosstab(long["station"], long["level"], margins=True, margins_name="total").loc["total"].to_dict())
# print(pd.crosstab(long["station"], long["level"], normalize="index").round(2).loc["Norte"].to_dict())


# ============================================
# PASO 6: Ancho para leer, largo para calcular
# ============================================
# Descomenta las siguientes líneas:
# print("largo, groupby:", long.groupby("station")["value"].max().to_dict())
# print("ancho, max:    ", wide.max().to_dict())
# growth = wide.loc["mar"] - wide.loc["lun"]
# print("de lunes a martes:", growth.round(1).to_dict())
# print(wide.to_string(na_rep="—", float_format=lambda value: f"{value:.1f}"))
