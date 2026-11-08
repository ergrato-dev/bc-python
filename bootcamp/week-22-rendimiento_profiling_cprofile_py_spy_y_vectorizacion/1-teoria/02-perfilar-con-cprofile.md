# 02 · Perfilar con cProfile

⏱️ 50 min

## 🎯 Objetivos

- Explicar qué es un perfilador y qué hace uno **determinista** como cProfile.
- Perfilar un programa entero desde la terminal y una función desde el código.
- Leer `ncalls`, `tottime` y `cumtime`, y ordenar por el que responde a tu pregunta.
- Explorar un perfil guardado con `pstats`: filtrar, ver quién llama a quién.
- Tener en cuenta lo que cProfile cambia al medir.

---

## 1. Qué es un perfil

Un **perfil** responde a "¿dónde se va el tiempo?" función por función: cuántas veces se llamó cada una y cuánto tardó. Un **perfilador** es la herramienta que lo construye mientras tu programa corre.

Python trae dos en la biblioteca estándar: `cProfile`, escrito en C, y `profile`, en Python puro y mucho más lento. Usa siempre `cProfile`.

cProfile es **determinista**: Python le avisa en **cada** llamada y en cada retorno de función, y él anota la hora. No se le escapa ninguna llamada, por corta que sea. A cambio, añade un coste a cada una (sección 7). La teoría 03 presenta la otra familia, la de **muestreo**.

---

## 2. Perfilar un programa entero

Sin tocar el código, desde la terminal:

```bash
uv run python -m cProfile -s cumulative -m observatorio informe -f perfil/grande.txt > perfil/w21.txt
```

- `-m cProfile` ejecuta el módulo `cProfile`, que a su vez ejecuta lo que le sigue;
- `-s cumulative` ordena el informe por tiempo acumulado;
- `-m observatorio informe ...` es tu programa, como si escribieras `python -m observatorio informe ...`.

El informe sale por la salida estándar **después** de la de tu programa; por eso aquí todo va a un archivo. Mejor aún, guarda el perfil en binario con `-o` y míralo después, de varias formas, sin volver a ejecutar:

```bash
uv run python -m cProfile -o perfil/w21.prof -m observatorio informe -f perfil/grande.txt > /dev/null
```

---

## 3. Leer el informe

Las primeras líneas del perfil de `informe` con 100 000 medidas, en la semana 21:

```
         137603367 function calls (132789672 primitive calls) in 51.295 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.081    0.081   51.801   51.801 cli.py:145(informe)
        2    0.000    0.000   49.374   24.687 console.py:1652(print)
        1    0.173    0.173    0.950    0.950 cli.py:132(table_of)
        1    0.097    0.097    0.622    0.622 analysis.py:17(process_lines)
        1    0.033    0.033    0.443    0.443 model.py:102(from_lines)
        1    0.000    0.000    0.008    0.008 trends.py:31(median)
```

(Aquí solo van algunas filas; el perfil real tiene más de 6 000.)

| Columna | Qué es |
|---|---|
| `ncalls` | Cuántas veces se llamó la función |
| `tottime` | Tiempo **propio**: dentro de la función, sin contar las que llama |
| `percall` (la primera) | `tottime / ncalls` |
| `cumtime` | Tiempo **acumulado**: desde que entra hasta que sale, con todo lo que llama |
| `percall` (la segunda) | `cumtime / ncalls` |
| `filename:lineno(function)` | Dónde está definida |

Leído de arriba abajo: `informe` acumula 51,8 s, y de ellos `Console.print`, 49,4 s. Lo curioso es `table_of`: **construir** la tabla de 100 000 filas cuesta 0,95 s; **pintarla** (`print` la convierte en texto con bordes, colores y anchos) cuesta 49. El análisis de las líneas, 1 s entre las dos funciones. La mediana, 8 ms.

Cuando una función es recursiva, `ncalls` sale como `3800053/1400026`: el primer número cuenta todas las llamadas y el segundo solo las **primitivas**, las que no vienen de la propia función. Rich pinta una tabla llamándose a sí mismo para cada celda.

---

## 4. Dos órdenes, dos preguntas

| Orden | Responde a | Arriba salen |
|---|---|---|
| `cumulative` | ¿Qué **rama** del programa es cara? | `main`, `informe`, las funciones que lo coordinan todo |
| `tottime` | ¿Dónde se **trabaja** de verdad? | Funciones pequeñas que se llaman mucho, a menudo de bibliotecas |

Empieza por `cumulative` para orientarte (de `informe` a `print`) y sigue con `tottime` para ver las funciones que gastan:

```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
3800053/1400026    2.406    0.000   48.483    0.000 console.py:1294(render)
  1400021    2.241    0.000   38.831    0.000 table.py:755(_render)
  4314920    1.937    0.000    2.276    0.000 cells.py:98(cell_len)
```

Con `tottime` el tiempo está **repartido**: ninguna función pasa de 2,5 s. No hay una función lenta que arreglar dentro de Rich; lo caro es pedirle 1,4 millones de celdas. El arreglo no está en Rich, sino en `informe`: pintar menos filas.

Es el caso típico: el perfil señala una biblioteca, y la solución es **llamarla menos**.

---

## 5. Explorar un perfil con `pstats`

El módulo `pstats` lee un perfil guardado:

