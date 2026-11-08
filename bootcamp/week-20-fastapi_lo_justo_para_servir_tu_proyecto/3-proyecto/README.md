# Proyecto — Observatorio, capa 19: una API HTTP con FastAPI

⏱️ 6 h 30 min · Capa 19 del [proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md). **Único entregable de la semana.**

## Qué construyes

Tus cargas viven en PostgreSQL, pero solo las alcanza quien tiene el Observatorio y la contraseña de la base. Esta semana las sirves por **HTTP**: cualquier programa que hable HTTP y JSON puede listar, consultar, guardar y borrar cargas, sin saber que hay PostgreSQL detrás.

```
$ uv run observatorio servir
INFO:     Started server process [4182]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

```
$ curl -s -X POST http://127.0.0.1:8000/loads -H 'content-type: application/json' \
       -d '{"source": "curl", "measurements": [{"label": "Norte", "value": "12,5"}, {"label": "Sur", "value": null}]}'
{"id":1,"source":"curl","created_at":"2026-11-08T04:59:56.464382Z","measurements":2}
$ curl -s http://127.0.0.1:8000/stats
[{"label":"Norte","measurements":1,"with_value":1,"mean":12.5},{"label":"Sur","measurements":1,"with_value":0,"mean":null}]
```

| Ruta | Qué hace | Códigos |
|---|---|---|
| `GET /health` | Responde si la API está viva y PostgreSQL contesta, con la versión | 200, 503 |
| `GET /loads` | Las cargas, con su número, origen, fecha y medidas | 200 |
| `POST /loads` | Guarda una carga: `{"source": ..., "measurements": [{"label": ..., "value": ...}]}` | 201 con `Location`, 422 |
| `GET /loads/{id}/measurements` | Las medidas de una carga, en su orden | 200, 404 |
| `DELETE /loads/{id}` | Borra una carga y sus medidas | 204, 404 |
| `GET /stats?load=N` | Medidas, medidas con valor y media por etiqueta, de una carga o de todas | 200, 404 |

Y un comando: `observatorio servir [--host H] [-p PUERTO]`. La documentación de todo, en <http://127.0.0.1:8000/docs>.

```
src/observatorio/
├── api.py            # nuevo: create_app, get_session, las rutas, ReadingIn y LoadIn
└── cli.py            # + database_url (refactor) y el comando servir
tests/
├── test_api.py       # nuevo: los tests del bootcamp
├── test_my_api.py    # nuevo: los tuyos
└── test_package.py   # modificado: api fuera de core, las dependencias nuevas y 0.20.0
compose.yaml          # modificado: + el servicio api
```

`api.py`, como `cli.py`, es un **programa sobre `core`**: usa las funciones de `database.py` de la semana 19 sin cambiarlas, y no lee el entorno. La URL de la base le llega como argumento.

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-20`. El `starter/` trae la capa 18 resuelta. **Tú** escribes `api.py` y el comando `servir`.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-19` está fusionado en `main`. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-20
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-20-fastapi_lo_justo_para_servir_tu_proyecto/3-proyecto/starter
cp $STARTER/tests/test_api.py $STARTER/tests/test_my_api.py $STARTER/tests/test_package.py tests/
cp $STARTER/compose.yaml .
git status --short
```

Copias estos archivos:

- **Nuevos:**
  - `tests/test_api.py`, con 58 tests de la API y del comando `servir`;
  - `tests/test_my_api.py`, con un ejemplo y la fixture `client`.
- **Modificados:**
  - `test_package.py`, que espera `api.py` fuera de `core`, que `core` no importe FastAPI, las dependencias nuevas y la versión `0.20.0`;
  - `compose.yaml`, con el servicio `api` y la imagen `week-20`. Lee sus comentarios (teoría 05, sección 8).

### 3. Dependencias y tests en rojo

```bash
docker compose up -d --wait db
uv run pytest
```

```
E   ModuleNotFoundError: No module named 'uvicorn'
E   ModuleNotFoundError: No module named 'fastapi'
...
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Añade las dependencias, con la versión fijada (`docs/stack-versions.md`, con su fecha y su revisión de avisos de seguridad):

```bash
uv add fastapi==0.162.0 uvicorn==0.54.0
uv add --dev httpx2==2.16.0
uv run pytest
```

```
E   ImportError: cannot import name 'api' from 'observatorio' (...)
...
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

