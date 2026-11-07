# Proyecto — Observatorio, capa 17: descargar medidas por HTTP

⏱️ 6 h 30 min · Capa 17 del [proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md). **Único entregable de la semana.**

## Qué construyes

Hasta ahora, tus medidas estaban en archivos de tu máquina. Esta semana tu Observatorio las va a **buscar**: el comando `descargar` pide varios JSON de medidas por HTTP a la vez, los valida y guarda cada uno como un `.txt` que `lote`, `vigilar` e `informe` ya saben leer.

```
$ uv run observatorio descargar http://127.0.0.1:8000/norte.json http://127.0.0.1:8000/sur.json http://127.0.0.1:8000/este.json
error: http://127.0.0.1:8000/este.json respondió 404
Archivos
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Archivo             ┃ Medidas ┃ Con valor ┃       Media ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ descargas/norte.txt │       7 │         6 │ 32.5 unidad │
│ descargas/sur.txt   │       7 │         6 │ 32.5 unidad │
└─────────────────────┴─────────┴───────────┴─────────────┘
archivos: 3 · con error: 1
```

| Opción o variable | Qué hace |
|---|---|
| `URLS...` | Una o más URLs `http://` o `https://` de JSON de medidas, como `medidas.json` |
| `--carpeta DIR`, `-c DIR` | Dónde se guardan los `.txt`; por defecto, `descargas`. Se crea si no existe |
| `--limite N`, `-l N` | Cuántas URLs se descargan a la vez; por defecto, `WORKERS = 4` |
| `OBSERVATORIO_TOKEN` | Si existe, cada petición lleva `Authorization: Bearer <token>` |
| `OBSERVATORIO_TIMEOUT` | Segundos de plazo de httpx; por defecto, 10 |
| `OBSERVATORIO_RETRIES` | Reintentos de los fallos pasajeros, entre 0 y 10; por defecto, 3 |

Las variables se pueden poner en el entorno o en un archivo `.env`, que **nunca** va a Git. Los fallos de red, los `429` y los `5xx` se reintentan con espera exponencial; un `404` no. Lo que llega se valida con el mismo `MeasurementIn` de la semana 13: si no vale, no se guarda nada.

```
src/observatorio/
├── cli.py          # + BACKOFF y el comando descargar
├── settings.py     # nuevo: Settings, la configuración de .env y el entorno
└── core/
    ├── __init__.py # + la API de remote y parse_measurements
    ├── remote.py   # nuevo: make_client, get_text, target_of, download, download_all
    └── schemas.py  # + parse_measurements
tests/
├── test_remote.py     # nuevo: los tests del bootcamp
├── test_my_remote.py  # nuevo: los tuyos
└── test_package.py    # modificado: el módulo remote, las dependencias y la versión 0.18.0
.env.example           # nuevo: la plantilla de la configuración, sin secretos
```

`settings.py` va **fuera** de `core`, junto a `cli.py`: la configuración la leen los programas (la CLI, y la API de la semana 20), no el núcleo. `core/remote.py` recibe el token como un argumento más y no sabe de dónde salió.

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-18`. El `starter/` trae la capa 16 resuelta. **Tú** escribes `core/remote.py`, `settings.py` y el comando `descargar`.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-17` está fusionado en `main`. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-18
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-18-http_con_httpx_reintentos_secretos_y_env/3-proyecto/starter
cp $STARTER/tests/test_remote.py $STARTER/tests/test_my_remote.py $STARTER/tests/test_package.py tests/
cp $STARTER/.env.example .
sed -i 's/week-17/week-18/' compose.yaml
git status --short
```

Copias estos archivos:

- **Nuevos:**
  - `tests/test_remote.py`, con 78 tests de `remote.py`, de `Settings`, de `parse_measurements` y del comando `descargar`;
  - `tests/test_my_remote.py`, con un ejemplo;
  - `.env.example`, la plantilla de la configuración (teoría 04).
- **Modificado:** `test_package.py`, que espera el módulo `remote`, su API en `core`, `settings.py` fuera de `core`, las dos dependencias nuevas y la versión `0.18.0`.

### 3. Dependencias y tests en rojo

```bash
uv run pytest
```

```
E   ModuleNotFoundError: No module named 'httpx'
...
!!!!!!!!!!!!!!!!!!! Interrupted: 3 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Los tests importan httpx y pydantic-settings, que tu proyecto todavía no tiene. Añádelos con la versión fijada (están en `docs/stack-versions.md`, con su fecha y su revisión de avisos de seguridad):

