# Tus tests de la semana 4: sustituye este ejemplo por al menos 6 tests tuyos (paso 10).
from observatorio.core.analysis import share


def test_example_share_of_one_half() -> None:
    assert share(1, 2) == "50.0 %"
