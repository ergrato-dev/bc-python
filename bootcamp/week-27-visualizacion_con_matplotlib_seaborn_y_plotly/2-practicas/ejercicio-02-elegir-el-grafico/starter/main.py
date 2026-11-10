"""Ejercicio 02 · Elegir el gráfico y contarlo bien: ejes, paneles, color y escalas.

Ejecuta `uv run python main.py` después de cada paso y compara con el README. Los gráficos
van a la carpeta salida/: ábrelos y compara cada pareja.
"""

import shutil
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib.figure import Figure

print("Ejercicio 02 · Elegir el gráfico")

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


def size(path: Path) -> str:
    """El nombre y el tamaño de un archivo de salida/, en kB."""
    return f"{path.name}: {path.stat().st_size / 1000:.1f} kB"


# Los tres primeros días, una columna por estación.
days = readings.pivot(index="time", columns="station", values="value")[list(LEVELS)].iloc[:72]
by_station = readings.groupby("station", sort=False)["value"].mean()


# ============================================
# PASO 1: Las barras empiezan en cero
# ============================================
# Descomenta las siguientes líneas:
# figure = Figure(figsize=(10, 4), layout="constrained")
# honest, cut = figure.subplots(1, 2)
# for axes in (honest, cut):
#     axes.bar(by_station.index, by_station.to_numpy())
# honest.set_title("Desde cero")
# cut.set_title("Desde 14")
# cut.set_ylim(14, 25)
# print(by_station.round(1).to_dict())
# print("Sur / Oeste, de verdad:", round(by_station["Sur"] / by_station["Oeste"], 1))
# low = cut.get_ylim()[0]
# print(
#     "Sur / Oeste, como se ve desde 14:",
#     round((by_station["Sur"] - low) / (by_station["Oeste"] - low), 1),
# )
# figure.savefig(OUT / "01-barras.png")


# ============================================
# PASO 2: Un panel por estación
# ============================================
# Descomenta las siguientes líneas:
# print(days.head(3))
# spaghetti = Figure(figsize=(8, 4), layout="constrained")
# axes = spaghetti.add_subplot()
# for station in days.columns:
#     axes.plot(days.index, days[station], label=station)
# axes.legend(ncols=5, loc="upper center")
# spaghetti.savefig(OUT / "02-todas-juntas.png")
# panels = Figure(figsize=(10, 6), layout="constrained")
# grid = panels.subplots(len(days.columns), 1, sharex=True, sharey=True)
# for axes, station in zip(grid, days.columns, strict=True):
#     axes.plot(days.index, days[station], color="0.3")
#     axes.set_ylabel(station, rotation=0, ha="right")
# print(
#     "paneles:", len(panels.axes), "· mismos límites:", len({axes.get_ylim() for axes in grid}) == 1
# )
# panels.savefig(OUT / "02-un-panel-por-estacion.png")


# ============================================
# PASO 3: Color para una cantidad
# ============================================
# Descomenta las siguientes líneas:
# hours = norte.groupby([norte.index.date, norte.index.hour]).mean().unstack()
# print("días x horas:", hours.shape, "· huecos:", int(hours.isna().sum().sum()))
# figure = Figure(figsize=(9, 5), layout="constrained")
# axes = figure.add_subplot()
# # extent pone el día 1 arriba y el 30 abajo, y cada hora centrada en su casilla.
# image = axes.imshow(hours.to_numpy(), aspect="auto", cmap="viridis", extent=(-0.5, 23.5, 30.5, 0.5))
# figure.colorbar(image, label="temperatura (°C)")
# axes.set(title="Norte: cada día, cada hora", xlabel="hora", ylabel="día de noviembre")
# print("mapa de color:", image.get_cmap().name, "· de", image.norm.vmin, "a", image.norm.vmax)
# figure.savefig(OUT / "03-mapa-de-calor.png")


# ============================================
# PASO 4: Cómo se reparten
# ============================================
# Descomenta las siguientes líneas:
# groups = [readings.loc[readings["station"] == station, "value"].dropna() for station in LEVELS]
# figure = Figure(figsize=(9, 4), layout="constrained")
# axes = figure.add_subplot()
# boxes = axes.boxplot(groups, tick_labels=list(LEVELS))
# axes.set(title="Valores por estación", ylabel="temperatura (°C)")
# medians = [round(float(line.get_ydata()[0]), 1) for line in boxes["medians"]]
# print("medianas en el gráfico:", medians)
# print("medianas de pandas:   ", [round(float(group.median()), 1) for group in groups])
# figure.savefig(OUT / "04-cajas.png")


# ============================================
# PASO 5: Cuando los datos crecen multiplicando
# ============================================
# Descomenta las siguientes líneas:
# rain = pd.Series(rng.lognormal(0, 1.2, 2000)).round(2)
# print("lluvia: mediana", rain.median(), "· máximo", rain.max())
# figure = Figure(figsize=(10, 4), layout="constrained")
# linear, logarithmic = figure.subplots(1, 2)
# linear.hist(rain, bins=40)
# linear.set_title("Escala lineal")
# logarithmic.hist(rain, bins=np.geomspace(rain[rain > 0].min(), rain.max(), 40))
# logarithmic.set_xscale("log")
# logarithmic.set_title("Escala logarítmica")
# print("escalas:", linear.get_xscale(), logarithmic.get_xscale())
# figure.savefig(OUT / "05-escalas.png")
