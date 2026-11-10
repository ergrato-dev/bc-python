# Semana 27 — Visualización con matplotlib, seaborn y plotly

> Hasta ahora tu Observatorio responde con tablas: buenas para leer un número, malas para ver qué sube, qué baja y dónde faltan datos. Esta semana aprendes a **dibujar** con las tres bibliotecas de gráficos que más se usan en Python: **matplotlib**, la base de casi todas, con sus figuras, ejes y artistas; **seaborn**, que encima de ella agrupa, calcula y colorea a partir de una tabla; y **plotly**, que dibuja en el navegador gráficos que se exploran con el ratón. Aprendes también a elegir el gráfico para cada pregunta y a no engañar con él. Tu Observatorio gana el comando `graficar`, que dibuja la evolución de tus medidas en PNG, SVG o PDF, sin `pyplot`, igual byte a byte cada vez y con tests que miran dentro del gráfico.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Dibujar** con matplotlib líneas, puntos, barras, histogramas, cajas y mapas de calor, sabiendo qué hacen `Figure`, `Axes` y cada artista
- **Elegir** el gráfico según la pregunta, y **evitar** los que engañan: barras recortadas, escalas distintas, paletas que no se leen
- **Describir** gráficos estadísticos con seaborn sobre tablas largas, y leer lo que calcula por ti
- **Hacer** gráficos interactivos con plotly, y decidir cuándo compensan
- **Llevar** los gráficos a un proyecto sin `pyplot`, con tests que miran los artistas y archivos reproducibles
- **Medir** lo que cuesta cada biblioteca en tiempo y en la imagen Docker, y elegir cuál entra en el proyecto

---

## 📋 Prerrequisitos

- [Semana 25](../week-25-pandas_groupby_merge_y_series_de_tiempo/README.md): `pivot`, `resample` y la tabla de `evolucion`.
- [Semana 26](../week-26-polars_parquet_y_duckdb/README.md): imports dentro de los comandos y el precio de una dependencia en la imagen.
- El *pull request* `week-26` de tu proyecto fusionado en `main`, con la CI en verde.

---

## 🗂️ Estructura de la Semana

