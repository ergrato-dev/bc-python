# Tus tests de la semana 9: sustituye este ejemplo por al menos 6 tests tuyos (paso 10).
# Importa solo de observatorio.core y usa datos de tu dominio.
from observatorio.core import Measurement, Series


def test_example_series_of_two_measurements() -> None:
    series = Series([Measurement("Norte", 12.5), Measurement("Sur", None)])
    assert series.values() == [12.5]
