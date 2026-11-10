# Tus tests de la semana 23: sustituye este ejemplo por al menos 6 tests tuyos (paso 14).
# Usa los valores de tu dominio y las funciones de test_arrays.py (floats, stats_rows,
# write): un atípico de verdad en tus datos, un histograma con tus intervalos, la media
# de tus etiquetas con group_means, que values_array respete el orden...
import math

import numpy as np

from observatorio.core import Measurement, Series
from observatorio.core.arrays import values_array


def test_example_values_array_puts_nan_for_na() -> None:
    values = values_array(Series([Measurement("Norte", None), Measurement("Sur", 8.0)]))
    assert math.isnan(values[0])
    np.testing.assert_array_equal(values[1:], [8.0])
