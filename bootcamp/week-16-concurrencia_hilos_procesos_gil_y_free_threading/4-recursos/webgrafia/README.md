# Webgrafía — Semana 16

| Recurso | Para qué |
|---|---|
| [`concurrent.futures`](https://docs.python.org/es/3.14/library/concurrent.futures.html) (en español) | `Executor`, `submit`, `map`, `as_completed`, `wait` y los tres *pools*, con ejemplos. La teoría 04 |
| [`threading`](https://docs.python.org/es/3.14/library/threading.html) (en español) | `Thread`, `Lock`, `RLock`, `Event`, `Barrier` y `Semaphore`: la teoría 02 y el ejercicio 01 |
| [`queue`](https://docs.python.org/es/3.14/library/queue.html) (en español) | La cola segura entre hilos del paso 7 del ejercicio 01, con su ejemplo de productor y consumidores |
| [`multiprocessing`](https://docs.python.org/es/3.14/library/multiprocessing.html) (en español) | Lee "Contextos y métodos de inicio" y "Pautas de programación": `spawn`, `fork`, `forkserver` y el guardián `__main__` |
| [`concurrent.interpreters`](https://docs.python.org/es/3.14/library/concurrent.interpreters.html) (en español) | Los subintérpretes de Python 3.14, que usa `InterpreterPoolExecutor` (ejercicio 03, paso 5) |
| [Python support for free threading](https://docs.python.org/3.14/howto/free-threading-python.html) (en inglés) | La guía oficial del Python sin GIL: cómo instalarlo, cómo saber si el GIL está activo, qué es seguro y cuánto cuesta |
| [Novedades de Python 3.14](https://docs.python.org/3.14/whatsnew/3.14.html) (en inglés) | Busca "free-threaded", "forkserver" e "InterpreterPoolExecutor": los tres cambios de 3.14 que usas esta semana |
| [PEP 703](https://peps.python.org/pep-0703/) y [PEP 779](https://peps.python.org/pep-0779/) (en inglés) | Por qué y cómo se quitó el GIL, y los criterios para declararlo compatible en 3.14. Lee la motivación de la 703 |
| [PEP 734](https://peps.python.org/pep-0734/) (en inglés) | Los subintérpretes en la biblioteca estándar: qué son y para qué sirven |
| [Python free-threading guide](https://py-free-threading.github.io/) (en inglés) | La guía de la comunidad para usar y portar código al Python sin GIL, y su [lista de bibliotecas compatibles](https://py-free-threading.github.io/tracking/) |
| [uv: versiones de Python](https://docs.astral.sh/uv/concepts/python-versions/) (en inglés) | Cómo pide e instala uv un Python concreto, incluido el *free-threaded*: el `3.14.10t` del ejercicio 03 |
| [`timeit`](https://docs.python.org/es/3.14/library/timeit.html) (en español) | Medir fragmentos pequeños desde la terminal o desde Python, sin errores de medida comunes: la teoría 05 |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Proyecto](../../3-proyecto/README.md) | **Webgrafía** | [Ebooks gratuitos](../ebooks-free/README.md) |
