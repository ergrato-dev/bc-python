# Tus tests de la semana 26: sustituye este ejemplo por al menos 6 tests tuyos (paso 13).
# Usa los valores de tu dominio y las funciones de test_columnar.py (summary_rows,
# parquet_of, cells, header, write): un Parquet de tus medidas, una consulta SQL que
# tenga sentido en tu dominio, el resumen de Polars frente al de pandas...
from observatorio.core import Measurement, Series
from observatorio.core.columnar import frame_of


def test_example_a_missing_value_is_null() -> None:
    series = Series([Measurement("Norte", 12.5), Measurement("Norte", None)])
    assert frame_of(series)["value"].null_count() == 1
