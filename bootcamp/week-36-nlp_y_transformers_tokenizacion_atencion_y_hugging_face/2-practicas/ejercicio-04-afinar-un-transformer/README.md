# Ejercicio 04 — Afinar un Transformer

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-hugging-face.md)

## Objetivo

El *transfer learning* de la semana 35, con un Transformer preentrenado y 30 notas etiquetadas:

- la referencia: TF-IDF con las mismas 30 notas;
- un cuerpo preentrenado con una salida nueva, sin entrenar;
- congelar el cuerpo y entrenar solo la salida;
- afinar todo el modelo, con un ritmo pequeño;
- qué dice de notas que usan otras palabras;
- guardarlo en `safetensors` y usarlo con un `pipeline`.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-36-nlp_y_transformers_tokenizacion_atencion_y_hugging_face/2-practicas/ejercicio-04-afinar-un-transformer/starter
uv run python main.py
```

```
Ejercicio 04 · Afinar un Transformer
300 notas · 30 para entrenar, 30 para validar, 100 de prueba · 6 con otras palabras
```

Las 300 notas del ejercicio 03, repartidas en tres grupos que no se tocan, y las 6 frases con otras palabras de su paso 6. El modelo es el multilingüe del ejercicio 03 (470 MB, ya en tu caché).

Las funciones de arriba:

- `tokens(batch)`: el lote del ejercicio 01, paso 7, como tensores;
- `scores(model, batch)`: las puntuaciones, en modo evaluación y sin gradientes;
- `report(name, model)`: acierto en prueba y cuántas de las 6 frases acierta;
- `train(model, epochs, rate)`: el bucle de la semana 35, con lotes de 8 y `AdamW`, que solo optimiza lo no congelado y escribe el acierto en validación tras cada época;
- `fresh()`: el modelo preentrenado con una salida nueva de 3 tipos.

El ejercicio entero tarda menos de un minuto en CPU.

## Pasos

### 1. La referencia: TF-IDF con 30 notas

Descomenta el **PASO 1** y ejecuta:

```
          tf-idf · prueba 0.87 · con otras palabras 2 de 6
```

Lo mismo que en el ejercicio 03: 0,87 en prueba, y 2 de 6 con otras palabras.

### 2. Un cuerpo preentrenado y una salida nueva

Descomenta el **PASO 2** y ejecuta:

```
BertForSequenceClassification
117.654.915 parámetros · 96.014.208 son la tabla de piezas · salida 1.155
    sin entrenar · prueba 0.31 · con otras palabras 2 de 6
```

`AutoModelForSequenceClassification` con `num_labels=3` toma el cuerpo preentrenado (`model.bert`) y le pone encima una capa lineal nueva, `model.classifier`, de 384 × 3 + 3 = **1155** parámetros, al azar. `transformers` avisa en la terminal ("Some weights ... are newly initialized"): `logging.set_verbosity_error()` lo calla, porque ya sabes por qué pasa.

- **118 millones** de parámetros, y **96 millones** son la tabla de piezas: 250 037 filas × 384 números (el tokenizador usa 250 002; el resto sobra, ejercicio 01, paso 6). Hablar 50 idiomas sale caro.
- Sin entrenar, acierta **0,31**: la salida es azar.
- `id2label` y `label2id` guardan los nombres de los tipos dentro del modelo: el paso 6 los aprovecha.

### 3. Congelar el cuerpo y entrenar la salida

Descomenta el **PASO 3** y ejecuta:

```
entrenables: 1.155
  época 1 · validación 0.73
  época 2 · validación 0.83
  época 3 · validación 0.80
  época 4 · validación 0.80
  época 5 · validación 0.83
  solo la salida · prueba 0.87 · con otras palabras 4 de 6
```

Como `freeze` en la semana 35: `requires_grad_(False)` en todo `model.bert`. Solo se entrenan los 1155 de la salida, con un ritmo normal (0,01). Es casi el paso 6 del ejercicio 03 (una regresión logística sobre los vectores), pero sobre el vector de la pieza `<s>` (pasado por `model.bert.pooler`, una capa lineal del cuerpo) en lugar de la media.

- En prueba, 0,87: lo mismo que TF-IDF.
- Con otras palabras, 4 de 6: el cuerpo congelado ya sabe que "mugre" y "polvo" se parecen.

### 4. Afinar todo el modelo

Descomenta el **PASO 4** y ejecuta:

```
  época 1 · validación 0.73
  época 2 · validación 0.87
  época 3 · validación 0.83
  época 4 · validación 0.83
  época 5 · validación 0.87
         afinado · prueba 0.82 · con otras palabras 6 de 6
