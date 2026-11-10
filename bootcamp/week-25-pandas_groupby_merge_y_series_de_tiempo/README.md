# Semana 25 — pandas II: groupby, merge y series de tiempo

> En la semana 24 aprendiste a elegir filas de una tabla. Ahora toca **resumirlas** y **juntarlas**: una media por estación sin escribir un bucle, las medidas de hoy cruzadas con las de ayer, la misma tabla en formato largo para calcular y ancho para leer, y medidas con fecha y hora agrupadas por periodos. Son las cuatro operaciones que más vas a escribir en análisis de datos: `groupby`, `merge`, `pivot` y `resample`. Tu Observatorio gana dos comandos: `resumir`, que da una fila por etiqueta y compara dos archivos, y `evolucion`, que muestra la media de cada etiqueta hora a hora o día a día.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Resumir** una tabla por grupos con `groupby` y `agg`, distinguiendo `count` de `size` y sabiendo qué pasa con las claves que faltan
- **Devolver** un resultado por fila con `transform`, y **quitar** grupos con `filter`
- **Apilar** tablas con `concat` y **cruzarlas** con `merge` y `join`, eligiendo `how` y protegiéndote de claves repetidas con `validate`
- **Pasar** de formato largo a ancho y vuelta con `pivot`, `pivot_table` y `melt`, y **contar** combinaciones con `crosstab`
- **Convertir** texto en fechas sin confundir el día con el mes, y **elegir** por día o por intervalo con un índice de tiempo
- **Agrupar** por periodos con `resample`, sabiendo dónde empieza cada uno, y **calcular** medias móviles con `rolling`
- **Llevar** todo a un proyecto con tipos que mypy entiende, tests que vigilan el orden y los tipos, y duraciones escritas por una persona

---

## 📋 Prerrequisitos

- [Semana 24](../week-24-pandas_series_dataframe_y_seleccion/README.md): `Series`, `DataFrame`, `loc` e `iloc`, máscaras y *copy-on-write*.
- El *pull request* `week-24` de tu proyecto fusionado en `main`, con la CI en verde.

---

## 🗂️ Estructura de la Semana

