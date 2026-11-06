# Tus tests de la semana 8: sustituye este ejemplo por al menos 6 tests tuyos (paso 11).
# Importa solo de observatorio.core: así pruebas la API pública, no los módulos de dentro.
from pathlib import Path

from observatorio.core import read_data, records_of, summary_data


def test_example_csv_to_summary(tmp_path: Path) -> None:
    path = tmp_path / "medidas.csv"
    path.write_text("etiqueta;valor\nSur;8\nNorte;12,5\n", encoding="utf-8")
    summary = summary_data(records_of(read_data(path)))
    assert summary == {"registros": 2, "con_valor": 2, "mediana": 10.2, "mayor_salto": 4.5}
