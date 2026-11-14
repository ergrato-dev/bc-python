# Ejercicio 02 — pgvector por dentro

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-pgvector.md)

## Objetivo

Guardar vectores en PostgreSQL y buscar los más cercanos, con SQL:

- instalar la extensión `vector` y ver qué tipo devuelve a Python;
- las tres distancias de pgvector, comparadas con NumPy;
- una tabla con una columna `vector(3)` y una búsqueda con `ORDER BY ... LIMIT`;
- veinte mil vectores y una búsqueda exacta: qué hace PostgreSQL;
- un índice HNSW: búsqueda aproximada, más rápida, y cuánto acierta;
- `ef_search`, y lo que pasa al filtrar con un índice.

Es un ejercicio **guiado**: descomentas cada paso de `main.py`, lo ejecutas y comparas la salida con la de este README. No se entrega.

## Antes de empezar

El ejercicio usa su propio PostgreSQL con pgvector, en el puerto 5433, para no tocar el de tu proyecto:

```bash
cd bootcamp/week-38-rag_embeddings_pgvector_en_postgresql_y_evaluacion/2-practicas/ejercicio-02-pgvector-por-dentro/starter
docker compose up -d --wait
uv run python main.py
```

```
Ejercicio 02 · pgvector
```

Cada ejecución borra sus tablas y la extensión, y las vuelve a crear: puedes repetir sin miedo. Al terminar el ejercicio, `docker compose down -v` borra el contenedor y sus datos.

Los tiempos y algunos números de los pasos 4 a 6 cambian un poco en cada ejecución y en cada máquina: compara el orden de magnitud, no la cifra exacta.

## Pasos

### 1. La extensión `vector`

Descomenta el **PASO 1** y ejecuta:

```
pgvector 0.8.7
vuelve como Vector Vector([1.0, 2.0, 3.0]) · dimensiones: 3
```

`CREATE EXTENSION vector` instala pgvector **en esta base**: el tipo `vector`, sus operadores y sus índices. La imagen de Docker trae la extensión, pero cada base la instala una vez (en tu proyecto, la migración `0002`).

`register_vector(conn)` le enseña a psycopg el tipo nuevo. Desde ese momento, un array de NumPy que pasas como parámetro llega como `vector`, y un `vector` vuelve como un objeto `Vector` de pgvector (`.to_numpy()` lo convierte en array). `vector_dims` dice cuántos números tiene.

### 2. Tres distancias

Descomenta el **PASO 2** y ejecuta:

```
euclídea (<->) 2.236 · coseno (<=>) 0.293 · producto (<#>) -2.000
con NumPy: 2.236 · 0.293
error: different vector dimensions 3 and 2
```

| Operador | Distancia | Cuándo |
|---|---|---|
| `<->` | Euclídea (L2) | Cuando la longitud del vector importa |
| `<=>` | Coseno: 1 − coseno | Textos: solo importa la dirección. Es la de tu proyecto |
| `<#>` | Producto escalar, **con el signo cambiado** | Vectores de longitud 1: da el mismo orden que el coseno y es más barato |

`<#>` devuelve −2 y no 2 porque PostgreSQL ordena de menor a mayor, y el producto más grande debe salir primero. Comparar dos vectores con distinto número de números es un error, no un cero.

### 3. Una tabla con vectores

Descomenta el **PASO 3** y ejecuta:

```
  0.004 · filtro lleno de polvo
  0.020 · filtro sucio cambiado
  0.704 · sensor quemado
error: expected 3 dimensions, not 2
```

Una columna `vector(3)` solo admite vectores de 3 números, como `varchar(100)` solo admite 100 caracteres. La búsqueda es SQL normal: `ORDER BY embedding <=> %s LIMIT 3` ordena todas las filas por distancia a la consulta y se queda con las 3 primeras. Es lo que hace `rag.search` en tu proyecto, escrito con SQLAlchemy.

### 4. Veinte mil vectores, búsqueda exacta

Descomenta el **PASO 4** y ejecuta:

