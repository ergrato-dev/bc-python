# Ejercicio 02 — Elegir el gráfico y contarlo bien

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-elegir-el-grafico-y-contarlo-bien.md)

## Objetivo

Ver con tus datos cómo un gráfico puede contar la verdad o exagerarla:

- barras que empiezan en cero, y barras que no;
- cinco líneas en un gráfico frente a cinco paneles;
- un mapa de calor con una paleta que se lee bien;
- la forma de una distribución, con cajas;
- una escala logarítmica para datos que crecen multiplicando.

Todo con matplotlib. Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-27-visualizacion_con_matplotlib_seaborn_y_plotly/2-practicas/ejercicio-02-elegir-el-grafico/starter
uv run python main.py
```

```
Ejercicio 02 · Elegir el gráfico
```

Son las mismas medidas del ejercicio 01: treinta días, cinco estaciones, una por hora y la semilla 27. Además, `days` son los tres primeros días con una columna por estación, y `by_station`, la media de cada estación. Los gráficos van a `salida/`. En cada paso, **abre los dos gráficos y compáralos** antes de leer la explicación.

## Pasos

### 1. Las barras empiezan en cero

Descomenta el **PASO 1** y ejecuta:

```
{'Norte': 18.1, 'Sur': 24.1, 'Este': 21.0, 'Oeste': 15.0, 'Centro': 20.0}
Sur / Oeste, de verdad: 1.6
Sur / Oeste, como se ve desde 14: 10.4
```

- Las mismas cinco medias, dibujadas dos veces. A la izquierda, el eje empieza en 0; a la derecha, en 14.
- Una barra se lee por su **longitud**. Desde cero, la del Sur mide 1,6 veces la del Oeste, como sus medias. Desde 14, mide 10,4 veces: el gráfico exagera la diferencia más de seis veces.
- Las barras empiezan **siempre** en cero. Si lo que importa es la diferencia, dibuja la diferencia, o usa puntos o una línea, que se leen por su **posición**.

### 2. Un panel por estación

Descomenta el **PASO 2** y ejecuta:

```
station              Norte   Sur  Este  Oeste  Centro
time
2026-11-01 00:00:00   15.6  20.0  17.4   10.2    14.6
2026-11-01 01:00:00   14.0  19.0  16.8    8.8    15.3
2026-11-01 02:00:00    NaN  21.4  15.8    9.3     NaN
paneles: 5 · mismos límites: True
```

- `02-todas-juntas.png` tiene cinco líneas que se cruzan. Para seguir una estación hay que buscar su color en la leyenda, y los huecos de una se esconden detrás de las otras.
- `02-un-panel-por-estacion.png` tiene un panel por estación, todos con el mismo eje x y el mismo eje y (`sharex`, `sharey`). Son ***small multiples***: cada línea se ve sola, y aun así se comparan, porque la escala es la misma.
- Si cada panel tuviera su propio eje y, el Oeste parecería tan caluroso como el Sur. `mismos límites: True` lo comprueba.
- Con un color basta: lo que distingue cada estación es el panel, y no hace falta leyenda.

### 3. Color para una cantidad

Descomenta el **PASO 3** y ejecuta:

```
días x horas: (30, 24) · huecos: 34
mapa de color: viridis · de 8.8 a 28.1
```

- Una tabla de 30 días × 24 horas, con la media de cada hora del Norte. `imshow` la dibuja como una cuadrícula y pinta cada casilla con un color según su valor: un **mapa de calor**.
- Se ve de un vistazo lo que con las líneas costaba: cada día se calienta a la misma hora. Los 34 huecos salen en blanco, sin color: no hay dato.
- `viridis` es una paleta **secuencial**: va de oscuro a claro sin saltos, se lee igual con daltonismo y en blanco y negro. Las paletas arcoíris, como `jet`, inventan fronteras donde cambia el tono.
- `colorbar` es la leyenda del color, con su unidad. Sin ella, el color no dice ningún número.

### 4. Cómo se reparten

Descomenta el **PASO 4** y ejecuta:

```
medianas en el gráfico: [17.9, 24.4, 21.1, 14.9, 20.0]
medianas de pandas:    [17.9, 24.4, 21.1, 14.9, 20.0]
```

- Un **diagrama de caja** resume cada grupo con cinco números: la línea del medio es la mediana; la caja va del cuartil 1 al 3, la mitad central de los datos; los bigotes llegan hasta 1,5 veces la altura de la caja, y lo que queda fuera se dibuja como puntos sueltos.
- Las medianas del gráfico son las de pandas: `boxplot` las calcula, y las líneas las guardan.
- Las barras del paso 1 enseñaban la media; las cajas enseñan además cuánto varía cada estación. Dos estaciones con la misma media pueden ser muy distintas.

### 5. Cuando los datos crecen multiplicando

Descomenta el **PASO 5** y ejecuta:

```
lluvia: mediana 0.98 · máximo 54.06
escalas: linear log
```

- `rain` son 2000 lluvias diarias inventadas: casi todas pequeñas y unas pocas enormes. La mitad no llega a 1 mm, y la mayor pasa de 54.
- Con escala lineal, casi todo cae en la primera barra, y el resto del gráfico está vacío.
- Con escala logarítmica, cada marca multiplica por 10 (0,1, 1, 10), y se ve la forma de los datos. Las barras deben tener **el mismo ancho en escala logarítmica**: por eso los límites salen de `np.geomspace` y no de `bins=40`.
- Úsala cuando importan las proporciones (el doble, la mitad) y no las diferencias, y dilo en el eje: quien no lo vea leerá mal el gráfico.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'matplotlib'` | Ejecuta con `uv run python main.py` dentro de `starter/` |
| `mismos límites: False` en el paso 2 | Falta `sharey=True` en `subplots` |
| El mapa de calor sale con los días al revés | Falta el `extent`, o tiene los números de y cambiados: va de 30,5 a 0,5 |
| `TypeError: boxplot() got an unexpected keyword argument 'tick_labels'` | Tienes una versión de matplotlib anterior a la 3.9: el `pyproject.toml` fija la 3.11.2 |
| `ValueError` con la escala logarítmica | Algún valor es 0 o negativo, y no tiene logaritmo: filtra con `rain[rain > 0]` |
| Los gráficos de dos pasos se ven iguales | Abres un archivo viejo: cada ejecución borra y rehace `salida/` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · matplotlib: figuras y ejes](../ejercicio-01-matplotlib-figuras-y-ejes/README.md) | **Ejercicio 02 · Elegir el gráfico** | [Ejercicio 03 · Gráficos con seaborn](../ejercicio-03-graficos-con-seaborn/README.md) |
