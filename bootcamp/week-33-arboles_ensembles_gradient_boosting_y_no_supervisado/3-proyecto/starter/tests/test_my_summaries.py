# Tus tests de la semana 25: sustituye este ejemplo por al menos 6 tests tuyos (paso 13).
# Usa los valores de tu dominio y las funciones de test_summaries.py (summary_table,
# means_table, data_rows, write): un resumen de tus etiquetas, una comparación entre dos
# archivos tuyos, la evolución de tus medidas por horas o por días...
from observatorio.core import Measurement, Series
from observatorio.core.frames import frame_of
from observatorio.core.summaries import summary


def test_example_summary_counts_the_missing_values() -> None:
    series = Series([Measurement("Norte", 12.5), Measurement("Norte", None)])
    assert summary(frame_of(series)).loc["Norte", "missing"] == 1
