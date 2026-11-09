# Rúbrica de Evaluación — Semana 23: NumPy

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 22 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | `np.arange(12).reshape(3, 4)` tiene `strides` `(32, 8)`. ¿Qué significan esos dos números? ¿Por qué `reshape` y `.T` no copian nada? | 10 |
| 2 | ¿Qué `dtype` tiene `np.array([1, None])`, y por qué es un problema? ¿Qué usa tu Observatorio en su lugar? | 10 |
| 3 | `np.array([120], dtype=np.int8) + 10` da `[-126]`. ¿Qué ha pasado, y por qué Python puro no tiene ese problema? | 10 |
| 4 | `north = week[:, 0]` y luego `north[:] = 0`. ¿Cambia `week`? ¿Y si en lugar de un corte usas `week[[0, 1, 2], 0]`? ¿Cómo lo compruebas sin adivinar? | 10 |
| 5 | ¿Por qué `WEEK[(WEEK > 10) and (WEEK < 50)]` da `ValueError`? Escríbelo bien, y explica por qué hacen falta los paréntesis | 10 |
| 6 | `WEEK` tiene forma `(7, 4)`. `WEEK - WEEK.mean(axis=0)` funciona y `WEEK - WEEK.mean(axis=1)` no. Explica las dos con la regla del broadcasting y arregla la segunda de dos formas | 10 |
| 7 | Tienes `values = np.array([12.5, np.nan, 8.0])`. ¿Qué dan `values.mean()`, `values == np.nan` y `values > 10`? ¿Cómo calculas la media de los presentes? | 10 |
| 8 | Dos picos de 120 y −30 en 1 000 valores normales: con \|z\| > 2 salen menos atípicos de los que esperas. ¿Por qué? ¿Qué alternativa conoces? | 10 |
| 9 | ¿Cómo consigue tu Observatorio que `informe` no pague los 0,1 s de importar NumPy? Di las tres cosas que lo hacen posible y cómo lo prueba un test | 10 |
| 10 | En tu medida, `group_means` es más lenta que `Series.means()` y `zscores` 200 veces más rápida que la comprensión. ¿Por qué cada una? ¿Qué mutante de la semana sobrevive y por qué ningún test puede matarlo? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. Son los **bytes que hay que saltar** en el bloque para avanzar uno en cada eje: 32 para bajar una fila (4 elementos de 8 bytes) y 8 para pasar a la columna siguiente. El elemento `[1, 2]` está en el byte `1 × 32 + 2 × 8 = 48`. `reshape` y `.T` no mueven datos: crean otro array que mira el **mismo bloque** con otra `shape` y otros `strides` (la traspuesta, `(8, 32)`). Son vistas.
2. `object`: `None` no cabe en ningún tipo numérico, así que NumPy guarda **referencias** a objetos de Python, como una lista. Pierde la velocidad (vuelve a mirar el tipo de cada elemento) y muchas funciones dejan de funcionar. El Observatorio usa **NaN**, que es un `float64`: `values_array` pone `np.nan` donde falta el dato, en su posición.
3. `int8` va de −128 a 127: 130 no cabe y el resultado **da la vuelta** (desbordamiento), sin error ni aviso. Los enteros de Python crecen lo que haga falta; los de NumPy tienen un tamaño fijo en bytes. Solo al **crear** un array con un número que no cabe da `OverflowError`.
4. Sí: un corte es una **vista** del mismo bloque, y escribir en ella escribe en `week`. Con una lista de posiciones (`week[[0, 1, 2], 0]`) se crea una **copia**: cambiarla no toca `week`. Se comprueba con `np.shares_memory(week, north)` (o `north.base is week`).
5. `and` le pide a Python **un** `bool` de cada lado, y una máscara tiene muchos: NumPy no sabe si quieres "alguno" o "todos" y da `The truth value of an array with more than one element is ambiguous`. Bien: `WEEK[(WEEK > 10) & (WEEK < 50)]`. Los paréntesis hacen falta porque `&` tiene más prioridad que `>`: sin ellos se calcularía `10 & WEEK` primero.
6. Se comparan las formas por la derecha, y cada eje debe ser igual o 1. `(7, 4)` con `(4,)`: 4 con 4 encaja, y al `(4,)` le falta un eje que cuenta como 1 y se estira a 7: resta la media de cada **columna**. `(7, 4)` con `(7,)`: por la derecha, 4 frente a 7, ni iguales ni 1: `operands could not be broadcast together with shapes (7,4) (7,)`. Arreglos: `WEEK.mean(axis=1, keepdims=True)` o `WEEK.mean(axis=1)[:, None]`, las dos de forma `(7, 1)`.
7. `values.mean()` da `nan`: el NaN se contagia. `values == np.nan` da `[False False False]`: NaN no es igual a nada, ni a sí mismo. `values > 10` da `[ True False False]`: cualquier comparación con NaN es `False`. La media de los presentes: `np.nanmean(values)` o `values[~np.isnan(values)].mean()`, las dos 10.25.
8. Los picos **inflan la desviación** (en el ejercicio, de 9.96 a 10.52) y la media, que se calculan **con** ellos: todas las z se encogen y los valores que deberían destacar quedan por debajo del umbral. Los atípicos esconden a los demás. Alternativa robusta: los cuartiles, con atípico lo que quede fuera de `Q1 − 1,5 × IQR` y `Q3 + 1,5 × IQR`, porque los cuartiles casi no se mueven con unos pocos extremos. Y mirar los datos.
9. (1) `arrays.py` **no** se reexporta en `core/__init__.py`; (2) la CLI hace `from observatorio.core import arrays` **dentro** de `estadisticas`, no al principio; (3) los tipos `Stats`, `Counts` y `Floats` se importan en un bloque `if TYPE_CHECKING:`, que solo ve mypy, y funcionan en las anotaciones porque Python 3.14 las evalúa cuando alguien las pide (PEP 649). El test arranca **otro proceso** que importa `observatorio.cli` y escribe `'numpy' in sys.modules`: debe dar `False`. En el proceso de pytest no serviría, porque otros tests ya importaron NumPy.
10. `zscores` hace una resta y una división sobre 100 000 `float64` seguidos, en C, sin crear objetos; la comprensión crea un `float` de Python por valor. `group_means`, en cambio, trabaja con **texto**: `np.unique` ordena las 100 000 etiquetas (O(n log n), comparando cadenas), mientras que el diccionario de `Series.means` agrupa en una pasada. NumPy brilla con números de un tipo, no con etiquetas. Sobrevive quitar `count=len(series)` de `np.fromiter`: el array resultante es idéntico, solo cambia cómo se reserva la memoria (de una vez o creciendo). Es un **mutante equivalente**: no cambia lo que hace el programa, así que ningún test de comportamiento puede distinguirlo.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños | El historial de `week-23` muestra un commit por paso (tests, NumPy, módulo, comando, versión, tests propios), sin cambiar los tests del bootcamp, y cada commit pasó por los ganchos | 8 |
| Rojo a verde | Leyó `test_arrays.py` antes de escribir; puede decir qué test pasó a verde con cada paso, y qué le dijo Hypothesis si alguno falló | 8 |
| Ejecución en vivo | Ante el instructor: `estadisticas` con sus datos y con `-u`, el comprobante de `sys.modules`, una medida con `timeit` de `zscores` frente a la comprensión, y `pytest` en verde | 8 |
| Rompe y explica | Sube el `import` de `arrays` al principio de `cli.py` y explica qué test falla y por qué; cambia `if std == 0:` y explica por qué solo lo mata el test de los avisos | 8 |
| Explica sus decisiones | Explica el umbral que eligió para su dominio, dónde gana y dónde pierde NumPy con sus números, el coste en la imagen, y por qué el superviviente es equivalente | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 22

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| La serie como array | `core/arrays.py` con los alias `Floats` y `Counts`; `values_array` con `fromiter` y NaN en su sitio; `labels_array` con `dtype=np.str_`; sin reexportar en `core/__init__.py` | 15 |
| Estadística | `Stats` inmutable con tipos de Python; `stats_of` con `None` sin valores; `zscores` sin avisos; `outliers` con `flatnonzero`; `histogram` sin NaN; `group_means` con `unique` y `bincount` | 25 |
| El comando | `estadisticas RUTA` con `--umbral`/`-u` (`min=0`) e `--intervalos`/`-i` (`min=1`); import dentro del comando y tipos en `TYPE_CHECKING`; `stats_table` e `histogram_lines`; errores a stderr y código 1 | 15 |
| Tests propios | Al menos 6 tests en `tests/test_my_arrays.py` con datos de su dominio, cada uno visto fallar con un mutante | 20 |
| Calidad | `pre-commit run --all-files`, `coverage report` y `alembic check` sin avisos; `docker compose run --rm app` en verde; CI en verde; `numpy==2.5.4` en las dependencias; imágenes `week-23`; versión `0.23.0` | 10 |
| Git y README | Rama `week-23` en `python-<nombre>-<apellido>`; README con la sección "Estadísticas" | 5 |
| Pull request | Salidas, CI, `estadisticas` con sus datos y su umbral, tabla de tiempos, tamaño de la imagen, tabla de mutantes y el equivalente explicado | 10 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | [Semana 24](../week-24-pandas_series_dataframe_y_seleccion/README.md) |
