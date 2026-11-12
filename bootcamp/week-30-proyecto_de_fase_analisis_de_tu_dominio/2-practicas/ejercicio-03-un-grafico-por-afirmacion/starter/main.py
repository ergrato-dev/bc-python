"""Ejercicio 03 · Un gráfico por afirmación: el título dice la conclusión, el gráfico la prueba.

Ejecuta `uv run python main.py` después de cada paso, compara con el README y abre los SVG
de salida/ en tu navegador o en VS Code.
"""

import hashlib
from pathlib import Path

import matplotlib
import numpy as np
from matplotlib.figure import Figure
from scipy import stats

print("Ejercicio 03 · Un gráfico por afirmación")

# salida/ no va a Git: el ejercicio escribe ahí sus gráficos en cada ejecución.
OUT = Path("salida")
OUT.mkdir(exist_ok=True)

# Cinco zonas, 40 medidas cada una. Centro es la referencia.
rng = np.random.default_rng(30)
LEVELS = {"Centro": 20.0, "Norte": 21.0, "Sur": 26.0, "Este": 19.5, "Oeste": 24.0}
samples = {zone: rng.normal(level, 6, 40) for zone, level in LEVELS.items()}
others = [zone for zone in LEVELS if zone != "Centro"]
print({zone: round(float(values.mean()), 2) for zone, values in samples.items()})


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


# ============================================
# PASO 1: Barras de medias
# ============================================
# Descomenta las siguientes líneas:
# figure = Figure(figsize=(6, 4), layout="constrained")
# axes = figure.add_subplot()
# axes.bar(list(samples), [values.mean() for values in samples.values()])
# axes.set(title="Media por zona", ylabel="valor medio")
# figure.savefig(OUT / "1-barras.svg")
# print("salida/1-barras.svg: ¿qué zonas difieren de Centro?")


# ============================================
# PASO 2: Cada diferencia, con su intervalo
# ============================================
# Descomenta las siguientes líneas:
# results = {}
# for zone in others:
#     welch = stats.ttest_ind(samples[zone], samples["Centro"], equal_var=False)
#     interval = welch.confidence_interval(0.95)
#     results[zone] = (samples[zone].mean() - samples["Centro"].mean(), interval.low, interval.high)
#     print(f"{zone} - Centro: {results[zone][0]:.2f} [{interval.low:.2f}, {interval.high:.2f}]")
# rows = range(len(others))
# centers = [results[zone][0] for zone in others]
# below = [results[zone][0] - results[zone][1] for zone in others]
# above = [results[zone][2] - results[zone][0] for zone in others]
# figure = Figure(figsize=(6, 3), layout="constrained")
# axes = figure.add_subplot()
# axes.errorbar(centers, rows, xerr=[below, above], fmt="o", capsize=4)
# axes.axvline(0, color="grey", linestyle="--")
# axes.set_yticks(rows, [f"{zone} - Centro" for zone in others])
# axes.invert_yaxis()
# axes.set(title="Diferencia con Centro", xlabel="diferencia de medias")
# figure.savefig(OUT / "2-diferencias.svg")
# print("salida/2-diferencias.svg")


# ============================================
# PASO 3: El título es la conclusión
# ============================================
# Descomenta las siguientes líneas:
# differ = [zone for zone in others if results[zone][1] > 0 or results[zone][2] < 0]
# title = f"{len(differ)} de {len(others)} zonas difieren de Centro: {', '.join(differ)}"
# axes.set_title(title)
# figure.savefig(OUT / "3-conclusion.svg")
# print(f"salida/3-conclusion.svg: {title}")


# ============================================
# PASO 4: El mismo gráfico, dos veces
# ============================================
# Descomenta las siguientes líneas:
# figure.savefig(OUT / "4a.svg")
# figure.savefig(OUT / "4b.svg")
# print(f"por defecto:  {digest(OUT / '4a.svg')} {digest(OUT / '4b.svg')}")
# with matplotlib.rc_context({"svg.hashsalt": "semana-30"}):
#     figure.savefig(OUT / "4a.svg", metadata={"Date": None})
#     figure.savefig(OUT / "4b.svg", metadata={"Date": None})
# print(f"sin fecha y con sal: {digest(OUT / '4a.svg')} {digest(OUT / '4b.svg')}")


# ============================================
# PASO 5: Texto que se puede buscar
# ============================================
# Descomenta las siguientes líneas:
# with matplotlib.rc_context({"svg.hashsalt": "semana-30", "svg.fonttype": "none"}):
#     figure.savefig(OUT / "5-texto.svg", metadata={"Date": None})
# for name in ("4a.svg", "5-texto.svg"):
#     text = (OUT / name).read_text(encoding="utf-8")
    # Con "path", cada letra es un trazo; el título solo aparece en un comentario <!-- -->.
#     as_text = f">{title}</text>" in text
#     print(f"{name}: {len(text) // 1024} KB, título como <text>: {as_text}")