```

`fresh()` otra vez (empieza del preentrenado, no del paso 3) y **nada congelado**: los 118 millones de parámetros cambian, con un ritmo de **5e-5**, doscientas veces menor. Con un ritmo grande, unas pocas notas borrarían lo que el modelo aprendió con miles de millones de frases (*catastrophic forgetting*).

- En prueba, 0,82: algo por debajo. Con 30 notas para ajustar 118 millones de parámetros, y 100 de prueba, cinco puntos son tres notas: ruido.
- Con otras palabras, **6 de 6**.

Ninguno de los tres pasa de 0,87 en prueba, y es lógico: un 15 % de las notas no dice qué se hizo ("Visita a Centro, se revisó el equipo."). Ningún modelo puede acertarlas más que por suerte: el techo está en los datos, no en el modelo.

### 5. Qué dice de notas nuevas

Descomenta el **PASO 5** y ejecuta:

```
       averia 0.40 · Monitor muerto, ni prende
       averia 0.36 · Sin corriente desde ayer
     limpieza 0.56 · Barrimos mugre acumulada
     limpieza 0.60 · Aspiramos suciedad
  calibracion 0.44 · Corregimos el desvío del aparato
  calibracion 0.47 · Afinamos la medición
```

Las seis bien, pero con probabilidades **bajas**: 0,36 es apenas más que el 0,33 de no saber nada. Con 30 notas y 5 épocas, el modelo acierta el orden de los tipos, pero no está seguro. Si vas a usar la probabilidad para algo (por ejemplo, revisar a mano las notas por debajo de 0,5), mídela antes; no la tomes por una certeza.

### 6. Guardar y volver a cargar

Descomenta el **PASO 6** y ejecuta:

```
['config.json', 'model.safetensors', 'tokenizer.json', 'tokenizer_config.json']
model.safetensors: 471 MB
       averia 0.56 · El sensor de Norte se quemó
     limpieza 0.63 · Se limpió la carcasa
```

- **`save_pretrained`** escribe la carpeta `modelo-afinado/`: la configuración (con los nombres de los tipos), los pesos y el tokenizador.
- **`model.safetensors`**: los pesos en un formato que solo guarda tensores, como `weights_only=True` en la semana 35. Cargarlo no ejecuta código. Un `pytorch_model.bin` antiguo es `pickle`, y sí podría.
- **471 MB**: el modelo entero, aunque solo cambiaste unas pocas notas. Por eso no va a tu repositorio, ni al de este bootcamp: `modelo-afinado/` está en el `.gitignore`. Bórrala al terminar con `rm -r modelo-afinado`.
- `pipeline("text-classification", model="modelo-afinado")` carga todo desde la carpeta y devuelve el nombre del tipo, no un número.

Para terminar, escribe en un comentario al final de `main.py`: en tu dominio, ¿afinarías un modelo de 118 millones de parámetros, te quedarías con TF-IDF, o usarías *zero-shot* (ejercicio 03)? ¿Cuántas notas etiquetadas tienes, y cuánto cambian las palabras de unos técnicos a otros?

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `FileNotFoundError: notas.csv` | Ejecuta desde `starter/`, donde está `notas.csv` |
| `entrenables` no es 1.155 en el paso 3 | El bucle congela `model.bert.parameters()`, no `model.parameters()` |
| La validación del paso 4 se queda en 0,33 | El ritmo es demasiado grande: `5e-5`, no `5e-2` |
| `RuntimeError: ... out of memory` en el paso 4 | AdamW guarda dos números por parámetro: unos 2 GB de RAM. Cierra otros programas |
| `OSError: ... modelo-afinado does not appear to have a file named config.json` | El paso 6 no llegó a guardar: ejecuta otra vez desde el paso 4 |
| Tus aciertos difieren en una nota | Otro procesador suma en otro orden; con 100 notas, una nota es 0,01 |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Modelos preentrenados](../ejercicio-03-modelos-preentrenados/README.md) | **Ejercicio 04 · Afinar un Transformer** | [Proyecto](../../3-proyecto/README.md) |
