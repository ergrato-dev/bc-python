# Ejercicio 01 — Medir con `perf_counter` y `timeit`

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-medir-antes-de-optimizar.md)

## Objetivo

Medir bien antes de cambiar nada:

- ver que una sola medida baila de una ejecución a otra;
- repetir con `timeit.repeat` y quedarte con el **mínimo**;
- comprobar con números qué cambia al buscar en un `set` en lugar de en una lista;
- dejar que `timeit` elija cuántas vueltas dar;
- medir cómo **crece** el tiempo al doblar los datos;
- distinguir el tiempo de reloj del tiempo de CPU.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-22-rendimiento_profiling_cprofile_py_spy_y_vectorizacion/2-practicas/ejercicio-01-medir-con-timeit/starter
uv run python main.py
```

```
Ejercicio 01 · Medir
```

`LABELS` tiene 10 000 etiquetas y `WANTED`, 1 000 que buscar: la mitad están y la otra mitad no. `count_known` cuenta cuántas encuentra. Los tiempos de abajo son de un portátil con WSL2: los tuyos serán otros, pero el orden de magnitud y quién gana deben coincidir.

## Pasos

### 1. Una sola medida con `perf_counter`

Descomenta el **PASO 1** y ejecuta:

```
intento 1: 0.0450 s · 500 encontradas
intento 2: 0.0477 s · 500 encontradas
intento 3: 0.0444 s · 500 encontradas
```

Tres veces el mismo código con los mismos datos, y tres tiempos distintos. Mientras tu programa corre, el sistema atiende otros procesos, la CPU sube o baja de frecuencia y las cachés están más o menos calientes. Ese **ruido** es la razón de no fiarte nunca de una medida suelta.

### 2. Repetir y quedarse con el mínimo

Descomenta el **PASO 2** y ejecuta:

```
lista · mínimo 0.0445 s · mediana 0.0458 s
lista · máximo 0.0580 s
```

`timeit.repeat(función, number=5, repeat=7)` ejecuta la función 5 veces seguidas y mide el total; lo hace 7 veces y devuelve los 7 totales. Divides por 5 para tener el tiempo de una llamada.

El **mínimo** es la mejor estimación de lo que cuesta el código: el ruido solo puede **sumar** tiempo, nunca restarlo. La mediana te dice qué es lo normal; el máximo, cuánto ruido hubo.

### 3. La misma pregunta a un `set`

Descomenta el **PASO 3** y ejecuta:

```
set · mínimo 0.000024 s · 1871 veces más rápido
crear el set: 0.000103 s
```

`label in lista` compara con cada elemento hasta encontrarlo: **O(n)**, y las que no están obligan a recorrerla entera. `label in set` calcula un *hash* y va directo: **O(1)**. Con 10 000 etiquetas, unas 1 900 veces más rápido.

Crear el `set` cuesta algo (0,1 ms), y compensa en cuanto lo consultas más de un par de veces. Un cambio de **estructura de datos** como este gana más que cualquier truco: es lo primero que buscas cuando un perfil señala un `in` o un bucle anidado.

### 4. `timeit` elige cuántas vueltas

Descomenta el **PASO 4** y ejecuta:

```
join: 10000 vueltas en 0.35 s · 35 µs por vuelta
```

`Timer.autorange()` prueba 1, 2, 5, 10, 20... vueltas hasta que el total pasa de 0,2 s, y devuelve cuántas dio y cuánto tardaron. Así mides bien algo que dura microsegundos: una sola vuelta estaría por debajo de la resolución útil del reloj.

Desde la terminal, `python -m timeit` hace lo mismo y repite 5 veces:

```bash
uv run python -m timeit -s "labels = [str(n) for n in range(10_000)]" "'9999' in labels"
uv run python -m timeit -s "labels = {str(n) for n in range(10_000)}" "'9999' in labels"
```

```
5000 loops, best of 5: 77.2 usec per loop
20000000 loops, best of 5: 13.6 nsec per loop
```

`-s` es la preparación (*setup*): se ejecuta una vez y no cuenta. "best of 5" es el mínimo del paso 2.

### 5. Cómo crece con el tamaño

Descomenta el **PASO 5** y ejecuta:

```
n= 10000 · list.insert(0) 0.0071 s · deque.appendleft 0.0003 s
n= 20000 · list.insert(0) 0.0299 s · deque.appendleft 0.0006 s
n= 40000 · list.insert(0) 0.1125 s · deque.appendleft 0.0011 s
```

Mira cómo cambia cada columna al **doblar** n. `deque.appendleft` dobla su tiempo: es O(1) por elemento, O(n) en total. `list.insert(0)` lo multiplica por 4: cada inserción mueve todos los elementos que ya hay, O(n) por elemento, **O(n²)** en total.

Medir con dos o tres tamaños es la forma práctica de ver la complejidad de la semana 6 en tu código: si al doblar los datos el tiempo se cuadruplica, con 10 veces más datos tardará 100 veces más.

`partial(insert_front, n)` es la función `insert_front` con `n` ya puesto: `timeit` la llama sin argumentos.

### 6. Tiempo de reloj y tiempo de CPU

Descomenta el **PASO 6** y ejecuta:

```
reloj: 0.55 s · CPU: 0.06 s
```

`perf_counter` mide el tiempo **de reloj**: todo lo que pasa, también la espera de `sleep`. `process_time` mide solo el tiempo que la CPU trabajó para tu proceso. Si el reloj es mucho mayor que la CPU, tu programa **espera** (red, disco, `sleep`) y optimizar el cálculo no lo acelerará; si son parecidos, es **cálculo** y un perfil te dirá dónde.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| Tus tiempos son 2 o 3 veces los del README | Es normal: otra máquina. Compara las proporciones (cuántas veces más rápido, cómo crece), no los segundos |
| Un paso da tiempos muy distintos cada vez | Cierra lo que esté usando la CPU (el navegador con vídeo, una compilación) y mira el mínimo, no la media |
| `NameError: name 'per_call' is not defined` | El paso 3 usa el resultado del paso 2: descomenta los pasos en orden |
| El paso 5 tarda mucho | Con un portátil en ahorro de energía, conéctalo a la corriente; o quita el 40 000 de la tupla |
| `python -m timeit` dice `SyntaxError` | Las comillas: el código va entre comillas dobles y el texto de dentro entre simples |
| `CPU` es mayor que `reloj` | Varios hilos trabajando a la vez suman su CPU; aquí no debería pasar |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Vectorizar con NumPy](../../1-teoria/05-vectorizar-con-numpy.md) | **Ejercicio 01 · Medir** | [Ejercicio 02 · Perfilar con cProfile](../ejercicio-02-perfilar-con-cprofile/README.md) |
