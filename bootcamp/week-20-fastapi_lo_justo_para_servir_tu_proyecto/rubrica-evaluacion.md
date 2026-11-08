# Rúbrica de Evaluación — Semana 20: FastAPI, lo justo para servir tu proyecto

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 19 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | ¿Qué hace uvicorn, qué hace FastAPI y qué es ASGI? ¿Por qué `TestClient` puede probar tu API sin abrir ningún puerto? | 10 |
| 2 | En `def get_stats(session: SessionDep, load: int \| None = None)`, ¿de dónde saca FastAPI cada parámetro? ¿Qué responde a `/stats?load=uno`, y se llega a ejecutar la función? | 10 |
| 3 | Un compañero quita `max_length=100` de `ReadingIn` "porque Pydantic ya valida". ¿Qué responde ahora la API a una etiqueta de 150 caracteres, y por qué es peor que antes? | 10 |
| 4 | `get_loads` devuelve `list_loads(session)` y su tipo de retorno es `list[LoadInfo]`. ¿Qué tres cosas hace FastAPI con ese tipo? ¿Qué pasaría si `LoadInfo` tuviera un campo `owner_email` y el tipo de retorno fuera otro modelo sin él? | 10 |
| 5 | Describe, en orden, qué pasa con la sesión en un `POST /loads`: desde que llega la petición hasta que se responde 201. ¿Por qué el `commit` va en la ruta y no después del `yield` de `get_session`? | 10 |
| 6 | ¿Por qué `create_app(url)` recibe la URL, en lugar de un `app = FastAPI()` a nivel de módulo que lea `Settings()`? Da dos razones | 10 |
| 7 | Un compañero cambia todas las rutas a `async def` "para que la API vaya más rápido". ¿Qué pasa con cinco peticiones a `/stats` a la vez? ¿Y con `/health` mientras tanto? | 10 |
| 8 | La fixture `client` sustituye `get_session` por la sesión del test. ¿Qué test del bootcamp seguiría pasando si quitaras el `session.commit()` de `post_load`, y cuál lo detecta? ¿Por qué? | 10 |
| 9 | Si PostgreSQL no contesta, ¿qué respondería la API sin `database_unavailable`, y qué responde con él? ¿Por qué su mensaje es fijo y no `str(problem)`? | 10 |
| 10 | En `compose.yaml`, el servicio `api` usa `--host 0.0.0.0` y publica `127.0.0.1:8000:8000`. ¿Por qué cada uno? ¿Por qué la API no aplica las migraciones al arrancar? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. **uvicorn** es el servidor: abre el puerto, acepta conexiones TCP y lee y escribe HTTP. **FastAPI** es la aplicación: busca la ruta, valida con Pydantic, llama a tu función y convierte el resultado en JSON. **ASGI** es el contrato entre los dos: el servidor llama a la aplicación con un diccionario que describe la petición (`scope`) y dos funciones, `receive` y `send`. Como la aplicación es solo eso, una corrutina, `TestClient` construye el `scope` y la llama directamente, igual que uvicorn: no hace falta red.
2. `session` es una **dependencia**: FastAPI llama a `get_session` y le pasa lo que entrega su `yield`. `load` es un tipo sencillo que no está en la ruta: sale de la **consulta**, y puede faltar (`None`). A `/stats?load=uno` responde **422**, con `loc: ["query", "load"]`, porque `"uno"` no se convierte en `int`. La función **no** se ejecuta.
3. La etiqueta pasaría la validación y llegaría a PostgreSQL, cuya columna es `String(100)`. PostgreSQL la rechaza con un `DataError` que nadie atrapa: la API responde **500**. Es peor porque quien llama no sabe qué hizo mal (un 500 dice "fallo del servidor"), el registro se llena de trazas por un error que no es tuyo y una alarma podría saltar. Con `max_length=100`, es un **422** con `loc` en la etiqueta. Lo que la base rechazaría, la API lo rechaza antes.
4. **Convierte** el resultado en JSON (la *dataclass* en un objeto, el `datetime` en ISO 8601), lo **valida** (si no cumple el tipo, es un 500 porque el error es tuyo) y lo **filtra**: solo salen los campos del tipo. Con un modelo de salida sin `owner_email`, el correo **no** saldría aunque el objeto lo tuviera: el tipo de retorno es el contrato y protege de filtrar datos que alguien añadió a lo guardado.
5. Llega la petición; FastAPI llama a `get_session`, que abre una `Session` con el motor de `app.state` y la entrega con `yield`. FastAPI valida el cuerpo con `LoadIn` (con 422 si no vale, y la sesión se cierra sin haber hecho nada). La ruta llama a `save_series`, que añade la carga y hace `flush` (PostgreSQL asigna el `id`), y después `session.commit()`. La ruta pone `Location` y devuelve el `LoadInfo`. Al terminar, el `with` de `get_session` cierra la sesión y devuelve la conexión al pool. El `commit` va en la ruta para que el 201 solo salga **si el commit funcionó**: si fallara después de que la ruta devolviera su resultado, quien llama podría recibir "creado" de algo que no está. Además, es quien escribe quien sabe que el trabajo está terminado, como `guardar` en la CLI.
6. Una: si `api.py` leyera `Settings()` al importarse, **importar el módulo dependería del entorno** y fallaría sin `OBSERVATORIO_DATABASE_URL` (en los tests, en `mypy`, en otro programa). Dos: con la URL como argumento, **cada uno decide cuál**: la CLI la lee de `Settings` y los tests pasan la de la base de pruebas, sin tocar el entorno. Y `api.py`, como `core`, no lee el entorno: recibe lo que necesita.
7. Las rutas usan una `Session` síncrona, que **bloquea** mientras espera a PostgreSQL. En una `async def` se ejecutan en el bucle de eventos, y mientras una espera, **nadie más avanza**: las cinco peticiones van una detrás de otra, y tardan cinco veces lo que una. `/health` también espera su turno: el servidor parece caído. Con `def`, FastAPI las ejecuta en hilos de su pool y avanzan a la vez. `async def` solo si todo lo de dentro espera con `await`.
8. Todos los tests que usan la fixture `client` seguirían pasando: la sesión es **la misma** durante todo el test, dentro de una transacción, y ve sus propios cambios aunque nadie los confirme. Lo detecta `test_own_engine_post_load_commits`: usa el **motor propio** de la aplicación (sin override), guarda con una aplicación y lee con **otra**, con otras conexiones. Sin `commit`, la sesión se cierra, PostgreSQL deshace el `INSERT` y la segunda aplicación no ve nada.
9. Sin el manejador, el `OperationalError` que lanza la primera consulta llegaría a FastAPI sin atrapar: **500**, con la traza en el registro. Con él, **503** ("ahora no puedo, inténtalo luego"), que es la verdad: el fallo es de un servicio del que dependes, no de tu código, y puede arreglarse solo. El mensaje es fijo porque el texto del error puede llevar el **usuario**, el **servidor** y el puerto de la base, y una respuesta HTTP la ve cualquiera que llame. `test_the_503_does_not_show_the_password` lo comprueba con una contraseña reconocible.
10. Dentro del contenedor, `127.0.0.1` es el propio contenedor: uvicorn solo se oiría a sí mismo, y Docker no podría llevarle las peticiones. Con **`0.0.0.0`** escucha en todas sus interfaces. Fuera, **`127.0.0.1:8000`** publica el puerto solo para tu máquina, no para la red: la API no comprueba quién llama, y cualquiera que la alcance puede borrar cargas. Las migraciones no las aplica al arrancar porque son un paso **aparte y único**: si arrancaran varias copias de la API a la vez, todas intentarían migrar la misma base. Se aplican antes con `docker compose run --rm app alembic upgrade head`.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños | El historial de `week-20` muestra un commit por paso (tests, dependencias, esqueleto, cada ruta, el 503, `database_url`, `servir`, versión, tests propios), sin cambiar los tests del bootcamp | 8 |
| Contrato con cuidado | Las reglas de `LoadIn` y `ReadingIn` coinciden con las columnas; códigos 201, 204, 404 y 503 donde tocan; ninguna respuesta con datos de la base ni contraseñas; `.env` fuera de Git | 8 |
| Ejecución en vivo | Ante el instructor: `uv run pytest`, `ruff`, `mypy`, `coverage report`, `observatorio servir`, un `POST` y un 422 con `curl`, `/docs` en el navegador, `observatorio cargas` con la carga recién creada, y la API en Docker con `docker compose up -d --wait api` | 8 |
| Rompe y explica | Quita el `session.commit()` de `post_load` y explica qué test falla y por qué solo ese; cambia una ruta a `async def` con `time.sleep` y explica qué pasa; para PostgreSQL con la API sirviendo y enseña el 503 | 8 |
| Explica sus medidas | Explica su tabla del paso 12 (por qué `/health` es la más rápida, dónde se va el tiempo del `POST`), y qué mutante sobrevivió y cómo lo mata su test | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 19

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| Modelos y contrato | `ReadingIn` hereda de `MeasurementIn` con `max_length=100`; `LoadIn` con `extra="forbid"` y los límites de `source` y de la lista; las rutas devuelven las *dataclasses* de `core`; `/openapi.json` con las seis rutas y sus métodos | 15 |
| Rutas | `/health` con `SELECT 1`; `GET` y `POST /loads` con 201, `Location` y `commit`; las medidas en orden con 404; `DELETE` con 204 y 404; `/stats` con `?load` y 404; todas `def`; pasan los tests de `test_api.py` | 20 |
| Dependencias y errores | `get_session` con una sesión por petición; `create_app(url)` con el motor en el lifespan y `dispose`; `database_unavailable` con un 503 y un mensaje fijo; `api.py` no lee el entorno | 15 |
| Comando | `database_url` compartida con `database()` sin cambiar sus mensajes; `servir` con `--host` y `-p`, códigos 2 sin URL o con una no válida, y FastAPI y uvicorn importados dentro | 10 |
| Tests propios | Al menos 6 tests en `tests/test_my_api.py` con datos del dominio: ida y vuelta, un 422 con `loc`, `/stats` de una carga, `DELETE` y 404, un 503 sin la contraseña; al menos uno mata el mutante que sobrevive a los tests del bootcamp | 15 |
| Calidad | `ruff check`, `ruff format --check`, `mypy`, `coverage report` y `alembic check` sin avisos; `api.py` al 100 %; `docker compose run --rm app` en verde y `api` sano; dependencias fijadas; versión `0.20.0` | 10 |
| Git y README | Rama `week-20` en `python-<nombre>-<apellido>`; README con `servir`, la sección "API" con la tabla de rutas, un ejemplo con `curl` y el aviso de que no hay autenticación | 5 |
| Pull request | Descripción con tests, `mypy`, `ruff`, cobertura y `alembic check`, las tablas de medidas y de mutantes, y las dos preguntas del paso 16 | 10 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | [Semana 21](../week-21-calidad_y_entrega_pre_commit_github_actions_auditoria_e_imagen_docker_segura/README.md) |
