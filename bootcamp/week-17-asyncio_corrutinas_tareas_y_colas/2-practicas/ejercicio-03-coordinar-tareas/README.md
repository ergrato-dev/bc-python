# Ejercicio 03 — Coordinar tareas

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-coordinar-tareas-y-no-bloquear-el-bucle.md)

## Objetivo

Hacer que varias tareas trabajen juntas sin pisarse:

- limitar cuántas corren a la vez con un `Semaphore`;
- provocar una **condición de carrera** con un solo hilo, y arreglarla con `asyncio.Lock`;
- repartir trabajo con una `asyncio.Queue`: uno, varios consumidores y una cola con tope;
- dar una señal a todas las tareas con un `Event`;
- cerrar una cola con `shutdown`.

Son las mismas herramientas que en la semana 16 con hilos, en su versión de `asyncio`. Tu proyecto usa el `Semaphore` en `watch_files`. Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-17-asyncio_corrutinas_tareas_y_colas/2-practicas/ejercicio-03-coordinar-tareas/starter
uv run python main.py
```

```
Ejercicio 03 · Coordinar tareas
```

## Pasos

### 1. `Semaphore`: como mucho dos a la vez

Descomenta el **PASO 1** y ejecuta:

```
límite 2: a la vez como mucho 2 · 0.6 s
límite 6: a la vez como mucho 6 · 0.2 s
```

Seis lecturas de 0,2 s. Un `Semaphore(2)` tiene dos permisos: `async with semaphore:` coge uno y lo devuelve al salir. La tercera tarea espera en la puerta hasta que una de las dos primeras sale. Con dos a la vez, tres tandas: 0,6 s. Con seis permisos, todas a la vez: 0,2 s.

¿Para qué limitar, si todas a la vez es más rápido? Porque al otro lado hay alguien: un servidor que no acepta más de 10 conexiones, un sistema que se queda sin archivos abiertos. Con `asyncio` es fácil lanzar 10 000 tareas a la vez; el semáforo hace que solo trabajen unas pocas cada vez. Es el `--limite` de `vigilar` y el `max_workers` de la semana 16.

`active` y `peak` se modifican sin ningún `Lock`, y el resultado es correcto. Entre `active += 1` y la línea siguiente no hay ningún `await`, así que ninguna otra tarea puede colarse (paso 5 del ejercicio 01).

### 2. Una carrera en un solo hilo

Descomenta el **PASO 2** y ejecuta:

```
sin Lock: esperado 100 · obtenido 1
```

Cien tareas suman uno cada una, y el resultado es **1**. `add` lee el valor, hace un `await` y escribe. En el `await`, el bucle pasa a la tarea siguiente, que lee el **mismo** 0. Las cien leen 0 antes de que ninguna escriba, y las cien escriben 1.

Con hilos, la carrera de la semana 16 daba un número distinto cada vez. Aquí sale siempre 1, porque el bucle reparte los turnos siempre igual. Pero el fallo es el mismo: **leer, esperar y escribir**, con algo compartido. Un solo hilo no te protege si hay un `await` en medio.

### 3. `asyncio.Lock`

Descomenta el **PASO 3** y ejecuta:

```
con Lock: esperado 100 · obtenido 100
```

`async with self.lock:` deja entrar a una sola tarea. Las demás esperan **con `await`**, sin bloquear el bucle, hasta que sale. Leer, esperar y escribir quedan juntos.

No uses `threading.Lock` en código `asyncio`: su `acquire` bloquea el hilo entero, y con él el bucle y todas las tareas. Y si la tarea que lo tiene espera en un `await`, nadie puede soltarlo: el programa se cuelga.

### 4. Productor y consumidor con `Queue`

Descomenta el **PASO 4** y ejecuta:

```
un consumidor: ['c1:Norte', 'c1:Sur', 'c1:Oriente']
```

`asyncio.Queue` es la cola de la semana 16 para tareas: `await queue.get()` espera hasta que haya algo, sin bloquear el bucle. El consumidor nunca termina solo (`while True`). Para saber cuándo ha acabado el trabajo:

- el consumidor llama a `task_done()` después de procesar cada elemento;
- `await queue.join()` espera hasta que **todos** los elementos que entraron tengan su `task_done()`;
- después, `worker.cancel()` para al consumidor, que está esperando en un `get()` que ya no llegará.

`put_nowait` mete un elemento sin esperar. Con una cola sin tope, nunca tiene que esperar.

### 5. Varios consumidores y una cola con tope

Descomenta el **PASO 5** y ejecuta:

```
  pone Norte · en cola: 1
  pone Sur · en cola: 2
  pone Oriente · en cola: 1
  pone Occidente · en cola: 2
  pone Centro · en cola: 2
  pone Isla · en cola: 1
tres consumidores: 6 en 0.2 s
```

Con `maxsize=2`, la cola admite dos elementos. Cuando está llena, `await queue.put(...)` **espera** a que un consumidor saque uno. Es la **contrapresión** (*backpressure*): si el productor va más rápido que los consumidores, se frena en lugar de llenar la memoria.

Tres consumidores, seis estaciones de 0,1 s cada una: dos tandas, 0,2 s.

### 6. `Event`, una señal para todas

Descomenta el **PASO 6** y ejecuta:

```
  Norte espera la señal
  Sur espera la señal
señal
  Norte arranca
  Sur arranca
```

Un `Event` empieza apagado. `await start.wait()` espera hasta que alguien lo encienda con `start.set()`, y entonces **todas** las que esperaban siguen a la vez. Sirve para "empezad ya" o "parad ya". Fíjate en que `set()` no es una corrutina: no lleva `await`.

### 7. Cerrar la cola con `shutdown`

Descomenta el **PASO 7** y ejecuta:

```
  c0: la cola está cerrada, termino
  c1: la cola está cerrada, termino
procesadas: 6
```

En el paso 4 parabas al consumidor cancelándolo. `queue.shutdown()` (nuevo en Python 3.13) es más limpio: cierra la cola. Los `get()` siguientes sacan lo que queda y, cuando está vacía, lanzan `QueueShutDown`. Cada consumidor la captura y termina por sí mismo, y el `TaskGroup` puede salir. Un `put()` en una cola cerrada también lanza `QueueShutDown`.

Es lo mismo que el `None` por consumidor de la semana 16, sin tener que contar cuántos consumidores hay.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| El paso 1 da `a la vez como mucho 6` con límite 2 | El `await asyncio.sleep` está fuera del bloque `async with semaphore:` |
| El paso 3 sigue dando 1 | `add_safely` tiene que llamar a `add` **dentro** del `async with self.lock:` |
| El paso 4 o el 5 no terminan | Falta `queue.task_done()` en el consumidor: `join()` espera por cada elemento |
| `RuntimeWarning: coroutine 'Queue.put' was never awaited` | `put` es una corrutina: `await queue.put(...)`, o `put_nowait(...)` sin `await` |
| `TypeError: 'NoneType' object can't be awaited` | Escribiste `await start.set()`: `set()` es una función normal |
| `AttributeError: module 'asyncio' has no attribute 'QueueShutDown'` | Tu Python es anterior al 3.13: comprueba que usas el 3.14.10 del `.python-version` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Tareas, errores y cancelación](../ejercicio-02-tareas-errores-y-cancelacion/README.md) | **Ejercicio 03 · Coordinar tareas** | [Ejercicio 04 · Iteradores y gestores asíncronos](../ejercicio-04-iteradores-y-gestores-asincronos/README.md) |
