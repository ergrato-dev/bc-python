# Tus tests de la semana 10: sustituye este ejemplo por al menos 6 tests tuyos (paso 12).
# Importa solo de observatorio.core y usa datos de tu dominio.
from observatorio.core import LinesSource, Series


def test_example_series_from_a_lines_source() -> None:
    source = LinesSource(["Norte;12,5", "Sur;NA"])
    assert Series.from_lines(source.lines()).values() == [12.5]