`fastapi` trae `starlette` (las rutas y las respuestas ASGI) y `opentelemetry-api`; `uvicorn` trae `click`. `httpx2` va en `dev` porque solo lo usa `TestClient`, en los tests (teoría 05, sección 1). Míralos en `uv.lock`.

Lee `tests/test_api.py` antes de escribir nada. Fíjate en (teoría 05):

- la fixture `client` crea la aplicación con `create_app(TEST_URL)` y le cambia `get_session` por la sesión del test;
- los tests `own_engine` usan el motor de la aplicación, sin override, para probar el `commit`;
- `broken_client` apunta a un PostgreSQL que no existe, con una contraseña que no debe salir;
- `served` sustituye `uvicorn.run`, para probar `servir` sin servir.

### 4. El esqueleto: `api.py`

Crea `src/observatorio/api.py` con un *docstring* de módulo (qué, para qué, impacto), y:

```python
from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Request, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from observatorio import __version__
from observatorio.core import (
    LabelStats,
    LoadInfo,
    Measurement,
    MeasurementIn,
    make_engine,
)


class ReadingIn(MeasurementIn):
    """Una medida en el cuerpo de POST /loads: como en los JSON, con el límite de la tabla."""

    # String(100) en readings.label: sin este límite, una etiqueta más larga llegaría a
    # PostgreSQL, que la rechazaría con un error 500 en lugar de un 422.
    label: Annotated[str, Field(min_length=1, max_length=100)]


class LoadIn(BaseModel):
    """El cuerpo de POST /loads: de dónde vienen las medidas y la lista de medidas."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    source: Annotated[str, Field(min_length=1, max_length=500)]
    measurements: Annotated[list[ReadingIn], Field(min_length=1)]


class Health(BaseModel):
    """La respuesta de GET /health."""

    status: str
    version: str


def get_session(request: Request) -> Iterator[Session]:
    """Una sesión por petición, con el motor de la aplicación; se cierra al responder."""
    with Session(request.app.state.engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter()


@router.get("/health")
def health(session: SessionDep) -> Health:
    """Responde si la API está viva y PostgreSQL contesta."""
    raise NotImplementedError


@router.get("/loads")
def get_loads(session: SessionDep) -> list[LoadInfo]:
    """Todas las cargas, de la más antigua a la más nueva, con cuántas medidas tiene cada una."""
    raise NotImplementedError


@router.post("/loads", status_code=status.HTTP_201_CREATED)
def post_load(body: LoadIn, session: SessionDep, response: Response) -> LoadInfo:
    """Guarda una carga nueva con sus medidas y la devuelve con su número."""
    raise NotImplementedError


@router.get("/loads/{load_id}/measurements")
def get_measurements(load_id: int, session: SessionDep) -> list[Measurement]:
    """Las medidas de una carga, en su orden; 404 si no existe."""
    raise NotImplementedError


@router.delete("/loads/{load_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_load(load_id: int, session: SessionDep) -> None:
    """Borra una carga y sus medidas; 404 si no existe."""
    raise NotImplementedError


@router.get("/stats")
def get_stats(session: SessionDep, load: int | None = None) -> list[LabelStats]:
    """Medidas, medidas con valor y media por etiqueta, de una carga (?load=N) o de todas."""
    raise NotImplementedError


def create_app(url: str) -> FastAPI:
    """La aplicación de la API, con su motor para `url`, abierto al arrancar y cerrado al parar."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.engine = make_engine(url)
        yield
        app.state.engine.dispose()

    app = FastAPI(title="Observatorio", version=__version__, lifespan=lifespan)
    app.include_router(router)
    return app
```

Repásalo con la teoría antes de seguir. Los modelos, `get_session`, las firmas de las rutas y `create_app` ya están completos: describen el contrato, y casi todo lo que hace FastAPI sale de ahí (teoría 02 y 03):

