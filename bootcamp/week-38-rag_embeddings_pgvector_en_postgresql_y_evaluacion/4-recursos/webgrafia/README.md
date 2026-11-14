# Webgrafía — Semana 38

Casi todo en inglés. La documentación sigue la última versión de cada proyecto; si algo no coincide con `pgvector` 0.5.1, la extensión 0.8.7 o scikit-learn 1.9.1, manda lo que ves al ejecutar.

| Recurso | Para qué |
|---|---|
| [pgvector](https://github.com/pgvector/pgvector) | El README de la extensión: el tipo, los operadores, HNSW, IVFFlat, `ef_search`, el escaneo iterativo y el rendimiento. Las teorías 02 y 05 |
| [pgvector-python](https://github.com/pgvector/pgvector-python) | El paquete de Python: `register_vector` para psycopg y `Vector` para SQLAlchemy, con ejemplos. La teoría 02, sección 3 |
| [pgvector/pgvector en Docker Hub](https://hub.docker.com/r/pgvector/pgvector) | Las etiquetas de la imagen, por versión de pgvector y de PostgreSQL. La teoría 02, sección 1 |
| [PostgreSQL: CREATE EXTENSION](https://www.postgresql.org/docs/current/sql-createextension.html) | Qué hace instalar una extensión y qué permisos pide. La teoría 02, sección 2 |
| [scikit-learn: TF-IDF](https://scikit-learn.org/stable/modules/feature_extraction.html) | `TfidfVectorizer`, sus opciones y la fórmula. La teoría 01, sección 3 |
| [scikit-learn: descomposición, LSA](https://scikit-learn.org/stable/modules/decomposition.html) | `TruncatedSVD` y por qué sirve para matrices dispersas de texto. La teoría 01, sección 4 |
| [Claude Docs: Embeddings](https://docs.claude.com/en/docs/build-with-claude/embeddings) | Cómo elegir un modelo de embeddings para usarlo con Claude, y por qué Anthropic recomienda un proveedor externo. La teoría 01, sección 5 |
| [Sentence Transformers](https://www.sbert.net/) | La biblioteca de referencia para embeddings de frases, con modelos multilingües. El siguiente paso tras el ejercicio 01 |
| [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) | Una comparación de modelos de embeddings por tarea e idioma. Para elegir uno midiendo, no por fama |
| [Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) (Anthropic) | Fragmentos con contexto, búsqueda híbrida y reordenación, con sus números. Ampliación de las teorías 03 y 04 |
| [Cookbook: RAG con Claude](https://github.com/anthropics/claude-cookbooks/tree/main/capabilities/retrieval_augmented_generation) (Anthropic) | Un RAG completo en un cuaderno, evaluado por partes. Las teorías 03 y 04 |
| [Crear tests para un prompt](https://docs.claude.com/en/docs/test-and-evaluate/develop-tests) | Casos etiquetados y un LLM como juez. La teoría 04, sección 5 |
| [Ragas](https://docs.ragas.io/en/stable/) | Una biblioteca de métricas de RAG: fidelidad, relevancia y recuperación. Para ver qué prompts de juez empaqueta. La teoría 04, sección 5 |
| [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) (Lewis y otros, 2020) | El artículo que dio nombre a RAG. Lectura opcional |
| [Efficient and robust approximate nearest neighbor search using HNSW graphs](https://arxiv.org/abs/1603.09320) (Malkov y Yashunin) | El artículo de HNSW, con el grafo en capas. Lectura opcional de la teoría 02, sección 5 |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Proyecto](../../3-proyecto/README.md) | **Webgrafía** | [Ebooks gratuitos](../ebooks-free/README.md) |
