# Ejercicio 01 — Contar pasos y medir

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-algoritmos-y-big-o.md)

## Objetivo

Ver con tus ojos cómo crece el trabajo de un algoritmo cuando crece la entrada: primero contando pasos, que no depende de tu máquina, y después midiendo tiempos con `perf_counter` y `timeit`. Ejercicio **guiado**: descomentas cada paso de `big_o_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-06-algoritmos_big_o_collections_e_itertools/2-practicas/ejercicio-01-contar-pasos-y-medir/starter
uv run python big_o_lab.py
```

```
Ejercicio 01 · Contar pasos y medir
```

Desde el paso 2, los tiempos de tu máquina serán **otros**. No compares los números con los del README: compara cómo cambian de una fila a la siguiente.

## Pasos

### 1. Contar pasos

Descomenta el **PASO 1** y ejecuta:

```
n=   10 | buscar el último:     10 | todas las parejas:      45
n=  100 | buscar el último:    100 | todas las parejas:    4950
n= 1000 | buscar el último:   1000 | todas las parejas:  499500
```

Buscar el último elemento mira los `n`: con el doble de datos, el doble de pasos. Eso es **O(n)**, lineal. Comparar todas las parejas hace `n × (n − 1) / 2` pasos: con 10 veces más datos, unas 100 veces más pasos. Eso es **O(n²)**, cuadrático. Cambia `[10, 100, 1_000]` por `[10, 100, 1_000, 10_000]`: la última fila tarda varios segundos en salir, y son casi 50 millones de pasos. Deshaz el cambio.

### 2. Medir con `perf_counter`

Descomenta el **PASO 2**:

```
sum de    100,000 números:    0.36 ms
sum de  1,000,000 números:    4.97 ms
sum de 10,000,000 números:   38.63 ms
```

`sum` mira cada número una vez: O(n). Cada fila tiene 10 veces más números y tarda unas 10 veces más. Ejecuta el programa dos o tres veces: los milisegundos cambian, porque tu máquina hace otras cosas a la vez. Por eso una sola medida no basta, y por eso existe `timeit`.

### 3. Lista frente a set con `timeit`

Descomenta el **PASO 3**:

```
n=  1,000 | lista:     6.81 ms | set:  0.020 ms
n= 10,000 | lista:    64.96 ms | set:  0.020 ms
n=100,000 | lista:   632.48 ms | set:  0.021 ms
```

Es la promesa del ejercicio 04 de la semana 5: `in` en una lista es **O(n)**, recorre hasta encontrarlo; en un set es **O(1)**, va directo al sitio por el hash. La columna de la lista crece por 10 en cada fila; la del set no se mueve. `timeit` repite la instrucción 1 000 veces y devuelve el total: así el ruido de una ejecución suelta pesa menos. `globals=globals()` le deja ver los nombres del programa; prueba a quitarlo:

```
NameError: name 'target' is not defined
```

Deshaz el cambio.

### 4. El mismo problema, dos órdenes

Descomenta el **PASO 4**:

```
n=1,000 | O(n²):     12.0 ms | O(n):  0.056 ms
n=2,000 | O(n²):     48.7 ms | O(n):  0.085 ms
n=4,000 | O(n²):    174.0 ms | O(n):  0.113 ms
```

Las dos funciones responden lo mismo: ¿hay algún repetido? La lenta compara cada pareja: al doblar `n`, el tiempo se multiplica por unos 4. La rápida recuerda lo que ya vio en un set: al doblar `n`, el tiempo crece mucho menos, y con tamaños tan pequeños lo que pesa es arrancar la función. La lista no tiene repetidos a propósito: es el **peor caso**, en el que ninguna de las dos puede parar antes. Cambia `values = list(range(n))` por `values = [0] + list(range(n))`: las dos encuentran el repetido enseguida. Deshaz el cambio.

### 5. Cómo crece cada orden

Descomenta el **PASO 5**:

```
         n  log n      n log n                 n²
        10      3           33                100
     1,000     10        9,966          1,000,000
 1,000,000     20   19,931,569  1,000,000,000,000
```

Con un millón de datos, un algoritmo O(log n) da 20 pasos, uno O(n log n) unos 20 millones y uno O(n²) un billón. A unos 100 millones de pasos sencillos por segundo, el último tardaría casi tres horas. Es la tabla de la teoría 01: guárdala.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `IndentationError` al descomentar una función | Quita solo el `# ` del principio: el cuerpo de la función tiene que quedar con sus cuatro espacios |
| `NameError: name 'target' is not defined` | Falta `globals=globals()` en `timeit.timeit` |
| Tus tiempos no se parecen a los del README | Es normal: compara la proporción entre filas, no los números |
| Los tiempos saltan mucho entre ejecuciones | Cierra programas pesados y repite; mira la tendencia, no una medida suelta |
| El programa parece colgado | Pusiste un `n` demasiado grande en un algoritmo O(n²): `Ctrl+C` y redúcelo |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · itertools](../../1-teoria/05-itertools.md) | **Ejercicio 01 · Contar pasos y medir** | [Ejercicio 02 · Buscar y ordenar](../ejercicio-02-buscar-y-ordenar/README.md) |
