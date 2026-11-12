"""Tests de la semana 30: el informe de tu dominio está en el repositorio, y al día.

Qué: comprueban la carpeta informe/: que hallazgos.md es exactamente lo que escribe hoy
`hallazgos` con tu instantánea, que la figura está, que tu README.md tiene las secciones
de un informe y que cita la misma huella que tu notebook.
Para qué: un informe copiado a mano envejece en silencio: cambias la instantánea o el
código, y los números del informe ya no salen de ninguna parte. Aquí, si no coinciden,
falla la CI.
Impacto: no necesitan PostgreSQL: leen notebooks/instantanea.csv, como el notebook.
"""

import re
from pathlib import Path

from observatorio.core.findings import FIGURE, REPORT, compare_all, read_snapshot, render

ROOT = Path(__file__).parent.parent
FOLDER = ROOT / "informe"
SNAPSHOT = ROOT / "notebooks" / "instantanea.csv"
NOTEBOOK = ROOT / "notebooks" / "eda.ipynb"
SECTIONS = ["## Pregunta", "## Datos", "## Hallazgos", "## Limitaciones", "## Siguientes pasos"]


def readme() -> str:
    return (FOLDER / "README.md").read_text(encoding="utf-8")


def test_report_is_up_to_date() -> None:
    # Con las opciones por defecto: `uv run observatorio hallazgos notebooks/instantanea.csv
    # informe`. Si falla, vuelve a ejecutarlo y mira con `git diff` qué cambió.
    frame, digest = read_snapshot(SNAPSHOT)
    expected = render(frame, compare_all(frame), name=SNAPSHOT.name, digest=digest)
    assert (FOLDER / REPORT).read_text(encoding="utf-8") == expected


def test_figure_is_the_svg_of_the_report() -> None:
    figure = (FOLDER / FIGURE).read_text(encoding="utf-8")
    assert figure.startswith("<?xml")
    # svg.fonttype none: el título es texto dentro del SVG, no trazos.
    assert "Difieren " in figure


def test_readme_has_the_sections_of_a_report_in_order() -> None:
    headings = [line for line in readme().splitlines() if line.startswith("## ")]
    assert [h for h in headings if h in SECTIONS] == SECTIONS


def test_readme_links_the_report_the_figure_and_the_notebook() -> None:
    text = readme()
    for target in (REPORT, FIGURE, "../notebooks/eda.ipynb"):
        assert f"]({target})" in text, target


def test_readme_cites_the_digest_of_the_notebook() -> None:
    (expected,) = re.findall(r'EXPECTED = \\"([0-9a-f]{64})\\"', NOTEBOOK.read_text("utf-8"))
    assert expected in readme()


def test_readme_has_no_placeholders() -> None:
    # Los huecos de la plantilla del paso 7 son `<tu pregunta>`, `<tu dominio>`...
    text = readme()
    assert "TODO" not in text
    assert not re.search(r"<[A-Za-zÁÉÍÓÚáéíóúñ]", text)