```
week-27-visualizacion_con_matplotlib_seaborn_y_plotly/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 26 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
|---|---|---|
| [01 · matplotlib: figuras, ejes y artistas](1-teoria/01-matplotlib-figuras-ejes-y-artistas.md) | Para qué dibujar, `Figure`, `Axes` y artistas, los gráficos básicos, `NaN`, textos y leyenda, objetos frente a `pyplot`, *backends* y formatos | 50 min |
| [02 · Elegir el gráfico y contarlo bien](1-teoria/02-elegir-el-grafico-y-contarlo-bien.md) | Un gráfico por pregunta, cómo leemos, barras desde cero, *small multiples*, escala logarítmica, color y daltonismo, lo que falta | 45 min |
| [03 · seaborn: gráficos estadísticos](1-teoria/03-seaborn-graficos-estadisticos.md) | Una capa sobre matplotlib, datos largos, `hue`, intervalos de confianza, funciones de ejes y de figura, temas y una dependencia con poca actividad | 45 min |
| [04 · plotly: gráficos interactivos](1-teoria/04-plotly-graficos-interactivos.md) | Quién dibuja, plotly express, `data` y `layout`, HTML con y sin plotly.js, Kaleido, interactivo o estático | 45 min |
| [05 · Gráficos en un proyecto](1-teoria/05-graficos-en-un-proyecto.md) | `charts.py` y `evolution_of`, sin `pyplot`, tests que miran artistas, archivos reproducibles, `MPLCONFIGDIR`, el precio en la imagen y qué biblioteca entra | 55 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, ejecutas y comparas con la salida esperada. Preparan el proyecto. Las salidas coinciden con las del README salvo los tiempos; los gráficos van a `salida/`, y hay que abrirlos.

| Ejercicio | Qué haces | Duración |
|---|---|---|
| [01 · matplotlib: figuras y ejes](2-practicas/ejercicio-01-matplotlib-figuras-y-ejes/README.md) | Una línea y sus datos, lo que recuerda `pyplot`, cuatro gráficos para cuatro preguntas, textos y referencias, PNG, SVG y PDF | 1 h 30 min |
| [02 · Elegir el gráfico](2-practicas/ejercicio-02-elegir-el-grafico/README.md) | Barras recortadas, un panel por estación, un mapa de calor, cajas y escala logarítmica | 1 h 30 min |
| [03 · Gráficos con seaborn](2-practicas/ejercicio-03-graficos-con-seaborn/README.md) | Datos largos, líneas con su intervalo, distribuciones, paneles con `relplot`, temas y paletas | 1 h 30 min |
| [04 · plotly, y tres bibliotecas](2-practicas/ejercicio-04-plotly-y-tres-bibliotecas/README.md) | Un gráfico interactivo, su diccionario, el peso del HTML, paneles, y el mismo gráfico con las tres | 1 h 30 min |

### Proyecto

Añades a tu Observatorio:

- `core/charts.py`: `evolution_figure` (la tabla de la evolución, una línea por etiqueta, con `Figure` y sin `pyplot`) y `save` (el formato por la extensión, igual byte a byte con los mismos datos);
- `evolution_of`, que comparten `evolucion` y el comando nuevo;
- el comando `graficar RUTA SALIDA --inicio ... [--cada] [--periodo]`;
- `MPLCONFIGDIR` en la imagen `runtime`, para que matplotlib tenga dónde escribir.

Una dependencia nueva, `matplotlib==3.11.2`, cargada **solo** en `graficar`. 43 tests nuevos, uno con Hypothesis, que miran dentro de la figura en lugar de comparar píxeles. La versión sube a `0.27.0`. **Es el único entregable de la semana.**
→ [3-proyecto/README.md](3-proyecto/README.md)

---

## ⏱️ Distribución del Tiempo (18 horas)

| Actividad | Tiempo |
|---|---|
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
| Una figura sin `pyplot` | `from matplotlib.figure import Figure`; `figure = Figure()`; `axes = figure.add_subplot()` |
| Varios gráficos con la misma escala | `figure.subplots(5, 1, sharex=True, sharey=True)` |
| Que nada se pise | `Figure(layout="constrained")` |
| La leyenda fuera de los datos | `figure.legend(loc="outside right upper")` |
| Fechas legibles | `ConciseDateFormatter(axes.xaxis.get_major_locator())` |
| Un punto aislado entre `NaN` | `plot(..., marker="o")` |
| Los datos de una línea | `line.get_xdata()`, `line.get_ydata()` |
| Texto buscable en un SVG | `rc_context({"svg.fonttype": "none"})` |
| Un SVG igual dos veces | `svg.hashsalt` y `savefig(..., metadata={"Date": None})` |
| Ancha a larga | `frame.melt(id_vars="time", var_name="station", value_name="value")` |
| seaborn en tus ejes | `sns.lineplot(..., ax=axes)` |
| Un HTML pequeño con plotly | `figure.write_html("g.html", include_plotlyjs="cdn")` |
| matplotlib en Docker sin avisos | `ENV MPLCONFIGDIR=/tmp/matplotlib` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-27` de `python-<nombre>-<apellido>` con:
   - `core/charts.py` sin reexportar en `core/__init__.py` y sin `pyplot`, `evolution_of` y el comando `graficar`, con matplotlib importado dentro;
   - `matplotlib==3.11.2` en las dependencias, las imágenes `week-27` en `compose.yaml` y `MPLCONFIGDIR` en el `Dockerfile`;
   - la versión `0.27.0` y al menos 6 tests propios en `tests/test_my_charts.py`.

   Todo en verde en tu máquina, en Docker y en GitHub Actions.
2. ✅ `README.md` del repositorio con la sección "Gráficos" y una imagen
3. ✅ Pull request `week-27` → `main` con:
   - las salidas de los ganchos, la cobertura, `alembic check` y la CI en verde;
   - un gráfico de `graficar` con tus datos;
   - tu tabla de tiempos, el tamaño de tu imagen y la tabla de mutantes con las dos respuestas del paso 10.

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
uv run observatorio graficar medidas.txt evolucion.svg --inicio 2026-11-01T08:00:00 --periodo 2h
uv run observatorio graficar medidas.txt evolucion.txt --inicio 2026-11-01T08:00:00
uv run python -c "import sys, observatorio.cli; print('matplotlib' in sys.modules)"
docker compose build app api && docker compose run --rm app
gh pr checks
```

Lo que debes ver:

- todos los ganchos en `Passed` (o `Skipped`);
- los tests terminan en `passed` sin `failed`, al menos 1108;
- `coverage report` termina sin `Coverage failure`;
- `alembic check` dice `No new upgrade operations detected.`;
- `--version` escribe `observatorio 0.27.0`;
- el primer `graficar` escribe la línea mala en stderr y `N etiquetas y M periodos de K medidas en evolucion.svg · B bytes`, con código 1 por esa línea; el SVG se abre en el navegador, y al repetir el comando sale igual byte a byte;
- el segundo, `error: no se puede escribir evolucion.txt: Format 'txt' is not supported ...` y código 2;
- la comprobación de `sys.modules` escribe `False`;
- `gh pr checks` con `quality`, `tests` e `image` en `pass`.

En los ejercicios, cada paso descomentado da la salida que muestra su README; los tiempos, los de tu máquina.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 26](../week-26-polars_parquet_y_duckdb/README.md) | **Semana 27** | Semana 28 (próximamente) |
