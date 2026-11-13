# Tus tests de la semana 17: sustituye este ejemplo por al menos 6 tests tuyos (paso 14).
# Con archivos de tu dominio en tmp_path: replay, watch_file con éxito y con error, el
# orden de watch_files, el límite, y el comando vigilar con CliRunner.
import asyncio
from pathlib import Path

from observatorio.core import FileReport, watch_file


def test_example_missing_file_is_an_error(tmp_path: Path) -> None:
    report = asyncio.run(watch_file(tmp_path / "falta.txt"))
    assert report == FileReport(tmp_path / "falta.txt", error=report.error)
    assert report.error is not None
