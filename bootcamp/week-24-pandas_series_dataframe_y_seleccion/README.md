# Semana 24 — pandas I: Series, DataFrame y selección

> En la semana 23 guardabas los valores en un array y las etiquetas en otro, y cuidabas de que no se desordenaran. pandas los junta: una **tabla** con un índice para las filas y columnas con nombre, cada una de su tipo. Esta semana aprendes las dos piezas, `Series` y `DataFrame`; a leer un CSV sin perder datos por el camino; a **elegir** filas y columnas por etiqueta, por posición y con máscaras; a ordenar y contar; y a entender *copy-on-write*, la regla de pandas 3 que hace que una selección nunca cambie la tabla de la que sale. Tu Observatorio gana un comando, `filtrar`, que responde preguntas como "¿qué medidas de Norte y Sur pasan de 9, de mayor a menor?" y guarda la respuesta en un CSV.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Crear** `Series` y `DataFrame`, y **leer** su índice, sus columnas y sus tipos, también con datos que faltan
- **Prever** qué da una operación entre dos `Series` con índices distintos
- **Leer** un CSV con `read_csv` eligiendo separador, decimal y datos que faltan, y **mirar** la tabla antes de usarla
- **Elegir** filas y columnas con `.loc`, `.iloc`, máscaras y `query`, sabiendo dónde acaba cada corte y qué pasa con los NaN
- **Ordenar**, **contar** y **categorizar** con `sort_values`, `value_counts` y `pd.cut`
- **Explicar** *copy-on-write* y **escribir** funciones que devuelven una tabla nueva
- **Llevar** pandas a un proyecto con `pandas-stubs`, tests con `pandas.testing` y una importación que solo paga quien la usa

---

## 📋 Prerrequisitos

- [Semana 23](../week-23-numpy_arrays_broadcasting_y_estadistica/README.md): NumPy, sobre todo máscaras, NaN y la teoría 05.
- El *pull request* `week-23` de tu proyecto fusionado en `main`, con la CI en verde.

---

## 🗂️ Estructura de la Semana

