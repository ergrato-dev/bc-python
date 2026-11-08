# Semana 18 — HTTP con httpx, reintentos, secretos y `.env`

> Tus medidas viven en archivos de tu máquina. Las de verdad viven en otro sitio: un portal de datos abiertos, la API de una estación, el servidor de un compañero. Esta semana aprendes a ir a buscarlas con **HTTP**: qué viaja en una petición y en una respuesta, cómo pedir con **httpx** (también a la vez, con lo que sabes de `asyncio`), qué hacer cuando la red falla y cómo guardar un **token** sin que acabe en GitHub. Lo aplicas en `descargar`, un comando que baja varios JSON de medidas a la vez, reintenta lo que merece la pena, valida todo y lo guarda para el resto del Observatorio.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Explicar** qué viaja en una petición y una respuesta HTTP, y **decidir** qué hacer con cada código de estado
- **Hacer** peticiones con `httpx.Client` y `httpx.AsyncClient`, con plazos y límites, y **distinguir** "no hubo respuesta" de "la respuesta dice error"
- **Escribir** un bucle de reintentos con espera exponencial, y **explicar** qué se reintenta y qué no
- **Sacar** la configuración del código con variables de entorno, `.env` y `pydantic-settings`, y **proteger** los secretos con `SecretStr`
- **Probar** código que hace peticiones sin salir a Internet, con `MockTransport` y un servidor en `127.0.0.1`
- **Validar** lo que llega de un servidor antes de guardarlo

---

## 📋 Prerrequisitos

- [Semana 17](../week-17-asyncio_corrutinas_tareas_y_colas/README.md): asyncio, corrutinas, tareas y colas.
- El *pull request* `week-17` de tu proyecto fusionado en `main`.

---

## 🗂️ Estructura de la Semana

```
week-18-http_con_httpx_reintentos_secretos_y_env/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 17 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · HTTP: peticiones y respuestas](1-teoria/01-http-peticiones-y-respuestas.md) | El diálogo de texto, la URL por partes, métodos e idempotencia, códigos de estado, cabeceras, JSON, HTTPS y tokens | 45 min |
| [02 · httpx: clientes, plazos y errores](1-teoria/02-httpx-clientes-plazos-y-errores.md) | Por qué httpx, `Client` y `AsyncClient`, plazos por fases, `Limits`, las dos clases de error y la familia de excepciones | 50 min |
| [03 · Reintentos y espera exponencial](1-teoria/03-reintentos-y-espera-exponencial.md) | Qué se reintenta, espera exponencial, *jitter*, `Retry-After`, los dos topes y lo que ya existe | 45 min |
| [04 · Secretos y configuración con `.env`](1-teoria/04-secretos-y-configuracion-con-env.md) | Configuración fuera del código, `os.environ`, `.env` y `.env.example`, `pydantic-settings`, `SecretStr`, dónde no puede acabar un secreto y qué hacer si se filtra | 50 min |
| [05 · Probar clientes HTTP y validar lo que llega](1-teoria/05-probar-clientes-http-y-validar-lo-que-llega.md) | `MockTransport`, un servidor en `127.0.0.1`, reintentos sin esperar, la CLI sin tus variables, datos que no son de fiar y pedir con educación | 50 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, lo ejecutas y comparas con la salida esperada. Preparan el proyecto. Los tres primeros traen un servidor de prueba (`servidor.py`) que arranca en tu máquina: no necesitas Internet.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · Peticiones con httpx](2-practicas/ejercicio-01-peticiones-con-httpx/README.md) | `GET`, `.json()`, `params`, un `404`, un fallo de conexión, un plazo, un cliente que reutiliza la conexión, `POST` y redirecciones | 1 h 30 min |
| [02 · Cliente asíncrono y concurrencia](2-practicas/ejercicio-02-cliente-asincrono-y-concurrencia/README.md) | `AsyncClient`, seis peticiones en serie y a la vez, `Semaphore` y `Limits`, `except*`, un plazo total y `MockTransport` | 1 h 30 min |
| [03 · Reintentos con espera](2-practicas/ejercicio-03-reintentos-con-espera/README.md) | Un fallo pasajero, reintentar sin y con espera, qué se reintenta, *jitter*, `Retry-After`, un tope total y los reintentos de httpx | 1 h 30 min |
| [04 · Secretos y configuración](2-practicas/ejercicio-04-secretos-y-configuracion/README.md) | `os.environ`, `uv run --env-file`, `pydantic-settings`, validación, prioridades, `SecretStr` y `.gitignore` | 1 h |

### Proyecto

Añades a tu Observatorio el módulo `core/remote.py`, el archivo `settings.py` y el comando `descargar`:

- `make_client`, que prepara un `AsyncClient` con tu `User-Agent`, tu token y tu plazo;
- `get_text`, que pide una URL y reintenta los fallos pasajeros con espera exponencial;
- `download` y `download_all`, que bajan varios JSON de medidas a la vez, los validan y los guardan como `.txt`;
- `Settings`, que lee `OBSERVATORIO_TOKEN`, `OBSERVATORIO_TIMEOUT` y `OBSERVATORIO_RETRIES` del entorno o de `.env`;
- `observatorio descargar URLS... [-c DIR] [-l N]`, que termina con la tabla de `lote`.

Por el camino, un refactor: `parse_measurements`, que separa validar de leer el archivo. Después descargas de un servidor de verdad, mides lo que cuestan los reintentos y haces una prueba de mutación. La versión sube a `0.18.0`. **Es el único entregable de la semana.**
→ [3-proyecto/README.md](3-proyecto/README.md)

---

## ⏱️ Distribución del Tiempo (18 horas)

| Actividad | Tiempo |
| --------- | ------ |
| Teoría (5 archivos) | 4 h |
| Ejercicio 01 | 1 h 30 min |
| Ejercicio 02 | 1 h 30 min |
| Ejercicio 03 | 1 h 30 min |
| Ejercicio 04 | 1 h |
| Proyecto | 6 h 30 min |
| Recursos y glosario | 1 h |
| Autoevaluación (cuestionario de la rúbrica) | 1 h |
| **Total** | **18 h** |

---

## 🎩 Trucos y atajos

| Truco | Cómo |
|---|---|
| Un servidor de archivos en un segundo | `uv run python -m http.server 8000 --bind 127.0.0.1 --directory <carpeta>` |
| Ver cada petición y cada reintento | `uv run observatorio -v descargar ...`: `HTTP Request: GET ...` y `intento 1 de 4: ...` |
| Probar sin esperar los reintentos | `OBSERVATORIO_RETRIES=0 uv run observatorio descargar ...` |
| Cargar `.env` para cualquier orden | `uv run --env-file .env <orden>` |
| Comprobar que Git no verá `.env` | `git check-ignore -v .env`: si no escribe nada, **no** está ignorado |
| Ver qué variables tienes puestas | `env \| grep OBSERVATORIO` |
| Una petición rápida desde Python | `uv run python -c "import httpx; print(httpx.get('http://127.0.0.1:8000/').status_code)"` |
| Buscar un secreto antes de subir | `git diff --cached \| grep -i token` antes de cada `git commit` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-18` de `python-<nombre>-<apellido>` con:
   - `core/remote.py` con `make_client`, `get_text`, `target_of`, `download` y `download_all`, exportados desde `core`, y `parse_measurements` en `schemas.py`;
   - `settings.py` con `Settings`, fuera de `core`; `.env.example` en Git, y `.env` en `.gitignore` y `.dockerignore`;
   - el comando `descargar` con `--carpeta` y `--limite`, y la constante `BACKOFF`;
   - las dependencias `httpx==0.28.1` y `pydantic-settings==2.16.1`, la versión `0.18.0` y al menos 6 tests propios en `tests/test_my_remote.py`.

   Todo en verde en tu máquina y en Docker, con `ruff check`, `ruff format --check`, `mypy` y `coverage report` sin avisos.
