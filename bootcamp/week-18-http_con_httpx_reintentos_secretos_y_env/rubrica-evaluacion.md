# Rúbrica de Evaluación — Semana 18: HTTP con httpx, reintentos, secretos y `.env`

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 17 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | `httpx.get` devuelve una respuesta con un `404` sin lanzar nada, pero lanza `ConnectError` si el servidor no existe. ¿Por qué la diferencia? ¿Cómo trata cada caso `get_text`? | 10 |
| 2 | `get_text` reintenta un `503` y un `ReadTimeout`, pero no un `404` ni un `401`. ¿Por qué? ¿Y por qué tu Observatorio puede reintentar sin miedo, y un programa que hace `POST` no? | 10 |
| 3 | Con `retries=3` y `backoff=0.5`, ¿cuántos intentos hay y cuánto se espera en total antes de rendirse? ¿Por qué tardan lo mismo una URL caída que dos? | 10 |
| 4 | ¿Para qué sirve el *jitter*? ¿Por qué tu Observatorio no lo usa, y cuándo lo añadirías? | 10 |
| 5 | Una respuesta `200` trae una página HTML de mantenimiento. ¿Qué pasa en `download`, qué ve el usuario y qué queda en la carpeta? ¿Por qué no se reintenta? | 10 |
| 6 | `make_client` tiene un parámetro `transport` que el programa nunca usa. ¿Para qué está? ¿Qué tendrías que hacer para probar `descargar` sin él? | 10 |
| 7 | La CLI abre **un** `AsyncClient` y se lo pasa a todas las descargas. ¿Qué ganas frente a abrir uno en cada `download`? ¿Por qué el cliente se abre con `async with`? | 10 |
| 8 | Escribes `OBSERVATORIO_TOKEN=abc123` en `.env` y exportas `OBSERVATORIO_TOKEN=xyz789` en tu terminal. ¿Qué token se manda? ¿Y si en `.env` pones `OBSERVATORIO_TOKEN=`, vacío, y no exportas nada? | 10 |
| 9 | ¿Qué protege `SecretStr`, y qué no? Si un compañero sube su `.env` a GitHub y lo borra en el commit siguiente, ¿está resuelto? ¿Qué tiene que hacer? | 10 |
| 10 | `core/remote.py` recibe el token como argumento y `settings.py` vive fuera de `core`. ¿Por qué no leer `Settings()` directamente en `make_client`? Piensa en los tests y en la semana 20 | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. Con un `404`, **hubo respuesta**: el servidor existe, te escuchó y dijo que el recurso no está. Es un dato, y httpx te deja decidir (`is_error`, `raise_for_status()`). Sin servidor **no hay respuesta** que devolver, así que solo queda una excepción, de la familia `TransportError`. `get_text` captura `TransportError` y la reintenta; con una respuesta, mira el código: si está en `RETRY_STATUSES` la reintenta, si es otro error lanza `FetchError` al momento, y si no, devuelve el texto.
2. Un `503` o un `ReadTimeout` pueden ser **pasajeros**: el servidor está saturado o la red se cortó un momento, y la siguiente vez puede salir bien. Un `404` o un `401` dicen que **la petición** está mal: repetirla da lo mismo y solo carga al servidor. El Observatorio solo hace `GET`, que es **idempotente**: repetirlo no cambia nada en el servidor. Un `POST` que falló a medias pudo haberse procesado, y repetirlo podría crear el recurso dos veces.
3. **Cuatro** intentos: `range(retries + 1)`, porque el primero no es un reintento. Las esperas van antes de cada reintento: 0,5 + 1 + 2 = **3,5 s**. Dos URLs tardan lo mismo porque cada descarga es una tarea del `TaskGroup` y espera con `await asyncio.sleep`: mientras una duerme, la otra también, en el mismo hilo. Las esperas se solapan, no se suman.
4. Para que muchos clientes que fallaron a la vez **no reintenten a la vez**: sin azar, todos vuelven al mismo instante y tumban otra vez al servidor (una estampida). Con *jitter*, las peticiones se reparten. El Observatorio es un solo cliente con unas pocas URLs, y una espera exacta es más fácil de medir y de probar (`waits == [0.5, 1.0, 2.0]`). Lo añadirías si muchas máquinas lo ejecutaran a la vez contra el mismo servidor, por ejemplo, desde un cron.
5. `get_text` devuelve el texto, porque es un `200`. `parse_measurements` falla: no es JSON, y lanza `DataFileError("datos no válidos en <url>: ...")`. `download` lo captura y devuelve un `FileReport` con `error`, **sin escribir** el archivo: el usuario ve `error: datos no válidos en ...` en stderr, la URL cuenta como `con error` y el código de salida es 1. No se reintenta porque el servidor **contestó**: preguntar otra vez dará la misma página.
6. Es una **costura**: el punto por donde un test cambia el transporte de verdad por un `httpx.MockTransport`, que contesta sin red lo que el test quiera (un `503`, un `ConnectError`, datos raros) y apunta las peticiones. Sin él, para probar `descargar` necesitarías un servidor real para cada caso, o parchear httpx por dentro. Con él, la *fixture* `served` sustituye `cli.make_client` por uno que llama al de verdad con `transport=MockTransport(...)`.
7. Un cliente **reutiliza las conexiones**: con varias URLs del mismo servidor, no repite el DNS, el saludo TCP ni el de TLS en cada una (ejercicio 01, paso 7). Además, las cabeceras, el plazo y el token se configuran en un solo sitio. `async with` **cierra** las conexiones al salir, haya error o no; sin él, quedan abiertas hasta que el recolector de basura se acuerde.
8. Se manda **`xyz789`**: una variable del entorno gana a la misma en `.env`. Con `OBSERVATORIO_TOKEN=` vacío y nada exportado, el token es **`None`**, y no se manda cabecera `Authorization`: lo decide `env_ignore_empty=True`. Sin esa opción, el token sería `""`, y cada petición llevaría un `Authorization: Bearer ` vacío.
9. `SecretStr` evita que el token salga **por accidente al imprimir**: `print`, `repr`, un registro o un `model_dump_json()` enseñan `'**********'`. No protege nada fuera del programa: ni un `.env` en Git, ni en una imagen Docker, ni un `get_secret_value()` que alguien imprima. Borrarlo en otro commit **no** lo resuelve: sigue en el historial, y quien clonó el repositorio, o cualquier copia en caché, lo tiene. Tiene que **revocar** el token en la web de la API, crear uno nuevo y, después, añadir `.env` al `.gitignore`.
10. Si `make_client` leyera `Settings()`, cada test que crea un cliente dependería del entorno y del `.env` de quien lo ejecuta, y para probar un token habría que tocar variables globales. Con el token como argumento, `core` es una función normal: le das lo que quieras y mira lo que hace. En la semana 20, la API de FastAPI leerá la configuración a su manera (una vez al arrancar el servidor) y usará el mismo `core` sin cambiarlo. Leer la configuración es cosa de **los programas**, no del núcleo.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños | El historial de `week-18` muestra un commit por paso (tests, dependencias, esqueleto, `parse_measurements`, `make_client`, reintentos, `download`, `download_all`, `Settings`, `descargar`, versión, tests propios), sin cambiar los tests del bootcamp | 8 |
| Secretos fuera del repositorio | Ningún commit del historial contiene `.env` ni un token; `.gitignore` y `.dockerignore` lo ignoran antes de que exista; `.env.example` sin valores | 8 |
| Ejecución en vivo | Ante el instructor: `uv run pytest`, `ruff check`, `ruff format --check`, `mypy`, `coverage report`, `descargar` contra `http.server` con una URL que falta, con `-v` y un token (que no aparece), con `OBSERVATORIO_RETRIES=0`, en su máquina y en Docker | 8 |
| Rompe y explica | Cambia `range(retries + 1)` por `range(retries)` y explica qué test falla y por qué; quita el `429` de `RETRY_STATUSES` y explica el fallo; quita `env_prefix` y explica por qué `TOKEN=x` ya se colaría | 8 |
| Explica sus medidas | Explica sus tiempos del paso 14 con las cuentas, por qué dos URLs tardan lo mismo que una, y qué mutante sobrevivió y cómo lo mata su test | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 17

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| `make_client` y `get_text` | `User-Agent` con la versión, `Authorization: Bearer` solo con token, plazo y `follow_redirects`; reintentos de `TransportError` y `RETRY_STATUSES` con espera exponencial y `asyncio.sleep`, sin esperar antes del primer intento; otros errores al momento; `FetchError` con el último fallo y los intentos | 20 |
| `download` y `download_all` | `target_of` con el último trozo de la ruta; `parse_measurements` antes de guardar; nada guardado si falla; escritura con `to_thread`; `TaskGroup` y `Semaphore(limit)`, resultados en el orden de entrada; sin `asyncio.run`, Typer, Rich ni `Settings` en `remote.py`; pasan los tests de `test_remote.py` | 15 |
| Configuración y comando | `Settings` fuera de `core` con prefijo, `.env`, `env_ignore_empty`, `SecretStr` y validación; `descargar` con `--carpeta` y `--limite`, URLs comprobadas, configuración no válida con código 2, `get_secret_value()` una sola vez, un cliente con `async with`, `show_reports` | 15 |
| Tests propios | Al menos 6 tests en `tests/test_my_remote.py` con datos del dominio y `MockTransport`, sin red: `get_text` con éxito, sin reintentar y con reintentos, `download` y su archivo, `Settings`; al menos uno mata el mutante que sobrevive a los tests del bootcamp | 20 |
| Calidad | `ruff check`, `ruff format --check`, `mypy` y `coverage report` sin avisos; `remote.py` y `settings.py` al 100 %; `docker compose run --build --rm app` en verde; dependencias fijadas; versión `0.18.0` | 10 |
| Git y README | Rama `week-18` en `python-<nombre>-<apellido>`; README con `descargar` y la configuración; `.env.example` en Git, `.env` no | 5 |
| Pull request | Descripción con tests, `mypy`, `ruff`, cobertura, las tablas de tiempos y de mutantes, y las dos preguntas del paso 17; sin ningún token en lo que se pega | 15 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | [Semana 19](../week-19-postgresql_psycopg_sqlalchemy_y_alembic/README.md) |
