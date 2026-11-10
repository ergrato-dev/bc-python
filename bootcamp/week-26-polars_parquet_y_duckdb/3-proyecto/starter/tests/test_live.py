"""Tests de la semana 17: vigilar varios archivos a la vez con asyncio.

Cada test es una función normal que arranca el bucle con `asyncio.run`: pytest no
ejecuta funciones `async def` sin un plugin. Como en la semana 16, nada depende de
cuánto se tarda: las tareas falsas se esperan con una Barrier o ceden el turno con
`asyncio.sleep(0)`, y lo que se comprueba es el orden y cuántas había a la vez.
"""

import asyncio
import inspect
from collections.abc import AsyncIterator, Callable, Iterable
from pathlib import Path

import pytest
from typer.testing import CliRunner

from observatorio import cli
from observatorio.core import (
    FileReport,
    Measurement,
    Scale,
    Series,
    live,
    replay,
    report_file,
    watch_file,
    watch_files,
)

runner = CliRunner()

WriteFile = Callable[[str, str], Path]


def table_rows(output: str) -> list[list[str]]:
    """Las celdas de las filas de datos de la tabla: las líneas entre "│" sin cabecera."""
    lines = [line for line in output.splitlines() if line.startswith("│")]
    return [[cell.strip() for cell in line.split("│")[1:-1]] for line in lines]


async def collect(stream: AsyncIterator[Measurement]) -> list[Measurement]:
    """Todas las medidas de un iterador asíncrono, en una lista."""
    return [measurement async for measurement in stream]


# --- FileReport.from_series ---


def test_from_series_counts_and_averages() -> None:
    series = Series([Measurement("Norte", 10.0), Measurement("Sur", None)])
    series.add(Measurement("Este", 30.0))
    assert FileReport.from_series(Path("a.txt"), series) == FileReport(Path("a.txt"), 3, 2, 20.0)


def test_from_series_without_values_has_no_mean() -> None:
    report = FileReport.from_series(Path("a.txt"), Series([Measurement("Sur", None)]))
    assert report == FileReport(Path("a.txt"), 1, 0, None)


def test_report_file_still_gives_the_same(write_file: WriteFile) -> None:
    path = write_file("a.csv", "etiqueta;valor\nNorte;10\nSur;NA\n")
    assert report_file(path) == FileReport(path, 2, 1, 10.0)


# --- replay ---


def test_replay_is_an_async_generator() -> None:
    assert inspect.isasyncgenfunction(replay)


def test_replay_gives_the_valid_measurements() -> None:
    lines = ["etiqueta;valor\n", "Norte;10\n", "basura\n", "Sur;NA\n", "\n"]
    assert asyncio.run(collect(replay(lines))) == [
        Measurement("Norte", 10.0),
        Measurement("Sur", None),
    ]


def test_replay_waits_before_each_measurement(monkeypatch: pytest.MonkeyPatch) -> None:
    waits: list[float] = []
    real_sleep = asyncio.sleep

    async def fake_sleep(delay: float) -> None:
        waits.append(delay)
        await real_sleep(0)

    monkeypatch.setattr(asyncio, "sleep", fake_sleep)
    asyncio.run(collect(replay(["Norte;10", "basura", "Sur;20"], interval=0.25)))
    assert waits == [0.25, 0.25]


def test_replay_is_lazy() -> None:
    read: list[str] = []

    def lines() -> Iterable[str]:
        for line in ["Norte;10", "Sur;20"]:
            read.append(line)
            yield line

    async def first() -> Measurement:
        stream = replay(lines())
        return await anext(stream)

    assert asyncio.run(first()) == Measurement("Norte", 10.0)
    assert read == ["Norte;10"]


