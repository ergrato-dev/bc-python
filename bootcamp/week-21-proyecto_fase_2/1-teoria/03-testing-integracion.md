# Testing de Integración

## Objetivos

- Testear servicios con base de datos en memoria (SQLite `:memory:`)
- Mockear clientes HTTP sin tocar la red
- Estructurar fixtures de pytest reutilizables
- Distinguir tests unitarios de tests de integración

---

## 1. Fixture de sesión con DB en memoria

```python
# tests/conftest.py
import pytest
from sqlmodel import SQLModel, Session, create_engine
from src.models import Client, Project, Asset

@pytest.fixture(name="engine", scope="function")
def engine_fixture():
    """Engine SQLite en memoria — aislado por test."""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="session")
def session_fixture(engine):
    with Session(engine) as session:
        yield session

@pytest.fixture(name="sample_client")
def sample_client_fixture(session: Session) -> Client:
    client = Client(name="Canal 9", email="prod@canal9.com", country="AR")
    session.add(client)
    session.commit()
    session.refresh(client)
    return client

@pytest.fixture(name="sample_project")
def sample_project_fixture(session: Session, sample_client: Client) -> Project:
    project = Project(
        name="Spot Verano", client_id=sample_client.id, budget=5000.0
    )
    session.add(project)
    session.commit()
    session.refresh(project)
    return project
```

---

## 2. Testear servicios (integración con DB)

```python
# tests/test_project_service.py
import pytest
from sqlmodel import Session
from src.services.project_service import ProjectService
from src.repositories.project import ProjectRepository
from src.exceptions import NotFoundError

@pytest.fixture
def service() -> ProjectService:
    return ProjectService(project_repo=ProjectRepository())

def test_create_project(session: Session, service: ProjectService, sample_client) -> None:
    project = service.create(session, "Test", sample_client.id, 1000.0)
    assert project.id is not None
    assert project.name == "Test"
    assert project.budget == 1000.0

def test_create_project_invalid_client(session: Session, service: ProjectService) -> None:
    with pytest.raises(NotFoundError):
        service.create(session, "Test", client_id=9999, budget=0.0)

def test_list_active_excludes_inactive(
    session: Session, service: ProjectService, sample_client
) -> None:
    service.create(session, "Activo", sample_client.id, 100.0)
    p2 = service.create(session, "Inactivo", sample_client.id, 100.0)
    service.deactivate(session, p2.id)

    active = service.list_active(session)
    names = [p.name for p in active]
    assert "Activo" in names
    assert "Inactivo" not in names
```

---

## 3. Mockear el cliente HTTP

Para tests que involucran llamadas a APIs externas, usá `pytest-httpx` o un fake manual:

```python
# tests/test_exchange_service.py
import pytest
import httpx
from unittest.mock import AsyncMock, patch
from src.services.exchange_service import ExchangeService
from src.exceptions import ExternalServiceError

def test_get_ars_rate_success() -> None:
    mock_rates = {"base": "USD", "rates": {"ARS": 1050.0, "EUR": 0.92}}

    async def fake_get_rates(base: str = "USD"):
        from src.api_clients.exchange import ExchangeRates
        return ExchangeRates(base=base, rates=mock_rates["rates"])

    service = ExchangeService()
    with patch.object(service, "_fetch", new_callable=AsyncMock) as mock:
        mock.return_value = 1050.0
        # Si tu servicio envuelve el fetch, mockear a ese nivel
    # Alternativa: inyectar el cliente como dependencia (más testeable)

def test_get_ars_rate_network_error() -> None:
    """Verifica que ExternalServiceError se lanza ante fallo de red."""
    service = ExchangeService()

    async def failing_fetch() -> float:
        raise httpx.ConnectError("timeout")

    with patch.object(service, "_async_fetch", side_effect=httpx.ConnectError("down")):
        with pytest.raises(ExternalServiceError):
            service.get_ars_rate()
```

### Alternativa: inyectar el cliente como dependencia (más limpia)

```python
# src/services/exchange_service.py
from ..api_clients.exchange import ExchangeClient

class ExchangeService:
    def __init__(self, client: ExchangeClient | None = None) -> None:
        self._client = client or ExchangeClient()

# tests/test_exchange_service.py
class FakeExchangeClient:
    async def get_rates(self, base: str = "USD"):
        from src.api_clients.exchange import ExchangeRates
        return ExchangeRates(base=base, rates={"ARS": 1050.0})

def test_with_fake_client() -> None:
    service = ExchangeService(client=FakeExchangeClient())
    rate = service.get_ars_rate()
    assert rate == 1050.0
```

---

## 4. Testear el reporte con Polars

```python
# tests/test_report_service.py
import polars as pl
from sqlmodel import Session
from src.services.report_service import ReportService

def test_report_generates_dataframe(
    session: Session, sample_project, sample_client
) -> None:
    service = ReportService()
    df = service.generate_project_report(session)

    assert isinstance(df, pl.DataFrame)
    assert "project_name" in df.columns
    assert "budget" in df.columns
    assert len(df) >= 1

def test_report_totals(session: Session, sample_client) -> None:
    from src.models import Project
    session.add_all([
        Project(name="P1", client_id=sample_client.id, budget=1000.0),
        Project(name="P2", client_id=sample_client.id, budget=3000.0),
    ])
    session.commit()

    service = ReportService()
    df = service.generate_project_report(session)
    total = df.select(pl.sum("budget")).item()
    assert total == 4000.0
```

---

## 5. Testear comandos Typer con CliRunner

```python
# tests/test_commands.py
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from main import app

runner = CliRunner()

def test_projects_list_empty(engine_fixture) -> None:
    # Parchear get_session_ctx para usar el engine de test
    with patch("src.commands.projects.get_session_ctx") as mock_ctx:
        mock_session = MagicMock()
        mock_ctx.return_value.__enter__ = lambda s: mock_session
        mock_ctx.return_value.__exit__ = MagicMock(return_value=False)
        with patch("src.services.project_service.project_service.list_active", return_value=[]):
            result = runner.invoke(app, ["projects", "list"])
    assert result.exit_code == 0

def test_projects_create_not_found_client() -> None:
    with patch("src.commands.projects.project_service") as mock_svc:
        from src.exceptions import NotFoundError
        mock_svc.create.side_effect = NotFoundError("Client", 9999)
        result = runner.invoke(app, ["projects", "create", "--name", "X", "--client-id", "9999", "--budget", "100"])
    assert result.exit_code == 1
```

---

## 6. Organización de tests

```
tests/
├── conftest.py               # fixtures compartidas
├── test_project_service.py   # integración con DB
├── test_exchange_service.py  # mockea HTTP
├── test_report_service.py    # Polars
└── test_commands.py          # CLI con CliRunner
```

Correr:
```bash
pytest tests/ -v
pytest tests/ -v --tb=short   # traceback corto
pytest tests/test_project_service.py -k "test_create"   # filtrar
```

---

## ✅ Resumen

| Qué testear | Herramienta | Fixture clave |
|-------------|-------------|---------------|
| Servicios + DB | pytest + SQLite `:memory:` | `session_fixture` |
| Clientes HTTP | Fake o `patch` | `FakeExchangeClient` |
| Reportes Polars | Assertions sobre `pl.DataFrame` | `sample_project` |
| Comandos CLI | `typer.testing.CliRunner` | `patch` de servicios |
