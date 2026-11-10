import pytest

from observatorio.core.record import describe_record, is_valid, parse_value


def test_parse_value_with_dot() -> None:
    assert parse_value("12.5") == 12.5


def test_parse_value_with_comma_and_spaces() -> None:
    assert parse_value(" 12,5 ") == 12.5


@pytest.mark.parametrize("text", ["", "NA", "N/A", "-", "  NA  "])
def test_parse_value_missing_markers_give_none(text: str) -> None:
    assert parse_value(text) is None


def test_parse_value_zero_is_a_real_value() -> None:
    assert parse_value("0") == 0.0


def test_describe_record_rounds_to_one_decimal() -> None:
    assert describe_record("Estación Norte", 12.54, "µg/m³") == "Estación Norte: 12.5 µg/m³"


def test_describe_record_without_value() -> None:
    assert describe_record("Estación Norte", None, "µg/m³") == "Estación Norte: sin dato"


def test_is_valid_includes_the_limits() -> None:
    assert is_valid(0.0, 0.0, 500.0)
    assert is_valid(500.0, 0.0, 500.0)


def test_is_valid_rejects_out_of_range_and_none() -> None:
    assert not is_valid(-1.0, 0.0, 500.0)
    assert not is_valid(None, 0.0, 500.0)
