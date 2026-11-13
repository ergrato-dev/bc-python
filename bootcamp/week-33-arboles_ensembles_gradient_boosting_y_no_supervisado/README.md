# Semana 33 — Árboles, ensembles, gradient boosting y no supervisado

> En la semana 32 ajustaste un modelo lineal y lo mediste pliegue a pliegue. Ahora entrenas modelos que hacen preguntas en vez de sumar pesos: un árbol, un bosque de árboles y un *gradient boosting*. Y das el primer paso sin una respuesta que acertar: agrupas con KMeans y resumes con PCA. Tu Observatorio gana dos comandos: `competir`, los cinco modelos con los mismos pliegues, y `agrupar`, tus etiquetas en grupos.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Explicar** cómo predice y cómo crece un árbol de decisión, y **controlar** su profundidad
- **Explicar** por qué un bosque aleatorio predice mejor que sus árboles, y **leer** sus importancias sin dejarte engañar
- **Entrenar** un *gradient boosting* con `learning_rate`, número de árboles y parada temprana
- **Comparar** un árbol, un bosque, un boosting, un modelo lineal y la referencia con los mismos pliegues
- **Agrupar** con KMeans, escalando antes, y **decidir** con la silueta si los grupos existen
- **Resumir** muchas columnas en pocas con PCA

---

## 📋 Prerrequisitos

- [Semana 32](../week-32-features_pipelines_validacion_cruzada_y_tuning/README.md): pipelines, `ColumnTransformer`, validación cruzada, hiperparámetros.
- El *pull request* `week-32` de tu proyecto fusionado en `main`, con la CI en verde.

---

## 🗂️ Estructura de la Semana

```
week-33-arboles_ensembles_gradient_boosting_y_no_supervisado/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 32 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
|---|---|---|
| [01 · Árboles de decisión](1-teoria/01-arboles-de-decision.md) | Preguntas de sí o no, cómo se elige cada corte, `max_depth`, umbrales y cruces, no extrapola | 45 min |
| [02 · Bosques aleatorios](1-teoria/02-bosques-aleatorios.md) | La varianza de un árbol, *bagging*, `RandomForestRegressor`, *out-of-bag* e importancias | 50 min |
| [03 · Gradient boosting](1-teoria/03-gradient-boosting.md) | Aprender el residuo, `learning_rate`, parada temprana, `HistGradientBoosting*` | 50 min |
| [04 · Agrupar con KMeans](1-teoria/04-agrupar-con-kmeans.md) | Aprender sin respuesta, KMeans, escalar, la inercia, la silueta y los grupos que no existen | 50 min |
| [05 · PCA, y tus modelos y grupos](1-teoria/05-pca-y-tus-modelos-y-grupos.md) | Componentes principales, varianza explicada, y los comandos `competir` y `agrupar` | 45 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, ejecutas y comparas con la salida esperada. Preparan el proyecto.

| Ejercicio | Qué haces | Duración |
|---|---|---|
| [01 · Árboles de decisión](2-practicas/ejercicio-01-arboles-de-decision/README.md) | Un árbol que se lee, escalones, la profundidad, un árbol frente a una recta, la escala y la extrapolación | 1 h 30 min |
| [02 · Bosques aleatorios](2-practicas/ejercicio-02-bosques-aleatorios/README.md) | Un árbol inestable, un bosque estable, cuántos árboles, *out-of-bag* e importancias con una columna de ruido | 1 h 30 min |
| [03 · Gradient boosting](2-practicas/ejercicio-03-gradient-boosting/README.md) | Árbol a árbol, el ritmo, parar a tiempo, categorías y huecos, cinco modelos y las horas de aire malo | 1 h 30 min |
| [04 · Agrupar y reducir](2-practicas/ejercicio-04-agrupar-y-reducir/README.md) | Perfiles de sensores, KMeans, cuántos grupos, una columna en otra escala, PCA y grupos en el ruido | 1 h 30 min |

### Proyecto

Añades a tu Observatorio:

- `core/ensembles.py`: `candidates` (los cinco modelos), `compete` (todos con los mismos pliegues y la misma preparación) y `Contest` (la mejor media y si gana a la referencia en todos los pliegues);
- `core/clustering.py`: `profiles` (media, mediana y desviación de cada etiqueta) y `cluster` (KMeans sobre los perfiles escalados, con la silueta);
- los comandos `competir INSTANTANEA [--huella] [--pliegues] [--tiempo]` y `agrupar INSTANTANEA [--huella] [--grupos]`.

78 tests nuevos: 51 de `ensembles` y `competir`, 26 de `clustering` y `agrupar`, y un ejemplo tuyo. Sin dependencias nuevas. La versión sube a `0.33.0`. **Es el único entregable de la semana.**
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
| Leer un árbol pequeño | `print(export_text(tree, feature_names=names))` |
| Cuánto creció un árbol | `tree.get_depth()` y `tree.get_n_leaves()` |
| La nota de un bosque sin validación cruzada | `RandomForestRegressor(oob_score=True)` y `oob_score_` |
| Qué columnas usa de verdad un modelo | `permutation_importance(model, test_x, test_y, n_repeats=10)` |
| Que un boosting pare solo | `HistGradientBoostingRegressor(early_stopping=True)` y `n_iter_` |
| Categorías y huecos sin preparar | `HistGradientBoostingRegressor(categorical_features="from_dtype")`, con columnas `category` |
| Que el bosque vaya más rápido | `RandomForestRegressor(n_jobs=-1)`: usa todos los núcleos |
| Agrupar bien | `make_pipeline(StandardScaler(), KMeans(k, n_init=10, random_state=33))` |
| Cuánto recoge cada componente | `PCA().fit(x).explained_variance_ratio_` |
| Comparar tus modelos | `uv run observatorio competir notebooks/instantanea.csv --tiempo` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-33` de `python-<nombre>-<apellido>` con:
   - `core/ensembles.py` y `core/clustering.py` sin reexportar en `core/__init__.py`, y los comandos `competir` y `agrupar`, con los imports dentro;
   - las imágenes `week-33`, la versión `0.33.0` y al menos 6 tests propios en `tests/test_my_ensembles.py`.

   Todo en verde en tu máquina, en Docker y en GitHub Actions.
