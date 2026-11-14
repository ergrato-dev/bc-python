"""Los gráficos del Observatorio, con matplotlib y sin pyplot.

Qué: evolution_figure dibuja la tabla de summaries.evolution, una línea por etiqueta, y
save guarda una figura en el formato que diga la extensión del archivo.
Para qué: un gráfico deja ver de un vistazo lo que en la tabla de `evolucion` hay que leer
número a número: qué etiqueta sube, cuál baja y dónde faltan datos.
Impacto: usa Figure y no pyplot: sin estado global ni ventanas, funciona igual en tu
terminal, en un test y en Docker. No se reexporta en core: importar matplotlib cuesta.
"""

from pathlib import Path

import matplotlib
import pandas as pd
from matplotlib.figure import Figure


def evolution_figure(table: pd.DataFrame, title: str) -> Figure:
    """Una línea por columna de table, con un punto por periodo; un NaN corta la línea."""
    figure = Figure(figsize=(8, 4.5), layout="constrained")
    axes = figure.add_subplot()
    # El marcador hace visible un periodo con valor entre dos sin él: una línea de un solo
    # punto no se ve.
    lines = [axes.plot(table.index, table[label], marker="o")[0] for label in table.columns]
    axes.set(title=title, xlabel="periodo", ylabel="media")
    # Los nombres van explícitos: si no, legend se salta las etiquetas que empiezan por "_".
    axes.legend(lines, list(table.columns), title="etiqueta")
    return figure


def save(figure: Figure, path: Path) -> None:
    """Guarda la figura en el formato de la extensión de path: .png, .svg, .pdf...

    Sin fecha y con una sal fija para los identificadores del SVG: los mismos datos dan el
    mismo PNG y el mismo SVG, byte a byte. En el SVG, el texto sigue siendo texto.
    """
    with matplotlib.rc_context({"svg.hashsalt": "observatorio", "svg.fonttype": "none"}):
        figure.savefig(path, metadata={"Date": None})
