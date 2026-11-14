"""Tests de la semana 20: la API HTTP de api.py y el comando `servir`.

La fixture `client` sustituye get_session por la sesión de db_fixtures.py
(dependency_overrides): cada test habla con PostgreSQL de verdad, dentro de una
transacción que se deshace al terminar. Sin `with`, TestClient no ejecuta el lifespan
y la aplicación no abre su propio motor. Los tests que dicen "own engine" sí lo abren,
con `with`, y por eso usan db_env, que vacía las tablas.
"""

import subprocess
import sys
from collections.abc import Iterator, Mapping
from datetime import datetime
from pathlib import Path

import pytest
import uvicorn
from db_fixtures import TEST_URL
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import make_url
from sqlalchemy.orm import Session
from typer.testing import CliRunner

from observatorio import __version__, api, cli
from observatorio.core import make_engine

runner = CliRunner()

NORTE: dict[str, object] = {
    "source": "norte.txt",
    "measurements": [
        {"label": "Norte", "value": 12.5},
        {"label": "Sur", "value": None},
        {"label": "Norte", "value": 7.5},
    ],
}
ESTE: dict[str, object] = {"source": "este.csv", "measurements": [{"label": "Este", "value": 3}]}


@pytest.fixture
def client(session: Session) -> Iterator[TestClient]:
    """Un cliente de la API cuyas peticiones usan la sesión del test."""
    app = api.create_app(TEST_URL)
    app.dependency_overrides[api.get_session] = lambda: session
    with TestClient(app) as client:
        # El lifespan sí se ejecuta (abre un motor que nadie usa): así se prueba también.
        yield client


def post(client: TestClient, body: Mapping[str, object]) -> int:
    """Guarda una carga por la API y devuelve su número."""
    response = client.post("/loads", json=body)
    assert response.status_code == 201
    load_id = response.json()["id"]
    assert isinstance(load_id, int)
    return load_id


# --- GET /health -------------------------------------------------------------------------


