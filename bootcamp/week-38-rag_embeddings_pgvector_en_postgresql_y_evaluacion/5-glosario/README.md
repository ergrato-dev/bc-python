# Glosario — Semana 38

| Término | Definición |
|---|---|
| **Aumentar** (*augment*) | El segundo paso de RAG: poner los fragmentos recuperados en el prompt, cada uno con su número |
| **Búsqueda aproximada** (*ANN*) | Encontrar casi siempre los vecinos más cercanos sin mirar todas las filas, con un índice como HNSW. Se mide con recall@k |
| **Búsqueda exacta** | Calcular la distancia a todas las filas y ordenarlas: siempre da los `k` más cercanos de verdad, y tarda en proporción a las filas |
| **Búsqueda híbrida** | Combinar una búsqueda léxica y una semántica: la primera encuentra nombres y códigos exactos, la segunda sinónimos |
| **Búsqueda léxica** | La que compara palabras, como TF-IDF. No encuentra sinónimos |
| **Búsqueda semántica** | La que compara sentidos, con un modelo de embeddings preentrenado |
| **Cita inventada** | Un número en `citas` que no es de ningún fragmento enviado. Tu código la detecta sin otro modelo |
| **Coseno** | El coseno del ángulo entre dos vectores: 1 si apuntan igual, 0 si no comparten nada |
| **Distancia de coseno** | 1 − coseno. Es el operador `<=>` de pgvector |
| ***ef_search*** | Cuántos candidatos guarda un índice HNSW mientras busca. Más candidatos, más acierto y más tiempo |
| **Embedding** | Una lista de números de longitud fija que representa un texto, de modo que textos parecidos quedan cerca |
| **Escaneo iterativo** (*iterative scan*) | Desde pgvector 0.8, seguir buscando en el índice hasta llenar el `LIMIT` cuando un `WHERE` descarta candidatos |
| **Extensión** (PostgreSQL) | Código que se carga en el servidor y añade tipos, operadores o índices. Se instala en cada base con `CREATE EXTENSION` |
| **Fidelidad** (*faithfulness*) | Que todo lo que afirma una respuesta esté en los fragmentos que recibió. Se mide con un LLM como juez |
| **Fragmento** (*chunk*) | Cada trozo en que se divide un documento para recuperarlo. Debe entenderse solo |
| **Generar** | El tercer paso de RAG: la respuesta del modelo con los fragmentos en el prompt |
| **HNSW** | *Hierarchical Navigable Small World*: un índice en forma de grafo en capas que busca saltando hacia la consulta |
| **IVFFlat** | Un índice de pgvector que agrupa los vectores con k-means y busca solo en los grupos cercanos |
| **LLM como juez** | Usar un modelo para evaluar respuestas de otro, con un prompt de juez y salida estructurada |
| **LSA** | *Latent Semantic Analysis*: una SVD truncada de la matriz TF-IDF, que resume las palabras en pocos números |
| **MRR** | *Mean Reciprocal Rank*: la media de 1 / puesto del primer resultado relevante |
| **Normalizar** | Dividir un vector por su longitud, para que mida 1. Así el coseno es un producto escalar |
| **pgvector** | La extensión de PostgreSQL que añade el tipo `vector`, las distancias y los índices HNSW e IVFFlat |
| **Precisión@k** | La parte de los `k` resultados que son relevantes: cuánto ruido llega |
| **Preguntas etiquetadas** | Un conjunto de preguntas con el fragmento que las responde, para medir una búsqueda |
| **RAG** | *Retrieval-Augmented Generation*: recuperar fragmentos, ponerlos en el prompt y generar la respuesta con ellos |
| **Recall@k** | La parte de los resultados relevantes que está entre los `k` primeros: si llega lo que hace falta |
| **Recuperar** (*retrieve*) | El primer paso de RAG: buscar los fragmentos más parecidos a la pregunta |
| **SVD truncada** | Una descomposición que se queda con las `n` direcciones más importantes de una matriz. Como PCA, pero sin centrar |
| **TF-IDF** | El recuento de cada palabra multiplicado por lo rara que es en el conjunto |
| **`vector(n)`** | El tipo de pgvector: `n` números de 4 bytes en una columna |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
