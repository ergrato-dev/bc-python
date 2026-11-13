# Semana 32 — Features, pipelines, validación cruzada y tuning

> En la semana 31 entrenaste un modelo, lo mediste con un reparto y lo comparaste con una referencia. Ahora preparas las entradas **dentro** de un pipeline, mides con **varios** repartos y eliges los hiperparámetros sin hacer trampa. Tu Observatorio gana el comando `ajustar`: los dos modelos, ajustados y validados pliegue a pliegue.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Preparar** entradas con transformadores: escalar, codificar, rellenar huecos y derivar entradas de una fecha
- **Encadenar** la preparación y el modelo con `Pipeline` y `ColumnTransformer`, y **explicar** por qué así no hay fugas
- **Validar** con k pliegues, y **elegir** cómo repartir: al azar, por grupos o por tiempo
- **Ajustar** hiperparámetros con `GridSearchCV` y `RandomizedSearchCV`, y **leer** una curva de validación
- **Medir** un modelo ajustado con validación anidada, sin el optimismo de `best_score_`
- **Comparar** un modelo con su referencia pliegue a pliegue

---

## 📋 Prerrequisitos

- [Semana 31](../week-31-ml_con_scikit_learn_regresion_clasificacion_y_metricas/README.md): `fit`, `predict`, el reparto, las métricas, la referencia y las fugas de datos.
- El *pull request* `week-31` de tu proyecto fusionado en `main`, con la CI en verde.

---

## 🗂️ Estructura de la Semana

```
week-32-features_pipelines_validacion_cruzada_y_tuning/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 31 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
|---|---|---|
| [01 · Preparar las entradas](1-teoria/01-preparar-las-entradas.md) | *Features*, transformadores, `StandardScaler`, `OneHotEncoder`, `SimpleImputer` y entradas derivadas | 45 min |
| [02 · Pipelines](1-teoria/02-pipelines.md) | `Pipeline`, `ColumnTransformer`, `named_steps`, `set_params` y la fuga de elegir columnas | 50 min |
| [03 · Validación cruzada](1-teoria/03-validacion-cruzada.md) | Un reparto es una tirada, `KFold`, `cross_val_score`, la referencia pliegue a pliegue, grupos y tiempo | 50 min |
| [04 · Ajuste de hiperparámetros](1-teoria/04-ajuste-de-hiperparametros.md) | Parámetros e hiperparámetros, Ridge y `C`, la curva de validación, `GridSearchCV` y `RandomizedSearchCV` | 50 min |
| [05 · Validación anidada y tu modelo ajustado](1-teoria/05-validacion-anidada-y-tu-modelo-ajustado.md) | El optimismo de `best_score_`, la validación anidada y el comando `ajustar` | 45 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, ejecutas y comparas con la salida esperada. Preparan el proyecto.

| Ejercicio | Qué haces | Duración |
|---|---|---|
| [01 · Preparar las entradas](2-practicas/ejercicio-01-preparar-las-entradas/README.md) | La hora punta de una fecha, escalar, codificar una zona nueva, rellenar huecos y un `ColumnTransformer` | 1 h 30 min |
| [02 · Pipelines sin fugas](2-practicas/ejercicio-02-pipelines-sin-fugas/README.md) | Un pipeline de principio a fin, sus coeficientes con nombre, `set_params` y la fuga de `SelectKBest` | 1 h 30 min |
| [03 · Validación cruzada](2-practicas/ejercicio-03-validacion-cruzada/README.md) | Diez semillas, cinco pliegues, datos ordenados sin mezclar, una zona nueva y un cambio en julio | 1 h 30 min |
| [04 · Ajuste de hiperparámetros](2-practicas/ejercicio-04-ajuste-de-hiperparametros/README.md) | La curva de `n_neighbors`, una rejilla, una búsqueda al azar, cinco ganadores con suerte y la anidada | 1 h 30 min |

### Proyecto

Añades a tu Observatorio:

- `core/validation.py`: `ordered` (las medidas en orden de llegada), `prepare` (la etiqueta en one-hot y la posición escalada), `folds` (al azar o por tiempo) y `validate` (el modelo ajustado frente a su referencia, en cada pliegue);
- el comando `ajustar INSTANTANEA [--huella] [--pliegues] [--tiempo]`.

57 tests nuevos: 56 del módulo y el comando, y un ejemplo tuyo. Sin dependencias nuevas. La versión sube a `0.32.0`. **Es el único entregable de la semana.**
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
| Ver las columnas que salen de la preparación | `pipeline.named_steps["prepare"].get_feature_names_out()` |
| Cambiar un hiperparámetro sin rehacer el pipeline | `pipeline.set_params(model__alpha=10)` |
| Ver todos los parámetros que se pueden buscar | `sorted(pipeline.get_params())` |
| Los mismos pliegues para dos modelos | Un `KFold(5, shuffle=True, random_state=32)` pasado a los dos |
| El error en positivo | `-cross_val_score(model, x, y, scoring="neg_mean_absolute_error")` |
| Todo lo que probó una búsqueda | `pd.DataFrame(search.cv_results_).sort_values("rank_test_score")` |
| Valores en potencias de 10 | `np.logspace(-2, 2, 5)` da 0,01, 0,1, 1, 10 y 100 |
| La validación anidada | `cross_val_score(GridSearchCV(...), x, y, cv=otros_pliegues)` |
| Ajustar con pliegues por tiempo | `uv run observatorio ajustar notebooks/instantanea.csv --tiempo` |
| Que vaya más rápido | `GridSearchCV(..., n_jobs=-1)`: usa todos los núcleos |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-32` de `python-<nombre>-<apellido>` con:
   - `core/validation.py` sin reexportar en `core/__init__.py` y el comando `ajustar`, con los imports dentro;
   - las imágenes `week-32`, la versión `0.32.0` y al menos 6 tests propios en `tests/test_my_validation.py`.

   Todo en verde en tu máquina, en Docker y en GitHub Actions.
