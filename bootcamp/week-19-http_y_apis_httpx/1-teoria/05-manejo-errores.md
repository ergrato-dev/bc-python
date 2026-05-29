# Manejo de Errores HTTP

## Objetivos

- Distinguir y manejar `HTTPStatusError`, `ConnectError` y `TimeoutException`
- Validar respuestas JSON con modelos Pydantic
- Construir un manejador de errores centralizado y reutilizable
- Evitar crasheos silenciosos por respuestas inesperadas

---

## 1. Jerarquía de excepciones de httpx

```
httpx.HTTPError
├── httpx.TransportError
│   ├── httpx.TimeoutException
│   │   ├── httpx.ConnectTimeout
│   │   ├── httpx.ReadTimeout
│   │   ├── httpx.WriteTimeout
│   │   └── httpx.PoolTimeout
│   ├── httpx.NetworkError
│   │   ├── httpx.ConnectError
│   │   └── httpx.ReadError
│   └── httpx.TooManyRedirects
└── httpx.HTTPStatusError       # response.raise_for_status()
```

Regla práctica:
- **`ConnectError` / `ConnectTimeout`** → servidor inaccesible → reintentar
- **`ReadTimeout`** → respuesta tardó demasiado → reintentar con timeout mayor
- **`HTTPStatusError` 5xx / 429** → error transitorio → reintentar
- **`HTTPStatusError` 4xx** → error permanente → no reintentar, reportar al usuario

---

## 2. Manejo básico por tipo de error

```python
import httpx

def call_api(client: httpx.Client, path: str) -> dict:
    try:
        response = client.get(path, timeout=10.0)
        response.raise_for_status()
        return response.json()

    except httpx.ConnectTimeout:
        print(f"No se pudo conectar al servidor en {path}")
        raise

    except httpx.ReadTimeout:
        print(f"Timeout leyendo respuesta de {path}")
        raise

    except httpx.ConnectError as e:
        print(f"Error de red: {e}")
        raise

    except httpx.HTTPStatusError as e:
        status = e.response.status_code
        if status == 401:
            print("No autorizado — verifica el token")
        elif status == 403:
            print("Acceso prohibido — sin permisos suficientes")
        elif status == 404:
            print(f"Recurso no encontrado: {path}")
        elif status == 429:
            retry_after = e.response.headers.get("Retry-After", "desconocido")
            print(f"Rate limit superado — esperar {retry_after}s")
        elif status >= 500:
            print(f"Error del servidor ({status}) — reintentar más tarde")
        raise
```

---

## 3. Validar respuestas con Pydantic

Nunca acceder a `response.json()` sin validar su estructura:

```python
from __future__ import annotations
from pydantic import BaseModel, ValidationError
import httpx

class Project(BaseModel):
    project_id: str
    client: str
    budget: float
    status: str

class ProjectList(BaseModel):
    items: list[Project]
    total: int

def get_projects(client: httpx.Client) -> ProjectList:
    response = client.get("/projects", timeout=10.0)
    response.raise_for_status()

    try:
        return ProjectList.model_validate(response.json())
    except ValidationError as e:
        print(f"Respuesta inesperada de la API:\n{e}")
        raise
```

### Modelo con campos opcionales y aliases

```python
from pydantic import BaseModel, Field, AliasChoices
from datetime import datetime

class Asset(BaseModel):
    asset_id: str = Field(alias="id", validation_alias=AliasChoices("id", "asset_id"))
    name: str
    size_mb: float = Field(gt=0)
    created_at: datetime
    tags: list[str] = Field(default_factory=list)

# Tolera tanto {"id": ...} como {"asset_id": ...}
asset = Asset.model_validate({"id": "a1", "name": "intro.mp4", "size_mb": 45.2, "created_at": "2025-01-01T00:00:00Z"})
```

---

## 4. Función de parseo defensiva

