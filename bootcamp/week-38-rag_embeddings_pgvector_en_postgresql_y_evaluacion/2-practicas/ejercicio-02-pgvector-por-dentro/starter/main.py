"""Ejercicio 02 · pgvector: vectores en PostgreSQL, distancias e índices.

Antes de ejecutar, arranca el PostgreSQL de las prácticas: `docker compose up -d --wait`.
Cada ejecución borra y vuelve a crear sus tablas: puedes repetir sin miedo.
"""

import time

import numpy as np
import psycopg
from pgvector.psycopg import register_vector

# Usuario, contraseña, máquina, puerto y base: los de compose.yaml.
DSN = "postgresql://practicas:practicas@127.0.0.1:5433/practicas"

print("Ejercicio 02 · pgvector")

# autocommit: cada orden se confirma sola; en este ejercicio no hacen falta transacciones.
conn = psycopg.connect(DSN, autocommit=True)
conn.execute("DROP TABLE IF EXISTS notes, items")
conn.execute("DROP EXTENSION IF EXISTS vector")

# ============================================
# PASO 1: La extensión vector
# ============================================
# Descomenta las siguientes líneas:
# conn.execute("CREATE EXTENSION vector")
# row = conn.execute(
#     "SELECT extversion FROM pg_extension WHERE extname = 'vector'"
# ).fetchone()
# assert row is not None
# print("pgvector", row[0])
# Desde aquí, psycopg convierte un array de NumPy en un `vector` y un `vector` en un array.
# register_vector(conn)
# row = conn.execute(
#     "SELECT '[1, 2, 3]'::vector, vector_dims('[1, 2, 3]'::vector)"
# ).fetchone()
# assert row is not None
# print("vuelve como", type(row[0]).__name__, row[0], "· dimensiones:", row[1])

# ============================================
# PASO 2: Tres distancias
# ============================================
# Descomenta las siguientes líneas:
# a = np.array([1.0, 0.0])
# b = np.array([2.0, 2.0])
# row = conn.execute(
#     "SELECT %s <-> %s, %s <=> %s, %s <#> %s", (a, b, a, b, a, b)
# ).fetchone()
# assert row is not None
# print(
#     f"euclídea (<->) {row[0]:.3f} · coseno (<=>) {row[1]:.3f} · producto (<#>) {row[2]:.3f}"
# )
# print(
#     f"con NumPy: {np.linalg.norm(a - b):.3f} · {1 - a @ b / np.linalg.norm(a) / np.linalg.norm(b):.3f}"
# )
# try:
#     conn.execute("SELECT '[1, 2, 3]'::vector <-> '[1, 2]'::vector")
# except psycopg.errors.DataException as problem:
#     print("error:", problem)

# ============================================
# PASO 3: Una tabla con vectores
# ============================================
# Descomenta las siguientes líneas:
# conn.execute(
#     "CREATE TABLE notes (id bigserial PRIMARY KEY, text text, embedding vector(3))"
# )
# NOTES = {
#     "filtro lleno de polvo": [0.9, 0.1, 0.0],
#     "filtro sucio cambiado": [0.8, 0.3, 0.1],
#     "sensor quemado": [0.1, 0.9, 0.2],
#     "deriva corregida en el cero": [0.1, 0.2, 0.9],
# }
# with conn.cursor() as cur:
#     cur.executemany(
#         "INSERT INTO notes (text, embedding) VALUES (%s, %s)",
#         [(text, np.array(vector)) for text, vector in NOTES.items()],
#     )
# query = np.array([1.0, 0.2, 0.0])
# rows = conn.execute(
#     "SELECT text, embedding <=> %s AS distance FROM notes ORDER BY distance LIMIT 3",
#     (query,),
# )
# for text, distance in rows:
#     print(f"  {distance:.3f} · {text}")
# try:
#     conn.execute("INSERT INTO notes (text, embedding) VALUES ('otra', '[1, 0]')")
# except psycopg.errors.DataException as problem:
#     print("error:", problem)

