# 01 · Análisis exploratorio

⏱️ 50 min

## 🎯 Objetivos

- Explicar qué es un análisis exploratorio (EDA) y por qué va antes de cualquier media, gráfico o prueba.
- Recorrer una tabla nueva con un orden fijo: forma, tipos, huecos, etiquetas, repetidos, distribuciones, atípicos y relaciones.
- Distinguir un hueco de verdad (`NaN`) de un valor que significa "sin dato" (999, −1, "NA").
- Encontrar problemas que ninguna función encuentra sola, comparando grupos.
- Escribir hallazgos, no solo calcular.

---

## 1. Qué es explorar

Hasta ahora has calculado sobre datos que conocías: los escribías tú en `medidas.txt`. Con datos de verdad, lo primero no es calcular, es **mirar**. Un análisis exploratorio (EDA, *exploratory data analysis*) responde a una pregunta antes de todas las demás: ¿estos datos dicen lo que creo que dicen?

En el ejercicio 01 recibes 186 medidas de tres estaciones. Si calculas la media de temperatura sin mirar, sale 33,9 °C en marzo. El número es correcto, pero no significa nada: la tabla tiene cuatro problemas que lo estropean, y ninguna función de pandas te avisa de ellos.

Un EDA no es un procedimiento automático. Es una lista de preguntas que haces siempre en el mismo orden, para que no se te olvide ninguna:

| Pregunta | Herramienta |
|---|---|
| ¿Cuántas filas y columnas, de qué tipo? | `shape`, `dtypes`, `head` |
| ¿Qué falta, y dónde? | `isna().sum()`, por grupo |
| ¿Las etiquetas están bien escritas? | `value_counts()` |
| ¿Hay filas repetidas? | `duplicated()` |
| ¿Hay valores que significan "sin dato"? | `describe()`, `value_counts().sort_index()` |
| ¿Cómo se reparten los valores, en cada grupo? | `groupby(...).describe()`, histogramas |
| ¿Hay medidas fuera de lo normal? | cuartiles, regla de Tukey |
| ¿Qué variables se mueven juntas? | `corr()`, por grupo |

Empieza siempre con **preguntas** escritas: "¿qué estación es más calurosa?", "¿falta algún día?". El EDA te dice si los datos pueden responderlas.

## 2. Forma y tipos

```python
frame = pd.read_csv("salida/medidas.csv")
frame.shape          # (186, 4)
frame.dtypes         # fecha: str, estacion: str, temperatura: float64, humedad: float64
```

La primera sorpresa suele estar aquí. `fecha` llega como **texto**: un CSV no tiene tipos, y pandas solo convierte lo que reconoce como número. Hasta que no la conviertes, ordenar por fecha es ordenar por letras, y restar dos fechas da un error:

```python
frame["fecha"] = pd.to_datetime(frame["fecha"], format="%Y-%m-%d")
```

Pasa `format` siempre que lo sepas: sin él, pandas adivina, y "03/04" puede ser 3 de abril o 4 de marzo según la fila.

## 3. Lo que falta

```python
frame.isna().sum()                   # temperatura: 9, el resto 0
frame.isna().any(axis=1).sum()       # 9 filas con algún hueco
```

Que falte algo no es un error: los sensores fallan. Lo que importa es **dónde** falta. Si los huecos se reparten por igual entre estaciones, las medias siguen siendo comparables. Si una estación tiene el 30 % sin dato y las demás el 2 %, su media es de otros días, y compararla es comparar cosas distintas:

```python
frame["temperatura"].isna().groupby(frame["estacion"]).mean()
```

## 4. Valores que significan "sin dato"

`isna()` dice que a `humedad` no le falta nada. `describe()` dice otra cosa:

```
       temperatura  humedad
mean          33.9     96.5
std           21.8    134.2
max           72.7    999.0
```

Una humedad del 999 % no existe: es lo que escribe el sensor cuando no puede medir. Es un **valor centinela**, y para pandas es un número como cualquier otro: entra en la media y la sube de 76,7 a 96,5. Los centinelas habituales son 999, 9999, −1, 0 y textos como "NA", "-" o "n/d". Para encontrarlos, mira los extremos de cada columna:

```python
frame["humedad"].value_counts().sort_index().tail(3)    # {86.0: 4, 88.0: 2, 999.0: 4}
frame["humedad"] = frame["humedad"].replace(999, np.nan)
```

El caso contrario también existe: un texto que **no** es un hueco y pandas convierte en uno. `read_csv` trata como `NaN`, por defecto, 19 textos, entre ellos "NA", "null", "nan" y "N/A". Una estación llamada "NA" (Norteamérica) desaparece al leer el archivo. Si tus datos pueden tener esos textos, desactívalo y di qué es un hueco en cada columna:

```python
pd.read_csv(path, keep_default_na=False, na_values={"valor": [""]})
```

Así lee la instantánea tu notebook del proyecto (teoría 05).

## 5. Etiquetas y repetidos

```python
frame["estacion"].value_counts()
# {'Este': 61, 'Sur': 58, 'Norte': 54, 'Sur ': 4, 'norte ': 3, 'NORTE': 3, 'sur': 3}
```

Tres estaciones, siete etiquetas. Para pandas, "Sur" y "Sur " (con un espacio al final) son grupos distintos, y un `groupby` daría siete medias. Normalizar es una línea, pero solo después de haberlo **visto**:

