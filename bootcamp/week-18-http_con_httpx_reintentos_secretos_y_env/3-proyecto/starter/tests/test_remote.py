"""Tests de la semana 18: descargar medidas por HTTP con httpx.

Ningún test sale a Internet. Casi todos responden con `httpx.MockTransport`: una función
que recibe la petición y devuelve la respuesta, sin red. Los dos de "servidor de verdad"
levantan `http.server` en 127.0.0.1, en un hilo, y lo apagan al terminar. Las esperas
entre reintentos se espían cambiando `asyncio.sleep`, así que nada espera de verdad.
"""

import asyncio
import inspect
import logging
from collections.abc import Awaitable, Callable, Coroutine, Iterator
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from importlib.metadata import version
from pathlib import Path
from threading import Thread

import httpx
import pytest
from pydantic import ValidationError
from typer.testing import CliRunner

from observatorio import cli
from observatorio.core import (
    DataFileError,
    FetchError,
    FileReport,
    Measurement,
    Series,
    download,
    download_all,
    get_text,
    make_client,
    parse_measurements,
    remote,
    report_file,
    target_of,
)
from observatorio.settings import Settings

runner = CliRunner()

URL = "http://estaciones.test/norte.json"
NORTE = [{"label": "Norte", "value": 10}, {"label": "Norte", "value": "60,5"}]
SUR = [{"label": "Sur", "value": 5}, {"label": "Sur", "value": None}]

# Lo que acepta MockTransport: una función normal o una corrutina que da la respuesta.
Handler = (
    Callable[[httpx.Request], httpx.Response]
    | Callable[[httpx.Request], Coroutine[None, None, httpx.Response]]
)


def run_with[T](
    handler: Handler, use: Callable[[httpx.AsyncClient], Awaitable[T]], token: str | None = None
) -> T:
    """Arranca el bucle, abre un cliente que responde con `handler` y le pasa el cliente a `use`."""

    async def main() -> T:
        transport = httpx.MockTransport(handler)
        async with make_client(transport=transport, token=token) as client:
            return await use(client)

    return asyncio.run(main())


def replies(
    *responses: httpx.Response | type[httpx.TransportError],
) -> tuple[Handler, list[httpx.Request]]:
    """Un handler que contesta con `responses` en orden (la última se repite) y las peticiones."""
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        response = responses[min(len(seen), len(responses)) - 1]
        if isinstance(response, httpx.Response):
            return response
        raise response("fallo de prueba", request=request)

    return handler, seen


@pytest.fixture
def waits(monkeypatch: pytest.MonkeyPatch) -> list[float]:
    """Las esperas que se piden a asyncio.sleep; ceden el turno, pero sin esperar."""
    asked: list[float] = []
    real_sleep = asyncio.sleep

    async def spy(delay: float) -> None:
        asked.append(delay)
        await real_sleep(0)

    monkeypatch.setattr(asyncio, "sleep", spy)
    return asked


# --- make_client ---


def test_make_client_says_who_it_is() -> None:
    handler, seen = replies(httpx.Response(200))
    run_with(handler, lambda client: client.get(URL))
    assert seen[0].headers["User-Agent"] == f"observatorio/{version('observatorio')}"


def test_make_client_sends_the_token_as_bearer() -> None:
    handler, seen = replies(httpx.Response(200))
    run_with(handler, lambda client: client.get(URL), token="abc123")
    assert seen[0].headers["Authorization"] == "Bearer abc123"


def test_make_client_without_token_sends_no_authorization() -> None:
    handler, seen = replies(httpx.Response(200))
    run_with(handler, lambda client: client.get(URL))
    assert "Authorization" not in seen[0].headers


def test_make_client_uses_the_timeout() -> None:
    client = make_client(timeout=2.5)
    assert client.timeout == httpx.Timeout(2.5)
    assert make_client().timeout == httpx.Timeout(10.0)


def test_make_client_follows_redirects() -> None:
    handler, seen = replies(
        httpx.Response(301, headers={"Location": "/nueva.json"}), httpx.Response(200, text="ok")
    )
    assert run_with(handler, lambda client: get_text(client, URL)) == "ok"
    assert [request.url.path for request in seen] == ["/norte.json", "/nueva.json"]


# --- get_text ---


def test_get_text_is_a_coroutine_function() -> None:
    assert inspect.iscoroutinefunction(get_text)


