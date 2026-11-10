# Ejercicio 04 — plotly, y un gráfico con tres bibliotecas

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-plotly-graficos-interactivos.md) y [05](../../1-teoria/05-graficos-en-un-proyecto.md)

## Objetivo

Hacer gráficos que se exploran con el ratón, y decidir con números cuándo compensan:

- un gráfico de líneas con plotly y lo que enseña al pasar el ratón;
- qué es por dentro una figura de plotly;
- cuánto pesa un HTML, y qué cambia con `include_plotlyjs`;
- paneles y puntos con detalle;
- el mismo gráfico con matplotlib, seaborn y plotly: código, tamaño y tiempo de importar.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-27-visualizacion_con_matplotlib_seaborn_y_plotly/2-practicas/ejercicio-04-plotly-y-tres-bibliotecas/starter
uv run python main.py
```

```
Ejercicio 04 · plotly
```

Son las medidas de los ejercicios anteriores. `daily` tiene la media de cada estación cada día, en formato largo: una fila por estación y día. Los gráficos van a `salida/`; los `.html` se abren con el navegador.

## Pasos

### 1. Un gráfico que responde al ratón

Descomenta el **PASO 1** y ejecuta:

```
  station       time  value
0   Norte 2026-11-01  17.82
1   Norte 2026-11-02  18.03
2   Norte 2026-11-03  18.04
Figure · trazas: 5
nombres: ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']
Norte, primeros días: [17.82, 18.03, 18.04]
al pasar el ratón: station=Norte<br>time=%{x}<br>value=%{y}<extra></extra>
01-linea.html: 4831.2 kB
```

- `px.line` es **plotly express**: como seaborn, recibe una tabla larga y nombres de columna, y hace una **traza** (una serie de datos con su estilo) por cada valor de `color`.
- Abre `01-linea.html` en el navegador. Pasa el ratón por una línea: sale la estación, el día y el valor. Arrastra para ampliar una zona, haz doble clic para volver, y pulsa una estación en la leyenda para esconderla.
- `hovertemplate` es el texto de esa etiqueta: `%{x}` y `%{y}` los rellena el navegador. Lo dibuja **JavaScript**, no Python: el HTML lleva dentro la biblioteca plotly.js y tus datos.

### 2. Una figura es un diccionario

Descomenta el **PASO 2** y ejecuta:

```
claves: ['data', 'layout']
tipo de traza: scatter · modo: lines
eje y: temperatura (°C) · formas: 1
JSON: 14839 caracteres · f8
```

- Una figura de plotly son dos cosas: `data`, la lista de trazas, y `layout`, todo lo demás (títulos, ejes, leyenda, formas). Una línea es una traza `scatter` en modo `lines`.
- `update_layout` cambia el `layout` con nombres separados por `_`: `xaxis_title` es `layout.xaxis.title`. `add_hline` añade una **forma** (*shape*) y su texto.
- `to_json()` es lo que viaja al navegador. Los números van en binario (`f8`, `float` de 8 bytes) codificado en base64, no como texto: ocupan menos. Un `NaN` dejaría un hueco en la línea, igual que en matplotlib.

### 3. Lo que pesa un HTML

Descomenta el **PASO 3** y ejecuta:

```
03-completo.html: 4831.5 kB
03-cdn.html: 15.8 kB
de dónde baja plotly.js: https://cdn.plot.ly/plotly-4.1.1.min.js
write_image: Image export requires the Kaleido package, v1.0.0 or greater,
```

- Con `include_plotlyjs=True` (lo que hace `write_html` por defecto), el HTML lleva dentro los 4,8 MB de plotly.js: funciona sin internet, pero cada gráfico pesa casi 5 MB.
- Con `"cdn"`, el HTML pesa 16 kB y el navegador baja plotly.js de internet al abrirlo. Diez gráficos en una web comparten esa descarga; sin conexión, no se ve nada.
- Para un PNG o un PDF, plotly necesita **Kaleido**, otro paquete que dibuja con un navegador Chrome. matplotlib, en cambio, escribe PNG, SVG y PDF sin nada más.

### 4. Paneles y puntos con detalle

Descomenta el **PASO 4** y ejecuta:

```
trazas: 5 · puntos: 794
paneles: ['station=Oeste', 'station=Centro', 'station=Norte', 'station=Sur', 'station=Este']
paneles: ['Oeste', 'Centro', 'Norte', 'Sur', 'Este']
04-paneles.html: 42.9 kB
```

- `facet_col` hace un panel por estación, como `relplot` de seaborn; `facet_col_wrap=3`, tres por fila.
- `hover_data` decide qué sale al pasar el ratón y con qué formato: el valor con un decimal y la fecha como `04 Nov 15:00`.
- El título de cada panel es una **anotación** del `layout`. Salen en el orden en que plotly los coloca, empezando por la fila de abajo. `for_each_annotation` cambia todos a la vez: aquí quita el `station=`.
- 794 puntos de una semana caben bien. Con un millón, el navegador iría lento, y el HTML pesaría decenas de megas: para muchos datos, resume antes de dibujar.

### 5. Un gráfico, tres bibliotecas

Descomenta el **PASO 5** y ejecuta:

```
05-matplotlib.png: 72.9 kB
05-seaborn.png: 73.4 kB
05-plotly.html: 15.8 kB
importar matplotlib.figure: 0.36 s
importar seaborn: 0.57 s
importar plotly.express: 0.14 s
```

Los tiempos son los de la máquina del bootcamp: los tuyos serán otros.

- El mismo gráfico tres veces. Con matplotlib, un bucle por estación y una leyenda a mano; con seaborn, una llamada con `hue`, sobre la tabla larga; con plotly, la figura del paso 2.
- Los dos PNG pesan lo mismo, porque los dos los dibuja matplotlib: seaborn es una capa encima. El HTML con CDN pesa menos, pero necesita internet y un navegador.
- seaborn tarda más en importarse porque al importarse carga matplotlib, pandas y sus propios módulos de estadística. plotly carga poco al importar, y deja el trabajo para cuando dibujas.

| Necesitas | Usa |
|---|---|
| Un PNG, SVG o PDF desde un programa, un test o Docker | matplotlib, con `Figure` |
| Explorar un análisis rápido, con estadística y paneles | seaborn |
| Que otra persona explore los datos en el navegador | plotly |

Cuando acabes, borra `salida/`: los dos HTML completos son casi 10 MB.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'plotly'` | Ejecuta con `uv run python main.py` dentro de `starter/` |
| El HTML del paso 3 con `cdn` sale en blanco | Necesita internet para bajar plotly.js; el completo funciona sin conexión |
| `ValueError: Value of 'color' is not the name of a column` | Le pasaste una tabla ancha: plotly express, como seaborn, quiere la larga |
| `RuntimeError: Image export requires the Kaleido package` | Es lo esperado en el paso 3: no instalamos Kaleido. Usa `write_html`, o matplotlib para imágenes |
| Los paneles del paso 4 salen en otro orden | Es el orden de las anotaciones, no el de los paneles: en el gráfico, Norte sigue arriba a la izquierda |
| Tus tiempos del paso 5 son muy distintos | La primera importación de cada biblioteca, recién instalada, es más lenta: ejecuta otra vez |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Gráficos con seaborn](../ejercicio-03-graficos-con-seaborn/README.md) | **Ejercicio 04 · plotly, y tres bibliotecas** | [Proyecto · Dibujar la evolución](../../3-proyecto/README.md) |
