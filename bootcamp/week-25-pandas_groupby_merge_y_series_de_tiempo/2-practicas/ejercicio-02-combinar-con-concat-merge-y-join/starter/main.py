"""Ejercicio 02 · Combinar tablas: apilar con concat y cruzar con merge y join.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import pandas as pd

print("Ejercicio 02 · Combinar tablas")

# Las medidas de dos días, cada una en su tabla, y una tabla de estaciones con su región
# y su altitud. Oeste tiene medidas pero no está en la tabla; Centro está pero no midió.
monday = pd.DataFrame({"station": ["Norte", "Sur", "Oeste"], "value": [12.5, 8.0, 3.1]})
tuesday = pd.DataFrame({"station": ["Norte", "Sur"], "value": [48.9, 9.5]})
stations = pd.DataFrame(
    {
        "station": ["Norte", "Sur", "Centro"],
        "region": ["montaña", "costa", "valle"],
        "altitude": [2600, 5, 1500],
    }
)


# ============================================
# PASO 1: Apilar con concat
# ============================================
# Descomenta las siguientes líneas:
# both = pd.concat([monday, tuesday])
# print(both)
# print("índice repetido:", both.index.tolist())
# both = pd.concat([monday, tuesday], ignore_index=True)
# print("ignore_index:", both.index.tolist())
# by_day = pd.concat({"lunes": monday, "martes": tuesday}, names=["day", "row"])
# print(by_day.loc["martes"])


# ============================================
# PASO 2: Columnas que no coinciden
# ============================================
# Descomenta las siguientes líneas:
# with_unit = tuesday.assign(unit="mm")
# print(pd.concat([monday, with_unit], ignore_index=True))
# side = pd.concat([monday["value"], tuesday["value"]], axis=1, keys=["lunes", "martes"])
# print(side)


# ============================================
# PASO 3: merge y sus cuatro how
# ============================================
# Descomenta las siguientes líneas:
# for how in ["inner", "left", "right", "outer"]:
#     joined = monday.merge(stations, on="station", how=how)
#     print(f"{how:>5}:", joined["station"].tolist(), "· región:", joined["region"].tolist())
# print(monday.merge(stations, on="station", how="outer", indicator=True)[["station", "_merge"]])


# ============================================
# PASO 4: Una clave repetida
# ============================================
# Descomenta las siguientes líneas:
# both = pd.concat([monday, tuesday], ignore_index=True)
# print("left con medidas a la izquierda:", len(both.merge(stations, on="station", how="left")), "filas")
# dirty = pd.concat([stations, stations.iloc[[0]]], ignore_index=True)
# print("con Norte dos veces en estaciones:", len(both.merge(dirty, on="station", how="left")), "filas")
# try:
#     both.merge(dirty, on="station", how="left", validate="many_to_one")
# except pd.errors.MergeError as problem:
#     print("MergeError:", str(problem).splitlines()[0])


# ============================================
# PASO 5: Columnas con el mismo nombre
# ============================================
# Descomenta las siguientes líneas:
# compared = monday.merge(tuesday, on="station", suffixes=("_lunes", "_martes"))
# print(compared)
# print("cambio:", (compared["value_martes"] - compared["value_lunes"]).round(1).tolist())
# renamed = stations.rename(columns={"station": "name"})
# print(monday.merge(renamed, left_on="station", right_on="name").columns.tolist())


# ============================================
# PASO 6: join por el índice
# ============================================
# Descomenta las siguientes líneas:
# indexed = stations.set_index("station")
# means = both.groupby("station")["value"].mean()
# print(indexed.join(means.rename("mean"), how="left"))
# print("map:", monday["station"].map(indexed["region"]).tolist())
