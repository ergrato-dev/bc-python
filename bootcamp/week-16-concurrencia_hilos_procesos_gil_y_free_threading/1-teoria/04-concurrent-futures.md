# 04 · concurrent.futures

⏱️ 50 min

## 🎯 Objetivos

- Usar un `Executor` con `with`, y saber qué hace al cerrarse.
- Enviar tareas con `submit` y recoger sus resultados de un `Future`.
- Elegir entre `map` y `as_completed` según necesites el orden o la rapidez.
- Tratar los errores de las tareas, poner límites de espera y cancelar.
- Elegir cuántos trabajadores usar.
- Escribir código que funcione igual con hilos y con procesos.

---

## 1. `Executor`

`concurrent.futures` tiene una interfaz, `Executor`, y tres implementaciones:

| Clase | Trabajadores |
|---|---|
| `ThreadPoolExecutor` | Hilos del mismo proceso |
| `ProcessPoolExecutor` | Procesos hijos |
| `InterpreterPoolExecutor` | Subintérpretes (Python 3.14) |

Un `Executor` es un *pool*: un grupo de trabajadores que se crean una vez y se reutilizan para muchas tareas. Crear un hilo o un proceso por tarea sería mucho más caro.

```python
with ThreadPoolExecutor(max_workers=4) as pool:
    ...   # enviar tareas
# aquí, todas las tareas han terminado y los trabajadores se han cerrado
```

Al salir del `with`, el *pool* llama a `shutdown(wait=True)`: **espera** a que terminen todas las tareas y cierra los trabajadores. También si sale por una excepción. Es el mismo patrón de los archivos de la semana 7: el `with` garantiza que se libera lo que se abrió.

## 2. `submit` y `Future`

```python
with ThreadPoolExecutor(max_workers=4) as pool:
    future = pool.submit(report_file, Path("medidas.csv"))
    ...                        # el hilo principal sigue
    report = future.result()   # espera al resultado
```

`submit(función, *args, **kwargs)` pone la tarea en la cola y devuelve **enseguida** un `Future`: el resguardo de un resultado que todavía no existe.

| Método | Qué hace |
|---|---|
| `result(timeout=None)` | Espera y devuelve el resultado, o **relanza** la excepción de la tarea |
| `exception(timeout=None)` | Espera y devuelve la excepción, o `None`, sin lanzarla |
| `done()` | `True` si terminó: bien, con error o cancelada |
| `running()` | `True` si un trabajador la está ejecutando ahora |
| `cancel()` | La cancela si aún no empezó, y devuelve si lo consiguió |
| `add_done_callback(f)` | Llama a `f(future)` al terminar, desde el hilo que la terminó |

## 3. `map`: el orden de entrada

```python
with ThreadPoolExecutor(max_workers=4) as pool:
    reports = list(pool.map(report_file, paths))
```

`pool.map(función, entradas)` envía una tarea por entrada y devuelve sus resultados **en el orden de las entradas**, como el `map` de siempre. Si la primera tarea es la más lenta, `map` espera por ella antes de dar las demás, aunque ya estén listas.

Tres detalles:

- **Envía todas las tareas al llamarlo**, pero da los resultados **perezosamente**, uno a uno, al recorrerlo. `list(...)` los recoge todos.
- **`buffersize=`** (nuevo en Python 3.14): envía solo unas pocas tareas por delante y las demás a medida que recorres. Ahorra memoria con millones de entradas, pero entonces hay que recorrer **dentro** del `with`: fuera, el *pool* ya está cerrado y no acepta tareas nuevas.
- **`timeout=`**: si el total supera ese tiempo, el recorrido lanza `TimeoutError`.
- **`chunksize=`**: con procesos, envía las entradas en paquetes de ese tamaño. Con miles de tareas pequeñas, reduce mucho el coste de enviarlas (ejercicio 02, paso 7). Con hilos no hace nada.

Tu proyecto usa `map` porque la tabla de `lote` tiene que salir en el orden en que escribiste los archivos.

## 4. `as_completed` y `wait`: el orden de llegada

```python
futures = {pool.submit(report_file, path): path for path in paths}
for future in as_completed(futures):
    path = futures[future]
    print(f"{path}: {future.result()}")
```

`as_completed(futures)` da cada `Future` en cuanto **termina**, en el orden en que van terminando. Sirve para enseñar progreso, o para empezar a usar los primeros resultados sin esperar al más lento. Como pierdes el orden, un diccionario `Future → entrada` te dice a qué corresponde cada uno.

`wait(futures, return_when=...)` espera y devuelve dos conjuntos, `(terminados, pendientes)`:

| `return_when` | Vuelve cuando... |
|---|---|
| `ALL_COMPLETED` (por defecto) | han terminado todas |
| `FIRST_COMPLETED` | ha terminado la primera |
| `FIRST_EXCEPTION` | una ha fallado, o han terminado todas |

## 5. Errores

Una excepción dentro de una tarea no tumba el programa en ese momento: se **guarda en el `Future`**, y salta cuando alguien pide el resultado.

- **`future.result()`** la relanza, con la traza original de la tarea.
- **`map`** la relanza al llegar a ese resultado en el recorrido: los resultados siguientes se pierden, aunque sus tareas se ejecuten.
- **`as_completed`** te deja poner cada `result()` en su `try`, y seguir con los demás.