def test_get_text_returns_the_body() -> None:
    handler, seen = replies(httpx.Response(200, text="hola"))
    assert run_with(handler, lambda client: get_text(client, URL)) == "hola"
    assert len(seen) == 1


@pytest.mark.parametrize("status", [400, 401, 403, 404])
def test_get_text_does_not_retry_a_client_error(status: int, waits: list[float]) -> None:
    handler, seen = replies(httpx.Response(status))
    with pytest.raises(FetchError, match=f"^{URL} respondió {status}$"):
        run_with(handler, lambda client: get_text(client, URL))
    assert len(seen) == 1
    assert waits == []


@pytest.mark.parametrize("status", [429, 500, 502, 503, 504])
def test_get_text_retries_a_passing_failure(status: int, waits: list[float]) -> None:
    handler, seen = replies(httpx.Response(status), httpx.Response(200, text="ok"))
    assert run_with(handler, lambda client: get_text(client, URL)) == "ok"
    assert len(seen) == 2


def test_get_text_gives_up_after_the_retries(waits: list[float]) -> None:
    handler, seen = replies(httpx.Response(503))
    with pytest.raises(FetchError, match=f"^{URL} respondió 503 tras 4 intentos$"):
        run_with(handler, lambda client: get_text(client, URL))
    assert len(seen) == 4


def test_get_text_without_retries_tries_once(waits: list[float]) -> None:
    handler, seen = replies(httpx.Response(503))
    with pytest.raises(FetchError, match="tras 1 intentos$"):
        run_with(handler, lambda client: get_text(client, URL, retries=0))
    assert len(seen) == 1


@pytest.mark.parametrize(
    "problem", [httpx.ConnectError, httpx.ReadTimeout, httpx.RemoteProtocolError]
)
def test_get_text_retries_when_there_is_no_answer(
    problem: type[httpx.TransportError], waits: list[float]
) -> None:
    handler, seen = replies(problem, httpx.Response(200, text="ok"))
    assert run_with(handler, lambda client: get_text(client, URL)) == "ok"
    assert len(seen) == 2


def test_get_text_says_why_there_was_no_answer(waits: list[float]) -> None:
    handler, _ = replies(httpx.ConnectError)
    with pytest.raises(FetchError, match=r"^sin respuesta de .* \(ConnectError\) tras 2 intentos$"):
        run_with(handler, lambda client: get_text(client, URL, retries=1))


def test_get_text_waits_twice_as_long_each_time(waits: list[float]) -> None:
    handler, _ = replies(httpx.Response(503))
    with pytest.raises(FetchError):
        run_with(handler, lambda client: get_text(client, URL))
    assert waits == [0.5, 1.0, 2.0]


def test_get_text_waits_with_the_backoff_it_is_given(waits: list[float]) -> None:
    handler, _ = replies(httpx.Response(503), httpx.Response(503), httpx.Response(200))
    run_with(handler, lambda client: get_text(client, URL, backoff=0.1))
    assert waits == [0.1, 0.2]


def test_get_text_does_not_wait_when_the_first_try_works(waits: list[float]) -> None:
    handler, _ = replies(httpx.Response(200))
    run_with(handler, lambda client: get_text(client, URL))
    assert waits == []


def test_get_text_logs_each_failed_try(
    waits: list[float], caplog: pytest.LogCaptureFixture
) -> None:
    handler, _ = replies(httpx.Response(503), httpx.Response(200))
    with caplog.at_level(logging.DEBUG, logger="observatorio.core.remote"):
        run_with(handler, lambda client: get_text(client, URL))
    assert f"intento 1 de 4: {URL} respondió 503" in caplog.messages


# --- parse_measurements ---


def test_parse_measurements_validates_a_text() -> None:
    series = parse_measurements('[{"label": "Norte", "value": "12,5"}]', URL)
    assert list(series) == [Measurement("Norte", 12.5)]


def test_parse_measurements_names_the_source_in_the_error() -> None:
    with pytest.raises(DataFileError, match=f"^datos no válidos en {URL}: 0.value: "):
        parse_measurements('[{"label": "Norte", "value": true}]', URL)


def test_parse_measurements_rejects_what_is_not_json() -> None:
    with pytest.raises(DataFileError, match=f"^datos no válidos en {URL}: "):
        parse_measurements("<html>Mantenimiento</html>", URL)


