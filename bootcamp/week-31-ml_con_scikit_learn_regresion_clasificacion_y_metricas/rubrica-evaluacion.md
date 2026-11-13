# Rúbrica de Evaluación — Semana 31: ML con scikit-learn, regresión, clasificación y métricas

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 30 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | ¿Qué son `X` e `y`? ¿Por qué `X` tiene dos dimensiones aunque haya una sola entrada? Predecir el valor y predecir el nivel, ¿qué tipo de problema es cada uno, y por qué? | 10 |
| 2 | ¿Qué hacen `fit`, `predict` y `score`? ¿Por qué `coef_` acaba en `_`? En el ejercicio 01, ¿qué aprendió el modelo con sol y nubes, y por qué `intercept_` era 9,76 cuando solo veía el sol? | 10 |
| 3 | En la teoría 02, el polinomio de grado 12 tiene el menor error en entrenamiento (1,71) y el mayor en prueba (10,77). ¿Cómo se llama lo que le pasa? ¿Qué señal lo delata, y por qué ningún modelo baja de un error de 3 con esos datos? | 10 |
| 4 | ¿Qué hacen `test_size`, `random_state` y `stratify`? En el ejercicio 02, ¿qué pasó con las medidas de nivel alto en prueba sin estratificar? ¿Cuándo no se debe repartir al azar? | 10 |
| 5 | Con solo la etiqueta en one-hot, ¿qué predice una regresión lineal? ¿Por qué no se numeran las etiquetas? Relaciónalo con la semana 30: si ninguna zona difiere, ¿qué esperas del modelo? | 10 |
| 6 | Calcula MAE, RMSE y R² de las predicciones 12, 18, 33 y 30 para los valores reales 10, 20, 30 y 40. ¿Qué dice que RMSE sea mayor que MAE? ¿Puede R² ser negativo, y cuándo? | 10 |
| 7 | Con la matriz `[[3, 1], [2, 14]]` (filas reales "alto" y "normal", columnas predichas en el mismo orden), calcula exactitud, precisión, exhaustividad y exactitud equilibrada. ¿Qué exactitud daría decir siempre "normal"? | 10 |
| 8 | ¿Qué devuelve `predict_proba` y en qué orden? ¿Qué pasa al bajar el umbral de 0,5 a 0,2? En el ejercicio 04, ¿por qué la regresión logística decía siempre "no" aunque la batería influyera, y qué cambió con `class_weight="balanced"`? | 10 |
| 9 | ¿Qué es una fuga de datos? Explica las tres de la teoría 05 con un ejemplo de tu dominio cada una. ¿Por qué las columnas one-hot del Observatorio, creadas con todas las medidas, no son una fuga? | 10 |
| 10 | ¿Por qué el comando `modelo` muestra cada métrica junto a la de una referencia, y decide con la MAE y la exactitud equilibrada? Con los datos de ejemplo dice "no mejora" en los dos modelos: ¿es un fallo? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. `X` son las entradas de todos los casos: una fila por caso y una columna por entrada; `y` es el objetivo de cada caso, uno por fila. `X` tiene dos dimensiones porque un modelo puede tener varias entradas, y scikit-learn exige siempre la tabla: con una dimensión, `fit` no sabe si son muchos casos de una entrada o un caso de muchas, y falla. Predecir el valor es **regresión**, porque el objetivo es un número; predecir el nivel es **clasificación**, porque es una categoría.
2. `fit` aprende de los ejemplos y devuelve el estimador; `predict` da una predicción por fila de `X`; `score` da una métrica por defecto (R² en regresión, exactitud en clasificación). El `_` final marca lo que solo existe después de `fit`. Con sol y nubes aprendió 1,52 por hora de sol, −4,2 con el cielo cubierto y 12,08 de base: casi la fórmula con la que se generaron los datos (1,5, −4 y 12). Solo con el sol, la nubosidad no era una entrada y su efecto medio se metió en el término independiente: con una nubosidad media de 0,54, 12 − 4 × 0,54 = 9,84; los 9,76 son eso más el ruido.
3. **Sobreajuste**: memoriza el ruido de los 30 puntos de entrenamiento. Lo delata la distancia entre los dos errores: bajísimo en entrenamiento, el peor en prueba. Ningún modelo baja de 3 porque es la desviación del ruido que se sumó a la recta: es azar, y el azar no se predice.
4. `test_size` dice qué parte va a prueba; `random_state` fija la semilla para que el reparto sea el mismo en cada ejecución; `stratify` mantiene la proporción de cada clase en las dos partes. Sin estratificar, según la semilla salían 7, 3 o 4 medidas altas en vez de 5: con 3, la prueba tenía casi la mitad de las que debía. No se reparte al azar cuando los datos tienen orden temporal y se quiere predecir el futuro, ni cuando hay medidas repetidas o muy parecidas (mismo sensor, mismo minuto): ahí se reparte por tiempo o por grupos (semana 32).
5. La **media de cada etiqueta** en el entrenamiento: es lo que hace mínimo el error al cuadrado de cada grupo. Numerarlas inventa un orden y unas distancias (el Sur "entre" el Norte y el Centro) y el modelo ajusta una recta que no corresponde a ninguna media (ejercicio 01, paso 5). Si ninguna zona difiere, las medias de cada una son casi la media de todas, y el modelo predice casi lo mismo que la referencia: no la mejora.
6. Errores 2, 2, 3 y 10. MAE = 17 / 4 = 4,25. RMSE = √(117 / 4) = 5,41. R² = 1 − 117 / 500 = 0,766 (la media es 25, y la suma de (real − 25)² es 225 + 25 + 25 + 225 = 500). RMSE mayor que MAE dice que hay errores grandes: el 10. R² es negativo cuando el modelo se equivoca más que predecir siempre la media; en entrenamiento, una regresión lineal no baja de 0, pero en prueba sí puede (sobreajuste, o una media de entrenamiento distinta de la de prueba).
7. Exactitud (3 + 14) / 20 = 0,85; precisión 3 / (3 + 2) = 0,60; exhaustividad 3 / (3 + 1) = 0,75; exactitud equilibrada = media de la exhaustividad de cada clase = (0,75 + 14/16) / 2 = (0,75 + 0,875) / 2 = 0,8125. Decir siempre "normal" acierta 16 de 20: exactitud 0,80, con exactitud equilibrada 0,5.
8. Una probabilidad por clase y fila, en el orden de `classes_` (alfabético); cada fila suma 1. Al bajar el umbral, el modelo dice "sí" más veces: sube la exhaustividad (se le escapan menos) y baja la precisión (más falsas alarmas). En el ejercicio 04, con un 4 % de fallos ninguna lectura llegaba a una probabilidad de 0,5 (la más alta era 0,14), así que `predict` decía siempre "no" aunque la probabilidad sí cambiara con la batería. `class_weight="balanced"` hizo que cada fallo pesara como unas 25 lecturas sin fallo: encontró 10 de los 12 fallos, con muchas falsas alarmas, y la exactitud equilibrada subió de 0,50 a 0,73.
9. Información que el modelo no tendría en la realidad y que se cuela al entrenar o al predecir; da métricas buenas y un modelo que falla con datos nuevos. El **objetivo disfrazado**: una entrada calculada del objetivo o conocida después (el valor para predecir el nivel). **Calcular con la prueba**: medias, escalas o categorías aprendidas con todas las medidas antes de repartir (la media de cada sensor). **El futuro y los repetidos**: medidas posteriores, o la misma medida a los dos lados del reparto. Los ejemplos de tu dominio, los tuyos. Las columnas one-hot solo deciden **qué** columnas existen a partir de las etiquetas; no usan el valor ni el nivel de ninguna medida, así que no dicen nada de la respuesta.
10. Porque una métrica sola no dice si el modelo aporta: un error de 20 o una exactitud de 0,50 pueden ser lo mismo que no saber nada. La referencia es "no saber nada" (la media, el nivel más frecuente), y un modelo útil tiene que mejorarla en prueba. Decide con la MAE porque está en la unidad del valor y se explica sin estadística, y con la exactitud equilibrada porque la exactitud premia acertar siempre el nivel más frecuente. "No mejora" no es un fallo: con los datos de ejemplo las zonas no difieren (semana 30), así que la etiqueta no lleva información para predecir. Es la conclusión correcta, y para predecir hacen falta otras entradas (semana 32).

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños y rojo a verde | Un commit por paso, sin cambiar los tests del bootcamp, cada uno con los ganchos; puede decir qué tests pasaron a verde con cada paso | 8 |
| La dependencia, bien fijada | scikit-learn 1.9.1 con `uv add`, threadpoolctl en 3.7.0 y la excepción de mypy solo para `sklearn.*`; sabe explicar por qué no se fija una versión de hace menos de dos semanas | 8 |
| Ejecución en vivo | Ante el instructor: `modelo` con su instantánea, con dos semillas distintas, y `pytest` en verde | 8 |
| Rompe y explica | Mete el valor en `features` y explica qué pasa con `modelo` y qué tests fallan; entrena con `x_test` y explica por qué las métricas siguen siendo buenas | 8 |
| Explica su modelo | Lee sus dos tablas: qué predice cada modelo, cuál es su referencia y por qué mejora o no; relaciona el resultado con su informe de la semana 30 | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 30

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| El módulo | `known` con las columnas y los niveles comprobados; `features` solo con la etiqueta; `split` con semilla y estratificado; `regress` y `classify` entrenando con el entrenamiento, midiendo en prueba y comparando con su referencia; sin reexportar `learning` en `core/__init__.py` | 25 |
| El comando | `modelo` con el import dentro, `--huella`, `--prueba` y `--semilla`, código 1 y 2 según el error, y las dos tablas con su veredicto | 15 |
| Tests propios | Al menos 6 tests en `tests/test_my_learning.py` con datos de su dominio, cada uno visto fallar con un mutante | 20 |
| Calidad | `pre-commit run --all-files`, `coverage report` y `alembic check` sin avisos; el gancho sin tocar los SVG; `docker compose run --rm app` y la CI en verde; imágenes `week-31` y versión `0.31.0` | 15 |
| Git y README | Rama `week-31` en `python-<nombre>-<apellido>`; README con la sección "Modelo", e `informe/README.md` con el resultado en "Siguientes pasos" | 10 |
| Pull request | Salidas, CI, `modelo` con su instantánea y su lectura, y la tabla de mutantes con las dos respuestas | 15 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | [Semana 32](../week-32-features_pipelines_validacion_cruzada_y_tuning/README.md) |
