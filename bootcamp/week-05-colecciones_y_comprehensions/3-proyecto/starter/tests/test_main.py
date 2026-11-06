import io

import pytest

from observatorio.__main__ import HIGH, LOW, UNIT, USAGE, main

TOP = 3
from observatorio.analysis import count_level, share
from observatorio.groups import distinct_labels, label_means, parse_record, top, values_by_label
from observatorio.record import describe_record
from observatorio.report import longest_streak, summarize
from observatorio.rules import parse_line


def expected_output(lines: list[str]) -> str:
    """Lo que main debe escribir en stdout para estas líneas válidas: filas, resumen, racha,
    porcentaje, etiquetas distintas y medias más altas."""
    rows: list[str] = []
    records: list[tuple[str, float | None]] = []
    for line in lines:
        row = parse_line(line, UNIT, LOW, HIGH)
        record = parse_record(line)
        # Estas líneas son válidas; además, así mypy sabe que no son None.
        assert row is not None and record is not None
        rows.append(row)
        records.append(record)
    best = top(label_means(values_by_label(records)), TOP)
    footer = [
        summarize(rows),
        f"racha más larga en alto: {longest_streak(rows, 'alto')}",
        f"en alto: {share(count_level(rows, 'alto'), len(rows))}",
        f"etiquetas distintas: {len(distinct_labels(records))}",
        "medias más altas:",
    ]
    footer += [f"  {describe_record(label, mean, UNIT)}" for label, mean in best]
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


def test_main_reports_means_of_repeated_labels(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["Norte;10", "Sur;NA", "Norte;20", "Este;5"]) == 0
    out = capsys.readouterr().out
    assert out.endswith(
        f"etiquetas distintas: 3\nmedias más altas:\n  Norte: 15.0 {UNIT}\n  Este: 5.0 {UNIT}\n"
    )


def test_main_shows_at_most_three_means(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["A;1", "B;2", "C;3", "D;4"]) == 0
    out = capsys.readouterr().out
    assert out.endswith(f"medias más altas:\n  D: 4.0 {UNIT}\n  C: 3.0 {UNIT}\n  B: 2.0 {UNIT}\n")


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
