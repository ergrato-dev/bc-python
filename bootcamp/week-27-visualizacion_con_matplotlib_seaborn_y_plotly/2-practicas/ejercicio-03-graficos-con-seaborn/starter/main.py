"""Ejercicio 03 · seaborn: datos largos, color por grupo, estadística y paneles.

Ejecuta `uv run python main.py` después de cada paso y compara con el README. Los gráficos
van a la carpeta salida/.
"""

import shutil
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure

print("Ejercicio 03 · seaborn")

OUT = Path(__file__).parent / "salida"
shutil.rmtree(OUT, ignore_errors=True)
OUT.mkdir()

# Treinta días de medidas, una por hora, de cinco estaciones: sube de día y baja de noche,
# cada estación a su nivel, con ruido y un 5 % sin valor. La semilla las repite siempre.
rng = np.random.default_rng(27)
TIMES = pd.date_range("2026-11-01", periods=30 * 24, freq="h")
LEVELS = {"Norte": 18.0, "Sur": 24.0, "Este": 21.0, "Oeste": 15.0, "Centro": 20.0}
readings = pd.concat(
    pd.DataFrame(
        {
            "time": TIMES,
            "station": station,
            "value": (
                level
                + 6 * np.sin((TIMES.hour.to_numpy() - 9) / 24 * 2 * np.pi)
                + rng.normal(0, 1.5, len(TIMES))
            ).round(1),
        }
    )
    for station, level in LEVELS.items()
).reset_index(drop=True)
readings.loc[rng.random(len(readings)) < 0.05, "value"] = np.nan
norte = readings[readings["station"] == "Norte"].set_index("time")["value"]

readings["hour"] = readings["time"].dt.hour


# ============================================
# PASO 1: Datos anchos y datos largos
# ============================================
# Descomenta las siguientes líneas:
# wide = readings.pivot(index="time", columns="station", values="value")
# print("ancha:", wide.shape, list(wide.columns))
# long = wide.reset_index().melt(id_vars="time", var_name="station", value_name="value")
# print("larga:", long.shape, list(long.columns))
# print(long.head(3))
# print("¿las mismas medidas?", long["value"].count() == readings["value"].count())


# ============================================
# PASO 2: Una línea por grupo, con su incertidumbre
# ============================================
# Descomenta las siguientes líneas:
# figure = Figure(figsize=(9, 4.5), layout="constrained")
# axes = figure.add_subplot()
# returned = sns.lineplot(
#     data=readings, x="hour", y="value", hue="station", errorbar=("ci", 95), seed=27, ax=axes
# )
# print("¿devuelve los mismos ejes?", returned is axes)
# lines = axes.get_lines()
# print("líneas:", len(lines), "· con datos:", sum(len(line.get_xdata()) > 0 for line in lines))
# print("nombres:", [line.get_label() for line in lines])
# print("bandas:", len(axes.collections))
# norte = axes.get_lines()[0]
# by_hour = readings[readings["station"] == "Norte"].groupby("hour")["value"].mean()
# print("Norte a las 15, en el gráfico:", round(float(norte.get_ydata()[15]), 2))
# print("Norte a las 15, con pandas:   ", round(float(by_hour[15]), 2))
# print("leyenda:", [text.get_text() for text in axes.get_legend().get_texts()])
# figure.savefig(OUT / "02-por-hora.png")


# ============================================
# PASO 3: Distribuciones por grupo
# ============================================
# Descomenta las siguientes líneas:
# figure = Figure(figsize=(11, 4), layout="constrained")
# left, right = figure.subplots(1, 2)
# sns.histplot(data=readings, x="value", hue="station", element="step", stat="density", ax=left)
# sns.violinplot(data=readings, x="station", y="value", inner="quart", ax=right)
# print("pasos del histograma:", len(left.collections))
# print("violines:", len(right.collections))
# print("NaN que seaborn dejó fuera:", readings["value"].isna().sum())
# figure.savefig(OUT / "03-distribuciones.png")


# ============================================
# PASO 4: Paneles con una sola llamada
# ============================================
# Descomenta las siguientes líneas:
# grid = sns.relplot(
#     data=readings[readings["time"] < "2026-11-04"],
#     x="time",
#     y="value",
#     col="station",
#     col_wrap=3,
#     kind="line",
#     height=2.5,
#     aspect=1.4,
# )
# print(type(grid).__name__, "·", type(grid.figure).__name__, "· paneles:", len(grid.axes))
# print("títulos:", [axes.get_title() for axes in grid.axes])
# grid.figure.autofmt_xdate()
# grid.savefig(OUT / "04-paneles.png")
# import matplotlib.pyplot as plt  # noqa: E402
#
# print("figuras abiertas en pyplot:", plt.get_fignums())
# plt.close(grid.figure)
# print("después de close:", plt.get_fignums())


# ============================================
# PASO 5: Temas y paletas
# ============================================
# Descomenta las siguientes líneas:
# print("fondo antes:", matplotlib.rcParams["axes.facecolor"])
# with sns.axes_style("darkgrid"):
#     print("fondo dentro del with:", matplotlib.rcParams["axes.facecolor"])
#     figure = Figure(figsize=(9, 4.5), layout="constrained")
#     axes = figure.add_subplot()
#     sns.barplot(data=readings, x="station", y="value", hue="station", palette="colorblind", ax=axes)
# print("fondo después:", matplotlib.rcParams["axes.facecolor"])
# figure.savefig(OUT / "05-tema.png")
# print("colorblind:", sns.color_palette("colorblind", 5).as_hex())
# sns.set_theme()
# print("fondo tras set_theme:", matplotlib.rcParams["axes.facecolor"])
