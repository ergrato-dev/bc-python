# Glosario — Semana 23

| Término | Definición |
|---|---|
| **`argsort`** | Las posiciones que ordenarían un array, de menor a mayor. Sirve para ordenar otro array igual sin perder las parejas |
| **Atípico** | Un valor muy alejado del resto. Con puntuaciones z, el que tiene \|z\| mayor que un umbral |
| **`axis`** | El eje por el que resume una función: `axis=0` hace desaparecer las filas y deja un resultado por columna |
| **Broadcasting** | La regla con la que NumPy opera arrays de formas distintas: comparadas por la derecha, cada eje debe ser igual o 1, y el 1 se estira sin copiar |
| **Copia** | Un array con su propio bloque de memoria. Lo dan las listas de posiciones, las máscaras y `.copy()` |
| **Cuartiles** | Los percentiles 25, 50 y 75 (Q1, Q2 y Q3). Q2 es la mediana; Q3 − Q1, el rango intercuartílico |
| **`ddof`** | Lo que se resta a `n` al calcular la desviación: 0 para la de la población (NumPy por defecto), 1 para la de la muestra (pandas por defecto) |
| **`default_rng`** | La forma recomendada de crear un generador de números aleatorios de NumPy, con su propia semilla |
| **Desbordamiento (*overflow*)** | Un resultado entero que no cabe en su `dtype` y da la vuelta sin aviso: en `int8`, 120 + 10 da −126 |
| **`dtype`** | El tipo de todos los elementos de un array: `float64`, `int64`, `bool`, `<U5`, `object`... |
| ***Fancy indexing*** | Elegir elementos con una lista de posiciones, como `a[[0, 3]]`. Da una copia |
| **`fromiter`** | Crea un array desde un generador, sin lista intermedia; con `count`, reserva la memoria de una vez |
| **Generador (aleatorio)** | El objeto que produce números aleatorios a partir de una semilla. Cada llamada lo avanza |
| **Histograma** | Los conteos de valores en intervalos iguales. `np.histogram` da los conteos y los bordes (uno más que conteos) |
| **`keepdims`** | Argumento de las funciones de resumen que conserva el eje reducido con tamaño 1, para que el resultado encaje con la tabla original |
| **Máscara** | Un array de `bool` que sale de una comparación. Sirve para contar, filtrar y asignar |
| **Mutante equivalente** | Un cambio en el código que no cambia lo que hace el programa. Ningún test puede matarlo |
| **NaN** | *Not a number*: el valor de coma flotante que representa un dato que falta. No es igual a nada y contagia los cálculos |
| **`NDArray`** | La anotación de tipos de un array de NumPy: `NDArray[np.float64]` |
| **`np.intp`** | El entero que usa NumPy para posiciones y conteos; `int64` en una máquina de 64 bits |
| **Percentil** | El valor por debajo del cual queda un porcentaje de los datos. `np.percentile` interpola entre valores |
| **Puntuación z** | A cuántas desviaciones de la media está un valor: `(valor − media) / desviación` |
| **`reshape`** | Cambia la forma de un array sin cambiar sus datos; casi siempre da una vista |
| **`RuntimeWarning`** | El aviso de NumPy ante una división por cero o una media de nada. No para el programa |
| **Semilla** | El número con el que nace un generador aleatorio. La misma semilla da la misma secuencia |
| **`shape`** | La forma de un array: el tamaño de cada eje, como `(7, 4)` |
| **`strides`** | Los bytes que hay que saltar en memoria para avanzar uno en cada eje. Con ellos un bloque se lee como tabla |
| **Subnormal** | Un número de coma flotante tan cercano a cero que pierde precisión, como `5e-324`. Dividir por él puede dar `inf` |
| ***Ufunc*** | Función universal: una función de NumPy que opera elemento a elemento en C, como `np.sqrt` o `np.maximum` |
| **Vista** | Un array que mira el bloque de memoria de otro, con otra forma o con un corte. Cambiarla cambia el original |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
