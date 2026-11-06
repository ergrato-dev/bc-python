# 03 · Tiempo límite y cancelación

⏱️ 45 min

## 🎯 Objetivos

- Poner un tiempo máximo a una espera con `asyncio.timeout`.
- Explicar cómo llega una cancelación a una tarea, y qué debe hacer la tarea.
- Limpiar recursos al cancelar sin tragarse la cancelación.
- Recibir resultados en orden de llegada con `as_completed`, y el primero con `wait`.
- Saber para qué sirve `shield`, y por qué casi nunca lo necesitas.

---

## 1. Nada espera para siempre

Una red se cae, un servidor deja de responder, un sensor se apaga. Si tu programa espera sin límite, se queda colgado sin error. Toda espera que dependa de otro sistema necesita un **tiempo máximo**.

```python
try:
    async with asyncio.timeout(2):
        line = await read("Norte")
except TimeoutError:
    print("Norte no responde")
```

`asyncio.timeout(segundos)` es un gestor de contexto asíncrono:

- todo lo que hay **dentro** del bloque comparte el mismo plazo, no cada `await` por separado;
- si el plazo vence, **cancela** la tarea que está esperando dentro del bloque;
- al salir del bloque, convierte esa cancelación en un **`TimeoutError`**, la excepción de siempre de Python;
- con `None`, no pone límite. Por eso `vigilar` puede escribir `asyncio.timeout(tiempo)` tanto si el usuario da `--tiempo` como si no.

Variantes:

| Herramienta | Qué hace |
|---|---|
| `asyncio.timeout(segundos)` | Un plazo relativo a ahora, para un bloque |
| `asyncio.timeout_at(instante)` | Un plazo absoluto, en el reloj del bucle (`loop.time()`): útil para dar el mismo final a varias esperas |
| `asyncio.wait_for(esperable, segundos)` | Lo mismo para una sola espera, en una línea. Es la forma anterior a Python 3.11 |
| `cm.reschedule(nuevo)` | Mueve el plazo de un `timeout` ya abierto (`async with asyncio.timeout(5) as cm:`) |

## 2. Cómo llega una cancelación

`task.cancel()` no detiene una tarea en seco. **Pide** que se cancele:

1. el bucle marca la tarea;
2. la próxima vez que la tarea esté parada en un `await`, ese `await` lanza **`asyncio.CancelledError`** dentro de ella;
3. la excepción sube por la pila de la tarea, como cualquier otra, ejecutando los `finally` y los `__aexit__` que encuentre;
4. si llega arriba del todo, la tarea termina **cancelada**: `task.cancelled()` es `True`, y quien la espere con `await` recibe la `CancelledError`.

Consecuencia: una tarea solo se puede cancelar en un `await`. Una tarea que calcula durante 10 s sin ningún `await` no se entera de la cancelación hasta que termina (teoría 04).

`TaskGroup`, `timeout` y `asyncio.run` usan este mismo mecanismo. Cuando el grupo de `watch_files` cancela las demás tareas, o el `--tiempo` de `vigilar` se agota, a cada tarea le llega una `CancelledError` en el `asyncio.sleep` donde está esperando.

## 3. Limpiar sin tragarse la cancelación

Cuando te cancelan, puedes **limpiar** (cerrar un archivo, una conexión, escribir un registro), pero después tienes que **dejar pasar** la cancelación:

```python
async def read(station: str) -> str:
    connection = await connect(station)
    try:
        return await connection.read()
    finally:
        await connection.close()   # se ejecuta también al cancelar
```

O, si necesitas saber que fue una cancelación:

```python
    except asyncio.CancelledError:
        log.info("cancelada %s", station)
        raise   # ← imprescindible
```

`CancelledError` hereda de **`BaseException`**, no de `Exception`, justo para que un `except Exception:` no la capture por accidente. Si la capturas y no la relanzas, la tarea sigue como si nada: `timeout` no puede convertirla en `TimeoutError`, y `TaskGroup` se queda esperando a una tarea que debía haber parado.

