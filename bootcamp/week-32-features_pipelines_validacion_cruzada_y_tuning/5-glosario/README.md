# Glosario — Semana 32

| Término | Definición |
|---|---|
| **`ColumnTransformer`** | Aplica a cada grupo de columnas su transformador y pega los resultados. Lo que no nombra, lo descarta |
| **Curva de validación** | El error en entrenamiento y en validación para cada valor de un hiperparámetro. `validation_curve` |
| **Doble guion bajo** | Cómo se llega a un parámetro dentro de un pipeline: `model__alpha`, el paso y su parámetro |
| **Escalar** | Llevar una columna a media 0 y desviación 1 (`StandardScaler`), con la media y la desviación del entrenamiento |
| ***Feature*** (característica) | Cada columna de `X` tal como la recibe el modelo: casi nunca es la columna original |
| **`GridSearchCV`** | Prueba cada combinación de una rejilla con validación cruzada, elige la mejor y reentrena con todo |
| **`GroupKFold`** | Validación cruzada que deja todas las medidas de un grupo (un sensor, una zona) en el mismo pliegue |
| **Hiperparámetro** | Un valor que eliges antes de `fit`, en el constructor: `alpha`, `C`, `n_neighbors` |
| **Imputar** | Rellenar los huecos con un valor aprendido del entrenamiento. `SimpleImputer` |
| **`KFold`** | Reparte en k pliegues; con `shuffle=True` y `random_state`, mezcla antes de cortar, siempre igual |
| **One-hot con `OneHotEncoder`** | Una columna 0/1 por categoría aprendida en el entrenamiento. Con `handle_unknown="ignore"`, una nueva da todo ceros |
| **Optimismo de la selección** | Elegir el mejor de varios y medirlo con los mismos datos: sale mejor de lo que es. Le pasa a `best_score_` |
| **Pipeline** | Una cadena de transformadores y un modelo que se comporta como un solo estimador. Evita las fugas de la preparación |
| **Pliegue (*fold*)** | Cada una de las k partes de la validación cruzada. Cada pliegue prueba una vez |
| **`RandomizedSearchCV`** | Prueba un número fijo de combinaciones al azar, sacadas de una distribución |
| **Regularización** | Castigar los pesos grandes para que el modelo no aprenda el ruido. `alpha` en Ridge; `C`, al revés, en la logística |
| **Ridge** | Una regresión lineal con regularización: encoge los coeficientes según `alpha` |
| **`TimeSeriesSplit`** | Validación cruzada que prueba siempre con lo que viene después de su entrenamiento. Las filas, ordenadas |
| **Transformador** | Un objeto con `fit` (aprende de los datos) y `transform` (lo aplica): un escalador, un codificador |
| **Validación anidada** | La búsqueda de hiperparámetros dentro de cada pliegue de otra validación cruzada: mide sin el optimismo de elegir |
| **Validación cruzada** | Entrenar y medir k veces, cada vez con otro pliegue como prueba: una media y una desviación en vez de un número |

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
