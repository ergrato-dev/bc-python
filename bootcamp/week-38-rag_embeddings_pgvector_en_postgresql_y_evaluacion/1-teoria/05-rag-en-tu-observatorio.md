# 05 · RAG en tu Observatorio

⏱️ 45 min

## 🎯 Objetivos

- Entender qué hacen `indexar`, `buscar` y `preguntar`, y qué comparan.
- Conocer `core/rag.py`: la tabla, los vectores, la búsqueda, la evaluación y la pregunta a Claude.
- Entender por qué el modelo de los vectores se rehace y no se guarda.
- Probar una búsqueda en PostgreSQL y una pregunta a Claude sin red ni clave.
- Leer la salida con la grabación de ejemplo, sin sacar de ella lo que no dice.

## 1. Lo que añade la semana

`clasificar` (semana 36) y `leer-notas` (semana 37) asignan un tipo a las mismas 60 notas de prueba. Esta semana las notas pasan a PostgreSQL con un vector cada una, y tu Observatorio aprende a **buscarlas** y a **responder preguntas** con ellas:

```bash
uv run observatorio indexar notas.csv
uv run observatorio buscar "filtro con polvo" -k 3
uv run observatorio preguntar "¿Qué estaciones quedaron fuera de servicio por un corte de energía?"
```

| Comando | Qué hace | ¿Llama a Claude? |
|---|---|---|
| `indexar NOTAS` | Guarda las notas que no son de prueba con su vector, y mide la búsqueda con las de prueba | No |
| `buscar TEXTO` | Las `k` notas más cercanas al texto, con su distancia | No |
| `preguntar PREGUNTA` | Las `k` notas más cercanas, la respuesta de Claude con sus citas, los tokens y el coste | Sí, salvo que no haya ninguna nota parecida |

`indexar` acepta `--semilla` (la del reparto de `clasificar`) y `-k`; `buscar`, `-k`; `preguntar`, `-k`, `--grabacion` y `--grabar`, como `leer-notas`.

## 2. La tabla y la migración

`Note` es la tabla `notes`: número, etiqueta, tipo, texto y una columna `vector(32)`. Vive en `rag.py` y no en `database.py` por una razón concreta: `pgvector` carga NumPy, y `import observatorio.core` no debe cargarlo (lo comprueba `test_importing_does_not_load_numpy` desde la semana 23). Como consecuencia, `migrations/env.py` importa `rag` para que Alembic vea la tabla.

La migración `0002` la genera *autogenerate*, con dos arreglos a mano:

- `import pgvector.sqlalchemy`, que autogenerate usa y no escribe;
- `CREATE EXTENSION IF NOT EXISTS vector` antes de crear la tabla, y `DROP EXTENSION` al deshacerla.

## 3. `core/rag.py`

| Pieza | Qué hace |
|---|---|
| `DIMENSION`, `K`, `WORDS`, `MAX_TOKENS` | 32 números por vector, 5 vecinas, respuestas de 60 palabras como mucho, 1024 tokens |
| `embedder(texts)` | TF-IDF, LSA a 32 números y longitud 1, ajustado con esos textos. Falla si hay menos de 32 notas o de 32 palabras distintas |
| `embed(model, texts)` | Los vectores, en `float32` como la columna |
| `index(session, notes)` | Vacía la tabla con `TRUNCATE ... RESTART IDENTITY` y guarda cada nota con su vector |
| `model_of(session)` | Rehace el modelo con las notas guardadas |
| `search(session, model, query, k)` | Las `k` notas más cercanas por distancia de coseno; `[]` si la pregunta no tiene ninguna palabra conocida |
| `vote`, `Evaluation`, `evaluate` | El tipo más repetido entre las vecinas, la precisión@k y el acierto del voto |
| `INSTRUCTIONS`, `context`, `Answer` | El prompt de la teoría 03 y la salida estructurada: `respuesta` y `citas` |
| `ask(client, question, hits)` | Una petición con `transform_schema` y `effort`; valida solo si `stop_reason` es `end_turn` |
| `Reply` | La respuesta (o `None`), el `stop_reason`, las notas enviadas, los tokens, las citas inventadas y el coste |

Cuatro decisiones:

- **El modelo se rehace, no se guarda.** LSA se ajusta con las notas indexadas, y la pregunta necesita **el mismo** modelo. Guardarlo exigiría un archivo con su versión de scikit-learn y su sitio en Docker. Rehacerlo con las notas de la tabla, la misma semilla y los mismos textos da los mismos vectores, y tarda milisegundos con cientos de notas. Un test cambia el orden de las filas con un `UPDATE` y comprueba que los vectores no cambian. Con miles de notas, o con un modelo preentrenado, se guardaría.
- **`TRUNCATE ... RESTART IDENTITY`.** Volver a indexar las mismas notas les da los mismos números. Así las citas de una grabación siguen valiendo, y el resultado no depende de cuántas veces indexaste.
- **PostgreSQL calcula y ordena.** `search` no trae los vectores a Python: pide `cosine_distance` (el `<=>`) ordenado y con `LIMIT`. A igual distancia, sale primero la nota más antigua. Un test compara esa distancia con la de NumPy.
- **Sin índice HNSW.** Con 240 notas, la búsqueda exacta tarda menos de un milisegundo y nunca se equivoca (teoría 02).