```bash
uv add httpx==0.28.1 pydantic-settings==2.16.1
uv run pytest
```

```
E   ImportError: cannot import name 'FetchError' from 'observatorio.core' (...)
...
!!!!!!!!!!!!!!!!!!! Interrupted: 3 errors during collection !!!!!!!!!!!!!!!!!!!!
```

`uv add` trae también sus dependencias: anyio, httpcore, h11, certifi, idna y python-dotenv. Míralas en `uv.lock`.

Lee `tests/test_remote.py` antes de escribir nada. Fíjate en cuatro cosas (teoría 05):

- **ningún test sale a Internet**. Casi todos contestan con `httpx.MockTransport`, a través de `run_with(handler, ...)`; `replies(...)` fabrica un *handler* que contesta en orden y apunta las peticiones;
- la *fixture* `waits` cambia `asyncio.sleep` por un espía: los tests de reintentos comprueban **cuánto** se esperó sin esperar nada;
- dos tests levantan un servidor de verdad (`http.server`) en `127.0.0.1`, en un hilo, con un puerto libre;
- `clean_env` deja cada test sin tu `.env` ni tus variables `OBSERVATORIO_*`, y `served` cambia el `make_client` de la CLI por uno que contesta sin red.

### 4. El esqueleto: `remote.py`, `settings.py` y la API

Crea `src/observatorio/core/remote.py` con un *docstring* de módulo (qué, para qué, impacto) y:

```python
logger = logging.getLogger(__name__)

# Respuestas que pueden salir bien si se repite la petición: demasiadas peticiones (429)
# y fallos del servidor o de lo que hay delante de él (5xx). Un 404 no cambiará.
RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})


class FetchError(Exception):
    """Una descarga que no salió bien: el servidor no contestó o contestó con un error."""


def make_client(
    *,
    token: str | None = None,
    timeout: float = 10.0,
    transport: httpx.AsyncBaseTransport | None = None,
) -> httpx.AsyncClient:
    """Un cliente que se presenta como observatorio/<versión> y espera `timeout` segundos."""
    raise NotImplementedError


async def get_text(
    client: httpx.AsyncClient, url: str, *, retries: int = 3, backoff: float = 0.5
) -> str:
    """El texto de `url`. Reintenta hasta `retries` veces los fallos de red y RETRY_STATUSES."""
    raise NotImplementedError


def target_of(url: str, folder: Path) -> Path:
    """Dónde se guarda lo que se baja de `url`: <folder>/<nombre del archivo de la URL>.txt."""
    raise NotImplementedError


async def download(
    client: httpx.AsyncClient,
    url: str,
    folder: Path,
    *,
    retries: int = 3,
    backoff: float = 0.5,
) -> FileReport:
    """Baja un JSON de medidas, lo valida y lo guarda en `folder` con una línea por medida."""
    raise NotImplementedError


async def download_all(
    client: httpx.AsyncClient,
    urls: Iterable[str],
    folder: Path,
    *,
    limit: int = 4,
    retries: int = 3,
    backoff: float = 0.5,
) -> list[FileReport]:
    """Baja las URLs a la vez, como mucho `limit` cada vez, en el orden de `urls`."""
    raise NotImplementedError
```

Fíjate en las firmas: todo recibe el **cliente** como argumento. Nadie crea su propio cliente dentro: la CLI abre uno y lo comparte, y los tests pasan uno con `MockTransport`.

En `schemas.py`, el esqueleto del refactor del paso 5:

```python
def parse_measurements(text: str, source: Path | str) -> Series:
    """La serie de un texto JSON con una lista de medidas, validadas con MeasurementIn."""
    raise NotImplementedError
```

Y crea `src/observatorio/settings.py`, **fuera** de `core`, con su *docstring* y la clase, de momento sin configurar:

