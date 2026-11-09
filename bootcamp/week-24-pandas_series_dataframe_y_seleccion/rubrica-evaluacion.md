# Rúbrica de Evaluación — Semana 24: pandas I

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 23 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | ¿Qué añade una `Series` a un array de NumPy? ¿Qué `dtype` tienen `pd.Series([1, None, 3])` y `pd.Series(["A", None])`, y por qué el primero no es `int64`? | 10 |
| 2 | `monday` tiene el índice `["Norte", "Sur"]` y `tuesday`, `["Sur", "Este"]`. ¿Qué da `monday + tuesday`? ¿Y con `add(..., fill_value=0)`? | 10 |
| 3 | `codes = pd.Series(["a", "b", "c"], index=[10, 20, 30])`. ¿Qué dan `codes[0]`, `codes.iloc[0]`, `codes.loc[10:20]` y `codes.iloc[0:2]`? | 10 |
| 4 | Lees un CSV de estaciones con `sep=";"` y `decimal=","`, y la columna `pais` de Namibia sale vacía. ¿Por qué? Arréglalo sin perder el `NA` de la columna `valor` | 10 |
| 5 | Tras leer un CSV, `valor` tiene `dtype` `str` en lugar de `float64`. ¿Qué ha pasado, y cómo encuentras la fila culpable? | 10 |
| 6 | `READINGS` tiene una fila con `valor` NaN. ¿Qué diferencia hay entre `READINGS[~(READINGS["valor"] > 20)]` y `READINGS[READINGS["valor"] <= 20]`? ¿Y por qué `(a > 10) and (b == 1)` da `ValueError`? | 10 |
| 7 | ¿Por qué `df[df["estacion"] == "Norte"]["valor"] = 0` no cambia `df`, y cómo se escribe bien? Explica *copy-on-write* y por qué no gasta el doble de memoria | 10 |
| 8 | En `with_levels`, ¿qué pasaría sin `right=False` con un valor igual a `low` y otro igual a `high`? ¿Qué test lo detecta? | 10 |
| 9 | ¿Por qué tu Observatorio lee con `Series.parse` y convierte con `frame_of`, si `read_csv` es diez veces más rápido? ¿Cuándo elegirías `read_csv`? | 10 |
| 10 | ¿Por qué `test_by_value_keeps_ties_in_their_order` no mata el mutante que quita `kind="stable"` y `test_by_value_keeps_ties_in_order_in_a_long_frame` sí? ¿Qué te dice eso de los tests con pocos datos? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. Un **índice**: una etiqueta para cada valor, con la que se elige (`s["Sur"]`) y se alinean las operaciones; y un nombre. Por dentro, los valores siguen en un array de NumPy. `pd.Series([1, None, 3])` es `float64`: `None` pasa a NaN, y NaN solo existe en coma flotante, así que los enteros se convierten en `1.0` y `3.0` (para enteros con datos que faltan, `dtype="Int64"`). `pd.Series(["A", None])` es `str`, el tipo de texto de pandas 3, con `nan` en el que falta.
2. pandas suma por **etiqueta**: `Este NaN`, `Norte NaN`, `Sur 25.0`. Sur está en las dos (20 + 5); Norte y Este solo en una, y no hay con qué sumar. El índice del resultado es la unión, ordenada. Con `fill_value=0`, lo que falta cuenta como 0: `Este 7.0`, `Norte 10.0`, `Sur 25.0`.
3. `codes[0]` da `KeyError: 0`: con corchetes, un entero es una **etiqueta**, y no hay ninguna 0. `codes.iloc[0]` da `'a'`, la posición 0. `codes.loc[10:20]` da `['a', 'b']`: por etiqueta, el final se incluye. `codes.iloc[0:2]` da `['a', 'b']`: por posición, el final (2) se excluye.
4. `read_csv` trata como dato que falta una lista de textos en **todas** las columnas, y `"NA"` (el código de Namibia) está en ella, como `"null"`, `"None"` o `""`. Arreglo: `keep_default_na=False` para apagar esa lista y `na_values={"valor": ["NA"]}` para que solo `NA` en `valor` sea un dato que falta.
5. Una celda de `valor` no es un número (por ejemplo, `"19,8 C"`): `read_csv` no da error, convierte **toda** la columna a texto. Se encuentra con `pd.to_numeric(df["valor"].str.replace(",", "."), errors="coerce")`, que pone NaN donde no puede convertir, y `df[numbers.isna()]` (descartando las que ya faltaban). Por eso, tras cada `read_csv`, se miran los `dtypes`.
6. Las comparaciones con NaN dan `False`. `~(valor > 20)` invierte la máscara, así que la fila con NaN (`False`) pasa a `True` y **entra**; `valor <= 20` da `False` en esa fila y **no entra**. `and` pide un solo `bool` a cada lado y una máscara tiene muchos: `The truth value of a Series is ambiguous`. Se escribe `(a > 10) & (b == 1)`, con paréntesis porque `&` se calcula antes que las comparaciones.
7. `df[máscara]` crea una tabla intermedia, y `["valor"] = 0` cambia **esa** tabla, que nadie guarda: pandas 3 avisa con `ChainedAssignmentError`. Bien: `df.loc[df["estacion"] == "Norte", "valor"] = 0`, en un solo paso. *Copy-on-write*: toda tabla o columna que sale de otra se comporta como una copia; cambiarla no cambia la original. No gasta el doble porque mientras nadie escribe, las dos comparten los datos; la copia se hace al escribir, y solo de lo que cambia.
8. Con `right=True` (el valor por defecto), cada intervalo incluye su borde **derecho**: un valor igual a `low` caería en `(-inf, low]`, "bajo", y uno igual a `high` en `(low, high]`, "medio". `classify` dice "medio" y "alto". Lo detectan `test_with_levels_borders_like_classify` (los cuatro bordes) y `test_with_levels_agrees_with_scale_level`, que con Hypothesis compara con `Scale.level`.
9. Porque `read_csv` **no valida**: una línea sin `;` se convierte en una fila con la etiqueta rara y sin valor, y una celda que no es un número convierte la columna a texto, sin error. `Series.parse` aparta cada línea mala y dice cuál es, y `filtrar` acaba con código 1. Medido, convertir con `frame_of` cuesta 11,5 ms con 100 000 medidas; el análisis del texto domina igual. `read_csv` compensa con archivos enormes de una fuente en la que confías, o si validas después la tabla entera.
10. Con tres filas, el algoritmo por defecto también deja los empates en su orden: el `quicksort` de NumPy ordena los trozos pequeños por inserción, que no adelanta a nadie. Con y sin `kind="stable"` el resultado es el mismo y el test pasa. Con 100 filas y muchos empates, `quicksort` desordena y el test falla. Un test con pocos datos puede pasar por casualidad: para probar una propiedad que solo se nota con tamaño (orden estable, rendimiento, desbordamientos), el test necesita ese tamaño.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños | El historial de `week-24` muestra un commit por paso (tests, dependencias, módulo, comando, versión, tests propios), sin cambiar los tests del bootcamp, y cada commit pasó por los ganchos | 8 |
| Rojo a verde | Leyó `test_frames.py` antes de escribir; puede decir qué tests pasaron a verde con cada paso, y qué le dijo Hypothesis si alguno falló | 8 |
| Ejecución en vivo | Ante el instructor: `filtrar` con sus datos y tres filtros distintos, el CSV de `-o` leído con `informe`, el comprobante de `sys.modules` y `pytest` en verde | 8 |
| Rompe y explica | Cambia `right=False` por `right=True` y explica qué valores cambian de nivel; quita `kind="stable"` y explica por qué solo falla un test | 8 |
| Explica sus decisiones | Explica por qué `Series.parse` y no `read_csv`, dónde gana pandas con sus números, el coste en la imagen y por qué `with_levels` devuelve una tabla nueva | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 23

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| La serie como tabla | `core/frames.py` con `frame_of` (columnas con tipo, también vacía, índice `position` desde 1); sin reexportar en `core/__init__.py` | 15 |
| Operaciones | `with_levels` con `pd.cut` y `right=False`, sin cambiar la tabla recibida; `select` con máscaras; `by_value` estable con NaN al final; `label_counts` con tipos de Python; `write_frame` que se puede volver a leer | 25 |
| El comando | `filtrar RUTA` con `-e` repetible, `--desde`, `--hasta`, `--ordenar`, `--filas` (`min=1`) y `-o`; import dentro del comando y `pd` en `TYPE_CHECKING`; `frame_text`; errores a stderr con código 1 o 2 | 15 |
| Tests propios | Al menos 6 tests en `tests/test_my_frames.py` con datos de su dominio, cada uno visto fallar con un mutante | 20 |
| Calidad | `pre-commit run --all-files`, `coverage report` y `alembic check` sin avisos; `docker compose run --rm app` en verde; CI en verde; `pandas==3.1.0` en las dependencias y `pandas-stubs` en `dev`; imágenes `week-24`; versión `0.24.0` | 10 |
| Git y README | Rama `week-24` en `python-<nombre>-<apellido>`; README con la sección "Filtrar" | 5 |
| Pull request | Salidas, CI, `filtrar` con sus datos y el CSV releído, tabla de tiempos, tamaño de la imagen y tabla de mutantes con las dos respuestas | 10 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | Semana 25 (próximamente) |