# --- target_of ---


@pytest.mark.parametrize(
    ("url", "name"),
    [
        ("http://estaciones.test/norte.json", "norte.txt"),
        ("https://estaciones.test/datos/2026/sur.json?dia=1", "sur.txt"),
        ("http://estaciones.test/este", "este.txt"),
        ("http://estaciones.test/", "datos.txt"),
        ("http://estaciones.test", "datos.txt"),
    ],
)
def test_target_of_names_the_file_after_the_url(url: str, name: str) -> None:
    assert target_of(url, Path("descargas")) == Path("descargas") / name


# --- download ---


def test_download_is_a_coroutine_function() -> None:
    assert inspect.iscoroutinefunction(download)


def test_download_saves_a_file_that_report_file_reads(tmp_path: Path) -> None:
    handler, _ = replies(httpx.Response(200, json=NORTE))
    report = run_with(handler, lambda client: download(client, URL, tmp_path))
    assert report == FileReport(tmp_path / "norte.txt", 2, 2, 35.25)
    assert report_file(tmp_path / "norte.txt") == report


def test_download_saves_one_line_per_measurement(tmp_path: Path) -> None:
    handler, _ = replies(httpx.Response(200, json=SUR))
    run_with(handler, lambda client: download(client, URL, tmp_path))
    assert (tmp_path / "norte.txt").read_text(encoding="utf-8") == "Sur;5,0\nSur;NA\n"


def test_download_keeps_a_failed_fetch_as_an_error(tmp_path: Path, waits: list[float]) -> None:
    handler, _ = replies(httpx.Response(404))
    report = run_with(handler, lambda client: download(client, URL, tmp_path))
    assert report == FileReport(tmp_path / "norte.txt", error=f"{URL} respondió 404")
    assert not (tmp_path / "norte.txt").exists()


def test_download_keeps_invalid_data_as_an_error(tmp_path: Path) -> None:
    handler, _ = replies(httpx.Response(200, json=[{"label": "", "value": 1}]))
    report = run_with(handler, lambda client: download(client, URL, tmp_path))
    assert report.error is not None
    assert report.error.startswith(f"datos no válidos en {URL}: 0.label: ")
    assert not (tmp_path / "norte.txt").exists()


def test_download_keeps_a_failed_write_as_an_error(tmp_path: Path) -> None:
    handler, _ = replies(httpx.Response(200, json=NORTE))
    folder = tmp_path / "no-existe"
    report = run_with(handler, lambda client: download(client, URL, folder))
    assert report.error == f"no se pudo guardar {folder / 'norte.txt'}: No such file or directory"


