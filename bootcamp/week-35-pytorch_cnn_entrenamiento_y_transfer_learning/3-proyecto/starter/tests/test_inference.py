"""Tests de la semana 28: comparar dos etiquetas con SciPy.

Qué: comprueban core/inference.py con muestras cuyos resultados se pueden calcular a mano
(medias, desviaciones, el intervalo y el p-valor de Welch, la d de Cohen, el p-valor exacto
de Mann-Whitney), propiedades que se cumplen con cualquier muestra, y el comando `comparar`.
Para qué: un contraste mal hecho no falla: escribe un p-valor con buena cara. Usar la
prueba de Student en lugar de la de Welch, o la desviación de la población en lugar de la
de la muestra, cambia los números en la segunda cifra, y solo un test con el valor exacto
lo ve.
Impacto: inference.py no se reexporta en core: la CLI arranca sin cargar scipy.
"""

import dataclasses
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest
from hypothesis import assume, given
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays
from typer.testing import CliRunner

from observatorio import cli
from observatorio.core import Measurement, Series
from observatorio.core.arrays import Floats
from observatorio.core.inference import Comparison, difference, sample

runner = CliRunner()

NAN = math.nan


def floats(*values: float) -> Floats:
    """Un array de float64 con esos valores."""
    return np.array(values, dtype=np.float64)


# Dos muestras con la misma dispersión: medias 3 y 8, desviación sqrt(2,5) en las dos.
# Error estándar sqrt(2,5/5 + 2,5/5) = 1, t = -5 con 8 grados de libertad.
LOW = floats(1, 2, 3, 4, 5)
HIGH = floats(6, 7, 8, 9, 10)
# Dos muestras con dispersiones muy distintas (1 y 12,9): Welch y Student no coinciden.
NARROW = floats(1, 2, 3)
WIDE = floats(10, 20, 30, 40)

# Norte: 12,5, 14 y 13; Sur: 8, 9,5 y 8,5 (el NA no cuenta); Centro, un solo valor.
TEXT = "Norte;12,5\nSur;8\nNorte;14\nSur;9,5\nNorte;13\nSur;NA\nSur;8,5\nCentro;3\n"

# Décimas entre -1000 y 1000: sin valores casi iguales que hagan perder precisión a SciPy.
TENTHS = st.integers(-10_000, 10_000).map(lambda n: n / 10)
SAMPLES = arrays(np.float64, st.integers(2, 30), elements=TENTHS)


def write(tmp_path: Path, text: str, name: str = "medidas.txt") -> Path:
    """Guarda text en tmp_path/name y devuelve la ruta."""
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


# --- sample ---


def test_sample_keeps_the_values_of_the_label_in_order() -> None:
    series = Series([Measurement("Norte", 3.0), Measurement("Sur", 1.0), Measurement("Norte", 2.0)])
    np.testing.assert_array_equal(sample(series, "Norte"), [3.0, 2.0])


def test_sample_leaves_out_the_missing_values() -> None:
    series = Series([Measurement("Norte", None), Measurement("Norte", 2.0)])
    np.testing.assert_array_equal(sample(series, "Norte"), [2.0])


def test_sample_of_a_label_that_is_not_there_is_empty() -> None:
    result = sample(Series([Measurement("Norte", 2.0)]), "Sur")
    assert result.dtype == np.float64
    assert result.size == 0


# --- difference: los números ---


def test_difference_sizes_means_and_sample_stds() -> None:
    result = difference(LOW, HIGH)
    assert result.sizes == (5, 5)
    assert result.means == (3.0, 8.0)
    # ddof=1: dividir entre n - 1 = 4, no entre 5 (que daría sqrt(2) = 1,414).
    assert result.stds == pytest.approx((math.sqrt(2.5), math.sqrt(2.5)))


def test_difference_is_the_first_mean_minus_the_second() -> None:
    assert difference(LOW, HIGH).difference == -5.0
    assert difference(HIGH, LOW).difference == 5.0


def test_difference_interval_is_welch() -> None:
    # -5 ± t(0,975; 8 gl) · 1 = -5 ± 2,306.
    result = difference(LOW, HIGH)
    assert (result.low, result.high) == pytest.approx((-7.306004, -2.693996))


def test_difference_p_value_is_welch() -> None:
    # 2 · P(T > 5) con 8 grados de libertad.
    assert difference(LOW, HIGH).p_welch == pytest.approx(0.0010528258)


def test_difference_does_not_assume_equal_spreads() -> None:
    # Welch: 3,05 grados de libertad. Student daría p = 0,0299 con 5.
    result = difference(NARROW, WIDE)
    assert result.p_welch == pytest.approx(0.0371625)
    assert (result.low, result.high) == pytest.approx((-43.442451, -2.557549))


def test_difference_effect_is_cohen_d() -> None:
    # -5 / sqrt((2,5 + 2,5) / 2) = -5 / 1,581.
    assert difference(LOW, HIGH).effect == pytest.approx(-3.1622777)


