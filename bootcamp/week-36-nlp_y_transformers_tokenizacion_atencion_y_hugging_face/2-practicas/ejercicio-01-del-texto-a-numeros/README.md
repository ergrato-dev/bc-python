# Ejercicio 01 — Del texto a números

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-del-texto-a-numeros.md)

## Objetivo

Convertir notas de texto en números, de la forma más simple a la que usan los Transformers:

- una bolsa de palabras a mano, con `Counter`;
- TF-IDF con scikit-learn, y lo que una bolsa no ve;
- un tokenizador BPE entrenado con tus notas, con `tokenizers`;
- dos tokenizadores preentrenados de Hugging Face: WordPiece y SentencePiece;
- un lote listo para un modelo: identificadores, relleno y máscara de atención.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-36-nlp_y_transformers_tokenizacion_atencion_y_hugging_face/2-practicas/ejercicio-01-del-texto-a-numeros/starter
uv run python main.py
```

```
Ejercicio 01 · Del texto a números
10 notas · la primera: 'El sensor de Norte no responde desde la madrugada.'
```

Diez notas de mantenimiento de estaciones de calidad del aire. Este ejercicio no instala PyTorch: solo trabaja con texto. Por eso `transformers` escribe en la terminal `PyTorch was not found. Models won't be available...` al empezar: es un aviso, no un error. Aquí solo usas sus tokenizadores.

Los pasos 5 y 6 descargan de Hugging Face los tokenizadores (no los modelos): unos pocos MB, que quedan en `~/.cache/huggingface` para los ejercicios siguientes.

## Pasos

### 1. Una bolsa de palabras a mano

Descomenta el **PASO 1** y ejecuta:

```
vocabulario: 56 palabras · ['aire', 'ajustó', 'altos', 'analizador', 'apagó', 'avería']
nota 1: 56 números, 9 distintos de 0
las palabras de la nota 1: {'el': 1, 'sensor': 1, 'de': 1, 'norte': 1, 'no': 1, 'responde': 1, 'desde': 1, 'la': 1, 'madrugada': 1}
```

El **vocabulario** son todas las palabras distintas de las diez notas: 56. Cada nota se convierte en 56 números, uno por palabra, que dicen cuántas veces sale. La nota 1 tiene 9 palabras: 47 de sus números son 0. Con miles de notas, el vocabulario tiene decenas de miles de palabras y casi todo es 0: por eso scikit-learn guarda estas matrices *dispersas* (solo lo que no es 0).

### 2. TF-IDF con scikit-learn

Descomenta el **PASO 2** y ejecuta:

```
matriz: 10 notas x 55 palabras
nota 2, las palabras que más pesan: lleno 0.44, limpió 0.44, sur 0.37, polvo 0.37
'de' pesa 0.19: sale en casi todas las notas
```

- **55**, no 56: `TfidfVectorizer` ignora por defecto las palabras de una sola letra (aquí, "y").
- **TF-IDF** multiplica cuántas veces sale una palabra en la nota (TF) por lo rara que es en todas (IDF). "lleno" y "limpió" solo salen en la nota 2: pesan mucho. "de" sale en casi todas: pesa poco, aunque la nota la tenga.

Es la referencia de la semana: TF-IDF y una regresión logística (semana 31) clasifican sorprendentemente bien.

### 3. Lo que una bolsa no ve

Descomenta el **PASO 3** y ejecuta:

```
¿mismo vector? True
palabras conocidas en 'recalibrado ayer': 0
```

Dos límites de cualquier bolsa de palabras:

- **El orden no existe.** "se limpió el filtro, no el sensor" y "se limpió el sensor, no el filtro" dicen lo contrario y son el mismo vector.
- **Una palabra nueva no existe.** "recalibrado" no es "recalibró": para el vectorizador ajustado con las diez notas, es desconocida. Y "ayer" también.

Los Transformers resuelven los dos: las subpalabras (pasos 4 a 6) y las posiciones (ejercicio 02).

### 4. Subpalabras con BPE

Descomenta el **PASO 4** y ejecuta:

```
 40 piezas · recalibrado → ['r', 'e', 'c', 'al', 'i', 'b', 'r', 'a', 'd', 'o']
120 piezas · recalibrado → ['re', 'cali', 'b', 'r', 'ad', 'o']
190 piezas · recalibrado → ['recali', 'b', 'r', 'ad', 'o']
las primeras uniones: [['d', 'e'], ['e', 'n'], ['e', 'l'], ['o', 'r'], ['s', 'e'], ['e', 's']]
```

**BPE** (*Byte Pair Encoding*) empieza con las letras sueltas y junta, una y otra vez, la pareja que más se repite: primero "d"+"e" (por "de", "desde", "madrugada"...), luego "e"+"n"... Cada unión es una pieza nueva, hasta llegar al tamaño pedido.

- Con **40** piezas, casi solo hay letras: "recalibrado" son 10 piezas.
- Con **120**, ya hay "re" y "cali" (de "recalibró").
- Pediste **250** y salen **190**: con diez notas no hay más parejas que juntar.

