import json
from pathlib import Path

import pytest

from observatorio.groups import Record
from observatorio.storage import (
    DataFileError,
    read_csv,
    read_data,
    read_json,
    read_lines,
    summary_data,
    write_json,
)

# tmp_path es una carpeta temporal nueva para cada test, que pytest crea y borra:
# los tests escriben archivos sin ensuciar tu proyecto.


def test_read_lines_without_line_breaks(tmp_path: Path) -> None:
    path = tmp_path / "medidas.txt"
    path.write_text("Norte;12,5\nSur;8\n", encoding="utf-8")
    assert read_lines(path) == ["Norte;12,5", "Sur;8"]


def test_read_lines_keeps_blank_lines_and_comments(tmp_path: Path) -> None:
    path = tmp_path / "medidas.txt"
    path.write_text("# cabecera\n\nSur;8", encoding="utf-8")
    assert read_lines(path) == ["# cabecera", "", "Sur;8"]


def test_read_lines_reads_utf8(tmp_path: Path) -> None:
    path = tmp_path / "medidas.txt"
    path.write_text("Peñalara;3,5\n", encoding="utf-8")
    assert read_lines(path) == ["Peñalara;3,5"]


def test_read_lines_empty_file(tmp_path: Path) -> None:
    path = tmp_path / "vacio.txt"
    path.write_text("", encoding="utf-8")
    assert read_lines(path) == []


def test_read_lines_missing_file(tmp_path: Path) -> None:
    path = tmp_path / "no-esta.txt"
    with pytest.raises(DataFileError, match="no existe el archivo") as caught:
        read_lines(path)
    assert str(caught.value) == f"no existe el archivo {path}"
    # raise ... from: la excepción original queda guardada como causa.
    assert isinstance(caught.value.__cause__, FileNotFoundError)


def test_read_lines_folder(tmp_path: Path) -> None:
    with pytest.raises(DataFileError, match="es una carpeta"):
        read_lines(tmp_path)


def test_read_lines_not_utf8(tmp_path: Path) -> None:
    path = tmp_path / "latin1.txt"
    path.write_bytes("Peñalara;3,5\n".encode("latin-1"))
    with pytest.raises(DataFileError, match="no es texto UTF-8") as caught:
        read_lines(path)
    assert isinstance(caught.value.__cause__, UnicodeDecodeError)


def test_data_file_error_is_an_exception() -> None:
    assert issubclass(DataFileError, Exception)


def test_read_csv_skips_the_header(tmp_path: Path) -> None:
    path = tmp_path / "medidas.csv"
    path.write_text("etiqueta;valor\nNorte;12,5\nCentro;NA\n", encoding="utf-8")
    assert read_csv(path) == ["Norte;12,5", "Centro;NA"]


def test_read_csv_understands_quotes(tmp_path: Path) -> None:
    path = tmp_path / "medidas.csv"
    path.write_text('etiqueta;valor\n"Norte";"12,5"\n', encoding="utf-8")
    assert read_csv(path) == ["Norte;12,5"]


def test_read_csv_keeps_wrong_rows_for_process_lines(tmp_path: Path) -> None:
    path = tmp_path / "medidas.csv"
    path.write_text("etiqueta;valor\nNorte\nSur;8;9\n", encoding="utf-8")
    assert read_csv(path) == ["Norte", "Sur;8;9"]


def test_read_csv_only_header(tmp_path: Path) -> None:
    path = tmp_path / "medidas.csv"
    path.write_text("etiqueta;valor\n", encoding="utf-8")
    assert read_csv(path) == []


def test_read_csv_empty_file(tmp_path: Path) -> None:
    path = tmp_path / "medidas.csv"
    path.write_text("", encoding="utf-8")
    with pytest.raises(DataFileError, match="está vacío"):
        read_csv(path)


