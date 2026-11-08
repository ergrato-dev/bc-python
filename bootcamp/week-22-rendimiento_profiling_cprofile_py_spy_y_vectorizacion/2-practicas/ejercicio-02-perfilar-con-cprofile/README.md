# Ejercicio 02 — Perfilar con cProfile

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-perfilar-con-cprofile.md) y [04](../../1-teoria/04-optimizar-python-puro.md)

## Objetivo

Encontrar con cProfile dónde se va el tiempo de un programa lento y arreglarlo:

- perfilar una función con `cProfile.Profile` y leer el informe con `pstats`;
- distinguir el tiempo **acumulado** (`cumtime`) del tiempo **propio** (`tottime`);
- averiguar **quién** llama a la función cara;
- cambiar el algoritmo y comprobar que el resultado no cambia;
- perfilar otra vez y ver que el cuello de botella ya es otro;
- hacer lo mismo desde la terminal con `python -m cProfile` y `python -m pstats`.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-22-rendimiento_profiling_cprofile_py_spy_y_vectorizacion/2-practicas/ejercicio-02-perfilar-con-cprofile/starter
uv run python main.py
```

```
Ejercicio 02 · Perfilar
```

`report` calcula la mediana de cada etiqueta de 20 000 registros con 2 000 etiquetas distintas. Lee las cuatro funciones de arriba de `main.py` antes de seguir: ¿cuál crees que es la lenta? Apúntalo. Al final del paso 3 sabrás si acertaste.

## Pasos

### 1. Cuánto tarda

Descomenta el **PASO 1** y ejecuta:

```
report: 0.70 s · 2000 etiquetas
```

Casi un segundo para 20 000 registros. El ordenador hace cientos de millones de operaciones por segundo: algo está haciendo mucho más trabajo del necesario.

### 2. Perfilar con cProfile, por tiempo acumulado

Descomenta el **PASO 2** y ejecuta:

```
report con cProfile: 0.69 s
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.002    0.002    0.694    0.694 main.py:46(report)
     2000    0.562    0.000    0.562    0.000 main.py:32(values_of)
        1    0.125    0.125    0.125    0.125 main.py:23(unique_labels)
     2000    0.002    0.000    0.005    0.000 main.py:37(median)
     2000    0.002    0.000    0.002    0.000 {built-in method builtins.sorted}
     4000    0.000    0.000    0.000    0.000 {built-in method builtins.len}
```

`profiler.runcall(report, RECORDS)` ejecuta `report(RECORDS)` mientras cProfile anota **cada** llamada a una función y cuánto dura. `pstats.Stats` lee esas notas; `strip_dirs()` quita las rutas largas y `sort_stats("cumulative")` ordena por tiempo acumulado.

Las columnas:

| Columna | Qué es |
|---|---|
| `ncalls` | Cuántas veces se llamó |
| `tottime` | Tiempo **dentro** de la función, sin contar las que llama |
| `cumtime` | Tiempo desde que entra hasta que sale, **con** las que llama |
| `percall` | La de antes dividida por `ncalls` |

`report` acumula 0,694 s, pero su tiempo propio es 0,002: casi todo lo gastan las funciones que llama. Por `cumtime` lees el programa **de arriba abajo**: qué rama del árbol de llamadas pesa.

Aquí cProfile casi no ralentiza (0,69 s con y sin él) porque hay pocas llamadas. Su coste va **por llamada**: en un programa con millones de llamadas pequeñas puede doblar el tiempo (teoría 02).

### 3. Por tiempo propio

Descomenta el **PASO 3** y ejecuta:

```
---
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     2000    0.562    0.000    0.562    0.000 main.py:32(values_of)
        1    0.125    0.125    0.125    0.125 main.py:23(unique_labels)
        1    0.002    0.002    0.694    0.694 main.py:46(report)
     2000    0.002    0.000    0.002    0.000 {built-in method builtins.sorted}
     2000    0.002    0.000    0.005    0.000 main.py:37(median)
