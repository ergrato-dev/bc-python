import pytest

from observatorio.groups import Record
from observatorio.trends import (
    jumps,
    largest_jump,
    median,
    most_common_labels,
    moving_average,
    values_of,
)


def test_values_of_keeps_order_and_skips_none() -> None:
    records = [("Norte", 12.5), ("Centro", None), ("Sur", 8.0), ("Norte", 48.9)]
    assert values_of(records) == [12.5, 8.0, 48.9]


def test_values_of_empty() -> None:
    assert values_of([]) == []


def test_most_common_labels_counts_records_without_value() -> None:
    records = [("Sur", 8.0), ("Norte", 1.0), ("Norte", None), ("Norte", 3.0), ("Sur", 9.5)]
    assert most_common_labels(records, 2) == [("Norte", 3), ("Sur", 2)]


def test_most_common_labels_ties_keep_first_seen_order() -> None:
    records: list[Record] = [
        ("Este", 1.0),
        ("Sur", 2.0),
        ("Oeste", 3.0),
        ("Sur", 4.0),
        ("Este", 5.0),
    ]
    assert most_common_labels(records, 3) == [("Este", 2), ("Sur", 2), ("Oeste", 1)]


@pytest.mark.parametrize("n", [0, 1, 5])
def test_most_common_labels_returns_at_most_n(n: int) -> None:
    records: list[Record] = [("A", 1.0), ("B", 2.0), ("A", 3.0)]
    assert most_common_labels(records, n) == [("A", 2), ("B", 1)][:n]


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([12.5], 12.5),
        ([8.0, 61.0, 12.5], 12.5),
        ([8.0, 61.0, 12.5, 9.5], 11.0),
        ([5.0, 5.0, 5.0, 1.0], 5.0),
    ],
)
def test_median(values: list[float], expected: float) -> None:
    assert median(values) == pytest.approx(expected)


def test_median_does_not_change_values() -> None:
    values = [3.0, 1.0, 2.0]
    median(values)
    assert values == [3.0, 1.0, 2.0]


def test_median_of_nothing_fails() -> None:
    with pytest.raises(ValueError):
        median([])


def test_moving_average_window_three() -> None:
    values = [10.0, 20.0, 30.0, 40.0, 50.0]
    assert moving_average(values, 3) == pytest.approx([20.0, 30.0, 40.0])


def test_moving_average_window_one_gives_the_values() -> None:
    assert moving_average([12.5, 8.0, 48.9], 1) == pytest.approx([12.5, 8.0, 48.9])


def test_moving_average_fewer_values_than_window() -> None:
    assert moving_average([10.0, 20.0], 3) == []


def test_moving_average_window_equal_to_length() -> None:
    assert moving_average([10.0, 20.0, 60.0], 3) == pytest.approx([30.0])


@pytest.mark.parametrize("window", [0, -2])
def test_moving_average_rejects_small_window(window: int) -> None:
    with pytest.raises(ValueError):
        moving_average([1.0, 2.0], window)


def test_moving_average_is_linear() -> None:
    # Qué: 200 000 valores con ventana de 1 000.
    # Para qué: si cada media vuelve a sumar su ventana entera con un bucle, son 200
    # millones de sumas y el test tarda unos 10 s; sumando y restando, unas centésimas.
    values = [float(n % 100) for n in range(200_000)]
    averages = moving_average(values, 1_000)
    assert len(averages) == 199_001
    assert averages[0] == pytest.approx(49.5)


def test_jumps() -> None:
    assert jumps([10.0, 15.0, 12.0, 12.0]) == pytest.approx([5.0, -3.0, 0.0])


@pytest.mark.parametrize("values", [[], [7.0]])
def test_jumps_needs_two_values(values: list[float]) -> None:
    assert jumps(values) == []


def test_largest_jump_keeps_the_sign() -> None:
    assert largest_jump([10.0, 15.0, 7.0, 10.0]) == pytest.approx(-8.0)


def test_largest_jump_tie_gives_the_first() -> None:
    assert largest_jump([10.0, 14.0, 10.0]) == pytest.approx(4.0)


@pytest.mark.parametrize("values", [[], [7.0]])
def test_largest_jump_without_jumps(values: list[float]) -> None:
    assert largest_jump(values) == 0.0
