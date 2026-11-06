import pytest

from observatorio.analysis import count_level, process_lines, ratio, share
from observatorio.rules import format_row, parse_line

UNIT, LOW, HIGH = "µg/m³", 10.0, 50.0


def make_row(level: str) -> str:
    """Una fila real de format_row con el nivel pedido (el valor no importa aquí)."""
    return format_row("Norte", 12.5, "µg/m³", level)


def test_process_lines_rows_and_errors() -> None:
    rows, errors = process_lines(["# cabecera", "Norte;12,5", "", "malo", " Sur;80 "], UNIT, LOW, HIGH)
    assert rows == [parse_line("Norte;12,5", UNIT, LOW, HIGH), parse_line("Sur;80", UNIT, LOW, HIGH)]
    assert errors == ["línea 4: 'malo'"]


def test_process_lines_empty() -> None:
    assert process_lines([], UNIT, LOW, HIGH) == ([], [])


def test_process_lines_accepts_any_iterable() -> None:
    # Qué: un iterable que no es una lista (una línea por vuelta, como sys.stdin).
    # Para qué: comprobar que process_lines solo recorre las líneas una vez.
    lines = iter(["Norte;12,5", "Sur;8"])
    rows, errors = process_lines(lines, UNIT, LOW, HIGH)
    assert len(rows) == 2
    assert errors == []


def test_process_lines_does_not_print(capsys: pytest.CaptureFixture[str]) -> None:
    process_lines(["Norte;12,5", "malo"], UNIT, LOW, HIGH)
    assert capsys.readouterr() == ("", "")


@pytest.mark.parametrize(
    ("levels", "level", "expected"),
    [
        (["alto", "bajo", "alto"], "alto", 2),
        (["alto", "bajo", "alto"], "medio", 0),
        ([], "alto", 0),
        (["sin dato", "sin dato"], "sin dato", 2),
    ],
)
def test_count_level(levels: list[str], level: str, expected: int) -> None:
    assert count_level([make_row(each) for each in levels], level) == expected


@pytest.mark.parametrize(
    ("part", "total", "expected"),
    [(1, 4, 0.25), (2, 7, 0.2857142857), (0, 5, 0.0), (5, 5, 1.0), (0, 0, 0.0)],
)
def test_ratio(part: int, total: int, expected: float) -> None:
    assert ratio(part, total) == pytest.approx(expected)


@pytest.mark.parametrize(("part", "total"), [(-1, 4), (5, 4), (0, -1)])
def test_ratio_rejects_impossible_values(part: int, total: int) -> None:
    with pytest.raises(ValueError):
        ratio(part, total)


def test_share_default_decimals() -> None:
    assert share(2, 7) == "28.6 %"


def test_share_with_decimals() -> None:
    assert share(2, 7, decimals=2) == "28.57 %"
    assert share(1, 3, decimals=0) == "33 %"


def test_share_of_nothing() -> None:
    assert share(0, 0) == "0.0 %"


def test_share_propagates_ratio_errors() -> None:
    with pytest.raises(ValueError):
        share(8, 7)
