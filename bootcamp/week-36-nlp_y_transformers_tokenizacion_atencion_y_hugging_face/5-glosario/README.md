# Glosario — Semana 36

| Término | Definición |
|---|---|
| **Atención** (*self-attention*) | Cambiar el vector de cada pieza por una media de los vectores de todas las piezas, con más peso para las que más le importan |
| ***Attention mask*** (máscara de atención) | Una fila de 1 y 0 que dice qué piezas son de verdad y cuáles relleno, para que el modelo no mire el relleno |
| **Bolsa de palabras** (*bag of words*) | Representar un texto por cuántas veces sale cada palabra, sin el orden. `CountVectorizer` |
| **BPE** (*Byte Pair Encoding*) | Un tokenizador que empieza con letras sueltas y junta una y otra vez la pareja más frecuente, hasta tener las piezas pedidas |
| **Cabeza** (*head*) | Cada una de las atenciones que se hacen a la vez en una capa, con su propia consulta, clave y valor |
| **Clave** (*key*) | En la atención, lo que cada pieza ofrece a las que buscan |
| **Consulta** (*query*) | En la atención, lo que busca cada pieza |
| **Conexión residual** | Sumar a la salida de una parte del bloque su propia entrada: deja pasar la información y el gradiente entre capas |
| ***Decoder*** | Un Transformer que genera texto pieza a pieza, con atención causal. GPT, Llama, Claude |
| **Embedding** | El vector que representa una pieza, una frase o una nota. Se aprende; los parecidos acaban cerca |
| ***Encoder*** | Un Transformer que lee el texto entero, con atención de todas con todas. BERT, MiniLM, tu `Encoder` |
| **Estratificado** | Un reparto al azar que mantiene en cada parte la misma proporción de cada clase. `stratify=` |
| **Ficha del modelo** (*model card*) | El `README.md` de un modelo en el Hub: tarea, idioma, licencia, datos y limitaciones |
| **Hub** | El repositorio de modelos y datos de Hugging Face |
| **Máscara causal** | La que impide a cada pieza mirar las siguientes. La usan los modelos que generan |
| ***Pipeline*** | En `transformers`, tokenizador, modelo y posproceso juntos para una tarea. `pipeline("zero-shot-classification")` |
| **Pieza** (*token*) | Cada trozo en que el tokenizador parte un texto: una palabra, parte de una palabra o un signo |
| **Pieza especial** | Una pieza con un papel fijo: `[PAD]` (relleno), `[UNK]` (desconocida), `[CLS]` y `[SEP]` (principio y separación) |
| **Posición** (*positional embedding*) | El vector que se suma a cada pieza para que el modelo sepa dónde está |
| **Preentrenar** | Entrenar un modelo con muchísimo texto sin etiquetas (adivinar piezas tapadas o la siguiente) antes de usarlo para una tarea |
| **Relleno** (*padding*) | Piezas `[PAD]` que se añaden a los textos cortos para que todo el lote tenga la misma longitud |
| ***revision*** | El *commit* exacto de un modelo del Hub, para descargar siempre los mismos pesos |
| ***safetensors*** | Un formato de pesos que solo guarda tensores: cargarlo no ejecuta código |
| **Similitud coseno** | El parecido de dos vectores por su dirección: 1 iguales, 0 sin relación |
| **SentencePiece** | Un tokenizador que trabaja con el texto y sus espacios, y marca el comienzo de palabra con `▁` |
| **TF-IDF** | Pesar cada palabra por su frecuencia en el texto y lo rara que es en todos. `TfidfVectorizer` |
| **Tokenizador** | Lo que parte un texto en piezas y las convierte en identificadores. Cada modelo tiene el suyo |
| **Transformer** | Una red hecha de bloques de atención y redes por pieza, con sumas y normalizaciones (2017) |
| **Valor** (*value*) | En la atención, lo que cada pieza aporta cuando la eligen |
| **Vocabulario** | Las piezas (o palabras) que conoce un tokenizador o un vectorizador |
| **WordPiece** | El tokenizador de BERT, primo de BPE; marca con `##` las piezas que continúan una palabra |
| ***Zero-shot*** | Clasificar en clases que el modelo nunca vio en entrenamiento, describiéndolas con palabras |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
