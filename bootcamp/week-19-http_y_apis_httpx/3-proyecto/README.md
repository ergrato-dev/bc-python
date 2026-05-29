# Proyecto Semanal — Studio BC API Client

## Contexto

Studio BC integra servicios externos para gestionar su pipeline de producción:

- **MusicLicensing BC** — catálogo de música para spots y campañas (API Key)
- **CloudRender BC** — procesamiento de renders en la nube (Bearer Token)

El sistema debe funcionar aunque los servicios fallen temporalmente.

---

## Objetivo

Construir `studio-api-client`: un cliente Python que integra ambos proveedores con:

- Autenticación configurada por proveedor
- Retry con backoff exponencial en errores transitorios
- Timeouts granulares en todas las llamadas
- Respuestas validadas con Pydantic
- Ninguna llamada directa a `response.json()` sin validar

---

## Estructura

```
starter/
├── src/
│   ├── __init__.py
│   ├── models.py         # Pydantic models para ambos proveedores
│   ├── auth.py           # APIKeyAuth, BearerAuth (httpx.Auth)
│   ├── retry.py          # is_transient_error, retry decoradores
│   ├── music_client.py   # Cliente para MusicLicensing BC
│   └── render_client.py  # Cliente para CloudRender BC
├── tests/
│   └── test_clients.py
├── main.py               # Orquestador: busca música + lanza render
└── pyproject.toml
```

---

## Tareas

### 1. `src/models.py` — Modelos Pydantic

**MusicLicensing BC:**
```python
class Track(BaseModel):
    track_id: str
    title: str
    artist: str
    duration_secs: int
    genre: str
    license_type: str   # "royalty-free" | "licensed"
    price_usd: float

class TrackSearch(BaseModel):
    results: list[Track]
    total: int
    page: int
```

**CloudRender BC:**
```python
class RenderJob(BaseModel):
    job_id: str
    status: str   # "queued" | "processing" | "done" | "failed"
    progress: float   # 0.0 – 100.0
    output_url: str | None = None
    created_at: datetime

class RenderJobCreated(BaseModel):
    job_id: str
    estimated_secs: int
```

### 2. `src/auth.py` — Autenticación

- `APIKeyAuth(api_key, header_name="X-API-Key")` — para MusicLicensing
- `BearerAuth(token)` — para CloudRender

### 3. `src/retry.py` — Estrategia de retry

- `is_transient_error(exc)` — clasifica transitorios vs permanentes
- `MUSIC_RETRY` y `RENDER_RETRY` — decoradores `@retry(...)` pre-configurados para cada proveedor

### 4. `src/music_client.py` — Cliente de música

```python
class MusicClient:
    def __init__(self, api_key: str, base_url: str = "https://api.musiclicensing.bc") -> None: ...
    def search_tracks(self, genre: str, max_duration: int = 120) -> TrackSearch: ...
    def get_track(self, track_id: str) -> Track: ...
```

Requisitos:
- `httpx.Client` con `auth=APIKeyAuth(...)`, timeouts y `base_url`
- Retry en `search_tracks` y `get_track` usando `MUSIC_RETRY`
- Respuestas parseadas con los modelos Pydantic

### 5. `src/render_client.py` — Cliente de render

```python
class RenderClient:
    def __init__(self, token: str, base_url: str = "https://api.cloudrender.bc") -> None: ...
    def submit_job(self, project_id: str, track_id: str, resolution: str = "1080p") -> RenderJobCreated: ...
    def get_job_status(self, job_id: str) -> RenderJob: ...
    def wait_for_job(self, job_id: str, poll_interval: float = 2.0, max_wait: float = 120.0) -> RenderJob: ...
```

Requisitos:
- `httpx.Client` con `auth=BearerAuth(...)`, timeouts y `base_url`
- `wait_for_job` hace polling hasta que `status == "done"` o `max_wait` expire
- Levanta `TimeoutError` si supera `max_wait`

### 6. `main.py` — Orquestador

```python
def main() -> None:
    # 1. Buscar pistas de música genre=cinematic, max_duration=90
    # 2. Imprimir resultados con Rich (tabla: título, artista, precio)
    # 3. Si hay resultados, lanzar un render con la primera pista
    # 4. Imprimir el job_id y el estimated_secs
```

---

## Criterios de Aceptación

- [ ] `mypy --strict src/` pasa sin errores
- [ ] Todas las llamadas tienen `timeout=httpx.Timeout(connect=3.0, read=15.0)`
- [ ] No hay `response.json()` sin validación Pydantic
- [ ] `is_transient_error` cubre correctamente 429, 5xx y errores de red
- [ ] `MusicClient` y `RenderClient` usan `httpx.Auth` personalizado
- [ ] `wait_for_job` lanza `TimeoutError` si supera `max_wait`
