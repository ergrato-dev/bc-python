# Glosario — Semana 16

| Término | Definición |
|---|---|
| **Amdahl, ley de** | La aceleración máxima al repartir un programa es `1 / (parte secuencial)`: con un 20 % que no se puede repartir, como mucho 5 veces más rápido |
| **`as_completed`** | `as_completed(futures)`: da cada `Future` en cuanto termina, en orden de llegada y no de entrada |
| **`Barrier`** | `threading.Barrier(n)`: los hilos esperan en `wait()` hasta que llegan `n`. Sirve en los tests para comprobar que varias tareas corren a la vez |
| **`cancel`** | `future.cancel()`: cancela una tarea si aún no ha empezado, y devuelve si lo consiguió. Una tarea en marcha no se puede parar |
| **`chunksize`** | Argumento de `map` con procesos: envía las entradas en paquetes de ese tamaño para reducir el coste de enviarlas una a una |
| **Concurrencia** | Tener varias tareas en marcha a la vez, aunque en cada instante solo avance una. Aprovecha las esperas |
| **Condición de carrera** | Fallo en el que el resultado depende del orden en que se intercalan los hilos, por ejemplo dos `+= 1` que leen el mismo valor. Cambia en cada ejecución |
| **Contador de referencias** | Cuántas variables usan un objeto de Python. Al llegar a cero, se borra. El GIL existe para que dos hilos no lo cambien a la vez |
| **CPU-bound** | Limitado por CPU: el programa pasa casi todo el tiempo calculando. En Python con GIL, se acelera con procesos |
| **`Event`** | `threading.Event()`: una señal; un hilo hace `set()` y los que esperan en `wait()` siguen |
| **`Executor`** | La interfaz de `concurrent.futures`: `submit`, `map` y `shutdown`. La cumplen `ThreadPoolExecutor`, `ProcessPoolExecutor` e `InterpreterPoolExecutor` |
| **`fork`** | Método de arranque que copia el proceso actual tal como está. Rápido, pero puede heredar cerrojos cogidos por otros hilos. Ya no es el de Linux en 3.14 |
| **`forkserver`** | Método de arranque que crea cada hijo como copia de un proceso limpio y sin hilos. El de Linux desde Python 3.14 |
| **Free-threading** | La compilación de CPython sin GIL, compatible oficialmente desde 3.14. Sus versiones llevan una `t`: `3.14.10t` |
| **`Future`** | El resguardo de una tarea enviada a un *pool*: `result()`, `exception()`, `done()`, `cancel()` |
| **GIL** | *Global Interpreter Lock*: cerrojo de CPython que deja ejecutar código Python a un solo hilo cada vez. Se suelta al esperar E/S |
| **Guardián `__main__`** | `if __name__ == "__main__":`. El código que lanza procesos va dentro, porque los hijos importan el archivo como `__mp_main__` |
| **Hilo** | *Thread*: un flujo de ejecución dentro de un proceso. Los hilos de un proceso comparten su memoria |
| **I/O-bound** | Limitado por E/S: el programa pasa casi todo el tiempo esperando a la red, al disco o a otro programa. Se acelera con hilos o `asyncio` |
| **Interbloqueo** | *Deadlock*: dos hilos se esperan mutuamente, cada uno con un cerrojo que el otro necesita. El programa se queda colgado sin error |
| **`InterpreterPoolExecutor`** | *Pool* de Python 3.14 cuyos trabajadores son subintérpretes, cada uno con su GIL |
| **`join`** | `thread.join()`: espera a que un hilo termine |
| **`Lock`** | `threading.Lock()`: cerrojo que deja pasar a un solo hilo a la vez por un bloque `with lock:` |
| **`map` (de un *pool*)** | `pool.map(función, entradas)`: una tarea por entrada, con los resultados en el orden de las entradas |
| **`max_workers`** | Cuántos trabajadores tiene un *pool*. Por defecto, `min(32, núcleos + 4)` hilos o tantos procesos como núcleos |
| **Paralelismo** | Ejecutar varias tareas en el mismo instante, en varios núcleos. Solo ayuda si hay cálculo que repartir |
| **`pickle`** | Convierte objetos de Python en bytes y al revés. Es como viajan las tareas y los resultados entre procesos |
| **`PicklingError`** | El error al enviar a otro proceso algo que no se puede convertir en bytes, como una `lambda` o una función anidada |
| ***Pool*** | Grupo de trabajadores (hilos, procesos o subintérpretes) que se crean una vez y ejecutan muchas tareas |
| **Proceso** | Un programa en ejecución, con su propia memoria. Un proceso no puede leer la memoria de otro |
| **`process_cpu_count`** | `os.process_cpu_count()`: cuántos núcleos puede usar tu programa. En un contenedor pueden ser menos que los de la máquina |
| **`process_time`** | `time.process_time()`: tiempo de CPU que ha usado tu proceso. Comparado con `perf_counter`, dice si el programa calcula o espera |
| **`PYTHON_GIL`** | Variable de entorno del Python sin GIL: `PYTHON_GIL=1` vuelve a encender el GIL, y `PYTHON_GIL=0` lo mantiene apagado |
| **`Queue`** | `queue.Queue()`: cola segura entre hilos. `put` añade y `get` espera hasta que haya algo |
| **`Semaphore`** | `threading.Semaphore(n)`: como un `Lock`, pero deja pasar a `n` hilos a la vez |
| **`spawn`** | Método de arranque que crea un Python nuevo, que importa tu archivo desde cero. El de Windows y macOS |
| **Subintérprete** | Otro intérprete de Python dentro del mismo proceso, con su memoria y su GIL. Módulo `concurrent.interpreters` (3.14) |
| **`submit`** | `pool.submit(función, *args)`: envía una tarea y devuelve enseguida su `Future` |
| **Test frágil** | *Flaky test*: un test que unas veces pasa y otras falla sin que cambie el código. Típico al comprobar tiempos o depender del orden de los hilos |
| **`thread_name_prefix`** | Argumento de `ThreadPoolExecutor` que da nombre a sus hilos: `observatorio_0`, `observatorio_1`... |
| **`ThreadPoolExecutor`** | *Pool* de hilos de `concurrent.futures`. El de `report_files` por defecto |
| **`timeit`** | Módulo para medir fragmentos pequeños de código repitiéndolos muchas veces: `python -m timeit "..."` |

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