def test_difference_effect_averages_the_two_variances() -> None:
    # -23 / sqrt((1 + 166,67) / 2) = -23 / 9,156.
    assert difference(NARROW, WIDE).effect == pytest.approx(-2.5119990)


def test_difference_p_ranks_is_exact_mann_whitney() -> None:
    # Todos los de LOW por debajo de todos los de HIGH: 2 de las 252 formas de repartir
    # 10 rangos en dos grupos de 5 son así de extremas (una por cada lado).
    assert difference(LOW, HIGH).p_ranks == pytest.approx(2 / 252)


def test_difference_p_ranks_cannot_go_below_one_tenth_with_three_and_three() -> None:
    # Con 3 y 3 solo hay 20 repartos: lo más extremo es 2 / 20 = 0,1.
    assert difference(floats(1, 2, 3), floats(7, 8, 9)).p_ranks == pytest.approx(0.1)


def test_difference_of_the_same_sample_is_zero_with_p_one() -> None:
    result = difference(LOW, LOW)
    assert result.difference == 0.0
    assert result.effect == 0.0
    assert result.p_welch == pytest.approx(1.0)
    assert result.p_ranks == pytest.approx(1.0)


def test_difference_uses_95_percent_by_default() -> None:
    assert difference(LOW, HIGH) == difference(LOW, HIGH, 0.95)


def test_difference_more_confidence_gives_a_wider_interval() -> None:
    # -5 ± t(0,995; 8 gl) · 1 = -5 ± 3,355.
    result = difference(LOW, HIGH, 0.99)
    assert (result.low, result.high) == pytest.approx((-8.355387, -1.644613))


def test_difference_is_frozen() -> None:
    result = difference(LOW, HIGH)
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.difference = 0.0  # type: ignore[misc]


# --- difference: cuándo no se puede ---


@pytest.mark.parametrize(
    ("first", "second", "sizes"),
    [(floats(1), HIGH, "1 y 5"), (LOW, floats(1), "5 y 1"), (floats(), floats(), "0 y 0")],
)
def test_difference_needs_two_values_in_each_sample(
    first: Floats, second: Floats, sizes: str
) -> None:
    with pytest.raises(ValueError) as error:
        difference(first, second)
    assert str(error.value) == f"cada muestra necesita al menos 2 valores (tienen {sizes})"


@pytest.mark.parametrize(
    ("first", "second"),
    [(floats(5, 5, 5), LOW), (LOW, floats(1, 1)), (floats(0.1, 0.1, 0.1), LOW)],
)
def test_difference_needs_both_samples_to_vary(first: Floats, second: Floats) -> None:
    # Un sensor atascado: sin dispersión, Welch no puede medir cuánto mueve el azar la media.
    with pytest.raises(ValueError) as error:
        difference(first, second)
    assert str(error.value) == (
        "las dos muestras tienen que variar: una tiene todos sus valores iguales"
    )


# --- difference: propiedades ---


@given(SAMPLES, SAMPLES)
def test_difference_interval_contains_the_difference(first: Floats, second: Floats) -> None:
    assume(np.ptp(first) > 0 and np.ptp(second) > 0)
    result = difference(first, second)
    assert result.low <= result.difference <= result.high
    assert 0 <= result.p_welch <= 1
    assert 0 <= result.p_ranks <= 1


@given(SAMPLES, SAMPLES)
def test_difference_swapping_the_samples_changes_only_the_sign(
    first: Floats, second: Floats
) -> None:
    assume(np.ptp(first) > 0 and np.ptp(second) > 0)
    forward, backward = difference(first, second), difference(second, first)
    assert backward.difference == pytest.approx(-forward.difference)
    assert (backward.low, backward.high) == pytest.approx((-forward.high, -forward.low))
    assert backward.effect == pytest.approx(-forward.effect)
    assert backward.p_welch == pytest.approx(forward.p_welch)
    assert backward.p_ranks == pytest.approx(forward.p_ranks)


@given(SAMPLES, SAMPLES, st.integers(-1000, 1000))
def test_difference_does_not_change_when_both_samples_move(
    first: Floats, second: Floats, shift: int
) -> None:
    # Sumar lo mismo a todas las medidas (otro cero de la escala) no cambia la pregunta.
    assume(np.ptp(first) > 0 and np.ptp(second) > 0)
    before, after = difference(first, second), difference(first + shift, second + shift)
    assert after.difference == pytest.approx(before.difference, abs=1e-6)
    assert after.p_welch == pytest.approx(before.p_welch, abs=1e-6)
    assert after.p_ranks == pytest.approx(before.p_ranks)


# --- comparar ---


def comparar(tmp_path: Path, text: str, *arguments: str) -> tuple[int, str, str]:
    """Ejecuta `comparar` sobre text y devuelve el código de salida, stdout y stderr."""
    result = runner.invoke(cli.app, ["comparar", str(write(tmp_path, text)), *arguments])
    return result.exit_code, result.stdout, result.stderr