2. ✅ `README.md` del repositorio con la sección "Modelos y grupos", e `informe/README.md` con los resultados en "Siguientes pasos"
3. ✅ Pull request `week-33` → `main` con:
   - las salidas de los ganchos, la cobertura, `alembic check` y la CI en verde;
   - la salida de `competir` (al azar y por tiempo) y de `agrupar` con tu instantánea, y tu lectura;
   - la tabla de mutantes con las dos respuestas del paso 10.

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
uv run observatorio competir notebooks/instantanea.csv
uv run observatorio competir notebooks/instantanea.csv --pliegues 3 --tiempo
uv run observatorio agrupar notebooks/instantanea.csv -g 3
uv run observatorio agrupar notebooks/instantanea.csv --huella 0000
uv run python -c "import sys, observatorio.cli; print('sklearn' in sys.modules)"
docker compose build app api && docker compose run --rm app
gh pr checks
```

Lo que debes ver:

- todos los ganchos en `Passed` (o `Skipped`);
- los tests terminan en `passed` sin `failed`, al menos 1297;
- `coverage report` termina sin `Coverage failure`;
- `alembic check` dice `No new upgrade operations detected.`;
- `--version` escribe `observatorio 0.33.0`;
- el primer `competir` escribe tu número de medidas, tu huella, `pliegues al azar`, dos tablas de cinco modelos y cinco pliegues, y un veredicto por tabla;
- el segundo, `pliegues por tiempo` y tablas de tres pliegues;
- el primer `agrupar`, la tabla de tus etiquetas con su grupo (del 1 al 3) y su perfil, y la silueta; con menos de 4 etiquetas, usa `-g 2`;
- el segundo, `error: la huella de instantanea.csv es ..., no 0000` y código 1;
- la comprobación de `sys.modules` escribe `False`;
- `gh pr checks` con `quality`, `tests` e `image` en `pass`.

En los ejercicios, cada paso descomentado da la salida que muestra su README.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 32](../week-32-features_pipelines_validacion_cruzada_y_tuning/README.md) | **Semana 33** | [Semana 34](../week-34-pytorch_tensores_autograd_y_mlp/README.md) |
