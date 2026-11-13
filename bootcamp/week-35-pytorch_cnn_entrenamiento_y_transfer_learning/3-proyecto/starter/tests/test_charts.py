"""Tests de la semana 27: gráficos con matplotlib.

Qué: comprueban core/charts.py mirando lo que hay dentro de la figura (líneas, datos,
leyenda, títulos), no los píxeles; guardan PNG, SVG y PDF, y prueban el comando `graficar`.
Para qué: un gráfico puede salir sin errores y aun así mentir: una etiqueta que falta en la
leyenda, un periodo sin dato unido a los demás, un punto suelto que no se ve. Estos tests
dejan escrito qué tiene que haber en la figura.
Impacto: charts.py no se reexporta y no usa pyplot: la CLI arranca sin matplotlib, y
ninguna figura queda abierta en un registro global.
"""

import io
import math
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import numpy.typing as npt
import pandas as pd
import pytest
from hypothesis import given
from hypothesis import strategies as st
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from typer.testing import CliRunner

from observatorio import cli
from observatorio.core import Measurement, Series, frames, summaries
from observatorio.core.charts import evolution_figure, save

runner = CliRunner()

NAN = math.nan
# Tres periodos de dos horas: Norte no tiene dato en el segundo, Sur en el tercero.
TIMES = pd.date_range("2026-11-01 08:00", periods=3, freq="2h", name="time")
TABLE = pd.DataFrame({"Norte": [12.5, NAN, 48.9], "Sur": [8.0, 9.5, NAN]}, index=TIMES).rename_axis(
    columns="label"
)

TEXT = "Norte;12,5\nSur;8\nCentro;NA\nOriente;55,1\nOccidente;61\nNorte;48,9\nSur;9,5\n"
START = "2026-11-01T08:00:00"

LABELS = ["Norte", "Sur", "_oculta"]
VALUES = st.floats(min_value=-1e6, max_value=1e6, allow_nan=False)
MEASUREMENTS = st.lists(st.builds(Measurement, st.sampled_from(LABELS), st.none() | VALUES))


def table_of(series: Series, period: timedelta = timedelta(hours=2)) -> pd.DataFrame:
    """La tabla de summaries.evolution de una serie con una medida por hora."""
    frame = summaries.timed(frames.frame_of(series), datetime(2026, 11, 1, 8), timedelta(hours=1))
    return summaries.evolution(frame, period)


def legend_of(figure: Figure) -> list[str]:
    """Los nombres que escribe la leyenda de la figura, en orden."""
    legend = figure.axes[0].get_legend()
    assert legend is not None
    return [text.get_text() for text in legend.get_texts()]


def xs(line: Line2D) -> list[object]:
    """Los valores x de una línea, tal como se los dio plot."""
    return list(np.asarray(line.get_xdata()))


def ys(line: Line2D) -> npt.NDArray[np.float64]:
    """Los valores y de una línea, como array de float."""
    return np.asarray(line.get_ydata(), dtype=np.float64)


def saved(figure: Figure, suffix: str, tmp_path: Path) -> bytes:
    """Los bytes de la figura guardada con save en tmp_path, con esa extensión."""
    path = tmp_path / f"grafico{suffix}"
    save(figure, path)
    return path.read_bytes()


def write(tmp_path: Path, text: str, name: str = "medidas.txt") -> Path:
    """Guarda text en tmp_path/name y devuelve la ruta."""
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


# --- evolution_figure ---


def test_evolution_figure_is_a_figure_with_one_axes() -> None:
    figure = evolution_figure(TABLE, "título")
    assert isinstance(figure, Figure)
    assert len(figure.axes) == 1


def test_evolution_figure_has_one_line_per_label() -> None:
    assert len(evolution_figure(TABLE, "título").axes[0].get_lines()) == 2


def test_evolution_figure_lines_have_the_times_and_the_means() -> None:
    norte, sur = evolution_figure(TABLE, "título").axes[0].get_lines()
    assert (xs(norte)) == list(TIMES)
    assert (xs(sur)) == list(TIMES)
    np.testing.assert_array_equal(ys(norte), [12.5, NAN, 48.9])
    np.testing.assert_array_equal(ys(sur), [8.0, 9.5, NAN])


