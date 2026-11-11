# Tus tests de la semana 27: sustituye este ejemplo por al menos 6 tests tuyos (paso 11).
# Usa los valores de tu dominio y las funciones de test_charts.py (table_of, legend_of,
# saved, write): tus etiquetas en la leyenda, un periodo sin dato de tu dominio, un SVG de
# tus medidas que sale igual dos veces...
from test_charts import legend_of, table_of

from observatorio.core import Measurement, Series
from observatorio.core.charts import evolution_figure


def test_example_the_legend_names_my_labels() -> None:
    table = table_of(Series([Measurement("Norte", 12.5), Measurement("Sur", 8.0)]))
    assert legend_of(evolution_figure(table, "título")) == ["Norte", "Sur"]
