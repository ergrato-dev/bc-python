# Ejercicio 04 — concurrent.futures

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-concurrent-futures.md)

## Objetivo

Manejar un *pool* de trabajadores con `concurrent.futures`, la herramienta de tu proyecto:

- enviar una tarea con `submit` y recoger su resultado de un `Future`;
- elegir entre `map` (el orden de entrada) y `as_completed` (el orden de llegada);
- tratar los errores que ocurren dentro de una tarea;
- no esperar para siempre: `timeout` y `wait`;
- cancelar tareas que aún no han empezado;
- avisar cuando termina una tarea, y saber qué hilo ejecuta el aviso;
- saber cuántos trabajadores crea un *pool* si no lo dices.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-16-concurrencia_hilos_procesos_gil_y_free_threading/2-practicas/ejercicio-04-concurrent-futures/starter
uv run python main.py
```

```
Ejercicio 04 · concurrent.futures
```

`read_station` simula una lectura: `Norte` tarda 0,3 s, `Sur` 0,1 s y `Oriente` 0,2 s, y `Centro` lanza un `KeyError`. Como las tareas solo duermen, el orden de la salida es el mismo en cualquier máquina.

## Pasos

### 1. `submit` y `Future`

Descomenta el **PASO 1** y ejecuta:

```
recién enviada: done=False · <Future at 0x78ed51d71550 state=running>
result(): Norte;30
después: done=True
```

`submit(función, argumentos)` envía una tarea al *pool* y devuelve **enseguida** un `Future`: un resguardo de un resultado que todavía no existe. Su estado pasa por `pending` (en la cola), `running` (un trabajador la ejecuta) y `finished`. `result()` espera a que termine y devuelve lo que devolvió la función.

`with ThreadPoolExecutor(...) as pool:` cierra el *pool* al salir del bloque, y **espera** a que terminen todas sus tareas. Sin `with`, tendrías que llamar a `pool.shutdown()` tú.

### 2. `map` frente a `as_completed`

Descomenta el **PASO 2** y ejecuta:

```
map: ['Norte;30', 'Sur;10', 'Oriente;20']
as_completed: ['Sur;10', 'Oriente;20', 'Norte;30']
```

Las tres tareas corren a la vez, y `Sur` es la primera en terminar.

- **`map`** devuelve los resultados en el **orden de entrada**. Si `Norte` tarda más, espera por él antes de dar `Sur`, aunque `Sur` ya esté listo. Es lo que usa tu proyecto: la tabla sale en el orden en que escribiste los archivos.
- **`as_completed`** da cada `Future` en cuanto **termina**. Sirve para mostrar progreso o para empezar a usar el primer resultado sin esperar al más lento.

Con `as_completed` pierdes el orden. Si lo necesitas, guarda junto a cada `Future` a qué entrada corresponde: es lo que hace el paso 3 con un diccionario.

### 3. Errores dentro de una tarea

Descomenta el **PASO 3** y ejecuta:

```
el error espera en el Future: KeyError('estación desconocida: Centro')
map: Sur;10
map se para en el primer error: 'estación desconocida: Centro'
as_completed sigue: Centro falló con 'estación desconocida: Centro'
as_completed: Sur;10
as_completed: Norte;30
```

Una excepción dentro de una tarea **no** tumba el programa en ese momento: se guarda en el `Future`. `exception()` la devuelve sin lanzarla, y `result()` la **vuelve a lanzar** en el hilo que lo llama, con su traza original.

Con `map`, la excepción salta al llegar a su resultado: das `Sur`, y el bucle se rompe en `Centro`. `Norte` se ejecuta igual, pero su resultado se pierde. Con `as_completed`, cada `result()` va en su propio `try`, y un fallo no impide recoger los demás.

En tu proyecto, `report_file` convierte el `DataFileError` en un `FileReport` con el error: un archivo que falta es un resultado más, y `map` nunca ve esa excepción. Cualquier otra excepción sí llega hasta `map` y se relanza: es un bug, y no debe esconderse.

### 4. No esperar para siempre

Descomenta el **PASO 4** y ejecuta:

```
a los 0.1 s aún no: running=True
la primera: ['Sur;10'] · pendientes: 2
```

`result(timeout=0.1)` espera como mucho 0,1 s y, si la tarea no ha terminado, lanza `TimeoutError`. La tarea **sigue en marcha**: el *timeout* es de tu espera, no de la tarea. Un hilo no se puede matar desde fuera, y el `with` del final esperará a que termine.

`wait(futures, return_when=FIRST_COMPLETED)` espera hasta que termine la primera y devuelve dos conjuntos: los `Future` terminados y los pendientes. Con `ALL_COMPLETED` (por defecto) espera a todas, y con `FIRST_EXCEPTION`, al primer error.

### 5. Cancelar lo que aún no empezó

Descomenta el **PASO 5** y ejecuta:

```
cancelar la primera: False · la segunda: True
canceladas: [False, True, True]
```

Con un solo trabajador, `Sur` empieza y las otras dos esperan en la cola. `cancel()` devuelve `False` con `Sur`: ya está en marcha, y no se puede parar. Con `Norte`, devuelve `True`: estaba en la cola y no llegará a ejecutarse.

`shutdown(cancel_futures=True)` cancela todo lo que sigue en la cola y espera a lo que ya está en marcha. Es lo que harías al pulsar Ctrl+C: no empezar nada nuevo y dejar terminar lo empezado.

### 6. Avisos al terminar

Descomenta el **PASO 6** y ejecuta:

```
terminó Sur;10 en lector_0
y el principal es MainThread
```

`add_done_callback(función)` llama a `función(future)` cuando la tarea termina. Fíjate en **quién** la llama: `lector_0`, el hilo del *pool* que ejecutó la tarea, no el principal. Si el aviso toca datos compartidos (un contador de progreso, una lista), estás otra vez ante una posible carrera, y necesitas un `Lock`.

`thread_name_prefix="lector"` pone nombre a los hilos del *pool*: `lector_0`, `lector_1`... Tu proyecto usa `observatorio`, y uno de sus tests lo comprueba.

### 7. ¿Cuántos trabajadores por defecto?

Descomenta el **PASO 7** y ejecuta:

```
núcleos: 8 · hilos por defecto: 12
min(32, núcleos + 4) = 12
```

Sin `max_workers`, un `ThreadPoolExecutor` crea hasta `min(32, núcleos + 4)` hilos: más que núcleos, porque se espera que casi todos estén esperando. Un `ProcessPoolExecutor` crea tantos procesos como núcleos: cada uno calcula, y más procesos que núcleos solo se turnarían.

`_max_workers`, con guion bajo, es un detalle interno: sirve para mirar, no para tu código. Tu proyecto fija `WORKERS = 4` y deja cambiarlo con `--trabajadores`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `RuntimeError: cannot schedule new futures after shutdown` | Llamas a `submit` fuera del `with`, o después de `shutdown()`: el *pool* ya está cerrado |
| El programa se queda colgado al final | Una tarea no termina nunca, y el `with` la espera: revisa sus bucles y sus esperas |
| `TimeoutError` y el programa tarda igual | Normal: el *timeout* deja de esperar, pero la tarea sigue; el `with` la espera al salir |
| `cancel()` devuelve siempre `False` | La tarea ya había empezado: solo se cancela lo que sigue en la cola |
| Una excepción de una tarea no aparece por ningún sitio | Nadie llamó a `result()` ni a `exception()` de ese `Future`: el error se queda guardado sin que lo veas |
| El aviso de `add_done_callback` no sale | El aviso lanzó una excepción: Python la registra con `logging` y sigue. Comprueba `future.result()` dentro de un `try` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · El GIL y free-threading](../ejercicio-03-gil-y-free-threading/README.md) | **Ejercicio 04 · concurrent.futures** | [Proyecto · Observatorio, capa 15](../../3-proyecto/README.md) |
