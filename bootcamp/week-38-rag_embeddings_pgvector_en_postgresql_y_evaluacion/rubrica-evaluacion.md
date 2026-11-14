# Rúbrica de Evaluación — Semana 38: RAG, embeddings, pgvector en PostgreSQL y evaluación

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 37 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | ¿Qué es un embedding? ¿Por qué se compara con la distancia de coseno y no con la euclídea, y por qué con vectores de longitud 1 da igual? | 10 |
| 2 | ¿Qué hacen TF-IDF y LSA? ¿Por qué LSA acerca dos notas que no comparten palabras exactas? ¿Por qué falla «se cortó la electricidad» frente a «corte de energía», y qué lo arreglaría? | 10 |
| 3 | Tu modelo de LSA se ajusta con tus notas. ¿Por qué la pregunta necesita el mismo modelo? ¿Por qué `model_of` puede rehacerlo en lugar de guardarlo, y cuándo dejaría de valer? | 10 |
| 4 | ¿Por qué `uv add pgvector` no basta para usar `vector(32)`? ¿Qué hacen la imagen `pgvector/pgvector`, `CREATE EXTENSION` y el paquete de Python, y por qué se borró el volumen al cambiar de imagen? | 10 |
| 5 | Explica la búsqueda exacta y la de un índice HNSW: qué hace cada una, qué garantiza y cuánto tarda. ¿Qué es `ef_search`, y por qué un `WHERE` puede devolver menos filas con el índice? ¿Por qué tu proyecto no crea índice? | 10 |
| 6 | Describe los tres pasos de RAG con tu proyecto. ¿Qué hace que un fragmento sirva? ¿Qué cambia al subir o bajar `k`? | 10 |
| 7 | ¿Qué es una cita inventada y cómo la detecta tu código sin otro modelo? ¿Qué no garantiza que todas las citas sean válidas? | 10 |
| 8 | «¿Qué averías hubo en Norte?» responde dos, y la base tiene 17. Explica por qué, y qué harías con esa pregunta. Nombra otras dos cosas que RAG no hace. | 10 |
| 9 | Define precisión@k, recall@k y MRR. ¿Por qué en RAG importa sobre todo recall@k? ¿Por qué `indexar` no indexa las notas de prueba? | 10 |
| 10 | ¿Qué mide un LLM como juez que no mida una regla? ¿Cómo sabes si puedes fiarte de él, y cuánto cuesta? Con 571 tokens de entrada y 70 de salida por pregunta (2 $ y 10 $ por millón), ¿cuánto cuestan mil preguntas al día durante 30 días, sin juez y con un juez que lee lo mismo? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. Una lista de números de longitud fija que representa un texto, de modo que textos parecidos tienen vectores cercanos. Una nota corta y otra larga del mismo tema apuntan igual pero tienen tamaños distintos: el coseno mide el ángulo y no se fija en el tamaño. Con longitud 1, la euclídea al cuadrado es 2 − 2 × coseno: ordenar por una o por otra da el mismo orden, y el coseno es un producto escalar.
2. TF-IDF da un número por palabra, que pesa más cuanto más rara es la palabra en el conjunto. LSA es una SVD truncada de esa matriz: resume las columnas en 32 números que mezclan palabras que salen juntas en las notas, así que dos notas con palabras distintas del mismo grupo («filtro», «polvo», «limpio») se acercan. Las dos son léxicas: «cortó» no es «corte» ni «electricidad» es «energía», y solo comparten «la» y «se». Un modelo de embeddings preentrenado, que compara sentidos (0,69 frente a 0,27 en el ejercicio 01).
3. Cada uno de los 32 números significa algo distinto en cada ajuste: un vector de un modelo no se compara con uno de otro. Con la misma semilla y los mismos textos, el ajuste da los mismos vectores, sin depender del orden de las filas, y con cientos de notas tarda milisegundos: rehacerlo evita guardar un archivo atado a una versión de scikit-learn. Dejaría de valer con muchas notas (tardaría) o si cambiaran las notas sin reindexar (los vectores guardados serían de otro modelo).
4. El paquete de Python solo enseña el tipo a SQLAlchemy y a psycopg; la extensión es código C del servidor, y la imagen oficial no la trae. `pgvector/pgvector` es PostgreSQL con la extensión disponible; `CREATE EXTENSION`, en la migración, la instala en la base; el paquete convierte entre `vector` y arrays de NumPy. La imagen nueva es Debian y la anterior Alpine: ordenan el texto con bibliotecas distintas, y los índices de texto podrían quedar mal; con datos que se regeneran, borrar el volumen es lo más simple.
5. La exacta calcula la distancia a todas las filas, las ordena y se queda con `k`: siempre acierta y tarda en proporción a las filas (unos 5 ms con 20 000). HNSW salta por un grafo en capas hacia la consulta mirando pocos candidatos: más rápido (1 ms), pero aproximado (recall@10 de 0,92). `ef_search` es cuántos candidatos guarda: más, mejor y más lento. El `WHERE` se aplica después de sacar los candidatos: si pocos cumplen, quedan menos de `k`; `hnsw.iterative_scan` sigue buscando. Con 240 notas, la exacta tarda menos de un milisegundo y no se equivoca: un índice no gana nada.
6. Recuperar: la pregunta pasa a vector con el mismo modelo y pgvector trae las `k` notas más cercanas. Aumentar: las notas van al mensaje entre `<nota id=...>` con su número, y el sistema dice que use solo esas, que cite y que diga cuándo no responden. Generar: Claude responde con salida estructurada, `respuesta` y `citas`. Un fragmento sirve si se entiende solo (con el título de su sección) y trata una sola cosa. Con `k` pequeño, el prompt es barato pero la respuesta puede quedar incompleta; con `k` grande, más cobertura, más tokens y más ruido.
7. Un número en `citas` que no es de ninguna nota enviada: Claude no pudo leerla. El código conoce los números que envió y compara (`Reply.invented`). Que las citas sean válidas no dice que la respuesta diga lo que dicen las notas: puede citar la nota buena y añadir algo que no está. Para eso hace falta comprobar la fidelidad.
8. La búsqueda trae 5 notas, y se fijó en «Norte»: tres limpiezas y dos averías. Claude solo ve esas 5 y nombra las dos averías que recibe. Contar necesita todas las filas: es una consulta de SQL (`WHERE kind = 'averia' AND label = 'Norte'`), o una herramienta que la haga (semana 37). RAG tampoco arregla una búsqueda que no trae el fragmento bueno, ni sabe cuál de dos notas que se contradicen es la reciente.
9. Precisión@k: parte de los `k` resultados que son relevantes. Recall@k: parte de los relevantes que están entre los `k`. MRR: media de 1 / puesto del primer relevante. Si el fragmento bueno no está entre los `k`, Claude no lo ve y la respuesta no puede ser buena: recall@k pone el techo. Si las notas de prueba estuvieran indexadas, cada una se encontraría a sí misma a distancia 0, y el voto acertaría siempre: una fuga de datos.
10. La fidelidad: que todo lo que afirma la respuesta esté en los fragmentos. Una regla comprueba citas y datos, pero no si la respuesta añade algo (la malla que se cambia una vez al año del ejercicio 04). El juez también se equivoca: se comparan sus veredictos con los tuyos en una muestra antes de usarlo. Una pregunta: 571 × 2 / 1 000 000 + 70 × 10 / 1 000 000 = 0,001142 + 0,0007 = 0,001842 $. Mil al día, 30 días: 30 000 × 0,001842 = 55,26 $. Con un juez que lee lo mismo, aproximadamente el doble, unos 110 $.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños y rojo a verde | Un commit por paso, sin cambiar los tests del bootcamp, cada uno con los ganchos; puede decir qué tests pasaron a verde con cada paso | 8 |
| Ejecución en vivo | Ante el instructor: `indexar` con sus notas, `buscar` con una frase de su dominio y con otra sin palabras conocidas (el error), `preguntar` con una grabación y sin clave (el error), y `pytest` en verde | 8 |
| Rompe y explica | Cambia `TRUNCATE notes RESTART IDENTITY` por `DELETE FROM notes` y explica qué test falla y qué pasaría con una grabación; cambia `rag.index(session, notes.iloc[rest])` por `rag.index(session, notes)` y explica por qué el acierto sería mentira | 8 |
| Explica su búsqueda | Enseña una búsqueda que acierta y otra que falla con sus notas, y explica la segunda con TF-IDF y LSA; dice qué cambiaría para arreglarla y cómo lo mediría | 8 |
| RAG o SQL | Con tres preguntas de su dominio, dice cuáles van a `preguntar` y cuáles a una consulta SQL, y escribe la consulta de una | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 37

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| El módulo | `Note` en `rag.py` con `Vector(32)`; `embedder` con TF-IDF, LSA y `Normalizer`, y sus dos errores; `index` con `TRUNCATE ... RESTART IDENTITY`; `model_of` que rehace el modelo; `search` con `cosine_distance`, desempate por número y `[]` sin palabras conocidas; `vote` y `Evaluation`; `ask` con `transform_schema`, `effort` y `stop_reason` antes de validar; `Reply` con citas inventadas y coste; sin reexportar en `core/__init__.py` | 25 |
| La base | Migración `0002` con `CREATE EXTENSION` y el import de pgvector, y `downgrade` que los deshace; `env.py` importa `rag`; la imagen con pgvector en `compose.yaml` y en la CI | 10 |
| Los comandos | `claude()` sacado de `leer-notas` sin cambiar sus tests; `indexar`, `buscar` y `preguntar` con los imports dentro y sus opciones; `indexar` mide con las notas de prueba sin indexarlas; `preguntar` no llama a Claude sin notas parecidas y avisa de las citas inventadas; cada error con su código | 15 |
| Tests propios | Al menos 6 tests en `tests/test_my_rag.py` con notas de su dominio, sin red, cada uno visto fallar con un mutante | 20 |
| Calidad | `pre-commit run --all-files`, `coverage report` y `alembic check` sin avisos; `docker compose run --rm app` y la CI en verde sin ninguna clave; `pgvector==0.5.1`, imágenes `week-38` y versión `0.38.0` | 10 |
| Git y README | Rama `week-38` en `python-<nombre>-<apellido>`; README con la sección "Búsqueda y preguntas", e `informe/README.md` con el resultado en "Siguientes pasos"; ninguna clave en el historial | 5 |
| Pull request | Salidas, CI, `indexar` con sus notas y una de `preguntar`, con su lectura, y la tabla de mutantes con las dos respuestas | 15 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | Semana 39 (próximamente) |
