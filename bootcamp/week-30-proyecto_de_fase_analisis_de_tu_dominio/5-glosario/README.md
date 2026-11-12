# Glosario — Semana 30

| Término | Definición |
|---|---|
| **Análisis confirmatorio** | Responder una pregunta decidida antes de ver los datos, con un método fijado. Sostiene una afirmación |
| **Análisis exploratorio** | Mirar los datos para tener ideas y encontrar problemas. No confirma nada |
| **Benjamini-Hochberg (BH)** | Corrección que controla la FDR: ordena los p, multiplica el de puesto k por m/k y no deja que suban desde abajo. `false_discovery_control(p, method="bh")` |
| **Bonferroni** | Corrección que controla la FWER multiplicando cada p por el número de pruebas. La más sencilla y la más estricta |
| **Comparaciones múltiples** | Hacer muchas pruebas a la vez. Con m pruebas sin diferencia, la probabilidad de algún falso positivo es 1 − (1 − α)^m |
| **FDR** | *False discovery rate*: la proporción de falsos positivos entre los hallazgos que publicas |
| **Forest plot** | Un gráfico con un punto y su intervalo por comparación, y una línea en el cero |
| **FWER** | *Family-wise error rate*: la probabilidad de publicar al menos un falso positivo entre todas las pruebas |
| **Hallazgo defendible** | Una afirmación con su tamaño, su incertidumbre y su escala: diferencia, intervalo y d |
| **Holm** | Corrección que controla la FWER como Bonferroni, pero nunca es peor y a veces es mejor |
| **Jardín de los senderos que se bifurcan** | Las muchas decisiones de un análisis; probar varias hasta que algo sale invalida el p-valor |
| **p corregido** | Un p-valor ajustado por todas las pruebas que se hicieron para la misma pregunta. Se compara con α como uno normal |
| **Paradoja de Simpson** | Una tendencia que se invierte al juntar grupos, por una variable de confusión repartida de forma distinta |
| **Prerregistro** | Escribir la pregunta y el método antes de ver los resultados. En el Observatorio, un commit con la sección Pregunta |
| **Robustez** | Que un hallazgo no cambie con una decisión razonable distinta: otra prueba, otra carga, sin atípicos |
| **Unidad de análisis** | Qué cuenta como un caso: una medida, un sensor, un día. Cambiarla puede cambiar la respuesta |
| **Variable de confusión** | Algo que influye en el valor y está repartido de forma distinta entre los grupos que comparas |

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
