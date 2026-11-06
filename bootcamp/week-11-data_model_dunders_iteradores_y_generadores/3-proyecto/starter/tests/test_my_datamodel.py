# Tus tests de la semana 11: sustituye este ejemplo por al menos 6 tests tuyos (paso 12).
# Importa solo de observatorio.core y usa datos de tu dominio.
from observatorio.core import Series, running_mean


def test_example_running_mean_of_a_series() -> None:
    series = Series.from_lines(["Norte;10", "Sur;NA", "Norte;20"])
    assert list(running_mean(series.values())) == [10.0, 15.0]
