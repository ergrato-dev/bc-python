"""Los hallazgos de una instantánea: qué etiquetas difieren de verdad, con su informe.

Qué: read_snapshot lee la instantánea de `extraer` y comprueba su huella, compare_all
compara cada par de etiquetas con inference.difference y corrige los p-valores por
comparaciones múltiples, differences_figure dibuja cada diferencia con su intervalo, y
render escribe el informe en Markdown.
Para qué: con cinco etiquetas hay diez pares; si los compruebas uno a uno con α = 0,05, lo
normal es que alguno salga "significativo" por azar. La corrección de Benjamini-Hochberg
controla cuántos de los hallazgos que publicas son falsos, y el informe, generado desde el
código, dice exactamente con qué datos y con qué método se obtuvo cada número.
Impacto: importa pandas, scipy y matplotlib: core/__init__.py no lo reexporta, y la CLI lo
importa solo en `hallazgos`.
"""

import hashlib
import io
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib.figure import Figure
from scipy import stats

from observatorio.core.inference import Comparison, difference

# Los nombres de los dos archivos que escribe `hallazgos`; el informe enlaza la figura.
REPORT = "hallazgos.md"
FIGURE = "diferencias.svg"
COLUMNS = {"etiqueta", "valor"}


@dataclass(frozen=True)
class Finding:
    """Un par de etiquetas comparado; p_adjusted es el p de Welch ya corregido."""

    first: str
    second: str
    comparison: Comparison
    p_adjusted: float


def read_snapshot(path: Path, expected: str | None = None) -> tuple[pd.DataFrame, str]:
    """La instantánea y su huella SHA-256. Lanza ValueError si la huella no es expected o
    si le faltan las columnas `etiqueta` y `valor`."""
    # Una sola lectura: la huella es la de los mismos bytes que se analizan.
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if expected is not None and digest != expected:
        raise ValueError(f"la huella de {path.name} es {digest}, no {expected}")
    # Como el notebook: "NA" es una etiqueta, solo una celda vacía de `valor` falta.
    frame = pd.read_csv(
        io.BytesIO(data),
        keep_default_na=False,
        na_values={"valor": [""]},
        dtype={"etiqueta": "str", "valor": "float64"},
    )
    missing = COLUMNS - set(frame.columns)
    if missing:
        raise ValueError(f"a {path.name} le faltan las columnas {', '.join(sorted(missing))}")
    return frame, digest


def comparable(frame: pd.DataFrame) -> list[str]:
    """Las etiquetas con al menos dos valores distintos, en orden alfabético: las que
    inference.difference puede comparar."""
    distinct = frame.groupby("etiqueta")["valor"].nunique()
    return [str(label) for label in distinct.index[distinct >= 2]]


def compare_all(frame: pd.DataFrame, confidence: float = 0.95) -> list[Finding]:
    """Cada par de etiquetas comparables, en orden alfabético, con su p corregido.

    Lanza ValueError si hay menos de dos etiquetas comparables.
    """
    labels = comparable(frame)
    if len(labels) < 2:
        raise ValueError(f"hacen falta dos etiquetas con valores que varíen (hay {len(labels)})")
    samples = {
        label: frame.loc[frame["etiqueta"] == label, "valor"].dropna().to_numpy(np.float64)
        for label in labels
    }
    pairs = list(combinations(labels, 2))
    comparisons = [difference(samples[a], samples[b], confidence) for a, b in pairs]
    # Benjamini-Hochberg: el p de cada par, corregido por todos los que se comparan a la vez.
    adjusted = stats.false_discovery_control([c.p_welch for c in comparisons], method="bh")
    return [
        Finding(a, b, comparison, float(p))
        for (a, b), comparison, p in zip(pairs, comparisons, adjusted, strict=True)
    ]


def headline(findings: list[Finding], alpha: float) -> str:
    """La conclusión en una frase: el título de la figura y el resumen del informe."""
    real = sum(finding.p_adjusted < alpha for finding in findings)
    return f"Difieren {real} de {len(findings)} pares de etiquetas (BH, α = {alpha:g})"


def differences_figure(findings: list[Finding], unit: str, alpha: float) -> Figure:
    """Un punto por par con su intervalo, y una línea en el cero: un intervalo que la cruza
    es una diferencia que puede no existir."""
    figure = Figure(figsize=(8, 1.5 + 0.4 * len(findings)), layout="constrained")
    axes = figure.add_subplot()
    rows = range(len(findings))
    centers = [finding.comparison.difference for finding in findings]
    below = [finding.comparison.difference - finding.comparison.low for finding in findings]
    above = [finding.comparison.high - finding.comparison.difference for finding in findings]
    axes.errorbar(centers, rows, xerr=[below, above], fmt="o", capsize=4)
    axes.axvline(0, color="grey", linestyle="--")
    axes.set_yticks(rows, [f"{finding.first} - {finding.second}" for finding in findings])
    # El primer par arriba, como en la tabla del informe.
    axes.invert_yaxis()
    axes.set(title=headline(findings, alpha), xlabel=f"diferencia de medias ({unit})")
    return figure


def cell(label: str) -> str:
    """Una etiqueta dentro de una tabla de Markdown: una barra la partiría en dos columnas."""
    return label.replace("|", "\\|")


def render(
    frame: pd.DataFrame,
    findings: list[Finding],
    *,
    name: str,
    digest: str,
    confidence: float = 0.95,
    alpha: float = 0.05,
) -> str:
    """El informe en Markdown. Sin fecha ni rutas: los mismos datos dan los mismos bytes."""
    level = f"{confidence * 100:g} %"
    compared = {label for finding in findings for label in (finding.first, finding.second)}
    left_out = sorted(set(frame["etiqueta"]) - compared)
    lines = [
        "# Hallazgos: diferencias entre etiquetas",
        "",
        (
            f"**Datos**: `{name}`, sha256 `{digest}`: {len(frame)} medidas,"
            f" {int(frame['valor'].notna().sum())} con valor."
        ),
        "",
        (
            f"**Método**: para cada par de etiquetas ({len(findings)} pares), la diferencia de"
            f" medias con su intervalo del {level} (Welch) y el tamaño del efecto (d de Cohen)."
            " Los p-valores de Welch se corrigen con Benjamini-Hochberg; un par difiere si su p"
            f" corregido es menor que {alpha:g}. Mann-Whitney, que no supone una campana, sirve de"
            " contraste."
        ),
        "",
        "## Resumen",
        "",
        f"{headline(findings, alpha)}.",
        "",
        f"![Diferencia de medias de cada par, con su intervalo del {level}]({FIGURE})",
        "",
        "## Pares",
        "",
        (
            f"| Par | Medidas | Diferencia | IC {level} | d | p Welch | p corregido"
            " | p Mann-Whitney | ¿Difiere? |"
        ),
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for finding in findings:
        result = finding.comparison
        lines.append(
            f"| {cell(finding.first)} - {cell(finding.second)}"
            f" | {result.sizes[0]} / {result.sizes[1]} | {result.difference:.2f}"
            f" | [{result.low:.2f}, {result.high:.2f}] | {result.effect:.2f}"
            f" | {result.p_welch:.3g} | {finding.p_adjusted:.3g} | {result.p_ranks:.3g}"
            f" | {'sí' if finding.p_adjusted < alpha else 'no'} |"
        )
    if left_out:
        lines += [
            "",
            (
                "Sin comparar, por tener menos de dos valores distintos:"
                f" {', '.join(cell(label) for label in left_out)}."
            ),
        ]
    return "\n".join(lines) + "\n"
