# Semana 28 — Estadística aplicada con SciPy y statsmodels

> Hasta ahora tu Observatorio describe: medias, cuartiles, tablas y gráficos de lo que has medido. Esta semana das el paso a la **inferencia**: decir algo sobre todo lo que podrías medir a partir de lo que mediste, y cuánto puedes equivocarte. Aprendes a hacerle preguntas a una distribución con **SciPy**, a ponerle un intervalo de confianza a una media, a contrastar si dos grupos son distintos (y a no fiarte de un p-valor a solas), y a medir tendencias y diferencias entre grupos con los modelos de **statsmodels**. Tu Observatorio gana el comando `comparar`, que dice si la diferencia entre dos etiquetas es real o puede ser azar, con su intervalo, su tamaño del efecto y dos pruebas, y con tests que comprueban los números a mano.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Usar** las distribuciones de `scipy.stats` para responder preguntas de probabilidad, y simular cuando no hay fórmula
- **Estimar** una media con su error estándar y su intervalo de confianza, e **interpretar** el 95 % sin caer en la lectura equivocada
- **Contrastar** dos grupos con Welch, Mann-Whitney, permutaciones y chi cuadrado, y **leer** un p-valor junto a la potencia y el tamaño del efecto
- **Ajustar** regresiones con statsmodels, con variables con categorías y predicciones con su incertidumbre
- **Llevar** la estadística a un proyecto: comprobaciones antes de calcular, tests con valores calculados a mano y con propiedades, y tipos para SciPy
- **Medir** lo que cuesta cada biblioteca, y elegir cuál entra en el proyecto

---

## 📋 Prerrequisitos

- [Semana 23](../week-23-numpy_arrays_broadcasting_y_estadistica/README.md): arrays, vectorización, media, desviación y percentiles con NumPy.
- [Semana 27](../week-27-visualizacion_con_matplotlib_seaborn_y_plotly/README.md): tablas largas, histogramas y el precio de una dependencia en la imagen.
- El *pull request* `week-27` de tu proyecto fusionado en `main`, con la CI en verde.

---

## 🗂️ Estructura de la Semana