- `ReadingIn` **hereda** de `MeasurementIn`, de la semana 13: las mismas reglas que un archivo JSON, más el límite de la columna;
- las rutas devuelven las *dataclasses* de `core` (`LoadInfo`, `LabelStats`, `Measurement`), sin modelos de salida nuevos;
- `create_app` recibe la URL: `api.py` no lee el entorno.

```bash
uv run pytest
```

```
49 failed, 610 passed
```

Ya pasan los tests que FastAPI resuelve sin tus rutas: el 422 de cada cuerpo no válido, el 404 de una ruta que no existe, el 405, `/openapi.json` y `/docs`. Los 49 que fallan llaman a una ruta, o al comando `servir`.

### 5. `GET /health`

```python
    session.execute(text("SELECT 1"))
    return Health(status="ok", version=__version__)
```

Con `from sqlalchemy import text`. `SELECT 1` no lee ninguna tabla: comprueba que PostgreSQL contesta. Un `/health` que siempre dijera `ok` diría que todo va bien con la base caída, y el *healthcheck* de Docker no serviría de nada.

```
46 failed, 613 passed
```

### 6. `GET /loads` y `POST /loads`

```python
    return list_loads(session)
```

```python
    series = Series([reading.to_measurement() for reading in body.measurements])
    load = save_series(session, body.source, series)
    session.commit()
    response.headers["Location"] = f"/loads/{load.id}"
    return LoadInfo(load.id, load.source, load.created_at, len(series))
```

Importa `Series`, `list_loads` y `save_series` de `observatorio.core`. En `post_load`:

- `to_measurement()` es de `MeasurementIn` (semana 13): convierte cada medida validada en una `Measurement` de `core`;
- el **`commit`** va en la ruta, antes de responder: el 201 solo sale si la carga está confirmada (teoría 03, sección 4);
- la respuesta se construye con lo que ya sabes, sin otra consulta para contar las medidas.

```
25 failed, 634 passed
```

### 7. `GET /loads/{id}/measurements` y `DELETE /loads/{id}`

```python
    series = load_series(session, load_id)
    if series is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"no existe la carga {load_id}")
    return series.measurements
```

```python
    if not delete_load(session, load_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"no existe la carga {load_id}")
    session.commit()
```

Con `HTTPException` de `fastapi`, y `delete_load` y `load_series` de `core`. `remove_load` no devuelve nada: un 204 no lleva cuerpo. Fíjate en el `is None` de `get_measurements`: lo vas a poner a prueba en el paso 14.

```
17 failed, 642 passed
```

### 8. `GET /stats`

```python
    if load is not None and session.get(Load, load) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"no existe la carga {load}")
    return label_stats(session, load)
```

Con `Load` y `label_stats` de `core`. Sin la comprobación, `?load=999` respondería `[]`, igual que una carga que existe sin medidas: quien llama no sabría si se equivocó de número. Es lo mismo que hace `consultar -c` en la CLI.

```
13 failed, 646 passed
```

### 9. Sin PostgreSQL: 503

```python
def database_unavailable(request: Request, problem: Exception) -> JSONResponse:
    """503 sin el texto del error, que podría llevar el usuario o el servidor."""
    return JSONResponse(
        {"detail": "no se pudo conectar con PostgreSQL"},
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    )
```

Antes de `create_app`, con `JSONResponse` de `fastapi.responses` y `OperationalError` de `sqlalchemy.exc`. Y en `create_app`, después de `include_router`:

```python
    app.add_exception_handler(OperationalError, database_unavailable)
```

Un `OperationalError` en cualquier ruta es ahora un 503, con un mensaje que **no** copia el del error (teoría 03, sección 6). `problem` no se usa, pero la firma la pide FastAPI.

```
9 failed, 650 passed
```

### 10. El comando `servir`, y un refactor por el camino

`servir` necesita la URL de la base, como `database()`, pero no una sesión: la aplicación abre las suyas. Saca de `database()` la parte que lee y valida la URL a una función nueva en `cli.py`, encima de `database()`:

