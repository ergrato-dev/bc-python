"""Ejercicio 04 · plotly, y el mismo gráfico con tres bibliotecas.

Ejecuta `uv run python main.py` después de cada paso y compara con el README. Los gráficos
van a la carpeta salida/: abre los .html con tu navegador.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px

print("Ejercicio 04 · plotly")

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


# La media de cada estación cada día, en formato largo: lo que piden plotly y seaborn.
daily = (
    readings.set_index("time")
    .groupby("station", sort=False)["value"]
    .resample("D")
    .mean()
    .round(2)
    .reset_index()
)


# ============================================
# PASO 1: Un gráfico que responde al ratón
# ============================================
# Descomenta las siguientes líneas:
# print(daily.head(3))
# figure = px.line(daily, x="time", y="value", color="station", title="Media diaria por estación")
# print(type(figure).__name__, "· trazas:", len(figure.data))
# print("nombres:", [trace.name for trace in figure.data])
# print("Norte, primeros días:", figure.data[0].y[:3].tolist())
# print("al pasar el ratón:", figure.data[0].hovertemplate)
# figure.write_html(OUT / "01-linea.html")
# print(size(OUT / "01-linea.html"))


# ============================================
# PASO 2: Una figura es un diccionario
# ============================================
# Descomenta las siguientes líneas:
# spec = figure.to_dict()
# print("claves:", list(spec))
# print("tipo de traza:", spec["data"][0]["type"], "· modo:", spec["data"][0]["mode"])
# figure.update_layout(xaxis_title="día", yaxis_title="temperatura (°C)", legend_title="estación")
# figure.add_hline(y=25, line_dash="dash", annotation_text="umbral 25")
# print("eje y:", figure.layout.yaxis.title.text, "· formas:", len(figure.layout.shapes))
# text = figure.to_json()
# print("JSON:", len(text), "caracteres ·", json.loads(text)["data"][0]["y"]["dtype"])


# ============================================
# PASO 3: Lo que pesa un HTML
# ============================================
# Descomenta las siguientes líneas:
# figure.write_html(OUT / "03-completo.html", include_plotlyjs=True)
# figure.write_html(OUT / "03-cdn.html", include_plotlyjs="cdn")
# print(size(OUT / "03-completo.html"))
# print(size(OUT / "03-cdn.html"))
# cdn = (OUT / "03-cdn.html").read_text()
# print("de dónde baja plotly.js:", cdn[cdn.index("https://cdn") :].split('"')[0])
# try:
#     figure.write_image(OUT / "03-imagen.png")
# except RuntimeError as problem:
#     print("write_image:", str(problem).strip().splitlines()[0])


# ============================================
# PASO 4: Paneles y puntos con detalle
# ============================================
# Descomenta las siguientes líneas:
# week = readings[readings["time"] < "2026-11-08"].dropna()
# scatter = px.scatter(
#     week,
#     x="time",
#     y="value",
#     facet_col="station",
#     facet_col_wrap=3,
#     hover_data={"value": ":.1f", "time": "|%d %b %H:%M"},
#     opacity=0.5,
# )
# print("trazas:", len(scatter.data), "· puntos:", sum(len(trace.x) for trace in scatter.data))
# print("paneles:", [a.text for a in scatter.layout.annotations])
# scatter.for_each_annotation(lambda a: a.update(text=a.text.removeprefix("station=")))
# print("paneles:", [a.text for a in scatter.layout.annotations])
# scatter.write_html(OUT / "04-paneles.html", include_plotlyjs="cdn")
# print(size(OUT / "04-paneles.html"))


# ============================================
# PASO 5: Un gráfico, tres bibliotecas
# ============================================
# Descomenta las siguientes líneas:
# import seaborn as sns  # noqa: E402
# from matplotlib.figure import Figure  # noqa: E402
#
# wide = daily.pivot(index="time", columns="station", values="value")
# mpl = Figure(figsize=(9, 4.5), layout="constrained")
# axes = mpl.add_subplot()
# for station in LEVELS:
#     axes.plot(wide.index, wide[station], label=station)
# axes.set(title="Media diaria por estación", xlabel="día", ylabel="temperatura (°C)")
# axes.legend()
# mpl.savefig(OUT / "05-matplotlib.png")
#
# sea = Figure(figsize=(9, 4.5), layout="constrained")
# axes = sea.add_subplot()
# sns.lineplot(data=daily, x="time", y="value", hue="station", ax=axes)
# axes.set(title="Media diaria por estación", xlabel="día", ylabel="temperatura (°C)")
# sea.savefig(OUT / "05-seaborn.png")
#
# figure.write_html(OUT / "05-plotly.html", include_plotlyjs="cdn")
# for name in ["05-matplotlib.png", "05-seaborn.png", "05-plotly.html"]:
#     print(size(OUT / name))
# for module in ["matplotlib.figure", "seaborn", "plotly.express"]:
#     code = f"import time; s = time.perf_counter(); import {module}; print(time.perf_counter() - s)"
#     seconds = float(
#         subprocess.run([sys.executable, "-c", code], capture_output=True, text=True).stdout
#     )
#     print(f"importar {module}: {seconds:.2f} s")
