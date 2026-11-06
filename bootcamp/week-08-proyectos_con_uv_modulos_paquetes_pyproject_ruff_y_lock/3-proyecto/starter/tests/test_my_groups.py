# Tus tests de la semana 5: sustituye este ejemplo por al menos 6 tests tuyos (paso 13).
from observatorio.groups import distinct_labels


def test_example_distinct_labels_ignores_repeats() -> None:
    assert distinct_labels([("Norte", 1.0), ("Norte", 2.0)]) == {"Norte"}
