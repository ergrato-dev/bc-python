# Tus tests de la semana 14: sustituye este ejemplo por al menos 6 tests tuyos (paso 15).
# Importa solo de observatorio.core (y de pytest, hypothesis o unittest.mock) y usa
# datos de tu dominio.
from observatorio.core import Series


def test_example_series_fixture_has_three_measurements(series: Series) -> None:
    assert len(series) == 3
