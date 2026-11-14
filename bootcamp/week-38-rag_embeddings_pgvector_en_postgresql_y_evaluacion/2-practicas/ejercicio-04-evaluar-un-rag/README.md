# Ejercicio 04 — Evaluar un RAG

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-evaluar-un-rag.md)

## Objetivo

Medir un RAG por partes, con números en lugar de impresiones:

- un conjunto de preguntas con su trozo correcto, escrito a mano;
- recall@k: ¿está el trozo correcto entre los k primeros?;
- MRR: ¿en qué puesto sale?;
- comparar dos formas de trocear con las mismas preguntas;
- comprobar las respuestas con reglas: citas válidas, cita correcta, el dato;
- Claude como juez de la fidelidad, y lo que cuesta evaluar.

Es un ejercicio **guiado**: descomentas cada paso de `main.py`, lo ejecutas y comparas la salida con la de este README. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-38-rag_embeddings_pgvector_en_postgresql_y_evaluacion/2-practicas/ejercicio-04-evaluar-un-rag/starter
uv run python main.py
```

```
Ejercicio 04 · Evaluar un RAG
```

El manual, `split` y la búsqueda son los del ejercicio 03; `ranking` ordena **todos** los trozos. `QUESTIONS` son doce preguntas. Cada una lleva una frase que solo está en el trozo que la responde, y el dato que debe traer la respuesta. Varias usan otras palabras que el manual («apagón», «repuesto», «sin corriente»), como preguntaría una persona. Las respuestas de Claude son **de ejemplo**, como en el ejercicio 03; con tu clave, `CLAUDE_REAL=1`.

## Pasos

### 1. Un conjunto de preguntas etiquetadas

Descomenta el **PASO 1** y ejecuta:

```
12 preguntas · 14 trozos · trozos que responden: [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 10, 13]
```

Para cada pregunta, `relevant` busca el **único** trozo que contiene su frase: es la etiqueta, la respuesta correcta de la búsqueda. Si la frase saliera en dos trozos, o en ninguno, `[number] = ...` fallaría. Así ves enseguida una etiqueta mal escrita.

Escribir las preguntas es la parte cara de evaluar: hay que conocer el documento. Pero sin ellas, cada cambio del RAG es una opinión. Con doce, cada pregunta pesa un 8 %; un conjunto de verdad tiene decenas o cientos.

### 2. ¿Está el trozo bueno entre los k primeros?

Descomenta el **PASO 2** y ejecuta:

```
puestos: [1, 1, 1, 1, 1, 7, 1, 7, 5, 14, 9, 1]
recall@1: 0.58 (7 de 12)
recall@3: 0.58 (7 de 12)
recall@5: 0.67 (8 de 12)
```

**recall@k** es la parte de las preguntas cuyo trozo bueno sale entre los `k` primeros. Es lo que importa en RAG: si el trozo no llega al prompt, Claude no puede usarlo (ejercicio 03, paso 6).

Siete preguntas lo encuentran el primero. Las otras cinco lo dejan en el puesto 5 o más abajo: con `k = 3`, Claude no lo vería. Con una sola respuesta correcta por pregunta, recall@k y *hit rate*@k son lo mismo.

### 3. El rango recíproco medio (MRR)

Descomenta el **PASO 3** y ejecuta:

```
MRR: 0.64
  puesto 7: ¿Qué significa que el ozono salga negativo?
  puesto 7: ¿Cuánto aguanta la estación sin corriente?
  puesto 5: ¿Qué datos no valen después de un apagón?
  puesto 14: ¿Cuánto tarda en llegar un repuesto?
  puesto 9: ¿Qué pasa si una estación deja de transmitir?
```

**MRR** (*Mean Reciprocal Rank*) es la media de 1/puesto. Vale 1 si el bueno sale siempre primero y 0,5 si sale siempre segundo. Recall@k solo mira si está; MRR también premia que esté arriba.

Las preguntas que fallan son las de **otras palabras**:

- «sin corriente» frente a «autonomía» y «corte»;
- «apagón» frente a «volver la corriente»;
- «repuesto» frente a «pieza».

«¿Cuánto tarda en llegar un repuesto?» deja el trozo bueno en el último puesto (14 de 14). Es el límite léxico del ejercicio 01, ahora medido. Mirar los fallos uno a uno dice qué arreglar: sinónimos, un modelo de embeddings o una búsqueda híbrida (teoría 04).

### 4. Otro troceo, otros números

Descomenta el **PASO 4** y ejecuta:

```
 párrafos: 14 trozos de 203 caracteres · recall@1 0.58 · recall@3 0.58 · MRR 0.64