```python
class Settings(BaseSettings):
    """OBSERVATORIO_TOKEN, OBSERVATORIO_TIMEOUT y OBSERVATORIO_RETRIES, validadas."""

    token: SecretStr | None = None
    timeout: Annotated[float, Field(gt=0)] = 10.0
    retries: Annotated[int, Field(ge=0, le=10)] = 3
```

En `core/__init__.py`, importa `FetchError`, `download`, `download_all`, `get_text`, `make_client` y `target_of` de `observatorio.core.remote`, y `parse_measurements` de `observatorio.core.schemas`, y añádelos a `__all__`. `uv run ruff check --fix` los ordena.

```
61 failed, 464 passed, 14 errors
```

Los 14 errores son los tests del comando `descargar`: su *fixture* `served` no encuentra `cli.make_client`. Desaparecen en el paso 12.

### 5. Un refactor: `parse_measurements`

`read_measurements` (semana 13) lee un archivo y valida su texto. Ahora el texto también puede llegar de la red, así que separa las dos cosas. `_invalid` recibe ahora `source: Path | str`, y la validación se mueve a `parse_measurements`:

```python
def parse_measurements(text: str, source: Path | str) -> Series:
    """La serie de un texto JSON con una lista de medidas, validadas con MeasurementIn.

    `source` (un archivo, una URL) solo sirve para el mensaje: si el texto no es JSON o
    alguna medida no es válida, DataFileError("datos no válidos en <source>: ...").
    """
    try:
        items = _MEASUREMENTS.validate_json(text)
    except ValidationError as error:
        raise _invalid(source, error) from error
    return Series([item.to_measurement() for item in items])


def read_measurements(path: Path) -> Series:
    """La serie de un archivo JSON de medidas: read_lines y después parse_measurements."""
    return parse_measurements("\n".join(read_lines(path)), path)
```

Los 29 tests de `test_schemas.py` siguen en verde: los mensajes de error son los mismos.

```
58 failed, 467 passed, 14 errors
```

### 6. `make_client`

Un diccionario de cabeceras con `"User-Agent": f"observatorio/{version('observatorio')}"` (con `version` de `importlib.metadata`, como en la semana 8). Si hay `token`, añade `"Authorization": f"Bearer {token}"`. Devuelve:

```python
    return httpx.AsyncClient(
        headers=headers, timeout=timeout, follow_redirects=True, transport=transport
    )
```

Con `transport=None`, httpx usa su transporte de verdad, el de la red. Es la costura por donde entran los tests (teoría 05, sección 2).

```
54 failed, 471 passed, 14 errors
```

### 7. `get_text`, de momento sin reintentos

Una sola petición, con las dos clases de error de la teoría 02:

```python
    try:
        response = await client.get(url)
    except httpx.TransportError as problem:
        raise FetchError(f"sin respuesta de {url} ({type(problem).__name__})") from problem
    if response.is_error:
        raise FetchError(f"{url} respondió {response.status_code}")
    return response.text
```

El mensaje usa el **nombre de la clase** (`ConnectError`, `ReadTimeout`), no el texto del error, que cambia con el sistema operativo (ejercicio 01, paso 5).

```
46 failed, 479 passed, 14 errors
```

### 8. Los reintentos

Ahora el bucle completo, el del ejercicio 03, paso 4:

```python
    failure = ""
    for attempt in range(retries + 1):
        if attempt > 0:
            await asyncio.sleep(backoff * 2 ** (attempt - 1))
        try:
            response = await client.get(url)
        except httpx.TransportError as problem:
            # Sin respuesta: no conecta, se agota el plazo, se corta. El mensaje viene del
            # sistema operativo y cambia de una máquina a otra; el nombre de la clase, no.
            failure = f"sin respuesta de {url} ({type(problem).__name__})"
        else:
            if response.status_code not in RETRY_STATUSES:
                if response.is_error:
                    raise FetchError(f"{url} respondió {response.status_code}")
                return response.text
            failure = f"{url} respondió {response.status_code}"
        logger.debug("intento %d de %d: %s", attempt + 1, retries + 1, failure)
    raise FetchError(f"{failure} tras {retries + 1} intentos")
```

Repasa cada decisión con la teoría 03:

- `range(retries + 1)`: con `retries=3`, cuatro intentos;
- la espera va **antes** de cada reintento, nunca antes del primero, y se dobla: 0,5, 1 y 2 s;
- `try`/`except`/`else`: el `else` se ejecuta solo si no hubo excepción, es decir, si **hubo respuesta**;
- un error que no está en `RETRY_STATUSES` sale **al momento**, sin esperas;
- `failure` guarda el último fallo, para el mensaje final y para el registro.

```
32 failed, 493 passed, 14 errors
```

### 9. `target_of` y `download`

`target_of` toma el último trozo de la ruta de la URL, sin extensión, y le pone `.txt`:

```python
    name = PurePosixPath(httpx.URL(url).path).stem or "datos"
    return folder / f"{name}.txt"
```

`httpx.URL(url).path` ya no tiene la consulta (`?dia=1`); `PurePosixPath`, porque las rutas de las URLs usan `/` también en Windows. Y como solo usas el **último** trozo, una URL como `http://x/../../etc/passwd` acaba en `<folder>/passwd.txt`, dentro de tu carpeta (teoría 05, sección 6).

`download`, en tres partes:

1. `target = target_of(url, folder)`; después, `get_text` y `parse_measurements(text, url)`. Si cualquiera de los dos falla (`FetchError` o `DataFileError`), devuelve `FileReport(target, error=str(problem))` **sin guardar nada**.
2. Escribe una línea por medida, con `str(measurement)` (semana 11): `"".join(f"{measurement}\n" for measurement in series)`. Escribir en el disco bloquea, como leer: `await asyncio.to_thread(target.write_text, content, encoding="utf-8")`. Un `OSError` al escribir, `FileReport(target, error=f"no se pudo guardar {target}: {problem.strerror}")`.
3. Devuelve `FileReport.from_series(target, series)` (semana 17).

Lo que guardas es un `.txt` como cualquier otro, y `report_file` lo resume igual: `test_download_saves_a_file_that_report_file_reads` lo comprueba.

```
19 failed, 506 passed, 14 errors
```

### 10. `download_all`

Es `watch_files` otra vez, con otras piezas:

```python
    semaphore = asyncio.Semaphore(limit)

    async def guarded(url: str) -> FileReport:
        async with semaphore:
            return await download(client, url, folder, retries=retries, backoff=backoff)

    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(guarded(url)) for url in urls]
    return [task.result() for task in tasks]
```

¿Merece la pena sacar el patrón a una función común? Todavía no: son dos usos, de seis líneas, y una abstracción con un parámetro para cada diferencia sería más difícil de leer. Si aparece un tercero, se piensa.

```
12 failed, 513 passed, 14 errors
```

### 11. `Settings` y `.env`

Configura la clase como en la teoría 04:

```python
    # env_prefix: `timeout` se lee de OBSERVATORIO_TIMEOUT, no de TIMEOUT, que podría
    # ser de otro programa. env_ignore_empty: `OBSERVATORIO_TOKEN=`, como en .env.example,
    # es "sin token", no un token vacío. extra="ignore": .env puede tener otras variables.
    model_config = SettingsConfigDict(
        env_prefix="OBSERVATORIO_",
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
        frozen=True,
    )
```

```
2 failed, 523 passed, 14 errors
```

Y antes de crear ningún `.env`, protégelo. Añade `.env` a tu `.gitignore` y a tu `.dockerignore`, y compruébalo:

```bash
echo ".env" >> .gitignore
echo ".env" >> .dockerignore
cp .env.example .env
git check-ignore -v .env
git status --short
```

```
.gitignore:<línea>:.env	.env
```

`git status` no debe enseñar `.env`; `.env.example`, sí: ese va a Git, sin secretos. Si quieres, añade también `descargas/` al `.gitignore`: los datos descargados se vuelven a bajar cuando haga falta.

### 12. El comando `descargar`

En `cli.py`, una constante más:

```python
# Segundos antes del primer reintento de `descargar`; cada reintento espera el doble.
BACKOFF = 0.5
```

y el comando, con:

- `urls: list[str]`, con `typer.Argument(metavar="URLS", help="Las URLs de los JSON de medidas.")`;
- `carpeta: Path`, con `typer.Option("--carpeta", "-c", help=...)` y valor por defecto `Path("descargas")`;
- `limite: int`, con `typer.Option("--limite", "-l", min=1, help=...)` y valor por defecto `WORKERS`.

