# 05 · PCA, y tus modelos y grupos

⏱️ 45 min

## 🎯 Objetivos

- Explicar qué hace PCA: resumir muchas columnas en pocas, sin perder casi nada.
- Leer la varianza explicada y los pesos de cada componente.
- Usar PCA para dibujar datos con muchas columnas, o antes de agrupar.
- Leer `competir` y `agrupar` con tu instantánea.

---

## 1. Muchas columnas que dicen lo mismo

Treinta sensores con su perfil diario: la media de PM2.5 de cada hora, veinticuatro columnas. Hay tres tipos de sitio, como en el ejercicio 04. Pero veinticuatro columnas no se pueden dibujar, y muchas dicen casi lo mismo: si un sensor está alto a las 8, también lo está a las 9.

**PCA** (*análisis de componentes principales*) busca la dirección en la que los datos varían más: la **primera componente**. Después, la que más varía de lo que queda, sin repetir nada de la primera (perpendicular a ella): la **segunda**. Y así hasta tantas como columnas.

```python
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

rng = np.random.default_rng(5)
hours = np.arange(24)


def peak(center, width):
    return np.exp(-(((hours - center) / width) ** 2))


shapes = {
    "avenida": 15 + 20 * peak(8, 1.5) + 18 * peak(19, 1.5),
    "barrio": 12 + 16 * peak(21, 2.5),
    "parque": 9 + 2 * peak(14, 4),
}
kinds = pd.Series(np.repeat(list(shapes), 10), name="sitio")
profiles = pd.DataFrame(
    [shapes[kind] * rng.uniform(0.8, 1.2) + rng.normal(0, 1.5, 24) for kind in kinds],
    columns=[f"h{hour:02}" for hour in hours],
)
pca = PCA().fit(profiles)
ratios = pca.explained_variance_ratio_
print(f"varianza explicada: {ratios[:5].round(3)} · las dos primeras: {ratios[:2].sum():.3f}")
```

```
varianza explicada: [0.83  0.124 0.011 0.005 0.005] · las dos primeras: 0.954
```

`explained_variance_ratio_` dice qué parte de la variación total recoge cada componente. La primera, un 83 %; la segunda, un 12,4 %. Las dos juntas, un 95,4 %: los veinticuatro números de cada sensor se resumen en **dos**, casi sin perder nada. Las demás componentes recogen el ruido de cada hora.

Si prefieres decir cuánto quieres conservar en vez de cuántas componentes, `PCA(n_components=0.95)` se queda con las justas para llegar al 95 %: aquí, dos.

## 2. Qué significa cada componente

Cada componente es una mezcla de las columnas originales, con un peso para cada una (`components_`). Las horas que más pesan en las dos primeras:

```python
first = pd.Series(pca.components_[0], index=profiles.columns)
second = pd.Series(pca.components_[1], index=profiles.columns)
print("primera:", first.nlargest(3).round(2).to_dict())
print("segunda:", second.nlargest(2).round(2).to_dict(), second.nsmallest(2).round(2).to_dict())
```

```
primera: {'h08': 0.45, 'h19': 0.4, 'h09': 0.34}
segunda: {'h21': 0.55, 'h22': 0.54} {'h08': -0.25, 'h09': -0.21}
```

- La **primera** pesa sobre todo las 8, las 9 y las 19: las horas punta. Un sensor con valor alto en ella es uno con picos de tráfico.
- La **segunda** pesa a favor de las 21 y las 22, y en contra de las 8 y las 9: separa los sensores que suben de noche de los que suben por la mañana.

PCA no sabe qué es la hora punta: lo encuentra porque es lo que más varía entre sensores. Ponerle nombre a cada componente es cosa tuya, y no siempre se puede.

## 3. Dibujar y agrupar con menos columnas

Con dos componentes, cada sensor es un punto en un plano:

```python
plane = pd.DataFrame(PCA(2).fit_transform(profiles), columns=["pc1", "pc2"])
print(plane.groupby(kinds).mean().round(1).to_string())
```

```
          pc1   pc2
sitio              
avenida  39.0  -5.5
barrio   -8.5  15.8
parque  -30.5 -10.2
```

La avenida, a la derecha (picos de tráfico); el barrio, arriba (pico de noche); el parque, abajo a la izquierda. Con matplotlib (semana 27), un `scatter` de `pc1` frente a `pc2` muestra los tres grupos a la vista. Es el uso más común de PCA: **mirar** datos con muchas columnas.

Otros usos, y sus cuidados:

- **Antes de KMeans**, para quitar ruido: agrupar con las componentes que recogen el 95 % deja fuera el ruido de las demás. `make_pipeline(StandardScaler(), PCA(0.95), KMeans(3))`.
- **Escalar antes**: PCA busca dónde varían más los datos, y una columna con números más grandes varía más. Aquí todas son PM2.5, en la misma unidad, y no hace falta; con columnas en unidades distintas, sí.
- **No es un modelo de `y`**: PCA no mira la `y`. La dirección que más varía puede no ser la que predice. Para predecir, un bosque o un boosting eligen sus columnas solos.

## 4. Tu comando `competir`

El comando de esta semana mide los cinco modelos (la referencia, el lineal, un árbol, un bosque y un *gradient boosting*) con los mismos pliegues y la misma preparación de la semana 32. Con los datos de ejemplo:

```
$ uv run observatorio competir notebooks/instantanea.csv
instantanea.csv: 2000 medidas · sha256: 3193779438eecdede9910a3cbc922f05a883e69a8a92fd4ef9a33e482d636c65 · pliegues al azar
regresión del valor · MAE en cada pliegue
┏━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ Modelo     ┃      1 ┃      2 ┃      3 ┃      4 ┃      5 ┃  Media ┃   Gana ┃
┡━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│ referencia │ 20.275 │ 19.598 │ 19.820 │ 19.873 │ 20.209 │ 19.955 │        │
│ lineal     │ 20.366 │ 19.583 │ 19.807 │ 19.849 │ 20.227 │ 19.966 │ 3 de 5 │
│ árbol      │ 20.556 │ 19.718 │ 20.256 │ 20.080 │ 20.809 │ 20.284 │ 0 de 5 │
│ bosque     │ 21.139 │ 20.668 │ 20.496 │ 21.216 │ 21.165 │ 20.937 │ 0 de 5 │
│ boosting   │ 21.056 │ 20.740 │ 20.603 │ 21.060 │ 21.171 │ 20.926 │ 0 de 5 │
└────────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┘
regresión del valor: ningún modelo mejora la media de la referencia
...
clasificación del nivel: el mejor es bosque, gana en 3 de 5 pliegues: no mejora la referencia
```

Cómo leerlo:

- **"Media"** decide cuál es el mejor. Aquí, en la regresión, la referencia: ningún modelo predice el valor mejor que la media del entrenamiento.
- **"Gana"** dice en cuántos pliegues gana cada modelo a la referencia. El veredicto "mejora" pide que el mejor gane en **todos**, como en `ajustar`.
- **De más sencillo a más flexible, peor.** El lineal empata; el árbol, limitado a 4 niveles, pierde un poco; el bosque y el boosting, casi un punto. Sin señal, los modelos flexibles aprenden el ruido de cada entrenamiento (teoría 02, sección 5).
- **El lineal gana en 3 de 5** y aun así tiene peor media: por centésimas, a un lado o a otro. Es el mismo resultado que `ajustar` en la semana 32.

Con `--tiempo`, mira el árbol en el último pliegue: no extrapola (teoría 01, sección 5).

## 5. Tu comando `agrupar`

`agrupar` resume cada etiqueta en tres números (media, mediana y desviación de sus valores), los escala y los reparte en grupos con KMeans:

```
$ uv run observatorio agrupar notebooks/instantanea.csv
instantanea.csv: 2000 medidas · sha256: 3193779438eecdede9910a3cbc922f05a883e69a8a92fd4ef9a33e482d636c65
Grupos de etiquetas
┏━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Etiqueta ┃ Grupo ┃ Media ┃ Mediana ┃ Desviación ┃
┡━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━┩
│ Centro   │     1 │  38.2 │    38.7 │       23.1 │
│ Este     │     1 │  39.8 │    38.6 │       23.6 │
│ Norte    │     1 │  40.4 │    39.1 │       23.2 │
│ Oeste    │     1 │  39.3 │    37.9 │       22.8 │
│ Sur      │     2 │  40.7 │    41.8 │       22.8 │
└──────────┴───────┴───────┴─────────┴────────────┘
2 grupos · silueta 0.28: grupos que se solapan
```

- KMeans aparta el **Sur**: su mediana, 41,8, es la más alta. Pero mira las diferencias: de 37,9 a 41,8, con una desviación de 23 dentro de cada zona.
- Al **escalar**, esas pocas unidades se estiran hasta parecer distancias grandes. Escalar es necesario (teoría 04, sección 2), pero también agranda diferencias pequeñas.
- La **silueta**, 0,28, lo pone en su sitio: por debajo de 0,5, los grupos se solapan. Son las cinco zonas de la semana 30, que no se diferenciaban.

Cuatro semanas, cuatro formas de llegar a lo mismo con los datos de ejemplo: las comparaciones de la 30, el modelo de la 31, los pliegues de la 32 y los ensembles y los grupos de la 33. Con tus datos, el resultado puede ser otro: es lo que cuentas en el *pull request*.

## ⚠️ Errores comunes

| Error | Consecuencia | Mejor |
|---|---|---|
| PCA con columnas en unidades distintas, sin escalar | La primera componente es la columna con números más grandes | `StandardScaler` antes |
| Quedarse con dos componentes porque se dibujan bien | Pueden recoger poco | Mirar `explained_variance_ratio_` |
| Esperar que PCA mejore un modelo | No mira la `y`: puede quitar lo que predecía | Validación cruzada con y sin PCA |
| Ponerle nombre a cada componente siempre | A veces no lo tiene | Mirar `components_`, y decir "no se sabe" si no se sabe |
| Leer "mejor media" como "mejora" | Por centésimas, puede perder en la mitad de los pliegues | Mirar también en cuántos pliegues gana |
| Dar por buenos los grupos de `agrupar` | KMeans siempre encuentra grupos | Mirar la silueta |

## ✅ Qué debes saber al terminar

- Qué hace PCA, y qué dicen `explained_variance_ratio_` y `components_`.
- Para qué sirve reducir columnas: mirar, y quitar ruido antes de agrupar.
- Cuándo hay que escalar antes de PCA, y por qué PCA no sustituye a un modelo.
- Cómo leer la tabla de `competir`: la media, los pliegues que gana y el veredicto.
- Cómo leer `agrupar`: los grupos, los perfiles y la silueta.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [04 · Agrupar con KMeans](04-agrupar-con-kmeans.md) | **05 · PCA, y tus modelos y grupos** | [Ejercicio 01 · Árboles de decisión](../2-practicas/ejercicio-01-arboles-de-decision/README.md) |
