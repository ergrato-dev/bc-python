# Glosario — Semana 31

| Término | Definición |
|---|---|
| **Aprendizaje supervisado** | Ajustar un modelo con ejemplos que traen la respuesta correcta, para predecir la de casos nuevos |
| **Clasificación** | Predecir una categoría: el nivel, si habrá aviso. `LogisticRegression` |
| **Clase desequilibrada** | Una clase mucho menos frecuente que otra. La exactitud la ignora; la exactitud equilibrada, no |
| **`class_weight="balanced"`** | Hace que cada clase pese lo mismo al aprender, aunque tenga menos casos |
| **Entradas (*features*)** | Lo que el modelo sabe de cada caso antes de predecir. Forman `X`, con dos dimensiones |
| **Entrenamiento** | La parte de los datos que ve `fit` |
| **Estimador** | Un objeto de scikit-learn con `fit`. Los modelos y las referencias lo son |
| **Estratificar** | Repartir manteniendo la proporción de cada clase en las dos partes. `stratify=y` |
| **Exactitud (*accuracy*)** | Qué parte de las predicciones acierta. Engaña con clases desequilibradas |
| **Exactitud equilibrada** | La media de la exhaustividad de cada clase. Con k clases, la referencia da 1/k |
| **Exhaustividad (*recall*)** | De los casos de una clase, cuántos encuentra el modelo. VP / (VP + FN) |
| **F1** | La media armónica de precisión y exhaustividad. Solo es alta si las dos lo son |
| **`fit`** | El método que aprende de los ejemplos. Devuelve el propio estimador |
| **Fuga de datos (*leakage*)** | Información que el modelo no tendría en la realidad y que se cuela al entrenar o al predecir. Da métricas buenas y modelos inútiles |
| **Infraajuste (*underfitting*)** | Un modelo demasiado simple: se equivoca mucho en entrenamiento y en prueba |
| **MAE** | Error absoluto medio: cuánto se equivoca de media, en la unidad del objetivo |
| **Matriz de confusión** | Tabla de casos por clase real (filas) y predicha (columnas). La diagonal son los aciertos |
| **Media macro** | La media de una métrica en todas las clases, con el mismo peso |
| **Objetivo (*target*)** | Lo que se predice: el valor, el nivel. Forma `y`, con una dimensión |
| **One-hot** | Una columna 0/1 por cada valor de una etiqueta. `pd.get_dummies` |
| **Precisión (*precision*)** | De las veces que el modelo dice una clase, cuántas acierta. VP / (VP + FP) |
| **`predict_proba`** | La probabilidad de cada clase, en el orden de `classes_` |
| **Prueba** | La parte de los datos que el modelo no ve al entrenar, y con la que se mide |
| **R²** | Qué parte de la variación explica el modelo. 1 es perfecto, 0 es predecir la media, negativo es peor que ella |
| **`random_state`** | La semilla del azar en scikit-learn: con la misma, el mismo resultado |
| **Referencia (*baseline*)** | Un modelo que ignora las entradas: la media o la clase más frecuente. Todo modelo debe mejorarla |
| **Regresión** | Predecir un número: el valor. `LinearRegression` |
| **Regresión logística** | Un clasificador que da una probabilidad por clase con una curva en S |
| **Residuo** | Lo real menos lo predicho, en cada caso |
| **RMSE** | Raíz del error cuadrático medio. En la unidad del objetivo, castiga más los errores grandes |
| **Sobreajuste (*overfitting*)** | Un modelo que memoriza el ruido del entrenamiento: error bajo ahí, alto en prueba |
| **Umbral** | La probabilidad a partir de la cual se predice una clase. 0,5 por defecto, elegible según el coste de cada error |

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
