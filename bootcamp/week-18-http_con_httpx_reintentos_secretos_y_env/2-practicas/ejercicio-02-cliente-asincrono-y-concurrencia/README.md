# Ejercicio 02 — Cliente asíncrono y concurrencia

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-httpx-clientes-plazos-y-errores.md) y [05](../../1-teoria/05-probar-clientes-http-y-validar-lo-que-llega.md)

## Objetivo

Juntar lo de la semana 17 con httpx:

- hacer peticiones con `httpx.AsyncClient`;
- lanzar varias a la vez con un `TaskGroup` y medir cuánto ganas;
- limitar cuántas van a la vez, con un `Semaphore` o con `httpx.Limits`;
- tratar un error dentro del grupo con `except*`;
- poner un plazo total con `asyncio.timeout`;
- responder sin servidor con `httpx.MockTransport`.

Es exactamente lo que hace `download_all` en tu proyecto. Las peticiones van al servidor de prueba de `servidor.py`, como en el ejercicio 01. Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-18-http_con_httpx_reintentos_secretos_y_env/2-practicas/ejercicio-02-cliente-asincrono-y-concurrencia/starter
uv run python main.py
```

```
Ejercicio 02 · Cliente asíncrono y concurrencia
```

`SLOW` son seis rutas `/lenta?s=0.3`: cada una tarda 0,3 s en contestar. El `n=` solo las hace distintas.

## Pasos

### 1. `AsyncClient`

Descomenta el **PASO 1** y ejecuta:

```
200 {'label': 'Norte', 'value': 12.5}
```

La misma API que `httpx.Client`, con dos cambios: el cliente se abre con `async with` y cada petición se espera con `await`. Como todo código asíncrono, vive dentro de una corrutina que arranca `asyncio.run`.

### 2. Una detrás de otra

Descomenta el **PASO 2** y ejecuta:

```
una detrás de otra: 2.0 s
```

Seis peticiones de 0,3 s, una detrás de otra: 1,8 s, más lo que cuesta cada petición. Que el cliente sea asíncrono no hace nada por sí solo: cada `await client.get(...)` espera su respuesta antes de que el bucle `for` pase a la siguiente.

### 3. Todas a la vez, con `TaskGroup`

Descomenta el **PASO 3** y ejecuta:

```
todas a la vez: 0.3 s · [200, 200, 200, 200, 200, 200]
```

Cada petición es una **tarea**. Mientras una espera, el bucle de eventos manda la siguiente: las seis esperan a la vez, y el total es lo que tarda la más lenta. Al salir del bloque, el grupo ya esperó a todas, y `task.result()` da cada respuesta en el orden en que las creaste.

Fíjate en el `async with` con dos gestores: primero se abre el cliente y después el grupo; al salir, primero el grupo espera a sus tareas y después se cierra el cliente. Al revés, las tareas usarían un cliente cerrado.

### 4. Como mucho dos a la vez

Descomenta el **PASO 4** y ejecuta:

```
dos a la vez, con Semaphore: 1.0 s
```

Seis peticiones, dos a la vez: tres tandas de 0,3 s. Es el `--limite` de `descargar`, con el mismo patrón que `vigilar`: el `await` va **dentro** del `async with semaphore:`.

### 5. El límite del cliente, con `Limits`

Descomenta el **PASO 5** y ejecuta:

```
dos a la vez, con Limits: 1.0 s
```

El mismo resultado sin semáforo: `httpx.Limits(max_connections=2)` hace que el cliente abra como mucho dos conexiones, y las demás peticiones esperan dentro de httpx a que quede una libre. Por defecto, el límite es 100.

¿Cuál usar? `Limits` limita solo las conexiones de **ese** cliente. El semáforo limita lo que tú quieras: en tu proyecto, cada descarga entera (pedir, validar y guardar el archivo). Por eso `download_all` usa el semáforo.

### 6. Un error en el grupo

Descomenta el **PASO 6** y ejecuta:

```
falló: Client error '404 Not Found' for url 'http://127.0.0.1:36839/estaciones/oeste'
```

`checked` llama a `raise_for_status()`, y la estación `oeste` no existe. La excepción sale de su tarea, el grupo **cancela** las demás (la de `/lenta` no llega a terminar) y lanza un `ExceptionGroup`. `except* httpx.HTTPStatusError` lo captura, y `group_error.exceptions` tiene los errores de ese tipo.

En tu proyecto no quieres esto: que una estación falte no debería cancelar las demás descargas. Por eso `download` no deja escapar los errores esperados: los convierte en un `FileReport` con `error`, como `watch_file` en la semana 17. Solo un bug llega al grupo.

### 7. Un plazo para todo

Descomenta el **PASO 7** y ejecuta:

```
plazo total agotado: 0.5 s
```

El cliente tiene `timeout=10.0`, y ninguna petición lo agota: la más lenta tarda 3 s. Pero el conjunto no puede pasar de 0,5 s: `asyncio.timeout(0.5)` cancela las tareas que quedan y convierte la cancelación en `TimeoutError`, como `vigilar --tiempo`. El plazo de httpx es por fase de **cada** petición; el de `asyncio` es para **todo** lo que hay dentro del bloque.

### 8. Sin servidor, con `MockTransport`

Descomenta el **PASO 8** y ejecuta:

```
200 {'label': 'Norte', 'value': 99.9} · 503
peticiones: ['/estaciones/norte', '/estaciones/sur']
```

`http://falso.test` no existe, y no hace falta: con `transport=httpx.MockTransport(handler)`, el cliente no abre ninguna conexión. Llama a `handler` con cada petición y devuelve lo que ella devuelva. Así se prueban tus descargas: contestas lo que quieras (un `99.9` que el servidor de verdad nunca daría, un `503`) y después miras qué peticiones hizo tu código.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `RuntimeWarning: coroutine 'first' was never awaited` | Llamaste a la corrutina sin `asyncio.run(...)` |
| `TypeError: 'httpx.AsyncClient' object does not support the context manager protocol (missed __exit__ method) but it supports the asynchronous context manager protocol. Did you mean to use 'async with'?` | Lo que dice Python 3.14: un `AsyncClient` se abre con `async with` |
| El paso 3 tarda 2 s | Esperas cada petición antes de crear la siguiente: crea todas las tareas dentro del grupo |
| El paso 4 tarda 0,3 s | El `await client.get(...)` está fuera del `async with semaphore:` |
| `RuntimeError: Cannot send a request, as the client has been closed.` | Las tareas siguen después de cerrar el cliente: el grupo va **dentro** del `async with` del cliente, o después en la misma línea |
| El paso 8 da `httpx.ConnectError` | Te falta `transport=transport` en el cliente: intentó conectar con `falso.test` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Peticiones con httpx](../ejercicio-01-peticiones-con-httpx/README.md) | **Ejercicio 02 · Cliente asíncrono y concurrencia** | [Ejercicio 03 · Reintentos con espera](../ejercicio-03-reintentos-con-espera/README.md) |