```python
from typing import TypeVar
from pydantic import BaseModel, ValidationError
import httpx

T = TypeVar("T", bound=BaseModel)

def parse_response(response: httpx.Response, model: type[T]) -> T:
    """Valida la respuesta HTTP con el modelo Pydantic dado."""
    response.raise_for_status()

    content_type = response.headers.get("content-type", "")
    if "application/json" not in content_type:
        raise ValueError(
            f"Se esperaba JSON pero se recibió: {content_type!r}"
        )

    try:
        return model.model_validate(response.json())
    except ValidationError as e:
        raise ValueError(f"Schema de respuesta inesperado: {e}") from e

# Uso
with httpx.Client(base_url="https://api.studio.bc") as client:
    resp = client.get("/projects")
    projects = parse_response(resp, ProjectList)
```

---

## 5. Manejador centralizado de errores HTTP

```python
import httpx
import logging

logger = logging.getLogger(__name__)

class APIError(Exception):
    """Error de negocio de la API — ya logueado y listo para mostrar al usuario."""
    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code

def handle_http_error(exc: Exception, context: str = "") -> None:
    """Loguea y re-lanza como APIError si el error es permanente."""
    prefix = f"[{context}] " if context else ""

    if isinstance(exc, httpx.HTTPStatusError):
        status = exc.response.status_code
        logger.error(f"{prefix}HTTP {status}: {exc.request.url}")
        if 400 <= status < 500:
            raise APIError(f"Error del cliente ({status})", status_code=status) from exc
        # 5xx → dejar que tenacity reintente
        raise exc

    if isinstance(exc, (httpx.ConnectError, httpx.TimeoutException)):
        logger.warning(f"{prefix}Error de red: {exc}")
        raise exc  # tenacity reintenta

    logger.error(f"{prefix}Error inesperado: {exc}")
    raise exc

# Integración
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception

TRANSIENT = (httpx.ConnectError, httpx.TimeoutException)

def is_retriable(exc: BaseException) -> bool:
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in {429, 500, 502, 503, 504}
    return isinstance(exc, TRANSIENT)

@retry(
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=1, min=1, max=20),
    retry=retry_if_exception(is_retriable),
    reraise=True,
)
def robust_call(client: httpx.Client, path: str) -> dict:
    try:
        response = client.get(path, timeout=10.0)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        handle_http_error(e, context=path)
        raise  # nunca llega aquí — handle_http_error siempre lanza
```

---

## 6. Logging estructurado de respuestas

```python
import httpx
import logging
import time

logger = logging.getLogger(__name__)

class LoggingTransport(httpx.BaseTransport):
    """Transport que loguea cada request/response con su duración."""

    def __init__(self, wrapped: httpx.BaseTransport) -> None:
        self._wrapped = wrapped

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        start = time.monotonic()
        response = self._wrapped.handle_request(request)
        elapsed = time.monotonic() - start
        logger.info(
            "HTTP %s %s → %d (%.2fs)",
            request.method,
            request.url,
            response.status_code,
            elapsed,
        )
        return response

# Uso
transport = LoggingTransport(httpx.HTTPTransport())
with httpx.Client(base_url="https://api.studio.bc", transport=transport) as client:
    client.get("/projects")
```

---

## ✅ Resumen

| Excepción | Causa | Acción |
|-----------|-------|--------|
| `ConnectTimeout` / `ConnectError` | Servidor inaccesible | Reintentar con backoff |
| `ReadTimeout` | Respuesta lenta | Reintentar, o aumentar `read=` |
| `HTTPStatusError` 4xx | Error del cliente (401, 403, 404) | No reintentar — reportar |
| `HTTPStatusError` 429 | Rate limit | Esperar `Retry-After` y reintentar |
| `HTTPStatusError` 5xx | Error del servidor | Reintentar |
| `ValidationError` | Respuesta no coincide con schema | Log + excepción informativa |

---

## Recursos Adicionales

- [httpx — Exceptions](https://www.python-httpx.org/exceptions/)
- [Pydantic — Models](https://docs.pydantic.dev/latest/concepts/models/)
