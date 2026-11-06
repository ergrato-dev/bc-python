import io
import json
from pathlib import Path

import pytest

from observatorio.__main__ import HIGH, LOW, UNIT, USAGE, main
from observatorio.core import (
    count_level,
    describe_record,
    distinct_labels,
    label_means,
    largest_jump,
    longest_streak,
    median,
    most_common_labels,
    moving_average,
    parse_line,
    parse_record,
    share,
    summarize,
    top,
    values_by_label,
    values_of,
)

TOP = 3
WINDOW = 3


def expected_output(lines: list[str]) -> str:
    """Lo que main debe escribir en stdout para estas líneas válidas: filas, resumen, racha,
    porcentaje, etiquetas distintas, medias más altas, más frecuentes y tendencias."""
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
    footer.append("más frecuentes:")
    footer += [f"  {label}: {count}" for label, count in most_common_labels(records, TOP)]
    values = values_of(records)
    if values:
        averages = " · ".join(f"{average:.1f}" for average in moving_average(values, WINDOW))
        footer += [
            f"mediana: {median(values):.1f} {UNIT}",
            f"media móvil ({WINDOW}): {averages}",
            f"mayor salto: {largest_jump(values):+.1f} {UNIT}",
        ]
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
    assert (
        f"etiquetas distintas: 3\nmedias más altas:\n  Norte: 15.0 {UNIT}\n  Este: 5.0 {UNIT}\n"
        in out
    )


def test_main_shows_at_most_three_means(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["A;1", "B;2", "C;3", "D;4"]) == 0
    out = capsys.readouterr().out
    assert f"medias más altas:\n  D: 4.0 {UNIT}\n  C: 3.0 {UNIT}\n  B: 2.0 {UNIT}\n" in out


def test_main_reports_trends(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["Norte;10", "Sur;20", "Norte;NA", "Norte;60", "Sur;30"]) == 0
    out = capsys.readouterr().out
    assert out.endswith(
        "más frecuentes:\n  Norte: 3\n  Sur: 2\n"
        f"mediana: 25.0 {UNIT}\n"
        "media móvil (3): 30.0 · 36.7\n"
        f"mayor salto: +40.0 {UNIT}\n"
    )


def test_main_without_values_skips_trends(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["Centro;NA", "Sur;NA"]) == 0
    out = capsys.readouterr().out
    assert out.endswith("más frecuentes:\n  Centro: 1\n  Sur: 1\n")


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


@pytest.mark.parametrize("flag", ["-f", "--archivo"])
def test_main_reads_a_text_file(
    flag: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "medidas.txt"
    path.write_text("# cabecera\nNorte;12,5\nSur;NA\n", encoding="utf-8")
    assert main([flag, str(path)]) == 0
    assert capsys.readouterr().out == expected_output(["Norte;12,5", "Sur;NA"])


def test_main_reads_a_csv_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "medidas.csv"
    path.write_text("etiqueta;valor\nNorte;12,5\nSur;80\n", encoding="utf-8")
    assert main(["-f", str(path)]) == 0
    assert capsys.readouterr().out == expected_output(["Norte;12,5", "Sur;80"])


def test_main_missing_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "no-esta.txt"
    assert main(["-f", str(path)]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == f"error: no existe el archivo {path}\n"


@pytest.mark.parametrize("flag", ["-j", "--json"])
def test_main_saves_the_summary(
    flag: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "medidas.txt"
    source.write_text("Norte;10\nSur;NA\nNorte;30\n", encoding="utf-8")
    summary = tmp_path / "resumen.json"
    assert main(["-f", str(source), flag, str(summary)]) == 0
    out = capsys.readouterr().out
    assert out == expected_output(["Norte;10", "Sur;NA", "Norte;30"]) + (
        f"resumen guardado en {summary}\n"
    )
    assert json.loads(summary.read_text(encoding="utf-8")) == {
        "registros": 3,
        "con_valor": 2,
        "mediana": 20.0,
        "mayor_salto": 20.0,
    }


def test_main_cannot_save_the_summary(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    source = tmp_path / "medidas.txt"
    source.write_text("Norte;10\n", encoding="utf-8")
    summary = tmp_path / "no-esta" / "resumen.json"
    assert main(["-f", str(source), "-j", str(summary)]) == 2
    assert capsys.readouterr().err == f"error: no se puede escribir {summary}\n"


def test_main_json_without_file_is_unknown(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["-j", "resumen.json"]) == 2
    assert capsys.readouterr().err == f"{USAGE}\n"


@pytest.mark.parametrize("flag", ["-V", "--version"])
def test_main_version(flag: str, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([flag]) == 0
    assert capsys.readouterr().out == "observatorio 0.11.0\n"


def test_main_version_with_more_arguments_is_unknown(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--version", "Sur;8"]) == 2
    assert capsys.readouterr().err == USAGE + "\n"


def test_usage_mentions_version() -> None:
    assert "--version" in USAGE
