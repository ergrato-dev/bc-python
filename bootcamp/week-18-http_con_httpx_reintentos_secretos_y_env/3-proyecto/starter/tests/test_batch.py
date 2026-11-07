"""Tests de la semana 16: resumir muchos archivos a la vez con hilos o procesos.

El código concurrente se prueba sin depender de la suerte: las tareas falsas duermen
un poco o se esperan con una Barrier, y lo que se comprueba es el resultado (el orden,
cuántas tareas había a la vez), nunca cuánto tardó.
"""

import pickle
import subprocess
import sys
import threading
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest
from typer.testing import CliRunner

from observatorio import cli
from observatorio.core import FileReport, batch, report_file, report_files

runner = CliRunner()

WriteFile = Callable[[str, str], Path]


def table_rows(output: str) -> list[list[str]]:
    """Las celdas de las filas de datos de la tabla: las líneas entre "│" sin cabecera."""
    lines = [line for line in output.splitlines() if line.startswith("│")]
    return [[cell.strip() for cell in line.split("│")[1:-1]] for line in lines]


# --- FileReport ---


def test_file_report_defaults_to_an_empty_summary() -> None:
    report = FileReport(Path("a.txt"))
    assert (report.measurements, report.with_value, report.mean, report.error) == (
        0,
        0,
        None,
        None,
    )


def test_file_report_is_frozen() -> None:
    report = FileReport(Path("a.txt"))
    with pytest.raises(FrozenInstanceError):
        report.measurements = 3  # type: ignore[misc]


def test_file_report_survives_pickle() -> None:
    # Los procesos se pasan los resultados en bytes: FileReport tiene que poder viajar.
    report = FileReport(Path("a.txt"), 2, 1, 12.5)
    assert pickle.loads(pickle.dumps(report)) == report


# --- report_file ---


def test_report_file_counts_the_measurements(write_file: WriteFile, lines: list[str]) -> None:
    path = write_file("medidas.txt", "\n".join(lines) + "\n")
    report = report_file(path)
    assert (report.measurements, report.with_value, report.error) == (3, 2, None)
    assert report.mean == pytest.approx(33.8)


def test_report_file_reads_csv(write_file: WriteFile) -> None:
    path = write_file("medidas.csv", "etiqueta;valor\nNorte;10\nSur;20\n")
    assert report_file(path) == FileReport(path, 2, 2, 15.0)


def test_report_file_without_values_has_no_mean(write_file: WriteFile) -> None:
    path = write_file("vacio.txt", "Norte;NA\nSur;NA\n")
    assert report_file(path) == FileReport(path, 2, 0, None)


def test_report_file_of_an_empty_file(write_file: WriteFile) -> None:
    path = write_file("nada.txt", "")
    assert report_file(path) == FileReport(path, 0, 0, None)


def test_report_file_turns_a_missing_file_into_an_error(tmp_path: Path) -> None:
    path = tmp_path / "falta.txt"
    assert report_file(path) == FileReport(path, error=f"no existe el archivo {path}")


def test_report_file_turns_a_bad_header_into_an_error(write_file: WriteFile) -> None:
    path = write_file("malo.csv", "nombre;valor\nNorte;10\n")
    report = report_file(path)
    assert report.measurements == 0
    assert report.error is not None
    assert str(path) in report.error


# --- report_files: el orden, la concurrencia y los errores ---


def slow_report(path: Path) -> FileReport:
    """Una tarea falsa: el primer archivo es el más lento, así termina el último."""
    time.sleep(0.05 * (3 - int(path.stem)))
    return FileReport(path, int(path.stem))


