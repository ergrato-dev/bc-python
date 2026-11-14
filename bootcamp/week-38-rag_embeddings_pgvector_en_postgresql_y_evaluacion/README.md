# Semana 38 — RAG: embeddings, pgvector en PostgreSQL y evaluación

> En la semana 37, Claude respondía con lo que sabe en general. Esta semana responde con **tus** documentos. Conviertes textos en vectores y los guardas en PostgreSQL con pgvector. Para cada pregunta, buscas los fragmentos más cercanos y se los das a Claude, que responde con ellos y los cita: es RAG. Después lo mides por partes, la búsqueda y la respuesta, con números en lugar de impresiones. Tu Observatorio gana tres comandos: `indexar`, `buscar` y `preguntar`. Los vectores salen de TF-IDF y LSA, sin descargas, y las respuestas de Claude se graban y se repiten, como en la semana 37.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Convertir** textos en vectores con TF-IDF y LSA, y **compararlos** con un modelo de embeddings preentrenado
- **Guardar** vectores en PostgreSQL con pgvector y **buscar** los más cercanos con SQL y SQLAlchemy
- **Distinguir** la búsqueda exacta de la aproximada con HNSW, y **ajustar** `ef_search` y los filtros
- **Construir** un RAG: trocear, recuperar, aumentar el prompt y generar con citas que tu código comprueba
- **Evaluar** la búsqueda con recall@k, MRR y precisión@k, y la respuesta con reglas y un LLM como juez
- **Reconocer** las preguntas que no son de RAG, como contar o sumar, y mandarlas a SQL

---

## 📋 Prerrequisitos

- [Semana 37](../week-37-llms_por_api_prompting_salida_estructurada_y_tool_use/README.md): la API de Messages, prompting, salida estructurada, grabaciones y `leer-notas`.
- [Semana 36](../week-36-nlp_y_transformers_tokenizacion_atencion_y_hugging_face/README.md): TF-IDF, *encoders* y el modelo multilingüe del ejercicio 03.
- [Semana 33](../week-33-arboles_ensembles_gradient_boosting_y_no_supervisado/README.md): PCA y k-means.
- [Semana 19](../week-19-postgresql_psycopg_sqlalchemy_y_alembic/README.md): PostgreSQL, SQLAlchemy 2 y Alembic.
- El *pull request* `week-37` de tu proyecto fusionado en `main`, con la CI en verde.
- **Opcional**: una clave de la API de Anthropic, con un límite de gasto. Todo se puede hacer sin ella.

---

## 🗂️ Estructura de la Semana