def test_health_says_ok_and_the_version(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": __version__}


def test_responses_are_json(client: TestClient) -> None:
    assert client.get("/health").headers["content-type"] == "application/json"


# --- POST /loads ------------------------------------------------------------------------


def test_post_load_returns_201_and_the_new_load(client: TestClient) -> None:
    response = client.post("/loads", json=NORTE)
    assert response.status_code == 201
    body = response.json()
    assert set(body) == {"id", "source", "created_at", "measurements"}
    assert body["source"] == "norte.txt"
    assert body["measurements"] == 3


def test_post_load_says_where_the_new_load_is(client: TestClient) -> None:
    response = client.post("/loads", json=NORTE)
    assert response.headers["location"] == f"/loads/{response.json()['id']}"


def test_post_load_dates_are_iso_8601_with_time_zone(client: TestClient) -> None:
    created = datetime.fromisoformat(client.post("/loads", json=NORTE).json()["created_at"])
    assert created.tzinfo is not None


def test_each_load_gets_its_own_number(client: TestClient) -> None:
    first = post(client, NORTE)
    second = post(client, ESTE)
    assert second > first


def test_post_load_accepts_the_values_of_the_json_files(client: TestClient) -> None:
    body = {"source": "texto", "measurements": [{"label": " Norte ", "value": "12,5"}]}
    load_id = post(client, body)
    response = client.get(f"/loads/{load_id}/measurements")
    assert response.json() == [{"label": "Norte", "value": 12.5}]


def test_post_load_accepts_na_as_a_missing_value(client: TestClient) -> None:
    load_id = post(client, {"source": "x", "measurements": [{"label": "Sur", "value": "NA"}]})
    assert client.get(f"/loads/{load_id}/measurements").json() == [{"label": "Sur", "value": None}]


@pytest.mark.parametrize(
    "body",
    [
        pytest.param({"measurements": NORTE["measurements"]}, id="no source"),
        pytest.param({"source": "", "measurements": NORTE["measurements"]}, id="empty source"),
        pytest.param(
            {"source": "x" * 501, "measurements": NORTE["measurements"]}, id="long source"
        ),
        pytest.param({"source": "x"}, id="no measurements"),
        pytest.param({"source": "x", "measurements": []}, id="empty measurements"),
        pytest.param({**NORTE, "extra": 1}, id="unknown key"),
        pytest.param({"source": "x", "measurements": [{"label": ""}]}, id="no value"),
        pytest.param(
            {"source": "x", "measurements": [{"label": "", "value": 1}]}, id="empty label"
        ),
        pytest.param(
            {"source": "x", "measurements": [{"label": "N" * 101, "value": 1}]}, id="long label"
        ),
        pytest.param(
            {"source": "x", "measurements": [{"label": "N", "value": True}]}, id="boolean value"
        ),
        pytest.param(
            {"source": "x", "measurements": [{"label": "N", "value": "doce"}]}, id="text value"
        ),
        pytest.param(
            {"source": "x", "measurements": [{"label": "N", "value": 1, "unit": "u"}]},
            id="unknown measurement key",
        ),
    ],
)
def test_post_load_rejects_invalid_bodies_with_422(
    client: TestClient, body: dict[str, object]
) -> None:
    assert client.post("/loads", json=body).status_code == 422
    assert client.get("/loads").json() == []


def test_a_label_of_100_characters_is_valid(client: TestClient) -> None:
    post(client, {"source": "x", "measurements": [{"label": "N" * 100, "value": 1}]})


def test_422_says_where_the_problem_is(client: TestClient) -> None:
    body = {"source": "x", "measurements": [{"label": "N", "value": 1}, {"label": "", "value": 2}]}
    detail = client.post("/loads", json=body).json()["detail"]
    assert [error["loc"] for error in detail] == [["body", "measurements", 1, "label"]]


def test_post_load_without_json_is_422(client: TestClient) -> None:
    assert client.post("/loads", content="Norte;12,5").status_code == 422


# --- GET /loads y GET /loads/{id}/measurements ----------------------------------------


def test_loads_is_an_empty_list_at_first(client: TestClient) -> None:
    response = client.get("/loads")
    assert response.status_code == 200
    assert response.json() == []


def test_loads_lists_every_load_with_its_measurements(client: TestClient) -> None:
    first = post(client, NORTE)
    second = post(client, ESTE)
    loads = client.get("/loads").json()
    assert [(load["id"], load["source"], load["measurements"]) for load in loads] == [
        (first, "norte.txt", 3),
        (second, "este.csv", 1),
    ]


def test_measurements_come_back_in_their_order(client: TestClient) -> None:
    load_id = post(client, NORTE)
    response = client.get(f"/loads/{load_id}/measurements")
    assert response.status_code == 200
    assert response.json() == NORTE["measurements"]


def test_measurements_of_a_missing_load_are_404(client: TestClient) -> None:
    response = client.get("/loads/999/measurements")
    assert response.status_code == 404
    assert response.json() == {"detail": "no existe la carga 999"}


def test_the_load_number_must_be_an_integer(client: TestClient) -> None:
    response = client.get("/loads/norte/measurements")
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["path", "load_id"]


# --- DELETE /loads/{id} -----------------------------------------------------------------


def test_delete_returns_204_without_a_body(client: TestClient) -> None:
    response = client.delete(f"/loads/{post(client, NORTE)}")
    assert response.status_code == 204
    assert response.content == b""


def test_delete_removes_the_load_and_its_measurements(client: TestClient) -> None:
    load_id = post(client, NORTE)
    keep = post(client, ESTE)
    client.delete(f"/loads/{load_id}")
    assert client.get(f"/loads/{load_id}/measurements").status_code == 404
    assert [load["id"] for load in client.get("/loads").json()] == [keep]


def test_delete_a_missing_load_is_404(client: TestClient) -> None:
    response = client.delete("/loads/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "no existe la carga 999"}


# --- GET /stats -------------------------------------------------------------------------


def test_stats_of_every_load(client: TestClient) -> None:
    post(client, NORTE)
    post(client, ESTE)
    assert client.get("/stats").json() == [
        {"label": "Este", "measurements": 1, "with_value": 1, "mean": 3.0},
        {"label": "Norte", "measurements": 2, "with_value": 2, "mean": 10.0},
        {"label": "Sur", "measurements": 1, "with_value": 0, "mean": None},
    ]


def test_stats_of_one_load(client: TestClient) -> None:
    post(client, NORTE)
    load_id = post(client, ESTE)
    response = client.get("/stats", params={"load": load_id})
    assert response.json() == [{"label": "Este", "measurements": 1, "with_value": 1, "mean": 3.0}]


def test_stats_without_loads_is_an_empty_list(client: TestClient) -> None:
    assert client.get("/stats").json() == []


def test_stats_of_a_missing_load_are_404(client: TestClient) -> None:
    response = client.get("/stats", params={"load": 999})
    assert response.status_code == 404
    assert response.json() == {"detail": "no existe la carga 999"}


def test_stats_load_must_be_an_integer(client: TestClient) -> None:
    response = client.get("/stats", params={"load": "uno"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "load"]


# --- Lo que FastAPI hace solo ------------------------------------------------------------


def test_openapi_describes_every_route(client: TestClient) -> None:
    schema = client.get("/openapi.json").json()
    assert schema["info"] == {"title": "Observatorio", "version": __version__}
    paths = {path: sorted(methods) for path, methods in schema["paths"].items()}
    assert paths == {
        "/health": ["get"],
        "/loads": ["get", "post"],
        "/loads/{load_id}": ["delete"],
        "/loads/{load_id}/measurements": ["get"],
        "/stats": ["get"],
    }


def test_docs_is_an_html_page(client: TestClient) -> None:
    response = client.get("/docs")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")


def test_an_unknown_route_is_404(client: TestClient) -> None:
    assert client.get("/medidas").status_code == 404


def test_a_wrong_method_is_405(client: TestClient) -> None:
    assert client.put("/loads", json=NORTE).status_code == 405


# --- Sin PostgreSQL ---------------------------------------------------------------------


@pytest.fixture
def broken_client() -> Iterator[TestClient]:
    """Un cliente cuya sesión apunta a un PostgreSQL que no existe (puerto 1)."""
    url = make_url(TEST_URL).set(port=1, password="secreto-de-prueba")
    engine = make_engine(url.render_as_string(hide_password=False))
    app = api.create_app(TEST_URL)

    def broken_session() -> Iterator[Session]:
        with Session(engine) as session:
            yield session

    app.dependency_overrides[api.get_session] = broken_session
    yield TestClient(app)
    engine.dispose()


@pytest.mark.parametrize("path", ["/health", "/loads", "/stats"])
def test_without_postgres_the_api_answers_503(broken_client: TestClient, path: str) -> None:
    response = broken_client.get(path)
    assert response.status_code == 503
    assert response.json() == {"detail": "no se pudo conectar con PostgreSQL"}


def test_the_503_does_not_show_the_password(broken_client: TestClient) -> None:
    assert "secreto" not in broken_client.get("/loads").text


# --- Con su propio motor (lifespan) ------------------------------------------------------


def test_own_engine_post_load_commits(db_env: Path) -> None:
    with TestClient(api.create_app(TEST_URL)) as client:
        load_id = post(client, NORTE)
    # Otra aplicación, otro motor, otras conexiones: solo ve lo confirmado.
    with TestClient(api.create_app(TEST_URL)) as client:
        assert [load["id"] for load in client.get("/loads").json()] == [load_id]


def test_own_engine_delete_commits(db_env: Path) -> None:
    with TestClient(api.create_app(TEST_URL)) as client:
        client.delete(f"/loads/{post(client, NORTE)}")
    with TestClient(api.create_app(TEST_URL)) as client:
        assert client.get("/loads").json() == []


def test_own_engine_is_closed_when_the_app_stops(db_env: Path) -> None:
    app = api.create_app(TEST_URL)
    with TestClient(app) as client:
        client.get("/health")
        assert app.state.engine.pool.checkedin() == 1
    assert app.state.engine.pool.checkedin() == 0


# --- observatorio servir ----------------------------------------------------------------


@pytest.fixture
def served(db_env: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, object]:
    """Sustituye uvicorn.run: apunta con qué se llamó, en lugar de servir para siempre."""
    calls: dict[str, object] = {}

    def fake_run(app: FastAPI, *, host: str, port: int) -> None:
        calls.update(app=app, host=host, port=port)

    monkeypatch.setattr(uvicorn, "run", fake_run)
    return calls


def test_servir_runs_uvicorn_with_the_api(served: dict[str, object]) -> None:
    result = runner.invoke(cli.app, ["servir"])
    assert result.exit_code == 0, result.output
    assert isinstance(served["app"], FastAPI)
    assert (served["host"], served["port"]) == ("127.0.0.1", 8000)


def test_servir_serves_the_routes_of_the_api(served: dict[str, object]) -> None:
    runner.invoke(cli.app, ["servir"])
    app = served["app"]
    assert isinstance(app, FastAPI)
    with TestClient(app) as client:
        assert client.get("/loads").json() == []


@pytest.mark.parametrize("flag", ["--puerto", "-p"])
def test_servir_with_host_and_port(served: dict[str, object], flag: str) -> None:
    result = runner.invoke(cli.app, ["servir", "--host", "0.0.0.0", flag, "8080"])
    assert result.exit_code == 0, result.output
    assert (served["host"], served["port"]) == ("0.0.0.0", 8080)


@pytest.mark.parametrize("port", ["0", "65536"])
def test_servir_rejects_impossible_ports(served: dict[str, object], port: str) -> None:
    assert runner.invoke(cli.app, ["servir", "-p", port]).exit_code == 2
    assert served == {}


def test_servir_without_database_url(
    served: dict[str, object], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("OBSERVATORIO_DATABASE_URL")
    result = runner.invoke(cli.app, ["servir"])
    assert result.exit_code == 2
    assert result.stderr == "error: falta OBSERVATORIO_DATABASE_URL (en el entorno o en .env)\n"
    assert served == {}


@pytest.mark.parametrize("url", ["nada", "nada://usuario@servidor/base"])
def test_servir_with_an_invalid_database_url(
    served: dict[str, object], monkeypatch: pytest.MonkeyPatch, url: str
) -> None:
    monkeypatch.setenv("OBSERVATORIO_DATABASE_URL", url)
    result = runner.invoke(cli.app, ["servir"])
    assert result.exit_code == 2
    assert "no es una URL de base de datos válida" in result.stderr
    assert served == {}


def test_servir_help() -> None:
    result = runner.invoke(cli.app, ["servir", "--help"])
    assert result.exit_code == 0
    assert "--puerto" in result.output
    assert "/docs" in result.output


def test_the_cli_loads_fastapi_only_to_serve() -> None:
    # Importar la API cuesta tiempo: --version, informe o guardar no deben pagarlo.
    code = "import sys, observatorio.cli; print('fastapi' in sys.modules)"
    result = subprocess.run(
        [sys.executable, "-c", code], check=False, capture_output=True, text=True
    )
    assert result.stdout == "False\n"
