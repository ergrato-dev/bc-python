import io

import pytest

from observatorio.__main__ import HIGH, LOW, UNIT, USAGE, main
from observatorio.report import longest_streak, summarize
from observatorio.rules import parse_line


def expected_output(lines: list[str]) -> str:
    """Lo que main debe escribir en stdout para estas líneas válidas: filas, resumen y racha."""
    rows = [parse_line(line, UNIT, LOW, HIGH) for line in lines]
    footer = [summarize(rows), f"racha más larga en alto: {longest_streak(rows, 'alto')}"]
    return "".join(f"{text}\n" for text in rows + footer)


def test_main_with_several_arguments(capsys: pytest.CaptureFixture[str]) -> None:
    lines = ["Norte;12,5", "Sur;80", "Centro;NA"]
    assert main(lines) == 0
    captured = capsys.readouterr()
    assert captured.out == expected_output(lines)
    assert captured.err == ""


def test_main_invalid_line_does_not_stop_the_rest(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["Norte;12,5", "Norte 12,5", "Sur;80"]) == 1
    captured = capsys.readouterr()
    assert captured.out == expected_output(["Norte;12,5", "Sur;80"])
    assert captured.err == "error: línea 2: 'Norte 12,5'\n"


def test_main_skips_comments_and_blank_lines_but_counts_them(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["# etiqueta;valor", "   ", "  Sur;8  ", "malo"]) == 1
    captured = capsys.readouterr()
    assert captured.out == expected_output(["Sur;8"])
    assert captured.err == "error: línea 4: 'malo'\n"


@pytest.mark.parametrize("flag", ["-h", "--ayuda"])
def test_main_help(flag: str, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([flag]) == 0
    assert capsys.readouterr().out == f"{USAGE}\n"


def test_main_unknown_option(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["-x", "Norte;12,5"]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == f"{USAGE}\n"


def test_main_reads_stdin(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # Qué: sustituye la entrada estándar por un texto en memoria.
    # Para qué: probar `observatorio < archivo` sin archivo ni teclado.
    monkeypatch.setattr("sys.stdin", io.StringIO("# cabecera\nNorte;12,5\n\nSur;NA\n"))
    assert main([]) == 0
    assert capsys.readouterr().out == expected_output(["Norte;12,5", "Sur;NA"])


def test_main_empty_stdin(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr("sys.stdin", io.StringIO(""))
    assert main([]) == 0
    assert capsys.readouterr().out == expected_output([])
