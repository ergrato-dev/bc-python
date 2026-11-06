import pytest

from observatorio.report import is_data_line, level_of, longest_streak, summarize
from observatorio.rules import format_row


def make_row(level: str) -> str:
    """Una fila real de format_row con el nivel pedido (el valor no importa aquí)."""
    return format_row("Norte", 12.5, "µg/m³", level)


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("Norte;12,5", True),
        ("Norte # sin comentario;12,5", True),
        ("", False),
        ("    ", False),
        ("# etiqueta;valor", False),
        ("   # comentario con espacios delante", False),
        ("#Norte;12,5", False),
    ],
)
def test_is_data_line(line: str, expected: bool) -> None:
    assert is_data_line(line) is expected


@pytest.mark.parametrize("level", ["bajo", "medio", "alto", "sin dato"])
def test_level_of(level: str) -> None:
    assert level_of(make_row(level)) == level


def test_summarize_empty() -> None:
    assert summarize([]) == "registros: 0 | bajo: 0 | medio: 0 | alto: 0 | sin dato: 0"


def test_summarize_mixed() -> None:
    rows = [make_row(level) for level in ["medio", "alto", "bajo", "medio", "sin dato"]]
    assert summarize(rows) == "registros: 5 | bajo: 1 | medio: 2 | alto: 1 | sin dato: 1"


def test_summarize_one_level() -> None:
    rows = [make_row("alto"), make_row("alto"), make_row("alto")]
    assert summarize(rows) == "registros: 3 | bajo: 0 | medio: 0 | alto: 3 | sin dato: 0"


@pytest.mark.parametrize(
    ("levels", "level", "expected"),
    [
        (["alto", "alto", "medio", "alto"], "alto", 2),
        (["medio", "alto", "medio", "alto", "alto", "alto"], "alto", 3),
        (["bajo", "medio"], "alto", 0),
        ([], "alto", 0),
        (["sin dato", "sin dato", "bajo", "sin dato"], "sin dato", 2),
    ],
)
def test_longest_streak(levels: list[str], level: str, expected: int) -> None:
    rows = [make_row(each) for each in levels]
    assert longest_streak(rows, level) == expected
