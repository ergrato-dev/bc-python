# Ejercicio 02 — Tareas, errores y cancelación

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-tareas-gather-y-taskgroup.md) y [03](../../1-teoria/03-tiempo-limite-y-cancelacion.md)

## Objetivo

Controlar un grupo de tareas cuando algo sale mal:

- lanzar tareas con `TaskGroup` y saber cuándo terminan;
- ver cómo un error **cancela** a las demás y llega como `ExceptionGroup`;
- seguir adelante con `gather(..., return_exceptions=True)`;
- poner un tiempo máximo con `asyncio.timeout`;
- cancelar una tarea a mano, y recibir resultados en orden de llegada;
- descubrir qué pasa con el error de una tarea que nadie espera.

Tu proyecto usa un `TaskGroup` en `watch_files` y un `timeout` en `vigilar`. Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-17-asyncio_corrutinas_tareas_y_colas/2-practicas/ejercicio-02-tareas-errores-y-cancelacion/starter
uv run python main.py
```

```
Ejercicio 02 · Tareas, errores y cancelación
```

`read(estación, segundos)` simula una lectura que tarda lo que le digas. Si la cancelan, escribe `cancelada` y **relanza** la `CancelledError`. `broken` es una estación que falla con un `ValueError`.

## Pasos

### 1. `TaskGroup`

Descomenta el **PASO 1** y ejecuta:

```
dentro del bloque: 0 terminadas
después del bloque: 2 terminadas
TaskGroup: ['Norte ok', 'Sur ok']
```

`async with asyncio.TaskGroup() as group:` abre un grupo. `group.create_task(...)` añade una tarea, que empieza a correr en cuanto el código cede el turno. Al **salir** del bloque, el grupo espera a que terminen todas. Dentro del bloque, ninguna ha terminado aún; después, todas. Es el `with pool:` de la semana 16: no puedes salir del bloque y olvidarte de una tarea.

`task.result()` da lo que devolvió cada tarea, en el orden en que las creaste.

### 2. Un error cancela a las demás

Descomenta el **PASO 2** y ejecuta:

```
  Norte: cancelada
  Este: cancelada
ExceptionGroup con 1 error: Sur: lectura imposible
tardó 0.1 s, no 1 s
```

`Sur` falla a los 0,1 s. El grupo **cancela** a `Norte` y `Este`, que iban a tardar 1 s, espera a que terminen de cancelarse y lanza un `ExceptionGroup` con el error. Las dos líneas de `cancelada` pueden salir en el otro orden.

Un `ExceptionGroup` es una excepción que lleva **varias** dentro, porque en un grupo pueden fallar varias tareas a la vez. `except* ValueError` captura las `ValueError` que haya en el grupo. Con un `except ValueError` normal no lo capturarías: lo que llega es un `ExceptionGroup`, no un `ValueError`.

¿Por qué cancelar? Si una parte del trabajo es imposible, seguir con el resto suele ser gastar tiempo en un resultado que no se va a usar. En tu proyecto, un archivo que falta **no** es un error de este tipo: `watch_file` lo convierte en un `FileReport` con `error`, y el grupo sigue.

### 3. `gather` con `return_exceptions`

Descomenta el **PASO 3** y ejecuta:

```
  str: Norte ok
  ValueError: Sur: lectura imposible
  str: Este ok
```

Con `return_exceptions=True`, `gather` no cancela a nadie: espera a todas y devuelve cada excepción **como un resultado más**, en su posición. Útil cuando los fallos son independientes. El precio: tienes que revisar cada resultado, y un bug se mezcla con los datos si no lo miras.

Sin `return_exceptions`, `gather` lanzaría el primer error, pero **no** cancelaría a las demás: seguirían corriendo sin que nadie las espere. Por eso, para tareas que van juntas, `TaskGroup` es la opción más segura.

### 4. Un tiempo máximo con `timeout`

Descomenta el **PASO 4** y ejecuta:

```
a tiempo: Norte ok
  Norte: cancelada