```python
frame["estacion"] = frame["estacion"].str.strip().str.title()
```

Las filas repetidas son el otro clásico: el sensor reintenta, el ETL se ejecuta dos veces. `duplicated()` marca cada fila igual a una anterior:

```python
frame.duplicated().sum()                          # 6
frame = frame[~frame.duplicated()]
frame.duplicated(["fecha", "estacion"]).sum()     # 0: un día por estación
```

La segunda comprobación es la importante: dos filas con la misma fecha y estación pero valores distintos no son repetidas para `duplicated()`, y aun así una de las dos sobra. Pregúntate qué columnas **deberían** identificar una fila, y comprueba que lo hacen.

## 6. Distribuciones por grupo

`describe()` sobre toda la tabla mezcla grupos. Por estación, el cuarto problema salta a la vista:

```
          count  mean  std   min   25%   50%   75%   max
estacion
Este       56.0  65.0  3.9  55.8  63.0  64.9  67.9  72.7
Norte      58.0  16.5  2.4  11.7  14.3  16.4  18.6  21.1
Sur        57.0  21.4  2.3  16.3  19.7  21.7  22.8  26.2
```

El Este no está 45 °C más caliente que el Norte: mide en **grados Fahrenheit**. 65 °F son 18,3 °C. Ninguna función de pandas puede saberlo; tú sí, porque conoces el dominio. El histograma de toda la tabla lo enseñaba también: dos montañas separadas por un hueco, cuando esperabas una.

Mira siempre la distribución de cada grupo, no solo su media: la forma (una montaña o dos, simétrica o con cola), el rango y la dispersión. La semana 27 te enseñó a dibujarla; la semana 28, a describirla.

## 7. Atípicos

Un atípico es una medida muy lejos de las demás. La **regla de Tukey** marca como atípico lo que queda a más de 1,5 rangos intercuartílicos del primer o del tercer cuartil:

```python
q1, q3 = frame["temperatura"].quantile([0.25, 0.75])
fence = 1.5 * (q3 - q1)
outside = frame[(frame["temperatura"] < q1 - fence) | (frame["temperatura"] > q3 + fence)]
```

Usa cuartiles y no la media y la desviación porque los cuartiles no se mueven con los propios atípicos. Y recuerda dos cosas:

- **Atípico no es error.** Un día de 40 °C en verano es raro y es real. Antes de quitar una medida, explica por qué es imposible, no solo rara.
- **Tukey no lo ve todo.** Con los grados Fahrenheit sin corregir, ninguna medida del Este queda fuera de los límites: hay tantas que el tercer cuartil sube hasta ellas. El problema lo encontraste comparando grupos, no con una regla.

## 8. Relaciones

```python
frame["temperatura"].corr(frame["humedad"])         # -0.42
frame.groupby("estacion")[["temperatura", "humedad"]].corr()   # -0.64, -0.67, -0.58
```

Cuando sube la temperatura baja la humedad, y dentro de cada estación la relación es más fuerte que con todo junto. Mezclar grupos con niveles distintos puede debilitar, esconder o incluso invertir una relación (la paradoja de Simpson). Calcula las relaciones también dentro de cada grupo.

La correlación mide solo relaciones **lineales**, y no dice nada de causas (teoría 04 de la semana 28): para ver la forma, dibuja el diagrama de dispersión.

## 9. Escribir lo que encuentras

Un EDA termina con texto, no con una celda de código. En el notebook de tu proyecto, cada sección acaba con un **hallazgo** en una celda de Markdown, y el notebook termina con unas conclusiones:

- qué responde y con qué datos (la carga, la fecha de la instantánea);
- qué problemas encontraste y qué hiciste con cada uno;
- qué **no** puede responder este análisis.

Un hallazgo es una frase que alguien puede comprobar: "el Este mide en °F: su media de 65,0 son 18,3 °C", no "hay datos raros".

## 10. Errores frecuentes

| Error | Consecuencia | Mejor |
|---|---|---|
| Calcular medias antes de mirar | Medias de datos con centinelas, unidades mezcladas o repetidos | El recorrido de la sección 1, siempre |
| Fiarse de `isna()` | Los 999 y los −1 entran en las medias | `describe()` y los extremos de cada columna |
| `read_csv` con sus valores por defecto | Una etiqueta "NA" se convierte en hueco | `keep_default_na=False` y `na_values` por columna |
| `describe()` de toda la tabla | Un grupo distinto se esconde en la mezcla | `groupby(...).describe()` |
| Quitar los atípicos porque sí | Borras lo más interesante de los datos | Explica por qué cada uno es imposible |
| Corregir sin dejar rastro | Nadie sabe qué cambiaste ni por qué | Cada corrección, con su hallazgo escrito |

## ✅ Qué debes saber al terminar

- El orden del recorrido: forma, tipos, huecos, centinelas, etiquetas, repetidos, distribuciones, atípicos y relaciones.
- Por qué un `NaN` y un 999 son cosas distintas para pandas, y por qué "NA" puede ser una etiqueta.
- Cómo encuentras un problema que ninguna función detecta: comparando grupos con lo que sabes del dominio.
- Qué es la regla de Tukey y por qué un atípico no es un error.
- Que un EDA termina con hallazgos escritos.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 29](../README.md) | **01 · Análisis exploratorio** | [02 · Notebooks y JupyterLab](02-notebooks-y-jupyterlab.md) |
