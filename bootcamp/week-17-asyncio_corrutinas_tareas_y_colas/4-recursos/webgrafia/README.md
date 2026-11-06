# Webgrafía — Semana 17

| Recurso | Para qué |
|---|---|
| [A Conceptual Overview of asyncio](https://docs.python.org/3.14/howto/a-conceptual-overview-of-asyncio.html) (en inglés) | La guía oficial que explica cómo funciona por dentro: el bucle, las tareas, `await` y los `Future`. El complemento de la teoría 01 |
| [`asyncio`](https://docs.python.org/es/3.14/library/asyncio.html) (en español) | El índice de la documentación: empieza aquí y sigue los enlaces de abajo |
| [Corrutinas y tareas](https://docs.python.org/es/3.14/library/asyncio-task.html) (en español) | `create_task`, `gather`, `TaskGroup`, `timeout`, `wait`, `as_completed`, `shield` y `to_thread`, con ejemplos. Las teorías 02 y 03 |
| [Primitivas de sincronización](https://docs.python.org/es/3.14/library/asyncio-sync.html) y [colas](https://docs.python.org/es/3.14/library/asyncio-queue.html) (en español) | `Lock`, `Event`, `Semaphore`, `Barrier` y `Queue` con `shutdown`: la teoría 04 y el ejercicio 03 |
| [Desarrollando con asyncio](https://docs.python.org/es/3.14/library/asyncio-dev.html) (en español) | El modo debug, las corrutinas que nunca se esperan y las excepciones que nadie recoge: el paso 6 del ejercicio 04 |
| [Introspección del grafo de llamadas](https://docs.python.org/3.14/library/asyncio-graph.html) (en inglés) | Nuevo en 3.14: ver qué tarea espera a cuál, desde el código o con `python -m asyncio ps` |
| [`contextlib`](https://docs.python.org/es/3.14/library/contextlib.html) (en español) | `asynccontextmanager` y `aclosing`: los pasos 3 y 5 del ejercicio 04 |
| [PEP 492](https://peps.python.org/pep-0492/), [PEP 525](https://peps.python.org/pep-0525/) y [PEP 654](https://peps.python.org/pep-0654/) (en inglés) | Por qué existen `async`/`await`, los generadores asíncronos y `ExceptionGroup` con `except*`. Lee la motivación de cada una |
| [What Color is Your Function?](https://journal.stuffwithstuff.com/2015/02/01/what-color-is-your-function/) (en inglés) | El artículo que bautizó el "color de las funciones" de la teoría 01 |
| [Notes on structured concurrency](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/) (en inglés) | La idea detrás de `TaskGroup`: por qué una tarea no debería poder escaparse de su bloque. Largo, pero cambia cómo piensas la concurrencia |
| [Reglas `ASYNC` de ruff](https://docs.astral.sh/ruff/rules/#flake8-async-async) (en inglés) | Todo lo que ruff detecta en código asíncrono: `time.sleep`, `open`, peticiones HTTP que bloquean... |
| [pytest-asyncio](https://pytest-asyncio.readthedocs.io/en/stable/) y [AnyIO: testing](https://anyio.readthedocs.io/en/stable/testing.html) (en inglés) | Los dos plugins para escribir tests `async def`, de la teoría 05, por si los necesitas más adelante |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Proyecto](../../3-proyecto/README.md) | **Webgrafía** | [Ebooks gratuitos](../ebooks-free/README.md) |
