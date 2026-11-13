# Semana 31 — ML con scikit-learn: regresión, clasificación y métricas

> Abre la fase 5. En la fase 4 describiste tus datos; ahora **predices**. Entrenas tus primeros modelos con scikit-learn, los mides con medidas que no vieron y los comparas con una referencia que no sabe nada. Tu Observatorio gana el comando `modelo`: una regresión del valor y una clasificación del nivel, cada una con su veredicto.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Plantear** un problema supervisado: casos, entradas, objetivo, `X` e `y`, regresión o clasificación
- **Usar** la interfaz de scikit-learn: `fit`, `predict`, `predict_proba` y `score`
- **Repartir** los datos en entrenamiento y prueba con semilla y estratificados, y **reconocer** el sobreajuste
- **Medir** una regresión con MAE, RMSE y R², y una clasificación con la matriz de confusión, precisión, exhaustividad, F1 y exactitud equilibrada
- **Comparar** cada modelo con una referencia (`DummyRegressor`, `DummyClassifier`)
- **Detectar** fugas de datos: el objetivo disfrazado, calcular con la prueba y las medidas repetidas

---

## 📋 Prerrequisitos

- [Semana 28](../week-28-estadistica_aplicada_con_scipy_y_statsmodels/README.md): la regresión lineal por mínimos cuadrados y R².
- [Semana 30](../week-30-proyecto_de_fase_analisis_de_tu_dominio/README.md): `read_snapshot`, la instantánea con su huella y tu informe.
- El *pull request* `week-30` de tu proyecto fusionado en `main`, con la CI en verde.

---

## 🗂️ Estructura de la Semana

```
week-31-ml_con_scikit_learn_regresion_clasificacion_y_metricas/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 30 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
|---|---|---|
| [01 · Aprender de los datos](1-teoria/01-aprender-de-los-datos.md) | De describir a predecir, casos, entradas y objetivo, regresión o clasificación, `fit`, `predict` y `score` | 45 min |
| [02 · Entrenar y probar](1-teoria/02-entrenar-y-probar.md) | El examen con las respuestas, sobreajuste e infraajuste, `train_test_split`, la referencia, la prueba se usa una vez | 50 min |
| [03 · Regresión y sus métricas](1-teoria/03-regresion-y-sus-metricas.md) | Varias entradas, one-hot con `get_dummies`, MAE, RMSE y R², R² negativo, residuos | 50 min |
| [04 · Clasificación y sus métricas](1-teoria/04-clasificacion-y-sus-metricas.md) | Regresión logística, el umbral, la matriz de confusión, precisión, exhaustividad, F1 y la trampa de la exactitud | 50 min |
| [05 · Fugas de datos y tu primer modelo](1-teoria/05-fugas-de-datos-y-tu-primer-modelo.md) | El objetivo disfrazado, calcular con la prueba, el futuro, el comando `modelo` y un "no mejora" | 45 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, ejecutas y comparas con la salida esperada. Preparan el proyecto.

| Ejercicio | Qué haces | Duración |
|---|---|---|
| [01 · Tu primer modelo](2-practicas/ejercicio-01-tu-primer-modelo/README.md) | `X` e `y`, `fit` y `coef_`, `predict`, dos entradas, one-hot y otro modelo con la misma interfaz | 1 h 30 min |
| [02 · Entrenar, probar y la referencia](2-practicas/ejercicio-02-entrenar-probar-y-la-referencia/README.md) | Repartir y estratificar, MAE, RMSE y R² a mano, un modelo que memoriza, `DummyRegressor` y residuos por zona | 1 h 30 min |
| [03 · Clasificar y medir](2-practicas/ejercicio-03-clasificar-y-medir/README.md) | `predict_proba`, la matriz de confusión, las métricas a mano, mover el umbral y tres clases | 1 h 30 min |
| [04 · Desbalance y fugas](2-practicas/ejercicio-04-desbalance-y-fugas/README.md) | Un 96 % sin aprender nada, `class_weight`, el objetivo disfrazado, calcular con la prueba y medidas repetidas | 1 h 30 min |

### Proyecto

Añades a tu Observatorio:

- `core/learning.py`: `known` (las medidas con valor), `features` (la etiqueta en one-hot), `split` (entrenamiento y prueba, estratificado) y `regress` y `classify` (cada modelo frente a su referencia);
- el comando `modelo INSTANTANEA [--huella] [--prueba] [--semilla]`;
- el gancho `trailing-whitespace` sin tocar los SVG que genera `hallazgos`.

49 tests nuevos: 47 del módulo y el comando, uno del gancho y un ejemplo tuyo. Una dependencia nueva, scikit-learn 1.9.1. La versión sube a `0.31.0`. **Es el único entregable de la semana.**
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
| `X` de una columna | `frame[["columna"]]`, con dos corchetes |
| Entrenar y predecir en una línea | `LinearRegression().fit(x_train, y_train).predict(x_test)` |
| Repartir dos tablas a la vez | `x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=31, stratify=y)` |
| La referencia | `DummyRegressor(strategy="mean")`, `DummyClassifier(strategy="most_frequent")` |
| One-hot | `pd.get_dummies(frame["etiqueta"], dtype="float64")` |
| Todas las métricas de clasificación | `print(classification_report(y_test, predicted, zero_division=0))` |
| La matriz, en tu orden | `confusion_matrix(y_test, predicted, labels=["sí", "no"])` |
| Otro umbral | `np.where(model.predict_proba(x)[:, 1] >= 0.3, "sí", "no")` |
| Ver qué aprendió | `dict(zip(model.feature_names_in_, model.coef_))` |
| Buscar duplicados antes de repartir | `frame.duplicated().sum()` |
| Probar con otra semilla | `uv run observatorio modelo notebooks/instantanea.csv --semilla 7` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-31` de `python-<nombre>-<apellido>` con:
   - `core/learning.py` sin reexportar en `core/__init__.py` y el comando `modelo`, con los imports dentro;
   - scikit-learn 1.9.1 fijado con `uv add` y la excepción de mypy para `sklearn.*`;
   - el `exclude` de los SVG en `trailing-whitespace`, las imágenes `week-31`, la versión `0.31.0` y al menos 6 tests propios en `tests/test_my_learning.py`.

   Todo en verde en tu máquina, en Docker y en GitHub Actions.