def test_download_writes_in_another_thread(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    called: list[str] = []
    real_to_thread = asyncio.to_thread

    async def spy[T](function: Callable[..., T], /, *args: object, **kwargs: object) -> T:
        called.append(getattr(function, "__name__", ""))
        return await real_to_thread(function, *args, **kwargs)

    monkeypatch.setattr(asyncio, "to_thread", spy)
    handler, _ = replies(httpx.Response(200, json=NORTE))
    run_with(handler, lambda client: download(client, URL, tmp_path))
    assert called == ["write_text"]


# --- download_all ---


def urls_of(*names: str) -> list[str]:
    return [f"http://estaciones.test/{name}.json" for name in names]


def test_download_all_keeps_the_order_of_the_urls(tmp_path: Path) -> None:
    second_done = asyncio.Event()

    async def handler(request: httpx.Request) -> httpx.Response:
        # La primera URL no contesta hasta que la segunda ya contestó.
        if request.url.path == "/a.json":
            async with asyncio.timeout(5):
                await second_done.wait()
        else:
            second_done.set()
        return httpx.Response(200, json=NORTE)

    reports = run_with(handler, lambda client: download_all(client, urls_of("a", "b"), tmp_path))
    assert [report.path.name for report in reports] == ["a.txt", "b.txt"]


def test_download_all_runs_the_downloads_at_once(tmp_path: Path) -> None:
    barrier = asyncio.Barrier(3)

    async def handler(request: httpx.Request) -> httpx.Response:
        # Solo se abre si las tres peticiones esperan a la vez; si no, falla a los 5 s.
        async with asyncio.timeout(5):
            await barrier.wait()
        return httpx.Response(200, json=NORTE)

    urls = urls_of("a", "b", "c")
    assert len(run_with(handler, lambda client: download_all(client, urls, tmp_path))) == 3


@pytest.mark.parametrize("limit", [1, 2, 3])
def test_download_all_respects_the_limit(limit: int, tmp_path: Path) -> None:
    active = peak = 0

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal active, peak
        active += 1
        peak = max(peak, active)
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        active -= 1
        return httpx.Response(200, json=NORTE)

    urls = urls_of("a", "b", "c", "d", "e", "f")
    run_with(handler, lambda client: download_all(client, urls, tmp_path, limit=limit))
    assert peak == limit


def test_download_all_keeps_going_when_one_url_fails(tmp_path: Path, waits: list[float]) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/mal.json":
            return httpx.Response(500)
        return httpx.Response(200, json=NORTE)

    reports = run_with(
        handler, lambda client: download_all(client, urls_of("a", "mal", "b"), tmp_path)
    )
    assert [report.error is None for report in reports] == [True, False, True]


def test_download_all_does_not_hide_a_bug(tmp_path: Path) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise ValueError("un bug")

    with pytest.raises(ExceptionGroup) as caught:
        run_with(handler, lambda client: download_all(client, urls_of("a"), tmp_path))
    assert caught.group_contains(ValueError, match="un bug")


def test_remote_does_not_start_the_loop_nor_read_the_configuration() -> None:
    source = Path(remote.__file__).read_text(encoding="utf-8")
    for word in ["asyncio.run(", "typer", "rich", "print(", "os.environ", "Settings"]:
        assert word not in source


# --- con un servidor de verdad, en 127.0.0.1 ---


class QuietHandler(SimpleHTTPRequestHandler):
    """El servidor de archivos de la biblioteca estándar, sin escribir cada petición."""

    def log_message(self, format: str, *args: object) -> None:
        pass


@pytest.fixture
def server(tmp_path: Path) -> Iterator[str]:
    """Sirve tmp_path/web por HTTP en un puerto libre y da su dirección."""
    web = tmp_path / "web"
    web.mkdir()
    (web / "norte.json").write_text('[{"label": "Norte", "value": 10}]', encoding="utf-8")
    # Puerto 0: el sistema elige uno libre. server_address dice cuál.
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=web))
    thread = Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_address[1]}"
    httpd.shutdown()
    httpd.server_close()


def test_download_from_a_real_server(server: str, tmp_path: Path) -> None:
    async def main() -> FileReport:
        async with make_client() as client:
            return await download(client, f"{server}/norte.json", tmp_path)

    assert asyncio.run(main()) == FileReport(tmp_path / "norte.txt", 1, 1, 10.0)


def test_a_missing_file_on_a_real_server_is_a_404(server: str, tmp_path: Path) -> None:
    async def main() -> FileReport:
        async with make_client() as client:
            return await download(client, f"{server}/sur.json", tmp_path)

    assert asyncio.run(main()).error == f"{server}/sur.json respondió 404"


# --- Settings ---


