# Ejercicio 01 — Peticiones con httpx

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-http-peticiones-y-respuestas.md) y [02](../../1-teoria/02-httpx-clientes-plazos-y-errores.md)

## Objetivo

Hacer tus primeras peticiones HTTP con httpx y leer lo que vuelve:

- el código de estado, las cabeceras y el cuerpo, como texto y como datos;
- una consulta con `params`, bien codificada;
- una respuesta que dice error (`404`) y una petición que no recibe respuesta;
- un plazo que se agota;
- un cliente que reutiliza la conexión, con sus cabeceras, un `POST` y una redirección.

Todas las peticiones van a un **servidor de prueba** que arranca en tu máquina al ejecutar `main.py` (`servidor.py`, en la misma carpeta). No necesitas Internet ni leer ese archivo, aunque puedes: la lista de rutas está en su *docstring*. Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-18-http_con_httpx_reintentos_secretos_y_env/2-practicas/ejercicio-01-peticiones-con-httpx/starter
uv run python main.py
```

La primera vez, uv instala httpx 0.28.1 y sus dependencias. Después:

```
Ejercicio 01 · Peticiones con httpx
```

`BASE = start()` arranca el servidor en un hilo, en `127.0.0.1` y un puerto libre que elige el sistema (en tu máquina, otro número). El programa termina, y con él el servidor, al acabar `main.py`.

## Pasos

### 1. Una petición `GET`

Descomenta el **PASO 1** y ejecuta:

```
200 OK
application/json
[{"label": "Norte", "value": 12.5}, {"label": "Sur", "value": 8.0}, {"label": "Centro", "value": null}]
```

`httpx.get` manda la petición y espera la respuesta entera. La primera línea de la respuesta trae `200 OK`: `status_code` y `reason_phrase`. `headers` es un diccionario que no distingue mayúsculas: `headers["Content-Type"]` da lo mismo. Y `text` es el cuerpo tal cual llegó: **un texto**, aunque parezca una lista.

### 2. El cuerpo, como datos

Descomenta el **PASO 2** y ejecuta:

```
list 3
  Norte: 12.5
  Sur: 8.0
  Centro: sin dato
