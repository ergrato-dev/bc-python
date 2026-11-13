# Ejercicio 02 — Pipelines sin fugas

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-pipelines.md)

## Objetivo

Unir la preparación del ejercicio 01 y un modelo en un solo estimador:

- un `Pipeline` con el `ColumnTransformer` y Ridge, entrenado y medido;
- predecir con la tabla original, con huecos y con una zona nueva;
- leer los coeficientes con sus nombres;
- cambiar un hiperparámetro con `set_params` y el doble guion bajo;
- la fuga de elegir columnas antes de validar, y cómo la evita el pipeline.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-32-features_pipelines_validacion_cruzada_y_tuning/2-practicas/ejercicio-02-pipelines-sin-fugas/starter
uv run python main.py
```

```
Ejercicio 02 · Pipelines sin fugas
1200 medidas · de 05/01 a 31/10
```

Los datos del ejercicio 01, con las tres columnas derivadas ya creadas y el reparto hecho: `x_train`, `x_test`, `y_train` e `y_test`. `prepare()` devuelve el `ColumnTransformer` del paso 6 del ejercicio 01, **nuevo y sin ajustar** cada vez que lo llamas.

## Pasos

### 1. Un pipeline

Descomenta el **PASO 1** y ejecuta:

```
R² en prueba: 0.804
MAE en prueba: 2.56
```

Un `fit` con la tabla original: el pipeline rellena, codifica y escala con el entrenamiento, y entrena Ridge con el resultado. Un `score` con la prueba: la prepara con lo aprendido y predice. Un error medio de 2,56 con un ruido de 3 en el generador: el modelo ha aprendido casi todo lo que se puede.

### 2. Predecir con la tabla original

Descomenta el **PASO 2** y ejecuta:

```
[28.8 27.8 22.6]
```

Tres medidas a las 8 de un lunes:

- Centro con 50 % de humedad: 28,8.
- Centro **sin** humedad: el pipeline pone la mediana del entrenamiento (63) y marca el hueco. Más humedad, menos partículas: 27,8.
- Puerto, una zona que no existe: fila de ceros en las zonas, y el modelo predice como "ninguna zona conocida", entre todas.

No has preparado nada a mano: `predict` recibe la misma forma de tabla que `fit`.

### 3. Qué aprendió

Descomenta el **PASO 3** y ejecuta:

```
tal_cual__punta                        8.18
zona__zona_Centro                      6.18
zona__zona_Sur                        -5.23
tal_cual__finde                       -3.60
zona__zona_Norte                      -1.68
zona__zona_Este                        0.73
hora__hora                            -0.20
humedad__missingindicator_humedad      0.15
humedad__humedad                      -0.09
```

Compáralo con el generador: +8 en hora punta, −4 en fin de semana, −0,1 por punto de humedad. Las zonas, respecto a su media: Centro 12, Sur 0, Norte 4, Este 6. La hora escalada casi no pesa: lo que importa es si es punta, no si es tarde. Y el hueco no dice nada, porque faltaba al azar.

`named_steps` da cada paso ya ajustado; `get_feature_names_out` pone nombre a cada coeficiente.

### 4. Cambiar un paso

Descomenta el **PASO 4** y ejecuta:

```
alpha=1        R² 0.804
alpha=100      R² 0.727
alpha=10000    R² 0.096
```

`model__alpha`: el paso `"model"`, su parámetro `alpha`. Cuanta más regularización, más se encogen los coeficientes y más se parece el modelo a predecir la media. Aquí la señal es clara y no hace falta regularizar. La teoría 04 y el ejercicio 04 buscan el mejor valor.

### 5. La fuga de elegir columnas

Descomenta el **PASO 5** y ejecuta. Tarda unos segundos:

```
eligiendo antes de validar: 0.76
eligiendo dentro del pipeline: 0.43
```

Cien casos con 2000 columnas de ruido y un nivel "alto" o "normal" al azar: no hay nada que aprender.

- **Antes de validar**, `SelectKBest` mira las cien filas y se queda con las diez columnas que más se parecen al nivel, **por casualidad**. La validación cruzada da 0,76: un modelo que "acierta" con ruido.
- **Dentro del pipeline**, cada pliegue elige sus diez columnas solo con su entrenamiento. En prueba, esas columnas no dicen nada: 0,43, el azar.

Es la fuga más fácil de cometer sin darte cuenta: cualquier cosa que mire `y` (elegir columnas, medias por grupo, quitar "atípicos") va dentro del pipeline.

Para terminar, escribe en un comentario al final de `main.py` qué paso de preparación de tu dominio podría mirar el objetivo sin que te dieras cuenta.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ValueError: Invalid parameter 'alpha' for estimator Pipeline(...)` | Falta el paso: `model__alpha`, con doble guion bajo |
| `ValueError: Found unknown categories ['Puerto']` | Falta `handle_unknown="ignore"` en `prepare()` |
| `ValueError: Input X contains NaN` en el paso 2 | Quitaste el `SimpleImputer` de `prepare()` |
| `AttributeError: 'Pipeline' object has no attribute 'coef_'` | El coeficiente es del paso: `model.named_steps["model"].coef_` |
| Tus números del paso 5 no coinciden | El paso 5 saca números del mismo generador que los datos: no añadas pasos que lo usen antes |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Preparar las entradas](../ejercicio-01-preparar-las-entradas/README.md) | **Ejercicio 02 · Pipelines sin fugas** | [Ejercicio 03 · Validación cruzada](../ejercicio-03-validacion-cruzada/README.md) |