```
week-25-pandas_groupby_merge_y_series_de_tiempo/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 24 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · groupby: dividir, calcular y juntar](1-teoria/01-groupby-dividir-calcular-y-juntar.md) | *Split-apply-combine*, `agg` con nombre, `count` y `size`, claves que faltan, dos claves, `transform`, `filter` y `apply` | 45 min |
| [02 · Combinar tablas: concat, merge y join](1-teoria/02-combinar-tablas-concat-merge-y-join.md) | Apilar o cruzar, `concat` y su índice, los cuatro `how`, claves repetidas y `validate`, `suffixes`, `join`, `map` y `merge` por el índice | 50 min |
| [03 · Dar forma: pivot, melt y crosstab](1-teoria/03-dar-forma-pivot-melt-y-crosstab.md) | Formato largo y ancho, `pivot` y sus repetidos, `pivot_table`, `melt`, `stack` y `unstack`, `crosstab` | 45 min |
| [04 · Series de tiempo](1-teoria/04-series-de-tiempo.md) | `Timestamp`, `Timedelta` y `NaT`, `to_datetime` con formato, `date_range`, índice de tiempo, `resample`, `rolling`, `shift` y zonas horarias | 50 min |
| [05 · pandas II en un proyecto](1-teoria/05-pandas-ii-en-un-proyecto.md) | Dónde vive cada pieza, tipos con `pandas-stubs`, probar resúmenes, tiempo en la frontera, qué gana pandas y cuándo no usarlo | 50 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, ejecutas y comparas con la salida esperada. Preparan el proyecto. Las salidas coinciden con las del README salvo los tiempos del ejercicio 01.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · groupby: dividir, calcular y juntar](2-practicas/ejercicio-01-groupby-dividir-calcular-y-juntar/README.md) | Medias por estación, `agg` con nombre, la fila sin estación, dos claves, `transform`, `filter` y `groupby` frente a un diccionario | 1 h 30 min |
| [02 · Combinar con concat, merge y join](2-practicas/ejercicio-02-combinar-con-concat-merge-y-join/README.md) | Apilar dos días, los cuatro `how`, una clave repetida que multiplica filas, `suffixes`, `join` y `map` | 1 h 30 min |
| [03 · Dar forma con pivot y melt](2-practicas/ejercicio-03-dar-forma-con-pivot-y-melt/README.md) | De largo a ancho y vuelta, `pivot_table` con repetidos, `stack`, `unstack` y `crosstab` | 1 h 30 min |
| [04 · Series de tiempo](2-practicas/ejercicio-04-series-de-tiempo/README.md) | Leer fechas día/mes/año, elegir por día, `resample`, `rolling` por filas y por tiempo, y el cambio de hora | 1 h 30 min |

### Proyecto

Añades a tu Observatorio:

- `core/summaries.py`: `summary` (una fila por etiqueta con `groupby`), `compare` (dos resúmenes con `merge`), `duration`, `timed` y `evolution` (`pivot` y `resample`);
- el comando `resumir RUTA [-c OTRA]`, que resume cada etiqueta o compara sus medias con las de otro archivo;
- el comando `evolucion RUTA --inicio FECHA [--cada 1h] [--periodo 1D] [-n FILAS]`, con la media de cada etiqueta en cada periodo;
- `NAMES`, un solo diccionario que pone en español las columnas y los índices de todas las tablas.

pandas sigue cargándose **solo** en los comandos que lo usan. No hay dependencias nuevas. 52 tests nuevos, cuatro con Hypothesis que comparan con lo que ya tenías. La versión sube a `0.25.0`. **Es el único entregable de la semana.**
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
| Varias estadísticas por grupo con nombres claros | `df.groupby("k").agg(media=("v", "mean"), n=("v", "count"))` |
| ¿Cuántos faltan en cada grupo? | `df.groupby("k")["v"].agg(lambda v: v.isna().sum())`, o `size - count` |
| Que la fila sin clave no desaparezca | `groupby("k", dropna=False)` |
| La media de su grupo en cada fila | `df.groupby("k")["v"].transform("mean")` |
| ¿Qué filas no cruzaron? | `merge(..., how="outer", indicator=True)` y mirar `_merge` |
| Que un `merge` no multiplique filas | `validate="many_to_one"` (o la relación que esperes) |
| Aplanar columnas de dos niveles | `df.columns = [f"{a}_{b}" for a, b in df.columns]` |
| Leer fechas día/mes/año | `pd.to_datetime(col, format="%d/%m/%Y %H:%M", errors="coerce")` |
| Ver los periodos vacíos de `resample` | `.resample("1D").count()` |
| Periodos que empiezan en la primera medida | `resample("6h", origin="start")` |
| Media móvil con medidas irregulares | `rolling("6h").mean()` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-25` de `python-<nombre>-<apellido>` con:
   - `core/summaries.py` sin reexportar en `core/__init__.py`, y los comandos `resumir` y `evolucion` con pandas importado dentro;
   - las imágenes `week-25` en `compose.yaml`;
   - la versión `0.25.0` y al menos 6 tests propios en `tests/test_my_summaries.py`.

   Todo en verde en tu máquina, en Docker y en GitHub Actions.
2. ✅ `README.md` del repositorio con la sección "Resumir y evolución"
3. ✅ Pull request `week-25` → `main` con:
   - las salidas de los ganchos, la cobertura, `alembic check` y la CI en verde;
   - `resumir`, `resumir --contra` y `evolucion` con tus datos;
   - tu tabla de tiempos y la tabla de mutantes con las dos respuestas del paso 12.

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
uv run observatorio resumir medidas.txt
uv run observatorio evolucion medidas.txt --inicio 2026-11-01T08:00:00 --periodo 3h
uv run python -c "import sys, observatorio.cli; print('pandas' in sys.modules)"
docker compose build app api && docker compose run --rm app
gh pr checks
```

Lo que debes ver:

- todos los ganchos en `Passed` (o `Skipped`);
- los tests terminan en `passed` sin `failed`, al menos 1006;
- `coverage report` termina sin `Coverage failure`;
- `alembic check` dice `No new upgrade operations detected.`;
- `--version` escribe `observatorio 0.25.0`;
- `resumir` escribe una fila por etiqueta con `medidas`, `faltan`, `media`, `mínimo` y `máximo`, y la línea `N etiquetas · M medidas`;
- `evolucion` escribe una fila por periodo y una columna por etiqueta, y la línea `N periodos · M medidas`;
- la comprobación de `sys.modules` escribe `False`;
- `gh pr checks` con `quality`, `tests` e `image` en `pass`.

En los ejercicios, cada paso descomentado da la salida que muestra su README; los tiempos, los de tu máquina.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 24](../week-24-pandas_series_dataframe_y_seleccion/README.md) | **Semana 25** | Semana 26 (próximamente) |
