# Integración de Componentes

## Objetivos

- Gestionar configuración centralizada con `pydantic-settings`
- Inyectar la sesión de DB y los clientes HTTP sin acoplar capas
- Propagar errores entre capas de forma coherente
- Combinar async y sync en una CLI Typer

---

## 1. Configuración centralizada con pydantic-settings

```python
# src/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    database_url: str = "sqlite:///studio.db"
    exchange_api_url: str = "https://open.er-api.com/v6/latest"
    exchange_api_key: str = ""
    log_level: str = "WARNING"

# Singleton — instanciado una vez
settings = Settings()
```

Archivo `.env` de desarrollo:

```env
DATABASE_URL=sqlite:///studio_dev.db
EXCHANGE_API_KEY=your-key-here
LOG_LEVEL=INFO
```

---

## 2. Inyección de la sesión de DB

Patrón generador — compatible con FastAPI y CLI:

```python
# src/database.py
from collections.abc import Generator
from contextlib import contextmanager
from sqlmodel import Session, create_engine, SQLModel
from .config import settings

engine = create_engine(settings.database_url)

def create_tables() -> None:
    SQLModel.metadata.create_all(engine)

@contextmanager
def get_session_ctx() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
```

Uso en comandos Typer:

```python
# commands/projects.py
from src.database import get_session_ctx
from src.services.project_service import project_service

@projects_app.command("list")
def projects_list() -> None:
    with get_session_ctx() as session:
        items = project_service.list_active(session)
    _render_table(items)
```

---

## 3. Inyección del cliente HTTP

El cliente httpx se construye una vez y se reutiliza:

```python
# src/api_clients/exchange.py
import asyncio
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from pydantic import BaseModel
from ..config import settings

class ExchangeRates(BaseModel):
    base: str
    rates: dict[str, float]

class ExchangeClient:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            base_url=settings.exchange_api_url,
            timeout=httpx.Timeout(connect=3.0, read=10.0),
            headers={"User-Agent": "studio-bc-manager/1.0"},
        )

    async def __aenter__(self) -> "ExchangeClient":
        return self

    async def __aexit__(self, *args: object) -> None:
        await self._client.aclose()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
    async def get_rates(self, base: str = "USD") -> ExchangeRates:
        r = await self._client.get(f"/latest/{base}")
        r.raise_for_status()
        return ExchangeRates.model_validate(r.json())

exchange_client = ExchangeClient()
```

---

## 4. Combinar async y sync en Typer

Typer es sincrónico. Para llamadas async, usá `asyncio.run()`:

```python
# services/exchange_service.py
import asyncio
from ..api_clients.exchange import exchange_client

class ExchangeService:
    def get_ars_rate(self) -> float:
        """Obtiene ARS/USD de forma sincrónica para uso en CLI."""
        async def _fetch() -> float:
            async with exchange_client as client:
                rates = await client.get_rates("USD")
                return rates.rates.get("ARS", 1.0)

        return asyncio.run(_fetch())

exchange_service = ExchangeService()
```

Para múltiples llamadas concurrentes:

```python
async def _fetch_multiple() -> tuple[float, float]:
    async with exchange_client as client:
        ars_task = asyncio.create_task(client.get_rates("USD"))
        eur_task = asyncio.create_task(client.get_rates("EUR"))
        ars_rates, eur_rates = await asyncio.gather(ars_task, eur_task)
    return ars_rates.rates["ARS"], eur_rates.rates["USD"]

ars, eur = asyncio.run(_fetch_multiple())
```

---

## 5. Propagación de errores entre capas

Define excepciones de dominio propias — no expongas `httpx.HTTPStatusError` a la CLI:

```python
# src/exceptions.py
class StudioError(Exception):
    """Base para todos los errores de dominio."""

class NotFoundError(StudioError):
    def __init__(self, entity: str, id: int) -> None:
        super().__init__(f"{entity} con id={id} no encontrado")

class ExternalServiceError(StudioError):
    """Falla al contactar una API externa."""

class ValidationError(StudioError):
    """Datos de entrada inválidos."""
```

Conversión en la capa de servicio:

```python
# services/exchange_service.py
import httpx
from ..exceptions import ExternalServiceError

class ExchangeService:
    def get_ars_rate(self) -> float:
        try:
            return asyncio.run(self._fetch())
        except (httpx.ConnectError, httpx.TimeoutException) as e:
            raise ExternalServiceError(f"No se pudo contactar el servicio de cambio: {e}") from e
        except httpx.HTTPStatusError as e:
            raise ExternalServiceError(f"Error {e.response.status_code} del servicio") from e
```

Captura en la CLI con mensaje amigable:

```python
# commands/projects.py
from src.exceptions import NotFoundError, ExternalServiceError

@projects_app.command("create")
def projects_create(name: str, client_id: int, budget: float) -> None:
    try:
        with get_session_ctx() as session:
            project = project_service.create(session, name, client_id, budget)
        console.print(f"[green]Proyecto creado: {project.name} (id={project.id})[/]")
    except NotFoundError as e:
        console.print(f"[red]Error:[/] {e}")
        raise typer.Exit(1)
    except ExternalServiceError as e:
        console.print(f"[yellow]Advertencia:[/] tipo de cambio no disponible — {e}")
        # continuar sin tipo de cambio
```

---

## 6. Inicialización en `main.py`

```python
# main.py
import typer
from src.database import create_tables
from src.commands.clients import clients_app
from src.commands.projects import projects_app
from src.commands.assets import assets_app
from src.commands.report import report_app

app = typer.Typer(help="Studio BC — Gestión de producción")
app.add_typer(clients_app,  name="clients")
app.add_typer(projects_app, name="projects")
app.add_typer(assets_app,   name="assets")
app.add_typer(report_app,   name="report")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    create_tables()   # idempotente — crea si no existen
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())

if __name__ == "__main__":
    app()
```

---

## ✅ Resumen

| Problema | Solución |
|----------|----------|
| Configuración dispersa | `pydantic-settings` con `.env` |
| Sesión de DB acoplada | `get_session_ctx()` como context manager |
| Cliente HTTP global | Instancia única en `api_clients/` |
| Async en CLI sync | `asyncio.run()` en la capa de servicio |
| Errores de infraestructura | Convertir a excepciones de dominio en servicios |
