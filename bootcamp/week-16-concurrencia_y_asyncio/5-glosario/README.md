# Glosario — Semana 16: Concurrencia y AsyncIO

| Término | Definición |
|---------|-----------|
| `async def` | Define una corutina — función que puede pausarse con `await`. Retorna un objeto corutina al ser llamada, no ejecuta el cuerpo. |
| `asyncio.as_completed()` | Iterador que produce cada awaitable en el orden en que termina, no en el orden de creación. |
| `asyncio.gather()` | Ejecuta múltiples awaitables concurrentemente y retorna sus resultados en el mismo orden de los argumentos. |
| `asyncio.run()` | Crea el event loop, ejecuta la corutina raíz y lo cierra. Solo debe llamarse una vez por programa. |
| `asyncio.Semaphore` | Primitiva de sincronización que limita cuántas corutinas pueden avanzar simultáneamente a través de un bloque `async with sem:`. |
| `asyncio.TaskGroup` | Context manager (Python 3.11+) para concurrencia estructurada. Cancela todos los tasks si uno falla. |
| `asyncio.timeout()` | Context manager (Python 3.11+) que lanza `TimeoutError` si el bloque no termina en el tiempo especificado. |
| `asyncio.wait()` | Espera un conjunto de Tasks con control fino: `FIRST_COMPLETED`, `FIRST_EXCEPTION`, `ALL_COMPLETED`. |
| `asyncio.wait_for()` | Envuelve un awaitable con un timeout. Compatible con Python 3.10+. |
| `await` | Suspende la corutina actual y cede control al event loop hasta que el awaitable complete. |
| backoff exponencial | Estrategia de retry donde el tiempo de espera crece como `base * 2^n`. Evita saturar un servicio que ya está fallando. |
| corutina | Función definida con `async def` cuya ejecución puede suspenderse y reanudarse. No es un thread — es código cooperativo. |
| CPU-bound | Código cuyo cuello de botella es la CPU (cálculo, compresión, codificación). El GIL impide paralelismo real con threads en Python puro. |
| event loop | Bucle único que gestiona múltiples tareas async. Cuando una tarea espera I/O, el loop avanza con otra tarea en lugar de bloquearse. |
| `Future` | Objeto de bajo nivel que representa un resultado futuro. `Task` es un subtipo de `Future`. Raramente se crea directamente. |
| GIL (Global Interpreter Lock) | Mutex interno de CPython que permite que solo un thread ejecute bytecode Python a la vez. Se libera automáticamente durante I/O. |
| I/O-bound | Código cuyo cuello de botella es la espera de red, disco, o dispositivos externos. asyncio y threading son efectivos aquí. |
| `ProcessPoolExecutor` | Executor que ejecuta funciones en procesos separados. Evita el GIL — permite paralelismo CPU real. |
| `run_in_executor()` | Método del event loop para delegar código síncrono bloqueante a un executor sin bloquear el loop. |
| `Task` | Corutina envuelta para ejecutarse en el event loop. Creada con `asyncio.create_task()` o `TaskGroup.create_task()`. |
| `ThreadPoolExecutor` | Executor que reutiliza un pool de threads para código síncrono I/O-bound. Limitado por el GIL para código CPU puro. |
| thundering herd | Problema donde muchos clientes reintentan simultáneamente después de un fallo, saturando el servidor recuperado. Se mitiga con jitter aleatorio en el backoff. |
| `aiofiles` | Biblioteca que provee versiones async de `open()`, `read()` y `write()` para no bloquear el event loop con I/O de disco. |
