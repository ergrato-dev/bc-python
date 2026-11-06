# Ejercicio 01 — Corrutinas y el bucle

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-corrutinas-y-el-bucle-de-eventos.md) y [02](../../1-teoria/02-tareas-gather-y-taskgroup.md)

## Objetivo

Dar los primeros pasos con `asyncio`, de la mano:

- ver que llamar a una función `async` no la ejecuta;
- esperar con `await`, una cosa detrás de otra;
- esperar cuatro cosas a la vez con tareas y con `gather`;
- comprobar que todo pasa en **un solo hilo**, por turnos;
- parar el bucle entero con una llamada que bloquea, y arreglarlo con `to_thread`.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-17-asyncio_corrutinas_tareas_y_colas/2-practicas/ejercicio-01-corrutinas-y-el-bucle/starter
uv run python main.py
```

```
Ejercicio 01 · Corrutinas y el bucle
```

`download` es la misma descarga falsa de la semana 16, ahora escrita con `async def`. Espera medio segundo con `await asyncio.sleep(0.5)`. Cada paso añade salida debajo de la anterior. Los tiempos de tu máquina pueden variar en el segundo decimal.

## Pasos

### 1. Una corrutina no se ejecuta sola

Descomenta el **PASO 1** y ejecuta:

```
download('Norte') es coroutine
asyncio.run da 'Norte;17.5'
```

Llamar a `download("Norte")` **no** ejecuta nada: devuelve un objeto **corrutina**, una tarea que todavía no ha empezado. Para ejecutarla hace falta un **bucle de eventos**. `asyncio.run` crea uno, ejecuta la corrutina hasta el final, devuelve su resultado y cierra el bucle.

Prueba a borrar la línea de `asyncio.run` y ejecuta. Python avisa al salir:

```
RuntimeWarning: coroutine 'download' was never awaited
```

Es el error más común de `asyncio`: olvidar el `await`. El programa no falla, simplemente no hace lo que creías. Vuelve a poner la línea.

### 2. `await`, una detrás de otra

Descomenta el **PASO 2** y ejecuta:

```
con await: 2.0 s · Norte;17.5
```

`await download(...)` ejecuta la corrutina y **espera** su resultado antes de seguir. Cuatro esperas de 0,5 s, una detrás de otra: 2 s, como el paso 1 de la semana 16.

`await` solo se puede escribir dentro de una función `async def`. Por eso el código va en `one_by_one`, y `asyncio.run(one_by_one())` arranca el bucle desde el programa normal.

### 3. Tareas que esperan a la vez

Descomenta el **PASO 3** y ejecuta:

```
tareas creadas: 5 (con la principal)
con tareas: 0.5 s · Occidente;31.5
```

`asyncio.create_task(corrutina)` **programa** la corrutina en el bucle y vuelve enseguida, como `Thread.start()`. Las cuatro tareas empiezan a esperar casi a la vez. Después, `await task` espera a cada una: cuando llegas a la segunda, ya casi ha terminado.

Total: 0,5 s, igual que con cuatro hilos, pero aquí no hay ningún hilo más. `all_tasks()` cuenta cinco: las cuatro descargas y la corrutina principal, que también es una tarea.

### 4. `gather`, los resultados en orden

Descomenta el **PASO 4** y ejecuta:

```
  termina rápido
  termina medio
  termina lento
gather: ['lento', 'medio', 'rápido']
```

`gather(*corrutinas)` las convierte en tareas, espera a todas y devuelve sus resultados **en el orden en que se las diste**, no en el que terminan. Es el `map` de `asyncio`, igual que `pool.map` en la semana 16.

### 5. Un solo hilo, turnos en cada `await`

Descomenta el **PASO 5** y ejecuta:

```
  A0 en MainThread
  B0 en MainThread
  C0 en MainThread
  A1 en MainThread
  B1 en MainThread
  C1 en MainThread
```

Las tres tareas corren en `MainThread`: no hay más hilos. El bucle ejecuta una tarea hasta que llega a un `await` que tiene que esperar, y entonces pasa a la siguiente. `asyncio.sleep(0)` no espera nada: solo **cede el turno**. Por eso salen intercaladas, A, B, C, A, B, C, y siempre en el mismo orden.

Esa es la gran diferencia con los hilos: un hilo puede ser interrumpido en **cualquier** instrucción; una tarea, solo en un `await`. Entre dos `await`, nadie se cuela.

### 6. Una llamada que bloquea para el bucle entero

Descomenta el **PASO 6** y ejecuta:

```
con time.sleep: 2.0 s
```

`blocking` es `async def`, pero llama a `read_slowly`, que usa `time.sleep`: una función normal que no sabe nada del bucle. Mientras duerme, el bucle **no puede** pasar a otra tarea, porque nadie le devuelve el turno. Las cuatro tareas se ejecutan una detrás de otra: 2 s.

Lo mismo pasa con cualquier función que bloquee: leer un archivo grande, `requests.get`, un cálculo largo. `async def` no hace rápido nada por sí solo: solo ayuda si dentro hay `await` de algo que de verdad espera.

ruff tiene reglas para esto: si escribes `time.sleep` **directamente** dentro de una función `async def`, avisa con ``ASYNC251 Async functions should not call `time.sleep` ``. Aquí no lo ve porque la llamada está escondida en otra función.

### 7. `to_thread`: lo que bloquea, a otro hilo

Descomenta el **PASO 7** y ejecuta:

```
con to_thread: 0.5 s
```

`asyncio.to_thread(función, *args)` ejecuta una función **normal** en un hilo aparte y te da algo que puedes esperar con `await`. Mientras el hilo duerme, el bucle sigue atendiendo a las demás tareas. Es lo que hace `watch_file` en tu proyecto para leer el archivo sin parar el bucle.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `RuntimeWarning: coroutine 'download' was never awaited` | Llamaste a una función `async` sin `await` ni `asyncio.run`: la corrutina nunca se ejecutó |
| `SyntaxError: 'await' outside function` o `'await' outside async function` | `await` solo puede ir dentro de `async def`. En el programa principal, usa `asyncio.run` |
| `RuntimeError: asyncio.run() cannot be called from a running event loop` | Llamaste a `asyncio.run` desde dentro de una corrutina: ahí se usa `await` |
| `RuntimeError: no running event loop` | `create_task` necesita un bucle en marcha: llámalo dentro de una corrutina |
| El paso 3 tarda 2 s | Creas cada tarea y la esperas en la misma vuelta del bucle: créalas todas primero y espéralas después |
| El paso 7 tarda 2 s | Llamas a `read_slowly(s)` en lugar de pasar la función: `to_thread(read_slowly, s)`, sin paréntesis en `read_slowly` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Iteradores, gestores y probar código asíncrono](../../1-teoria/05-iteradores-gestores-y-probar-codigo-asincrono.md) | **Ejercicio 01 · Corrutinas y el bucle** | [Ejercicio 02 · Tareas, errores y cancelación](../ejercicio-02-tareas-errores-y-cancelacion/README.md) |
