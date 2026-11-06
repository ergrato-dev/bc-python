"""Tests de las fuentes: Source, LinesSource, FileSource, TextFile, CsvFile y open_file (semana 10)."""

import dataclasses
from abc import ABC
from pathlib import Path

import pytest

import observatorio.__main__ as entry
from observatorio.core import (
    CsvFile,
    DataFileError,
    FileSource,
    LinesSource,
    Source,
    TextFile,
    open_file,
    read_data,
)

LINES = ["Norte;12,5", "Sur;NA"]


def write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


# --- Source: el Protocol ---


def test_lines_source_is_a_source() -> None:
    assert isinstance(LinesSource(LINES), Source)


def test_file_sources_are_sources() -> None:
    assert isinstance(TextFile(Path("medidas.txt")), Source)
    assert isinstance(CsvFile(Path("medidas.csv")), Source)


def test_any_object_with_lines_is_a_source() -> None:
    class Fixed:
        def lines(self) -> list[str]:
            return ["Norte;1"]

    assert isinstance(Fixed(), Source)
    assert not isinstance(object(), Source)


def test_lines_source_does_not_inherit_from_source() -> None:
    assert Source not in LinesSource.__mro__


# --- LinesSource ---


def test_lines_source_gives_its_lines() -> None:
    assert LinesSource(LINES).lines() == LINES


def test_lines_source_gives_a_copy() -> None:
    source = LinesSource(["Norte;1"])
    lines = source.lines()
    lines.append("Sur;2")
    assert source.lines() == ["Norte;1"]


def test_lines_source_is_frozen() -> None:
    source = LinesSource(LINES)
    with pytest.raises(dataclasses.FrozenInstanceError):
        source.data = []  # type: ignore[misc]


def test_lines_source_repr_is_generated() -> None:
    assert repr(LinesSource(["Norte;1"])) == "LinesSource(data=['Norte;1'])"


# --- FileSource: la base abstracta ---


def test_file_source_cannot_be_created() -> None:
    with pytest.raises(TypeError, match="abstract"):
        FileSource(Path("medidas.txt"))  # type: ignore[abstract]


def test_a_subclass_without_lines_cannot_be_created() -> None:
    class Forgetful(FileSource):
        pass

    with pytest.raises(TypeError, match="lines"):
        Forgetful(Path("medidas.txt"))  # type: ignore[abstract]


def test_file_sources_inherit_from_file_source() -> None:
    assert issubclass(FileSource, ABC)
    assert issubclass(TextFile, FileSource)
    assert issubclass(CsvFile, FileSource)


def test_file_sources_keep_their_path() -> None:
    source = TextFile(Path("medidas.txt"))
    assert source.path == Path("medidas.txt")
    assert repr(source).startswith("TextFile(path=")


def test_file_sources_compare_class_and_path() -> None:
    path = Path("medidas")
    # Anotado como FileSource: con un CsvFile, mypy --strict avisaría de que TextFile y
    # CsvFile nunca pueden ser iguales (comparison-overlap), que es justo lo que se prueba.
    other: FileSource = CsvFile(path)
    assert TextFile(path) == TextFile(path)
    assert TextFile(path) != other
    assert TextFile(path) != TextFile(Path("otras"))


def test_file_sources_are_frozen_and_hashable() -> None:
    path = Path("medidas")
    with pytest.raises(dataclasses.FrozenInstanceError):
        TextFile(path).path = Path("otras")  # type: ignore[misc]
    assert len({TextFile(path), TextFile(path), CsvFile(path)}) == 2


def test_creating_a_file_source_does_not_read_it(tmp_path: Path) -> None:
    source = TextFile(tmp_path / "no-existe.txt")
    with pytest.raises(DataFileError, match="no existe"):
        source.lines()


# --- TextFile y CsvFile ---


def test_text_file_reads_its_lines(tmp_path: Path) -> None:
    path = write(tmp_path / "medidas.txt", "Norte;12,5\nSur;NA\n")
    assert TextFile(path).lines() == LINES


def test_csv_file_reads_its_rows(tmp_path: Path) -> None:
    path = write(tmp_path / "medidas.csv", "etiqueta;valor\nNorte;12,5\nSur;NA\n")
    assert CsvFile(path).lines() == LINES


def test_csv_file_checks_the_header(tmp_path: Path) -> None:
    path = write(tmp_path / "medidas.csv", "nombre;dato\nNorte;12,5\n")
    with pytest.raises(DataFileError, match="cabecera"):
        CsvFile(path).lines()


# --- open_file ---


@pytest.mark.parametrize(
    ("name", "kind"),
    [
        ("medidas.csv", CsvFile),
        ("MEDIDAS.CSV", CsvFile),
        ("medidas.txt", TextFile),
        ("medidas", TextFile),
    ],
)
def test_open_file_chooses_by_suffix(name: str, kind: type[FileSource]) -> None:
    source = open_file(Path(name))
    assert type(source) is kind
    assert source.path == Path(name)


@pytest.mark.parametrize(
    ("name", "text"),
    [("medidas.txt", "Norte;12,5\nSur;NA\n"), ("medidas.csv", "etiqueta;valor\nNorte;12,5\n")],
)
def test_open_file_reads_like_read_data(tmp_path: Path, name: str, text: str) -> None:
    path = write(tmp_path / name, text)
    assert open_file(path).lines() == read_data(path)


# --- main ---


def test_main_reads_files_through_open_file(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # Sustituye open_file en __main__ por una fuente en memoria: si main la usa, el
    # archivo no hace falta. raising=False: si main aún no importa open_file, el test
    # falla en el assert y no al preparar.
    monkeypatch.setattr(entry, "open_file", lambda path: LinesSource(["Norte;12,5"]), raising=False)
    assert entry.main(["-f", "no-existe.csv"]) == 0
    assert "Norte" in capsys.readouterr().out
