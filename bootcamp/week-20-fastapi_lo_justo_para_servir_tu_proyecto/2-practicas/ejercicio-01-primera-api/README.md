# Ejercicio 01 — Tu primera API

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-de-la-cli-a-la-web-http-asgi-y-fastapi.md) y [02](../../1-teoria/02-rutas-parametros-y-modelos.md)

## Objetivo

Escribir una API pequeña con **FastAPI** y ver lo que hace sola:

- declarar **rutas** con `@app.get`;
- recibir **parámetros de ruta** y **de consulta** convertidos al tipo que anotas;
- ver el **422** cuando un parámetro no tiene el tipo que esperas;
- responder **404** con `HTTPException`, y ver el 404 y el 405 que FastAPI da solo;
- leer la **documentación** que FastAPI escribe: `/openapi.json` y `/docs`;
- servirla **de verdad** con uvicorn y llamarla por la red.

Hasta el paso 5 no hay servidor: `TestClient` llama a la aplicación directamente, como lo harán tus tests. Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-20-fastapi_lo_justo_para_servir_tu_proyecto/2-practicas/ejercicio-01-primera-api/starter
uv run python main.py
```

```
...
Ejercicio 01 · Tu primera API
```

`uv` instala `fastapi`, `uvicorn` y `httpx2`, el cliente que usa `TestClient` por dentro.

## Pasos

### 1. Una ruta

Descomenta el **PASO 1** y ejecuta:

```
--- Paso 1: GET / ---
estado: 200
tipo: application/json
cuerpo: {"mensaje":"hola desde FastAPI"}
como Python: {'mensaje': 'hola desde FastAPI'}
```

`@app.get("/")` registra la función: cuando llegue un `GET` a `/`, FastAPI la llama. Devuelves un diccionario de Python, y FastAPI lo convierte en **JSON**, con la cabecera `content-type: application/json` y el código **200**. `response.text` es el texto que viajó; `response.json()` lo vuelve a convertir en Python.

`client.get("/")` no abre ninguna conexión: `TestClient` construye la petición y se la pasa a la aplicación como lo haría un servidor.

### 2. Parámetros de ruta, con tipo

Descomenta el **PASO 2** y ejecuta:

```
--- Paso 2: /stations/{station_id} ---
/stations/2 -> {'id': 2, 'name': 'Sur', 'type': 'int'}
/stations/dos -> 422
   ['path', 'station_id'] Input should be a valid integer, unable to parse string as an integer
```

`{station_id}` en la ruta es un hueco, y el parámetro de la función con el mismo nombre lo recibe. En la URL todo es texto (`"2"`), pero la función recibe un `int`: FastAPI lee la **anotación** y convierte el valor con Pydantic. Si no puede, la función **no se llama**: responde **422** con la lista de problemas. Cada problema dice dónde está (`loc`: en la ruta, el parámetro `station_id`) y qué pasa (`msg`).

### 3. Parámetros de consulta

Descomenta el **PASO 3** y ejecuta:

```
--- Paso 3: /readings?... ---
sin parámetros       -> [12.5, 30.0, 7.5, 55.1, 41.0]
minimum=10&limit=2   -> [12.5, 30.0]
label=Sur            -> [30.0, 41.0]
limit=muchos         -> 422 ['query', 'limit']
```

Un parámetro que **no** está en la ruta es de la **consulta**: lo que va detrás del `?`. Con valor por defecto es opcional; con `str | None = None`, puede faltar. `params={...}` construye la consulta por ti, con los caracteres especiales bien escritos. El 422 dice ahora `query`: el problema está en la consulta.

### 4. Errores con `HTTPException`

Descomenta el **PASO 4** y ejecuta:

```
--- Paso 4: errores ---
GET /stations/1/name  -> 200 Norte
GET /stations/9/name  -> 404 {'detail': 'no existe la estación 9'}
GET /nada             -> 404 {'detail': 'Not Found'}
POST /stations/1/name -> 405 {'detail': 'Method Not Allowed'}
```

`raise HTTPException(404, ...)` corta la función y responde con ese código y `{"detail": ...}`. Es `raise` y no `return`: puedes lanzarla desde una función auxiliar, y FastAPI la recoge igual. Los otros dos errores no los escribes tú: una ruta que no existe es **404**; una que existe con otro método, **405**.

### 5. La documentación que FastAPI escribe sola

Descomenta el **PASO 5** y ejecuta:

```
--- Paso 5: /openapi.json ---
título: Estaciones · versión: 0.1.0
  GET  /                            parámetros: []
  GET  /stations/{station_id}       parámetros: ['station_id']
  GET  /readings                    parámetros: ['minimum', 'limit', 'label']
  GET  /stations/{station_id}/name  parámetros: ['station_id']
/docs -> 200 text/html; charset=utf-8
```

Con las rutas y sus anotaciones, FastAPI escribe la descripción **OpenAPI** de tu API: rutas, métodos, parámetros con sus tipos y respuestas. `/docs` es una página que la lee y te deja probar cada ruta desde el navegador. No la mantienes tú: cambia cuando cambia el código.

### 6. Un servidor de verdad

Descomenta el **PASO 6** y ejecuta:

```
--- Paso 6: uvicorn en 127.0.0.1:8001 ---
GET /           -> {'mensaje': 'hola desde FastAPI'}
GET /stations/3 -> {'id': 3, 'name': 'Este', 'type': 'int'}
servidor parado
```

Ahora sí hay red. **uvicorn** es el servidor: abre el puerto 8001, lee las peticiones HTTP que llegan por TCP y se las pasa a la aplicación por **ASGI** (teoría 01). Aquí corre en un hilo para que el programa pueda llamarlo con `httpx2` y pararlo después (`should_exit`).

Para verlo en el navegador, sírvelo sin hilo, con uvicorn desde la terminal:

```bash
uv run python -c "import uvicorn, main; uvicorn.run(main.app, port=8001)"
```

El programa ejecuta antes todos los pasos y después sirve hasta que pulses **Ctrl+C**. Abre <http://127.0.0.1:8001/docs>, despliega `GET /readings`, pulsa **Try it out** y prueba `limit=muchos`. En la terminal, uvicorn escribe una línea por petición.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `RuntimeError: The starlette.testclient module requires the httpx2 package` | Ejecutaste sin `uv run`, con otro entorno: `uv run python main.py` |
| `422` donde esperabas `200` | Lee `detail`: `loc` dice qué parámetro y dónde (`path`, `query`) |
| `404 Not Found` en una ruta que escribiste | Revisa la ruta letra por letra, y que el paso que la define esté descomentado |
| `[Errno 98] address already in use` en el paso 6 | Otro programa usa el puerto 8001: ciérralo o cambia `port=8001` |
| El paso 6 no termina | Falta `server.should_exit = True` antes de `thread.join()` |
| `/docs` en blanco en el navegador | La página baja su JavaScript de una CDN: necesita Internet |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Teoría 05 · Probar y servir una API](../../1-teoria/05-probar-y-servir-una-api.md) | **Ejercicio 01 · Tu primera API** | [Ejercicio 02 · Cuerpos y respuestas con Pydantic](../ejercicio-02-cuerpos-y-respuestas-con-pydantic/README.md) |
