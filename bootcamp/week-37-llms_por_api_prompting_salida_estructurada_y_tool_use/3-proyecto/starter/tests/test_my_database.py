# Tus tests de la semana 19: sustituye este ejemplo por al menos 6 tests tuyos (paso 15).
# Con medidas de tu dominio y las fixtures de db_fixtures.py (session, engine, db_env):
# save_series y load_series de ida y vuelta, el orden de las medidas, list_loads,
# label_stats con valores que faltan, delete_load y un comando de la CLI con CliRunner.
from sqlalchemy.orm import Session

from observatorio.core import Measurement, Series, load_series, save_series


def test_example_a_series_comes_back_the_same(session: Session) -> None:
    series = Series([Measurement("Norte", 12.5), Measurement("Sur", None)])
    load = save_series(session, "ejemplo.txt", series)
    assert load_series(session, load.id) == series