## 4. Medir la búsqueda con las mismas 60 notas

`indexar` reparte con `llm.split` y la misma semilla que `clasificar` y `leer-notas`. Indexa solo las 240 notas que **no** son de prueba, y busca cada una de las 60 de prueba entre ellas:

- **precisión@5:** de sus 5 vecinas, ¿cuántas son de su tipo?
- **voto:** ¿el tipo más repetido entre las 5 es el suyo? Los empates los decide la vecina más cercana.

Así la búsqueda se compara con los clasificadores, con las mismas notas:

| Comando | Acierto con las notas de ejemplo |
|---|---|
| `clasificar` (TF-IDF y regresión logística) | 0.950 |
| `leer-notas` (Claude, grabación de ejemplo) | 0.917 |
| `indexar` (voto de las 5 vecinas) | 0.950 |

Que el voto acierte tanto como el clasificador dice que las vecinas de una nota suelen ser de su tipo. Es lo que necesita `preguntar`: si las notas cercanas fueran de cualquier tipo, la respuesta saldría de notas que no vienen al caso.

## 5. `claude()`: un refactor antes de repetir

`leer-notas` comprobaba la clave y convertía los errores de la API en mensajes. `preguntar` necesita exactamente lo mismo. En lugar de copiarlo, sale a un gestor de contexto, como `database()` en la semana 19:

```python
with claude(grabacion, grabar) as client:
    ...
```

- **Al entrar:** comprueba `--grabar` sin `--grabacion` y la clave, salvo para repetir una grabación, y crea el cliente.
- **Al salir:** convierte los errores de la API en `error: ...` con su código.

`leer-notas` queda más corto, y sus tests, que no cambian, demuestran que el refactor no rompió nada.

## 6. Probar sin red ni clave

Los tests de `test_rag.py` combinan lo de las semanas 19 y 37:

- **PostgreSQL de verdad.** La búsqueda la hace pgvector en la base de los tests, no un simulacro. `notes()` crea notas en las que el tipo se ve en dos palabras, nueve palabras por tipo: suficientes para los 32 números de LSA.
- **Claude falso.** `fake()` responde citando las dos primeras notas que recibe y, si se le pide, una que no recibió. Con él se prueban las citas inventadas, las respuestas cortadas y el coste.
- **Grabaciones.** El fixture `recorded` graba con `--grabar` y el Claude falso, y el test repite la grabación con la CLI, como en la semana 37.

## 7. Leer la salida de ejemplo

`preguntas-claude-ejemplo.json` son respuestas **de ejemplo**, con la forma exacta de la API: las escribió el bootcamp, no Claude, y los tokens son aproximados. La búsqueda sí es de verdad. Lo que enseñan:

- **«¿Qué estaciones quedaron fuera de servicio por un corte de energía?»** Las 5 notas son cortes de energía, y la respuesta cita las 5. Pero la base tiene 14: Claude solo ve 5.
- **«¿Cuánto costó cambiar el filtro?»** Ninguna nota habla de costes. La respuesta dice que las notas no lo dicen, con `citas: ninguna`.
- **«¿Qué averías hubo en Norte?»** La búsqueda se fija en «Norte» y trae tres limpiezas y dos averías. La respuesta nombra dos averías; la base tiene 17. Es una pregunta de SQL.
- **«el sensor no envía datos»**, con `buscar`, trae tres calibraciones que dicen «el sensor ... no responde igual»: el límite léxico de la teoría 01.

Lo que **no** enseñan: cómo respondería Claude de verdad, ni cuánto costaría exactamente. Para eso, `--grabar` con tu clave y tus preguntas.

## ⚠️ Errores comunes

| Error | Por qué falla | Qué hacer |
|---|---|---|
| Indexar todas las notas y medir con las de prueba | Cada nota se encuentra a sí misma: acierto falso | Indexa solo las que no son de prueba |
| `DELETE` en lugar de `TRUNCATE ... RESTART IDENTITY` | Los números cambian al reindexar, y las grabaciones dejan de valer | Reinicia la secuencia |
| Poner `Note` en `database.py` | `import observatorio.core` carga NumPy | La tabla vive en `rag.py`, y `env.py` la importa |
| Llamar a Claude sin notas parecidas | Pagas por un «no lo sé» | Si `search` devuelve `[]`, no preguntes |
| Copiar la gestión de la clave en cada comando | Dos copias que se separan con el tiempo | Un gestor de contexto, `claude()` |

## ✅ Qué debes saber al terminar

- `indexar` guarda vectores y mide la búsqueda con las mismas 60 notas que `clasificar` y `leer-notas`.
- El modelo de LSA se rehace con las notas guardadas, y da los mismos vectores.
- `search` deja la distancia y el orden a PostgreSQL, con desempate por número.
- `preguntar` no llama a Claude sin notas parecidas, y avisa de las citas inventadas.
- La grabación de ejemplo enseña el formato y los límites de RAG, no el comportamiento real de Claude.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [04 · Evaluar un RAG](04-evaluar-un-rag.md) | **05 · RAG en tu Observatorio** | [Ejercicio 01 · Embeddings](../2-practicas/ejercicio-01-embeddings/README.md) |
