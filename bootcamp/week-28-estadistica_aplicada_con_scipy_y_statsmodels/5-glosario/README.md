# Glosario — Semana 28

| Término | Definición |
|---|---|
| **ANOVA** | Análisis de la varianza: contrasta si alguna de varias medias de grupo difiere. Es una regresión con una variable de categorías. `stats.f_oneway`, `anova_lm` |
| **Benjamini-Hochberg** | Corrección para muchas pruebas que controla la proporción de falsos positivos entre lo que declaras positivo. `stats.false_discovery_control` |
| **Bonferroni** | Corrección para muchas pruebas: dividir α entre el número de pruebas. Simple y muy estricta |
| **Bootstrap** | Estimar la incertidumbre de un estadístico remuestreando con reemplazo tu propia muestra muchas veces. `stats.bootstrap` |
| **`cdf`** | Función de distribución acumulada: P(X ≤ x), el área a la izquierda de x |
| **Chi cuadrado** | Prueba de independencia entre dos variables de categorías, a partir de una tabla de conteos. `stats.chi2_contingency` |
| **d de Cohen** | Tamaño del efecto: la diferencia de medias dividida entre la desviación. 0,2 pequeña, 0,5 mediana, 0,8 grande |
| **Error de tipo I** | Rechazar una hipótesis nula cierta: un falso positivo. Su probabilidad es α |
| **Error de tipo II** | No rechazar una hipótesis nula falsa: un falso negativo. Su probabilidad es β |
| **Error estándar** | La desviación de un estadístico de muestra a muestra. Para la media, s / √n |
| **Grados de libertad** | Cuánta información queda para estimar la dispersión tras estimar otras cosas: n − 1 para una media |
| **Hipótesis nula (H₀)** | Lo que supones para calcular un p-valor, casi siempre "no hay diferencia" o "no hay relación" |
| **Intervalo de confianza** | Un rango construido con un método que, repetido muchas veces, contiene el valor de verdad en la proporción indicada (95 %) |
| **Intervalo de predicción** | El rango donde caerá un valor nuevo concreto, no su media. Más ancho que el de confianza. `obs_ci` en statsmodels |
| **Ley de los grandes números** | La media de una muestra se acerca a la de la población a medida que la muestra crece |
| **Mann-Whitney** | Prueba que compara dos grupos por los rangos de sus valores, no por sus medias. No supone una distribución. `stats.mannwhitneyu` |
| **Mínimos cuadrados (OLS)** | Ajustar un modelo lineal haciendo mínima la suma de los cuadrados de los residuos. `smf.ols` |
| **Muestra** | Las medidas que tienes, una parte de todas las posibles |
| **Nivel de significación (α)** | El umbral de p-valor fijado antes de mirar los datos por debajo del cual rechazas H₀. Casi siempre 0,05 |
| **p-valor** | Si H₀ fuera cierta, la probabilidad de ver un resultado tan extremo como el tuyo o más. No es la probabilidad de que H₀ sea cierta |
| ***p-hacking*** | Probar análisis hasta que uno da p < 0,05. Llena los resultados de falsos positivos |
| **`pdf` / `pmf`** | Densidad de una variable continua (la altura de la curva, no una probabilidad) / probabilidad de cada valor de una discreta |
| **Población** | Todas las medidas posibles, que casi nunca ves |
| **Potencia** | La probabilidad de detectar una diferencia que existe: 1 − β. Crece con n y con el tamaño de la diferencia |
| **`ppf`** | La inversa de `cdf`: el valor que deja una probabilidad dada a su izquierda |
| **Prueba de permutación** | Calcular un p-valor barajando las etiquetas de los grupos muchas veces. `stats.permutation_test` |
| **R²** | La fracción de la variación que explica un modelo de regresión |
| **Residuo** | Valor observado menos valor ajustado por el modelo |
| **Semilla** | El número que fija la secuencia de un generador aleatorio, para que se repita. `np.random.default_rng(28)` |
| **`sf`** | Función de supervivencia: P(X > x) = 1 − `cdf(x)`, sin perder precisión en las colas |
| **Tamaño del efecto** | Cuánto difieren los grupos, en unidades del dominio o sin unidades (d de Cohen). Lo que dice si una diferencia importa |
| **Teorema central del límite** | La media de n valores independientes se reparte casi como una normal, con desviación σ / √n, sea cual sea la distribución de partida |
| **t de Student (distribución)** | Como la normal, con colas más gruesas cuantos menos grados de libertad. La de una media medida en errores estándar |
| **Welch (prueba de)** | La prueba t para dos grupos que no supone la misma dispersión. `ttest_ind(..., equal_var=False)` |

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
