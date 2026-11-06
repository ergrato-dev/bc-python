import pytest

from observatorio.__main__ import HIGH, LOW, UNIT, USAGE, main
from observatorio.rules import parse_line


def test_main_with_one_argument(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["Norte;12,5"]) == 0
    assert capsys.readouterr().out == f"{parse_line('Norte;12,5', UNIT, LOW, HIGH)}\n"


def test_main_invalid_line_goes_to_stderr(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["Norte 12,5"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "error: línea inválida: 'Norte 12,5'\n"


def test_main_too_many_arguments(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["Norte", "12,5"]) == 2
    assert capsys.readouterr().err == f"{USAGE}\n"


@pytest.mark.parametrize("flag", ["-h", "--ayuda"])
def test_main_help(flag: str, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([flag]) == 0
    assert capsys.readouterr().out == f"{USAGE}\n"


def test_main_without_arguments_reads_input(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # Qué: sustituye input() por una función que devuelve una línea fija.
    # Para qué: probar la lectura por teclado sin teclado.
    monkeypatch.setattr("builtins.input", lambda prompt: "Sur;NA")
    assert main([]) == 0
    assert capsys.readouterr().out == f"{parse_line('Sur;NA', UNIT, LOW, HIGH)}\n"