def test_report_files_keeps_the_order_of_the_paths(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(batch, "report_file", slow_report)
    paths = [Path("0"), Path("1"), Path("2")]
    reports = report_files(paths, workers=3)
    assert [report.path for report in reports] == paths


def test_report_files_of_nothing() -> None:
    assert report_files([]) == []


def test_report_files_accepts_any_iterable(write_file: WriteFile) -> None:
    paths = [write_file(f"{name}.txt", "Norte;1\n") for name in "abc"]
    reports = report_files(path for path in paths)
    assert [report.path for report in reports] == paths


def test_report_files_runs_the_tasks_at_the_same_time(monkeypatch: pytest.MonkeyPatch) -> None:
    # Cada tarea espera en la barrera a que lleguen las tres. Si fueran una detrás de
    # otra, la primera esperaría para siempre: el timeout lo convierte en un error.
    barrier = threading.Barrier(3, timeout=5)

    def meet(path: Path) -> FileReport:
        barrier.wait()
        return FileReport(path)

    monkeypatch.setattr(batch, "report_file", meet)
    assert len(report_files([Path("a"), Path("b"), Path("c")], workers=3)) == 3


@pytest.mark.parametrize("workers", [1, 2, 3])
def test_workers_limit_the_tasks_at_the_same_time(
    monkeypatch: pytest.MonkeyPatch, workers: int
) -> None:
    lock = threading.Lock()
    active = 0
    peak = 0

    def count(path: Path) -> FileReport:
        nonlocal active, peak
        # Varios hilos cambian active y peak: sin el Lock, dos podrían leer el mismo
        # valor y perder una suma (una condición de carrera).
        with lock:
            active += 1
            peak = max(peak, active)
        time.sleep(0.05)
        with lock:
            active -= 1
        return FileReport(path)

    monkeypatch.setattr(batch, "report_file", count)
    report_files([Path(str(number)) for number in range(6)], workers=workers)
    assert peak == workers


def test_report_files_uses_threads_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    names: list[str] = []

    def remember(path: Path) -> FileReport:
        names.append(threading.current_thread().name)
        return FileReport(path)

    monkeypatch.setattr(batch, "report_file", remember)
    report_files([Path("a"), Path("b")])
    assert names
    assert all(name.startswith("observatorio") for name in names)


def test_processes_uses_a_process_pool(monkeypatch: pytest.MonkeyPatch) -> None:
    # Un sustituto de ProcessPoolExecutor que apunta cómo se creó y trabaja con hilos.
    created: list[int | None] = []

    class SpyPool(ThreadPoolExecutor):
        def __init__(self, max_workers: int | None = None) -> None:
            created.append(max_workers)
            super().__init__(max_workers=max_workers)

    monkeypatch.setattr(batch, "ProcessPoolExecutor", SpyPool)
    report_files([Path("falta.txt")], workers=2, processes=True)
    assert created == [2]


def test_processes_give_the_same_reports_as_threads(write_file: WriteFile) -> None:
    paths = [
        write_file("a.txt", "Norte;10\nSur;NA\n"),
        write_file("b.csv", "etiqueta;valor\nEste;30\n"),
        write_file("c.txt", "malo\n"),
    ]
    paths.append(paths[0].parent / "falta.txt")
    assert report_files(paths, workers=2, processes=True) == report_files(paths, workers=2)


def test_unexpected_errors_reach_the_caller(monkeypatch: pytest.MonkeyPatch) -> None:
    def broken(path: Path) -> FileReport:
        raise RuntimeError(f"bug con {path}")

    monkeypatch.setattr(batch, "report_file", broken)
    with pytest.raises(RuntimeError, match="bug con a"):
        report_files([Path("a")])


# --- el comando lote ---


@pytest.fixture
def files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """Tres archivos en una carpeta temporal, que pasa a ser la carpeta de trabajo.

    Con rutas cortas, la tabla cabe en las 80 columnas de una salida sin terminal.
    """
    monkeypatch.chdir(tmp_path)
    (tmp_path / "norte.txt").write_text("Norte;10\nNorte;20\n", encoding="utf-8")
    (tmp_path / "sur.csv").write_text("etiqueta;valor\nSur;5\nSur;NA\n", encoding="utf-8")
    (tmp_path / "nada.txt").write_text("Este;NA\n", encoding="utf-8")
    return ["norte.txt", "sur.csv", "nada.txt"]


def test_lote_writes_a_row_per_file(files: list[str]) -> None:
    result = runner.invoke(cli.app, ["lote", *files])
    assert result.exit_code == 0
    assert table_rows(result.stdout) == [
        ["norte.txt", "2", "2", "15.0 unidad"],
        ["sur.csv", "2", "1", "5.0 unidad"],
        ["nada.txt", "1", "0", "sin dato"],
    ]
    assert result.stdout.splitlines()[-1] == "archivos: 3 · con error: 0"
    assert result.stderr == ""


def test_lote_keeps_the_order_of_the_arguments(files: list[str]) -> None:
    result = runner.invoke(cli.app, ["lote", *reversed(files)])
    assert [row[0] for row in table_rows(result.stdout)] == list(reversed(files))


def test_lote_uses_the_unit_of_the_cli(files: list[str], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cli, "UNIT", "kWh")
    result = runner.invoke(cli.app, ["lote", "norte.txt"])
    assert table_rows(result.stdout) == [["norte.txt", "2", "2", "15.0 kWh"]]


def test_lote_reports_the_files_it_cannot_read(files: list[str]) -> None:
    result = runner.invoke(cli.app, ["lote", "norte.txt", "falta.txt"])
    assert result.exit_code == 1
    assert result.stderr == "error: no existe el archivo falta.txt\n"
    assert table_rows(result.stdout) == [["norte.txt", "2", "2", "15.0 unidad"]]
    assert result.stdout.splitlines()[-1] == "archivos: 2 · con error: 1"


def test_lote_with_processes_writes_the_same(files: list[str]) -> None:
    with_threads = runner.invoke(cli.app, ["lote", *files])
    with_processes = runner.invoke(cli.app, ["lote", "--procesos", "-t", "2", *files])
    assert with_processes.exit_code == 0
    assert with_processes.stdout == with_threads.stdout


def test_lote_passes_the_options_to_report_files(
    files: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[tuple[list[Path], int, bool]] = []

    def spy(paths: list[Path], *, workers: int, processes: bool) -> list[FileReport]:
        calls.append((list(paths), workers, processes))
        return []

    monkeypatch.setattr(cli, "report_files", spy)
    runner.invoke(cli.app, ["lote", "norte.txt"])
    runner.invoke(cli.app, ["lote", "-t", "2", "--procesos", "norte.txt"])
    assert calls == [
        ([Path("norte.txt")], cli.WORKERS, False),
        ([Path("norte.txt")], 2, True),
    ]


def test_lote_default_workers_is_4() -> None:
    assert cli.WORKERS == 4


def test_lote_needs_at_least_one_file() -> None:
    result = runner.invoke(cli.app, ["lote"])
    assert result.exit_code == 2
    assert "Missing argument" in result.stderr


def test_lote_rejects_zero_workers(files: list[str]) -> None:
    result = runner.invoke(cli.app, ["lote", "-t", "0", "norte.txt"])
    assert result.exit_code == 2
    assert "--trabajadores" in result.stderr


def test_help_lists_lote() -> None:
    result = runner.invoke(cli.app, ["--help"])
    assert "lote" in result.stdout


def test_lote_runs_processes_from_the_terminal(files: list[str]) -> None:
    # Otro proceso de verdad: así se prueba que los procesos hijos encuentran el código.
    command = [sys.executable, "-m", "observatorio", "lote", "--procesos", *files]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    assert result.returncode == 0
    assert result.stdout.splitlines()[-1] == "archivos: 3 · con error: 0"
