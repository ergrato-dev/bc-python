# Rúbrica de Evaluación — Semana 25: pandas II

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 24 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | El Sur tiene tres filas en `readings`, una con `value` NaN, y otra fila no tiene estación. ¿Qué dan `count` y `size` para el Sur en `groupby("station")["value"].agg(["count", "size"])`? ¿En qué grupo está la fila sin estación? | 10 |
| 2 | ¿En qué orden salen los grupos de un `groupby`, y qué cambia `sort=False`? ¿Por qué el test que compara `summary` con `Series.means` compara diccionarios y no listas? | 10 |
| 3 | ¿Qué diferencia hay entre `groupby("station")["value"].agg("mean")` y `.transform("mean")`? Escribe cómo calcularías cuánto se aparta cada medida de la media de su estación | 10 |
| 4 | `monday` tiene medidas de Norte, Sur y Oeste; `stations`, la región de Norte, Sur y Centro. ¿Qué filas da `monday.merge(stations, on="station")`? ¿Qué `how` usarías para no perder ninguna medida, y qué tipo tendrá después la columna `altitude`, que era `int64`? | 10 |
| 5 | Norte está dos veces en `stations` y tiene dos medidas. ¿Cuántas filas de Norte salen del `merge`? ¿Cómo lo detectas, y qué `validate` usa `compare` en tu proyecto? | 10 |
| 6 | ¿Por qué `pivot` puede lanzar `ValueError: Index contains duplicate entries, cannot reshape`, y qué usas en su lugar? Una tabla ancha de 3 días × 3 estaciones tiene 6 celdas con valor: ¿cuántas filas da `melt`? | 10 |
| 7 | ¿Qué fecha da `pd.to_datetime("03/11/2026")`? ¿Cómo lees bien una columna de fechas día/mes/año con una fila que dice `ayer`, y por qué no te fías de `parse_dates` en `read_csv`? | 10 |
| 8 | Una serie de Norte tiene medidas a las 8:00, 11:00 y 20:00 del día 1. ¿Qué periodos da `resample("6h").mean()`, y qué valor tiene el de las 12:00? ¿Qué cambia `origin="start"`? | 10 |
| 9 | Con medidas a intervalos irregulares, ¿por qué `rolling("6h")` y no `rolling(3)`? ¿Por qué `duration("1M")` falla y `duration("30D")` no, y por qué `duration("")` necesita su propia comprobación? | 10 |
| 10 | ¿Por qué `test_evolution_known_values` no mata el mutante que cambia `.mean()` por `.median()` en `evolution`, y quién lo mata? ¿Qué te dice eso de los datos de un test? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. `count` cuenta los **valores**: 2 (el NaN no cuenta). `size` cuenta las **filas**: 3. La resta, 1, son los que faltan: la columna `missing` de `summary`. La fila sin estación no está en **ningún** grupo: `groupby` quita las filas cuya clave es NaN sin avisar. Con `dropna=False` aparece un grupo `nan`.
2. Por defecto, ordenados por la clave. Con `sort=False`, en el orden en que aparece cada clave por primera vez, como hace tu `summary` para seguir el orden del archivo. El test compara diccionarios porque `Series.means` ordena por el primer **valor** de cada etiqueta y `summary` por la primera **aparición**, tenga valor o no: con `[Norte sin valor, Sur 0.0, Norte 0.0]`, uno da Sur, Norte y el otro Norte, Sur. Las medias son las mismas; el orden no es un error del código.
3. `agg` da **una fila por grupo**: una `Series` con la estación como índice. `transform` da **una fila por fila** de la tabla original, con su índice: cada medida recibe la media de su grupo. Por eso se puede restar directamente: `readings["value"] - readings.groupby("station")["value"].transform("mean")`.
4. Sin `how`, `merge` usa `inner`: solo Norte y Sur, las que están en las dos. Oeste desaparece sin aviso. Con `how="left"` salen las tres medidas, y Oeste tiene `region` y `altitude` en NaN. `altitude` pasa a `float64`, porque NaN solo cabe en una columna de coma flotante.
5. Cada medida de Norte se cruza con las dos filas de Norte: 2 × 2 = 4 filas, sin error. Se detecta con `validate`: aquí `"many_to_one"` (muchas medidas por estación, una fila por estación), que lanza `MergeError: Merge keys are not unique in right dataset; not a many-to-one merge`. `compare` usa `"one_to_one"`: cada resumen tiene una fila por etiqueta.
6. Porque dos filas tienen el mismo índice y la misma columna (Norte, el lunes, dos veces) y `pivot` no sabe cuál poner en la celda. `pivot_table` las junta con un `aggfunc` (la media, si no dices otro). `melt` da una fila por **celda**, también las vacías: 3 × 3 = 9 filas, tres con NaN; `dropna()` deja las 6.
7. `2026-03-11`: sin formato, pandas lee mes/día. Bien: `pd.to_datetime(columna, format="%d/%m/%Y %H:%M", errors="coerce")`, que convierte `ayer` en `NaT`; después buscas las `NaT` para saber cuáles eran. `parse_dates` con `date_format` deja la columna **entera** como texto si una fila no encaja, sin error ni aviso: lees como texto y conviertes con `to_datetime`, donde el problema se ve.
8. Los periodos se cuentan desde la medianoche: el de las 6:00 (de 6:00 a 12:00, sin incluir las 12:00) tiene las de las 8:00 y las 11:00, y da su media; el de las 12:00 no tiene ninguna; el de las 18:00 tiene la de las 20:00. El de las 12:00 sale aunque esté vacío, con NaN: `resample` saca todos los periodos entre la primera medida y la última. Con `origin="start"` los periodos empiezan en la primera medida: 8:00, 14:00 y 20:00.
9. `rolling(3)` mezcla las tres últimas **filas**, aunque estén separadas por horas o días. `rolling("6h")` usa las filas de las últimas **6 horas**, sean cuantas sean. `pd.Timedelta("1M")` falla porque un mes no es una duración fija (28 a 31 días); `"30D"` sí lo es. `pd.Timedelta("")` no lanza: devuelve `NaT`, y `NaT <= pd.Timedelta(0)` es `False`, así que sin `pd.isna(value)` `duration` devolvería `NaT` y `date_range` fallaría más tarde con un error poco claro.
10. Porque en sus datos cada etiqueta tiene **un** valor por periodo, o dos (como `A;1` y `A;3` en los tests de `evolucion`): con uno o dos números, la media y la mediana coinciden. Lo mata `test_evolution_in_one_period_gives_the_means_of_summary`: Hypothesis mete muchas medidas en un solo día y compara con las medias de `summary`. Los datos de un test tienen que poder distinguir el código bueno del malo: si con ellos dan lo mismo, el test no prueba esa línea.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños | El historial de `week-25` muestra un commit por paso (tests, módulo, nombres en español, comandos, versión, tests propios), sin cambiar los tests del bootcamp, y cada commit pasó por los ganchos | 8 |
| Rojo a verde | Leyó `test_summaries.py` antes de escribir; puede decir qué tests pasaron a verde con cada paso, y qué le dijo Hypothesis si alguno falló | 8 |
| Ejecución en vivo | Ante el instructor: `resumir` con sus datos, `resumir --contra` con dos archivos suyos, `evolucion` con dos periodos distintos, el comprobante de `sys.modules` y `pytest` en verde | 8 |
| Rompe y explica | Quita `validate` y explica qué test falla y por qué; cambia `.mean()` por `.median()` y explica por qué solo lo mata Hypothesis | 8 |
| Explica sus decisiones | Explica por qué `count` y `size`, por qué `outer` en `compare`, dónde empiezan los periodos de `resample`, por qué `timed` supone una medida cada `--cada` y qué gana pandas con sus números | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 24

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| Resumen y comparación | `summary` con agregación con nombre, `sort=False` y `missing`; `compare` con `outer` y `validate="one_to_one"`; sin reexportar `summaries` en `core/__init__.py` | 15 |
| Tiempo | `duration` que rechaza lo que no es una duración mayor que cero con un solo mensaje; `timed` con `date_range`; `evolution` con `pivot` y `resample` | 20 |
| Los comandos | `resumir RUTA [-c OTRA]` y `evolucion RUTA --inicio [--cada] [--periodo] [-n]`; `NAMES` y `frame_text` para todas las tablas; `parsed` con el nombre del archivo en los errores; import dentro de los comandos; códigos 1 y 2 | 15 |
| Tests propios | Al menos 6 tests en `tests/test_my_summaries.py` con datos de su dominio, cada uno visto fallar con un mutante | 20 |
| Calidad | `pre-commit run --all-files`, `coverage report` y `alembic check` sin avisos; `docker compose run --rm app` en verde; CI en verde; imágenes `week-25`; versión `0.25.0` | 10 |
| Git y README | Rama `week-25` en `python-<nombre>-<apellido>`; README con la sección "Resumir y evolución" | 5 |
| Pull request | Salidas, CI, los dos comandos con sus datos, tabla de tiempos y tabla de mutantes con las dos respuestas | 15 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | [Semana 26](../week-26-polars_parquet_y_duckdb/README.md) |
