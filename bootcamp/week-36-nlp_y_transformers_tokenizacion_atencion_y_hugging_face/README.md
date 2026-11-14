# Semana 36 — NLP y Transformers: tokenización, atención y Hugging Face

> Hasta ahora tu Observatorio solo leía números. Esta semana lee texto: las notas que escriben las personas de tu dominio. Conviertes texto en números (bolsas de palabras, TF-IDF y subpalabras), calculas la atención a mano, construyes un Transformer pequeño con PyTorch y usas modelos preentrenados de Hugging Face. Tu Observatorio gana un comando: `clasificar`, que compara un Transformer entrenado con tus notas frente a TF-IDF y la referencia.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Convertir** texto en números con una bolsa de palabras y TF-IDF, y **explicar** lo que pierden
- **Entrenar** un tokenizador BPE con `tokenizers` y **preparar** un lote: piezas, relleno, corte y máscara
- **Calcular** la atención a mano con consultas, claves y valores, y **aplicar** las máscaras de relleno y causal
- **Construir** un Transformer *encoder* con PyTorch, **seguir** su forma capa a capa y **contar** sus parámetros
- **Usar** modelos preentrenados de Hugging Face de forma reproducible y segura: *zero-shot*, embeddings y afinar
- **Clasificar** las notas de tu dominio sin fugas, y **comparar** honestamente un Transformer con TF-IDF

---

## 📋 Prerrequisitos

- [Semana 35](../week-35-pytorch_cnn_entrenamiento_y_transfer_learning/README.md): `fit` con mini-lotes y parada temprana, y el *transfer learning*.
- [Semana 31](../week-31-ml_con_scikit_learn_regresion_clasificacion_y_metricas/README.md): clasificar con regresión logística y medir el acierto.
- El *pull request* `week-35` de tu proyecto fusionado en `main`, con la CI en verde.
- Unos 2 GB libres en disco para los dos modelos de los ejercicios (se descargan una vez).

---

## 🗂️ Estructura de la Semana

```
week-36-nlp_y_transformers_tokenizacion_atencion_y_hugging_face/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 4 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 35 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
|---|---|---|
| [01 · Del texto a números](1-teoria/01-del-texto-a-numeros.md) | El texto libre de tu dominio, bolsa de palabras, TF-IDF, lo que no ven, BPE, WordPiece y SentencePiece, relleno y máscara | 45 min |
| [02 · Embeddings y atención](1-teoria/02-embeddings-y-atencion.md) | `nn.Embedding`, similitud coseno, la atención a mano, consultas, claves y valores, máscaras y cabezas | 50 min |
| [03 · El Transformer](1-teoria/03-el-transformer.md) | El bloque, las posiciones, tu `Encoder` capa a capa, *encoders* y *decoders*, preentrenar y afinar | 50 min |
| [04 · Hugging Face](1-teoria/04-hugging-face.md) | El Hub y las fichas, `revision`, `safetensors`, las clases `Auto`, `pipeline`, tres formas de usar un modelo y lo que cuesta | 50 min |
| [05 · Clasificar notas en tu Observatorio](1-teoria/05-clasificar-notas-en-tu-observatorio.md) | `notas.csv`, el reparto estratificado, nada aprende de la prueba, `core/language.py` y la salida de `clasificar` | 45 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, ejecutas y comparas con la salida esperada. Preparan el proyecto.

| Ejercicio | Qué haces | Duración |
|---|---|---|
| [01 · Del texto a números](2-practicas/ejercicio-01-del-texto-a-numeros/README.md) | Una bolsa a mano, TF-IDF, lo que no ve, BPE con tus notas, WordPiece y SentencePiece, un lote para el modelo | 1 h 30 min |
| [02 · La atención por dentro](2-practicas/ejercicio-02-la-atencion-por-dentro/README.md) | La atención a mano, consultas, claves y valores, máscaras, posiciones, cabezas y la atención de un modelo real | 1 h 30 min |
| [03 · Modelos preentrenados](2-practicas/ejercicio-03-modelos-preentrenados/README.md) | *Zero-shot*, un `pipeline` por dentro, embeddings, búsqueda por significado, y TF-IDF frente a embeddings con otras palabras | 1 h 30 min |
| [04 · Afinar un Transformer](2-practicas/ejercicio-04-afinar-un-transformer/README.md) | 30 notas: congelar el cuerpo, afinar todo, probabilidades y guardar en `safetensors` | 1 h 30 min |

### Proyecto

Añades a tu Observatorio:

- `notas.csv`, las notas de texto libre de tu dominio, con `scripts/generar_notas.py`;
- `core/language.py`: `read_notes`, `tokenizer`, `encode`, `pieces`, `Encoder`, `classify`, `predict` y `Classification`;
- `fit` con una función de pérdida a elegir, y la dependencia `tokenizers`;
- el comando `clasificar NOTAS [--vocabulario] [--epocas] [--paciencia] [--semilla] [--nota]`.

59 tests nuevos: 58 de `language` y `clasificar`, y un ejemplo tuyo. La versión sube a `0.36.0`. **Es el único entregable de la semana.**
→ [3-proyecto/README.md](3-proyecto/README.md)

---

## ⏱️ Distribución del Tiempo (18 horas)

| Actividad | Tiempo |
|---|---|
| Teoría (5 archivos) | 4 h |
| Ejercicio 01 | 1 h 30 min |
| Ejercicio 02 | 1 h 30 min |
| Ejercicio 03 | 1 h 30 min |
| Ejercicio 04 | 1 h 30 min |
| Proyecto | 6 h 30 min |
| Recursos y glosario | 30 min |
| Autoevaluación (cuestionario de la rúbrica) | 1 h |
| **Total** | **18 h** |

---

## 🎩 Trucos y atajos

| Truco | Cómo |
|---|---|
| Ver las piezas de un texto | `tokenizer.tokenize("recalibrado")` en `transformers`; `model.encode("...").tokens` en `tokenizers` |
| De identificadores a texto | `tokenizer.decode(ids, skip_special_tokens=True)` |
| La atención en una línea | `F.scaled_dot_product_attention(q, k, v, attn_mask=..., is_causal=...)` |
| Un vector por frase | La media de `last_hidden_state` multiplicada por `attention_mask` |
| Los mismos pesos siempre | `from_pretrained(nombre, revision="<commit de 40 caracteres>")` |
| Sin red, desde la caché | `HF_HUB_OFFLINE=1 uv run python main.py` |
| Dónde está la caché | `~/.cache/huggingface/hub`, o la carpeta de `HF_HOME` |
| Callar el aviso de pesos nuevos | `transformers.logging.set_verbosity_error()` |
| Probar una nota nueva | `uv run observatorio clasificar notas.csv --nota "..."` |
| Ver cómo parte tus palabras | `uv run observatorio clasificar notas.csv --vocabulario 60` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-36` de `python-<nombre>-<apellido>` con:
   - `notas.csv` con notas de tu dominio, y `scripts/generar_notas.py` adaptado (o tus notas reales);
   - `core/language.py` sin reexportar en `core/__init__.py`, y el comando `clasificar`, con el import dentro;
   - `fit(..., loss_function)` en `core/convolution.py`, y `tokenizers==0.23.3`;
   - las imágenes `week-36`, la versión `0.36.0` y al menos 6 tests propios en `tests/test_my_language.py`.

   Todo en verde en tu máquina, en Docker y en GitHub Actions.