def test_evolution_figure_keeps_nan_so_the_line_breaks() -> None:
    # Un NaN corta la línea: quitarlo uniría el primer y el tercer periodo como si
    # hubiera dato en el segundo.
    norte = evolution_figure(TABLE, "título").axes[0].get_lines()[0]
    assert len(ys(norte)) == 3
    assert math.isnan(ys(norte)[1])


def test_evolution_figure_marks_every_point() -> None:
    # Sin marcador, un periodo con dato entre dos sin él no se vería.
    for line in evolution_figure(TABLE, "título").axes[0].get_lines():
        assert line.get_marker() == "o"


def test_evolution_figure_lines_have_different_colors() -> None:
    norte, sur = evolution_figure(TABLE, "título").axes[0].get_lines()
    assert norte.get_color() != sur.get_color()


def test_evolution_figure_legend_names_the_labels_in_order() -> None:
    figure = evolution_figure(TABLE, "título")
    assert legend_of(figure) == ["Norte", "Sur"]
    legend = figure.axes[0].get_legend()
    assert legend is not None
    assert legend.get_title().get_text() == "etiqueta"


def test_evolution_figure_legend_keeps_labels_that_start_with_underscore() -> None:
    table = TABLE.rename(columns={"Sur": "_sur"})
    assert legend_of(evolution_figure(table, "título")) == ["Norte", "_sur"]


def test_evolution_figure_has_the_title_and_the_axis_names() -> None:
    axes = evolution_figure(TABLE, "medidas.txt: media cada 2h").axes[0]
    assert axes.get_title() == "medidas.txt: media cada 2h"
    assert axes.get_xlabel() == "periodo"
    assert axes.get_ylabel() == "media"


def test_evolution_figure_size() -> None:
    assert tuple(evolution_figure(TABLE, "título").get_size_inches()) == (8.0, 4.5)


def test_evolution_figure_of_an_empty_table() -> None:
    figure = evolution_figure(table_of(Series([])), "vacío")
    assert figure.axes[0].get_lines() == []
    assert legend_of(figure) == []


def test_evolution_figure_of_a_label_without_values() -> None:
    # Centro no tiene ningún valor: su línea existe, sin puntos, y la leyenda lo nombra.
    table = table_of(Series([Measurement("Norte", 1.0), Measurement("Centro", None)]))
    figure = evolution_figure(table, "título")
    assert legend_of(figure) == ["Centro", "Norte"]
    assert all(math.isnan(value) for value in ys(figure.axes[0].get_lines()[0]))


@given(MEASUREMENTS)
def test_evolution_figure_draws_the_whole_table(measurements: list[Measurement]) -> None:
    table = table_of(Series(measurements))
    figure = evolution_figure(table, "título")
    lines = figure.axes[0].get_lines()
    assert legend_of(figure) == list(table.columns)
    assert len(lines) == len(table.columns)
    for line, label in zip(lines, table.columns, strict=True):
        assert (xs(line)) == list(table.index)
        np.testing.assert_array_equal(ys(line), table[label].to_numpy())


# --- save ---


@pytest.mark.parametrize(
    ("suffix", "start"),
    [(".png", b"\x89PNG\r\n\x1a\n"), (".svg", b"<?xml"), (".pdf", b"%PDF-")],
)
def test_save_chooses_the_format_from_the_suffix(tmp_path: Path, suffix: str, start: bytes) -> None:
    assert saved(evolution_figure(TABLE, "título"), suffix, tmp_path).startswith(start)


def test_save_svg_keeps_the_text_as_text(tmp_path: Path) -> None:
    # Con el texto como texto, el SVG se puede buscar, copiar y leer con un lector de pantalla.
    svg = saved(evolution_figure(TABLE, "medidas.txt: media"), ".svg", tmp_path).decode()
    for text in ["medidas.txt: media", "periodo", "media", "etiqueta", "Norte", "Sur"]:
        assert f">{text}</text>" in svg