```
week-38-rag_embeddings_pgvector_en_postgresql_y_evaluacion/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 4 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 37 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
|---|---|---|
| [01 · Embeddings](1-teoria/01-embeddings.md) | Vectores de texto, coseno, TF-IDF, LSA, léxico frente a semántico y cómo elegir de dónde salen los vectores | 50 min |
| [02 · pgvector](1-teoria/02-pgvector.md) | La extensión, `vector(n)`, las distancias, la búsqueda exacta, HNSW, `ef_search`, los filtros y el cambio de imagen | 50 min |
| [03 · RAG](1-teoria/03-rag.md) | Trocear, recuperar, aumentar y generar con citas, lo que RAG no hace y la inyección en los documentos | 50 min |
| [04 · Evaluar un RAG](1-teoria/04-evaluar-un-rag.md) | Preguntas etiquetadas, recall@k, MRR, precisión@k, reglas, un LLM como juez y decidir con números | 45 min |
| [05 · RAG en tu Observatorio](1-teoria/05-rag-en-tu-observatorio.md) | `indexar`, `buscar` y `preguntar`, `core/rag.py`, el modelo que se rehace, `claude()` y la grabación de ejemplo | 45 min |

### Prácticas

| Ejercicio | Qué haces | Duración |
|---|---|---|
| [01 · Embeddings](2-practicas/ejercicio-01-embeddings/README.md) | Contar palabras, TF-IDF, LSA, longitud 1, un modelo preentrenado y buscar con los dos | 1 h 30 min |
| [02 · pgvector por dentro](2-practicas/ejercicio-02-pgvector-por-dentro/README.md) | La extensión, tres distancias, una tabla, veinte mil vectores, un índice HNSW, `ef_search` y un filtro | 1 h 30 min |
| [03 · RAG paso a paso](2-practicas/ejercicio-03-rag-paso-a-paso/README.md) | Un manual: sin contexto, trocear, recuperar, generar con citas, una cita inventada y `k` | 1 h 30 min |
| [04 · Evaluar un RAG](2-practicas/ejercicio-04-evaluar-un-rag/README.md) | Doce preguntas etiquetadas, recall@k, MRR, dos troceos, reglas y un juez | 1 h 30 min |

### Proyecto

Añades a tu Observatorio:

- `core/rag.py`: la tabla `Note`, `embedder`, `embed`, `index`, `model_of`, `search`, `vote`, `Evaluation`, `evaluate`, `Answer`, `INSTRUCTIONS`, `context`, `ask` y `Reply`;
- la migración `0002`, con la extensión `vector` y la tabla `notes`;
- la dependencia `pgvector` y una imagen de PostgreSQL que trae la extensión;
- `claude()`, sacado de `leer-notas`, y los comandos `indexar NOTAS`, `buscar TEXTO` y `preguntar PREGUNTA`.

55 tests nuevos: 54 de `rag` y sus comandos, y un ejemplo tuyo. La versión sube a `0.38.0`. **Es el único entregable de la semana.**
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
| ¿Tiene pgvector esta base? | `SELECT extversion FROM pg_extension WHERE extname = 'vector';` |
| Ver si una búsqueda usa el índice | `EXPLAIN (COSTS OFF) SELECT ... ORDER BY embedding <=> ... LIMIT 5;` |
| La distancia de coseno en SQLAlchemy | `Note.embedding.cosine_distance(vector)` |
| Más acierto con HNSW en una sesión | `SET hnsw.ef_search = 100;` |
| Un filtro con HNSW que no se quede corto | `SET hnsw.iterative_scan = relaxed_order;` |
| Cuánto conserva LSA | `svd.explained_variance_ratio_.sum()` |
| Las palabras que pesan en una nota | `vectorizer.get_feature_names_out()` y la fila de TF-IDF |
| Buscar sin gastar | `buscar` no llama a Claude |
| Repetir sin gastar | `preguntar ... --grabacion preguntas-claude.json` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-38` de `python-<nombre>-<apellido>` con:
   - `core/rag.py` sin reexportar en `core/__init__.py`, la migración `0002` y los comandos `indexar`, `buscar` y `preguntar`, con los imports dentro;
   - `pgvector==0.5.1`, la imagen de PostgreSQL con pgvector en `compose.yaml` y en la CI, las imágenes `week-38` y la versión `0.38.0`;
   - al menos 6 tests propios en `tests/test_my_rag.py`.

   Todo en verde en tu máquina, en Docker y en GitHub Actions, sin ninguna clave en el repositorio.
2. ✅ `README.md` del repositorio con la sección "Búsqueda y preguntas", e `informe/README.md` con el resultado en "Siguientes pasos"
3. ✅ Pull request `week-38` → `main` con:
   - las salidas de los ganchos, la cobertura, `alembic check` y la CI en verde;
   - la salida de `indexar` con tus notas, una de `preguntar` y tu lectura;
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
uv run observatorio indexar $STARTER/notas.csv
uv run observatorio buscar "el sensor no envía datos" -k 3
uv run observatorio preguntar "¿Cuánto costó cambiar el filtro?" --grabacion $STARTER/preguntas-claude-ejemplo.json
uv run observatorio buscar xyz; echo $?
uv run observatorio preguntar "¿Cuánto costó cambiar el filtro?"; echo $?
uv run python -c "import sys, observatorio.cli; print([m in sys.modules for m in ('pgvector', 'sklearn', 'anthropic')])"
git grep -n "sk-ant-" || echo "sin claves"
docker compose build app api && docker compose run --rm app
gh pr checks
```

Lo que debes ver:

- todos los ganchos en `Passed` (o `Skipped`);
- los tests terminan en `passed` sin `failed`, al menos 1564;
- `coverage report` termina sin `Coverage failure`;
- `alembic check` dice `No new upgrade operations detected.`;
- `--version` escribe `observatorio 0.38.0`;
- `indexar` termina con `el voto de las 5 más cercanas acierta 57 de 60 (0.950)`;
- `buscar` trae tres calibraciones, y `preguntar` responde que las notas no lo dicen, con `citas: ninguna`;
- `buscar xyz` da `error: ninguna nota se parece` y código 1; `preguntar` sin clave, `error: falta ANTHROPIC_API_KEY` y código 2;
- la comprobación de `sys.modules` escribe `[False, False, False]`, y `git grep` escribe `sin claves`;
- `gh pr checks` con `quality`, `tests` e `image` en `pass`.

En los ejercicios, cada paso descomentado da la salida que muestra su README.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 37](../week-37-llms_por_api_prompting_salida_estructurada_y_tool_use/README.md) | **Semana 38** | Semana 39 (próximamente) |