2. ✅ `README.md` del repositorio con la sección "Notas", e `informe/README.md` con el resultado en "Siguientes pasos"
3. ✅ Pull request `week-36` → `main` con:
   - las salidas de los ganchos, la cobertura, `alembic check` y la CI en verde;
   - la salida de `clasificar` con tus notas, por defecto, con otra semilla y con dos `--nota`, y tu lectura;
   - la tabla de mutantes con las dos respuestas del paso 11.

El cuestionario de la [rúbrica](rubrica-evaluacion.md) es tu autoevaluación: respóndelo antes de mirar las respuestas.

---

## ✅ Verificación

En tu proyecto:

```bash
docker compose up -d --wait db
uv run pre-commit run --all-files
uv run pytest
uv run coverage run -m pytest -q && uv run coverage report
uv run alembic check
uv run observatorio --version
uv run observatorio clasificar notas.csv
uv run observatorio clasificar notas.csv --epocas 3
uv run observatorio clasificar notas.csv --nota "<una nota nueva>"
uv run observatorio clasificar no-existe.csv; echo $?
uv run python -c "import sys, observatorio.cli; print('tokenizers' in sys.modules)"
docker compose build app api && docker compose run --rm app
gh pr checks
```

Lo que debes ver:

- todos los ganchos en `Passed` (o `Skipped`);
- los tests terminan en `passed` sin `failed`, al menos 1464;
- `coverage report` termina sin `Coverage failure`;
- `alembic check` dice `No new upgrade operations detected.`;
- `--version` escribe `observatorio 0.36.0`;
- el primer `clasificar` escribe tus notas y sus tipos, el reparto, las piezas de la primera nota, la red, la tabla de la pérdida, dónde paró, el acierto de los tres modelos y el veredicto;
- el segundo, `entrenó 3 épocas`; el tercero, al final, `«...» → <tipo> (transformer, NN%)`;
- el cuarto, `error: no se puede usar no-existe.csv: No such file or directory` y código 2;
- la comprobación de `sys.modules` escribe `False`;
- `gh pr checks` con `quality`, `tests` e `image` en `pass`.

En los ejercicios, cada paso descomentado da la salida que muestra su README.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 35](../week-35-pytorch_cnn_entrenamiento_y_transfer_learning/README.md) | **Semana 36** | Semana 37 (próximamente) |