@pytest.fixture
def clean_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Una carpeta de trabajo vacía, sin .env, y sin variables OBSERVATORIO_* de tu máquina."""
    monkeypatch.chdir(tmp_path)
    for name in ["TOKEN", "TIMEOUT", "RETRIES"]:
        monkeypatch.delenv(f"OBSERVATORIO_{name}", raising=False)
    return tmp_path


def test_settings_defaults(clean_env: Path) -> None:
    settings = Settings()
    assert (settings.token, settings.timeout, settings.retries) == (None, 10.0, 3)


def test_settings_reads_the_environment(clean_env: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OBSERVATORIO_TOKEN", "abc123")
    monkeypatch.setenv("OBSERVATORIO_TIMEOUT", "2.5")
    monkeypatch.setenv("OBSERVATORIO_RETRIES", "0")
    settings = Settings()
    assert settings.token is not None
    assert settings.token.get_secret_value() == "abc123"
    assert (settings.timeout, settings.retries) == (2.5, 0)


def test_settings_reads_the_env_file(clean_env: Path) -> None:
    (clean_env / ".env").write_text("OBSERVATORIO_RETRIES=5\nOTRO_PROGRAMA=1\n", encoding="utf-8")
    assert Settings().retries == 5


def test_an_empty_variable_is_no_value(clean_env: Path) -> None:
    # Como queda .env si copias .env.example y no rellenas el token.
    (clean_env / ".env").write_text(
        "OBSERVATORIO_TOKEN=\nOBSERVATORIO_RETRIES=\n", encoding="utf-8"
    )
    assert (Settings().token, Settings().retries) == (None, 3)


def test_the_environment_wins_over_the_env_file(
    clean_env: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (clean_env / ".env").write_text("OBSERVATORIO_RETRIES=5\n", encoding="utf-8")
    monkeypatch.setenv("OBSERVATORIO_RETRIES", "1")
    assert Settings().retries == 1


def test_settings_ignores_variables_without_the_prefix(
    clean_env: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("TOKEN", "de-otro-programa")
    assert Settings().token is None


def test_settings_hides_the_token(clean_env: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OBSERVATORIO_TOKEN", "abc123")
    settings = Settings()
    assert "abc123" not in repr(settings)
    assert "abc123" not in str(settings)
    assert str(settings.token) == "**********"


@pytest.mark.parametrize(
    ("name", "value"),
    [("TIMEOUT", "0"), ("TIMEOUT", "rápido"), ("RETRIES", "-1"), ("RETRIES", "11")],
)
def test_settings_rejects_impossible_values(
    name: str, value: str, clean_env: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(f"OBSERVATORIO_{name}", value)
    with pytest.raises(ValidationError):
        Settings()


def test_settings_cannot_be_changed() -> None:
    assert Settings.model_config.get("frozen") is True


# --- el comando descargar ---

PAGES: dict[str, object] = {"/norte.json": NORTE, "/sur.json": SUR}


@pytest.fixture
def served(
    clean_env: Path, waits: list[float], monkeypatch: pytest.MonkeyPatch
) -> list[httpx.Request]:
    """Cambia el make_client de la CLI por uno que contesta con PAGES; da las peticiones.

    Con `waits`, los reintentos de /caido.json no esperan de verdad.
    """
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        page = PAGES.get(request.url.path)
        if request.url.path == "/caido.json":
            return httpx.Response(503)
        return httpx.Response(404) if page is None else httpx.Response(200, json=page)

    def fake_client(*, token: str | None = None, timeout: float = 10.0) -> httpx.AsyncClient:
        return make_client(token=token, timeout=timeout, transport=httpx.MockTransport(handler))

    monkeypatch.setattr(cli, "make_client", fake_client)
    return seen


def table_rows(output: str) -> list[list[str]]:
    """Las celdas de las filas de datos de la tabla: las líneas entre "│" sin cabecera."""
    lines = [line for line in output.splitlines() if line.startswith("│")]
    return [[cell.strip() for cell in line.split("│")[1:-1]] for line in lines]


def test_descargar_saves_the_files_and_writes_the_table(served: list[httpx.Request]) -> None:
    result = runner.invoke(cli.app, ["descargar", *urls_of("norte", "sur")])
    assert result.exit_code == 0
    assert table_rows(result.stdout) == [
        [str(Path("descargas/norte.txt")), "2", "2", "35.2 unidad"],
        [str(Path("descargas/sur.txt")), "2", "1", "5.0 unidad"],
    ]
    assert result.stdout.splitlines()[-1] == "archivos: 2 · con error: 0"
    assert Path("descargas/sur.txt").read_text(encoding="utf-8") == "Sur;5,0\nSur;NA\n"


def test_descargar_gives_the_same_table_as_lote(served: list[httpx.Request]) -> None:
    downloaded = runner.invoke(cli.app, ["descargar", *urls_of("norte", "sur")])
    batched = runner.invoke(cli.app, ["lote", "descargas/norte.txt", "descargas/sur.txt"])
    assert table_rows(downloaded.stdout) == table_rows(batched.stdout)


def test_descargar_reports_the_failed_urls(served: list[httpx.Request]) -> None:
    result = runner.invoke(cli.app, ["descargar", *urls_of("norte", "falta", "caido")])
    assert result.exit_code == 1
    assert result.stderr.splitlines() == [
        f"error: {urls_of('falta')[0]} respondió 404",
        f"error: {urls_of('caido')[0]} respondió 503 tras 4 intentos",
    ]
    assert result.stdout.splitlines()[-1] == "archivos: 3 · con error: 2"


def test_descargar_creates_the_folder(served: list[httpx.Request]) -> None:
    result = runner.invoke(cli.app, ["descargar", "-c", "datos/hoy", *urls_of("norte")])
    assert result.exit_code == 0
    assert Path("datos/hoy/norte.txt").exists()


def test_descargar_fails_cleanly_when_it_cannot_create_the_folder(
    served: list[httpx.Request], clean_env: Path
) -> None:
    (clean_env / "ocupado").write_text("un archivo, no una carpeta", encoding="utf-8")
    result = runner.invoke(cli.app, ["descargar", "-c", "ocupado", *urls_of("norte")])
    assert result.exit_code == 2
    assert result.stderr == "error: no se pudo crear ocupado: File exists\n"
    assert served == []


def test_descargar_rejects_what_is_not_a_url(served: list[httpx.Request]) -> None:
    result = runner.invoke(cli.app, ["descargar", "norte.json"])
    assert result.exit_code == 2
    assert "no empieza por http:// ni https://" in result.stderr
    assert served == []


def test_descargar_rejects_a_limit_of_zero(served: list[httpx.Request]) -> None:
    result = runner.invoke(cli.app, ["descargar", "-l", "0", *urls_of("norte")])
    assert result.exit_code == 2


def test_descargar_sends_the_token_from_the_environment(
    served: list[httpx.Request], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("OBSERVATORIO_TOKEN", "abc123")
    runner.invoke(cli.app, ["descargar", *urls_of("norte")])
    assert served[0].headers["Authorization"] == "Bearer abc123"


def test_descargar_sends_the_token_from_the_env_file(
    served: list[httpx.Request], clean_env: Path
) -> None:
    (clean_env / ".env").write_text("OBSERVATORIO_TOKEN=xyz789\n", encoding="utf-8")
    runner.invoke(cli.app, ["descargar", *urls_of("norte")])
    assert served[0].headers["Authorization"] == "Bearer xyz789"


def test_descargar_never_shows_the_token(
    served: list[httpx.Request], monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    monkeypatch.setenv("OBSERVATORIO_TOKEN", "abc123")
    with caplog.at_level(logging.DEBUG):
        result = runner.invoke(cli.app, ["-v", "descargar", *urls_of("norte", "falta", "caido")])
    assert "HTTP Request: GET" in caplog.text
    assert "abc123" not in result.stdout + result.stderr + caplog.text


def test_descargar_waits_backoff_and_doubles_it(
    served: list[httpx.Request], waits: list[float]
) -> None:
    runner.invoke(cli.app, ["descargar", *urls_of("caido")])
    assert waits == [0.5, 1.0, 2.0]


def test_descargar_uses_the_retries_of_the_configuration(
    served: list[httpx.Request], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("OBSERVATORIO_RETRIES", "0")
    result = runner.invoke(cli.app, ["descargar", *urls_of("caido")])
    assert len(served) == 1
    assert "tras 1 intentos" in result.stderr


def test_descargar_rejects_an_invalid_configuration(
    served: list[httpx.Request], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("OBSERVATORIO_TIMEOUT", "0")
    result = runner.invoke(cli.app, ["descargar", *urls_of("norte")])
    assert result.exit_code == 2
    assert result.stderr.startswith("error: configuración no válida: OBSERVATORIO_TIMEOUT: ")
    assert served == []


def test_descargar_passes_the_timeout_to_the_client(
    clean_env: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    timeouts: list[float] = []

    def fake_client(*, token: str | None = None, timeout: float = 10.0) -> httpx.AsyncClient:
        timeouts.append(timeout)
        return make_client(transport=httpx.MockTransport(lambda request: httpx.Response(404)))

    monkeypatch.setattr(cli, "make_client", fake_client)
    monkeypatch.setenv("OBSERVATORIO_TIMEOUT", "2.5")
    runner.invoke(cli.app, ["descargar", *urls_of("norte")])
    assert timeouts == [2.5]


def test_saved_files_work_with_the_other_commands(served: list[httpx.Request]) -> None:
    runner.invoke(cli.app, ["descargar", *urls_of("norte")])
    result = runner.invoke(cli.app, ["informe", "-f", "descargas/norte.txt"])
    assert result.exit_code == 0
    assert list(Series.from_lines(Path("descargas/norte.txt").read_text().splitlines())) == [
        Measurement("Norte", 10.0),
        Measurement("Norte", 60.5),
    ]
