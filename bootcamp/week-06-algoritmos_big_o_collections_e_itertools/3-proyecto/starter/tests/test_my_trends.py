# Tus tests de la semana 6: sustituye este ejemplo por al menos 6 tests tuyos (paso 13).
from observatorio.trends import jumps


def test_example_jumps_of_a_steady_series() -> None:
    assert jumps([5.0, 5.0, 5.0]) == [0.0, 0.0]
