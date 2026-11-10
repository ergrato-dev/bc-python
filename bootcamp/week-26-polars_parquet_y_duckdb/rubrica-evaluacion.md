# Rúbrica de Evaluación — Semana 26: Polars, Parquet y DuckDB

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 25 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | Nombra tres diferencias de diseño entre pandas y Polars. ¿Por qué `pl.DataFrame({"value": [1.0, "dos"]})` falla, y qué habría hecho pandas? | 10 |
| 2 | `values = pl.Series([1.0, None, float("nan")])`. ¿Qué dan `values.null_count()`, `values.is_nan().sum()` y `values.mean()`? ¿Qué es lo que falta en tu `columnar.frame_of`, y cómo lo cuentas? | 10 |
| 3 | ¿Qué devuelven `select`, `with_columns` y `filter`? `readings` tiene tres valores menores o iguales que 10 y una fila sin valor: ¿por qué `readings.filter(pl.col("value") <= 10)` deja tres filas y no cuatro? | 10 |
| 4 | ¿Qué hace `maintain_order=True` en `group_by`, y por qué hace falta en tu `summary`? ¿Qué pasa con las filas cuya clave es `null`, comparado con pandas? | 10 |
| 5 | ¿Qué diferencia hay entre `pl.read_parquet(ruta).filter(f)` y `pl.scan_parquet(ruta).filter(f).collect()`? En un plan, ¿qué significan `PROJECT 2/3 COLUMNS` y `SELECTION:` dentro de `Parquet SCAN`? | 10 |
| 6 | Un plan perezoso usa una columna `valor` que no existe. ¿Cuándo aparece el error? ¿Cómo lo descubres sin calcular ninguna fila? | 10 |
| 7 | ¿Por qué un Parquet ocupa menos que el CSV de los mismos datos y se lee más rápido? ¿Qué guarda su pie, y cómo le sirve a un filtro `value > 90` si el máximo de cada grupo es 80? | 10 |
| 8 | ¿Qué diferencia hay entre DuckDB y PostgreSQL? ¿Para qué usarías cada uno en tu Observatorio? | 10 |
| 9 | `station = "Norte' OR '1' = '1"`. ¿Qué cuenta `duckdb.sql(f"... WHERE station = '{station}'")`, y qué cuenta con `?`? ¿Por qué el nombre de la tabla de `query` sí va en una *f-string*? | 10 |
| 10 | ¿Por qué `query` copia el Parquet a una tabla **antes** de `SET enable_external_access = false`? ¿Qué pasa si se invierte el orden, y qué cuesta copiar? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. Tres de estas: Polars no tiene índice (las filas son posiciones); cada columna tiene un tipo fijo y un dato que no encaja es un error; lo que falta es `null` en cualquier tipo; usa todos los núcleos; puede ser perezoso y optimizar el plan; nunca cambia una tabla, siempre devuelve otra. El ejemplo falla porque `value` se crea como `Float64` y `"dos"` no es un número: `TypeError: unexpected value while building Series of type Float64`. pandas habría creado una columna `object` con un número y un texto, y el problema aparecería más tarde, lejos de su causa.
2. `null_count()` da 1 (el `None`); `is_nan().sum()` da 1 (el `NaN`: para el `None`, `is_nan` da `null`, que `sum` salta); `mean()` da `nan`, porque el `NaN` contagia la media y el `null` no cuenta. En `frame_of`, un `Measurement` sin valor es `null`, y se cuenta con `null_count()` o `is_null()`. Con `is_nan()` daría 0.
3. `select` da solo las columnas que pides; `with_columns`, las que había más las nuevas; `filter`, las filas donde la expresión es `True`. Comparar un `null` da `null`, no `True` ni `False`, y `filter` solo se queda con `True`: la fila sin valor no está ni en `<= 10` ni en `> 10`.
4. Deja los grupos en el orden en que aparece cada clave por primera vez, como `sort=False` en pandas. Sin él, Polars reparte los grupos entre núcleos y el orden cambia entre ejecuciones; tu `summary` debe dar las etiquetas en el orden del archivo, como `summaries.summary`. Las filas con clave `null` forman su propio grupo; pandas las quita sin avisar si no le dices `dropna=False`.
5. `read_parquet` lee el archivo entero a memoria y después filtra. `scan_parquet` devuelve un plan, y Polars empuja el filtro y la elección de columnas dentro de la lectura: lee solo las columnas y los grupos de filas que hacen falta. `PROJECT 2/3 COLUMNS` dice que lee 2 de las 3 columnas; `SELECTION:`, que filtra las filas mientras lee. Es el *pushdown*.
6. Al ejecutar el plan, con `collect()`: crearlo no comprueba nada. `collect_schema()` resuelve el plan y da el esquema del resultado, o el `ColumnNotFoundError`, sin calcular ninguna fila.
7. Guarda los números en binario y no como texto, y comprime cada columna por separado: una columna tiene datos parecidos (nombres que se repiten, fechas que suben) y se comprime mucho mejor que una fila. Se lee más rápido porque no hay texto que convertir y porque se leen solo las columnas pedidas. El pie guarda el esquema, dónde empieza cada bloque y las estadísticas de cada bloque (mínimo, máximo, nulos). Con `value > 90` y máximos de 80, quien lee sabe por el pie que ningún grupo puede tener esas filas, y no lee ninguno.
8. PostgreSQL es un servidor aparte, pensado para muchas escrituras pequeñas a la vez de muchos programas, con usuarios y transacciones. DuckDB es una biblioteca dentro de tu proceso, sin servidor, pensada para consultas de análisis sobre muchas filas, que lee Parquet y CSV directamente; solo un programa escribe a la vez. En el Observatorio, PostgreSQL guarda las cargas (`guardar`, `cargas`); DuckDB responde preguntas sobre los archivos exportados (`sql`).
9. Con la *f-string*, la comilla del texto cierra la de la consulta y `OR '1' = '1'` se ejecuta como SQL: cuenta todas las filas (8 en el ejercicio 03). Con `?`, el texto es un valor: ninguna estación se llama así, y cuenta 0. Los parámetros solo sirven para valores, no para nombres de tablas o columnas; `TABLE` es una constante del código, no algo que llegue de fuera, así que no hay nada que inyectar.
10. Porque `enable_external_access = false` corta **todo** acceso a archivos, incluido el tuyo: después ya no se podría leer el Parquet. Copiado antes, la tabla vive en memoria y sigue disponible. Al revés, `CREATE TABLE ... read_parquet(...)` falla con `PermissionException`. Copiar cuesta: con 100 000 medidas, unos 30 ms por llamada (14 en conectar, 8 en copiar, 3 en la consulta), frente a 3 ms preguntando al archivo directamente.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños | El historial de `week-26` muestra un commit por paso (tests, dependencias, módulo, comandos, versión, tests propios), sin cambiar los tests del bootcamp, y cada commit pasó por los ganchos | 8 |
| Rojo a verde | Leyó `test_columnar.py` antes de escribir; puede decir qué tests pasaron a verde con cada paso, y qué le dijo Hypothesis si alguno falló | 8 |
| Ejecución en vivo | Ante el instructor: `exportar` con sus datos, dos consultas `sql` con sentido en su dominio, una que intenta leer otro archivo, el comprobante de `sys.modules` y `pytest` en verde | 8 |
| Rompe y explica | Cambia `null_count()` por `is_nan().sum()` y explica qué test falla y por qué; mueve `SET enable_external_access` antes de `CREATE TABLE` y explica el error | 8 |
| Explica sus decisiones | Explica por qué `summary` recibe un `LazyFrame`, por qué Parquet entre Polars y DuckDB y no `pyarrow`, por qué `duckdb.Error`, y qué gana y cuesta cada biblioteca con sus números | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 25

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| Tabla y resumen | `frame_of` con esquema explícito y `null`; `summary` perezoso con `maintain_order`, `count` y `null_count`; sin reexportar `columnar` en `core/__init__.py` | 15 |
| SQL seguro | `query` con conexión en memoria, la ruta como parámetro `?`, la copia antes de `SET enable_external_access = false` y `duckdb.Error` sin atrapar dentro | 20 |
| Los comandos | `exportar RUTA PARQUET` que resume el archivo escrito y `sql PARQUET CONSULTA [-n]`; `rows_table` y `cell_text` con `NAMES`; `parsed`; imports dentro de los comandos; códigos 1 y 2 | 15 |
| Tests propios | Al menos 6 tests en `tests/test_my_columnar.py` con datos de su dominio, cada uno visto fallar con un mutante | 20 |
| Calidad | `pre-commit run --all-files`, `coverage report` y `alembic check` sin avisos; `docker compose run --rm app` en verde; CI en verde; `polars` y `duckdb` fijados; imágenes `week-26`; versión `0.26.0` | 10 |
| Git y README | Rama `week-26` en `python-<nombre>-<apellido>`; README con la sección "Parquet y SQL" | 5 |
| Pull request | Salidas, CI, `exportar` y dos consultas con sus datos, tabla de tiempos, tamaño de la imagen y tabla de mutantes con las dos respuestas | 15 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | [Semana 27](../week-27-visualizacion_con_matplotlib_seaborn_y_plotly/README.md) |
