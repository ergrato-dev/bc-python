# Glosario — Semana 27

| Término | Definición |
|---|---|
| **Agg** | El *backend* de matplotlib que dibuja en memoria, sin pantalla: el que escribe los PNG |
| **Artista** | Todo lo que se ve en un gráfico de matplotlib: una línea, una barra, un texto, una marca. Guarda sus datos y su estilo |
| **`Axes`** | Un gráfico dentro de una figura: la zona de dibujo con sus ejes x e y, su título y su leyenda. No confundir con `Axis`, un solo eje |
| **Backend** | La parte de matplotlib que convierte una figura en píxeles, en un archivo o en una ventana |
| **Barra de color** | La leyenda de un mapa de calor: qué número corresponde a cada color. `figure.colorbar` |
| **Bootstrap** | Estimar la incertidumbre de una media remuestreando los datos al azar muchas veces. Lo usa seaborn para su `errorbar=("ci", 95)` |
| **CDN** | Un servidor que reparte archivos públicos, como plotly.js. Un HTML con `include_plotlyjs="cdn"` lo baja de ahí al abrirse |
| **Datos anchos** | Una tabla con una columna por grupo: la de `pivot` y la de `evolucion` |
| **Datos largos** | Una tabla con una fila por observación y una columna por variable (*tidy*). La piden seaborn y plotly express |
| **`Figure`** | El lienzo de matplotlib: el archivo o la ventana entera, con uno o varios `Axes` |
| **Función de ejes** | En seaborn, una que dibuja en los `Axes` que le das con `ax=`: `lineplot`, `histplot`... |
| **Función de figura** | En seaborn, una que crea su propia figura y devuelve un `FacetGrid`, con paneles: `relplot`, `displot`, `catplot` |
| **Intervalo de confianza** | El rango donde probablemente está el valor real de una media, a partir de una muestra. La semana 28 lo explica a fondo |
| **Kaleido** | El paquete que convierte figuras de plotly en PNG, SVG o PDF con un navegador Chrome |
| **`layout`** | En plotly, todo lo que no son datos: títulos, ejes, leyenda, formas y anotaciones |
| **Mapa de calor** | Una cuadrícula en la que el color de cada casilla es un número: `imshow` |
| **`MPLCONFIGDIR`** | La carpeta donde matplotlib guarda su configuración y su caché de fuentes; tiene que poder escribir en ella |
| **Paleta** | El conjunto de colores de un gráfico: categórica (grupos), secuencial (cantidad) o divergente (cantidad con un centro) |
| **plotly.js** | La biblioteca de JavaScript que dibuja los gráficos de plotly en el navegador |
| **`pyplot`** | La interfaz de matplotlib con estado global: dibuja en "la figura actual" y guarda una lista de figuras abiertas |
| **`rc_context`** | Cambia `rcParams` solo dentro de un `with` |
| **`rcParams`** | El diccionario global de matplotlib con los valores por defecto de todos los gráficos |
| **Small multiples** | Muchos gráficos pequeños iguales, uno por grupo, con la misma escala |
| **`svg.fonttype`** | Cómo guarda matplotlib el texto en un SVG: `"path"` (formas, por defecto) o `"none"` (texto que se puede buscar) |
| **`svg.hashsalt`** | Fija la parte al azar de los identificadores de un SVG de matplotlib, para que salga igual dos veces |
| **Traza** | En plotly, una serie de datos con su tipo y su estilo; `px.line` con `color=` crea una por grupo |
| **Viridis** | Paleta secuencial de matplotlib que se lee igual con daltonismo y en blanco y negro |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
