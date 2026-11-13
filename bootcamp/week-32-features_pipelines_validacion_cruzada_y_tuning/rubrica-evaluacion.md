# Rúbrica de Evaluación — Semana 32: features, pipelines, validación cruzada y tuning

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 31 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | ¿Qué hacen `fit` y `transform` en un transformador? ¿Qué aprende `StandardScaler`, y con qué parte de los datos? En la teoría 01, ¿por qué la temperatura 40 queda en 2,83 y no entre −1,34 y 1,34? | 10 |
| 2 | ¿Qué hace `OneHotEncoder` que no hace `get_dummies`? ¿Qué pasa con una categoría nueva con `handle_unknown="ignore"`, y sin él? ¿Por qué `prepare` sustituye a `features` de la semana 31? | 10 |
| 3 | ¿Qué hace un `Pipeline` en `fit` y en `predict`? ¿Qué significa `model__alpha`? ¿Qué pasa con las columnas que un `ColumnTransformer` no nombra? | 10 |
| 4 | En la teoría 02, `SelectKBest` antes de validar da 1,0 y dentro del pipeline 0,53, con datos al azar. ¿Por qué? Da otro paso de preparación que provocaría la misma fuga. | 10 |
| 5 | En la teoría 03, diez semillas dan R² entre 0,79 y 0,906. ¿Qué arregla la validación cruzada, y qué dicen la media y la desviación de los pliegues? ¿Por qué el modelo y la referencia deben medirse con los mismos pliegues? | 10 |
| 6 | En la teoría 03, el modelo de los sensores da R² 0,97 al azar y −0,08 con `GroupKFold`. ¿Qué cifra es la buena? ¿Cuándo se reparte por tiempo, qué necesita `TimeSeriesSplit` de las filas, y qué hace `ordered` en tu proyecto por eso? | 10 |
| 7 | ¿Qué diferencia un parámetro de un hiperparámetro? Con los coeficientes de Ridge de la teoría 04, explica qué hace `alpha`. ¿Qué tiene de especial `C` en la logística, y por qué hay que escalar antes de regularizar? | 10 |
| 8 | Lee la curva de validación de la teoría 04: ¿dónde sobreajusta, dónde no aprende y qué `alpha` elegirías? ¿Por qué los valores se prueban en potencias de 10? ¿Qué hace `GridSearchCV` después de elegir? | 10 |
| 9 | En la teoría 05, `best_score_` es 0,574 con datos al azar y la validación anidada da 0,462. ¿Por qué `best_score_` es optimista? ¿Cómo se escribe la anidada, y qué mide exactamente? | 10 |
| 10 | Con los datos de ejemplo, `ajustar` dice que la regresión gana en 3 de 5 pliegues con `alpha=100`, y la clasificación en 0 de 5 con `C=0.01`. ¿Por qué "no mejora"? ¿Qué dice que la búsqueda elija esos dos valores? ¿Es un fallo del modelo? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. `fit` aprende de los datos lo que el transformador necesita (una media, unas categorías) y lo guarda en atributos con `_`; `transform` lo aplica a cualquier tabla. `StandardScaler` aprende la media y la desviación de cada columna, **solo** con el entrenamiento: aprender con la prueba sería una fuga. 40 se escala con la media (21) y la desviación (6,71) del entrenamiento: (40 − 21) / 6,71 = 2,83. Queda fuera porque es más alto que cualquier medida de entrenamiento, y el modelo debe verlo así.
2. `OneHotEncoder` **aprende** las categorías del entrenamiento y transforma cualquier tabla con esas mismas columnas, en el mismo orden; `get_dummies` crea columnas con lo que ve cada vez, y la prueba puede salir con otras. Con `handle_unknown="ignore"`, una categoría nueva es una fila de ceros; sin él, `transform` lanza `ValueError: Found unknown categories`. `features` creaba las columnas con todas las medidas antes de repartir, y no sabía qué hacer con una etiqueta nueva; `prepare` se ajusta con el entrenamiento de cada pliegue, dentro del pipeline, y da ceros a una etiqueta que no vio.
3. En `fit`, ajusta cada paso con lo que sale del anterior (`fit_transform`) y al final entrena el modelo; en `predict`, pasa la tabla por los pasos ya ajustados (solo `transform`) y predice. `model__alpha` es el parámetro `alpha` del paso llamado `"model"`: el doble guion bajo separa el paso del parámetro. Las columnas que el `ColumnTransformer` no nombra se descartan sin aviso (`remainder="drop"`).
4. `SelectKBest` mira `y` para elegir columnas. Fuera del pipeline, elige con las sesenta filas, también las que luego serán prueba: se queda con las columnas que por casualidad se parecen a `y` **en esas filas**, y la validación las encuentra "útiles". Dentro, cada pliegue elige con su entrenamiento, y en prueba esas columnas no dicen nada: 0,53, el azar. Otros pasos que miran `y`: la media del objetivo por categoría, quitar "atípicos" según el objetivo, elegir umbrales con el objetivo.
5. Con un reparto, el resultado depende de qué medidas caen en prueba: ves uno de muchos números posibles. La validación cruzada mide k veces con k pruebas distintas que cubren todos los datos: la **media** estima cómo predice el modelo, y la **desviación** cuánto cambia entre repartos. Con los mismos pliegues, la diferencia entre el modelo y la referencia en cada pliegue es solo del modelo, no de que les tocaran medidas distintas; y se puede contar en cuántos gana.
6. Depende del uso: si vas a predecir medidas nuevas de sensores que ya tienes, 0,97; si vas a instalar sensores nuevos, −0,08, porque en prueba solo hay sensores que el modelo no vio. Por tiempo se reparte cuando las medidas tienen orden y quieres predecir las siguientes: entrenar con el futuro es hacer trampa. `TimeSeriesSplit` solo mira la posición de las filas, así que tienen que estar ordenadas por tiempo; `ordered` ordena por carga y posición antes de repartir.
7. Los parámetros los aprende `fit` (`coef_`, `intercept_`); los hiperparámetros los eliges tú antes, en el constructor. `alpha` castiga los pesos grandes: con 0,01, la regresión da pesos a las 27 entradas inútiles (0,29 de media); con 10, los encoge (0,16) y las útiles bajan poco; con 1000, todo es casi 0 y el modelo predice la media. En la logística, `C` es el **inverso** de la fuerza: `C` bajo regulariza mucho. Como el castigo depende del tamaño de los pesos, una entrada con números grandes tendría pesos pequeños y casi no se castigaría: hay que escalar para que todas cuenten igual.
8. Con `alpha` 0,01 a 1, R² 0,95 en entrenamiento y 0 a 0,30 en validación: sobreajusta. Con 100 y 1000, los dos bajan: no aprende. El mejor en validación es `alpha=10` (0,59). El efecto de `alpha` va por órdenes de magnitud: entre 10 y 11 no hay diferencia que medir, entre 1 y 10 sí. Después de elegir, `GridSearchCV` reentrena el mejor con **todos** los datos: `search.predict` usa ese modelo.
9. Es el mejor de treinta, medido con los mismos pliegues con los que se eligió: si todos son igual de malos, gana el que más suerte tuvo con esos pliegues, y su número es mejor que lo que hará con datos nuevos. La anidada mete la búsqueda dentro de otra validación cruzada: `cross_val_score(GridSearchCV(modelo, rejilla, cv=internos), x, y, cv=externos)`. Cada pliegue externo busca solo con su entrenamiento y mide con su prueba, que nadie usó para elegir. Mide el **procedimiento** (buscar y quedarse con el mejor), no un modelo concreto: cada pliegue puede elegir otro valor.
10. `ajustar` solo dice "mejora" si el modelo gana en **todos** los pliegues: ganar en tres de cinco, por centésimas, y perder en los otros dos es una diferencia del tamaño del ruido entre pliegues. Que elija la regularización más fuerte (`alpha=100`, `C=0.01`, los extremos de la rejilla) dice que lo mejor que encuentra es parecerse todo lo posible a la referencia: las entradas no llevan información. No es un fallo: es la tercera forma de llegar a la conclusión de las semanas 30 y 31 con los datos de ejemplo. Para predecir hacen falta otras entradas, o tus datos.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños y rojo a verde | Un commit por paso, sin cambiar los tests del bootcamp, cada uno con los ganchos; puede decir qué tests pasaron a verde con cada paso | 8 |
| El pipeline, sin fugas | Explica qué ajusta cada pliegue y por qué `prepare` devuelve un `ColumnTransformer` sin ajustar | 8 |
| Ejecución en vivo | Ante el instructor: `ajustar` con su instantánea, al azar y con `--tiempo`, y `pytest` en verde | 8 |
| Rompe y explica | Cambia `cross_val_score(search, ...)` por `cross_val_score(pipeline, ...)` y explica qué deja de medir; quita `handle_unknown="ignore"` y explica cuándo fallaría | 8 |
| Explica su modelo ajustado | Lee sus dos tablas: en cuántos pliegues gana, qué hiperparámetro elige y por qué, y qué cambia por tiempo; lo relaciona con su `modelo` de la semana 31 | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 31

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| El módulo | `ordered` con las columnas comprobadas y el orden de llegada; `prepare` sin ajustar y con `handle_unknown`; `folds` al azar con semilla o por tiempo; `validate` con la búsqueda dentro de cada pliegue y la referencia en los mismos pliegues; sin reexportar `validation` en `core/__init__.py` | 25 |
| El comando | `ajustar` con el import dentro, `--huella`, `--pliegues` y `--tiempo`, código 1 y 2 según el error, y las dos tablas con su media, el hiperparámetro elegido y el veredicto | 15 |
| Tests propios | Al menos 6 tests en `tests/test_my_validation.py` con datos de su dominio, cada uno visto fallar con un mutante | 20 |
| Calidad | `pre-commit run --all-files`, `coverage report` y `alembic check` sin avisos; `docker compose run --rm app` y la CI en verde; imágenes `week-32` y versión `0.32.0` | 15 |
| Git y README | Rama `week-32` en `python-<nombre>-<apellido>`; README con la sección "Modelo ajustado", e `informe/README.md` con el resultado en "Siguientes pasos" | 10 |
| Pull request | Salidas, CI, `ajustar` al azar y por tiempo con su lectura, y la tabla de mutantes con las dos respuestas | 15 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | [Semana 33](../week-33-arboles_ensembles_gradient_boosting_y_no_supervisado/README.md) |