def test_read_csv_wrong_header(tmp_path: Path) -> None:
    path = tmp_path / "medidas.csv"
    path.write_text("zona;medida\nNorte;12,5\n", encoding="utf-8")
    with pytest.raises(DataFileError) as caught:
        read_csv(path)
    assert str(caught.value) == f"cabecera inesperada en {path}: zona;medida"


def test_read_csv_missing_file(tmp_path: Path) -> None:
    with pytest.raises(DataFileError, match="no existe el archivo"):
        read_csv(tmp_path / "no-esta.csv")


def test_read_data_uses_csv_for_csv_files(tmp_path: Path) -> None:
    path = tmp_path / "medidas.CSV"
    path.write_text("etiqueta;valor\nSur;8\n", encoding="utf-8")
    assert read_data(path) == ["Sur;8"]


def test_read_data_uses_lines_for_other_files(tmp_path: Path) -> None:
    path = tmp_path / "medidas.txt"
    path.write_text("etiqueta;valor\nSur;8\n", encoding="utf-8")
    assert read_data(path) == ["etiqueta;valor", "Sur;8"]


def test_summary_data() -> None:
    records: list[Record] = [("Norte", 10.0), ("Sur", None), ("Norte", 25.0), ("Este", 12.04)]
    assert summary_data(records) == {
        "registros": 4,
        "con_valor": 3,
        "mediana": 12.0,
        "mayor_salto": 15.0,
    }


def test_summary_data_keeps_the_sign_of_the_jump() -> None:
    assert summary_data([("Norte", 30.0), ("Sur", 8.0)])["mayor_salto"] == -22.0


def test_summary_data_without_values() -> None:
    assert summary_data([("Centro", None)]) == {
        "registros": 1,
        "con_valor": 0,
        "mediana": None,
        "mayor_salto": None,
    }


def test_summary_data_is_json_ready() -> None:
    text = json.dumps(summary_data([("Norte", 10.0)]))
    assert json.loads(text) == {"registros": 1, "con_valor": 1, "mediana": 10.0, "mayor_salto": 0.0}


def test_write_json_writes_indented_utf8(tmp_path: Path) -> None:
    path = tmp_path / "resumen.json"
    write_json({"zona": "Peñalara", "mediana": None}, path)
    assert path.read_text(encoding="utf-8") == '{\n  "zona": "Peñalara",\n  "mediana": null\n}\n'


def test_write_json_replaces_the_file(tmp_path: Path) -> None:
    path = tmp_path / "resumen.json"
    write_json({"registros": 1}, path)
    write_json({"registros": 2}, path)
    assert json.loads(path.read_text(encoding="utf-8")) == {"registros": 2}


def test_write_json_missing_folder(tmp_path: Path) -> None:
    path = tmp_path / "no-esta" / "resumen.json"
    with pytest.raises(DataFileError) as caught:
        write_json({"registros": 1}, path)
    assert str(caught.value) == f"no se puede escribir {path}"
    assert isinstance(caught.value.__cause__, FileNotFoundError)


def test_json_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "resumen.json"
    data = summary_data([("Norte", 10.0), ("Sur", 30.0), ("Este", None)])
    write_json(data, path)
    assert read_json(path) == data


def test_read_json_invalid(tmp_path: Path) -> None:
    path = tmp_path / "roto.json"
    path.write_text('{\n  "registros": 1,\n}\n', encoding="utf-8")
    with pytest.raises(DataFileError) as caught:
        read_json(path)
    assert str(caught.value) == f"JSON no válido en {path}, línea 2"
    assert isinstance(caught.value.__cause__, json.JSONDecodeError)


def test_read_json_not_an_object(tmp_path: Path) -> None:
    path = tmp_path / "lista.json"
    path.write_text("[1, 2]", encoding="utf-8")
    with pytest.raises(DataFileError, match="no contiene un objeto JSON"):
        read_json(path)


def test_read_json_missing_file(tmp_path: Path) -> None:
    with pytest.raises(DataFileError, match="no existe el archivo"):
        read_json(tmp_path / "no-esta.json")