2. ✅ `README.md` del repositorio con la sección "Modelo", e `informe/README.md` con el resultado en "Siguientes pasos"
3. ✅ Pull request `week-31` → `main` con:
   - las salidas de los ganchos, la cobertura, `alembic check` y la CI en verde;
   - la salida de `modelo` con tu instantánea y tu lectura;
   - la tabla de mutantes con las dos respuestas del paso 9.

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
uv run observatorio modelo notebooks/instantanea.csv
uv run observatorio modelo notebooks/instantanea.csv --huella 0000
uv run python -c "import sys, observatorio.cli; print('sklearn' in sys.modules)"
git status --short informe/
docker compose build app api && docker compose run --rm app
gh pr checks
```

Lo que debes ver:

- todos los ganchos en `Passed` (o `Skipped`);
- los tests terminan en `passed` sin `failed`, al menos 1162;
- `coverage report` termina sin `Coverage failure`;
- `alembic check` dice `No new upgrade operations detected.`;
- `--version` escribe `observatorio 0.31.0`;
- el primer `modelo` escribe tu número de medidas, tu huella, dos tablas y dos veredictos;
- el segundo, `error: la huella de instantanea.csv es ..., no 0000` y código 1;
- la comprobación de `sys.modules` escribe `False`;
- `git status` no muestra cambios en `informe/` después de los ganchos;
- `gh pr checks` con `quality`, `tests` e `image` en `pass`.

En los ejercicios, cada paso descomentado da la salida que muestra su README.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 30](../week-30-proyecto_de_fase_analisis_de_tu_dominio/README.md) | **Semana 31** | [Semana 32](../week-32-features_pipelines_validacion_cruzada_y_tuning/README.md) |
