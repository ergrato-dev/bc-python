# Tus tests de la semana 29: sustituye este ejemplo por al menos 6 tests tuyos (paso 11).
# Usa las etiquetas y los valores de tu dominio y las funciones de test_etl.py (save,
# values, snapshot_of): una carga de tu dominio extraída en su orden, un nivel en cada
# borde de tu escala, una etiqueta con coma o comillas en la instantánea, la huella que
# cambia con un solo valor, `extraer` de una sola carga...
from pathlib import Path

from test_etl import snapshot_of

from observatorio.core.etl import write_snapshot


def test_example_a_missing_value_is_an_empty_cell(tmp_path: Path) -> None:
    path = tmp_path / "instantanea.csv"
    write_snapshot(snapshot_of((1, 0, "Sur", float("nan"))), path)
    assert path.read_text(encoding="utf-8").splitlines()[1] == "1,0,Sur,,sin dato"