El cuerpo, en cuatro partes:

1. Comprueba que cada URL empieza por `http://` o `https://`; si no, `raise typer.BadParameter(f"{url!r} no empieza por http:// ni https://", param_hint="URLS")`. Sin esto, httpx lanzaría `UnsupportedProtocol`, que es un `TransportError`, y lo reintentarías cuatro veces para nada.
2. Lee la configuración. Un `ValidationError` es un error de configuración, con código 2:

   ```python
       try:
           settings = Settings()
       except ValidationError as problem:
           first = problem.errors()[0]
           name = f"OBSERVATORIO_{str(first['loc'][0]).upper()}"
           raise fail(f"configuración no válida: {name}: {first['msg']}", 2) from None
   ```

3. Saca el token del `SecretStr` **aquí**, y solo aquí: `token = None if settings.token is None else settings.token.get_secret_value()`. Crea la carpeta con `carpeta.mkdir(parents=True, exist_ok=True)`; si no se puede (ya hay un archivo con ese nombre, o no tienes permiso), `raise fail(f"no se pudo crear {carpeta}: {problem.strerror}", 2) from problem`.
4. Una corrutina anidada abre el cliente, que se cierra al salir del `async with`, y `asyncio.run` la arranca:

   ```python
       async def fetch() -> list[FileReport]:
           # `async with` cierra las conexiones del cliente al terminar, haya error o no.
           async with make_client(token=token, timeout=settings.timeout) as client:
               return await download_all(
                   client, urls, carpeta, limit=limite, retries=settings.retries, backoff=BACKOFF
               )

       show_reports(asyncio.run(fetch()))
   ```

`show_reports` es el de la semana 17: errores, tabla y total, y código 1 si falló alguna URL. Añade el comando al *docstring* del módulo, y un *docstring* al comando que diga de qué variables lee la configuración: sale en `--help`.

```bash
uv run observatorio descargar --help
uv run observatorio descargar 127.0.0.1:8000/norte.json; echo $?
uv run pytest
```

```
...
│ Invalid value for URLS: '127.0.0.1:8000/norte.json' no empieza por http://   │
│ ni https://                                                                  │
...
2
...
1 failed, 538 passed
```

### 13. La versión

```bash
uv version --bump minor
uv run observatorio --version
uv run pytest
```

```
observatorio 0.18.0
...
539 passed
```

### 14. Descargar de verdad, y medir

Necesitas un servidor. La biblioteca estándar trae uno que sirve los archivos de una carpeta (teoría 05). En **otra terminal**, en la raíz de tu proyecto:

```bash
mkdir -p /tmp/web
cp medidas.json /tmp/web/norte.json
cp medidas.json /tmp/web/sur.json
uv run python -m http.server 8000 --bind 127.0.0.1 --directory /tmp/web
```

Y en la tuya:

```bash
uv run observatorio descargar http://127.0.0.1:8000/norte.json http://127.0.0.1:8000/sur.json http://127.0.0.1:8000/este.json; echo $?
head -3 descargas/norte.txt
uv run observatorio lote descargas/*.txt
```

Debes ver la salida del principio de este README, con código 1 por el `404` de `este.json`, y en la otra terminal, una línea por petición. `descargas/norte.txt` empieza por `Norte;12,5`, `Sur;8,0` y `Centro;NA`, y `lote` lo resume sin saber que vino de la red.

Prueba el token: pon `OBSERVATORIO_TOKEN=abc123` en tu `.env` y ejecuta con `-v`. El registro enseña cada petición (`HTTP Request: GET ... "HTTP/1.1 200 OK"`), pero **no** el token. `http.server` no lo mira; una API de verdad, sí.

Ahora mide cuánto cuestan los reintentos. En el puerto 9 no escucha nadie, así que todos los intentos fallan:

```bash
time uv run observatorio --version
for n in 0 1 2 3; do
  echo "reintentos: $n"
  time OBSERVATORIO_RETRIES=$n uv run observatorio descargar http://127.0.0.1:9/a.json http://127.0.0.1:9/b.json > /dev/null 2>&1
done
time uv run observatorio descargar http://127.0.0.1:9/a.json > /dev/null 2>&1
```