## 4. `as_completed` y `wait`

Como en la semana 16, a veces no quieres los resultados en orden, sino según **llegan**:

```python
for next_result in asyncio.as_completed([read("lenta"), read("rápida")]):
    print(await next_result)   # primero rápida, después lenta
```

Desde Python 3.13, `as_completed` también se puede recorrer con `async for`, y entonces da las propias tareas:

```python
async for task in asyncio.as_completed(tasks):
    print(task.result())
```

`asyncio.wait(tareas, return_when=...)` devuelve dos conjuntos, `(hechas, pendientes)`, cuando se cumple la condición:

| `return_when` | Vuelve cuando |
|---|---|
| `ALL_COMPLETED` (por defecto) | Terminan todas |
| `FIRST_COMPLETED` | Termina la primera |
| `FIRST_EXCEPTION` | Falla la primera, o terminan todas |

Un uso típico: preguntar lo mismo a tres réplicas, quedarte con la primera respuesta y cancelar el resto.

```python
tasks = {asyncio.create_task(read(replica)) for replica in REPLICAS}
done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
for task in pending:
    task.cancel()
```

`wait` **no** cancela nada por su cuenta, ni lanza los errores de las tareas: hay que mirarlos con `task.exception()` o `task.result()`.

## 5. `shield`

`asyncio.shield(esperable)` protege una espera de la cancelación: si cancelan a quien espera, la tarea de dentro sigue corriendo. Sirve para trabajo que no debe quedar a medias, como guardar el último dato antes de salir.

Casi nunca lo necesitas, y es fácil usarlo mal: la tarea protegida sigue viva cuando nadie la espera, con los problemas de las tareas perdidas (teoría 02). Antes de usar `shield`, pregúntate si un `finally` con la limpieza no basta.

## 6. Interrumpir el programa

Con Ctrl+C, `asyncio.run` cancela la tarea principal; la cancelación baja a todas las tareas (los `finally` se ejecutan), el bucle se cierra y se lanza `KeyboardInterrupt` en el programa. Pruébalo con `vigilar`: el programa termina sin traza y con código 130.

---

## ⚠️ Errores comunes

| Error | Causa | Solución |
|---|---|---|
| El `timeout` no corta nada | El `await` lento está fuera del bloque `async with asyncio.timeout(...)` | Mete dentro todo lo que debe tener el plazo |
| `TimeoutError` no se captura con `except asyncio.CancelledError` | Al salir del bloque, `timeout` ya lo convirtió en `TimeoutError` | `except TimeoutError` |
| Una tarea no se cancela, o `timeout` no termina | La tarea captura `CancelledError` (o `BaseException`) y no la relanza | `raise` después de limpiar, o usa `finally` |
| Una tarea cancelada no se para | Calcula sin ningún `await`: la cancelación espera a su próximo `await` | Divide el cálculo, o llévalo a otro hilo o proceso |
| Tras `wait(FIRST_COMPLETED)`, las otras siguen corriendo | `wait` no cancela | Cancela tú las pendientes |

---

## ✅ Qué debes saber al terminar

- [ ] Cómo poner un plazo a un bloque con `timeout`, y qué excepción sale.
- [ ] Los cuatro pasos de una cancelación, y por qué solo ocurre en un `await`.
- [ ] Cómo limpiar al cancelar, y por qué hay que relanzar `CancelledError`.
- [ ] La diferencia entre `as_completed` y `wait`, y qué hace `FIRST_COMPLETED`.
- [ ] Qué pasa con las tareas de `vigilar` cuando se agota `--tiempo`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [02 · Tareas, gather y TaskGroup](02-tareas-gather-y-taskgroup.md) | **03 · Tiempo límite y cancelación** | [04 · Coordinar tareas y no bloquear el bucle](04-coordinar-tareas-y-no-bloquear-el-bucle.md) |
