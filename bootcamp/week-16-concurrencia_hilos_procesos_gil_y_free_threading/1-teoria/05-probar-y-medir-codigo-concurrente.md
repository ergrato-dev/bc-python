# 05 · Probar y medir código concurrente

⏱️ 45 min

## 🎯 Objetivos

- Medir tiempos de forma fiable: qué reloj usar, cuántas veces y qué número dar.
- Reconocer un test frágil (*flaky*) y por qué el código concurrente los produce.
- Probar el orden, la simultaneidad y el límite de trabajadores sin depender de la suerte.
- Saber qué llega a un proceso hijo en un test, y qué no.
- Comprobar que los tests concurrentes son estables y detectan bugs.

---

## 1. Medir bien

`time.perf_counter()` es el reloj para medir duraciones dentro de un programa. Para comparar dos versiones, tres reglas:

- **Repite**. La primera ejecución carga módulos, llena cachés del disco y despierta la CPU. Mide varias veces y da la **mediana**, que no se deja arrastrar por una ejecución rara.
- **Mide lo mismo**. Los mismos datos, la misma máquina, sin otro programa pesado a la vez.
- **Mide el programa entero** si eso es lo que va a notar quien lo usa. Desde la terminal, `time` incluye arrancar Python e importar las bibliotecas, y en tu proyecto eso es una parte fija de cada orden (paso 11).

Para fragmentos pequeños, `timeit` repite por ti:

```bash
uv run python -m timeit -s "from observatorio.core import parse_value" "parse_value('12,5')"
```

```
2000000 loops, best of 5: 151 nsec per loop
```

`-s` es la preparación, que no se mide. `timeit` elige cuántas repeticiones hacer y da la mejor de cinco series.

Y recuerda la teoría 01: compara `perf_counter` con `process_time`. Si el tiempo de CPU es mucho menor que el real, tu programa espera, y los hilos pueden ayudar. Si son iguales, calcula.

## 2. Tests frágiles

Un test **frágil** (*flaky*) unas veces pasa y otras falla, sin que cambie el código. Es peor que un test que falla siempre: enseña a todo el equipo a ignorar los fallos ("vuelve a lanzarlo, a veces falla").

El código concurrente los produce fácilmente, porque el orden en que se intercalan los hilos cambia en cada ejecución. Dos ejemplos de lo que **no** hay que hacer:

```python
def test_threads_are_faster() -> None:            # ❌ depende de la máquina
    start = time.perf_counter()
    report_files(paths, workers=4)
    assert time.perf_counter() - start < 0.6       # en un CI cargado, falla


def test_results_arrive() -> None:                # ❌ depende de la suerte
    results = []
    threading.Thread(target=lambda: results.append(1)).start()
    assert results == [1]                          # sin join, casi siempre pasa
```

El primero mide el **tiempo**: en una máquina lenta, o con el CI ocupado, falla. El segundo depende de que el hilo termine antes que la línea siguiente: casi siempre lo hace, y un día no.

La regla: un test de código concurrente comprueba un **resultado** que no depende de la velocidad (un orden, un número, un valor), y **espera** explícitamente lo que necesita (`join`, el `with` de un *pool*, una `Barrier`).

## 3. Técnicas para tu proyecto

`tests/test_batch.py` usa cuatro técnicas. Ninguna mide el tiempo.

### El orden, con tareas falsas que duermen

```python
def slow_report(path: Path) -> FileReport:
    time.sleep(0.05 * (3 - int(path.stem)))   # "0" duerme más que "2"
    return FileReport(path, int(path.stem))
```

Con `monkeypatch.setattr(batch, "report_file", slow_report)`, la primera tarea termina **la última**. Si `report_files` devolviera los resultados en orden de llegada, el test lo vería. Las esperas no son para medir nada: solo fuerzan un orden de llegada distinto del de entrada.

### La simultaneidad, con una `Barrier`

```python
barrier = threading.Barrier(3, timeout=5)

def meet(path: Path) -> FileReport:
    barrier.wait()      # se abre cuando hay 3 esperando
    return FileReport(path)
```

Si las tres tareas corren a la vez, la barrera se abre y el test pasa. Si fueran una detrás de otra, la primera esperaría a dos que no llegan, y a los 5 s el `timeout` lanzaría `BrokenBarrierError`. El test no depende de ningún tiempo cuando pasa; el `timeout` solo evita que, si falla, se quede colgado para siempre.