2. ✅ `README.md` del repositorio con el comando `descargar` y cómo configurarlo
3. ✅ Pull request `week-18` → `main` con:
   - tests, `mypy`, `ruff` y la cobertura;
   - la tabla de tiempos de los reintentos, con tus cuentas;
   - la tabla de mutantes y el test que mata al superviviente;
   - por qué `core/remote.py` no lee la configuración, y qué fallos reintenta `get_text` y por qué.

El cuestionario de la [rúbrica](rubrica-evaluacion.md) es tu autoevaluación: respóndelo antes de mirar las respuestas.

---

## ✅ Verificación

En tu proyecto:

```bash
uv run pytest
uv run ruff check && uv run ruff format --check
uv run mypy
uv run coverage run -m pytest -q && uv run coverage report
uv run observatorio --version
git check-ignore -v .env
docker compose run --build --rm app
```

Y con el servidor del paso 14 del proyecto en otra terminal:

```bash
uv run observatorio descargar http://127.0.0.1:8000/norte.json http://127.0.0.1:8000/sur.json
```

Lo que debes ver:

- los tests terminan en `passed` sin `failed`, al menos 631;
- ruff dice `All checks passed!` y `N files already formatted`;
- `mypy` dice `Success: no issues found`;
- `coverage report` termina sin `Coverage failure`;
- `--version` escribe `observatorio 0.18.0`;
- `git check-ignore` escribe la línea de tu `.gitignore` que ignora `.env`;
- `descargar` escribe la tabla con `descargas/norte.txt` y `descargas/sur.txt`, y `archivos: 2 · con error: 0`.

En los ejercicios, cada paso descomentado da la salida que muestra su README, con los tiempos y el puerto de tu máquina.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 17](../week-17-asyncio_corrutinas_tareas_y_colas/README.md) | **Semana 18** | [Semana 19](../week-19-postgresql_psycopg_sqlalchemy_y_alembic/README.md) |

← [Volver al índice de semanas](../README.md)