2. ✅ `README.md` del repositorio con la sección "Modelo ajustado", e `informe/README.md` con el resultado en "Siguientes pasos"
3. ✅ Pull request `week-32` → `main` con:
   - las salidas de los ganchos, la cobertura, `alembic check` y la CI en verde;
   - la salida de `ajustar` con tu instantánea, al azar y por tiempo, y tu lectura;
   - la tabla de mutantes con las dos respuestas del paso 8.

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
uv run observatorio ajustar notebooks/instantanea.csv
uv run observatorio ajustar notebooks/instantanea.csv --pliegues 3 --tiempo
uv run observatorio ajustar notebooks/instantanea.csv --huella 0000
uv run python -c "import sys, observatorio.cli; print('sklearn' in sys.modules)"
docker compose build app api && docker compose run --rm app
gh pr checks
```

Lo que debes ver:

- todos los ganchos en `Passed` (o `Skipped`);
- los tests terminan en `passed` sin `failed`, al menos 1219;
- `coverage report` termina sin `Coverage failure`;
- `alembic check` dice `No new upgrade operations detected.`;
- `--version` escribe `observatorio 0.32.0`;
- el primer `ajustar` escribe tu número de medidas, tu huella, `pliegues al azar`, dos tablas de cinco pliegues y su media, y dos veredictos con el hiperparámetro elegido;
- el segundo, `pliegues por tiempo` y tablas de tres pliegues;
- el tercero, `error: la huella de instantanea.csv es ..., no 0000` y código 1;
- la comprobación de `sys.modules` escribe `False`;
- `gh pr checks` con `quality`, `tests` e `image` en `pass`.

En los ejercicios, cada paso descomentado da la salida que muestra su README.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 31](../week-31-ml_con_scikit_learn_regresion_clasificacion_y_metricas/README.md) | **Semana 32** | [Semana 33](../week-33-arboles_ensembles_gradient_boosting_y_no_supervisado/README.md) |
