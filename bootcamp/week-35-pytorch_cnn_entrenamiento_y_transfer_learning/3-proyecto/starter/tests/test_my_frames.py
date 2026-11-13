# Tus tests de la semana 24: sustituye este ejemplo por al menos 6 tests tuyos (paso 13).
# Usa los valores de tu dominio y las funciones de test_frames.py (table, frame_rows,
# write): tus etiquetas con select, los bordes de tu escala con with_levels, empates en
# by_value, un archivo de tu dominio que vuelve igual tras write_frame...
import pandas as pd

from observatorio.core import Measurement, Series
from observatorio.core.frames import frame_of, select


def test_example_select_keeps_the_position_of_each_row() -> None:
    frame = frame_of(Series([Measurement("Norte", 12.5), Measurement("Sur", 8.0)]))
    pd.testing.assert_series_equal(
        select(frame, labels=["Sur"])["value"],
        pd.Series([8.0], index=pd.Index([2], name="position"), name="value"),
    )