def test_save_svg_has_no_date(tmp_path: Path) -> None:
    assert b"<dc:date>" not in saved(evolution_figure(TABLE, "título"), ".svg", tmp_path)


@pytest.mark.parametrize("suffix", [".png", ".svg"])
def test_save_is_reproducible(tmp_path: Path, suffix: str) -> None:
    # Los mismos datos, el mismo archivo: git solo ve un cambio si el gráfico cambia.
    first = saved(evolution_figure(TABLE, "título"), suffix, tmp_path)
    second = saved(evolution_figure(TABLE.copy(), "título"), suffix, tmp_path)
    assert first == second


def test_save_changes_when_the_data_changes(tmp_path: Path) -> None:
    first = saved(evolution_figure(TABLE, "título"), ".svg", tmp_path)
    second = saved(evolution_figure(TABLE * 2, "título"), ".svg", tmp_path)
    assert first != second


def test_save_does_not_change_the_global_settings(tmp_path: Path) -> None:
    import matplotlib

    # rc_context cambia la configuración solo mientras guarda, y la deja como estaba.
    with matplotlib.rc_context({"svg.hashsalt": None, "svg.fonttype": "path"}):
        save(evolution_figure(TABLE, "título"), tmp_path / "grafico.svg")
        assert matplotlib.rcParams["svg.hashsalt"] is None
        assert matplotlib.rcParams["svg.fonttype"] == "path"


def test_save_to_a_file_object() -> None:
    buffer = io.BytesIO()
    evolution_figure(TABLE, "título").savefig(buffer, format="png")
    assert buffer.getvalue().startswith(b"\x89PNG")