"recalibrado" no estaba en ninguna nota, y aun así se parte en piezas conocidas: ninguna palabra queda fuera. El normalizador quita tildes y mayúsculas antes de empezar: "recalibró" y "Recalibro" dan las mismas piezas.

### 5. Un tokenizador preentrenado: WordPiece

Descomenta el **PASO 5** y ejecuta:

```
BertTokenizer: 31002 piezas
  ['El', 'analiza', '##dor', 'de', 'Centro', 'se', 'recal', '##ib', '##ró', 'con', 'gas', 'de', 'referencia', '.']
  ['recal', '##ib', '##rado']
  ['PM', '##2', '.', '5', 'en', '[UNK]', '[UNK]', '[UNK]']
```

El tokenizador de un BERT en español (BETO), entrenado con miles de millones de palabras: 31 002 piezas. Es **WordPiece**, primo de BPE.

- `##` marca la pieza que continúa una palabra: `analiza` + `##dor`.
- Las palabras frecuentes ("referencia", "Centro") son una sola pieza; las raras se parten.
- Conserva mayúsculas y tildes (es un modelo *cased*).
- `µ`, `/` y `³` no estaban en su vocabulario: `[UNK]`, desconocido. Lo que el modelo no puede leer.

### 6. Otro estilo: SentencePiece, en 50 idiomas

Descomenta el **PASO 6** y ejecuta:

```
TokenizersBackend: 250002 piezas
  ['▁El', '▁analiza', 'dor', '▁de', '▁Centro', '▁se', '▁reca', 'li', 'bró', '▁con', '▁gas', '▁de', '▁referencia', '.']
  ['▁reca', 'lib', 'rado']
  ['▁PM', '2.5', '▁en', '▁μ', 'g', '/', 'm', '3']
```

El tokenizador del modelo multilingüe que usarás en los ejercicios 02 a 04: **SentencePiece**, con 250 002 piezas para 50 idiomas.

- Al revés que WordPiece, marca el **comienzo** de palabra con `▁`.
- Con tantas piezas, casi nada es desconocido: `µ` pasa a `μ` (la letra griega, que se ve igual) y `³` a `3`. Su normalizador las convierte antes de partir.
- El precio: una tabla de un vector por pieza, unos 250 000. En el ejercicio 04 verás que es casi todo el modelo.

### 7. Un lote para el modelo

Descomenta el **PASO 7** y ejecuta:

```
input_ids: [[4, 10777, 1238, 13806, 1009, 5, 1, 1], [4, 1162, 21042, 1008, 4692, 1084, 11303, 5]]
token_type_ids: [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
attention_mask: [[1, 1, 1, 1, 1, 1, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1]]
['[CLS]', 'Fil', '##tro', 'sucio', '.', '[SEP]', '[PAD]', '[PAD]']
['[CLS]', 'El', 'sensor', 'de', 'Norte', 'no', 'responde', '[SEP]']
de vuelta a texto: 'El sensor de Norte no responde'
```

Lo que de verdad recibe un modelo:

- **`input_ids`**: el número de cada pieza en el vocabulario.
- **`[CLS]`** (4) al principio y **`[SEP]`** (5) al final: piezas especiales que BERT espera.
- **`padding=True`**: la nota corta se rellena con `[PAD]` (1) hasta la longitud de la más larga. Un tensor necesita filas iguales.
- **`truncation=True, max_length=8`**: la nota larga se corta en 8 piezas. "desde la madrugada" se pierde: `decode` lo confirma.
- **`attention_mask`**: 1 en las piezas de verdad, 0 en el relleno. Con ella, el modelo no mira el relleno (ejercicio 02, paso 4).
- **`token_type_ids`**: para tareas con dos frases (pregunta y respuesta). Aquí, todo 0.

Para terminar, escribe en un comentario al final de `main.py` tres palabras de tu dominio que crees que el tokenizador del paso 5 partirá en varias piezas. Compruébalo con `spanish.tokenize(...)`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `PyTorch was not found. Models won't be available` | Es un aviso: este ejercicio solo usa tokenizadores. Sigue |
| `OSError: We couldn't connect to 'https://huggingface.co'` | Sin red no se descarga. Con la caché llena de un intento anterior, `HF_HUB_OFFLINE=1 uv run python main.py` |
| `OSError: ... is not a valid git identifier (branch name, tag name or commit id)` | La `revision` está mal copiada: son 40 caracteres hexadecimales |
| Tu paso 4 da otras piezas | Falta el normalizador (`NFD`, `StripAccents`, `Lowercase`) o el `pre_tokenizer` |
| `NameError: name 'model' is not defined` en el paso 4 | Descomentaste la línea de `merges` sin el bucle de arriba |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Clasificar notas en tu Observatorio](../../1-teoria/05-clasificar-notas-en-tu-observatorio.md) | **Ejercicio 01 · Del texto a números** | [Ejercicio 02 · La atención por dentro](../ejercicio-02-la-atencion-por-dentro/README.md) |
