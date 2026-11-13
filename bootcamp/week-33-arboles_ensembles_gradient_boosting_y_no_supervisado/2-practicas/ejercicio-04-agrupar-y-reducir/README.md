# Ejercicio 04 — Agrupar y reducir

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-agrupar-con-kmeans.md) y [05](../../1-teoria/05-pca-y-tus-modelos-y-grupos.md)

## Objetivo

Encontrar grupos en unos datos que no dicen a qué grupo pertenece cada fila, y comprobar si existen:

- cuarenta perfiles diarios de sensores, sin etiqueta;
- tres grupos con KMeans, comparados con la respuesta que KMeans no vio;
- cuántos grupos, con la inercia y la silueta;
- una columna en otra escala, que lo estropea todo;
- de 24 columnas a 2, con PCA;
- grupos en datos que no tienen ninguno.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-33-arboles_ensembles_gradient_boosting_y_no_supervisado/2-practicas/ejercicio-04-agrupar-y-reducir/starter
uv run python main.py
```

```
Ejercicio 04 · Agrupar y reducir
40 sensores · 24 horas por perfil
```

Otros datos: cuarenta sensores de PM2.5, cada uno con su **perfil**, la media de cada hora del día (`h00` a `h23`). Hay tres tipos de sitio: junto a una avenida, en un barrio o en un parque. `kinds` guarda el tipo de cada sensor, pero KMeans no lo verá: solo sirve para comprobar después.

Tus salidas coinciden con las del README si descomentas los pasos **en orden**: los pasos 4 y 6 sacan números del mismo generador que los datos.

## Pasos

### 1. Mirar los perfiles

Descomenta el **PASO 1** y ejecuta:

```
            h03   h08   h14   h19   h21
sensor 01  10.1   6.6  12.9   8.1   7.2
sensor 02  13.8  11.8  11.1  20.3  31.3
sensor 03  10.5  10.6  10.5  17.0  23.4
sensor 04  12.1  12.3  11.5  20.1  27.4
sensor 05   9.4   8.1  11.1  14.0  11.3
sensor 06  11.2  10.1  13.9   9.3   9.3
```

Cinco horas de las veinticuatro. Los sensores 02, 03 y 04 suben por la noche (21 h): parecen de barrio. El 01, el 05 y el 06 son bajos todo el día: parque. Con cuarenta sensores y veinticuatro columnas, a ojo no se puede.

### 2. Tres grupos

Descomenta el **PASO 2** y ejecuta:

```
grupo     0   1   2
sitio              
avenida   0  13   0
barrio   15   0   0
parque    0   0  12
```

`KMeans(3)` reparte los cuarenta perfiles en tres grupos sin saber el tipo de sitio. `pd.crosstab` cruza su respuesta con la de verdad: cada tipo cae entero en un grupo. KMeans ha encontrado los tres tipos de sitio solo con la forma del día.

Los números de grupo (0, 1, 2) no significan nada: con otra semilla, el barrio podría ser el 2. Por eso el proyecto los renumera.

### 3. ¿Cuántos grupos?

Descomenta el **PASO 3** y ejecuta:

```
k=2 · inercia   12367 · silueta 0.56
k=3 · inercia    4443 · silueta 0.62
k=4 · inercia    3089 · silueta 0.57
k=5 · inercia    2261 · silueta 0.48
k=6 · inercia    2047 · silueta 0.43
```

Aquí sabías que eran tres; normalmente no lo sabes.

- **La inercia**, la suma de las distancias al cuadrado de cada perfil a su centro, baja **siempre** con más grupos: con cuarenta grupos sería 0. De 2 a 3 cae a un tercio; después, mucho menos. Ese "codo" en el 3 es una pista.
- **La silueta** compara, para cada perfil, la distancia a los de su grupo con la distancia al grupo más cercano. Va de −1 a 1, y es más alta con 3: grupos compactos y separados.

### 4. Una columna en otra escala

Descomenta el **PASO 4** y ejecuta:

```
sin escalar:
grupo    0  1  2
sitio           
avenida  4  7  2
barrio   2  6  7
parque   3  5  4
escalando:
grupo     0   1   2
sitio              
avenida   0  13   0
barrio   15   0   0
parque    0   0  12
```

Una columna más: la altitud de cada sensor, entre 0 y 2500 metros, al azar.

- **Sin escalar**, KMeans reparte por altitud: una diferencia de cientos de metros pesa más que todo el perfil, que se mueve en decenas. Los tres tipos de sitio, mezclados en los tres grupos.
- **Escalando**, cada columna pesa lo mismo: la altitud es una de veinticinco, y los grupos vuelven.

KMeans mide distancias: escala siempre antes, como en la regularización de la semana 32.

### 5. De 24 columnas a 2

Descomenta el **PASO 5** y ejecuta:

```
varianza explicada: [0.738 0.202 0.011 0.006 0.005]
          pc1   pc2
avenida  31.4  -7.6
barrio   -5.8  15.8
parque  -26.8 -11.5
```

`PCA` busca las direcciones en las que más varían los perfiles. La primera explica un 73,8 % de la variación; la segunda, un 20,2 %. Entre las dos, un 94 %: las veinticuatro horas se resumen en **dos** números por sensor, casi sin perder nada. Las demás componentes son ruido.

La media de cada tipo en ese plano: la avenida, a la derecha en `pc1` (sus dos picos); el barrio, arriba en `pc2` (su pico de noche); el parque, abajo a la izquierda. Con dos columnas, se puede dibujar: un punto por sensor, y los tres grupos se ven.

### 6. Grupos en el ruido

Descomenta el **PASO 6** y ejecuta:

```
ruido: grupos de [8, 19, 13] sensores · silueta 0.04
```

Cuarenta perfiles al azar, todos con la misma media: no hay grupos. KMeans devuelve tres igual, de 8, 19 y 13 sensores, porque se los pides. La silueta, 0,04, dice que no significan nada.

KMeans **siempre** encuentra k grupos. La silueta es lo que te dice si existen.

Para terminar, escribe en un comentario al final de `main.py` qué perfil usarías para agrupar las etiquetas de tu dominio y cuántos grupos esperarías.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| Tus números de los pasos 4 o 6 no coinciden | Descomentaste en otro orden: los dos usan el mismo generador que los datos |
| Los grupos del paso 2 salen con otros números | Falta `random_state=33`: cambia el número de cada grupo, no el reparto |
| `ValueError: Number of labels is 1` | La silueta necesita al menos 2 grupos |
| `ValueError: n_samples=40 should be >= n_clusters=50` | No puede haber más grupos que filas |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Gradient boosting](../ejercicio-03-gradient-boosting/README.md) | **Ejercicio 04 · Agrupar y reducir** | [Proyecto · Árboles, ensembles y grupos](../../3-proyecto/README.md) |