Apunta el tiempo **real** de cada uno. En la máquina del bootcamp:

| Orden | Tiempo | Cuentas |
|---|---|---|
| `--version` (arrancar Python y la CLI) | 0,6 s | |
| 2 URLs, 0 reintentos | 0,7 s | 0,7 |
| 2 URLs, 1 reintento | 1,2 s | 0,7 + 0,5 |
| 2 URLs, 2 reintentos | 2,2 s | 0,7 + 0,5 + 1 |
| 2 URLs, 3 reintentos (por defecto) | 4,2 s | 0,7 + 0,5 + 1 + 2 |
| 1 URL, 3 reintentos | 4,2 s | lo mismo: las dos URLs esperan a la vez |

Fíjate en dos cosas. Cada reintento más **dobla** la espera: con 10 reintentos (el máximo que acepta `Settings`), un servidor caído te tendría más de 8 minutos esperando. Y dos URLs tardan lo mismo que una: mientras una descarga duerme su `asyncio.sleep`, la otra también, en el mismo hilo (semana 17).

Para el servidor de la otra terminal con Ctrl+C.

### 15. Calidad, cobertura y una prueba de mutación

```bash
uv run ruff check && uv run ruff format --check
uv run mypy
uv run coverage run -m pytest -q && uv run coverage report
```

`remote.py` y `settings.py` deben salir al 100 %.

Ahora la prueba de mutación. Haz cada cambio, **uno cada vez**, ejecuta `uv run pytest -x -q` y deshazlo con `git checkout <archivo>`:

| Archivo | Mutante | ¿Lo detectan? |
|---|---|---|
| `remote.py` | quita el `429` de `RETRY_STATUSES` | |
| `remote.py` | `range(retries + 1)` por `range(retries)` | |
| `remote.py` | `backoff * 2 ** (attempt - 1)` por `backoff` | |
| `remote.py` | `except httpx.TransportError` por `except httpx.TimeoutException` | |
| `remote.py` | `follow_redirects=True` por `follow_redirects=False` | |
| `remote.py` | `await asyncio.to_thread(target.write_text, ...)` por `target.write_text(...)` | |
| `settings.py` | `token: SecretStr \| None` por `token: str \| None` | |
| `cli.py` | `limit=limite` por `limit=WORKERS` en `descargar` | |

Siete mueren. Uno **sobrevive**: ¿cuál, y por qué ningún test del bootcamp lo ve? Lo vas a matar en el paso siguiente.

### 16. Tus tests

En `tests/test_my_remote.py`, sustituye el ejemplo por **al menos 6 tests** con medidas de **tu dominio** y `httpx.MockTransport`, sin red:

- `get_text` con un `200`: el texto;
- `get_text` con un error que no se reintenta (`404`, `401`...): `FetchError` y una sola petición;
- `get_text` con un `503` y después un `200`: dos peticiones, con el espía de `asyncio.sleep` para no esperar;
- `download`: el `FileReport` y el contenido del `.txt` guardado en `tmp_path`;
- `Settings` con `monkeypatch.setenv` y `monkeypatch.chdir(tmp_path)`;
- el mutante que sobrevivió en el paso 15.

Para el último, mira cómo prueba `test_remote.py` el límite de `download_all` (`test_download_all_respects_the_limit`): un *handler* asíncrono que cuenta cuántas peticiones hay a la vez. Hazlo con el **comando**: cambia `cli.make_client` con `monkeypatch.setattr`, como la *fixture* `served`, e invoca `descargar -l 1` con seis URLs.

Al final, al menos 631 tests en verde.

### 17. Contenedor, README y pull request

```bash
docker compose run --build --rm app
```

El contenedor **no** lleva tu `.env`: lo impide `.dockerignore`. Compruébalo:

```bash
docker compose run --rm app ls -a
```

En el `README.md` de tu repositorio, añade `descargar` a la lista de comandos, y una sección corta de configuración: copiar `.env.example` a `.env`, qué variable hace qué, y que `.env` no se sube nunca.

Commits sugeridos, en este orden:

