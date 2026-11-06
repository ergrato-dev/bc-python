import pytest

from observatorio.groups import (
    LEVELS,
    distinct_labels,
    label_means,
    level_counts,
    parse_record,
    records_of,
    top,
    values_by_label,
)
from observatorio.rules import format_row


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("Norte;12,5", ("Norte", 12.5)),
        ("  Sur  ; 8 ", ("Sur", 8.0)),
        ("Centro;NA", ("Centro", None)),
        ("Norte 12,5", None),
        ("a;b;c", None),
        ("  ;12", None),
    ],
)
def test_parse_record(line: str, expected: tuple[str, float | None] | None) -> None:
    assert parse_record(line) == expected


def test_records_of_skips_comments_blank_and_invalid() -> None:
    lines = ["# cabecera", " Norte;12,5 ", "", "malo", "Sur;NA"]
    assert records_of(lines) == [("Norte", 12.5), ("Sur", None)]


def test_records_of_accepts_any_iterable() -> None:
    assert records_of(iter(["Norte;1", "Sur;2"])) == [("Norte", 1.0), ("Sur", 2.0)]


def test_records_of_empty() -> None:
    assert records_of([]) == []


def test_level_counts() -> None:
    rows = [format_row("Norte", 1.0, "u", level) for level in ["alto", "bajo", "alto", "sin dato"]]
    assert level_counts(rows) == {"bajo": 1, "medio": 0, "alto": 2, "sin dato": 1}


def test_level_counts_keeps_order_and_zeros() -> None:
    # Qué: compara también el orden de las claves, que == entre diccionarios no mira.
    # Para qué: summarize y los informes las recorren en el orden de LEVELS.
    counts = level_counts([])
    assert list(counts) == list(LEVELS)
    assert set(counts.values()) == {0}


def test_values_by_label_groups_and_skips_none() -> None:
    records = [("Norte", 12.5), ("Sur", 8.0), ("Centro", None), ("Norte", 48.9), ("Sur", 9.5)]
    groups = values_by_label(records)
    assert groups == {"Norte": [12.5, 48.9], "Sur": [8.0, 9.5]}
    assert list(groups) == ["Norte", "Sur"]


def test_values_by_label_empty() -> None:
    assert values_by_label([]) == {}


def test_values_by_label_does_not_change_records() -> None:
    records: list[tuple[str, float | None]] = [("Norte", 1.0), ("Norte", 2.0)]
    values_by_label(records)
    assert records == [("Norte", 1.0), ("Norte", 2.0)]


def test_label_means() -> None:
    means = label_means({"Norte": [12.5, 48.9], "Sur": [8.0]})
    assert means == {"Norte": pytest.approx(30.7), "Sur": 8.0}


def test_label_means_empty() -> None:
    assert label_means({}) == {}


def test_top_orders_from_highest() -> None:
    means = {"Norte": 30.7, "Sur": 8.75, "Oriente": 55.1, "Occidente": 61.0}
    assert top(means, 3) == [("Occidente", 61.0), ("Oriente", 55.1), ("Norte", 30.7)]


def test_top_ties_in_alphabetical_order() -> None:
    assert top({"Sur": 5.0, "Este": 5.0, "Norte": 9.0}, 3) == [
        ("Norte", 9.0),
        ("Este", 5.0),
        ("Sur", 5.0),
    ]


@pytest.mark.parametrize(("n", "expected_len"), [(0, 0), (1, 1), (2, 2), (10, 2)])
def test_top_length(n: int, expected_len: int) -> None:
    assert len(top({"Norte": 1.0, "Sur": 2.0}, n)) == expected_len


def test_top_does_not_change_means() -> None:
    means = {"Norte": 1.0, "Sur": 2.0}
    top(means, 1)
    assert list(means.items()) == [("Norte", 1.0), ("Sur", 2.0)]


def test_distinct_labels() -> None:
    records = [("Norte", 12.5), ("Centro", None), ("Norte", 48.9)]
    assert distinct_labels(records) == {"Norte", "Centro"}


def test_distinct_labels_empty() -> None:
    assert distinct_labels([]) == set()