```
week-24-pandas_series_dataframe_y_seleccion/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 23 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · Series: índice, tipos y alineación](1-teoria/01-series-indice-tipos-y-alineacion.md) | De NumPy a pandas, valores e índice, tipos y `Int64`, `loc` e `iloc`, alineación por índice, NaN y texto | 45 min |
| [02 · DataFrames: crear, leer y mirar](1-teoria/02-dataframes-crear-leer-y-mirar.md) | Una tabla de `Series`, crearla con tipos, `read_csv` y sus trampas, una fila mala, `info` y `describe`, columnas y `to_csv` | 50 min |
| [03 · Seleccionar: loc, iloc y máscaras](1-teoria/03-seleccionar-loc-iloc-y-mascaras.md) | Etiqueta y posición, máscaras con `&`, `\|`, `~`, `isin` y `between`, NaN en un filtro, `query`, otro índice y cambiar valores | 50 min |
| [04 · Ordenar, contar y copy-on-write](1-teoria/04-ordenar-contar-y-copy-on-write.md) | `sort_values` y empates, `value_counts`, `pd.cut` y sus bordes, *copy-on-write* y funciones que no cambian lo que reciben | 45 min |
| [05 · pandas en un proyecto](1-teoria/05-pandas-en-un-proyecto.md) | `pandas-stubs` y mypy, tipos de Python en la frontera, `pandas.testing`, importar solo donde hace falta, `read_csv` o tu lector y dónde gana | 50 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, ejecutas y comparas con la salida esperada. Preparan el proyecto. Las salidas coinciden con las del README salvo los tiempos del ejercicio 04.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · Series, índice y tipos](2-practicas/ejercicio-01-series-indice-y-tipos/README.md) | Crear `Series`, ver qué tipo sale, sumar por etiqueta, la trampa del índice de enteros, NaN y texto | 1 h 30 min |
| [02 · DataFrames: leer y mirar](2-practicas/ejercicio-02-dataframes-leer-y-mirar/README.md) | Crear una tabla, leer un CSV sin perder a Namibia, `info` y `describe`, columnas nuevas, una fila mala y escribir | 1 h 30 min |
| [03 · Seleccionar con loc, iloc y máscaras](2-practicas/ejercicio-03-seleccionar-con-loc-iloc-y-mascaras/README.md) | `loc` e `iloc`, máscaras con NaN, `query`, otro índice, ordenar con empates y la asignación encadenada | 1 h 30 min |
| [04 · De Python a pandas](2-practicas/ejercicio-04-de-python-a-pandas/README.md) | De objetos a tabla, niveles con `pd.cut`, contar como `Counter`, tipos de Python, tiempos y memoria | 1 h 30 min |

### Proyecto

Añades a tu Observatorio:

- `pandas==3.1.0` como dependencia de producción y `pandas-stubs` como de desarrollo;
- `core/frames.py`: la serie como `DataFrame` y, sobre ella, `with_levels` con `pd.cut`, `select`, `by_value`, `label_counts` y `write_frame`;
- el comando `filtrar RUTA [-e ETIQUETA]... [--desde X] [--hasta Y] [--ordenar] [-n FILAS] [-o CSV]`, que escribe las medidas elegidas con su nivel y puede guardarlas en un CSV que el Observatorio vuelve a leer.

pandas se importa **solo** en ese comando, como NumPy en `estadisticas`, y un test lo vigila. Mides dónde gana pandas y cuánto cuesta convertir. 51 tests nuevos, cinco con Hypothesis que comparan lo nuevo con lo que ya tenías. La versión sube a `0.24.0`. **Es el único entregable de la semana.**
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
| Probar algo de pandas al vuelo | `uv run python` y `import pandas as pd` (en el proyecto o en un ejercicio) |
| ¿Qué tipo tiene cada columna? | `df.dtypes` o `df.info()` |
| ¿Cuántos faltan en cada columna? | `df.isna().sum()` |
| Leer un CSV español | `pd.read_csv(ruta, sep=";", decimal=",")` |
| Que `NA` no desaparezca de una columna de códigos | `keep_default_na=False, na_values={"valor": ["NA"]}` |
| Encontrar las celdas que no son números | `df[pd.to_numeric(df["valor"], errors="coerce").isna()]` |
| Ver todas las filas al imprimir | `pd.set_option("display.max_rows", None)` |
| La primera fila, sin dudas | `df.iloc[0]` |
| Cambiar valores de unas filas | `df.loc[máscara, "columna"] = valor` |
| Comparar tablas en un test | `pd.testing.assert_frame_equal(actual, esperada)` |
| ¿Importa pandas este módulo? | `uv run python -c "import sys, observatorio.cli; print('pandas' in sys.modules)"` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-24` de `python-<nombre>-<apellido>` con:
   - `core/frames.py` sin reexportar en `core/__init__.py`, y el comando `filtrar` con pandas importado dentro;
   - `pandas==3.1.0` en las dependencias, `pandas-stubs==3.1.0.261029` en `dev`, las imágenes `week-24` en `compose.yaml`;
   - la versión `0.24.0` y al menos 6 tests propios en `tests/test_my_frames.py`.

   Todo en verde en tu máquina, en Docker y en GitHub Actions.
2. ✅ `README.md` del repositorio con la sección "Filtrar"
3. ✅ Pull request `week-24` → `main` con:
   - las salidas de los ganchos, la cobertura, `alembic check` y la CI en verde;
   - `filtrar` con tus datos respondiendo preguntas de tu dominio, y el CSV de `-o` leído con `informe`;
   - tu tabla de tiempos, el tamaño de la imagen y la tabla de mutantes con las dos respuestas del paso 12.

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
uv run observatorio filtrar -e <una etiqueta tuya> --ordenar medidas.txt
uv run python -c "import sys, observatorio.cli; print('pandas' in sys.modules)"
docker compose build app api && docker compose run --rm app
gh pr checks
```

Lo que debes ver:

- todos los ganchos en `Passed` (o `Skipped`);
- los tests terminan en `passed` sin `failed`, al menos 948;
- `coverage report` termina sin `Coverage failure`;
- `alembic check` dice `No new upgrade operations detected.`;
- `--version` escribe `observatorio 0.24.0`;
- `filtrar` escribe las medidas de esa etiqueta de mayor a menor, con su nivel, y la línea `N de M medidas`;
- la comprobación de `sys.modules` escribe `False`;
- `gh pr checks` con `quality`, `tests` e `image` en `pass`.

En los ejercicios, cada paso descomentado da la salida que muestra su README; los tiempos, los de tu máquina.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 23](../week-23-numpy_arrays_broadcasting_y_estadistica/README.md) | **Semana 24** | [Semana 25](../week-25-pandas_groupby_merge_y_series_de_tiempo/README.md) |
