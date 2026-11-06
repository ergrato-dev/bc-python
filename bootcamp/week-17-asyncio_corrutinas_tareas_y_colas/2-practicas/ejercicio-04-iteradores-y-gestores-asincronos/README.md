# Ejercicio 04 — Iteradores y gestores asíncronos

⏱️ 1 h · Teoría previa: [05](../../1-teoria/05-iteradores-gestores-y-probar-codigo-asincrono.md)

## Objetivo

Las versiones asíncronas de dos herramientas que ya conoces, y cómo comprobar tu código:

- recorrer un **generador asíncrono** con `async for`, y en una comprensión;
- salir antes de tiempo y cerrar el generador con `aclose`;
- escribir un **gestor de contexto asíncrono** con `__aenter__`/`__aexit__` y con `@asynccontextmanager`;
- descubrir con el **modo debug** una llamada que bloquea el bucle;
- probar una corrutina con `asyncio.run`, sin plugins.

Tu proyecto usa un generador asíncrono, `replay`, y sus tests arrancan el bucle igual que el paso 7. Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-17-asyncio_corrutinas_tareas_y_colas/2-practicas/ejercicio-04-iteradores-y-gestores-asincronos/starter
uv run python main.py
```

```
Ejercicio 04 · Iteradores y gestores asíncronos
```

`ticker` es un **generador asíncrono**: una función `async def` con `yield`. Da una línea cada `interval` segundos, como una estación que manda una medida de vez en cuando.

## Pasos

### 1. `async for`

Descomenta el **PASO 1** y ejecuta:

```
  0.1 s · etiqueta;valor
  0.2 s · Norte;12,5
  0.3 s · Sur;8
  0.4 s · basura
  0.5 s · Oriente;55,1
```

Un `for` normal pide el siguiente elemento con `next()` y lo recibe enseguida. `async for` lo pide con `await anext()`: mientras `ticker` espera su `asyncio.sleep`, el bucle puede atender a otras tareas. Cada línea llega cuando está lista, no todas al final.

Un `for` normal sobre `ticker(...)` falla con `TypeError: 'async_generator' object is not iterable`: un generador asíncrono solo se recorre con `async for`.

### 2. Comprensiones asíncronas

Descomenta el **PASO 2** y ejecuta:

```
datos: ['Norte;12,5', 'Sur;8', 'Oriente;55,1']
```

`[x async for x in ...]` es una comprensión de lista sobre un iterador asíncrono. Solo puede ir dentro de una función `async def`, como `await`. El `if` filtra igual que en una comprensión normal, y `[1:]` quita la cabecera.

### 3. Salir antes y cerrar el generador

Descomenta el **PASO 3** y ejecuta:

```
  abro la conexión
  primera: etiqueta;valor
  segunda: Norte;12,5
  cierro la conexión
```

`await anext(stream)` pide un solo elemento. Después de dos, dejas el generador a medias, como un `break` en un `for`. El `finally` de `watched` tiene que ejecutarse para cerrar la conexión. `await stream.aclose()` lo fuerza: lanza `GeneratorExit` donde está parado el generador, y el `finally` se ejecuta.

Si no llamas a `aclose`, el generador se cierra más tarde, cuando el bucle se apaga al final de `asyncio.run`. Con un recurso de verdad (una conexión, un archivo), "más tarde" puede ser demasiado tarde. `contextlib.aclosing(generador)` lo cierra al salir de un `async with`.

Fíjate en la anotación: `AsyncGenerator[str]`, no `AsyncIterator[str]`. Los dos sirven para `async for`, pero solo un generador tiene `aclose`, y mypy lo sabe.

### 4. `async with` con una clase

Descomenta el **PASO 4** y ejecuta:

```
  conectada Norte
  leo de Norte
  desconectada Norte · ¿con error? False
  conectada Sur
  desconectada Sur · ¿con error? True
  fuera: lectura imposible
```

Un gestor de contexto **asíncrono** es uno cuya entrada y salida pueden hacer esperar: conectarse a una base de datos o a un servidor, cerrar la conexión. En lugar de `__enter__` y `__exit__`, tiene `__aenter__` y `__aexit__`, que son corrutinas, y se usa con `async with`.

Como en la semana 7, `__aexit__` se ejecuta **siempre**, también si hay un error dentro del bloque. Recibe la excepción en sus argumentos y, si devuelve `None`, la deja pasar: por eso el `ValueError` llega al `except` de fuera. `asyncio.TaskGroup`, `asyncio.timeout`, `Semaphore` y `Lock` son gestores asíncronos.

### 5. `asynccontextmanager`

Descomenta el **PASO 5** y ejecuta:

```
  conectada Oriente
  conectada Occidente
  leo de Oriente y Occidente
  desconectada Occidente
  desconectada Oriente
```

`@asynccontextmanager` es el `@contextmanager` de la semana 7 para `async with`: lo que hay antes del `yield` es la entrada; lo que hay en el `finally`, la salida. Con dos gestores en un mismo `async with`, se cierran en orden **inverso**: el último que se abrió, el primero que se cierra.

### 6. El modo debug encuentra lo que bloquea

Descomenta el **PASO 6** y ejecuta:

```
Executing <Task finished name='Task-16' coro=<sneaky() done, defined at .../main.py:134> result=None created at .../asyncio/runners.py:110> took 0.201 seconds
```

`asyncio.run(..., debug=True)` activa el **modo debug**: el bucle mide cuánto tarda cada tarea entre dos `await`, y avisa por stderr si pasa de 0,1 s. `sneaky` estuvo 0,2 s sin devolver el turno: durante ese tiempo, ninguna otra tarea pudo avanzar. Y si olvidas un `await`, el aviso `coroutine ... was never awaited` dice también dónde se creó la corrutina.

También lo puedes activar sin tocar el código, con una variable de entorno:

```bash
PYTHONASYNCIODEBUG=1 uv run python main.py
```

Úsalo cuando un programa asíncrono va más lento de lo que debería. Encuentra lo que el paso 6 del ejercicio 01 escondía en otra función, y que ruff no veía.

### 7. Probar una corrutina

Descomenta el **PASO 7** y ejecuta:

```
tests: 2 passed
```

Un test de una corrutina es una función **normal** que arranca el bucle con `asyncio.run` y comprueba el resultado. Es lo que hacen los tests de tu proyecto. pytest no ejecuta funciones `async def` sin un plugin (teoría 05).

Dentro de un test, una función `async` auxiliar como `collect` o `first` reúne lo que quieres comprobar: `asyncio.run` necesita una corrutina, y `await` solo puede ir dentro de `async def`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `TypeError: 'async_generator' object is not iterable` | Recorres un generador asíncrono con `for`: usa `async for` dentro de una función `async def` |
| `SyntaxError: asynchronous comprehension outside of an asynchronous function` | La comprensión con `async for` tiene que ir dentro de `async def` |
| No sale `cierro la conexión` en el paso 3 | Falta `await` delante de `stream.aclose()` |
| `TypeError: 'Station' object does not support the asynchronous context manager protocol` | Te falta `__aenter__` o `__aexit__`, o tu clase tiene `__enter__` y escribiste `async with` |
| mypy: `"AsyncIterator[str]" has no attribute "aclose"` | Anota el generador como `AsyncGenerator[str]` |
| El paso 6 no escribe nada | Falta `debug=True`, o la espera dura menos de 0,1 s |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Coordinar tareas](../ejercicio-03-coordinar-tareas/README.md) | **Ejercicio 04 · Iteradores y gestores asíncronos** | [Proyecto · Observatorio, capa 16](../../3-proyecto/README.md) |
