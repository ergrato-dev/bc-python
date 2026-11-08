# Semana 20 — FastAPI: lo justo para servir tu proyecto

> Tus cargas viven en PostgreSQL, pero solo llega a ellas quien tiene el Observatorio instalado y la contraseña de la base. Esta semana las sirves por **HTTP**, con **FastAPI** y **uvicorn**: rutas que validan lo que llega con los modelos de Pydantic que ya tienes, una sesión de base de datos por petición, errores con el código que les toca y una documentación que se escribe sola. Lo pruebas todo con `TestClient` contra el PostgreSQL de verdad, sin dejar rastro, y lo sirves en Docker junto a la base. Es lo justo para tu proyecto. Para seguir: [bc-fastapi](https://github.com/ergrato-dev/bc-fastapi).

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Explicar** qué hacen el servidor (uvicorn), la aplicación (FastAPI) y ASGI, y **leer** una petición y una respuesta desde el lado del servidor
- **Declarar** rutas con parámetros de ruta, de consulta y de cuerpo, validados con Pydantic, y **leer** un 422
- **Elegir** el código de cada respuesta (200, 201, 204, 404, 422, 503) y **controlar** lo que sale con el tipo de retorno
- **Abrir** una sesión de SQLAlchemy por petición con una dependencia, y el motor una vez con el lifespan
- **Decidir** entre `def` y `async def`, y **explicar** qué pasa si una `async def` bloquea
- **Probar** una API con `TestClient` y `dependency_overrides`, y **servirla** en Docker con su *healthcheck*

---

## 📋 Prerrequisitos

- [Semana 19](../week-19-postgresql_psycopg_sqlalchemy_y_alembic/README.md): PostgreSQL con psycopg, SQLAlchemy y Alembic.
- El *pull request* `week-19` de tu proyecto fusionado en `main`.
- Docker funcionando, y `curl` en tu terminal: `curl --version`.

---

## 🗂️ Estructura de la Semana

```
week-20-fastapi_lo_justo_para_servir_tu_proyecto/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 19 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · De la CLI a la web: HTTP, ASGI y FastAPI](1-teoria/01-de-la-cli-a-la-web-http-asgi-y-fastapi.md) | Por qué una API, petición y respuesta desde el servidor, códigos, uvicorn y ASGI, FastAPI en una página, OpenAPI y lo que queda fuera | 45 min |
| [02 · Rutas, parámetros y modelos](1-teoria/02-rutas-parametros-y-modelos.md) | Ruta, consulta y cuerpo, `Path` y `Query`, modelos de entrada, el 422 por dentro, el tipo de retorno, códigos y cabeceras, y las reglas de la base | 50 min |
| [03 · Dependencias, sesiones y ciclo de vida](1-teoria/03-dependencias-sesiones-y-ciclo-de-vida.md) | `Depends`, dependencias con `yield`, una sesión por petición, dónde va el `commit`, lifespan y `create_app(url)`, el 503 y `dependency_overrides` | 45 min |
| [04 · def o async def: concurrencia en el servidor](1-teoria/04-def-o-async-def-concurrencia-en-el-servidor.md) | El bucle de eventos del servidor, hilos para las rutas `def`, qué bloquea, el pool de conexiones y `--workers` | 40 min |
| [05 · Probar y servir una API](1-teoria/05-probar-y-servir-una-api.md) | `TestClient`, la fixture `client`, qué comprobar, probar el `commit` y el 503, `servir` sin servir, importar tarde y la API en Docker | 1 h |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, lo ejecutas y comparas con la salida esperada. Preparan el proyecto. Los tres primeros no necesitan nada más que `uv`; el 04 trae su PostgreSQL (`docker compose up -d --wait`), en el puerto 5433 para no chocar con el de tu proyecto.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · Tu primera API](2-practicas/ejercicio-01-primera-api/README.md) | Una ruta, parámetros de ruta y de consulta con su 422, `HTTPException`, el 404 y el 405, `/openapi.json` y `/docs`, y uvicorn de verdad | 1 h 30 min |
| [02 · Cuerpos y respuestas con Pydantic](2-practicas/ejercicio-02-cuerpos-y-respuestas-con-pydantic/README.md) | Un modelo de entrada, cuatro 422, reglas con `Field`, un modelo de respuesta que filtra, 201 con `Location`, 204, fechas y *dataclasses* | 1 h 30 min |
| [03 · Dependencias y ciclo de vida](2-practicas/ejercicio-03-dependencias-y-ciclo-de-vida/README.md) | `Depends`, `yield`, la caché por petición, `dependency_overrides`, el lifespan y cinco peticiones contra `def`, `async def` que bloquea y `async def` que espera | 1 h 30 min |
| [04 · Una API con PostgreSQL](2-practicas/ejercicio-04-una-api-con-postgresql/README.md) | `create_app(url)`, una sesión por petición, commit y 201, 404, 503 sin la contraseña, tests que no dejan rastro y el SQL de cada petición | 1 h 30 min |

### Proyecto

Añades a tu Observatorio el módulo `api.py` y el comando `servir`:

- `create_app(url)`, con el motor en el lifespan, y `get_session`, una sesión por petición;
- seis rutas sobre las funciones de `database.py`: `/health`, `GET` y `POST /loads`, las medidas de una carga, `DELETE` y `/stats`;
- `ReadingIn`, que hereda de `MeasurementIn` (semana 13), y `LoadIn`, con los límites de las columnas;
- un 503 sin la contraseña cuando PostgreSQL no contesta;
- `observatorio servir`, que importa FastAPI solo cuando sirve, y un servicio `api` en `compose.yaml`.

Por el camino, un refactor (`database_url`). Después mides cuántas peticiones por segundo atiende, y haces una prueba de mutación. La versión sube a `0.20.0`. **Es el único entregable de la semana.**
→ [3-proyecto/README.md](3-proyecto/README.md)

---

## ⏱️ Distribución del Tiempo (18 horas)

| Actividad | Tiempo |
| --------- | ------ |
| Teoría (5 archivos) | 4 h |
| Ejercicio 01 | 1 h 30 min |
| Ejercicio 02 | 1 h 30 min |
| Ejercicio 03 | 1 h 30 min |
| Ejercicio 04 | 1 h 30 min |
| Proyecto | 6 h 30 min |
| Recursos y glosario | 30 min |
| Autoevaluación (cuestionario de la rúbrica) | 1 h |
| **Total** | **18 h** |

---

## 🎩 Trucos y atajos

| Truco | Cómo |
|---|---|
| Probar una ruta desde el navegador | <http://127.0.0.1:8000/docs>, la ruta, **Try it out** |
| Ver el código y las cabeceras | `curl -i http://127.0.0.1:8000/health` |
| Solo el código | `curl -s -o /dev/null -w '%{http_code}\n' URL` |
| Enviar JSON | `curl -s -X POST URL -H 'content-type: application/json' -d '{...}'` |
| JSON legible | `curl -s URL \| python -m json.tool` |
| Servir en otro puerto | `uv run observatorio servir -p 8001` |
| ¿Qué ocupa el puerto 8000? | `docker ps --format '{{.Names}} {{.Ports}}'`, o `ss -ltnp \| grep 8000` |
| Solo los tests de la API | `uv run pytest tests/test_api.py -q` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-20` de `python-<nombre>-<apellido>` con:
   - `api.py` con `ReadingIn`, `LoadIn`, `Health`, `get_session`, las seis rutas, `database_unavailable` y `create_app`;
   - `cli.py` con `database_url` y el comando `servir`;
   - `compose.yaml` con el servicio `api`, las dependencias `fastapi==0.162.0`, `uvicorn==0.54.0` y `httpx2==2.16.0` (en `dev`), la versión `0.20.0` y al menos 6 tests propios en `tests/test_my_api.py`.

   Todo en verde en tu máquina y en Docker, con `ruff check`, `ruff format --check`, `mypy`, `coverage report` y `alembic check` sin avisos.
2. ✅ `README.md` del repositorio con el comando `servir` y la sección "API"
3. ✅ Pull request `week-20` → `main` con:
   - tests, `mypy`, `ruff`, la cobertura y `alembic check`;
   - la tabla de medidas del paso 12;
   - la tabla de mutantes y el test que mata al superviviente;
   - por qué las rutas son `def`, y por qué el `commit` va en la ruta.

El cuestionario de la [rúbrica](rubrica-evaluacion.md) es tu autoevaluación: respóndelo antes de mirar las respuestas.

---

## ✅ Verificación

En tu proyecto:

```bash
docker compose up -d --wait db
uv run pytest
uv run ruff check && uv run ruff format --check
uv run mypy
uv run coverage run -m pytest -q && uv run coverage report
uv run alembic upgrade head && uv run alembic check
uv run observatorio --version
docker compose build app && docker compose run --rm app
docker compose up -d --wait api && curl -s http://127.0.0.1:8000/health
```

Lo que debes ver:

- `db` y `api` salen `Healthy`;
- los tests terminan en `passed` sin `failed`, al menos 761;
- ruff dice `All checks passed!` y `N files already formatted`;
- `mypy` dice `Success: no issues found`;
- `coverage report` termina sin `Coverage failure`;
- `alembic check` dice `No new upgrade operations detected.`;
- `--version` escribe `observatorio 0.20.0`;
- `curl` escribe `{"status":"ok","version":"0.20.0"}`.

En los ejercicios, cada paso descomentado da la salida que muestra su README, con los tiempos de tu máquina.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 19](../week-19-postgresql_psycopg_sqlalchemy_y_alembic/README.md) | **Semana 20** | Semana 21 (próximamente) |