```

Ordenado por `tottime`, arriba sale **dónde se trabaja** de verdad: `values_of`, con el 81 % del total. Se llama 2 000 veces, una por etiqueta, y cada vez recorre los 20 000 registros: 40 millones de comparaciones. `unique_labels` es la segunda: `label not in seen` con `seen` una lista (ejercicio 01, paso 3).

`median`, que ordena, parecía la sospechosa: cuesta 0,005 s. Por eso se mide antes de optimizar.

En Python 3.14 la comprensión de `values_of` no sale como función aparte (`<listcomp>`): desde Python 3.12 va dentro de la función que la contiene.

### 4. Quién la llama

Descomenta el **PASO 4** y ejecuta:

```
---
   List reduced from 8 to 1 due to restriction <'values_of'>
main.py:32(values_of)  <-    2000    0.562    0.562  main.py:46(report)
```

`print_callers("values_of")` dice desde dónde se llama a `values_of` y cuántas veces. En un programa grande, la función lenta suele ser buena; el problema es quien la llama 2 000 veces. `print_callees` hace lo contrario: a quién llama una función.

### 5. Agrupar una vez

Descomenta el **PASO 5** y ejecuta:

```
report_grouped: 0.003 s · igual: True
```

`report_grouped` recorre los registros **una sola vez** y reparte cada valor en su grupo con un `defaultdict(list)`, como `values_by_label` de tu Observatorio. De O(n · k) a O(n): de 0,70 s a 0,003 s, más de 200 veces. Y como un `dict` guarda el orden de inserción, las etiquetas salen en el orden en que aparecen, sin `unique_labels`.

`igual: True` es tan importante como el tiempo: una optimización que cambia el resultado es un error. En tu proyecto, esa comprobación la hacen los tests.

### 6. Perfilar otra vez

Descomenta el **PASO 6** y ejecuta:

```
---
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.005    0.005    0.008    0.008 main.py:110(report_grouped)
    20000    0.002    0.000    0.002    0.000 {method 'append' of 'list' objects}
     2000    0.001    0.000    0.001    0.000 {built-in method builtins.sorted}
     2000    0.001    0.000    0.002    0.000 main.py:37(median)
```

El perfil ya no tiene un culpable: el tiempo se reparte entre el bucle, los `append` y las medianas. Es la señal de **parar**. Ahora cProfile sí pesa: 0,008 s con él frente a 0,003 s sin él, porque las 20 000 llamadas a `append` son cortas y su coste por llamada se nota.

### Desde la terminal

Sin tocar el código, con los pasos que tengas descomentados:

```bash
uv run python -m cProfile -s tottime main.py | head -12
```

```
Ejercicio 02 · Perfilar
report: 0.71 s · 2000 etiquetas
         153922 function calls (153894 primitive calls) in 0.751 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     2000    0.575    0.000    0.575    0.000 main.py:32(values_of)
        1    0.126    0.126    0.126    0.126 main.py:23(unique_labels)
        1    0.013    0.013    0.034    0.034 main.py:17(make_records)
        3    0.006    0.002    0.006    0.002 {built-in method builtins.compile}
```

(La salida es con solo el paso 1 descomentado.) Perfila el programa entero: aparecen también `make_records` y las importaciones. Para guardar el perfil y explorarlo después:

```bash
uv run python -m cProfile -o perfil.prof main.py
uv run python -m pstats perfil.prof
```

`pstats` abre un intérprete: escribe `sort tottime`, `stats 3` y `quit`. Así perfilas una vez un programa lento y lo miras de varias formas sin volver a ejecutarlo.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'medians' is not defined` | El paso 5 compara con el resultado del paso 1: descomenta en orden |
| `StopIteration` en `show` | `print_stats` no escribió la cabecera `ncalls`: revisa que `profiler.runcall` se ejecutó antes |
| Las rutas salen enteras (`/home/.../main.py`) | Falta `strip_dirs()` |
| `igual: False` | Has cambiado `report_grouped`: el `dict` debe guardar las etiquetas en el orden en que aparecen |
| `python -m cProfile` no escribe nada útil | Sin `-s`, ordena por nombre: usa `-s tottime` o `-s cumulative` |
| `perfil.prof` no se abre con `cat` | Es binario: se lee con `python -m pstats` o con `pstats.Stats("perfil.prof")` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Medir](../ejercicio-01-medir-con-timeit/README.md) | **Ejercicio 02 · Perfilar con cProfile** | [Ejercicio 03 · Muestrear con py-spy](../ejercicio-03-muestrear-con-py-spy/README.md) |
