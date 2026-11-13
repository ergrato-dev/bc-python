# Tus tests de la semana 20: sustituye este ejemplo por al menos 6 tests tuyos (paso 15).
# Con medidas de tu dominio, la fixture `client` de test_api.py copiada aquí y la de
# `session`: POST /loads de ida y vuelta, un cuerpo no válido con su 422 y su "loc",
# /stats de una carga, DELETE y su 404, una respuesta sin PostgreSQL y `servir`.
from collections.abc import Iterator

import pytest
from db_fixtures import TEST_URL
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from observatorio import api


@pytest.fixture
def client(session: Session) -> Iterator[TestClient]:
    app = api.create_app(TEST_URL)
    app.dependency_overrides[api.get_session] = lambda: session
    with TestClient(app) as client:
        yield client


def test_example_a_new_load_is_listed(client: TestClient) -> None:
    body = {"source": "ejemplo.txt", "measurements": [{"label": "Norte", "value": 12.5}]}
    load_id = client.post("/loads", json=body).json()["id"]
    assert [load["id"] for load in client.get("/loads").json()] == [load_id]