def test_comparar_writes_both_samples_the_interval_the_effect_and_the_p_values(
    tmp_path: Path,
) -> None:
    code, stdout, _ = comparar(tmp_path, TEXT, "Norte", "Sur")
    assert code == 0
    assert stdout.splitlines() == [
        "Norte: 3 medidas, media 13.17, desviación 0.76",
        "Sur: 3 medidas, media 8.67, desviación 0.76",
        "diferencia Norte - Sur: 4.50, IC 95 %: [2.77, 6.23]",
        "tamaño del efecto (d de Cohen): 5.89",
        "p (Welch): 0.00196 · p (Mann-Whitney): 0.1",
    ]


def test_comparar_order_of_the_labels_changes_the_sign(tmp_path: Path) -> None:
    _, stdout, _ = comparar(tmp_path, TEXT, "Sur", "Norte")
    lines = stdout.splitlines()
    assert lines[0] == "Sur: 3 medidas, media 8.67, desviación 0.76"
    assert lines[2] == "diferencia Sur - Norte: -4.50, IC 95 %: [-6.23, -2.77]"
    assert lines[3] == "tamaño del efecto (d de Cohen): -5.89"


def test_comparar_confianza_changes_the_interval(tmp_path: Path) -> None:
    _, stdout, _ = comparar(tmp_path, TEXT, "Norte", "Sur", "--confianza", "0.99")
    assert stdout.splitlines()[2] == "diferencia Norte - Sur: 4.50, IC 99 %: [1.63, 7.37]"


@pytest.mark.parametrize("value", ["0.4", "1"])
def test_comparar_confianza_out_of_range_exits_2(tmp_path: Path, value: str) -> None:
    code, stdout, stderr = comparar(tmp_path, TEXT, "Norte", "Sur", "--confianza", value)
    assert code == 2
    assert stdout == ""
    assert "--confianza" in stderr


@pytest.mark.parametrize(("other", "sizes"), [("Centro", "3 y 1"), ("Este", "3 y 0")])
def test_comparar_a_label_with_less_than_two_values_exits_2(
    tmp_path: Path, other: str, sizes: str
) -> None:
    code, stdout, stderr = comparar(tmp_path, TEXT, "Norte", other)
    assert code == 2
    assert stdout == ""
    assert stderr == (
        f"error: no se puede comparar Norte con {other}:"
        f" cada muestra necesita al menos 2 valores (tienen {sizes})\n"
    )


def test_comparar_a_label_without_spread_exits_2(tmp_path: Path) -> None:
    code, _, stderr = comparar(tmp_path, "A;1\nA;1\nB;2\nB;2\n", "A", "B")
    assert code == 2
    assert stderr == (
        "error: no se puede comparar A con B:"
        " las dos muestras tienen que variar: una tiene todos sus valores iguales\n"
    )


def test_comparar_reports_invalid_lines_compares_the_rest_and_exits_1(tmp_path: Path) -> None:
    code, stdout, stderr = comparar(tmp_path, TEXT + "malo\n", "Norte", "Sur")
    assert code == 1
    assert stderr == "error: medidas.txt: línea 9: 'malo'\n"
    assert stdout.splitlines()[2] == "diferencia Norte - Sur: 4.50, IC 95 %: [2.77, 6.23]"


def test_comparar_missing_file_exits_2(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["comparar", str(tmp_path / "no.txt"), "Norte", "Sur"])
    assert result.exit_code == 2
    assert result.stderr.startswith("error: ")


def test_comparar_needs_two_labels(tmp_path: Path) -> None:
    code, _, stderr = comparar(tmp_path, TEXT, "Norte")
    assert code == 2
    assert "OTRA" in stderr


def test_comparar_reads_csv(tmp_path: Path) -> None:
    path = write(tmp_path, "etiqueta;valor\nA;1\nA;2\nB;3\nB;5\n", "medidas.csv")
    result = runner.invoke(cli.app, ["comparar", str(path), "A", "B"])
    assert result.exit_code == 0
    assert result.stdout.splitlines()[0] == "A: 2 medidas, media 1.50, desviación 0.71"


# --- scipy solo cuando hace falta ---


def test_inference_is_not_reexported_from_core() -> None:
    import observatorio.core

    assert "inference" not in observatorio.core.__all__
    assert not hasattr(observatorio.core, "difference")


def run_python(code: str) -> str:
    """Lo que escribe code en otro proceso de Python, donde nadie ha importado nada aún."""
    result = subprocess.run(
        [sys.executable, "-c", code], check=False, capture_output=True, text=True
    )
    return result.stdout


def test_importing_the_cli_does_not_load_scipy() -> None:
    code = "import sys, observatorio.cli; print('scipy' in sys.modules)"
    assert run_python(code) == "False\n"


def test_comparison_fields() -> None:
    names = [field.name for field in dataclasses.fields(Comparison)]
    assert names == [
        "sizes",
        "means",
        "stds",
        "difference",
        "low",
        "high",
        "effect",
        "p_welch",
        "p_ranks",
    ]
