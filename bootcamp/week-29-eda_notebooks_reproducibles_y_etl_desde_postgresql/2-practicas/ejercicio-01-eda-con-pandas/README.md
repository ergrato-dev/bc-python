# Ejercicio 01 — EDA con pandas

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-analisis-exploratorio.md)

## Objetivo

Recorrer una tabla que no conoces con el orden de la teoría 01, y encontrar los cuatro problemas que esconde:

- forma y tipos;
- lo que falta;
- etiquetas mal escritas y filas repetidas;
- un valor que significa "sin dato";
- distribuciones por grupo, atípicos y relaciones.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-29-eda_notebooks_reproducibles_y_etl_desde_postgresql/2-practicas/ejercicio-01-eda-con-pandas/starter
uv run python main.py
```

```
Ejercicio 01 · Análisis exploratorio con pandas
medidas.csv: 186 filas, 4 columnas
```

El principio de `main.py` genera `salida/medidas.csv`: 60 días de tres estaciones, con los problemas que tendrían unos sensores de verdad. No leas cómo se genera: el ejercicio es encontrarlos mirando los datos. `salida/` no va a Git.

## Pasos

### 1. Forma y tipos

Descomenta el **PASO 1** y ejecuta:

```
        fecha estacion  temperatura  humedad
0  2026-03-01    Norte         13.4     84.0
1  2026-03-02    Norte          NaN     75.0
2  2026-03-03    Norte         13.9     84.0
{'fecha': <StringDtype(storage='python', na_value=nan)>, 'estacion': <StringDtype(storage='python', na_value=nan)>, 'temperatura': dtype('float64'), 'humedad': dtype('float64')}
de 2026-03-01 a 2026-04-29
```

- `fecha` llega como texto (`StringDtype`): un CSV no guarda tipos. `pd.to_datetime` con `format` la convierte, y después `min()` y `max()` son fechas de verdad.
- Ya ves un hueco en la segunda fila (`NaN`).

### 2. Lo que falta

Descomenta el **PASO 2** y ejecuta:

```
{'fecha': 0, 'estacion': 0, 'temperatura': 9, 'humedad': 0}
filas con algún hueco: 9 de 186
       temperatura  humedad
count        177.0    186.0
mean          33.9     96.5
std           21.8    134.2
min           11.7     63.0
25%           18.0     74.0
50%           21.7     77.0
75%           62.1     81.0
max           72.7    999.0
```

- Nueve temperaturas faltan. `humedad`, según `isna()`, está completa.
- Pero `describe()` dice otra cosa: una humedad máxima del **999 %**. Y una temperatura media de 33,9 °C en marzo, con la mitad de los días por debajo de 21,7 y un cuarto por encima de 62. Apunta las dos cosas: son dos de los cuatro problemas.

### 3. Etiquetas mal escritas y filas repetidas

Descomenta el **PASO 3** y ejecuta:

```
{'Este': 61, 'Sur': 58, 'Norte': 54, 'Sur ': 4, 'norte ': 3, 'NORTE': 3, 'sur': 3}
{'Sur': 65, 'Este': 61, 'Norte': 60}
filas repetidas: 6
quedan 180 filas, 0 días repetidos
```

- Siete etiquetas para tres estaciones. `str.strip().str.title()` quita los espacios de los extremos y deja cada palabra con la primera letra en mayúscula.
- `duplicated()` marca 6 filas iguales a una anterior. Las quitas, y la segunda comprobación confirma lo importante: queda un solo día por estación (180 = 60 × 3).
- Normaliza **antes** de buscar repetidos: con "Sur" y "sur" distintos, dos filas repetidas no parecerían iguales.

### 4. Un valor que significa "sin dato"

Descomenta el **PASO 4** y ejecuta:

```
{86.0: 4, 88.0: 2, 999.0: 4}
humedad: máximo 88 %, huecos 4
```

- Los tres valores más altos de `humedad`: entre 88 y 999 no hay nada. El 999 es lo que escribe el sensor cuando no mide.
- `replace(999, np.nan)` lo convierte en un hueco de verdad: ahora `isna()` lo cuenta y la media lo ignora.

### 5. Distribuciones por grupo

Descomenta el **PASO 5** y ejecuta:

```
          count  mean  std   min   25%   50%   75%   max
estacion
Este       56.0  65.0  3.9  55.8  63.0  64.9  67.9  72.7
Norte      58.0  16.5  2.4  11.7  14.3  16.4  18.6  21.1
Sur        57.0  21.4  2.3  16.3  19.7  21.7  22.8  26.2
 11.7 –  21.9 ######################
 21.9 –  32.0 ######
 32.0 –  42.2
 42.2 –  52.4
 52.4 –  62.5 ###
 62.5 –  72.7 ##########
{'Este': 18.3, 'Norte': 16.5, 'Sur': 21.4}
```

- Por estación, el problema de la media de 33,9 °C se ve solo: el Este mide en **grados Fahrenheit**. 65 °F son 18,3 °C.
- El histograma de toda la tabla lo enseñaba también: dos montañas separadas por un hueco donde no hay ninguna medida.
- `where` deja cada temperatura como está salvo en el Este, donde la convierte: `(°F − 32) × 5 / 9`. Las tres medias ya son de marzo.

### 6. Atípicos y relaciones

Descomenta el **PASO 6** y ejecuta:

```
Tukey: fuera de [9.9, 27.3] hay 0 medidas
correlación temperatura-humedad, todo junto: -0.42
dentro de cada estación: {'Este': -0.64, 'Norte': -0.67, 'Sur': -0.58}
```

- Con las unidades ya corregidas, ninguna temperatura queda fuera de los límites de Tukey. Cambia el orden (pon este paso antes del 5) y verás que tampoco detecta los °F: el problema lo encontraste comparando grupos, no con una regla.
- Más calor, menos humedad. Dentro de cada estación la relación es más fuerte que con todo junto: las estaciones tienen niveles distintos, y mezclarlas la debilita.
- `groupby(...).corr()` da una matriz por estación; `xs("temperatura", level=1)` se queda con la fila de la temperatura de cada una.

Para terminar, escribe en un comentario al final de `main.py` los cuatro problemas, con una frase cada uno, como harías en las conclusiones de un notebook.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'pandas'` | Ejecuta con `uv run python main.py` dentro de `starter/` |
| `ValueError: time data ... doesn't match format` | Cambiaste el `format` de `to_datetime`: es `"%Y-%m-%d"` |
| `value_counts` sigue dando siete etiquetas | Normalizaste la columna sin asignarla: `frame["estacion"] = ...` |
| Las medias del paso 5 no cambian tras convertir | Calculaste sobre un `groupby` creado antes de la conversión: agrupa de nuevo |
| Tus números no coinciden con los del README | Cambiaste la semilla (`29`) o el código que genera la tabla |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Notebooks en un proyecto](../../1-teoria/05-notebooks-en-un-proyecto.md) | **Ejercicio 01 · EDA con pandas** | [Ejercicio 02 · Notebooks por dentro](../ejercicio-02-notebooks-por-dentro/README.md) |
