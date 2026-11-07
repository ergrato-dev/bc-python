# 02 · httpx: clientes, plazos y errores

⏱️ 50 min

## 🎯 Objetivos

- Hacer peticiones con httpx y leer su respuesta.
- Usar un `Client` o un `AsyncClient` para reutilizar conexiones, con `with` y `async with`.
- Poner plazos con `httpx.Timeout` y limitar las conexiones con `httpx.Limits`.
- Distinguir las dos clases de error: no hubo respuesta, o la respuesta dice error.
- Saber por qué httpx y no `urllib` o `requests`.

---

## 1. Por qué httpx

La biblioteca estándar trae `urllib.request`, que funciona, pero es incómoda: sin plazos claros, sin sesiones, sin versión asíncrona. Durante años, la respuesta fue `requests`, que sigue muy viva pero **solo es síncrona**. **httpx** tiene casi la misma forma que `requests` y además:

- un cliente **asíncrono**, `AsyncClient`, con la misma API: lo que aprendiste en la semana 17 sirve tal cual;
- **plazo por defecto** de 5 s: `requests` puede esperar para siempre si no le dices nada;
- un transporte de pruebas, `MockTransport`, para responder sin red (teoría 05);
- es lo que usan FastAPI y su cliente de pruebas, que verás en la semana 20.

Se añade como dependencia del proyecto, con la versión fijada:

```bash
uv add httpx==0.28.1
```

## 2. Una petición

```python
import httpx

response = httpx.get("http://127.0.0.1:8000/medidas.json")
response.status_code       # 200
response.reason_phrase     # 'OK'
response.headers["content-type"]  # 'application/json'
response.text              # el cuerpo, como str
response.json()            # el cuerpo, ya convertido: una lista de dicts
response.is_success        # True con 2xx
response.is_error          # True con 4xx y 5xx
```

Para la consulta, un diccionario; para mandar JSON, `json=`; para tus cabeceras, `headers=`:

```python
httpx.get(url, params={"dia": "2026-11-06"}, headers={"Accept": "application/json"})
httpx.post(url, json={"label": "Norte", "value": 12.5})
```

`response.json()` no valida nada: si el cuerpo no es JSON, lanza `json.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`. En tu proyecto no lo usarás: le pasas `response.text` a Pydantic, que convierte y valida de una vez.

## 3. Un cliente para muchas peticiones

`httpx.get` abre una conexión, pide y la cierra. Abrir una conexión cuesta: buscar el nombre en el DNS, el saludo TCP y, con `https`, el saludo TLS. Si vas a hacer varias peticiones al mismo servidor, usa un **cliente**, que guarda las conexiones abiertas y las **reutiliza** (*connection pooling*):

```python
with httpx.Client(base_url="http://127.0.0.1:8000", timeout=10.0) as client:
    for name in ["norte", "sur", "este"]:
        response = client.get(f"/{name}.json")
```

El cliente es también donde pones lo que comparten todas las peticiones: `base_url`, `headers` (el `User-Agent`, el token), `timeout` y `follow_redirects`. El `with` es importante: al salir, **cierra las conexiones**. Sin él, quedan abiertas hasta que el recolector de basura se acuerde.

La versión asíncrona es idéntica, con `async with` y `await`:

```python
async with httpx.AsyncClient(timeout=10.0) as client:
    response = await client.get(url)
```

Mientras una petición espera la respuesta, el bucle de eventos atiende a las demás. Diez descargas con un `TaskGroup` (semana 17) tardan lo que la más lenta, no la suma.

**Un cliente por programa, no uno por petición.** Si creas un `AsyncClient` dentro de cada tarea, pierdes la reutilización. En tu Observatorio, la CLI crea uno con `async with` y se lo pasa a todas las descargas.

## 4. Plazos

Una petición puede quedarse esperando por muchas razones: el servidor está colgado, la red se cortó a medias, la respuesta es enorme. Un **plazo** (*timeout*) convierte esa espera infinita en un error que puedes tratar.

```python
httpx.Client(timeout=10.0)                    # 10 s para cada fase
httpx.Client(timeout=httpx.Timeout(10.0, connect=3.0))  # 3 s para conectar, 10 para el resto
httpx.Client(timeout=None)                    # sin plazo: casi nunca es buena idea
```

`httpx.Timeout` tiene cuatro fases: `connect` (abrir la conexión), `read` (esperar cada trozo de respuesta), `write` (mandar la petición) y `pool` (esperar a que quede libre una conexión del cliente). **Ninguno es un plazo total**: una respuesta que llega a gotas, un byte cada 9 s, nunca agota un `read` de 10. Para un límite total, `asyncio.timeout`, como en la semana 17.

Por defecto, httpx espera 5 s en cada fase. Tu Observatorio usa 10, configurable con `OBSERVATORIO_TIMEOUT` (teoría 04).

## 5. Cuántas conexiones a la vez