tarde: TimeoutError a los 0.3 s
```

`async with asyncio.timeout(0.3):` da 0,3 s a todo lo que hay dentro. Si se acaba el tiempo, **cancela** la tarea que espera dentro del bloque y, al salir, convierte la cancelación en un `TimeoutError`. Por eso ves `cancelada` antes del `TimeoutError`: es el mismo mecanismo que en el paso 2.

`TimeoutError` es la excepción de Python de siempre, la misma que lanzaría una conexión de red que no responde. Es lo que usa `vigilar --tiempo` en tu proyecto.

### 5. Cancelar una tarea a mano

Descomenta el **PASO 5** y ejecuta:

```
cancel() devuelve True
  Oriente: cancelada
cancelled() = True
```

`task.cancel()` **pide** la cancelación: devuelve `True` si la tarea aún no había terminado. La cancelación llega a la tarea como una `CancelledError` en el `await` donde está esperando. Ahí puede limpiar (cerrar un archivo, una conexión) con `except` o `finally`, pero debe **relanzarla**: si se la traga, la tarea sigue como si nada y quien la canceló no se entera.

Al esperar una tarea cancelada con `await task`, recibes la `CancelledError`. `task.cancelled()` dice si acabó así.

### 6. `as_completed`, en orden de llegada

Descomenta el **PASO 6** y ejecuta:

```
  llega rápida ok
  llega media ok
  llega lenta ok
```

Como en la semana 16: `as_completed` te da los resultados según **terminan**, no en el orden de entrada. Sirve para enseñar progreso o usar el primero que llegue. En tu proyecto, la tabla tiene que salir en el orden de los argumentos, así que `watch_files` guarda las tareas en una lista y lee `task.result()` en ese orden.

### 7. Una tarea que se pierde

Descomenta el **PASO 7** y ejecuta:

```
la corrutina principal termina sin enterarse del error
Task exception was never retrieved
future: <Task finished name='Task-35' coro=<broken() done, defined at .../main.py:21> exception=ValueError('Occidente: lectura imposible')>
Traceback (most recent call last):
  ...
ValueError: Occidente: lectura imposible
```

La tarea falla, pero nadie la espera: el programa sigue y termina "bien", con código 0. Solo al final, cuando Python borra la tarea, escribe en stderr `Task exception was never retrieved`. En un servidor que no termina nunca, ese aviso podría no salir jamás, y el error pasaría sin que nadie lo vea. Según tu terminal, el aviso puede salir antes o después de la línea de la corrutina principal: va por stderr.

Hay otro problema: el bucle solo guarda una referencia **débil** a cada tarea. Una tarea creada con `create_task` sin guardarla en ninguna variable puede ser borrada a medio camino. La solución a los dos es la misma: crea las tareas dentro de un `TaskGroup`, que las guarda y las espera por ti.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `except ValueError` no captura el error del paso 2 | Lo que llega es un `ExceptionGroup`: usa `except* ValueError` |
| `SyntaxError: cannot have both 'except' and 'except*' on the same 'try'` | Un mismo `try` usa solo `except` o solo `except*` |
| El paso 4 tarda 5 s | El `await` está fuera del bloque `async with asyncio.timeout(...)`: el tiempo solo cuenta dentro |
| La tarea del paso 5 no se cancela | `read` se traga la `CancelledError`: tiene que relanzarla con `raise` |
| `asyncio.exceptions.CancelledError` sin capturar | Esperaste una tarea cancelada sin `try`: la cancelación llega a quien la espera |
| No ves `Task exception was never retrieved` | Sale por stderr al final: si rediriges la salida con `>`, ejecuta sin redirigir |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Corrutinas y el bucle](../ejercicio-01-corrutinas-y-el-bucle/README.md) | **Ejercicio 02 · Tareas, errores y cancelación** | [Ejercicio 03 · Coordinar tareas](../ejercicio-03-coordinar-tareas/README.md) |
