# Glosario — Semana 17

| Término | Definición |
|---|---|
| **`aclose`** | `await generador.aclose()`: cierra un generador asíncrono a medias y ejecuta sus `finally`. `contextlib.aclosing` lo llama al salir de un `async with` |
| **`anext`** | `await anext(iterador)`: pide el siguiente elemento de un iterador asíncrono, como `next` en uno normal |
| **`as_completed`** | `asyncio.as_completed(esperables)`: da los resultados según terminan, no en el orden de entrada |
| **`async def`** | Define una función corrutina. Llamarla no ejecuta nada: devuelve una corrutina |
| **`async for`** | Recorre un iterador asíncrono: cada vuelta espera con `await anext(...)`, y mientras tanto el bucle atiende a otras tareas |
| **`async with`** | Usa un gestor de contexto asíncrono, cuya entrada y salida (`__aenter__`, `__aexit__`) pueden esperar |
| **`asynccontextmanager`** | Decorador de `contextlib` que convierte un generador asíncrono con un `yield` en un gestor para `async with` |
| **`asyncio.run`** | Crea un bucle de eventos, ejecuta una corrutina hasta el final, cancela lo que quede y cierra el bucle. La puerta de entrada de un programa asíncrono |
| **`await`** | Ejecuta un esperable y, si tiene que esperar, cede el turno al bucle hasta que esté listo. Solo dentro de `async def` |
| **Bloquear el bucle** | Ejecutar en una corrutina algo que para el hilo sin ceder el turno (`time.sleep`, `requests`, un cálculo largo): todas las tareas se detienen |
| **Bucle de eventos** | *Event loop*: el bucle que ejecuta las tareas por turnos, cada una hasta su próximo `await`, y duerme cuando ninguna está lista |
| **`CancelledError`** | La excepción que llega a una tarea cancelada en el `await` donde espera. Hereda de `BaseException` y hay que relanzarla después de limpiar |
| **Color de las funciones** | Nombre del problema de que una función normal no puede esperar a una `async`: el `async` se contagia hasta el `asyncio.run` |
| **Concurrencia cooperativa** | Varias tareas en un hilo que ceden el turno voluntariamente, en cada `await`. Con hilos, en cambio, el sistema operativo interrumpe cuando quiere |
| **Concurrencia estructurada** | Las tareas viven dentro de un bloque (`TaskGroup`) y no pueden seguir corriendo cuando el bloque termina; sus errores no se pierden |
| **Contrapresión** | *Backpressure*: frenar al productor cuando los consumidores no dan abasto. Con `Queue(maxsize=n)`, `put` espera si la cola está llena |
| **Corrutina** | El objeto que devuelve una función `async def`: un trabajo pendiente que el bucle ejecuta cuando alguien lo espera |
| **`create_task`** | `asyncio.create_task(corrutina)`: programa la corrutina como una tarea en el bucle y vuelve enseguida |
| **Esperable** | *Awaitable*: lo que puede ir detrás de `await`. Una corrutina, una `Task` o un `Future` |
| **`Event`** (`asyncio`) | Una señal: las tareas esperan con `await event.wait()` hasta que alguien llama a `event.set()` |
| **`except*`** | Captura las excepciones de un tipo que hay dentro de un `ExceptionGroup`. No se puede mezclar con `except` en el mismo `try` |
| **`ExceptionGroup`** | Excepción que lleva varias dentro, en `.exceptions`. La lanza `TaskGroup` cuando fallan sus tareas |
| **`gather`** | `asyncio.gather(*esperables)`: espera a todos y da los resultados en orden. Sin `return_exceptions`, un error no cancela a los demás |
| **Generador asíncrono** | Una función `async def` con `yield`. Da valores de uno en uno y puede esperar entre ellos; se recorre con `async for` |
| **Modo debug** | `asyncio.run(..., debug=True)` o `PYTHONASYNCIODEBUG=1`: avisa de cada paso de una tarea que tarda más de 0,1 s y de dónde se creó una corrutina olvidada |
| **`Queue`** (`asyncio`) | Cola entre tareas: `await put`, `await get`, `task_done`, `await join` y, desde 3.13, `shutdown` |
| **`QueueShutDown`** | La excepción que lanza `get` en una cola cerrada con `shutdown` y vacía, o `put` en una cola cerrada |
| **`Semaphore`** (`asyncio`) | `async with semaphore:` deja pasar como mucho N tareas a la vez. El `limit` de `watch_files` |
| **`shield`** | `asyncio.shield(esperable)`: protege una espera de la cancelación de quien la espera |
| **`Task`** | Una corrutina programada en el bucle. Como un `Future`: `done`, `result`, `exception`, `cancel`, `cancelled` |
| **`TaskGroup`** | `async with asyncio.TaskGroup() as group:` lanza tareas con `group.create_task`, las espera al salir y, si una falla, cancela al resto |
| **`timeout`** | `async with asyncio.timeout(segundos):` da un plazo al bloque. Al vencer, cancela lo de dentro y sale con `TimeoutError`. Con `None`, sin límite |
| **`to_thread`** | `await asyncio.to_thread(función, *args)`: ejecuta una función normal que bloquea en otro hilo, sin parar el bucle |
| **`wait`** | `asyncio.wait(tareas, return_when=...)`: devuelve `(hechas, pendientes)` cuando terminan todas, la primera o la primera que falla. No cancela nada |

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
