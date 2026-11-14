# Ejercicio 03 — RAG paso a paso

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-rag.md)

## Objetivo

Que Claude responda con **tu** documento y no con lo que sabe en general:

- preguntar sin contexto, y ver qué responde;
- trocear un manual en párrafos con su sección;
- recuperar los trozos más parecidos a una pregunta;
- poner los trozos en el prompt, cada uno con su número, y pedir citas;
- comprobar que las citas son de trozos que Claude recibió;
- lo que pasa cuando el manual no dice algo y cuando `k` es pequeño.

Es un ejercicio **guiado**: descomentas cada paso de `main.py`, lo ejecutas y comparas la salida con la de este README. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-38-rag_embeddings_pgvector_en_postgresql_y_evaluacion/2-practicas/ejercicio-03-rag-paso-a-paso/starter
uv run python main.py
```

```
Ejercicio 03 · RAG paso a paso
```

`manual.md` es el manual de mantenimiento de una red de estaciones, con nueve secciones. Ábrelo: es el documento que Claude no ha visto nunca. Las respuestas salen de `respuestas.json`, como en la semana 37. Son **de ejemplo**, escritas para el bootcamp con la forma exacta de la API; no las escribió Claude, y los tokens son aproximados. Con tu clave, `CLAUDE_REAL=1 uv run python main.py` las pide de verdad.

## Pasos

### 1. Preguntar sin contexto

Descomenta el **PASO 1** y ejecuta:

```
Depende del fabricante y del ambiente. Como orientación, muchos filtros de partículas se cambian cada uno a tres meses, o antes si se ven sucios o baja el caudal. Consulta el manual de tu equipo para el intervalo exacto.
tokens: 31 de entrada y 69 de salida
```

Una respuesta razonable y que no sirve. Claude no conoce **tu** manual, que dice «cada 30 días, o antes si la caída de presión supera 50 Pa». Responde con lo que suele pasar en general. Podrías pegar el manual entero en cada pregunta, pero con un manual de 300 páginas pagarías 300 páginas por pregunta. RAG pega solo los trozos que importan.

### 2. Trocear el manual

Descomenta el **PASO 2** y ejecuta:

```
14 trozos · de 117 a 288 caracteres
trozo 2: Filtro de partículas: Antes de cambiar el filtro, apaga la bomba de muestreo y espera a que la presión se iguale. Después del cambio, haz una prueba de fugas: tapa la entrada y comprueba que el caudal baja a cero en menos de un minuto.
```

`split` corta por párrafos (dos saltos de línea) y pone el **título de la sección** delante de cada uno. Sin el título, el trozo 2 diría «Antes de cambiar el filtro...» sin decir de qué filtro se habla. Un trozo debe entenderse solo, porque llegará solo al prompt.

Los títulos no son trozos: solo se guardan para ponerlos delante. Hay muchas formas de trocear (por frases, por un número fijo de caracteres con solapamiento, por secciones); el ejercicio 04 compara dos.

### 3. Recuperar los trozos más parecidos

Descomenta el **PASO 3** y ejecuta:

```
  [1] 0.62 · Filtro de partículas: El filtro de partículas se cambia cada 30 días, …
  [2] 0.43 · Filtro de partículas: Antes de cambiar el filtro, apaga la bomba de mu…
  [11] 0.31 · Averías: Una avería se anota con el equipo, el síntoma y lo que se hiz…
```

TF-IDF sobre los 14 trozos y la pregunta, y los 3 de mayor coseno. TF-IDF da vectores de longitud 1, así que el producto `matrix @ pregunta` ya es el coseno. El primero es el que responde; el tercero es ruido («cambiar» sale también en averías). En tu proyecto, esta búsqueda la hace PostgreSQL con pgvector.

### 4. Aumentar el prompt y generar, con citas

Descomenta el **PASO 4** y ejecuta:

```
  tokens: 526 de entrada y 30 de salida
