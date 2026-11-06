# Ejercicio 01 — Hilos

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-concurrencia-y-paralelismo.md) y [02](../../1-teoria/02-hilos-carreras-y-locks.md)

## Objetivo

Trabajar con hilos de `threading`, de la mano:

- esperar cuatro cosas a la vez en lugar de una detrás de otra;
- arrancar hilos con `start` y esperarlos con `join`;
- recoger lo que calcula cada hilo sin pisarse;
- provocar una **condición de carrera** y arreglarla con un `Lock`;
- repartir tareas con una `Queue`.

Tu proyecto usa un `ThreadPoolExecutor`, que hace todo esto por ti. Aquí ves qué hay debajo. Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-16-concurrencia_hilos_procesos_gil_y_free_threading/2-practicas/ejercicio-01-hilos/starter
uv run python main.py
```

```
Ejercicio 01 · Hilos
```

`download` simula una lectura lenta con `time.sleep(0.5)`: el programa espera medio segundo sin usar la CPU, como cuando espera a la red o al disco. Cada paso añade salida debajo de la anterior. Los tiempos de tu máquina pueden variar en el segundo decimal.

## Pasos

### 1. Una detrás de otra

Descomenta el **PASO 1** y ejecuta:

```
secuencial: 2.0 s · Norte;17.5
```

Cuatro descargas de 0,5 s, una detrás de otra: 2 s. Durante casi todo ese tiempo el programa no hace nada, solo espera. Es una tarea **limitada por E/S** (*I/O-bound*): lo que la frena es la espera, no el cálculo.

`time.perf_counter()` es el reloj para medir duraciones: no salta si cambia la hora del sistema, y tiene más resolución que `time.time()`.

### 2. Un hilo por descarga

Descomenta el **PASO 2** y ejecuta:

```
hilos vivos: 5
4 hilos: 0.5 s · vivos al final: 1
```

`Thread(target=download, args=(station,))` prepara un hilo que ejecutará `download(station)`. `start()` lo arranca y vuelve **enseguida**: el hilo principal sigue con la línea siguiente mientras el nuevo hilo duerme. Por eso `active_count()` dice 5: los cuatro nuevos y el principal.

`join()` espera a que un hilo termine. Las cuatro esperas se solapan y el total es 0,5 s, no 2. Mientras un hilo duerme, el GIL queda libre y otro hilo puede avanzar (teoría 03).

Fíjate en que `args` es una **tupla**: `(station,)`, con la coma. Sin ella, `("Norte")` es solo el texto `"Norte"`, y el hilo llamaría a `download("N", "o", "r", "t", "e")`.

### 3. Sin `join`, nadie espera

Descomenta el **PASO 3** y ejecuta:

```
el hilo principal sigue sin esperar
[lento] terminé
después de join: el hilo ya terminó
```

El hilo `lento` duerme 0,2 s antes de escribir, y el principal no lo espera: su línea sale primero. Con `join`, el principal se para hasta que `lento` termina. Sin `join`, tu programa seguiría como si el trabajo estuviera hecho, y leería resultados que aún no existen.

`name="lento"` da nombre al hilo. Si no se lo das, se llama `Thread-1`, `Thread-2`... Nombrar los hilos ayuda a leer los registros de `logging`, que pueden incluir `%(threadName)s`.

### 4. Los resultados de cada hilo

Descomenta el **PASO 4** y ejecuta:

```
resultados: ['Norte;17.5', 'Sur;10.5', 'Oriente;24.5', 'Occidente;31.5']
```

Un hilo **no devuelve** nada: `Thread` ignora lo que retorna su función. Para recoger resultados, cada hilo escribe en su **propia casilla** de una lista preparada antes. Dos hilos nunca escriben en la misma casilla, así que no se pisan, y el orden de la lista es el de las estaciones aunque terminen en otro orden.

Es exactamente lo que hace `ThreadPoolExecutor.map` por dentro, y la razón de que lo uses en el proyecto en lugar de escribir esto a mano.

### 5. Una condición de carrera

Descomenta el **PASO 5** y ejecuta varias veces:

```
sin Lock: esperado 400 · obtenido 104
```

Cuatro hilos suman 100 cada uno: deberían ser 400. Obtienes mucho menos, y **un número distinto cada vez**. `add` lee el valor, se detiene y escribe el valor leído más uno. Si dos hilos leen el mismo 7, los dos escriben 8: una suma se pierde.

El `time.sleep(0)` cede el turno a otro hilo a propósito, justo en el peor momento, para que lo veas en cada ejecución. Sin él, el fallo también existe, pero aparece muy de vez en cuando: en producción, un martes, sin que puedas repetirlo. Eso es una **condición de carrera**: el resultado depende de cómo se intercalen los hilos.

### 6. El Lock

Descomenta el **PASO 6** y ejecuta:

```
con Lock: esperado 400 · obtenido 400
```

`with self.lock:` deja entrar a **un solo hilo** en el bloque. Los demás esperan en la puerta hasta que sale. Leer y escribir quedan juntos, sin que nadie se cuele en medio, y el resultado es siempre 400.

Un `Lock` tiene un precio: mientras un hilo está dentro, los demás no avanzan. Protege solo lo imprescindible (la lectura y la escritura), no el trabajo lento. En el proyecto no hace falta ninguno, porque ninguna tarea toca nada compartido.

### 7. Productor y consumidores con `Queue`

Descomenta el **PASO 7** y ejecuta:

```
procesadas: ['Norte;17.5', 'Occidente;31.5', 'Oriente;24.5', 'Sur;10.5']
```

Una `Queue` es una cola segura entre hilos: lleva su propio `Lock` por dentro. El hilo principal **produce** tareas con `put`, y dos hilos **consumen** con `get`, que espera hasta que haya algo. Para que los consumidores terminen, el productor pone un `None` por cada uno: la señal de parar.

La salida va ordenada con `sorted`: qué consumidor coge cada tarea y en qué orden termina cambia en cada ejecución. Quita el `sorted` y ejecuta varias veces para verlo.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `TypeError: download() takes 1 positional argument but 5 were given` | Falta la coma en `args=(station,)`: sin ella, el texto se reparte letra a letra |
| `RuntimeError: threads can only be started once` | Llamas a `start()` dos veces sobre el mismo hilo: crea uno nuevo |
| El programa no termina | Un consumidor espera en `get()` una tarea que no llega: falta un `None` por consumidor |
| El paso 2 tarda 2 s en lugar de 0,5 | Haces `join()` dentro del mismo bucle que `start()`: arrancas uno, lo esperas y arrancas el siguiente |
| El paso 5 da 400 | Revisa que `time.sleep(0)` esté entre la lectura y la escritura, no después |
| Las líneas de los hilos salen mezcladas | Varios hilos escriben a la vez: es normal. Para que no pase, cada hilo devuelve su texto y lo escribe el principal |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Probar y medir código concurrente](../../1-teoria/05-probar-y-medir-codigo-concurrente.md) | **Ejercicio 01 · Hilos** | [Ejercicio 02 · Procesos](../ejercicio-02-procesos/README.md) |
