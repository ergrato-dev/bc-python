# Ejercicio 02 — Procesos

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-el-gil-procesos-y-free-threading.md) y [04](../../1-teoria/04-concurrent-futures.md)

## Objetivo

Repartir trabajo de CPU entre procesos y conocer sus reglas:

- comprobar que los hilos no aceleran un cálculo, y los procesos sí;
- entender por qué el código va dentro de `if __name__ == "__main__":`;
- ver qué no puede viajar a otro proceso y por qué;
- comprobar que cada proceso tiene su propia memoria;
- medir el coste de enviar muchas tareas pequeñas, y reducirlo con `chunksize`;
- saber cómo nace un proceso en tu sistema.

Tu proyecto tiene la opción `--procesos`. Aquí ves cuándo compensa y cuándo no. Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-16-concurrencia_hilos_procesos_gil_y_free_threading/2-practicas/ejercicio-02-procesos/starter
uv run python main.py
```

```
Ejercicio 02 · Procesos
```

Este `main.py` tiene una forma nueva. Cada paso es una función marcada con `@step`, que la apunta en la lista `STEPS`. Al final, **dentro** de `if __name__ == "__main__":`, un bucle las ejecuta en orden. El paso 4 explica por qué.

`count_primes(limit)` cuenta los primos menores que `limit` probando divisores. Es trabajo de **CPU puro**: no espera a nada, solo calcula. Los tiempos de este README son de una máquina con 8 núcleos. Los tuyos serán otros: compara las **proporciones**.

## Pasos

### 1. Trabajo de CPU, una tarea detrás de otra

Descomenta el **PASO 1** y ejecuta:

```
primos < 400 000: 33860
secuencial: 2.38 s
```

Cuatro tareas iguales, una detrás de otra: unos 0,6 s cada una. Es una tarea **limitada por CPU** (*CPU-bound*): lo que la frena es el cálculo.

### 2. Con 4 hilos

Descomenta el **PASO 2** y ejecuta:

```
4 hilos: 2.47 s
```

Lo mismo, o un poco más. En el ejercicio 01, cuatro hilos dividían el tiempo entre cuatro. Aquí no ganan nada. La diferencia es el **GIL**: en el Python normal, solo un hilo a la vez ejecuta código Python. Mientras un hilo **espera**, suelta el GIL y otro avanza. Mientras **calcula**, no lo suelta más que para turnarse. Cuatro hilos que calculan se turnan en un solo núcleo (teoría 03).

### 3. Con 4 procesos

Descomenta el **PASO 3** y ejecuta:

```
núcleos disponibles: 8
4 procesos: 1.02 s
```

Cada proceso es un intérprete de Python entero, con **su propio GIL**. Cuatro procesos calculan de verdad a la vez, en cuatro núcleos. `os.process_cpu_count()` dice cuántos núcleos puede usar tu programa.

¿Por qué no 0,6 s, la cuarta parte de 2,38? Porque arrancar los procesos cuesta, y enviarles el trabajo y recoger los resultados también. Con tareas de minutos, ese coste no se nota. Con tareas de milisegundos, puede ser mayor que el trabajo (paso 7).

### 4. Quién importa este archivo

Descomenta el **PASO 4**. Está fuera de cualquier función, a nivel de módulo. Ejecuta:

```
main.py cargado como __main__
Ejercicio 02 · Procesos
...
main.py cargado como __mp_main__
4 procesos: 1.02 s
```

La línea sale **dos veces**. Para ejecutar `count_primes` en otro proceso, ese proceso tiene que conocer la función, así que **importa `main.py`**. Lo importa con el nombre `__mp_main__`, no `__main__`. Por eso el bloque `if __name__ == "__main__":` del final se ejecuta solo en tu proceso, y los hijos solo definen funciones.

Sin ese guardián, cada hijo volvería a ejecutar los pasos, y crearía sus propios procesos, que importarían `main.py` y crearían los suyos... Python lo detecta: cada hijo se para con un `RuntimeError`, y tu proceso, con un `BrokenProcessPool`. **Regla**: el código que lanza procesos va siempre dentro de `if __name__ == "__main__":`. En tu proyecto ya lo está: el comando arranca desde `cli.py`, y nadie lo importa como `__main__`.

En Linux, desde Python 3.14, la línea sale **una vez** en los hijos aunque haya varios: el *forkserver* importa el archivo una sola vez y cada hijo nace como una copia suya (paso 8). En macOS y Windows sale una vez por cada hijo.

Vuelve a comentar el paso 4 antes de seguir: ensucia la salida.

### 5. Lo que no viaja a otro proceso

Descomenta el **PASO 5** y ejecuta:

```
PicklingError: Can't pickle local object <function not_picklable.<locals>.<lambda> at 0x7aedf9392a30>
```

Los procesos no comparten memoria. Para enviar una tarea, Python la convierte en bytes con `pickle` (la función, sus argumentos) y el otro proceso la reconstruye. Una función se envía **por su nombre**: `main.count_primes`, y el hijo la busca en su copia de `main.py`. Una `lambda` o una función definida dentro de otra no tienen un nombre que se pueda buscar, así que no pueden viajar.

Con hilos, el mismo código funciona: un hilo comparte la memoria y recibe la `lambda` tal cual. Con procesos, las funciones de las tareas van **a nivel de módulo**. Lo mismo vale para lo que devuelven: tu `FileReport` es una *dataclass* normal, y viaja sin problemas.

### 6. Memoria separada

Descomenta el **PASO 6** y ejecuta:

```
hilos: seen = [1, 2, 3]
procesos: seen = [] · hijos: 2 · ¿yo?: False
```

`remember` añade su número a la lista global `seen`. Con hilos, todos escriben en **la misma** lista: al final tiene los tres números. Con procesos, cada hijo añade el número a **su copia** de `seen`, y tu lista sigue vacía. Los procesos solo se comunican por lo que **devuelven**: aquí, su identificador de proceso (`os.getpid()`), que demuestra que eran dos procesos distintos del tuyo.

Es la ventaja de los procesos (ninguna carrera puede tocar tus datos) y su límite (para compartir algo, hay que enviarlo).

### 7. Muchas tareas pequeñas y `chunksize`

Descomenta el **PASO 7** y ejecuta. Tarda unos segundos:

```
20 000 tareas, secuencial: 0.28 s
20 000 tareas, procesos: 4.64 s
20 000 tareas, chunksize=500: 0.11 s
```

20 000 tareas diminutas. Con procesos, el programa tarda **16 veces más** que sin ellos: cada tarea viaja sola, ida y vuelta por `pickle`, y ese viaje cuesta mucho más que contar primos hasta 50.

`chunksize=500` envía las tareas en paquetes de 500: 40 viajes en lugar de 20 000. Ahora sí gana a la versión secuencial. Con `ThreadPoolExecutor`, `chunksize` no hace nada: los hilos no envían nada.

Esto es lo que verás en el proyecto con `--procesos`: resumir un archivo pequeño cuesta menos que enviarlo a otro proceso.

### 8. Cómo nace un proceso

Descomenta el **PASO 8** y ejecuta:

```
método de arranque: forkserver
disponibles: ['forkserver', 'fork', 'spawn']
```

Hay tres formas de crear un proceso de Python:

- **`spawn`**: arranca un intérprete nuevo, que importa tu archivo desde cero. Es la única en Windows y la de macOS. Es la más lenta.
- **`fork`**: copia el proceso actual tal como está. Es rápida, pero copia también los `Lock` que otro hilo tenía cogidos en ese momento, y el hijo se puede quedar bloqueado para siempre.
- **`forkserver`**: arranca un proceso limpio, sin hilos, y crea cada hijo como una copia de **ese**. Es la de Linux desde Python 3.14 (antes era `fork`).

Si en Windows o en macOS ves `spawn`, todo el ejercicio funciona igual. Los pasos 4 y 5 son la razón de que funcione en los tres sistemas.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| Un `RuntimeError` que empieza por `An attempt has been made to start a new process before the current process has finished its bootstrapping phase`, y después `BrokenProcessPool` | Lanzas procesos desde código a nivel de módulo: llévalo dentro de `if __name__ == "__main__":` |
| `AttributeError: module '__mp_main__' has no attribute 'remember'`, y después `BrokenProcessPool` | La función de la tarea solo existe en tu proceso: defínela a nivel de módulo, fuera de `if __name__` |
| `PicklingError: Can't pickle local object` | Una `lambda` o una función anidada no viaja: escribe una función a nivel de módulo |
| `BrokenProcessPool: A process in the process pool was terminated abruptly` sin otro error antes | Un hijo murió sin terminar su tarea (sin memoria, o un fallo de una biblioteca en C): reduce `max_workers` o el tamaño de las tareas |
| Con procesos tarda más que en secuencial | Normal si las tareas son pequeñas: usa `chunksize` o no uses procesos |
| En Jupyter o en la consola interactiva, `ProcessPoolExecutor` falla | Los hijos no pueden importar funciones definidas en una celda: escríbelas en un archivo `.py` e impórtalas |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Hilos](../ejercicio-01-hilos/README.md) | **Ejercicio 02 · Procesos** | [Ejercicio 03 · El GIL y free-threading](../ejercicio-03-gil-y-free-threading/README.md) |
