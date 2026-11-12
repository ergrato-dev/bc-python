# Rúbrica de Evaluación — Semana 29: EDA, notebooks reproducibles y ETL desde PostgreSQL

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 28 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | `isna().sum()` dice que a `humedad` no le falta nada, y su media es 96,5 %. ¿Qué buscas, con qué función, y qué haces cuando lo encuentras? ¿Por qué una estación llamada "NA" puede desaparecer al leer un CSV? | 10 |
| 2 | En el ejercicio 01, la temperatura media de marzo sale 33,9 °C. ¿Cómo encontraste el problema, y por qué la regla de Tukey no lo detecta? | 10 |
| 3 | Tu notebook da "media 26.33" en tu pantalla y "media 13.17" en la máquina de tu compañero, con el mismo archivo. ¿Qué ha pasado, qué pista lo delata en el notebook y qué haces antes de cada commit para evitarlo? | 10 |
| 4 | ¿Qué guarda un `.ipynb` además del código? Da tres razones para no subir las salidas a Git, y di qué hace cada opción del gancho `notebook-outputs`. | 10 |
| 5 | Nombra los cinco ingredientes de un análisis reproducible y, para cada uno, qué ocurre si falta. | 10 |
| 6 | ¿Por qué tu notebook lee una instantánea y no la base de datos? ¿Qué hace su primera celda de código con la huella, y por qué `extraer` tiene que escribir el archivo byte a byte igual con los mismos datos? | 10 |
| 7 | ¿Por qué la celda de Colab usa `"google.colab" in sys.modules` y `subprocess.run`, y no una orden con `!` delante? ¿Qué test la vigila? | 10 |
| 8 | `extract` usa `dtype=TYPES` y `ORDER BY`. ¿Qué pasaría sin cada uno? ¿Por qué el test del orden hace un `UPDATE`? | 10 |
| 9 | ¿Qué es una inyección de SQL? Explica la salida "pegado: 200000 filas · parámetro: 0 filas". ¿Qué diferencia hay entre `to_sql` con `replace` y con `append` si el ETL se ejecuta cada día? | 10 |
| 10 | ¿Por qué JupyterLab va en un grupo `notebook` y en una etapa propia, y no en `dependencies`? ¿Por qué la etapa no desactiva el token, y por qué usa el UID 1000? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. Un **centinela**: un valor que significa "sin dato". Se ve en `describe()` (un máximo de 999) y en los extremos de `value_counts().sort_index()`. Se cambia por `NaN` con `replace(999, np.nan)`: así `isna()` lo cuenta y la media lo ignora (sube de 76,7 a 96,5 con él). `read_csv` convierte en `NaN`, por defecto, 19 textos, entre ellos "NA" y "null": una etiqueta "NA" pasa a ser un hueco. Con `keep_default_na=False` y `na_values={"valor": [""]}` solo una celda vacía de `valor` es un hueco.
2. Comparando grupos: `groupby("estacion")["temperatura"].describe()` da 65 de media en el Este frente a 16,5 y 21,4; con lo que sabes del dominio, son grados Fahrenheit (65 °F son 18,3 °C). El histograma de toda la tabla tenía dos montañas. Tukey usa los cuartiles de toda la tabla, y hay tantas medidas del Este que el tercer cuartil (62,5) sube hasta ellas: ninguna queda fuera de los límites. Ninguna regla conoce tus unidades.
3. **Estado oculto**: ejecutaste la celda que suma dos veces, y el kernel recuerda las dos; el archivo solo guarda el código. La pista son los contadores de ejecución: `[1]`, `[3]`, `[4]` en lugar de `[1]`, `[2]`, `[3]`. Antes de cada commit, *Kernel → Restart Kernel and Run All Cells*; y en el proyecto, `test_notebook_runs_top_to_bottom` lo ejecuta en un espacio de nombres vacío.
4. Salidas (texto, tablas, imágenes en base64), contadores de ejecución, metadatos de cada celda (la hora en que se ejecutó) y metadatos del notebook (el kernel). Razones: cada ejecución cambia el archivo y el diff es ilegible; el repositorio crece (de 2 432 a 48 855 bytes en el ejercicio 02); se pueden filtrar datos o rutas de tu máquina. `--clear-output` quita salidas y contadores; `ClearMetadataPreprocessor.enabled=True`, los metadatos de cada celda; `preserve_nb_metadata_mask=kernelspec` conserva el kernel para que JupyterLab sepa con cuál abrirlo.
5. **Datos** (una instantánea con huella; sin ella, otros datos), **código** (en Git sin salidas, de arriba abajo; sin él, estado oculto), **versiones** (`uv.lock` y la celda de Colab; sin ellas, otro pandas, otro resultado o un error), **azar** (semillas y nada de `datetime.now()`; sin ellos, otros números en cada ejecución), **entorno** (la misma imagen, rutas relativas; sin él, `FileNotFoundError` u otra zona horaria).
6. La base cambia cada vez que alguien guarda o borra una carga: el análisis daría otro resultado cada día y nadie sabría cuál era el bueno. La instantánea fija los datos; la celda compara `hashlib.sha256` de sus bytes con `EXPECTED` y, si no coincide, se para con `AssertionError` en lugar de calcular sobre otros datos. Si `extraer` escribiera otro orden, otro formato de número u otro fin de línea con los mismos datos, la huella cambiaría sin que cambiaran los datos, y el notebook se pararía en falso: por eso `ORDER BY`, `to_csv` sin índice y `lineterminator="\n"`.
7. `google.colab` solo está cargado dentro de Colab: en tu máquina, en Docker y en la CI, la celda no hace nada. `subprocess.run` es Python normal; `!` es sintaxis de IPython y rompería la ejecución sin Jupyter de `test_notebook_runs_top_to_bottom` (y `test_notebook_is_plain_python` la rechaza). `test_colab_cell_installs_the_pinned_versions` comprueba que cada `paquete==versión` de la celda está en las dependencias de `pyproject.toml`.
8. Sin `dtype`, una carga sin ningún valor llegaría con `value` de tipo `object` lleno de `None` (y una base vacía, sin tipos), y las medias del notebook fallarían o darían algo raro. Sin `ORDER BY`, PostgreSQL devuelve las filas en el orden en que están en disco: otro orden, otro CSV, otra huella. Un `UPDATE` escribe una copia nueva de la fila al final de la tabla, así que sin `ORDER BY` la primera medida sale la última: es la forma fiable de provocar ese desorden en un test (sin él, las filas recién insertadas salen casi siempre en orden y el mutante sobrevive).
9. Un valor que viene de fuera, pegado en el texto de la consulta, se convierte en SQL. Pegado, `Norte' OR '1'='1` da `WHERE station = 'Norte' OR '1'='1'`, verdad para las 200 000 filas; como parámetro (`:station`), PostgreSQL lo trata como un dato y ninguna estación se llama así: 0 filas. `replace` borra la tabla y la vuelve a crear: ejecutarlo cada día deja una copia del último resultado (idempotente). `append` añade: cada día duplica las filas.
10. JupyterLab no lo necesitan ni la CLI, ni la API, ni los tests: en `dependencies`, sus 78 paquetes entrarían en la imagen que despliegas, con sus avisos de seguridad; en `dev`, la CI los instalaría para nada. En un grupo propio solo se instala con `--group notebook`, y en una etapa propia `runtime` no cambia. El token: con `--ip 0.0.0.0`, sin token cualquiera que llegue al puerto ejecuta código en tu máquina; Jupyter inventa uno al arrancar (sin él, `403`). El UID 1000 es el de tu usuario en casi cualquier Linux o WSL: el volumen comparte `notebooks/` con sus permisos, y con otro UID JupyterLab no podría guardar.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños | El historial de `week-29` muestra un commit por paso (tests, módulo, comando, versión, instantánea, grupo, notebook, Docker, gancho, tests propios), sin cambiar los tests del bootcamp, y cada commit pasó por los ganchos | 8 |
| Rojo a verde | Leyó `test_etl.py` y `test_notebook.py` antes de escribir; puede decir qué tests pasaron a verde con cada paso, y por qué tres fallaban aún con el notebook escrito | 8 |
| Ejecución en vivo | Ante el instructor: `extraer` con su carga y la misma huella del notebook, JupyterLab en Docker con el token del registro, *Restart Kernel and Run All Cells*, `curl` sin token con `403` y `pytest` en verde | 8 |
| Rompe y explica | Borra una celda del notebook que define algo y enseña el `NameError` del test; quita el `ORDER BY` y explica qué test falla y por qué | 8 |
| Explica sus decisiones | Explica por qué una instantánea y no la base, por qué el grupo `notebook`, qué limpia el gancho y qué no comprueba el test que ejecuta el notebook | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 28

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| El ETL | `extract` con `ORDER BY`, el `WHERE` solo con carga y `dtype=TYPES`; `transform` con `with_levels` y las columnas en español; `write_snapshot` sin índice, con `\n` y la huella de los bytes escritos; sin reexportar `etl` en `core/__init__.py` | 15 |
| El comando | `extraer SALIDA [--carga N]` con el import dentro, código 1 con una carga que no existe o sin medidas (sin escribir nada), código 2 si no puede escribir, y las dos líneas del informe | 15 |
| El notebook | De tu dominio, con botón de Colab, la celda de versiones, la huella comprobada, un recorrido de EDA con un hallazgo por sección y `## Conclusiones` que dicen también lo que no responde; sin salidas; se ejecuta de arriba abajo | 25 |
| Tests propios | Al menos 6 tests en `tests/test_my_etl.py` con datos de su dominio, cada uno visto fallar con un mutante | 15 |
| JupyterLab y calidad | Grupo `notebook` fijado; etapa `notebook` entre `test` y `runtime` con UID sin privilegios y sin desactivar el token; servicio con perfil, volumen y `127.0.0.1`; gancho `notebook-outputs`; `pre-commit run --all-files`, `coverage report` y `alembic check` sin avisos; `docker compose run --rm app` y la CI en verde; versión `0.29.0` | 15 |
| Git y README | Rama `week-29` en `python-<nombre>-<apellido>`, `.ipynb_checkpoints/` en `.gitignore`; README con la sección "Explorar los datos" y tres hallazgos | 5 |
| Pull request | Salidas, CI, `extraer` con su huella, conclusiones, tamaño de las imágenes, los dos tiempos y la tabla de mutantes con las dos respuestas | 10 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | [Semana 30](../week-30-proyecto_de_fase_analisis_de_tu_dominio/README.md) |