secciones: 9 trozos de 305 caracteres · recall@1 0.58 · recall@3 1.00 · MRR 0.75
```

Las mismas doce preguntas, con el manual troceado por secciones en lugar de por párrafos. Cada etiqueta se recalcula con su frase: el trozo bueno es otro, pero la pregunta es la misma.

Con secciones, recall@3 sube a 1,00: los trozos son más largos, tienen más palabras y la pregunta coincide con alguna. A cambio, cada trozo es un 50 % más largo, y en el prompt se paga cada carácter. Ninguna forma es la mejor siempre; con preguntas etiquetadas, decidir es medir, no adivinar.

### 5. Las respuestas, con comprobaciones

Descomenta el **PASO 5** y ejecuta:

```
cita válida · cita el bueno · trae el dato · pregunta
  sí  ·  sí  ·  sí · ¿Cuándo hay que cambiar el filtro antes de tiempo?
  sí  ·  sí  ·  sí · ¿Con qué se limpia la toma de aire?
  sí  ·  sí  ·  sí · ¿Cada cuánto se calibra el analizador de ozono?
  sí  ·  no  ·  sí · ¿Qué significa que el ozono salga negativo?
  sí  ·  no  ·  no · ¿Cuánto aguanta la estación sin corriente?
```

Cinco preguntas: tres que la búsqueda resuelve bien y dos que no (puesto 7). Tres comprobaciones con reglas, sin otro modelo:

- **Cita válida:** todas las citas son de trozos que recibió (ejercicio 03, paso 5).
- **Cita el bueno:** entre las citas está el trozo etiquetado.
- **Trae el dato:** la respuesta contiene el dato esperado.

Las dos últimas preguntas fallan porque el trozo bueno no llegó al prompt, y Claude no puede citarlo. Fíjate en la cuarta: «trae el dato» dice que sí, porque la respuesta menciona «el cero» por otro motivo. Una regla de texto es barata y a veces se engaña.

### 6. Claude como juez

Descomenta el **PASO 6** y ejecuta:

```
fiel · ¿Cuándo hay que cambiar el filtro antes de tiempo? · Lo dice el fragmento 1.
NO fiel · ¿Con qué se limpia la toma de aire? · Que la malla se cambie una vez al año no está en los fragmentos.
fiel · ¿Cada cuánto se calibra el analizador de ozono? · Lo dice el fragmento 4.
fiel · ¿Qué significa que el ozono salga negativo? · No responde del todo, pero no añade nada que no esté.
fiel · ¿Cuánto aguanta la estación sin corriente? · Dice que no lo sabe y lo que cita está en el fragmento 8.
evaluar 5 respuestas: 5174 tokens de entrada y 303 de salida · 0.0134 $
```

**Fidelidad** (*faithfulness*) es que todo lo que afirma la respuesta esté en los fragmentos. Ninguna regla de texto la mide, así que se pregunta a otro modelo con un prompt de juez y salida estructurada: es un **LLM como juez**.

La respuesta sobre la toma de aire pasó las tres reglas del paso 5. Aun así, añade «la malla se cambia una vez al año», que el manual no dice: es una alucinación, y solo el juez la ve. Las dos que dicen «no lo dicen» son **fieles**: incompletas, pero no inventan.

Un juez también se equivoca. Antes de fiarte de él, compara sus veredictos con los tuyos en unas cuantas respuestas. Además, cuesta. La cifra de la última línea suma las respuestas y los veredictos, y el juez lee otra vez los mismos fragmentos: juzgar cuesta tanto como responder. Con cien preguntas en cada cambio, evaluar es una parte del presupuesto.

Para terminar, añade a `QUESTIONS` dos preguntas tuyas sobre el manual, una con sus palabras y otra con sinónimos, y mira su puesto en los dos troceos.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ValueError: not enough values to unpack (expected 1, got 0)` | La frase de una pregunta no está en ningún trozo: cópiala tal cual del manual |
| `ValueError: too many values to unpack (expected 1, got 2)` | La frase está en dos trozos: elige una más larga, que solo esté en uno |
| `LookupError: respuestas.json no tiene esta petición` | Cambiaste una pregunta, el troceo o el prompt: vuelve al código del paso, o usa tu clave y `CLAUDE_REAL=1` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · RAG paso a paso](../ejercicio-03-rag-paso-a-paso/README.md) | **Ejercicio 04 · Evaluar un RAG** | [Proyecto](../../3-proyecto/README.md) |
