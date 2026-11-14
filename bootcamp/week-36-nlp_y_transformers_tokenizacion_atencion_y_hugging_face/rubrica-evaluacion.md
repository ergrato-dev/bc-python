# Rúbrica de Evaluación — Semana 36: NLP y Transformers, tokenización, atención y Hugging Face

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 35 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | ¿Qué es una bolsa de palabras? ¿Qué añade TF-IDF? ¿Qué dos cosas no puede ver ninguna bolsa de palabras? Da un ejemplo de cada una con notas de tu dominio. | 10 |
| 2 | Describe cómo aprende BPE sus piezas. ¿Por qué una palabra que nunca vio no se pierde? ¿Qué hacen el normalizador y el pre-tokenizador de `language.tokenizer`? | 10 |
| 3 | ¿En qué se diferencian WordPiece y SentencePiece? ¿Por qué no puedes usar el tokenizador de un modelo con otro modelo? | 10 |
| 4 | ¿Qué son el relleno, el corte y la máscara de atención? ¿Qué pasaría en tu `Encoder` si la atención mirase el relleno? | 10 |
| 5 | Calcula a mano los pesos de atención de "filtro" en la sección 3 de la teoría 02: escribe las tres operaciones. ¿Para qué se divide por `√d`? ¿Qué papel tienen la consulta, la clave y el valor? | 10 |
| 6 | ¿Por qué la atención no ve el orden? ¿Cómo se lo enseña tu `Encoder`? ¿Qué test del proyecto lo comprueba? | 10 |
| 7 | ¿Cuáles son las cuatro partes de un bloque Transformer? Cuenta los 6243 parámetros de tu `Encoder` con 200 piezas y 3 tipos. | 10 |
| 8 | ¿Qué diferencia un *encoder* de un *decoder*? ¿Qué es preentrenar y afinar? ¿Por qué tu `Encoder` desde cero, con 180 notas, no gana a TF-IDF? | 10 |
| 9 | ¿Por qué fijar `revision`, preferir `safetensors` y no usar `trust_remote_code`? Con los números de los ejercicios 03 y 04, compara *zero-shot*, embeddings y afinar. | 10 |
| 10 | En `classify`, ¿por qué el reparto es al azar y estratificado, y no por tiempo? ¿Qué tres cosas aprenden solo de las notas de entrenamiento? ¿Por qué el acierto del Transformer se calcula en `float` de Python? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. Representar cada nota por cuántas veces sale cada palabra del vocabulario. TF-IDF multiplica esa frecuencia por lo rara que es la palabra en todas las notas: "de" pesa poco, "quemada" mucho. No ve el **orden** ("se limpió el filtro, no el sensor" y al revés dan el mismo vector) ni las **palabras nuevas** ("recalibrado" no existe si al ajustar solo salía "recalibró").
2. Empieza con cada carácter como pieza, cuenta la pareja de piezas seguidas más frecuente del corpus y la junta en una pieza nueva; repite hasta tener las piezas pedidas. Una palabra nueva se parte en piezas que sí conoce, en el peor caso letras sueltas. El normalizador quita tildes (`NFD` y `StripAccents`) y mayúsculas (`Lowercase`): "Calibración" y "calibracion" dan lo mismo. El pre-tokenizador `Whitespace` separa por espacios y signos antes de juntar: ninguna pieza cruza dos palabras.
3. WordPiece (BERT) marca con `##` las piezas que **continúan** una palabra y usa `[CLS]`, `[SEP]`, `[PAD]`; SentencePiece trata el espacio como parte del texto y marca con `▁` las que **empiezan** una palabra, con `<s>`, `</s>`, `<pad>`. Cada modelo aprendió un vector para cada identificador de **su** vocabulario: con otro tokenizador, el identificador 503 es otra pieza, y el modelo lee otra cosa sin dar ningún error.
4. Relleno: piezas `[PAD]` para que todas las notas del lote tengan la misma longitud. Corte: las notas más largas que el máximo se quedan en él y pierden el final. Máscara: 1 en las piezas de verdad, 0 en el relleno. Si la atención mirase el relleno, las puntuaciones de una nota cambiarían según la nota más larga de su lote; `test_encoder_does_not_look_at_the_padding` lo detecta.
5. `X @ X.T` (el producto escalar de "filtro" con cada palabra), `/ √2` y `softmax` de la fila: 0,32, 0,30, 0,19 y 0,18. Sin dividir por `√d`, con vectores grandes los productos escalares son enormes y `softmax` daría casi todo el peso a una pieza, con gradientes que se apagan. La consulta es lo que busca cada pieza; la clave, lo que ofrece; el valor, lo que aporta si la eligen. Las tres son capas lineales que se aprenden.
6. Es una media con pesos: si desordenas las piezas, cada una recibe lo mismo, solo en otro sitio. Tu `Encoder` suma a cada pieza el vector de su posición, de una segunda tabla `nn.Embedding` (`self.positions`). `test_encoder_cares_about_the_order`: las mismas piezas en otro orden dan otras puntuaciones.
7. Atención de varias cabezas; suma con la entrada y normalización; una red para cada pieza (dos lineales con ReLU); otra suma y normalización. Piezas 200 × 16 = 3200; posiciones 48 × 16 = 768; atención 4 × 16 × 16 + 4 × 16 = 1088; red 16 × 32 + 32 + 32 × 16 + 16 = 1072; normalizaciones 2 × 32 = 64; salida 16 × 3 + 3 = 51. Total 6243.
8. Un *encoder* lee el texto entero, cada pieza mira a todas: sirve para clasificar y para embeddings (BERT). Un *decoder* genera pieza a pieza con máscara causal: cada pieza solo mira las anteriores (GPT, Claude). Preentrenar: entrenar con muchísimo texto sin etiquetas, adivinando piezas tapadas o la siguiente; afinar: seguir entrenando con pocas etiquetas de tu tarea y un ritmo pequeño. Tu `Encoder` empieza sin saber nada del idioma: con 180 notas solo puede aprender las palabras de esas notas, lo mismo que TF-IDF, con muchos más parámetros.
9. Sin `revision`, el dueño puede cambiar los pesos y tus resultados cambian sin tocar nada. Un `.bin` es `pickle` y cargarlo puede ejecutar código; `safetensors` solo guarda tensores. `trust_remote_code` deja que el repositorio ejecute su Python en tu máquina. *Zero-shot*: sin etiquetas, 0,72 con la plantilla del modelo y 0,58 con otra. Embeddings con 30 notas: 0,84 en prueba y 5 de 6 con otras palabras. Afinar con 30 notas: 0,82 y 6 de 6. TF-IDF: 0,87 y 2 de 6. En la prueba, que repite frases, empatan; con otras palabras ganan los preentrenados.
10. Las notas no son una serie: cada una se clasifica por lo que dice, no por las anteriores. Estratificado, para que las tres partes tengan la misma proporción de cada tipo, aunque haya pocas notas. El tokenizador BPE, TF-IDF y el Transformer: si vieran la prueba, sus palabras ya serían conocidas y el acierto sería falso. En `float32`, 52/60 es 0,86666667, más que el 0,8666... de TF-IDF: el Transformer ganaría un empate que no ha ganado.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños y rojo a verde | Un commit por paso, sin cambiar los tests del bootcamp, cada uno con los ganchos; puede decir qué tests pasaron a verde con cada paso | 8 |
| Ejecución en vivo | Ante el instructor: `clasificar` por defecto, con otra semilla, con `--vocabulario 60` y con dos `--nota` de su dominio, y `pytest` en verde | 8 |
| Rompe y explica | Entrena el tokenizador con todas las notas y explica qué test falla y por qué el acierto sería engañoso; quita la máscara del relleno y explica qué cambia | 8 |
| Explica su red | Cuenta a mano los parámetros de su `Encoder`; lee la tabla de la pérdida, dónde paró, el acierto de cada modelo y por cuántas notas gana el ganador | 8 |
| Sus notas | Explica de dónde salen sus notas, qué tipos y qué pistas engañosas tienen, y qué haría con notas reales (ejercicios 03 y 04) | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 35

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| El módulo | `read_notes` con sus validaciones; `tokenizer` BPE con normalizador, pre-tokenizador, `[PAD]` en el 0, relleno y corte; `Encoder` con posiciones, máscara de relleno y media sin relleno; `classify` estratificado, con el tokenizador y TF-IDF ajustados solo con entrenamiento, `fit` con `CrossEntropyLoss` y acierto exacto; `predict`; sin reexportar en `core/__init__.py` | 25 |
| El comando | `clasificar` con el import dentro y las cinco opciones; `fit` con `loss_function`; el reparto, las piezas de una nota, la pérdida, el acierto de cada modelo y el veredicto; código 1 y 2 según el error | 15 |
| Tests propios | Al menos 6 tests en `tests/test_my_language.py` con notas de su dominio, cada uno visto fallar con un mutante | 20 |
| Calidad | `pre-commit run --all-files`, `coverage report` y `alembic check` sin avisos; `docker compose run --rm app` y la CI en verde; `tokenizers==0.23.3`, imágenes `week-36` y versión `0.36.0` | 15 |
| Git y README | Rama `week-36` en `python-<nombre>-<apellido>` con `notas.csv` de su dominio; README con la sección "Notas", e `informe/README.md` con el resultado en "Siguientes pasos" | 10 |
| Pull request | Salidas, CI, `clasificar` por defecto, con otra semilla y con dos `--nota`, con su lectura, y la tabla de mutantes con las dos respuestas | 15 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | Semana 37 (próximamente) |