def test_save_unknown_suffix_raises_value_error(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Format 'txt' is not supported"):
        save(evolution_figure(TABLE, "título"), tmp_path / "grafico.txt")


def test_save_to_a_missing_folder_raises_os_error(tmp_path: Path) -> None:
    with pytest.raises(OSError):
        save(evolution_figure(TABLE, "título"), tmp_path / "no" / "grafico.png")


# --- graficar ---


def graficar(tmp_path: Path, text: str, name: str, *options: str) -> tuple[Path, int, str]:
    """Ejecuta `graficar` sobre text y devuelve el gráfico, el código de salida y stdout."""
    salida = tmp_path / name
    result = runner.invoke(
        cli.app,
        ["graficar", str(write(tmp_path, text)), str(salida), "--inicio", START, *options],
    )
    return salida, result.exit_code, result.stdout


def test_graficar_writes_a_png(tmp_path: Path) -> None:
    salida, code, _ = graficar(tmp_path, TEXT, "evolucion.png")
    assert code == 0
    assert salida.read_bytes().startswith(b"\x89PNG")


def test_graficar_writes_an_svg_with_the_labels_and_the_title(tmp_path: Path) -> None:
    salida, code, _ = graficar(tmp_path, TEXT, "evolucion.svg", "--periodo", "2h")
    svg = salida.read_text(encoding="utf-8")
    assert code == 0
    assert ">medidas.txt: media cada 2h</text>" in svg
    for label in ["Centro", "Norte", "Occidente", "Oriente", "Sur"]:
        assert f">{label}</text>" in svg


def test_graficar_ends_with_what_it_drew(tmp_path: Path) -> None:
    salida, _, stdout = graficar(tmp_path, TEXT, "evolucion.png", "--periodo", "2h")
    size = salida.stat().st_size
    assert stdout.splitlines() == [
        f"5 etiquetas y 4 periodos de 7 medidas en evolucion.png · {size} bytes"
    ]


def test_graficar_uses_the_one_day_period_by_default(tmp_path: Path) -> None:
    _, _, stdout = graficar(tmp_path, TEXT, "evolucion.png")
    assert stdout.startswith("5 etiquetas y 1 periodos de 7 medidas")


def test_graficar_cada_spaces_the_measurements(tmp_path: Path) -> None:
    _, _, stdout = graficar(tmp_path, TEXT, "evolucion.png", "--cada", "1D")
    assert stdout.startswith("5 etiquetas y 7 periodos de 7 medidas")


def test_graficar_draws_the_same_table_as_evolucion(tmp_path: Path) -> None:
    salida, _, _ = graficar(tmp_path, TEXT, "evolucion.svg", "--periodo", "2h")
    series = Series.parse(TEXT.splitlines())[0]
    figure = evolution_figure(table_of(series), "medidas.txt: media cada 2h")
    assert salida.read_bytes() == saved(figure, ".svg", tmp_path)


def test_graficar_empty_file_draws_an_empty_chart(tmp_path: Path) -> None:
    salida, code, stdout = graficar(tmp_path, "", "vacio.png")
    assert code == 0
    assert salida.exists()
    assert stdout.startswith("0 etiquetas y 0 periodos de 0 medidas en vacio.png")


def test_graficar_reports_invalid_lines_draws_the_rest_and_exits_1(tmp_path: Path) -> None:
    salida = tmp_path / "evolucion.png"
    result = runner.invoke(
        cli.app,
        ["graficar", str(write(tmp_path, "A;1\nmalo\n")), str(salida), "--inicio", START],
    )
    assert result.exit_code == 1
    assert "error: medidas.txt: línea 2: 'malo'" in result.stderr
    assert result.stdout.startswith("1 etiquetas y 1 periodos de 1 medidas")


@pytest.mark.parametrize("option", ["--cada", "--periodo"])
def test_graficar_bad_duration_exits_2_without_drawing(tmp_path: Path, option: str) -> None:
    salida, code, _ = graficar(tmp_path, TEXT, "evolucion.png", option, "0h")
    assert code == 2
    assert not salida.exists()


def test_graficar_needs_inicio(tmp_path: Path) -> None:
    result = runner.invoke(
        cli.app, ["graficar", str(write(tmp_path, TEXT)), str(tmp_path / "e.png")]
    )
    assert result.exit_code == 2
    assert "--inicio" in result.stderr


def test_graficar_missing_file_exits_2(tmp_path: Path) -> None:
    result = runner.invoke(
        cli.app,
        ["graficar", str(tmp_path / "no.txt"), str(tmp_path / "e.png"), "--inicio", START],
    )
    assert result.exit_code == 2
    assert result.stderr.startswith("error: ")


@pytest.mark.parametrize("name", ["no/existe.png", "evolucion.txt"])
def test_graficar_cannot_write_exits_2(tmp_path: Path, name: str) -> None:
    salida = tmp_path / name
    result = runner.invoke(
        cli.app, ["graficar", str(write(tmp_path, TEXT)), str(salida), "--inicio", START]
    )
    assert result.exit_code == 2
    assert result.stderr.startswith(f"error: no se puede escribir {salida}")


def test_evolucion_still_writes_the_table(tmp_path: Path) -> None:
    result = runner.invoke(
        cli.app, ["evolucion", str(write(tmp_path, TEXT)), "--inicio", START, "--periodo", "2h"]
    )
    assert result.exit_code == 0
    assert result.stdout.splitlines()[-1] == "4 periodos · 7 medidas"


# --- matplotlib solo cuando hace falta ---


def test_charts_is_not_reexported_from_core() -> None:
    import observatorio.core

    assert "charts" not in observatorio.core.__all__
    assert not hasattr(observatorio.core, "evolution_figure")


def run_python(code: str) -> str:
    """Lo que escribe code en otro proceso de Python, donde nadie ha importado nada aún."""
    result = subprocess.run(
        [sys.executable, "-c", code], check=False, capture_output=True, text=True
    )
    return result.stdout


def test_importing_the_cli_does_not_load_matplotlib() -> None:
    code = "import sys, observatorio.cli; print('matplotlib' in sys.modules)"
    assert run_python(code) == "False\n"


def test_charts_does_not_use_pyplot() -> None:
    # pyplot guarda cada figura en un registro global y elige una ventana: aquí sobra.
    code = "import sys, observatorio.core.charts; print('matplotlib.pyplot' in sys.modules)"
    assert run_python(code) == "False\n"
