# httpx — Fundamentos

## Objetivos

- Entender por qué httpx reemplaza a requests en código moderno
- Usar `httpx.Client` para sesiones reutilizables (sync)
- Usar `httpx.AsyncClient` para llamadas concurrentes (async)
- Inspeccionar el objeto `Response`: status, headers, JSON, texto

---

## 1. httpx vs requests

| Aspecto | requests | httpx |
|---------|----------|-------|
| API async | No | Sí (`AsyncClient`) |
| HTTP/2 | No | Sí (opcional) |
| Type hints | Parcial | Completo |
| Timeouts | Solo `timeout=` | Granular (connect/read/write) |
| Transports | No | Sí (mock, WSGI, ASGI) |
| Mantenimiento | Legacy | Activo |

```python
# requests — bloqueante, no async
import requests
r = requests.get("https://api.studio.bc/projects")

# httpx — sync y async, misma API de superficie
import httpx
r = httpx.get("https://api.studio.bc/projects")
```

---

## 2. One-shot vs `Client`

```python
import httpx

# One-shot — abre y cierra conexión TCP en cada llamada
response = httpx.get("https://api.studio.bc/projects")

# Client — reutiliza conexiones (connection pooling)
# Recomendado cuando se hacen varias llamadas al mismo host
with httpx.Client(base_url="https://api.studio.bc") as client:
    projects = client.get("/projects")
    assets   = client.get("/assets")
    # la conexión TCP se reutiliza — más rápido
```

El `Client` (context manager) garantiza que las conexiones se cierran correctamente.

---

## 3. Parámetros, headers y body

```python
import httpx

with httpx.Client(base_url="https://api.studio.bc") as client:
    # Query params — se codifican en la URL
    response = client.get("/assets", params={
        "project_id": "reel-2025",
        "type": "video",
        "page": 1,
    })
    # → GET /assets?project_id=reel-2025&type=video&page=1

    # Headers personalizados
    response = client.get("/projects", headers={
        "X-Client-Version": "1.0",
        "Accept-Language": "es",
    })

    # POST con JSON body
    response = client.post("/projects", json={
        "project_id": "new-spot",
        "client": "Canal 9",
        "budget": 5000.0,
    })

    # POST con form data
    response = client.post("/upload", data={
        "name": "intro.mp4",
        "type": "video",
    })

    # POST con archivo
    with open("intro.mp4", "rb") as f:
        response = client.post("/upload", files={"file": f})
```

---

## 4. El objeto `Response`

```python
response = client.get("/projects/reel-2025")

# Status
print(response.status_code)          # 200
print(response.is_success)           # True (2xx)
print(response.is_client_error)      # False (4xx)
print(response.is_server_error)      # False (5xx)

# Lanzar excepción si no es 2xx
response.raise_for_status()          # HTTPStatusError si 4xx/5xx

# Body
data = response.json()               # dict / list
text = response.text                 # str
raw  = response.content              # bytes

# Headers de respuesta
content_type = response.headers["content-type"]
rate_limit   = response.headers.get("x-ratelimit-remaining")

# URL final (después de redirects)
print(response.url)
```

---

## 5. `AsyncClient` — async/await

```python
import asyncio
import httpx

async def fetch_all_projects() -> list[dict]:
    async with httpx.AsyncClient(base_url="https://api.studio.bc") as client:
        response = await client.get("/projects")
        response.raise_for_status()
        return response.json()

async def main() -> None:
    # Llamadas concurrentes con asyncio.gather
    async with httpx.AsyncClient(base_url="https://api.studio.bc") as client:
        projects_task = asyncio.create_task(client.get("/projects"))
        assets_task   = asyncio.create_task(client.get("/assets"))

        projects_resp, assets_resp = await asyncio.gather(
            projects_task, assets_task
        )

    print(projects_resp.json())
    print(assets_resp.json())

asyncio.run(main())
```

---

## 6. Timeouts

```python
import httpx

# Timeout global (aplica a connect + read + write)
client = httpx.Client(timeout=10.0)

# Timeouts granulares
timeout = httpx.Timeout(
    connect=3.0,   # tiempo máximo para establecer conexión TCP
    read=10.0,     # tiempo máximo para recibir la respuesta
    write=5.0,     # tiempo máximo para enviar el body
    pool=2.0,      # tiempo máximo esperando conexión del pool
)
client = httpx.Client(timeout=timeout)

# Sin timeout — peligroso en producción
client = httpx.Client(timeout=None)

# Por-request (sobreescribe el del cliente)
response = client.get("/large-file", timeout=60.0)
```

---

## 7. Configuración del cliente

```python
import httpx

client = httpx.Client(
    base_url="https://api.studio.bc",
    headers={"User-Agent": "studio-bc-client/1.0"},
    timeout=httpx.Timeout(connect=3.0, read=15.0),
    follow_redirects=True,
    verify=True,          # verificar SSL (default True)
    limits=httpx.Limits(
        max_connections=20,
        max_keepalive_connections=10,
    ),
)
```

---

## ✅ Resumen

| Concepto | API |
|---------|-----|
| Llamada puntual | `httpx.get()` / `httpx.post()` |
| Sesión reutilizable (sync) | `with httpx.Client(...) as c:` |
| Sesión reutilizable (async) | `async with httpx.AsyncClient(...) as c:` |
| Params en URL | `client.get("/path", params={...})` |
| JSON body | `client.post("/path", json={...})` |
| Verificar status | `response.raise_for_status()` |
| Timeouts granulares | `httpx.Timeout(connect=, read=, write=)` |

---

## Recursos Adicionales

- [httpx docs](https://www.python-httpx.org/)
- [httpx — Clients](https://www.python-httpx.org/advanced/clients/)
