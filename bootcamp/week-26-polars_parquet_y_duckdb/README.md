# Semana 26 — Polars, Parquet y DuckDB

> En las semanas 24 y 25 aprendiste pandas. Ahora conoces las otras dos herramientas que usa hoy el análisis de datos en Python: **Polars**, una biblioteca de tablas en Rust, estricta con los tipos, que usa todos tus núcleos y planea la consulta antes de ejecutarla; y **DuckDB**, una base de datos SQL que vive dentro de tu programa. Entre las dos, **Parquet**: un formato de archivo por columnas que guarda los tipos y ocupa la cuarta parte que un CSV. Tu Observatorio gana dos comandos: `exportar`, que guarda tus medidas en Parquet, y `sql`, que les pregunta lo que quieras sin volver a leer el texto, y sin dejar que ese SQL toque ningún otro archivo.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Escribir** con Polars lo que ya sabes hacer con pandas: expresiones en `select`, `with_columns`, `filter` y `group_by`, `over` y `join`
- **Distinguir** `null` de `NaN`, y saber qué hace cada operación con los dos
- **Planear** consultas con `LazyFrame`, leer su plan y reconocer el *pushdown* de filtros y columnas
- **Explicar** cómo es un Parquet por dentro y qué conserva que un CSV pierde, y **particionar** una tabla en carpetas
- **Consultar** con DuckDB archivos Parquet y CSV y tablas de pandas, con parámetros `?` y sin servidor
- **Ejecutar** SQL que escribe otra persona sin darle acceso a tus archivos
- **Llevar** todo a un proyecto sin `pyarrow`, con tests que comparan tres bibliotecas, y **medir** qué gana y qué cuesta cada una

---

## 📋 Prerrequisitos

- [Semana 25](../week-25-pandas_groupby_merge_y_series_de_tiempo/README.md): `groupby`, `merge` y la agregación con nombre.
- [Semana 19](../week-19-postgresql_psycopg_sqlalchemy_y_alembic/README.md): SQL, `GROUP BY` e inyección de SQL.
- El *pull request* `week-25` de tu proyecto fusionado en `main`, con la CI en verde.

---

## 🗂️ Estructura de la Semana

```
week-26-polars_parquet_y_duckdb/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 25 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · Polars: expresiones y contextos](1-teoria/01-polars-expresiones-y-contextos.md) | Polars frente a pandas, tipos estrictos, `null` y `NaN`, expresiones, `when`, los cuatro contextos, `over`, `join` y la tabla de traducción | 50 min |
| [02 · Evaluación perezosa](1-teoria/02-evaluacion-perezosa.md) | `LazyFrame`, `scan_*` y `collect`, leer un plan, *pushdown*, errores y `collect_schema`, `streaming` y `sink_parquet` | 45 min |
| [03 · Parquet: un formato por columnas](1-teoria/03-parquet-un-formato-por-columnas.md) | Filas o columnas, *row groups*, bloques, estadísticas y pie, compresión, qué conserva, particionado *hive* | 45 min |
| [04 · DuckDB: SQL sin servidor](1-teoria/04-duckdb-sql-sin-servidor.md) | DuckDB frente a PostgreSQL, SQL sobre archivos y tablas de Python, la API, parámetros, bases en archivo, `enable_external_access` y sus errores | 45 min |
| [05 · Polars, Parquet y DuckDB en un proyecto](1-teoria/05-polars-parquet-y-duckdb-en-un-proyecto.md) | Dónde vive cada pieza, Parquet como puente sin `pyarrow`, probar tres bibliotecas, SQL ajeno, medir, el precio en la imagen y cuál elegir | 55 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, ejecutas y comparas con la salida esperada. Preparan el proyecto. Las salidas coinciden con las del README salvo los tiempos.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · Polars: expresiones y contextos](2-practicas/ejercicio-01-polars-expresiones-y-contextos/README.md) | Una tabla sin índice, `null` y `NaN`, expresiones, `filter`, `group_by`, `over`, `join` y Polars frente a pandas | 1 h 30 min |
| [02 · Evaluación perezosa y Parquet](2-practicas/ejercicio-02-evaluacion-perezosa-y-parquet/README.md) | Planes y `explain`, CSV frente a Parquet con tres compresiones, tipos, `scan_parquet` y particiones | 1 h 30 min |
| [03 · SQL con DuckDB](2-practicas/ejercicio-03-sql-con-duckdb/README.md) | SQL sobre Parquet y CSV, tablas de pandas, parámetros e inyección, una base en archivo y una conexión sin disco | 1 h 30 min |
| [04 · Una pregunta, tres herramientas](2-practicas/ejercicio-04-una-pregunta-tres-herramientas/README.md) | El CSV del Observatorio con Polars, una fila mala, `sink_parquet`, y la misma pregunta con pandas, Polars y DuckDB | 1 h 30 min |

### Proyecto

Añades a tu Observatorio:

- `core/columnar.py`: `frame_of` (la serie en Polars), `summary` (el resumen de la semana 25, perezoso) y `query` (SQL de DuckDB sobre un Parquet, sin acceso a otros archivos);
- el comando `exportar RUTA PARQUET`, que guarda las medidas y resume el archivo escrito;
- el comando `sql PARQUET CONSULTA [-n FILAS]`, que ejecuta tu SQL sobre la tabla `medidas`;
- `rows_table`, que escribe cualquier resultado de Polars o DuckDB con los nombres de `NAMES`.

Dos dependencias nuevas, `polars==2.1.0` y `duckdb==2.0.0`, cargadas **solo** en los comandos que las usan. 46 tests nuevos, cuatro con Hypothesis: Polars frente a pandas, DuckDB frente a Polars y la ida y vuelta por Parquet. La versión sube a `0.26.0`. **Es el único entregable de la semana.**
→ [3-proyecto/README.md](3-proyecto/README.md)

---

## ⏱️ Distribución del Tiempo (18 horas)

| Actividad | Tiempo |
| --------- | ------ |
| Teoría (5 archivos) | 4 h |
| Ejercicio 01 | 1 h 30 min |
| Ejercicio 02 | 1 h 30 min |
| Ejercicio 03 | 1 h 30 min |
| Ejercicio 04 | 1 h 30 min |
| Proyecto | 6 h 30 min |
| Recursos y glosario | 30 min |
| Autoevaluación (cuestionario de la rúbrica) | 1 h |
| **Total** | **18 h** |

---

## 🎩 Trucos y atajos

| Truco | Cómo |
|---|---|
| Ver el esquema de un plan sin ejecutarlo | `plan.collect_schema()` |
| ¿Qué lee de verdad mi consulta? | `plan.explain()`, y busca `PROJECT` y `SELECTION` dentro del `SCAN` |
| Grupos en orden de aparición | `group_by("k", maintain_order=True)` |
| La media de su grupo en cada fila | `pl.col("v").mean().over("k")` |
| Contar lo que falta en Polars | `pl.col("v").null_count()`, nunca `is_nan()` |
| CSV a Parquet sin cargarlo en memoria | `pl.scan_csv(...).sink_parquet("salida.parquet")` |
| Mirar las primeras filas de un Parquet | `uv run observatorio sql medidas.parquet "FROM medidas LIMIT 5"` |
| El pie de un Parquet | `duckdb.sql("FROM parquet_metadata('medidas.parquet')")` |
| Leer el CSV del Observatorio | Polars: `separator=";", decimal_comma=True, null_values="NA"`; DuckDB: `delim = ';', decimal_separator = ',', nullstr = 'NA'` |
| Agrupar sin repetir columnas en SQL | `GROUP BY ALL` |
| Valores que vienen de fuera | `duckdb.execute("... WHERE station = ?", [station])` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-26` de `python-<nombre>-<apellido>` con:
   - `core/columnar.py` sin reexportar en `core/__init__.py`, y los comandos `exportar` y `sql` con Polars y DuckDB importados dentro;
   - `polars==2.1.0` y `duckdb==2.0.0` en las dependencias, y las imágenes `week-26` en `compose.yaml`;
   - la versión `0.26.0` y al menos 6 tests propios en `tests/test_my_columnar.py`.

   Todo en verde en tu máquina, en Docker y en GitHub Actions.