def test_replay_lets_other_tasks_run() -> None:
    # Con asyncio.sleep, dos reproducciones se turnan; con time.sleep, una iría entera primero.
    seen: list[str] = []

    async def play(label: str) -> None:
        async for measurement in replay([f"{label};1", f"{label};2", f"{label};3"]):
            seen.append(f"{measurement.label}{measurement.value:g}")

    async def both() -> None:
        async with asyncio.TaskGroup() as group:
            group.create_task(play("A"))
            group.create_task(play("B"))

    asyncio.run(both())
    assert seen == ["A1", "B1", "A2", "B2", "A3", "B3"]


# --- watch_file ---


def test_watch_file_is_a_coroutine_function() -> None:
    assert inspect.iscoroutinefunction(watch_file)


def test_watch_file_summarizes_like_report_file(write_file: WriteFile) -> None:
    for path in [
        write_file("a.txt", "Norte;10\nSur;NA\nbasura\nEste;30\n"),
        write_file("b.csv", "etiqueta;valor\nNorte;5\n"),
    ]:
        assert asyncio.run(watch_file(path)) == report_file(path)


def test_watch_file_turns_a_missing_file_into_an_error(tmp_path: Path) -> None:
    path = tmp_path / "falta.txt"
    assert asyncio.run(watch_file(path)) == FileReport(path, error=f"no existe el archivo {path}")


def test_watch_file_turns_a_bad_header_into_an_error(write_file: WriteFile) -> None:
    path = write_file("a.csv", "nombre;cantidad\nNorte;10\n")
    report = asyncio.run(watch_file(path))
    assert report.measurements == 0
    assert report.error is not None


def test_watch_file_tells_each_measurement_in_order(write_file: WriteFile) -> None:
    path = write_file("a.txt", "Norte;10\nSur;NA\n")
    seen: list[tuple[Path, Measurement]] = []
    asyncio.run(watch_file(path, on_reading=lambda where, what: seen.append((where, what))))
    assert seen == [(path, Measurement("Norte", 10.0)), (path, Measurement("Sur", None))]


