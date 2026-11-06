# Tus tests de la semana 12: sustituye este ejemplo por al menos 6 tests tuyos (paso 14).
# Importa solo de observatorio.core y usa datos de tu dominio.
from observatorio.core import Series, above


def test_example_where_above() -> None:
    series = Series.from_lines(["Norte;10", "Sur;NA", "Norte;60"])
    assert len(series.where(above(50.0))) == 1