### El límite, con un contador protegido

```python
with lock:
    active += 1
    peak = max(peak, active)
time.sleep(0.05)
with lock:
    active -= 1
```

Cada tarea apunta cuántas hay a la vez, y `peak` guarda el máximo. Con `workers=2`, tiene que ser 2: ni 1 (no habría concurrencia), ni 6 (el *pool* ignoraría el límite). El contador lo modifican varios hilos, así que va protegido con un `Lock`. Sin él, el test tendría su propia carrera.

### Un espía en lugar del *pool* de procesos

```python
class SpyPool(ThreadPoolExecutor):
    def __init__(self, max_workers: int | None = None) -> None:
        created.append(max_workers)
        super().__init__(max_workers=max_workers)

monkeypatch.setattr(batch, "ProcessPoolExecutor", SpyPool)
```

¿Por qué no `monkeypatch.setattr(batch, "report_file", ...)` también con procesos? Porque con `forkserver` y `spawn` el hijo **importa `batch.py` desde cero**: tu sustitución vive en la memoria del proceso de pytest, y el hijo no la ve. Los procesos no comparten memoria, tampoco en un test.

Así que el código con procesos se prueba de dos formas: un espía que comprueba que se crea el *pool* adecuado con el número adecuado de trabajadores, y un test con archivos reales que compara el resultado con procesos y con hilos.

## 4. ¿Son estables? ¿Detectan bugs?

Un test concurrente que pasa una vez no demuestra mucho. Ejecútalo muchas veces:

```bash
for i in $(seq 20); do uv run pytest -q tests/test_batch.py | tail -1 | sed 's/ in .*//'; done | sort | uniq -c
```

```
     20 31 passed
```

`sed` quita el tiempo del final, que cambia en cada ejecución, y `uniq -c` cuenta las líneas iguales. Veinte veces la misma: estable. Una sola línea con `failed` es un test frágil, y hay que arreglarlo antes de seguir.

Y la pregunta de la semana 15: ¿detectarían un bug? Los mutantes del paso 13 del proyecto cambian justo lo que esta teoría protege: ignorar `workers`, usar hilos en lugar de procesos, cambiar el orden de los resultados. Cada uno debe matarlo al menos un test.

## 5. Y la semana que viene

Los hilos resuelven bien unas pocas decenas de esperas a la vez. Para **miles** (miles de peticiones HTTP, miles de conexiones), cada hilo cuesta memoria y cambios de turno. La semana 17 presenta `asyncio`: miles de tareas concurrentes en **un solo hilo**, que se ceden el turno explícitamente con `await` en cada espera. Y como hay un solo hilo, una carrera solo puede ocurrir en un `await`, que tienes a la vista en el código.

---

## ⚠️ Errores comunes

| Error | Causa | Solución |
|---|---|---|
| Un test pasa en tu máquina y falla en el CI | Compara tiempos, o depende de que un hilo llegue antes que otro | Comprueba resultados y espera explícitamente |
| Un test se queda colgado para siempre | Una `Barrier`, un `Event` o un `get()` sin `timeout` | Pon siempre `timeout` en las esperas de los tests |
| Tu sustitución con `monkeypatch` no tiene efecto con procesos | El hijo importa el módulo desde cero y no ve tu cambio | Prueba con hilos, o sustituye el *pool* por un espía |
| El contador de un test da números raros | Varios hilos lo modifican sin `Lock`: el test tiene su propia carrera | Protégelo con un `Lock` |
| Una medida dice que la versión nueva es más lenta, y la siguiente que más rápida | Una sola medida, con la máquina haciendo otras cosas | Repite y compara medianas |

---

## ✅ Qué debes saber al terminar

- [ ] Cómo medir bien: qué reloj, cuántas veces y qué número dar.
- [ ] Qué es un test frágil y por qué no se puede ignorar.
- [ ] Cómo probar el orden, la simultaneidad y el límite de trabajadores sin medir tiempos.
- [ ] Por qué `monkeypatch` no llega a un proceso hijo, y cómo se prueba el código con procesos.
- [ ] Cómo comprobar que un test concurrente es estable.
- [ ] Qué problema resuelve `asyncio`, que viene en la semana 17.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [04 · concurrent.futures](04-concurrent-futures.md) | **05 · Probar y medir código concurrente** | [Ejercicio 01 · Hilos](../2-practicas/ejercicio-01-hilos/README.md) |
