import pytest

from types_lab import (
    digits_of_power_of_two,
    floats_are_equal,
    is_missing,
    to_float,
    to_int,
    type_name,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [(3, "int"), (3.0, "float"), ("3", "str"), (True, "bool"), (None, "NoneType")],
)
def test_type_name(value: object, expected: str) -> None:
    assert type_name(value) == expected


def test_to_int_ignores_surrounding_spaces() -> None:
    assert to_int(" 42 ") == 42


def test_to_int_rejects_decimal_text() -> None:
    # int("4.5") falla: Python no adivina si redondear o truncar.
    with pytest.raises(ValueError):
        to_int("4.5")


def test_to_float_with_dot() -> None:
    assert to_float("3.5") == 3.5


def test_to_float_with_comma() -> None:
    assert to_float("3,5") == 3.5


def test_float_sum_is_not_exact_with_double_equals() -> None:
    # Este test documenta el comportamiento de los float: no lo cambies.
    assert 0.1 + 0.2 != 0.3


def test_floats_are_equal_tolerates_rounding() -> None:
    assert floats_are_equal(0.1 + 0.2, 0.3)


def test_floats_are_equal_detects_real_differences() -> None:
    assert not floats_are_equal(0.3, 0.31)


def test_digits_of_power_of_two() -> None:
    assert digits_of_power_of_two(10) == 4  # 1024
    assert digits_of_power_of_two(100) == 31  # int no tiene límite de tamaño


@pytest.mark.parametrize("value", [0, "", False, 0.0])
def test_empty_values_are_not_missing(value: object) -> None:
    assert not is_missing(value)


def test_none_is_missing() -> None:
    assert is_missing(None)
