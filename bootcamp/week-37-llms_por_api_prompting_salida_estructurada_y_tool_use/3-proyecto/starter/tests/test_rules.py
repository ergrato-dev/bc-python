import pytest

from observatorio.core.rules import classify, format_row, parse_line


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, "sin dato"),
        (0.0, "bajo"),
        (9.99, "bajo"),
        (10.0, "medio"),
        (49.9, "medio"),
        (50.0, "alto"),
        (612.0, "alto"),
    ],
)
def test_classify_levels_and_limits(value: float | None, expected: str) -> None:
    assert classify(value, 10.0, 50.0) == expected


def test_format_row_with_value() -> None:
    assert format_row("Norte", 12.54, "µg/m³", "medio") == "Norte               12.5 µg/m³ | medio"


def test_format_row_without_value() -> None:
    assert (
        format_row("Sur", None, "µg/m³", "sin dato") == "Sur                   sin dato | sin dato"
    )


def test_format_row_long_label_is_not_cut() -> None:
    assert (
        format_row("Estación Suroriental", 7.0, "µg/m³", "bajo")
        == "Estación Suroriental     7.0 µg/m³ | bajo"
    )


def test_parse_line_valid_with_comma_and_spaces() -> None:
    assert (
        parse_line(" Norte ; 12,5 ", "µg/m³", 10.0, 50.0)
        == "Norte               12.5 µg/m³ | medio"
    )


def test_parse_line_missing_value() -> None:
    assert parse_line("Sur;NA", "µg/m³", 10.0, 50.0) == "Sur                   sin dato | sin dato"


@pytest.mark.parametrize("line", ["Norte 12,5", "Norte;12;5", ";12,5", "   ;8", ""])
def test_parse_line_invalid_gives_none(line: str) -> None:
    assert parse_line(line, "µg/m³", 10.0, 50.0) is None