def test_watch_file_reads_the_disk_in_another_thread(
    write_file: WriteFile, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = write_file("a.txt", "Norte;10\n")
    sent: list[object] = []
    real_to_thread = asyncio.to_thread

    async def spy(function: Callable[[], list[str]]) -> list[str]:
        sent.append(function)
        return await real_to_thread(function)

    monkeypatch.setattr(asyncio, "to_thread", spy)
    asyncio.run(watch_file(path))
    assert len(sent) == 1


def test_watch_file_passes_the_interval_to_replay(
    write_file: WriteFile, monkeypatch: pytest.MonkeyPatch
) -> None:
    intervals: list[float] = []
    real_replay = live.replay

    def spy(lines: Iterable[str], *, interval: float = 0.0) -> AsyncIterator[Measurement]:
        intervals.append(interval)
        return real_replay(lines, interval=0)

    monkeypatch.setattr(live, "replay", spy)
    asyncio.run(watch_file(write_file("a.txt", "Norte;10\n"), interval=0.75))
    assert intervals == [0.75]


# --- watch_files ---


def test_watch_files_gives_a_report_per_file(write_file: WriteFile, tmp_path: Path) -> None:
    paths = [
        write_file("a.txt", "Norte;10\nNorte;20\n"),
        tmp_path / "falta.txt",
        write_file("b.csv", "etiqueta;valor\nSur;NA\n"),
    ]
    assert asyncio.run(watch_files(paths)) == [report_file(path) for path in paths]


def test_watch_files_keeps_the_order_of_the_paths(monkeypatch: pytest.MonkeyPatch) -> None:
    # La primera tarea cede el turno más veces, así que termina la última.
    async def slow_watch(path: Path, **options: object) -> FileReport:
        for _ in range(10 - int(path.stem)):
            await asyncio.sleep(0)
        return FileReport(path)

    monkeypatch.setattr(live, "watch_file", slow_watch)
    paths = [Path(f"{n}.txt") for n in range(5)]
    assert [report.path for report in asyncio.run(watch_files(paths))] == paths


def test_watch_files_runs_the_files_at_the_same_time(monkeypatch: pytest.MonkeyPatch) -> None:
    # La barrera solo se abre si tres tareas esperan en ella a la vez.
    async def run() -> list[FileReport]:
        barrier = asyncio.Barrier(3)

        async def waiting_watch(path: Path, **options: object) -> FileReport:
            async with asyncio.timeout(5):
                await barrier.wait()
            return FileReport(path)

        monkeypatch.setattr(live, "watch_file", waiting_watch)
        return await watch_files([Path("a"), Path("b"), Path("c")], limit=3)

    assert len(asyncio.run(run())) == 3


@pytest.mark.parametrize("limit", [1, 2, 3])
def test_limit_caps_the_files_at_the_same_time(limit: int, monkeypatch: pytest.MonkeyPatch) -> None:
    active = 0
    peak = 0

    async def counting_watch(path: Path, **options: object) -> FileReport:
        nonlocal active, peak
        active += 1
        peak = max(peak, active)
        for _ in range(3):
            await asyncio.sleep(0)
        active -= 1
        return FileReport(path)

    monkeypatch.setattr(live, "watch_file", counting_watch)
    asyncio.run(watch_files([Path(f"{n}.txt") for n in range(6)], limit=limit))
    assert peak == limit


def test_watch_files_passes_the_options_to_watch_file(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[Path, object]] = []

    def on_reading(path: Path, measurement: Measurement) -> None: ...

    async def spy(path: Path, *, interval: float, on_reading: object) -> FileReport:
        calls.append((path, (interval, on_reading)))
        return FileReport(path)

    monkeypatch.setattr(live, "watch_file", spy)
    asyncio.run(watch_files([Path("a.txt")], interval=0.5, on_reading=on_reading))
    assert calls == [(Path("a.txt"), (0.5, on_reading))]


def test_watch_files_defaults() -> None:
    parameters = inspect.signature(watch_files).parameters
    assert parameters["interval"].default == 0.0
    assert parameters["limit"].default == 4
    assert parameters["on_reading"].default is None


def test_unexpected_errors_cancel_the_rest(monkeypatch: pytest.MonkeyPatch) -> None:
    cancelled: list[Path] = []

    async def broken_watch(path: Path, **options: object) -> FileReport:
        if path.name == "roto.txt":
            raise ValueError("bug")
        try:
            await asyncio.sleep(10)
        except asyncio.CancelledError:
            cancelled.append(path)
            raise
        return FileReport(path)

    monkeypatch.setattr(live, "watch_file", broken_watch)
    with pytest.raises(ExceptionGroup) as caught:
        asyncio.run(watch_files([Path("a.txt"), Path("roto.txt"), Path("b.txt")]))
    assert caught.group_contains(ValueError, match="bug")
    assert sorted(cancelled) == [Path("a.txt"), Path("b.txt")]


def test_live_does_not_start_the_loop_nor_touch_the_terminal() -> None:
    source = Path(live.__file__).read_text(encoding="utf-8")
    for word in ["asyncio.run(", "typer", "rich", "print("]:
        assert word not in source


# --- el comando vigilar ---


@pytest.fixture
def files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """Tres archivos en una carpeta temporal, que pasa a ser la carpeta de trabajo."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "norte.txt").write_text("Norte;10\nNorte;60\n", encoding="utf-8")
    (tmp_path / "sur.csv").write_text("etiqueta;valor\nSur;5\nSur;NA\n", encoding="utf-8")
    (tmp_path / "nada.txt").write_text("Este;NA\n", encoding="utf-8")
    return ["norte.txt", "sur.csv", "nada.txt"]


def test_vigilar_writes_the_same_table_as_lote(files: list[str]) -> None:
    watched = runner.invoke(cli.app, ["vigilar", "-i", "0", *files])
    batched = runner.invoke(cli.app, ["lote", *files])
    assert watched.exit_code == 0
    assert table_rows(watched.stdout) == table_rows(batched.stdout)
    assert watched.stdout.splitlines()[-1] == "archivos: 3 · con error: 0"


def test_vigilar_writes_each_reading(files: list[str]) -> None:
    result = runner.invoke(cli.app, ["vigilar", "-i", "0", *files])
    readings = [
        line
        for line in result.stdout.splitlines()
        if " · " in line and not line.startswith("archivos")
    ]
    assert sorted(readings) == [
        "nada.txt · Este: sin dato",
        "norte.txt · Norte: 10.0 unidad medio",
        "norte.txt · Norte: 60.0 unidad alto",
        "sur.csv · Sur: 5.0 unidad bajo",
        "sur.csv · Sur: sin dato",
    ]
    norte = [line for line in readings if line.startswith("norte.txt")]
    assert norte == ["norte.txt · Norte: 10.0 unidad medio", "norte.txt · Norte: 60.0 unidad alto"]


def test_vigilar_writes_the_readings_before_the_table(files: list[str]) -> None:
    lines = runner.invoke(cli.app, ["vigilar", "-i", "0", "norte.txt"]).stdout.splitlines()
    assert lines[:2] == [
        "norte.txt · Norte: 10.0 unidad medio",
        "norte.txt · Norte: 60.0 unidad alto",
    ]


def test_vigilar_uses_the_scale_and_unit_of_the_cli(
    files: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(cli, "UNIT", "kWh")
    monkeypatch.setattr(cli, "SCALE", Scale("kWh", 70, 80))
    result = runner.invoke(cli.app, ["vigilar", "-i", "0", "norte.txt"])
    assert result.stdout.splitlines()[:2] == [
        "norte.txt · Norte: 10.0 kWh bajo",
        "norte.txt · Norte: 60.0 kWh bajo",
    ]
    assert table_rows(result.stdout) == [["norte.txt", "2", "2", "35.0 kWh"]]


def test_vigilar_reports_the_files_it_cannot_read(files: list[str]) -> None:
    result = runner.invoke(cli.app, ["vigilar", "-i", "0", "norte.txt", "falta.txt"])
    assert result.exit_code == 1
    assert result.stderr == "error: no existe el archivo falta.txt\n"
    assert table_rows(result.stdout) == [["norte.txt", "2", "2", "35.0 unidad"]]
    assert result.stdout.splitlines()[-1] == "archivos: 2 · con error: 1"


def test_vigilar_stops_when_the_time_is_up(files: list[str]) -> None:
    result = runner.invoke(cli.app, ["vigilar", "-i", "5", "--tiempo", "0.1", *files])
    assert result.exit_code == 1
    assert result.stderr == "error: tiempo agotado a los 0.1 s\n"
    assert table_rows(result.stdout) == []


def test_vigilar_passes_the_options_to_watch_files(
    files: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[tuple[list[Path], float, int]] = []

    async def spy(
        paths: list[Path], *, interval: float, limit: int, on_reading: object
    ) -> list[FileReport]:
        calls.append((list(paths), interval, limit))
        return []

    monkeypatch.setattr(cli, "watch_files", spy)
    runner.invoke(cli.app, ["vigilar", "norte.txt"])
    runner.invoke(cli.app, ["vigilar", "-i", "0", "-l", "2", "norte.txt"])
    assert calls == [
        ([Path("norte.txt")], getattr(cli, "INTERVAL", None), cli.WORKERS),
        ([Path("norte.txt")], 0.0, 2),
    ]


def test_vigilar_default_interval_is_half_a_second() -> None:
    assert getattr(cli, "INTERVAL", None) == 0.5


@pytest.mark.parametrize(
    "options", [["-l", "0", "a.txt"], ["-i", "-1", "a.txt"], ["--tiempo", "-1", "a.txt"], []]
)
def test_vigilar_rejects_bad_options(options: list[str]) -> None:
    result = runner.invoke(cli.app, ["vigilar", *options])
    assert result.exit_code == 2
