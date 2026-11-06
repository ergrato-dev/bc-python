# Tus tests de la semana 7: sustituye este ejemplo por al menos 6 tests tuyos (paso 11).
from pathlib import Path

from observatorio.storage import read_lines


def test_example_read_lines_of_one_line(tmp_path: Path) -> None:
    path = tmp_path / "una.txt"
    path.write_text("Sur;8", encoding="utf-8")
    assert read_lines(path) == ["Sur;8"]
