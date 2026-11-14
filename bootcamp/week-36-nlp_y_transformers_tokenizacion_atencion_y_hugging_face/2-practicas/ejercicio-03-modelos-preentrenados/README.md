# Ejercicio 03 — Modelos preentrenados

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-hugging-face.md)

## Objetivo

Usar Transformers que otros han entrenado con miles de millones de palabras, sin entrenar nada:

- clasificar notas sin un solo ejemplo (*zero-shot*), y cuánto acierta;
- qué hace un `pipeline` por dentro;
- convertir frases en vectores (*embeddings*) y comparar su significado;
- buscar notas por lo que dicen, no por sus palabras;
- con 30 notas etiquetadas, TF-IDF frente a embeddings, con palabras que nunca vio.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-36-nlp_y_transformers_tokenizacion_atencion_y_hugging_face/2-practicas/ejercicio-03-modelos-preentrenados/starter
uv run python main.py
```

```
Ejercicio 03 · Modelos preentrenados
300 notas · tipos: ['averia', 'calibracion', 'limpieza']
```

`notas.csv` son las 300 notas de ejemplo del proyecto, generadas con `scripts/generar_notas.py`: 100 de cada tipo, y un 15 % que no dice qué se hizo ("Visita a Centro, se revisó el equipo.").

Dos modelos, cada uno fijado a una versión con `revision`:

| Modelo | Tamaño | Para qué |
|---|---|---|
| `Recognai/bert-base-spanish-wwm-cased-xnli` | 440 MB | BETO afinado para inferencia (¿una frase implica otra?): *zero-shot* |
| `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | 470 MB | Frases a vectores, en 50 idiomas: embeddings |

El segundo ya está en tu caché si hiciste el paso 8 del ejercicio 02. Todo el ejercicio corre en CPU: tarda alrededor de un minuto.

## Pasos

### 1. Clasificar sin entrenar (zero-shot)

Descomenta el **PASO 1** y ejecuta. La primera vez descarga el modelo en español:

```
   limpieza 0.45 · Visita a Centro, se revisó el equipo.
   limpieza 0.98 · En Centro se quitó el polvo acumulado en la entrada, queda limpio.
   limpieza 0.61 · El analizador de Centro tenía deriva y se corrigió el cero, tras la limpieza, se anotó el nuevo factor.
     avería 0.83 · El analizador de Este se apagó por un corte de energía, queda fuera de servicio.
```

`pipeline("zero-shot-classification")` no se entrenó con tus tipos. Para cada nota y cada tipo, pregunta al modelo: ¿la nota implica "Este ejemplo es avería."? Y se queda con el tipo más probable.

- La segunda y la cuarta, bien y con seguridad.
- La primera no dice nada: 0,45 es un "no sé".
- La tercera es una **calibración** ("se corrigió el cero"), pero "tras la limpieza" lo despista: dice limpieza.

### 2. ¿Cuánto acierta?

Descomenta el **PASO 2** y ejecuta:

```
«Este ejemplo es {}.» · 60 notas, sin ver ni un ejemplo: acierta 0.72
  dice avería 17 veces; lo es 20
  dice limpieza 26 veces; lo es 20
  dice calibración 17 veces; lo es 20
«Esta nota trata de una {}.» · 60 notas, sin ver ni un ejemplo: acierta 0.58
  dice avería 7 veces; lo es 20
  dice limpieza 25 veces; lo es 20
  dice calibración 28 veces; lo es 20
```

- **0,72** sin una sola nota etiquetada. La referencia (siempre el mismo tipo) acierta 0,33.
- Cambiar solo la **plantilla** de la hipótesis lo baja a **0,58**. "Este ejemplo es {}." es la frase con la que se afinó este modelo (lo dice su ficha en el Hub); la otra, aunque a ti te parezca más natural, no.

*Zero-shot* sirve para empezar sin etiquetas, o para etiquetar un primer lote que luego revisas. Pero depende de cómo escribas la pregunta, y no lo sabes hasta medirlo con notas etiquetadas: igual que con un LLM en la semana 37.

### 3. Lo que hace el pipeline por dentro

Descomenta el **PASO 3** y ejecuta:

```
salidas del modelo: {0: 'contradiction', 1: 'neutral', 2: 'entailment'}
  «Este ejemplo es avería.» · contradiction 0.62 neutral 0.38 entailment 0.00
  «Este ejemplo es limpieza.» · contradiction 0.17 neutral 0.81 entailment 0.02
  «Este ejemplo es calibración.» · contradiction 0.05 neutral 0.94 entailment 0.01
109.853.187 parámetros
```

Sin `pipeline`, son tres piezas que ya conoces:

1. `AutoTokenizer` convierte la pareja (nota, hipótesis) en un lote, con `[SEP]` entre las dos.
2. `AutoModelForSequenceClassification` da tres puntuaciones (*logits*): contradicción, neutral, implicación.
3. `softmax` las convierte en probabilidades.

