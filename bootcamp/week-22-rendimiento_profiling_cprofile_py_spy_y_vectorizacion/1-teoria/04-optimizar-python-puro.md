# 04 · Optimizar en Python puro

⏱️ 45 min

## 🎯 Objetivos

- Ordenar las formas de optimizar de la que más gana a la que menos.
- Quitar trabajo que nadie necesita y hacer una sola vez el que se repite.
- Elegir la estructura de datos y el algoritmo antes que cualquier truco.
- Aprovechar las funciones de Python escritas en C.
- Medir el arranque de un programa y la memoria que usa.

---

## 1. De lo que más gana a lo que menos

Cuando el perfil ha señalado dónde se va el tiempo, prueba en este orden:

| # | Pregunta | Ejemplo de esta semana | Cuánto ganó |
|---|---|---|---|
| 1 | ¿Hace falta este trabajo? | Pintar 20 filas, no 100 000 | De 21 s a 1,1 s |
| 2 | ¿Se hace más de una vez? | Analizar cada línea una vez, no dos | Casi nada: dentro del ruido |
| 3 | ¿Hay una estructura o un algoritmo mejor? | Agrupar con un `dict` en una pasada | De 0,70 s a 0,003 s (ejercicio 02) |
| 4 | ¿Lo hace ya una función de Python en C? | `sum()` en vez de un bucle | 3 veces (ejercicio 04) |
| 5 | ¿Y con NumPy? | Teoría 05 | Hasta 100 veces, si los datos ya están en arrays |

Los trucos pequeños (guardar un método en una variable local para no buscarlo en cada vuelta, evitar un `.` en un bucle) ganan un poco por ciento y hacen el código más raro. Casi nunca merecen la pena: si el paso 1 o el 3 están sin hacer, ningún truco te salva.

---

## 2. No hacer el trabajo

El trabajo más rápido es el que no se hace. En el `informe`, el 95 % del tiempo se iba en pintar una tabla de 100 000 filas: 5,4 MB de texto que nadie lee en una terminal. La solución no es pintarla más deprisa, es pintar **menos**:

```python
shown = series.measurements[:rows]
caption = f"{len(shown)} de {len(series)} medidas" if len(shown) < len(series) else None
table = Table(title="Medidas", caption=caption)
```

Las primeras 20 filas y un pie que dice cuántas hay. Quien quiera todas, las pide con `--filas`. La salida pasa de 5,4 MB a 1,8 KB, el tiempo de 21 s a 1,1 s y la memoria de 330 a 119 MB.

Busca este tipo de trabajo inútil:

- **salida** que nadie va a leer entera: tablas, listas, registros (*logs*) en `DEBUG` dentro de un bucle;
- **cálculos** cuyo resultado no se usa, o que se usan solo a veces: calcúlalos solo cuando haga falta;
- **datos** que se cargan enteros para usar una parte: un generador (semana 11) lee de uno en uno.

---

## 3. Hacerlo una vez

Lo segundo es el trabajo **repetido**. El perfil lo delata en `ncalls`: después de arreglar la tabla, `parse_record` salía con 200 000 llamadas para 100 000 líneas. `informe` hacía:

```python
rows, errors = process_lines(lines, scale.unit, scale.low, scale.high)  # analiza cada línea
series = Series.from_lines(lines)                                       # y otra vez
```

`process_lines` daba las filas de texto y los errores; `from_lines`, las medidas. Las dos analizaban las mismas líneas. El arreglo es analizar **una vez** y sacar de ahí todo lo demás:

```python
series, errors = Series.parse(lines)
rows = [scale.row(measurement) for measurement in series]
```

`scale.row` da la misma fila que `parse_line` a partir de una medida ya analizada, sin volver a partir el texto. Un test con Hypothesis comprueba que `Series.parse` da las mismas filas y los mismos errores que `process_lines` para cualquier lista de líneas: así sabes que el atajo no cambió nada.

Medido, este arreglo apenas se nota: de 1,06 a 1,05 s, dentro del ruido. Analizar las líneas era una parte pequeña del total, y te has ahorrado la mitad de ella (Amdahl otra vez). El perfil decía la verdad, `parse_record` se llamaba el doble, pero no toda verdad del perfil vale segundos. Se queda porque `informe` es más simple así y porque, con un test que cuenta las llamadas, el trabajo no volverá a doblarse sin que nadie se entere.

Otras formas de no repetir:

- **guardar el resultado** en una variable en lugar de llamar dos veces a la misma función con lo mismo;
- `functools.cache` (semana 12) para una función **pura** que se llama muchas veces con los mismos argumentos;
- sacar del bucle lo que no cambia en cada vuelta: un `re.compile`, un `set(...)`, un `len(...)`.

Hay más repetición en el Observatorio: `Series.values()`, `labels()`, `means()` y `most_common()` construyen cada una la lista de tuplas `records`, cuatro veces en cada `informe` (80 ms de 1 s). Es un buen reto para tus tests propios, pero mira antes qué fracción es (teoría 01, Amdahl).

---

## 4. La estructura y el algoritmo

Cuando un perfil señala un bucle, pregúntate qué **complejidad** tiene (semana 6):

| Síntoma en el perfil | Causa típica | Cambio |
|---|---|---|
| `x in lista` dentro de un bucle | Buscar en una lista es O(n) | Un `set` o un `dict`: O(1) |
| Una función que recorre todo, llamada una vez por elemento | O(n²) escondido | Agrupar una vez con un `dict` |
| `lista.insert(0, x)` o `lista.pop(0)` | Mueven todos los elementos | `collections.deque` |
| Ordenar dentro de un bucle | O(n log n) en cada vuelta | Ordenar una vez fuera |
| Buscar el mínimo de lo que va llegando | Ordenar todo cada vez | `heapq` |

