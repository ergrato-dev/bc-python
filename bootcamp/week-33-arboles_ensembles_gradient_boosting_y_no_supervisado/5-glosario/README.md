# Glosario — Semana 33

| Término | Definición |
|---|---|
| ***Bagging*** | Entrenar un modelo con cada una de muchas muestras con repetición y promediar sus predicciones. Baja la varianza |
| **Bosque aleatorio** | *Bagging* de árboles en el que cada corte mira solo algunas columnas al azar. `RandomForestRegressor` |
| ***Boosting*** | Modelos débiles en fila, cada uno corrigiendo el error de los anteriores. Baja el sesgo |
| **Codo** | El `k` a partir del cual la inercia apenas baja con más grupos |
| **Componente principal** | Una dirección de los datos, mezcla de las columnas originales; la primera es la que más varía. PCA |
| **Corte** | Una pregunta de un árbol: una columna y un umbral, como `viento <= 1.9` |
| ***Early stopping*** (parada temprana) | Parar de añadir árboles cuando una validación interna deja de mejorar. `n_iter_` dice cuántos se usaron |
| ***Gradient boosting*** | *Boosting* en el que cada árbol aprende el gradiente de la pérdida: con el error cuadrático, el residuo |
| **Hoja** | El final de un árbol: predice la media (o la clase más frecuente) de sus medidas de entrenamiento |
| **Importancia por impureza** | Cuánto baja el error cada corte con una columna, en el entrenamiento. `feature_importances_`. Premia las columnas con muchos valores |
| **Importancia por permutación** | Cuánto empeora el modelo al barajar una columna en la prueba. `permutation_importance` |
| **Impureza** | Lo mezcladas que están las medidas de un nodo: el error cuadrático en la regresión, el índice de Gini al clasificar |
| **Inercia** | La suma de las distancias al cuadrado de cada fila a su centro. `inertia_`. Baja siempre con más grupos |
| **KMeans** | Agrupa en `k` grupos asignando cada fila al centro más cercano y moviendo los centros a la media, hasta que nada cambia |
| ***Learning rate*** (ritmo de aprendizaje) | Qué parte de su corrección suma cada árbol de un *boosting*. Va junto con el número de árboles |
| **Muestra con repetición** (*bootstrap*) | Una muestra del mismo tamaño sacada con reemplazo: unas dos terceras partes de las filas, algunas repetidas |
| **No supervisado** | Aprender sin una `y` que acertar: agrupar, reducir columnas |
| ***Out-of-bag*** | Predecir cada medida solo con los árboles que no la vieron, y medir con eso. `oob_score=True` |
| **PCA** | Análisis de componentes principales: resume muchas columnas en pocas componentes. `explained_variance_ratio_` dice cuánto recoge cada una |
| **Residuo** | Lo que le falta a una predicción para acertar: `y - predicción` |
| **Silueta** | Para cada fila, (*b* − *a*) / máx(*a*, *b*), con *a* la distancia media a su grupo y *b* al más cercano. De −1 a 1. `silhouette_score` |
| **Varianza (de un modelo)** | Cuánto cambian sus predicciones si cambian los datos de entrenamiento. Un árbol sin límite tiene mucha |

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