1. `test: add remote tests`
2. `build: add httpx and pydantic-settings`
3. `feat: add the remote api skeleton and settings`
4. `refactor: extract parse_measurements`
5. `feat: add make_client`
6. `feat: get a url with retries and exponential backoff`
7. `feat: download and save validated measurements`
8. `feat: download urls with a task group and a semaphore`
9. `feat: read settings from the environment and .env`
10. `feat: add descargar command`
11. `chore: bump version to 0.18.0`
12. `test: add my remote tests`

Antes de cada `git add`, un `git status --short`: `.env` no puede aparecer nunca. Al final:

```bash
git push -u origin week-18
```

En GitHub, abre un *pull request* de `week-18` hacia `main` con:

1. La salida de `uv run pytest`, `uv run mypy`, `uv run ruff check` y `uv run coverage report`.
2. La tabla de tiempos del paso 14, con tus cuentas.
3. La tabla de mutantes del paso 15, y el test con el que mataste al superviviente.
4. Por qué `core/remote.py` no lee la configuración y `settings.py` está fuera de `core`, y qué fallos reintenta `get_text` y por qué esos.

Revisa lo que pegas: ni la salida de `-v` ni ningún comando deben llevar tu token.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'httpx'` | Te falta el `uv add` del paso 3 |
| `ImportError: cannot import name 'FetchError' from 'observatorio.core'` | Falta `core/remote.py`, o no lo importas en `core/__init__.py` |
| 14 tests salen como `ERROR` con `AttributeError: ... has no attribute 'make_client'` | La CLI todavía no importa `make_client`: llega en el paso 12 |
| `test_get_text_does_not_retry_a_client_error` da `assert 4 == 1` | Reintentas todos los errores: solo los de `RETRY_STATUSES` |
| `test_get_text_gives_up_after_the_retries` da `assert 3 == 4` | `range(retries)`: el primer intento no es un reintento, `range(retries + 1)` |
| `test_get_text_waits_twice_as_long_each_time` da `[0.5, 0.5, 0.5]` o `[1.0, 2.0, 4.0]` | La espera es `backoff * 2 ** (attempt - 1)`, solo con `attempt > 0` |
| `test_download_writes_in_another_thread` da `assert [] == ['write_text']` | Escribes directamente: `await asyncio.to_thread(target.write_text, content, encoding="utf-8")` |
| `test_settings_reads_the_environment` falla, pero con `TOKEN` funciona | Te falta `env_prefix="OBSERVATORIO_"` |
| Un test de `Settings` pasa en tu máquina y falla en Docker, o al revés | Tu `.env` o tus variables `OBSERVATORIO_*` se cuelan: los tests usan `clean_env`; tú, `env \| grep OBSERVATORIO` |
| `descargar` da `ConnectError` contra `127.0.0.1:8000` | El servidor de la otra terminal no está en marcha, o en otro puerto |
| `descargar` tarda 4 s en dar un error | Son los reintentos con el servidor caído: `OBSERVATORIO_RETRIES=0` para probar más rápido |
| `.env` aparece en `git status` | No está en `.gitignore`. Si ya hiciste commit con un token de verdad, revócalo primero (teoría 04) |

## Entrega

- Rama `week-18` de `python-<nombre>-<apellido>` con:
  - `core/remote.py` con `make_client`, `get_text`, `target_of`, `download` y `download_all`, exportados desde `core`, y `parse_measurements` en `schemas.py`;
  - `settings.py` fuera de `core`, con `Settings`, y `.env.example` en Git; `.env` en `.gitignore` y `.dockerignore`;
  - el comando `descargar` con `--carpeta` y `--limite`, y la constante `BACKOFF`;
  - la versión `0.18.0` y al menos 6 tests propios en `tests/test_my_remote.py`.

  Todo en verde, también en Docker, con `ruff check`, `ruff format --check`, `mypy` y `coverage report` sin avisos.
- `README.md` del repositorio con el comando `descargar` y la configuración.
- *Pull request* `week-18` → `main` con la descripción del paso 17.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · Secretos y configuración](../2-practicas/ejercicio-04-secretos-y-configuracion/README.md) | **Proyecto · Observatorio, capa 17** | [Webgrafía](../4-recursos/webgrafia/README.md) |
