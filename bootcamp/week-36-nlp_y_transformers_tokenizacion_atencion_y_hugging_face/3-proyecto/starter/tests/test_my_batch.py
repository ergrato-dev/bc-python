# Tus tests de la semana 16: sustituye este ejemplo por al menos 6 tests tuyos (paso 14).
# Con archivos de tu dominio en tmp_path: report_file con éxito y con error, el orden de
# report_files, hilos frente a procesos, y el comando lote con CliRunner.
from pathlib import Path

from observatorio.core import FileReport, report_file


def test_example_missing_file_is_an_error(tmp_path: Path) -> None:
    report = report_file(tmp_path / "falta.txt")
    assert report == FileReport(tmp_path / "falta.txt", error=report.error)
    assert report.error is not None
