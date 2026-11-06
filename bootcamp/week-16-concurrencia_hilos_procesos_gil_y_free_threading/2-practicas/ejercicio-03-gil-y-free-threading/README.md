# Ejercicio 03 — El GIL y free-threading

⏱️ 1 h · Teoría previa: [03](../../1-teoria/03-el-gil-procesos-y-free-threading.md)

## Objetivo

Ejecutar el mismo programa en dos Pythons 3.14, uno con GIL y otro sin él, y comparar:

- saber qué Python estás usando y si tiene GIL;
- ver cómo los hilos que calculan pasan de no ganar nada a repartirse los núcleos;
- descubrir una condición de carrera que el GIL tenía escondida;
- comprobar que el `Lock` la arregla en los dos;
- probar los subintérpretes de Python 3.14, con un GIL para cada uno.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-16-concurrencia_hilos_procesos_gil_y_free_threading/2-practicas/ejercicio-03-gil-y-free-threading/starter
uv run python main.py
uv run --python 3.14.10t python main.py
```

```
Ejercicio 03 · El GIL y free-threading
Ejercicio 03 · El GIL y free-threading
```

La segunda orden tarda la primera vez: uv descarga **Python 3.14.10t**, la versión *free-threaded* (la `t` del final), y la guarda junto a las demás versiones que gestiona. Después, cada vez que cambias de un Python al otro, uv vuelve a crear el entorno `.venv` del ejercicio con el Python que pides. Este ejercicio no tiene dependencias y tarda menos de un segundo en hacerlo.

En cada paso, ejecuta las **dos** órdenes. Los tiempos de este README son de una máquina con 8 núcleos.

## Pasos

### 1. ¿Qué Python estás usando?

Descomenta el **PASO 1** y ejecuta las dos órdenes:

```
Python 3.14.10 · free-threaded: False
GIL activo: True
```

```
Python 3.14.10 · free-threaded: True
GIL activo: False
```

Son **dos compilaciones** del mismo Python 3.14.10. `Py_GIL_DISABLED` dice cómo se compiló: con GIL o sin él. `sys._is_gil_enabled()` dice si el GIL está activo **ahora**, que no siempre es lo mismo (paso 6). El guion bajo de `_is_gil_enabled` indica que es una función para diagnosticar, no para que tu programa cambie de comportamiento según su valor.

### 2. Hilos que calculan

Descomenta el **PASO 2** y ejecuta las dos órdenes:

```
1 hilo, 4 tareas: 1.74 s
4 hilos, 4 tareas: 1.88 s
```

```
1 hilo, 4 tareas: 1.26 s
4 hilos, 4 tareas: 0.39 s
```

Con GIL, lo mismo que en el ejercicio 02: los cuatro hilos se turnan y tardan lo que uno solo, o un poco más por los cambios de turno. Sin GIL, los cuatro calculan **a la vez** en cuatro núcleos: tres o cuatro veces menos.

El tiempo con un hilo también cambia entre las dos compilaciones, en un sentido o en otro, según cómo se compiló cada una. Lo que importa es la proporción entre una línea y la siguiente. En general, el Python *free-threaded* es algo más lento con un solo hilo: tiene que protegerse de hilos que podrían no existir.

### 3. Una carrera que el GIL esconde

Descomenta el **PASO 3** y ejecuta las dos órdenes, varias veces:

```
hits += 1 sin Lock: esperado 800000 · obtenido 800000
```

```
hits += 1 sin Lock: esperado 800000 · obtenido 218386
```

Con GIL, el resultado es correcto. Sin GIL, se pierden casi tres de cada cuatro sumas, y el número cambia cada vez.

`hits += 1` parece una sola operación, pero son tres: **leer** `hits`, **sumar** uno y **escribir** el resultado. Es la misma carrera del paso 5 del ejercicio 01, sin el `sleep(0)` que forzaba el cambio de turno. Con GIL, Python solo cambia de hilo en ciertos puntos del código, y en este bucle casi nunca cae entre la lectura y la escritura. Sin GIL, los hilos ejecutan **de verdad a la vez**, y se pisan constantemente.

El GIL no hacía tu programa correcto: hacía el fallo **raro**. Con GIL, en otro programa, en otra versión de Python o con otra carga, esta misma línea puede perder sumas. El código que comparte datos entre hilos necesita un `Lock`, tenga o no GIL el Python que lo ejecute.

### 4. El Lock, con GIL y sin él

Descomenta el **PASO 4** y ejecuta las dos órdenes:

```
hits += 1 con Lock: esperado 800000 · obtenido 800000 · 0.09 s
```

En las dos, 800000. El `Lock` funciona igual con GIL y sin él: solo un hilo a la vez ejecuta `hits += 1`.

Fíjate en el precio: con `Lock`, los cuatro hilos vuelven a avanzar de uno en uno, porque todo su trabajo está dentro del `with lock:`. Un `Lock` que protege el trabajo entero convierte el programa en secuencial otra vez. Por eso tu proyecto no comparte nada: cada tarea devuelve su `FileReport` y no toca ningún dato de las demás.

### 5. Subintérpretes, un GIL para cada uno

Descomenta el **PASO 5** y ejecuta las dos órdenes:

```
4 subintérpretes, 4 tareas: 0.81 s
```

```
4 subintérpretes, 4 tareas: 0.51 s
```

`InterpreterPoolExecutor` es nuevo en Python 3.14. Cada trabajador es un **subintérprete**: otro intérprete de Python dentro del mismo proceso, con su propia memoria y **su propio GIL**. Por eso calculan a la vez incluso con el Python normal.

Están a medio camino entre hilos y procesos. Arrancan más rápido que un proceso, pero, como en los procesos, las tareas y los resultados viajan con `pickle`, y no comparten variables. Todavía hay bibliotecas con extensiones en C que no funcionan en un subintérprete. Para tu proyecto, las dos opciones probadas siguen siendo hilos y procesos.

### 6. Volver a encender el GIL

Sin descomentar nada, ejecuta:

```bash
PYTHON_GIL=1 uv run --python 3.14.10t python main.py
```

```
Python 3.14.10 · free-threaded: True
GIL activo: True
1 hilo, 4 tareas: 1.29 s
4 hilos, 4 tareas: 1.29 s
hits += 1 sin Lock: esperado 800000 · obtenido 800000
...
```

El mismo Python sin GIL, con el GIL **encendido**: los hilos vuelven a turnarse y la carrera vuelve a esconderse. `PYTHON_GIL=1` (o `python -X gil=1`) sirve para comprobar si un problema se debe a la falta del GIL.

Python también lo enciende por su cuenta si importas una extensión en C que no declara que funciona sin GIL, y avisa con un `RuntimeWarning`. Las bibliotecas de tu proyecto (Pydantic, Rich, Typer) funcionan sin GIL: lo compruebas en el paso 10 del proyecto.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `error: No interpreter found for Python 3.14.10+freethreaded` y `Python downloads are set to 'never'` | Tienes desactivadas las descargas de uv: `uv python install 3.14.10t`, o quita `UV_PYTHON_DOWNLOADS=never` de tu entorno |
| `AttributeError: module 'sys' has no attribute '_is_gil_enabled'` | Usas un Python anterior al 3.13: revisa `uv run python --version` |
| `ImportError: cannot import name 'InterpreterPoolExecutor'` | Lo mismo con el 3.14: el paso 5 necesita Python 3.14 |
| El paso 3 da 800000 también sin GIL | Ejecútalo varias veces; si sigue, tu máquina tiene un solo núcleo disponible (`os.process_cpu_count()`) |
| `RuntimeWarning: The global interpreter lock (GIL) has been enabled to load module ...` | Una extensión en C no declara que funciona sin GIL: Python lo encendió. Busca una versión de la biblioteca con soporte *free-threaded* |
| Los tiempos no cambian entre los dos Pythons | Revisa el paso 1: si dice `GIL activo: True` en los dos, la segunda orden no usa 3.14.10t, o tienes `PYTHON_GIL=1` definida |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Procesos](../ejercicio-02-procesos/README.md) | **Ejercicio 03 · El GIL y free-threading** | [Ejercicio 04 · concurrent.futures](../ejercicio-04-concurrent-futures/README.md) |