```python
import pstats

stats = pstats.Stats("perfil/w21.prof")
stats.strip_dirs()                      # sin rutas largas
stats.sort_stats("tottime")
stats.print_stats(10)                   # las 10 primeras
stats.print_stats("observatorio")       # solo las funciones cuya ruta contiene "observatorio"
stats.print_callers("parse_record")     # quién llama a parse_record, y cuántas veces
stats.print_callees("informe")          # a quién llama informe
```

`print_stats` acepta números (cuántas filas) y textos (una expresión regular sobre `archivo:línea(función)`), y se pueden combinar: `print_stats("observatorio", 5)`.

También hay un modo interactivo:

```bash
uv run python -m pstats perfil/w21.prof
```

```
perfil/w21.prof% sort tottime
perfil/w21.prof% stats 5
perfil/w21.prof% callers parse_record
perfil/w21.prof% quit
```

`print_callers` es clave en el segundo cuello de botella del proyecto. Después de arreglar la tabla, `parse_record` sale con **200 000** llamadas para 100 000 líneas:

```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   200000    0.108    0.000    0.313    0.000 groups.py:27(parse_record)
```

`callers parse_record` dice que la llaman dos: `rules.py(parse_line)`, desde `process_lines`, y `groups.py(records_of)`, desde `Series.from_lines`. Cada línea se analiza dos veces. Mirar `ncalls` y preguntarte "¿cuántas veces **debería** llamarse?" encuentra tantos problemas como mirar los tiempos.

---

## 6. Perfilar una función desde el código

Para perfilar solo una parte, sin el arranque ni las importaciones:

```python
import cProfile
import pstats

with cProfile.Profile() as profiler:
    report(records)

pstats.Stats(profiler).strip_dirs().sort_stats("tottime").print_stats(5)
```

O con `runcall`, que además devuelve el resultado:

```python
profiler = cProfile.Profile()
result = profiler.runcall(report, records)
```

Así perfilas en un test. En el proyecto, `calls_of` cuenta las llamadas a una función leyendo el diccionario `stats` de `pstats.Stats`:

```python
code = function.__code__
key = (code.co_filename, code.co_firstlineno, code.co_name)
calls = pstats.Stats(profiler).stats[key][1]
```

Cada función se identifica por su archivo, la línea donde empieza y su nombre: lo que dice su objeto de código, da igual con qué nombre la importó cada módulo. El segundo número de cada entrada es `ncalls`. Los *stubs* de tipos de `pstats` no declaran el atributo `stats`, y por eso el proyecto lleva un `# type: ignore[attr-defined]` en esa línea.

---

## 7. El precio de mirar

cProfile hace trabajo en cada llamada y cada retorno. Con el `informe` de la semana 21:

| Ejecución | Tiempo |
|---|---|
| Sin perfilador | 21 s |
| Con cProfile | 51 s |

Más del doble: el programa hace 137 millones de llamadas, y cada una paga su parte. Consecuencias:

- los **tiempos absolutos** de un perfil no son los de tu programa; las **proporciones** sí te sirven;
- las funciones **pequeñas y muy llamadas** salen infladas, porque pagan el coste muchas veces para hacer poco trabajo: una función de una línea llamada un millón de veces puede parecer más cara de lo que es;
- el código en C (como `sorted` o `str.split`) se mide como una sola llamada, sin ver lo que hace dentro.

Para medir el arreglo, **no** uses el perfil: vuelve a `time` o `timeit` (teoría 01), sin perfilador. Y si sospechas que cProfile te engaña, contrasta con py-spy, que casi no frena el programa (teoría 03).

---

## 8. Errores frecuentes

| Error | Por qué está mal | Qué hacer |
|---|---|---|
| Usar `profile` en lugar de `cProfile` | Es el mismo informe, muchas veces más lento | `cProfile` |
| `python -m cProfile` sin `-s` | Ordena por nombre de función: no se ve nada | `-s cumulative` o `-s tottime`, o `-o` y `pstats` |
| Leer solo `cumtime` | Arriba siempre salen `main` y compañía, que no trabajan | `cumtime` para orientarte, `tottime` para el detalle |
| Optimizar la función de `tottime` más alto aunque sea de una biblioteca | Rara vez puedes cambiarla, y casi nunca es el problema | Busca quién la llama tanto (`print_callers`) |
| Ignorar `ncalls` | 200 000 llamadas para 100 000 líneas es un aviso, aunque cada una sea rápida | Pregúntate cuántas veces debería llamarse |
| Medir la mejora con el perfil | cProfile frena el programa de forma desigual | El perfil dice dónde; `time` o `timeit` dicen cuánto |
| Perfilar con datos pequeños | Con 10 líneas, el arranque tapa todo lo demás | Datos del tamaño real |

---

## ✅ Qué debes saber al terminar

- [ ] Qué es un perfilador determinista y por qué cProfile no se salta ninguna llamada.
- [ ] Cómo perfilar un programa con `python -m cProfile -o` y una función con `cProfile.Profile`.
- [ ] Qué son `ncalls`, `tottime` y `cumtime`, y qué pregunta responde cada orden.
- [ ] Cómo filtrar un perfil y ver quién llama a una función con `pstats`.
- [ ] Por qué cProfile ralentiza el programa, y qué partes del perfil se fían y cuáles no.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [01 · Medir antes de optimizar](01-medir-antes-de-optimizar.md) | **02 · Perfilar con cProfile** | [03 · Muestrear con py-spy](03-muestrear-con-py-spy.md) |