Si nadie pide el resultado, la excepción **se pierde** sin que nadie la vea. Es un error frecuente con `submit`: enviar tareas y no mirar sus `Future`.

Tu proyecto separa dos tipos de error:

```python
def report_file(path: Path) -> FileReport:
    try:
        lines = open_file(path).lines()
    except DataFileError as problem:
        return FileReport(path, error=str(problem))   # un error esperado: es un resultado
    ...
```

Un archivo que no existe es **un dato más** del lote, y vuelve como un `FileReport` con su error. Cualquier otra excepción es un bug: `report_file` no la captura, `map` la relanza en el hilo principal, y el programa falla con su traza. Esconderla como "archivo con error" haría el bug invisible.

## 6. Esperar con límite y cancelar

```python
try:
    report = future.result(timeout=2)
except TimeoutError:
    ...   # la tarea sigue en marcha: lo que se acabó es tu espera
```

`timeout` limita **tu espera**, no la tarea. Un hilo no se puede matar desde fuera: seguirá hasta terminar, y el `with` lo esperará al salir. Si una tarea puede quedarse colgada (una conexión que no responde), el límite tiene que estar **dentro** de la tarea, por ejemplo en el *timeout* del cliente HTTP (semana 18).

`future.cancel()` solo cancela tareas que **aún no han empezado**. `pool.shutdown(cancel_futures=True)` cancela todas las de la cola y espera a las que ya están en marcha.

## 7. ¿Cuántos trabajadores?

| *Pool* | Por defecto | Por qué |
|---|---|---|
| `ThreadPoolExecutor` | `min(32, núcleos + 4)` | Se espera que casi todos estén esperando E/S |
| `ProcessPoolExecutor` | Tantos como núcleos | Cada uno calcula; más se turnarían |

`núcleos` es `os.process_cpu_count()`: los que puede usar tu programa, que en un contenedor pueden ser menos que los de la máquina.

Para E/S, el número adecuado depende de **a quién** esperas. Un servidor que aguanta 4 conexiones a la vez no irá más rápido con 32 hilos: irá peor. Para CPU, más trabajadores que núcleos solo añade turnos. Por eso tu proyecto fija `WORKERS = 4` y deja cambiarlo con `--trabajadores`: el valor bueno depende de dónde están los archivos, y se encuentra midiendo.

## 8. Hilos o procesos con el mismo código

```python
def report_files(
    paths: Iterable[Path], *, workers: int = 4, processes: bool = False
) -> list[FileReport]:
    pool: Executor
    if processes:
        pool = ProcessPoolExecutor(max_workers=workers)
    else:
        pool = ThreadPoolExecutor(max_workers=workers, thread_name_prefix="observatorio")
    with pool:
        return list(pool.map(report_file, paths))
```

Los dos *pools* cumplen la interfaz `Executor`, así que el resto del código no sabe cuál tiene. Es el polimorfismo de la semana 10: `pool: Executor` es a los *pools* lo que `source: Source` era a las fuentes de datos.

Para que funcione con los dos, la tarea tiene que cumplir las reglas **más estrictas**, las de los procesos: función a nivel de módulo, argumentos y resultado que viajen con `pickle`, y nada compartido. Si funciona con procesos, funciona con hilos.

---

## ⚠️ Errores comunes

| Error | Causa | Solución |
|---|---|---|
| `RuntimeError: cannot schedule new futures after shutdown` | `submit` o `map` fuera del `with`, o después de `shutdown()` | Envía y recoge las tareas dentro del `with` |
| `RuntimeError: cannot schedule new futures after shutdown` al recorrer `map` | Usas `buffersize=` y recorres después del `with` | `return list(pool.map(...))` dentro del `with` |
| Una tarea falla y nadie se entera | Nadie pidió su `result()` | Recorre los `Future` y pide su resultado o su excepción |
| Con `as_completed` no sabes a qué entrada corresponde un resultado | El orden de llegada no es el de entrada | Un diccionario `Future → entrada` |
| El *timeout* no para la tarea | `timeout` limita tu espera, no la tarea | Pon el límite dentro de la tarea |
| `pool: ProcessPoolExecutor` y mypy rechaza el `ThreadPoolExecutor` | mypy deduce el tipo de la primera asignación | Anota la variable con `Executor` |

---

## ✅ Qué debes saber al terminar

- [ ] Qué hace el `with` de un `Executor` al salir.
- [ ] Qué es un `Future` y qué hacen `result`, `exception`, `done` y `cancel`.
- [ ] La diferencia entre `map` y `as_completed`, y por qué tu proyecto usa `map`.
- [ ] Dónde salta una excepción de una tarea, y cuándo se pierde.
- [ ] Qué limita un `timeout` y qué no.
- [ ] Cuántos trabajadores crea cada *pool* por defecto, y por qué.
- [ ] Qué reglas cumple una tarea que funciona con hilos y con procesos.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [03 · El GIL, procesos y free-threading](03-el-gil-procesos-y-free-threading.md) | **04 · concurrent.futures** | [05 · Probar y medir código concurrente](05-probar-y-medir-codigo-concurrente.md) |