```
week-28-estadistica_aplicada_con_scipy_y_statsmodels/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 27 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
|---|---|---|
| [01 · Variables aleatorias y distribuciones](1-teoria/01-variables-aleatorias-y-distribuciones.md) | Población y muestra, `cdf`, `sf`, `ppf` y `pdf`, normal, exponencial, binomial y Poisson, semillas, ley de los grandes números y teorema central del límite | 50 min |
| [02 · Estimar con incertidumbre](1-teoria/02-estimar-con-incertidumbre.md) | Error estándar, intervalo t, qué significa "95 %", ancho y tamaño de muestra, *bootstrap* y sus límites | 45 min |
| [03 · Pruebas de hipótesis](1-teoria/03-pruebas-de-hipotesis.md) | Hipótesis nula y p-valor, errores de tipo I y II, potencia, Welch y Student, Mann-Whitney, chi cuadrado, muchas pruebas y tamaño del efecto | 50 min |
| [04 · Regresión con statsmodels](1-teoria/04-regresion-con-statsmodels.md) | Mínimos cuadrados, fórmulas, categorías y ANOVA, varias variables, intervalos de predicción, residuos, relación y causa | 45 min |
| [05 · Estadística en un proyecto](1-teoria/05-estadistica-en-un-proyecto.md) | `inference.py` y `comparar`, comprobaciones antes de calcular, tests a mano y con propiedades, `scipy-stubs`, el precio en la imagen y qué biblioteca entra | 50 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, ejecutas y comparas con la salida esperada. Preparan el proyecto. Las salidas coinciden con las del README salvo los tiempos del ejercicio 04: todo lo aleatorio lleva semilla.

| Ejercicio | Qué haces | Duración |
|---|---|---|
| [01 · Distribuciones con scipy.stats](2-practicas/ejercicio-01-distribuciones-con-scipy/README.md) | Cuatro preguntas a una normal, muestras y ley de los grandes números, binomial y Poisson, teorema central del límite, ajustar un modelo | 1 h 30 min |
| [02 · Intervalos de confianza y bootstrap](2-practicas/ejercicio-02-intervalos-y-bootstrap/README.md) | El intervalo t a mano, contar cuántos intervalos aciertan, ancho y datos, *bootstrap* de la mediana, datos asimétricos | 1 h 30 min |
| [03 · Pruebas de hipótesis](2-practicas/ejercicio-03-pruebas-de-hipotesis/README.md) | Welch y Student, el p-valor barajando, un valor extremo, chi cuadrado, muchas pruebas, potencia y tamaño del efecto | 1 h 30 min |
| [04 · Regresión con statsmodels](2-practicas/ejercicio-04-regresion-con-statsmodels/README.md) | Una recta con SciPy y con statsmodels, categorías y ANOVA, predicciones y residuos, lo que cuesta cada biblioteca | 1 h 30 min |

### Proyecto

Añades a tu Observatorio:

- `core/inference.py`: `sample` (los valores de una etiqueta, sin pandas) y `difference` (Welch con su intervalo, la d de Cohen y Mann-Whitney, con un `ValueError` claro cuando no hay nada que comparar);
- el comando `comparar RUTA ETIQUETA OTRA [--confianza]`.

Dos dependencias nuevas: `scipy==1.18.1`, cargada **solo** en `comparar`, y `scipy-stubs==1.18.1.1` para mypy. 40 tests nuevos, tres con Hypothesis, que comparan con valores calculados a mano. La versión sube a `0.28.0`. **Es el único entregable de la semana.**
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
| Una distribución con sus parámetros | `noon = stats.norm(loc=20, scale=3)` |
| La probabilidad de una cola | `noon.sf(26)`, mejor que `1 - noon.cdf(26)` |
| El valor de un percentil | `noon.ppf(0.95)` |
| Números al azar reproducibles | `rng = np.random.default_rng(28)` |
| El intervalo de una media | `stats.ttest_1samp(x, popmean=0).confidence_interval(0.95)` |
| Comparar dos medias sin suponer la misma dispersión | `stats.ttest_ind(a, b, equal_var=False)` |
| El intervalo de esa diferencia | `.confidence_interval(0.95)` sobre el resultado anterior |
| Un intervalo para lo que no tiene fórmula | `stats.bootstrap((x,), np.median, rng=28)` |
| Un p-valor sin fórmula | `stats.permutation_test((a, b), estadístico, rng=28)` |
| Corregir muchas pruebas | `stats.false_discovery_control(pvalores)` |
| Una regresión con categorías | `smf.ols("value ~ day + C(station)", data=frame).fit()` |
| Predecir un valor concreto, con su intervalo | `fit.get_prediction(nuevos).summary_frame()["obs_ci_lower"]` |
| Tipos de SciPy para mypy | `uv add --dev scipy-stubs` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-28` de `python-<nombre>-<apellido>` con:
   - `core/inference.py` sin reexportar en `core/__init__.py` y el comando `comparar`, con SciPy importado dentro;
   - `scipy==1.18.1` en las dependencias, `scipy-stubs==1.18.1.1` en las de desarrollo y las imágenes `week-28` en `compose.yaml`;
   - la versión `0.28.0` y al menos 6 tests propios en `tests/test_my_inference.py`.

   Todo en verde en tu máquina, en Docker y en GitHub Actions.
2. ✅ `README.md` del repositorio con la sección "Comparar etiquetas"
3. ✅ Pull request `week-28` → `main` con:
   - las salidas de los ganchos, la cobertura, `alembic check` y la CI en verde;
   - dos salidas de `comparar` con tus datos y lo que concluyes de cada una;
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
uv run observatorio comparar medidas.txt Norte Sur
uv run observatorio comparar medidas.txt Norte Centro
uv run python -c "import sys, observatorio.cli; print('scipy' in sys.modules)"
docker compose build app api && docker compose run --rm app
gh pr checks
```

Lo que debes ver:

- todos los ganchos en `Passed` (o `Skipped`);
- los tests terminan en `passed` sin `failed`, al menos 1154;
- `coverage report` termina sin `Coverage failure`;
- `alembic check` dice `No new upgrade operations detected.`;
- `--version` escribe `observatorio 0.28.0`;
- el primer `comparar` escribe la línea mala en stderr y las cinco líneas del informe, con `IC 95 %: [-207.66, 251.56]`, y termina con código 1 por esa línea;
- el segundo, `error: no se puede comparar Norte con Centro: cada muestra necesita al menos 2 valores (tienen 2 y 0)` y código 2;
- la comprobación de `sys.modules` escribe `False`;
- `gh pr checks` con `quality`, `tests` e `image` en `pass`.

En los ejercicios, cada paso descomentado da la salida que muestra su README; los tiempos, los de tu máquina.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 27](../week-27-visualizacion_con_matplotlib_seaborn_y_plotly/README.md) | **Semana 28** | [Semana 29](../week-29-eda_notebooks_reproducibles_y_etl_desde_postgresql/README.md) |
