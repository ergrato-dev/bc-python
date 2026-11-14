"""Tests de la semana 30: de la instantánea a los hallazgos, y de los hallazgos al informe.

Qué: comprueban core/findings.py (leer la instantánea con su huella, comparar cada par de
etiquetas, corregir los p-valores, la figura y el informe) y el comando `hallazgos`.
Para qué: un informe es lo que lee quien decide. Si se cuela un par sin corregir, una
etiqueta que rompe la tabla o un número que no sale de los datos que dice, la conclusión
es falsa y nadie lo nota: el informe parece igual de serio.
Impacto: findings.py no se reexporta en core: la CLI arranca sin cargar pandas ni scipy.
"""

import hashlib
import math
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from scipy import stats
from typer.testing import CliRunner

from observatorio import cli
from observatorio.core.findings import (
    FIGURE,
    REPORT,
    Finding,
    comparable,
    compare_all,
    differences_figure,
    headline,
    read_snapshot,
    render,
)
from observatorio.core.inference import Comparison, difference

runner = CliRunner()

NAN = math.nan
# Tres etiquetas que se pueden comparar y dos que no: Este con un solo valor, Oeste sin
# ninguno. Sur mide claramente más que Norte y que Centro.
ROWS = [
    ("Norte", 10.0),
    ("Norte", 12.0),
    ("Norte", 11.0),
    ("Norte", NAN),
    ("Sur", 30.0),
    ("Sur", 33.0),
    ("Sur", 31.0),
    ("Centro", 11.0),
    ("Centro", 13.0),
    ("Centro", 10.0),
    ("Este", 5.0),
    ("Oeste", NAN),
]
# Una instantánea como la de `extraer`, pero solo con las columnas que lee findings.
CSV = "etiqueta,valor\n" + "".join(
    f"{label},{'' if math.isnan(value) else value}\n" for label, value in ROWS
)


def frame_of(rows: list[tuple[str, float]]) -> pd.DataFrame:
    return pd.DataFrame(rows, columns=["etiqueta", "valor"])


def write(tmp_path: Path, text: str = CSV) -> Path:
    path = tmp_path / "instantanea.csv"
    path.write_text(text, encoding="utf-8")
    return path


def values_of(label: str) -> np.ndarray:
    return np.array([v for name, v in ROWS if name == label and not math.isnan(v)])


def finding(first: str, second: str, p_adjusted: float) -> Finding:
    """Un hallazgo con números fijos, para probar la figura y el informe sin SciPy."""
    comparison = Comparison(
        sizes=(3, 4),
        means=(10.0, 12.5),
        stds=(1.0, 2.0),
        difference=-2.5,
        low=-5.0,
        high=-0.25,
        effect=-1.58,
        p_welch=0.0312,
        p_ranks=0.0571,
    )
    return Finding(first, second, comparison, p_adjusted)


# --- read_snapshot --------------------------------------------------------------------


def test_read_snapshot_returns_the_table_and_the_digest_of_its_bytes(tmp_path: Path) -> None:
    path = write(tmp_path)
    frame, digest = read_snapshot(path)
    assert digest == hashlib.sha256(path.read_bytes()).hexdigest()
    assert list(frame.columns) == ["etiqueta", "valor"]
    assert len(frame) == len(ROWS)


def test_read_snapshot_accepts_the_expected_digest(tmp_path: Path) -> None:
    path = write(tmp_path)
    expected = hashlib.sha256(path.read_bytes()).hexdigest()
    assert read_snapshot(path, expected)[1] == expected


def test_read_snapshot_stops_on_another_digest(tmp_path: Path) -> None:
    path = write(tmp_path)
    with pytest.raises(ValueError, match=r"instantanea\.csv.*0{64}"):
        read_snapshot(path, "0" * 64)


def test_read_snapshot_keeps_na_as_a_label_and_an_empty_cell_as_missing(tmp_path: Path) -> None:
    frame, _ = read_snapshot(write(tmp_path, "etiqueta,valor\nNA,1.5\nnull,\n"))
    assert list(frame["etiqueta"]) == ["NA", "null"]
    assert frame["valor"].iloc[0] == 1.5
    assert math.isnan(frame["valor"].iloc[1])