Con la nota vaga ("Visita a Centro, se revisó el equipo."), ninguna hipótesis se implica: todo es neutral o contradicción. `pipeline` compara la implicación de los tres tipos y elige la mayor, aunque sea 0,02: por eso el paso 1 dijo limpieza con 0,45.

**110 millones** de parámetros: 17 000 veces tu `Encoder` del proyecto.

### 4. Una frase, un vector (embeddings)

Descomenta el **PASO 4** y ejecuta:

```
vectores de 384 números
  0.22 · El sensor dejó de enviar lecturas
  0.43 · La estación no transmite mediciones
  -0.04 · Se limpió el filtro lleno de polvo
  -0.09 · Hoy hace sol en Norte
```

`embed` pasa cada frase por el modelo multilingüe y hace la **media** de los vectores de sus piezas, sin el relleno (la misma media de tu `Encoder`). Cada frase es un vector de 384 números.

Comparada con "El equipo no da datos":

- "La estación no transmite mediciones" (0,43) no comparte **ni una palabra** y es la más parecida;
- "Hoy hace sol en Norte", nada que ver: por debajo de 0.

Una bolsa de palabras daría 0 a las dos primeras: no tienen palabras en común con la pregunta.

### 5. Buscar por significado

Descomenta el **PASO 5** y ejecuta:

```
«problema eléctrico»:
  0.50 · El sensor de Este se apagó por un corte de energía, queda fuera de servicio.
  0.50 · El analizador de Este se apagó por un corte de energía, queda fuera de servicio.
  0.49 · La estación Este se apagó por un corte de energía, la limpieza no lo arregló, queda fuera de servicio.
«suciedad en la entrada de aire»:
  0.65 · En Centro se quitó el polvo acumulado en la entrada, queda limpio.
  0.61 · En Este se limpió el filtro lleno de polvo, queda limpio.
  0.61 · Hoy en Centro se quitó el polvo acumulado en la entrada, lecturas normales tras la limpieza.
```

Las 300 notas a vectores, una vez; cada búsqueda es un vector más y 300 similitudes coseno. "problema eléctrico" encuentra los cortes de energía sin que ninguna nota diga "eléctrico". Es la búsqueda semántica: la base del RAG de la semana 38, donde estos vectores irán a PostgreSQL con pgvector.

### 6. Pocas etiquetas: embeddings frente a TF-IDF

Descomenta el **PASO 6** y ejecuta:

```
    tf-idf · 30 notas · prueba 0.87 · con otras palabras 2 de 6
embeddings · 30 notas · prueba 0.84 · con otras palabras 5 de 6
```

La misma regresión logística, con 30 notas etiquetadas (10 de cada tipo), sobre dos representaciones: TF-IDF o los embeddings del paso 5.

- **En prueba**, empate técnico (0,87 frente a 0,84, en 100 notas): las notas de prueba usan las mismas frases que las de entrenamiento, y TF-IDF las reconoce por sus palabras.
- **Con otras palabras** ("Monitor muerto, ni prende", "Aspiramos suciedad"...), TF-IDF acierta 2 de 6, lo que acertaría tirando un dado; los embeddings, 5. Las seis frases no tienen palabras en común con las notas de entrenamiento (salvo "el", "la", "sin"...), pero el modelo preentrenado sabe que "mugre" y "polvo" se parecen.

Es la diferencia que importa en un dominio real: tus técnicos no escriben con plantillas. Con seis frases, eso sí, es una pista, no una prueba: con tu dominio, mídelo con más.

Para terminar, escribe en un comentario al final de `main.py` dos búsquedas del paso 5 con palabras de tu dominio, y si encuentran lo que esperas.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `FileNotFoundError: notas.csv` | Ejecuta desde `starter/`, donde está `notas.csv` |
| `OSError: We couldn't connect to 'https://huggingface.co'` | Sin red no se descarga. Con los modelos ya en la caché, `HF_HUB_OFFLINE=1 uv run python main.py` |
| El paso 2 tarda más de un minuto | Son 360 pasadas de un modelo de 110 millones de parámetros por la CPU: es normal |
| Tus números difieren en el segundo decimal | Otro procesador suma en otro orden; el tipo elegido no debería cambiar |
| `RuntimeError: ... out of memory` | Cierra otros programas: los dos modelos juntos ocupan unos 2 GB de RAM |
| Los embeddings del paso 4 dan casi todo 0,9 | Falta la media sin relleno: `mask` multiplica antes de sumar |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · La atención por dentro](../ejercicio-02-la-atencion-por-dentro/README.md) | **Ejercicio 03 · Modelos preentrenados** | [Ejercicio 04 · Afinar un Transformer](../ejercicio-04-afinar-un-transformer/README.md) |