Cada 30 días, o antes si la caída de presión supera 50 Pa.
citas: [1]
```

Las tres letras de RAG, en orden:

- **Recuperar** los trozos.
- **Aumentar** el prompt con ellos, cada uno entre `<fragmento id="...">` y `</fragmento>`.
- **Generar** la respuesta.

El sistema pide usar solo los fragmentos, citar sus números y decir cuándo no responden. La salida estructurada (semana 37) obliga a que haya `respuesta` y `citas`.

La respuesta es la del **manual**, no la general del paso 1, y cita el trozo 1. Cuesta unos 500 tokens de entrada: los tres trozos y las instrucciones.

### 5. Comprobar las citas

Descomenta el **PASO 5** y ejecuta:

```
  todas las citas son de trozos que recibió
  [5] 0.49 · Calibración del analizador de ozono: Si el analizador da lecturas nega…
  [4] 0.38 · Calibración del analizador de ozono: El analizador de ozono se calibra…
  [11] 0.18 · Averías: Una avería se anota con el equipo, el síntoma y lo que se hiz…
  tokens: 532 de entrada y 56 de salida
El cero se ha desplazado: repite el ajuste del cero antes de la calibración completa. Si la deriva supera 5 ppb en un mes, avisa al laboratorio.
  cita trozos que no recibió: [6]
```

Una cita es una afirmación que tu código **puede** comprobar sin otro modelo. Claude recibió los trozos 5, 4 y 11, y cita el 6. La respuesta es correcta y está en el trozo 5, pero la cita es falsa: Claude no pudo leer el 6. Esta respuesta de ejemplo enseña algo que pasa de verdad, sobre todo con muchos trozos.

¿Qué hacer con una cita inventada? Avisar, como `preguntar` en tu proyecto, o descartar la respuesta. Lo que no debes hacer es enseñarla como si estuviera respaldada.

### 6. Lo que el manual no dice, y `k`

Descomenta el **PASO 6** y ejecuta:

```
  [4] 0.63 · Calibración del analizador de ozono: El analizador de ozono se calibra…
  [5] 0.32 · Calibración del analizador de ozono: Si el analizador da lecturas nega…
  [13] 0.20 · Seguridad: Antes de abrir un analizador, desconecta la alimentación. L…
  tokens: 528 de entrada y 42 de salida
Los fragmentos no lo dicen: hablan de calibrar y de revisar el analizador de ozono, no de su precio.
k = 1:
  [7] 0.38 · Cortes de energía: Las estaciones tienen un sistema de alimentación in…
  tokens: 380 de entrada y 45 de salida
Si el corte dura más de cuatro horas, la estación se apaga sola y guarda los datos de las últimas 48 horas.
k = 3:
  [7] 0.38 · Cortes de energía: Las estaciones tienen un sistema de alimentación in…
  [12] 0.25 · Averías: Un equipo que queda fuera de servicio se marca en el servidor…
  [8] 0.24 · Cortes de energía: Al volver la corriente, la estación arranca sola, p…
  tokens: 489 de entrada y 67 de salida
Si dura más de cuatro horas, la estación se apaga y guarda los datos de las últimas 48 horas. Al volver la corriente, los datos de los primeros 30 minutos se marcan como no válidos.
```

Dos lecciones:

- **El precio no está en el manual.** La búsqueda siempre devuelve algo, aunque no responda. Con la instrucción «si no responden, dilo», Claude dice que no lo sabe en lugar de inventar un precio.
- **La respuesta está repartida en dos trozos**, el 7 y el 8. Con `k = 1`, Claude solo ve el 7, y su respuesta es correcta pero **incompleta**: no sabe que media hora de datos no vale. Con `k = 3`, la respuesta es completa, a cambio de más tokens. Elegir `k` es elegir entre coste y cobertura, y se mide (ejercicio 04).

Para terminar, escribe al final de `main.py` una pregunta sobre el manual que use **otras palabras** que el texto (por ejemplo, «¿qué hago si se va la luz?»). Mira qué trozos recupera TF-IDF. Con tu clave, mira también qué responde Claude.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `LookupError: respuestas.json no tiene esta petición` | Cambiaste una pregunta, un trozo, el prompt o `k`: vuelve al código del paso, o pruébalo con tu clave y `CLAUDE_REAL=1` |
| `FileNotFoundError: manual.md` | Ejecuta desde `starter/`, donde está el manual |
| `ValidationError` en `ask` con tu clave | La respuesta se cortó o no cumple el esquema: mira `response.stop_reason` |
| `NameError: name 'pieces' is not defined` | Descomenta los pasos en orden: todos usan los trozos del paso 2 |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · pgvector por dentro](../ejercicio-02-pgvector-por-dentro/README.md) | **Ejercicio 03 · RAG paso a paso** | [Ejercicio 04 · Evaluar un RAG](../ejercicio-04-evaluar-un-rag/README.md) |
