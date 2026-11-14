# 04 · Hugging Face

⏱️ 50 min

## 🎯 Objetivos

- Encontrar un modelo en el Hub y leer su ficha: tarea, idioma, licencia, tamaño.
- Descargarlo de forma reproducible y segura: `revision`, `safetensors`, sin `trust_remote_code`.
- Usar `AutoTokenizer`, `AutoModel...` y `pipeline`.
- Elegir entre *zero-shot*, embeddings con un clasificador, y afinar.

---

## 1. El Hub

[Hugging Face](https://huggingface.co) es, a la vez, un repositorio de modelos (el **Hub**, con más de un millón) y las bibliotecas para usarlos:

| Biblioteca | Para qué | Esta semana |
|---|---|---|
| `tokenizers` | Entrenar y usar tokenizadores, en Rust | Proyecto y ejercicio 01 |
| `transformers` | Cargar modelos preentrenados, usarlos y afinarlos | Ejercicios 01 a 04 |
| `huggingface-hub` | Descargar del Hub, con caché | Lo usan las dos de arriba |

Cada modelo es un repositorio git con sus pesos, su configuración, su tokenizador y una **ficha** (*model card*, el `README.md`). Antes de usar uno, la ficha responde cuatro preguntas:

- **¿Qué tarea?** Un BERT preentrenado no clasifica nada; uno afinado para inferencia (NLI) sirve para *zero-shot*; uno de `sentence-transformers` da embeddings.
- **¿Qué idioma?** Un modelo en inglés parte "recalibró" en piezas sin sentido. Para tus notas: español o multilingüe.
- **¿Qué licencia?** MIT y Apache 2.0 permiten casi todo; otras prohíben el uso comercial o piden condiciones. Los dos modelos de los ejercicios son MIT y Apache 2.0.
- **¿Qué tamaño?** 110 millones de parámetros son unos 440 MB y van bien en una CPU; 7000 millones necesitan una GPU.

## 2. Descargar sin sorpresas

`from_pretrained` descarga la primera vez y guarda en una caché (`~/.cache/huggingface/hub`, o donde diga `HF_HOME`). Las siguientes, lee de la caché:

```python
from transformers import AutoConfig, AutoTokenizer

NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
REVISION = "e8f8c211226b894fcb81acc59f3b34ba3efd5f42"
config = AutoConfig.from_pretrained(NAME, revision=REVISION)
print(config.model_type, config.num_hidden_layers, config.num_attention_heads, config.hidden_size)
print(config.vocab_size, config.max_position_embeddings)
tokenizer = AutoTokenizer.from_pretrained(NAME, revision=REVISION)
print(tokenizer("Se limpió el filtro.")["input_ids"])
```

```
bert 12 12 384
250037 512
[0, 503, 400, 11368, 849, 88, 132353, 5, 2]
```

12 capas de 12 cabezas sobre vectores de 384: lo que viste en el ejercicio 02. La tabla de piezas tiene 250 037 filas, algunas más que las 250 002 del tokenizador: es habitual reservar filas que nunca se usan.

Tres costumbres, que en el bootcamp son reglas:

- **`revision`**: el *commit* exacto del repositorio del modelo, como fijar una versión con `==` en `pyproject.toml`. Sin ella, `from_pretrained` baja lo último de la rama `main`, y el dueño puede cambiar los pesos mañana: tus resultados cambiarían sin que tocaras nada.
- **`safetensors`**: elige modelos con `model.safetensors`. Un `pytorch_model.bin` antiguo es `pickle`, y cargar un `pickle` puede ejecutar código (el `weights_only=True` de la semana 35). `transformers` usa `safetensors` siempre que el repositorio lo tiene.
- **Nunca `trust_remote_code=True`** con un modelo que no has revisado: deja que el repositorio ejecute su propio código Python en tu máquina.

Sin red, `HF_HUB_OFFLINE=1` lee solo de la caché y falla si falta algo, en lugar de quedarse esperando.

## 3. Las clases `Auto`

`config.json` dice qué arquitectura es; las clases `Auto` eligen la clase de Python que toca:

| Clase | Devuelve | Ejercicio |
|---|---|---|
| `AutoTokenizer` | El tokenizador del modelo | 01 |
| `AutoModel` | El cuerpo: un vector por pieza (`last_hidden_state`) | 02 y 03 |
| `AutoModelForSequenceClassification` | El cuerpo y una capa lineal con una puntuación por clase | 03 y 04 |

Con `num_labels=3`, `AutoModelForSequenceClassification` añade una salida nueva, al azar, sobre un cuerpo preentrenado: el `freeze` y la capa nueva de la semana 35, hechos por la biblioteca. `transformers` avisa en la terminal de que esos pesos son nuevos: es lo esperado.

Un modelo de `transformers` es un `nn.Module` de PyTorch: `model.eval()`, `torch.no_grad()`, `model.parameters()` y un bucle de entrenamiento como el tuyo funcionan igual (ejercicio 04). Al llamarlo con `labels=`, devuelve también la pérdida (entropía cruzada).

## 4. `pipeline`

Para usar un modelo sin escribir el tokenizado ni el `softmax`, `pipeline` junta las tres piezas:

```python
from transformers import pipeline

extractor = pipeline("feature-extraction", model=NAME, revision=REVISION, device="cpu")
vectors = extractor(["Se limpió el filtro.", "El sensor no responde."])
print(len(vectors), len(vectors[0][0]), len(vectors[0][0][0]))
```

```
2 9 384
```

Dos notas, cada una con sus piezas, cada pieza con 384 números: la salida de `AutoModel` como listas. Las tareas que usas esta semana:

| Tarea | Qué devuelve | Necesita un modelo |
|---|---|---|
| `"zero-shot-classification"` | La etiqueta más probable de las que le das, sin entrenar | Afinado para inferencia (NLI) |
| `"text-classification"` | La etiqueta del modelo afinado | Afinado para tu tarea (ejercicio 04, paso 6) |
| `"feature-extraction"` | Un vector por pieza | Cualquiera |
| `"fill-mask"` | Qué pieza va en `[MASK]` | Preentrenado con piezas tapadas (BERT) |

`pipeline` es cómodo para probar. En tu código, las clases `Auto` dejan ver y controlar cada paso.

## 5. Tres formas de usar un modelo preentrenado

| | Etiquetas que necesitas | Coste | Con tus notas (ejercicios 03 y 04) |
|---|---|---|---|
| **Zero-shot**: preguntarle si la nota implica "Este ejemplo es avería." | Ninguna (solo para medir) | Una pasada por tipo y nota: lento con muchos tipos | 0,72 con la plantilla buena, 0,58 con otra |
| **Embeddings + clasificador**: los vectores del ejercicio 03 con una regresión logística | Pocas | Una pasada por nota, una vez; el clasificador es instantáneo | 0,84 en prueba; 5 de 6 con otras palabras |
| **Afinar**: entrenar todo el modelo con un ritmo pequeño | Pocas a muchas | Un entrenamiento de verdad; 2 GB de RAM | 0,82 en prueba; 6 de 6 con otras palabras |
| (TF-IDF, la referencia) | Pocas | Nada | 0,87 en prueba; 2 de 6 con otras palabras |

Con estas notas de plantilla, en la prueba nadie gana a TF-IDF: las notas de prueba repiten las frases del entrenamiento, y un 15 % no dice nada. La diferencia aparece **con otras palabras**: lo que pasa cuando escribe otro técnico. Por eso un modelo se evalúa también con ejemplos que no se parecen al entrenamiento.

Por dónde empezar con tu dominio: TF-IDF como referencia; embeddings con un clasificador como primer intento (barato y sin entrenar el modelo); afinar solo si los embeddings se quedan cortos y tienes cientos de notas etiquetadas.

## 6. Lo que cuesta

- **Tamaño**: 470 MB por modelo, más PyTorch. La imagen del Observatorio pasaría de 2,5 GB a más de 3. Por eso el proyecto entrena su propio `Encoder` pequeño y usa solo `tokenizers`, sin descargar nada: los tests y la CI no dependen del Hub.
- **Tiempo**: en CPU, un modelo de 110 millones de parámetros clasifica decenas de notas por segundo. Para miles de notas al día basta; para millones, hace falta GPU o un modelo más pequeño.
- **Datos**: un modelo del Hub corre **en tu máquina**: tus notas no salen de ella. Con un modelo por API (semana 37), sí salen. Si las notas tienen datos personales, es una diferencia que importa (semana 41).

## ⚠️ Errores comunes

| Error | Consecuencia | Mejor |
|---|---|---|
| `from_pretrained(nombre)` sin `revision` | Los resultados cambian el día que el autor sube otros pesos | `revision="<commit>"`, como un `==` |
| Cargar un `pytorch_model.bin` de un repositorio desconocido | `pickle` puede ejecutar código | Modelos con `model.safetensors` |
| `trust_remote_code=True` por costumbre | El repositorio ejecuta su código en tu máquina | Solo con código revisado, y fijado con `revision` |
| Un modelo en inglés para notas en español | Piezas sin sentido y un acierto pobre | Español o multilingüe, según la ficha |
| No leer la licencia | Un modelo que no puedes usar en tu producto | Mirar la licencia en la ficha antes de empezar |
| Medir solo con notas parecidas a las de entrenamiento | Un modelo que se rompe con el primer técnico nuevo | Una prueba con otras palabras |

## ✅ Qué debes saber al terminar

- Qué responde la ficha de un modelo y cómo elegir uno para tus notas.
- Por qué fijar `revision`, preferir `safetensors` y no usar `trust_remote_code`.
- Qué hacen `AutoTokenizer`, `AutoModel` y `AutoModelForSequenceClassification`, y cuándo usar `pipeline`.
- Las tres formas de usar un modelo preentrenado, y cuál probar primero.
- Por qué el proyecto no descarga ningún modelo.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [03 · El Transformer](03-el-transformer.md) | **04 · Hugging Face** | [05 · Clasificar notas en tu Observatorio](05-clasificar-notas-en-tu-observatorio.md) |