Un cliente abre, como mucho, 100 conexiones a la vez y guarda 20 abiertas para reutilizarlas (`httpx.Limits(max_connections=100, max_keepalive_connections=20)`). Si lanzas 500 tareas, 400 esperan su turno dentro del cliente.

Tu Observatorio pone su propio límite con un `asyncio.Semaphore`, como en `vigilar`: `--limite 4` significa cuatro descargas a la vez, ni una más. ¿Por qué no `Limits`? Porque el semáforo limita **toda** la descarga (pedir, validar, guardar), es el mismo patrón que ya conoces y no depende de httpx. Lo importante es tener **algún** límite: un servidor que recibe 500 peticiones de golpe del mismo cliente puede bloquearte.

## 6. Dos clases de error

Esta es la idea más importante de la teoría. Una petición puede salir mal de dos formas muy distintas:

| | No hubo respuesta | Hubo respuesta, y dice error |
|---|---|---|
| Ejemplos | No conecta, el nombre no existe, se agota el plazo, se corta | `404`, `401`, `503` |
| En httpx | Una **excepción**: `httpx.TransportError` y sus hijas | Una **respuesta** normal con `is_error == True` |
| ¿Reintentar? | Casi siempre sí | Según el código (teoría 01) |

httpx **no lanza** nada con un `404`: te da la respuesta y tú decides. Si quieres que lance, `response.raise_for_status()`:

```
httpx.HTTPStatusError: Client error '404 Not Found' for url 'http://x.test/a'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404
```

La familia de excepciones de httpx:

```
HTTPError
├── HTTPStatusError          ← raise_for_status(): hubo respuesta, con 4xx o 5xx
└── RequestError
    └── TransportError       ← no hubo respuesta
        ├── TimeoutException
        │   ├── ConnectTimeout, ReadTimeout, WriteTimeout, PoolTimeout
        ├── NetworkError
        │   ├── ConnectError    "[Errno 111] Connection refused"
        │   └── ReadError, WriteError, CloseError
        ├── ProtocolError       el servidor habló mal HTTP
        └── UnsupportedProtocol "Request URL is missing an 'http://' or 'https://' protocol."
```

Captura **lo más concreto que te sirva**. `except httpx.TransportError` agrupa todos los "no hubo respuesta"; `except httpx.HTTPError` lo agrupa todo; `except Exception` esconde tus propios bugs.

Ojo con dos detalles que verás en el proyecto:

- el mensaje de un error de red viene del sistema operativo y cambia de una máquina a otra (`[Errno 111] Connection refused`, `timed out`). El **nombre de la clase** es corto, no cambia y dice qué pasó: `type(problem).__name__` da `ConnectError` o `ReadTimeout`;
- un nombre de servidor que no existe es un `ConnectError` con `[Errno -2] Name or service not known`, no una excepción aparte.

## 7. Redirecciones y cabeceras por defecto

httpx **no sigue** las redirecciones (`301`, `302`...) si no se lo pides: te da la respuesta `3xx`. Con `follow_redirects=True`, va solo a la nueva `Location`. `requests` las sigue por defecto; httpx prefiere que lo decidas tú.

Sin decir nada, httpx manda `User-Agent: python-httpx/0.28.1`. Un cliente educado dice quién es: muchas API rechazan o limitan los `User-Agent` genéricos. El tuyo dirá `observatorio/0.18.0`.

---

## ⚠️ Errores comunes

| Error | Causa | Solución |
|---|---|---|
| `httpx.UnsupportedProtocol: Request URL is missing an 'http://' or 'https://' protocol.` | La URL no tiene esquema (`127.0.0.1:8000/a.json`) | Escribe `http://` delante, o comprueba las URLs antes de pedir |
| `httpx.ConnectError: [Errno 111] Connection refused` | No hay nadie escuchando en ese puerto | ¿Arrancaste el servidor? ¿Es el puerto correcto? |
| `httpx.ReadTimeout: timed out` | El servidor tardó más que el plazo en contestar | Sube el plazo o reintenta |
| Un `404` "no da error" | httpx no lanza con `4xx`/`5xx` | Mira `response.is_error` o llama a `raise_for_status()` |
| Un `200` con el cuerpo vacío | Era una redirección `3xx` y no la seguiste | `follow_redirects=True` |
| Las descargas no van más rápido con un cliente por tarea | Cada cliente abre sus propias conexiones | Un solo cliente, compartido |

---

## ✅ Qué debes saber al terminar

- [ ] Cómo hacer una petición y qué te da la respuesta.
- [ ] Para qué sirve un cliente y por qué se usa con `with` o `async with`.
- [ ] Qué fases tiene `httpx.Timeout` y por qué ninguna es un plazo total.
- [ ] La diferencia entre "no hubo respuesta" y "la respuesta dice error", en httpx.
- [ ] Qué excepción capturar en cada caso.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [01 · HTTP: peticiones y respuestas](01-http-peticiones-y-respuestas.md) | **02 · httpx: clientes, plazos y errores** | [03 · Reintentos y espera exponencial](03-reintentos-y-espera-exponencial.md) |