```python
def database_url() -> str:
    """La URL de OBSERVATORIO_DATABASE_URL; si falta o no es válida, sale con código 2."""
    settings = read_settings()
    if settings.database_url is None:
        raise fail("falta OBSERVATORIO_DATABASE_URL (en el entorno o en .env)", 2)
    url = settings.database_url.get_secret_value()
    try:
        # get_dialect: también falla si el tipo de base no existe (nada://...).
        make_url(url).get_dialect()
    except ArgumentError:
        raise fail("OBSERVATORIO_DATABASE_URL no es una URL de base de datos válida", 2) from None
    return url
```

Y `database()` empieza ahora así:

```python
    url = database_url()
    engine = make_engine(url)
    try:
        with Session(engine) as session:
```

`make_engine` ya no necesita su `try`: la URL llega validada. Ejecuta `uv run pytest tests/test_database.py -q`: los tests de la CLI de la semana 19 siguen en verde, con los mismos mensajes. Eso es un refactor.

Ahora el comando, al final de `cli.py`:

```python
@app.command()
def servir(
    host: Annotated[
        str, typer.Option("--host", help="La dirección en la que escucha; 0.0.0.0 en Docker.")
    ] = "127.0.0.1",
    puerto: Annotated[
        int, typer.Option("--puerto", "-p", min=1, max=65535, help="El puerto en el que escucha.")
    ] = 8000,
) -> None:
    """Sirve la API HTTP con uvicorn hasta Ctrl+C. La documentación, en /docs.

    Lee OBSERVATORIO_DATABASE_URL del entorno o de .env.
    """
    url = database_url()
    # Importar aquí: FastAPI y uvicorn solo se cargan al servir, no en cada comando.
    import uvicorn

    from observatorio.api import create_app

    uvicorn.run(create_app(url), host=host, port=puerto)
```

Los dos `import` van **dentro** de la función a propósito: la CLI arranca un 22 % más rápido en todos los demás comandos (teoría 05, sección 7). `test_the_cli_loads_fastapi_only_to_serve` lo vigila.

```
1 failed, 658 passed
```

### 11. La versión

```bash
uv version --bump minor
uv run observatorio --version
uv run pytest
```

```
observatorio 0.20.0
...
659 passed
```

### 12. Usar de verdad, y medir

Aplica las migraciones a tu base de desarrollo, si no lo están, y sirve:

```bash
uv run alembic upgrade head
uv run observatorio servir
```

En **otra terminal**:

```bash
curl -i http://127.0.0.1:8000/health
curl -s -X POST http://127.0.0.1:8000/loads -H 'content-type: application/json' \
     -d '{"source": "curl", "measurements": [{"label": "Norte", "value": "12,5"}, {"label": "Sur", "value": null}]}'
uv run observatorio cargas
curl -s 'http://127.0.0.1:8000/stats?load=1'
curl -s -X POST http://127.0.0.1:8000/loads -H 'content-type: application/json' -d '{"source": ""}'
curl -s -o /dev/null -w '%{http_code}\n' -X DELETE http://127.0.0.1:8000/loads/999
```

```
HTTP/1.1 200 OK
...
{"status":"ok","version":"0.20.0"}
{"id":1,"source":"curl","created_at":"...","measurements":2}
...
{"detail":[{"type":"string_too_short","loc":["body","source"],...},{"type":"missing","loc":["body","measurements"],...}]}
404
```

La carga que guardaste por HTTP sale en `observatorio cargas`: la API y la CLI comparten la base. Usa el número de **tu** carga: si tu base tenía cargas de la semana 19, no será la 1. En la primera terminal, uvicorn escribe una línea por petición, con su código.

Abre <http://127.0.0.1:8000/docs>: están tus seis rutas, con los *docstrings* como descripción. Prueba `POST /loads` con **Try it out** y una medida de tu dominio.

Ahora mide, con la API sirviendo. Este programa hace 500 peticiones a cada ruta de lectura y una carga de 10 000 medidas:

```bash
uv run python - <<'EOF'
import time

import httpx

with httpx.Client(base_url="http://127.0.0.1:8000") as client:
    for path in ["/health", "/loads", "/stats"]:
        start = time.perf_counter()
        for _ in range(500):
            client.get(path).raise_for_status()
        elapsed = time.perf_counter() - start
        print(f"GET {path:<8} {500 / elapsed:.0f} peticiones por segundo")
    body = {
        "source": "grande",
        "measurements": [{"label": f"L{i % 7}", "value": i / 10} for i in range(10_000)],
    }
    start = time.perf_counter()
    client.post("/loads", json=body).raise_for_status()
    print(f"POST /loads con 10 000 medidas: {time.perf_counter() - start:.2f} s")
EOF
```

Rellena la tabla con tus números:

| Petición | Tu resultado |
|---|---|
| `GET /health` | |
| `GET /loads` | |
| `GET /stats` | |
| `POST /loads` con 10 000 medidas | |

En mi máquina, con la API en Docker: 495, 352 y 375 peticiones por segundo, y 1,02 s para guardar las 10 000 medidas. `/health` es la más rápida porque solo hace `SELECT 1`; `/loads` y `/stats` agrupan en PostgreSQL. El `POST` gasta la mayor parte del tiempo validando 10 000 medidas con Pydantic y enviando sus `INSERT`. Compáralo con `guardar` de la semana 19: casi lo mismo, sin el arranque de la CLI.

Para el servidor con **Ctrl+C**: uvicorn ejecuta el final del lifespan (`Waiting for application shutdown`) y cierra el motor.

### 13. Calidad y cobertura

```bash
uv run ruff check && uv run ruff format --check
uv run mypy
uv run coverage run -m pytest -q && uv run coverage report
uv run alembic check
```

`api.py` y `cli.py` deben salir al 100 %.

### 14. Una prueba de mutación

Haz cada cambio, **uno cada vez**, ejecuta `uv run pytest -x -q` y deshazlo con `git checkout <archivo>`:

| Archivo | Mutante | ¿Lo detectan? |
|---|---|---|
| `api.py` | quita el `session.commit()` de `post_load` | |
| `api.py` | `max_length=100` por `max_length=200` en `ReadingIn` | |
| `api.py` | `extra="forbid"` por `extra="ignore"` en `LoadIn` | |
| `api.py` | quita `session.execute(text("SELECT 1"))` de `health` | |
| `api.py` | quita `app.add_exception_handler(...)` | |
| `api.py` | quita `app.state.engine.dispose()` del lifespan | |
| `api.py` | `if series is None:` por `if not series:` en `get_measurements` | |
| `cli.py` | `port=puerto` por `port=8000` en `servir` | |

Siete mueren. Uno **sobrevive**: ¿cuál, y por qué ningún test del bootcamp lo ve? Pista: ¿puede existir una carga sin medidas? La API no deja crearla, pero la API no es la única que guarda cargas. Lo vas a matar en el paso siguiente.

### 15. Tus tests

En `tests/test_my_api.py`, sustituye el ejemplo por **al menos 6 tests** con medidas de **tu dominio**, con la fixture `client` que trae el archivo:

- `POST /loads` y `GET /loads/{id}/measurements` de ida y vuelta, con un valor que falta;
- un cuerpo no válido de tu dominio, con su 422 y su `loc`;
- `/stats?load=N` con dos cargas;
- `DELETE`, y que después la carga da 404;
- una respuesta sin PostgreSQL: 503, sin la contraseña;
- el mutante que sobrevivió en el paso 14.

Para el último, guarda una carga **vacía** como lo haría `guardar` con un archivo sin medidas válidas: `save_series(session, "vacio.txt", Series())`, con la misma `session` que usa `client`. Después, pide sus medidas por la API: tiene que responder 200 y `[]`, no 404.

Al final, al menos 761 tests en verde.

### 16. Contenedor, README y pull request

```bash
docker compose build app
docker compose run --rm app
docker compose run --rm app alembic upgrade head
docker compose up -d --wait api
curl -s http://127.0.0.1:8000/health
docker compose logs api
docker compose stop api
```

`app` ejecuta los tests contra `observatorio_test`; `api` sirve contra `observatorio`, la misma base que usas desde tu máquina. Los dos usan la imagen `local/observatorio:week-20`: por eso `build app` antes. Si `observatorio servir` sigue sirviendo en tu máquina, páralo antes: los dos quieren el puerto 8000.

