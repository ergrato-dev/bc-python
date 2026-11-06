# Tus tests de la semana 3: sustituye este ejemplo por al menos 6 tests tuyos (paso 10).
from observatorio.report import summarize


def test_example_summary_of_nothing() -> None:
    assert summarize([]) == "registros: 0 | bajo: 0 | medio: 0 | alto: 0 | sin dato: 0"
