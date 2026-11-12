# Ejercicio 03 — Un gráfico por afirmación

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-el-informe-desde-el-codigo.md)

## Objetivo

Pasar de un gráfico que describe a uno que prueba una frase, y guardarlo de forma reproducible:

- barras de medias, y por qué no responden a "¿qué zonas difieren?";
- un *forest plot*: cada diferencia con su intervalo y una línea en el cero;
- un título que dice la conclusión, calculada de los datos;
- el mismo SVG dos veces, con y sin fecha y sal;
- el texto del SVG como texto, no como trazos.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas, comparas y **abres los SVG** de `salida/` en tu navegador o en VS Code. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-30-proyecto_de_fase_analisis_de_tu_dominio/2-practicas/ejercicio-03-un-grafico-por-afirmacion/starter
uv run python main.py
```

```
Ejercicio 03 · Un gráfico por afirmación
{'Centro': 20.62, 'Norte': 20.78, 'Sur': 27.44, 'Este': 19.47, 'Oeste': 24.5}
```

Cinco zonas con 40 medidas cada una. La pregunta: ¿qué zonas difieren de Centro? Los gráficos usan `Figure`, sin `pyplot`, como `core/charts.py` (semana 27).

## Pasos

### 1. Barras de medias

Descomenta el **PASO 1** y ejecuta:

```
salida/1-barras.svg: ¿qué zonas difieren de Centro?
```

Abre `salida/1-barras.svg`. El Sur y el Oeste son más altos, pero ¿difieren de verdad, o es el azar de 40 medidas? El gráfico no lo puede decir: no tiene la incertidumbre. Y obliga a comparar alturas de barras separadas, a ojo.

### 2. Cada diferencia, con su intervalo

Descomenta el **PASO 2** y ejecuta:

```
Norte - Centro: 0.16 [-2.47, 2.79]
Sur - Centro: 6.82 [4.15, 9.49]
Este - Centro: -1.15 [-3.86, 1.57]
Oeste - Centro: 3.89 [1.07, 6.71]
salida/2-diferencias.svg
```

Abre `salida/2-diferencias.svg`. Ahora la pregunta se responde mirando una sola cosa: qué intervalos cruzan la línea del cero. Norte y Este la cruzan; Sur y Oeste no.

- `xerr=[below, above]`: cuánto se extiende cada barra a la izquierda y a la derecha del punto.
- `axes.invert_yaxis()`: el primer par arriba. Coméntala y vuelve a ejecutar: el orden se invierte.

### 3. El título es la conclusión

Descomenta el **PASO 3** y ejecuta:

```
salida/3-conclusion.svg: 2 de 4 zonas difieren de Centro: Sur, Oeste
```

El título se **calcula** con los mismos intervalos que dibuja el gráfico: no puede contradecirlo. Si cambias la semilla (`30`) y vuelves a ejecutar, el título cambia solo.

Aquí son cuatro comparaciones sin corregir, para centrarte en el gráfico. En tu Observatorio, `headline` cuenta los pares con su p **corregido** (teoría 03).

### 4. El mismo gráfico, dos veces

Descomenta el **PASO 4** y ejecuta:

```
por defecto:  c8624fca6e47 bcd2cbecbbe0
sin fecha y con sal: 543e04cc4ef8 543e04cc4ef8
```

Los doce primeros caracteres de la huella SHA-256 de cada archivo.

- **Por defecto**, dos SVG del mismo gráfico son distintos: matplotlib escribe la fecha y genera al azar los identificadores internos (`id="..."`). Tus dos huellas serán otras, y distintas entre sí.
- Con `metadata={"Date": None}` y una sal fija (`svg.hashsalt`), son iguales byte a byte. Tus huellas pueden diferir de las del README si tu sistema tiene otra versión de alguna fuente, pero las dos serán iguales entre sí.

Para ver qué cambia, comenta de nuevo el bloque `with` y sus dos líneas, ejecuta y compara: `diff salida/4a.svg salida/4b.svg`.

### 5. Texto que se puede buscar

Descomenta el **PASO 5** y ejecuta:

```
4a.svg: 30 KB, título como <text>: False
5-texto.svg: 12 KB, título como <text>: True
```

- Por defecto (`svg.fonttype` es `"path"`), cada letra se dibuja como un trazo: el SVG pesa más, y el título no se puede buscar ni copiar.
- Con `"none"`, el texto queda como texto: un 60 % más pequeño, y un lector de pantalla o un `grep` lo encuentran. Es lo que hace `charts.save` en tu Observatorio, y por eso `test_informe.py` puede buscar `Difieren` dentro de tu figura.

Para terminar, abre `salida/3-conclusion.svg` y escribe en un comentario al final de `main.py` qué le falta a ese gráfico para ir en un informe (pista: ¿en qué unidades está el eje x?).

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'matplotlib'` | Ejecuta con `uv run python main.py` dentro de `starter/` |
| `NameError: name 'results' is not defined` en el paso 3 | Descomenta antes el paso 2 |
| En el paso 4, las dos huellas "sin fecha" son distintas | Falta `metadata={"Date": None}` en alguno de los dos `savefig` |
| VS Code muestra el SVG como texto | Botón derecho, *Open Preview*, o ábrelo en el navegador |
| Las barras de error salen en vertical | Usaste `yerr` en lugar de `xerr` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Muchas comparaciones](../ejercicio-02-muchas-comparaciones/README.md) | **Ejercicio 03 · Un gráfico por afirmación** | [Ejercicio 04 · Un informe desde el código](../ejercicio-04-un-informe-desde-el-codigo/README.md) |