2. ✅ `README.md` del repositorio con la sección "Parquet y SQL"
3. ✅ Pull request `week-26` → `main` con:
   - las salidas de los ganchos, la cobertura, `alembic check` y la CI en verde;
   - `exportar` y dos consultas `sql` con tus datos;
   - tu tabla de tiempos, el tamaño de tu imagen y la tabla de mutantes con las dos respuestas del paso 12.

El cuestionario de la [rúbrica](rubrica-evaluacion.md) es tu autoevaluación: respóndelo antes de mirar las respuestas.

---

## ✅ Verificación

En tu proyecto:

```bash
docker compose up -d --wait db
uv run pre-commit run --all-files
uv run pytest
uv run coverage run -m pytest -q && uv run coverage report
uv run alembic check
uv run observatorio --version
uv run observatorio exportar medidas.txt medidas.parquet
uv run observatorio sql medidas.parquet "SELECT label, avg(value) AS mean FROM medidas GROUP BY label"
uv run observatorio sql medidas.parquet "SELECT * FROM 'medidas.csv'"
uv run python -c "import sys, observatorio.cli; print('polars' in sys.modules, 'duckdb' in sys.modules)"
docker compose build app api && docker compose run --rm app
gh pr checks
```

Lo que debes ver:

- todos los ganchos en `Passed` (o `Skipped`);
- los tests terminan en `passed` sin `failed`, al menos 1058;
- `coverage report` termina sin `Coverage failure`;
- `alembic check` dice `No new upgrade operations detected.`;
- `--version` escribe `observatorio 0.26.0`;
- `exportar` escribe una fila por etiqueta con `medidas`, `faltan`, `media`, `mínimo` y `máximo`, y la línea `N medidas en medidas.parquet · B bytes`;
- la primera consulta `sql`, una fila por etiqueta con `etiqueta` y `media`, y la línea `N filas`;
- la segunda, `error: Permission Error: Cannot access file "medidas.csv" ...` y código 2;
- la comprobación de `sys.modules` escribe `False False`;
- `gh pr checks` con `quality`, `tests` e `image` en `pass`.

En los ejercicios, cada paso descomentado da la salida que muestra su README; los tiempos, los de tu máquina.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 25](../week-25-pandas_groupby_merge_y_series_de_tiempo/README.md) | **Semana 26** | [Semana 27](../week-27-visualizacion_con_matplotlib_seaborn_y_plotly/README.md) |