# ============================================
# PASO 4: Veinte mil vectores, búsqueda exacta
# ============================================
# Descomenta las siguientes líneas:
# N, DIMENSION, K = 20_000, 64, 10
# rng = np.random.default_rng(38)
# Como los embeddings de verdad: grupos de vectores parecidos (textos que hablan de lo mismo),
# alrededor de 100 centros, y no puntos repartidos al azar por todo el espacio.
# centers = rng.normal(size=(100, DIMENSION))
# data = (
#     centers[rng.integers(100, size=N)] + 1.5 * rng.normal(size=(N, DIMENSION))
# ).astype(np.float32)
# conn.execute(
#     f"CREATE TABLE items (id bigint PRIMARY KEY, embedding vector({DIMENSION}))"
# )
# start = time.perf_counter()
# COPY en binario: la forma más rápida de meter muchas filas (semana 19).
# with conn.cursor().copy(
#     "COPY items (id, embedding) FROM STDIN WITH (FORMAT BINARY)"
# ) as copy:
#     copy.set_types(["int8", "vector"])
#     for number, vector in enumerate(data):
#         copy.write_row([number, vector])
# print(
#     f"{N} vectores de {DIMENSION} números, copiados en {time.perf_counter() - start:.1f} s"
# )
# conn.execute("ANALYZE items")

# QUERY = "SELECT id FROM items ORDER BY embedding <=> %s LIMIT %s"
# queries = (
#     centers[rng.integers(100, size=50)] + 1.5 * rng.normal(size=(50, DIMENSION))
# ).astype(np.float32)


# def plan(vector: np.ndarray) -> str:
#     """Los pasos del plan de PostgreSQL para la búsqueda: cómo la va a hacer."""
#     literal = str(vector.tolist())
#     text = f"EXPLAIN (COSTS OFF) SELECT id FROM items ORDER BY embedding <=> '{literal}' LIMIT {K}"
#     lines = [str(row[0]) for row in conn.execute(text)]
#     return " → ".join(
#         line.strip().removeprefix("->").strip()
#         for line in lines
#         if "Key" not in line and "Order By" not in line
#     )


# def search(limit: int = K) -> tuple[list[set[int]], float]:
#     """Las `limit` más cercanas a cada consulta, y los milisegundos por consulta."""
#     start = time.perf_counter()
#     found = [
#         {row[0] for row in conn.execute(QUERY, (vector, limit))} for vector in queries
#     ]
#     return found, (time.perf_counter() - start) * 1000 / len(queries)


# exact, milliseconds = search()
# print("plan:", plan(queries[0]))
# print(f"exacta: {milliseconds:.1f} ms por consulta")

# ============================================
# PASO 5: Un índice HNSW, búsqueda aproximada
# ============================================
# Descomenta las siguientes líneas:
# start = time.perf_counter()
# conn.execute(
#     "CREATE INDEX items_hnsw ON items USING hnsw (embedding vector_cosine_ops)"
# )
# print(f"índice HNSW creado en {time.perf_counter() - start:.1f} s")
# print("plan:", plan(queries[0]))


# def recall(found: list[set[int]]) -> float:
#     """La parte de las K exactas que encuentra la búsqueda aproximada (recall@K)."""
#     return float(
#         np.mean([len(one & right) / K for one, right in zip(found, exact, strict=True)])
#     )


# approximate, milliseconds = search()
# print(
#     f"aproximada: {milliseconds:.1f} ms por consulta · recall@{K} {recall(approximate):.2f}"
# )

# ============================================
# PASO 6: ef_search, y filtrar con un índice
# ============================================
# Descomenta las siguientes líneas:
# for ef in [10, 40, 200]:
#     conn.execute(f"SET hnsw.ef_search = {ef}")
#     found, milliseconds = search()
#     print(
#         f"ef_search {ef:>3}: {milliseconds:.1f} ms por consulta · recall@{K} {recall(found):.2f}"
#     )
# conn.execute("RESET hnsw.ef_search")

# FILTERED = "SELECT id FROM items WHERE id %% 10 = 0 ORDER BY embedding <=> %s LIMIT 10"
# rows = conn.execute(FILTERED, (queries[0],)).fetchall()
# print(f"con WHERE, el índice da {len(rows)} filas de 10")
# conn.execute("SET hnsw.iterative_scan = relaxed_order")
# rows = conn.execute(FILTERED, (queries[0],)).fetchall()
# print(f"con hnsw.iterative_scan, {len(rows)} de 10")

# conn.close()