def test_read_snapshot_reads_labels_as_text_even_if_they_look_like_numbers(
    tmp_path: Path,
) -> None:
    frame, _ = read_snapshot(write(tmp_path, "etiqueta,valor\n01,1.5\n2,2.5\n"))
    assert list(frame["etiqueta"]) == ["01", "2"]


def test_read_snapshot_reads_the_value_as_float_even_without_values(tmp_path: Path) -> None:
    frame, _ = read_snapshot(write(tmp_path, "etiqueta,valor\nNorte,\n"))
    assert frame["valor"].dtype == "float64"


def test_read_snapshot_a_value_that_is_not_a_number_raises_valueerror(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        read_snapshot(write(tmp_path, "etiqueta,valor\nNorte,doce\n"))


def test_read_snapshot_needs_etiqueta_and_valor(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="etiqueta, valor"):
        read_snapshot(write(tmp_path, "label,value\nNorte,1\n"))


def test_read_snapshot_of_a_missing_file_raises_oserror(tmp_path: Path) -> None:
    with pytest.raises(OSError):
        read_snapshot(tmp_path / "no-existe.csv")


# --- comparable y compare_all ---------------------------------------------------------


def test_comparable_keeps_labels_with_two_distinct_values_in_order() -> None:
    rows = [*ROWS, ("Igual", 4.0), ("Igual", 4.0)]
    assert comparable(frame_of(rows)) == ["Centro", "Norte", "Sur"]


def test_compare_all_compares_every_pair_in_alphabetical_order() -> None:
    pairs = [(f.first, f.second) for f in compare_all(frame_of(ROWS))]
    assert pairs == [("Centro", "Norte"), ("Centro", "Sur"), ("Norte", "Sur")]


def test_compare_all_uses_difference_without_the_missing_values() -> None:
    found = compare_all(frame_of(ROWS))
    assert found[1].comparison == difference(values_of("Centro"), values_of("Sur"))


def test_compare_all_passes_the_confidence() -> None:
    found = compare_all(frame_of(ROWS), confidence=0.99)
    assert found[0].comparison == difference(values_of("Centro"), values_of("Norte"), 0.99)


def test_compare_all_corrects_with_benjamini_hochberg() -> None:
    found = compare_all(frame_of(ROWS))
    raw = [f.comparison.p_welch for f in found]
    expected = stats.false_discovery_control(raw, method="bh")
    assert [f.p_adjusted for f in found] == pytest.approx(list(expected))


def test_compare_all_correction_by_hand() -> None:
    # BH a mano: ordena los m p-valores, multiplica el de puesto k por m/k y, de abajo
    # arriba, quédate con el menor visto. Ningún p corregido puede bajar del original.
    found = compare_all(frame_of(ROWS))
    m = len(found)
    ranked = sorted(found, key=lambda f: f.comparison.p_welch)
    scaled = [f.comparison.p_welch * m / k for k, f in enumerate(ranked, start=1)]
    by_hand = [min(scaled[i:]) for i in range(m)]
    assert [f.p_adjusted for f in ranked] == pytest.approx(by_hand)


def test_compare_all_with_two_labels_does_not_correct() -> None:
    (only,) = compare_all(frame_of([r for r in ROWS if r[0] in {"Norte", "Sur"}]))
    assert only.p_adjusted == pytest.approx(only.comparison.p_welch)


def test_compare_all_needs_two_comparable_labels() -> None:
    with pytest.raises(ValueError, match=r"\(hay 1\)"):
        compare_all(frame_of([r for r in ROWS if r[0] in {"Norte", "Este", "Oeste"}]))


@settings(max_examples=30, deadline=None)
@given(
    st.lists(
        st.lists(st.integers(0, 100).map(float), min_size=2, max_size=12).filter(
            lambda values: len(set(values)) >= 2
        ),
        min_size=2,
        max_size=5,
    )
)
def test_compare_all_never_lowers_a_p_value(groups: list[list[float]]) -> None:
    rows = [(f"E{index}", value) for index, group in enumerate(groups) for value in group]
    for found in compare_all(frame_of(rows)):
        assert found.comparison.p_welch <= found.p_adjusted + 1e-12
        assert found.p_adjusted <= 1


# --- headline y differences_figure ----------------------------------------------------


def test_headline_counts_only_p_strictly_below_alpha() -> None:
    found = [finding("A", "B", 0.01), finding("A", "C", 0.05), finding("B", "C", 0.2)]
    assert headline(found, 0.05) == "Difieren 1 de 3 pares de etiquetas (BH, α = 0.05)"


def test_headline_writes_alpha_without_trailing_zeros() -> None:
    assert headline([finding("A", "B", 0.5)], 0.1).endswith("(BH, α = 0.1)")


def test_figure_has_one_row_per_pair_with_the_first_on_top() -> None:
    figure = differences_figure([finding("A", "B", 0.01), finding("A", "C", 0.3)], "mm", 0.05)
    axes = figure.axes[0]
    assert [label.get_text() for label in axes.get_yticklabels()] == ["A - B", "A - C"]
    low, high = axes.get_ylim()
    assert low > high


def test_figure_bars_go_from_low_to_high() -> None:
    figure = differences_figure([finding("A", "B", 0.01)], "mm", 0.05)
    _, _, (bars,) = figure.axes[0].containers[0]
    ((start, _), (end, _)) = bars.get_segments()[0]
    assert (start, end) == pytest.approx((-5.0, -0.25))


def test_figure_title_is_the_headline_and_the_axis_has_the_unit() -> None:
    found = [finding("A", "B", 0.01)]
    axes = differences_figure(found, "mm", 0.05).axes[0]
    assert axes.get_title() == headline(found, 0.05)
    assert axes.get_xlabel() == "diferencia de medias (mm)"


def test_figure_marks_the_zero() -> None:
    axes = differences_figure([finding("A", "B", 0.01)], "mm", 0.05).axes[0]
    assert any(np.array_equal(line.get_xdata(), [0, 0]) for line in axes.get_lines())


# --- render ---------------------------------------------------------------------------


def report(*found: Finding, rows: list[tuple[str, float]] | None = None, **options: float) -> str:
    frame = frame_of(rows if rows is not None else [("A", 1.0), ("B", NAN), ("C", 2.0)])
    return render(frame, list(found), name="instantanea.csv", digest="ab" * 32, **options)


def test_render_says_which_data_and_how_many_values() -> None:
    text = report(finding("A", "B", 0.01))
    assert text.startswith("# Hallazgos: diferencias entre etiquetas\n")
    assert f"`instantanea.csv`, sha256 `{'ab' * 32}`: 3 medidas, 2 con valor." in text


def test_render_writes_the_headline_and_links_the_figure() -> None:
    text = report(finding("A", "B", 0.01))
    assert "\nDifieren 1 de 1 pares de etiquetas (BH, α = 0.05).\n" in text
    assert f"]({FIGURE})" in text


def test_render_writes_one_row_per_pair() -> None:
    lines = report(finding("A", "B", 0.0412), finding("A", "C", 0.3)).splitlines()
    rows = [line for line in lines if line.startswith("| A - ")]
    assert rows[0] == (
        "| A - B | 3 / 4 | -2.50 | [-5.00, -0.25] | -1.58 | 0.0312 | 0.0412 | 0.0571 | sí |"
    )
    assert rows[1].endswith("| 0.3 | 0.0571 | no |")


def test_render_a_p_equal_to_alpha_does_not_differ() -> None:
    assert "| 0.05 | 0.0571 | no |" in report(finding("A", "B", 0.05))


def test_render_uses_the_confidence_and_alpha_it_gets() -> None:
    text = report(finding("A", "B", 0.02), confidence=0.99, alpha=0.01)
    assert "| IC 99 % |" in text
    assert "intervalo del 99 %" in text
    assert "menor que 0.01" in text
    assert "| 0.02 | 0.0571 | no |" in text


def test_render_escapes_a_bar_in_a_label() -> None:
    text = report(finding("A|1", "B", 0.5), rows=[("A|1", 1.0), ("B", 2.0)])
    assert "| A\\|1 - B |" in text


def test_render_lists_the_labels_it_could_not_compare() -> None:
    assert report(finding("A", "B", 0.5)).endswith(
        "Sin comparar, por tener menos de dos valores distintos: C.\n"
    )


def test_render_without_labels_left_out_ends_with_the_table() -> None:
    text = report(finding("A", "B", 0.5), rows=[("A", 1.0), ("B", 2.0)])
    assert "Sin comparar" not in text
    assert text.endswith("| no |\n")


def test_render_has_no_date_or_path() -> None:
    text = report(finding("A", "B", 0.5))
    assert str(Path.cwd()) not in text
    assert not any(str(year) in text for year in range(2020, 2040))


# --- el comando hallazgos -------------------------------------------------------------


def test_hallazgos_writes_the_report_and_the_figure(tmp_path: Path) -> None:
    path, folder = write(tmp_path), tmp_path / "informe"
    result = runner.invoke(cli.app, ["hallazgos", str(path), str(folder)])
    assert result.exit_code == 0, result.output
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    assert result.stdout.splitlines() == [
        f"instantanea.csv: {len(ROWS)} medidas · sha256: {digest}",
        "Difieren 2 de 3 pares de etiquetas (BH, α = 0.05)",
        f"informe: {folder / REPORT} · figura: {folder / FIGURE}",
    ]
    assert (folder / REPORT).read_text(encoding="utf-8").startswith("# Hallazgos")
    assert (folder / FIGURE).read_text(encoding="utf-8").startswith("<?xml")


def test_hallazgos_twice_gives_the_same_bytes(tmp_path: Path) -> None:
    path, folder = write(tmp_path), tmp_path / "informe"
    files = []
    for _ in range(2):
        runner.invoke(cli.app, ["hallazgos", str(path), str(folder)])
        files.append([(folder / name).read_bytes() for name in (REPORT, FIGURE)])
    assert files[0] == files[1]


def test_hallazgos_report_does_not_depend_on_where_it_runs(tmp_path: Path) -> None:
    path = write(tmp_path)
    texts = []
    for folder in (tmp_path / "a", tmp_path / "b" / "c"):
        runner.invoke(cli.app, ["hallazgos", str(path), str(folder)])
        texts.append((folder / REPORT).read_text(encoding="utf-8"))
    assert texts[0] == texts[1]


def test_hallazgos_checks_the_digest(tmp_path: Path) -> None:
    path, folder = write(tmp_path), tmp_path / "informe"
    result = runner.invoke(cli.app, ["hallazgos", str(path), str(folder), "--huella", "0" * 64])
    assert result.exit_code == 1
    assert "la huella de instantanea.csv es" in result.stderr
    assert not folder.exists()


def test_hallazgos_with_the_right_digest(tmp_path: Path) -> None:
    path = write(tmp_path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    args = ["hallazgos", str(path), str(tmp_path / "informe"), "--huella", digest]
    assert runner.invoke(cli.app, args).exit_code == 0


def test_hallazgos_passes_confianza_and_alfa(tmp_path: Path) -> None:
    path, folder = write(tmp_path), tmp_path / "informe"
    args = ["hallazgos", str(path), str(folder), "--confianza", "0.99", "--alfa", "0.001"]
    result = runner.invoke(cli.app, args)
    text = (folder / REPORT).read_text(encoding="utf-8")
    assert "(BH, α = 0.001)" in result.stdout
    assert "(BH, α = 0.001)" in text
    assert "| IC 99 % |" in text


@pytest.mark.parametrize("option", [["--alfa", "0.9"], ["--confianza", "0.2"]])
def test_hallazgos_options_out_of_range_exit_2(tmp_path: Path, option: list[str]) -> None:
    args = ["hallazgos", str(write(tmp_path)), str(tmp_path / "informe"), *option]
    assert runner.invoke(cli.app, args).exit_code == 2


def test_hallazgos_missing_file_exits_2(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["hallazgos", str(tmp_path / "x.csv"), str(tmp_path)])
    assert result.exit_code == 2
    assert "no se puede leer" in result.stderr


def test_hallazgos_needs_two_labels(tmp_path: Path) -> None:
    path = write(tmp_path, "etiqueta,valor\nNorte,1\nNorte,2\n")
    result = runner.invoke(cli.app, ["hallazgos", str(path), str(tmp_path / "informe")])
    assert result.exit_code == 1
    assert "hacen falta dos etiquetas" in result.stderr


def test_hallazgos_folder_that_cannot_be_written_exits_2(tmp_path: Path) -> None:
    taken = tmp_path / "ocupado"
    taken.write_text("un archivo, no una carpeta", encoding="utf-8")
    result = runner.invoke(cli.app, ["hallazgos", str(write(tmp_path)), str(taken)])
    assert result.exit_code == 2
    assert "no se puede escribir" in result.stderr


def test_findings_is_not_reexported_from_core() -> None:
    import observatorio.core

    assert "findings" not in observatorio.core.__all__
    assert not hasattr(observatorio.core, "Finding")