```

`.json()` convierte el texto con el módulo `json` de la biblioteca estándar: el `null` de JSON llega como `None`. Pero no comprueba nada: si al servidor le faltara `"value"` en una medida, el `item["value"]` fallaría con un `KeyError` aquí, lejos de la petición. Por eso tu proyecto no usa `.json()`, sino Pydantic sobre `.text`.

### 3. La consulta, con `params`

Descomenta el **PASO 3** y ejecuta:

```
http://127.0.0.1:34875/eco?dia=6+de+noviembre&unidad=%C2%B0C
{'dia': '6 de noviembre', 'unidad': '°C'}
```

La ruta `/eco` devuelve lo que le mandaste. httpx **codificó** la consulta: los espacios son `+` y el `°` es `%C2%B0`, sus dos bytes en UTF-8. El servidor la descodificó y recibió los textos originales. Si la hubieras pegado a mano en la URL (`f"{BASE}/eco?dia={dia}"`), un `&` dentro de un valor la habría partido en dos.

### 4. Una respuesta que dice error

Descomenta el **PASO 4** y ejecuta:

```
404 Not Found · is_error: True
HTTPStatusError · Client error '404 Not Found' for url 'http://127.0.0.1:34875/estaciones/oeste'
```

Fíjate en el orden: `httpx.get` **no lanzó nada**. Un `404` es una respuesta como otra cualquiera: el servidor existe, te escuchó y te dijo que esa estación no está. Eres tú quien decide si es un error, mirando `is_error` o llamando a `raise_for_status()`, que lanza `HTTPStatusError` con cualquier `4xx` o `5xx`. El mensaje completo tiene una segunda línea, con un enlace a la documentación del código; el `splitlines()[0]` se queda con la primera.

### 5. Sin respuesta

Descomenta el **PASO 5** y ejecuta:

```
ConnectError: [Errno 111] Connection refused
UnsupportedProtocol: Request URL is missing an 'http://' or 'https://' protocol.
```

Ahora sí hay excepciones, porque **no hay respuesta** que mirar. En el puerto 9 de tu máquina no escucha nadie: el sistema operativo rechaza la conexión. La segunda URL no tiene esquema, y httpx no sabe si hablar `http` o `https`. Las dos son `httpx.TransportError`.

El texto de `ConnectError` lo pone el sistema operativo: en Windows o macOS será distinto. El nombre de la clase es siempre el mismo. Por eso tu proyecto escribe `(ConnectError)` en sus mensajes, y no el texto.

### 6. Un plazo

Descomenta el **PASO 6** y ejecuta:

```
ReadTimeout: timed out · 0.5 s
```

La ruta `/lenta?s=2` tarda 2 s en contestar. Con `timeout=0.5`, httpx deja de esperar a los 0,5 s: la conexión se abrió bien, pero la respuesta no llegó a tiempo, y por eso es un `ReadTimeout`, no un `ConnectTimeout`. Sin el `timeout`, httpx habría esperado sus 5 s por defecto, y habría llegado la respuesta.

### 7. Un cliente reutiliza las conexiones

Descomenta el **PASO 7** y ejecuta:

```
5 peticiones sueltas · conexiones nuevas: 5
5 peticiones con un cliente · conexiones nuevas: 1
```

El servidor cuenta cuántas conexiones ha aceptado (el `- 1` descuenta la de `/conexiones`). Cada `httpx.get` suelto abre una conexión, pide y la cierra. Un `httpx.Client` la deja **abierta** y la usa para las cinco peticiones. Aquí no se nota, porque el servidor está en tu máquina; con un servidor lejano y `https`, cada conexión nueva cuesta varios viajes de ida y vuelta antes de la primera petición.

Fíjate también en `base_url`: dentro del cliente, las rutas son relativas (`"/estaciones"`).

### 8. Cabeceras, `POST` y redirecciones

Descomenta el **PASO 8** y ejecuta:

```
POST · ejercicio/1.0 · {"label":"Norte","value":12.5}
301 → /estaciones
200 /estaciones 3 medidas
```

Las cabeceras del cliente van en **todas** sus peticiones: el servidor vio tu `User-Agent`. `json=` convierte el diccionario a JSON, lo pone como cuerpo y añade `Content-Type: application/json`.

`/mover` contesta `301` con una cabecera `Location`. httpx no la sigue si no se lo pides: te da la respuesta `301`, que no tiene cuerpo. Con `follow_redirects=True`, hace la segunda petición él solo, y `response.url` es la URL final. Tu proyecto lo activa en el cliente: una API que se muda de dirección no debería romper tus descargas.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'httpx'` | Ejecutaste `python main.py`, o `uv run` desde otra carpeta: entra en `starter/` y usa `uv run python main.py`, que usa el entorno del ejercicio |
| El paso 2 da `TypeError: object of type 'method' has no len()` | Escribiste `.json` sin paréntesis: es un método, `.json()` |
| El paso 4 no escribe la segunda línea | Llamaste a `raise_for_status` sin paréntesis: no hace nada |
| El paso 6 tarda 2 s y no da error | Te falta `timeout=0.5` en `httpx.get` |
| El paso 8 da `KeyError: 'location'` en la segunda línea | Pusiste `follow_redirects=True` también en la primera petición: ya no es un `301` |
| La salida tiene otro puerto | Es normal: el sistema elige uno libre cada vez |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Probar clientes HTTP y validar lo que llega](../../1-teoria/05-probar-clientes-http-y-validar-lo-que-llega.md) | **Ejercicio 01 · Peticiones con httpx** | [Ejercicio 02 · Cliente asíncrono y concurrencia](../ejercicio-02-cliente-asincrono-y-concurrencia/README.md) |
