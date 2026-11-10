"""Ejercicio 01 · matplotlib: figuras, ejes y artistas, sin pyplot y con pyplot.

Ejecuta `uv run python main.py` después de cada paso y compara con el README. Los gráficos
van a la carpeta salida/, junto a este archivo: ábrelos para ver lo que dibujaste.
"""

import shutil
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from matplotlib.dates import ConciseDateFormatter, DayLocator
from matplotlib.figure import Figure

print("Ejercicio 01 · matplotlib")

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


# ============================================
# PASO 1: Una figura, unos ejes, una línea
# ============================================
# Descomenta las siguientes líneas:
# print(readings.head(3))
# print("medidas:", len(readings), "· sin valor:", readings["value"].isna().sum())
# figure = Figure(figsize=(8, 4))
# axes = figure.add_subplot()
# (line,) = axes.plot(norte.index[:72], norte.iloc[:72])
# print(figure)
# print(axes)
# print(line)
# print("x:", line.get_xdata()[:2])
# print("y:", line.get_ydata()[:4])
# print("hijos de los ejes:", len(axes.get_children()))
# figure.savefig(OUT / "01-una-linea.png")
# print(size(OUT / "01-una-linea.png"))


# ============================================
# PASO 2: pyplot recuerda cada figura
# ============================================
# Descomenta las siguientes líneas:
# matplotlib.use("Agg")  # sin ventanas: este programa solo guarda archivos
# import matplotlib.pyplot as plt  # noqa: E402
#
# for days in [1, 2, 3]:
#     plt.figure()
#     plt.plot(norte.iloc[: days * 24])
# print("figuras abiertas en pyplot:", plt.get_fignums())
# plt.title("la última figura")
# print("el título fue a:", plt.gca().get_title(), "· figura", plt.gcf().number)
# plt.savefig(OUT / "02-pyplot.png")
# plt.close("all")
# print("después de close:", plt.get_fignums())
# print("¿y la del paso 1?", figure.number if hasattr(figure, "number") else "no es de pyplot")


# ============================================
# PASO 3: Cuatro gráficos, cuatro preguntas
# ============================================
# Descomenta las siguientes líneas:
# grid = Figure(figsize=(10, 7), layout="constrained")
# (evolution, spread), (means, dots) = grid.subplots(2, 2)
# evolution.plot(norte.index[:72], norte.iloc[:72])
# evolution.set_title("¿Cómo cambia? Norte, tres días")
# spread.hist(readings["value"].dropna(), bins=30)
# spread.set_title("¿Cómo se reparten? Todas las medidas")
# by_station = readings.groupby("station", sort=False)["value"].mean()
# means.bar(by_station.index, by_station.to_numpy())
# means.set_title("¿Cuál es mayor? Media por estación")
# hours = readings["time"].dt.hour
# dots.scatter(hours, readings["value"], s=4, alpha=0.3)
# dots.set_title("¿Qué relación hay? Valor y hora del día")
# print([axes.get_title() for axes in grid.axes])
# print("barras:", len(means.patches), "· puntos:", len(dots.collections[0].get_offsets()))
# print("medidas en el histograma:", int(sum(bar.get_height() for bar in spread.patches)))
# grid.savefig(OUT / "03-cuatro-preguntas.png")
# print(size(OUT / "03-cuatro-preguntas.png"))


# ============================================
# PASO 4: Que se entienda sin explicarlo
# ============================================
# Descomenta las siguientes líneas:
# week = norte.loc["2026-11-01":"2026-11-07"]
# figure = Figure(figsize=(9, 4), layout="constrained")
# axes = figure.add_subplot()
# axes.plot(week.index, week.to_numpy(), marker=".", label="Norte")
# axes.axhline(25, color="tab:red", linestyle="--", label="umbral 25")
# peak = week.idxmax()
# axes.annotate(
#     f"máximo: {week.max()}", xy=(peak, week.max()), xytext=(10, -25), textcoords="offset points"
# )
# axes.set(title="Norte, primera semana de noviembre", xlabel="día", ylabel="temperatura (°C)")
# axes.xaxis.set_major_locator(DayLocator())
# axes.xaxis.set_major_formatter(ConciseDateFormatter(axes.xaxis.get_major_locator()))
# figure.legend(loc="outside right upper")  # fuera de los ejes: no tapa ningún dato
# print("máximo:", peak, week.max())
# print("límites y:", [round(float(limit), 1) for limit in axes.get_ylim()])
# print("leyenda:", [text.get_text() for text in figure.legends[0].get_texts()])
# figure.savefig(OUT / "04-con-sentido.png")
# print(size(OUT / "04-con-sentido.png"))


# ============================================
# PASO 5: PNG, SVG y PDF
# ============================================
# Descomenta las siguientes líneas:
# for name, options in [
#     ("05-dpi-100.png", {"dpi": 100}),
#     ("05-dpi-200.png", {"dpi": 200}),
#     ("05-figura.svg", {}),
#     ("05-figura.pdf", {}),
# ]:
#     figure.savefig(OUT / name, **options)
#     print(size(OUT / name))
# pixels = matplotlib.image.imread(OUT / "05-dpi-200.png")
# print("píxeles a 200 dpi:", pixels.shape[1], "x", pixels.shape[0])
# svg = (OUT / "05-figura.svg").read_text()
# print("elementos <text> en el SVG:", svg.count("<text"))
# with matplotlib.rc_context({"svg.fonttype": "none"}):
#     figure.savefig(OUT / "05-texto.svg")
# print(size(OUT / "05-texto.svg"))
# print("¿y ahora?", (OUT / "05-texto.svg").read_text().count("<text"))