```
20000 vectores de 64 números, copiados en 0.1 s
plan: Limit → Sort → Seq Scan on items
exacta: 5.1 ms por consulta
```

`COPY` en binario mete 20 000 filas en una décima de segundo (semana 19). Los datos imitan embeddings de verdad: grupos de vectores parecidos alrededor de 100 centros.

`EXPLAIN` enseña el plan. **Seq Scan** significa que PostgreSQL lee las 20 000 filas, calcula la distancia de cada una y las ordena (**Sort**) para quedarse con 10. Es una búsqueda **exacta**: siempre da las 10 más cercanas de verdad, y tarda en proporción al número de filas. Con 20 000 filas son milisegundos; con 20 millones serían segundos.

### 5. Un índice HNSW, búsqueda aproximada

Descomenta el **PASO 5** y ejecuta:

```
índice HNSW creado en 4.9 s
plan: Limit → Index Scan using items_hnsw on items
aproximada: 1.2 ms por consulta · recall@10 0.92
```

**HNSW** (*Hierarchical Navigable Small World*) es un grafo en el que cada vector está unido a sus vecinos más cercanos, en varias capas. Para buscar, se salta por el grafo hacia la consulta en lugar de mirar todas las filas. `vector_cosine_ops` dice que el índice es para `<=>`: un índice de coseno no sirve para `<->`.

Es más rápido, pero **aproximado**: de las 10 más cercanas de verdad (las del paso 4), encuentra unas 9 (`recall@10` cerca de 0,92). Crearlo tarda segundos, y hacerlo antes de cargar los datos haría la carga más lenta. Por eso tu proyecto, con 240 notas, no lo usa: allí la búsqueda exacta tarda menos de un milisegundo y no se equivoca nunca.

### 6. `ef_search`, y filtrar con un índice

Descomenta el **PASO 6** y ejecuta:

```
ef_search  10: 0.7 ms por consulta · recall@10 0.75
ef_search  40: 1.3 ms por consulta · recall@10 0.92
ef_search 200: 2.2 ms por consulta · recall@10 0.99
con WHERE, el índice da 8 filas de 10
con hnsw.iterative_scan, 10 de 10
```

`hnsw.ef_search` es cuántos candidatos guarda el índice mientras recorre el grafo (40 por defecto). Con más candidatos acierta más y tarda más; con menos, al revés. Es el mando que equilibra calidad y velocidad, y se cambia por sesión con `SET`.

La segunda parte enseña un fallo que sorprende: con `WHERE id % 10 = 0`, el índice encuentra 40 candidatos y **después** filtra. Solo uno de cada diez pasa el filtro, así que devuelve menos de 10 filas aunque haya miles que cumplen. Desde pgvector 0.8, `hnsw.iterative_scan` sigue buscando hasta llenar el `LIMIT`. Si filtras por una columna (la estación, el tipo), piénsalo antes de crear un índice.

Para terminar, cambia `N` a 100 000 y vuelve a ejecutar. ¿Cuánto crece el tiempo de la búsqueda exacta? ¿Y el de la aproximada? ¿Y el de crear el índice?

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `connection refused` en el puerto 5433 | Arranca el contenedor: `docker compose up -d --wait` |
| `extension "vector" is not available` | El contenedor es de otra imagen: `docker compose down -v` y vuelve a arrancarlo con el `compose.yaml` del ejercicio |
| `cannot adapt type 'ndarray' using placeholder '%s'` | Falta `register_vector(conn)` del paso 1 |
| `operator does not exist: vector <=> double precision[]` | Pasaste una lista de Python: psycopg la envía como un array de números. Pasa un array de NumPy, con `register_vector` |
| `ProgrammingError: incomplete placeholder: '%'` | En una consulta con parámetros, el `%` del módulo se escribe `%%` |
| El paso 5 tarda mucho | Crear un índice HNSW es lo más caro del ejercicio: con más `N`, más tiempo |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Embeddings](../ejercicio-01-embeddings/README.md) | **Ejercicio 02 · pgvector por dentro** | [Ejercicio 03 · RAG paso a paso](../ejercicio-03-rag-paso-a-paso/README.md) |