En el `README.md` de tu repositorio, añade una sección "API": cómo servirla (`uv run observatorio servir` y `docker compose up -d --wait api`), la tabla de rutas y un ejemplo con `curl`. Y un aviso: la API no comprueba quién llama, y por eso solo escucha en `127.0.0.1`.

Commits sugeridos, en este orden:

1. `test: add api tests`
2. `build: add fastapi, uvicorn and httpx2, and an api service`
3. `feat: add the api skeleton`
4. `feat: add the health route`
5. `feat: list and create loads`
6. `feat: get and delete the measurements of a load`
7. `feat: add label stats route`
8. `feat: answer 503 when postgres is down`
9. `refactor: extract database_url`
10. `feat: add servir command`
11. `chore: bump version to 0.20.0`
12. `test: add my api tests`

Antes de cada `git add`, un `git status --short`: nada de `.env`. Al final:

```bash
git push -u origin week-20
```

En GitHub, abre un *pull request* de `week-20` hacia `main` con:

1. La salida de `uv run pytest`, `uv run mypy`, `uv run ruff check`, `uv run coverage report` y `uv run alembic check`.
2. La tabla de medidas del paso 12.
3. La tabla de mutantes del paso 14, y el test con el que mataste al superviviente.
4. Por qué las rutas son `def` y no `async def`, y por qué el `commit` va en la ruta y no en `get_session`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `fixture 'session' not found` | Tu `conftest.py` no importa `db_fixtures` (semana 19, paso 4) |
| `no hay PostgreSQL en 127.0.0.1:5432` | `docker compose up -d --wait db` |
| `StarletteDeprecationWarning: Using httpx with starlette.testclient is deprecated` | Falta `uv add --dev httpx2==2.16.0` |
| `AttributeError: 'State' object has no attribute 'engine'` en tus tests | Usas `TestClient(app)` sin `with`, y sin override de `get_session` |
| `test_own_engine_post_load_commits` falla | Falta `session.commit()` en `post_load` |
| `test_post_load_rejects_invalid_bodies_with_422[long label]` da 500 | Falta `max_length=100` en `ReadingIn` |
| `test_the_503_does_not_show_the_password` falla | `database_unavailable` copia el texto del error |
| `test_the_cli_loads_fastapi_only_to_serve` falla | Importas `api` o `uvicorn` arriba de `cli.py`: van dentro de `servir` |
| `test_core_does_not_import_fastapi` falla | Algo de `core` importa `observatorio.api` o `fastapi` |
| `[Errno 98] address already in use` | Ya sirves en el puerto 8000 (¿otra terminal, el servicio `api`?): `-p 8001`, o para el otro |
| `curl: (7) Failed to connect to 127.0.0.1 port 8000` | La API no está sirviendo: `uv run observatorio servir` en otra terminal |
| Las rutas dan 500 con `relation "loads" does not exist` en el registro | Faltan las migraciones: `uv run alembic upgrade head` |
| `docker compose up -d --wait api` acaba en `unhealthy` | `docker compose logs api`: casi siempre, la imagen no está construida (`docker compose build app`) o faltan las migraciones |

## Entrega

- Rama `week-20` de `python-<nombre>-<apellido>` con:
  - `api.py` con `ReadingIn`, `LoadIn`, `Health`, `get_session`, las seis rutas, `database_unavailable` y `create_app`;
  - `cli.py` con `database_url` y el comando `servir`;
  - `compose.yaml` con el servicio `api`, las dependencias `fastapi==0.162.0`, `uvicorn==0.54.0` y `httpx2==2.16.0` (en `dev`), la versión `0.20.0` y al menos 6 tests propios en `tests/test_my_api.py`.

  Todo en verde, también en Docker, con `ruff check`, `ruff format --check`, `mypy`, `coverage report` y `alembic check` sin avisos.
- `README.md` del repositorio con el comando `servir` y la sección "API".
- *Pull request* `week-20` → `main` con la descripción del paso 16.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · Una API con PostgreSQL](../2-practicas/ejercicio-04-una-api-con-postgresql/README.md) | **Proyecto · Observatorio, capa 19** | [Webgrafía](../4-recursos/webgrafia/README.md) |