El ejercicio 02 lo enseña con números: `values_of` recorría los 20 000 registros una vez por cada una de las 2 000 etiquetas, 40 millones de comparaciones. Con un `defaultdict(list)` es una sola pasada: más de 200 veces más rápido. Ningún truco de bajo nivel gana algo así.

---

## 5. Las funciones de Python en C

Las funciones incorporadas y la biblioteca estándar están escritas en C. Un bucle de Python ejecuta cada vuelta en el intérprete; `sum`, `max`, `sorted`, `str.join`, `Counter` o `itertools` hacen el bucle en C:

| Lo mismo, de dos formas | Un millón de valores |
|---|---|
| `for value in values: total += value` | 17 ms |
| `sum(values)` | 5 ms |

Las comprensiones también son más rápidas que el bucle equivalente con `append`, porque Python las compila de forma más directa, y se leen mejor. Para construir un texto, `"".join(partes)` en vez de sumar con `+=` en un bucle.

Es la misma idea que vectorizar (teoría 05), en pequeño: describir **qué** quieres en una sola operación y dejar el **cómo** a código compilado.

---

## 6. El arranque

Después de arreglar la tabla y el doble análisis, `informe` con 100 000 medidas tarda alrededor de 1 segundo. ¿Cuánto es tu código? Mide solo importar la CLI:

```bash
uv run python -X importtime -c "import observatorio.cli" 2>&1 | tail -1
```

```
import time:      3623 |     451584 | observatorio.cli
```

La segunda columna son microsegundos acumulados: **0,45 s** solo en importar, antes de leer una línea. SQLAlchemy, Pydantic, FastAPI, httpx y Rich se importan aunque `informe` no use la base de datos ni la red. Ordena la salida para ver quién pesa:

```bash
uv run python -X importtime -c "import observatorio.cli" 2>&1 | sort -t'|' -k2 -n | tail -5
```

Por Amdahl, ese medio segundo es ahora casi la mitad del `informe`, y todo el `observatorio --version`. La solución de la semana 20 fue importar uvicorn y la API **dentro** de `servir`, solo cuando hacen falta. Llevarlo a todo el paquete es un cambio grande que no compensa en una CLI que tarda un segundo; en una herramienta que se ejecuta cientos de veces al día, sí.

---

## 7. La memoria

El tiempo no es lo único que se mide. GNU `time` (en Linux, `/usr/bin/time`; en macOS, `gtime` con Homebrew) da la memoria máxima del proceso:

```bash
/usr/bin/time -f "%e s %M KB" uv run observatorio informe -f perfil/grande.txt > /dev/null
```

```
1.07 s 118972 KB
```

`%M` es el máximo de memoria que llegó a usar, en KB. Con la tabla entera eran 330 MB: Rich construye cada línea antes de escribirla. Para ver qué líneas de tu código reservan la memoria, la biblioteca estándar tiene `tracemalloc`.

Una lista de un millón de `float` ocupa unos 32 MB (8 bytes por referencia y 24 por cada objeto `float`); un array de NumPy con los mismos valores, 8 MB (teoría 05).

---

## 8. Cuando Python puro no basta

Si después de todo lo anterior el perfil sigue señalando un **cálculo numérico** en tu código:

- **NumPy** (teoría 05 y semana 23) si son operaciones sobre muchos números;
- **varios procesos** (semana 16) si el trabajo se reparte en partes independientes;
- una **extensión compilada** (Cython, o Rust con PyO3, como py-spy o ruff) si es un algoritmo propio muy usado.

Cada una añade complejidad. Llega a ellas con un perfil en la mano, no antes.

---

## 9. Errores frecuentes

| Error | Por qué está mal | Qué hacer |
|---|---|---|
| Empezar por los trucos pequeños | Ganan un poco por ciento; el algoritmo gana veces | Primero el trabajo inútil, el repetido y la estructura |
| Optimizar sin un test que compruebe el resultado | Rápido y mal es peor que lento | Tests antes, y uno que compare con la versión vieja |
| Quitar salida que alguien usa | Rompes a quien lee la tabla entera | Un valor por defecto razonable y una opción para pedir más |
| Cachear una función que no es pura | Devuelve un resultado viejo cuando lo de fuera cambia | `cache` solo para funciones que dependen solo de sus argumentos |
| Ignorar el arranque | En una CLI rápida puede ser la mitad del tiempo | `python -X importtime` |
| Mirar solo el tiempo | Un programa rápido que usa 4 GB también falla | `/usr/bin/time -f %M` y `tracemalloc` |

---

## ✅ Qué debes saber al terminar

- [ ] El orden: quitar trabajo, no repetirlo, mejor estructura, funciones en C, NumPy.
- [ ] Cómo detectar trabajo repetido con `ncalls` y cómo comprobar que el atajo da lo mismo.
- [ ] Qué cambio de estructura corresponde a cada síntoma típico de un perfil.
- [ ] Por qué `sum()` gana a un bucle aunque haga lo mismo.
- [ ] Cómo medir el arranque con `-X importtime` y la memoria con `/usr/bin/time`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [03 · Muestrear con py-spy](03-muestrear-con-py-spy.md) | **04 · Optimizar en Python puro** | [05 · Vectorizar con NumPy](05-vectorizar-con-numpy.md) |
