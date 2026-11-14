# Ejercicio 01 — Embeddings

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-embeddings.md)

## Objetivo

Convertir textos en vectores y compararlos, de lo más simple a un modelo preentrenado:

- contar palabras y medir el coseno entre dos notas;
- TF-IDF: las palabras raras pesan más;
- LSA: de muchas palabras a pocos números, y notas parecidas sin palabras en común;
- vectores de longitud 1: el coseno es un producto escalar;
- un modelo de embeddings preentrenado frente a TF-IDF;
- buscar notas con los dos y contar quién acierta.

Es un ejercicio **guiado**: descomentas cada paso de `main.py`, lo ejecutas y comparas la salida con la de este README. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-38-rag_embeddings_pgvector_en_postgresql_y_evaluacion/2-practicas/ejercicio-01-embeddings/starter
uv run python main.py
```

```
Ejercicio 01 · Embeddings
```

`NOTES` son nueve notas, tres de cada tipo, y `KINDS`, sus tipos. `QUERIES` son cuatro consultas que dicen lo mismo que alguna nota **con otras palabras**, cada una con el tipo que debería encontrar.

## Pasos

### 1. Contar palabras

Descomenta el **PASO 1** y ejecuta:

```
vocabulario: acumulado agua centro con de el en entrada estaba filtro la lavo limpio lleno oeste polvo quito se sucio sur
[[0 0 0 0 1 1 1 0 0 1 0 0 1 1 1 1 0 1 0 0]
 [1 0 1 0 0 1 2 1 0 0 1 0 0 0 0 1 1 1 0 0]
 [0 1 0 1 1 1 0 0 1 1 0 1 0 0 0 0 0 1 1 1]]
coseno nota 1 y nota 2: 0.48
coseno nota 1 y nota 3: 0.42
```

Las tres notas de limpieza, convertidas en **bolsas de palabras**: una columna por palabra del vocabulario y, en cada fila, cuántas veces sale cada palabra en esa nota. `strip_accents="unicode"` quita las tildes: «quitó» y «quito» son la misma palabra.

El coseno mide el ángulo entre dos vectores: 1 si apuntan igual y 0 si no comparten nada. La nota 1 se parece a la 2 por «polvo», «en», «se» y «el». Fíjate en que «en», «se» y «el» cuentan igual que «polvo».

### 2. TF-IDF, las palabras raras pesan más

Descomenta el **PASO 2** y ejecuta:

```
9 notas · 58 palabras distintas
nota 4: lleno 0.43 · limpio 0.43 · polvo 0.36 · oeste 0.36 · filtro 0.36 · en 0.31 · se 0.22 · el 0.22 · de 0.20
«se cortó la electricidad» comparte con las notas: la se
```

TF-IDF multiplica cada recuento por lo **rara** que es la palabra en el conjunto. «lleno» sale en una sola nota y pesa 0,43; «de» sale en casi todas y pesa 0,20. Ya lo usaste en la semana 36 para clasificar.

La consulta «se cortó la electricidad» solo comparte «la» y «se» con las notas. Para TF-IDF, «cortó» no tiene nada que ver con «corte», ni «electricidad» con «energía».

### 3. LSA, de muchas palabras a pocos números

Descomenta el **PASO 3** y ejecuta:

```
de 58 a 4 números por nota · conservan el 46% de la varianza
notas 4 y 5: TF-IDF 0.36 · LSA 0.81
notas 4 y 7: TF-IDF 0.15 · LSA 0.34
```

**LSA** (*Latent Semantic Analysis*) es una SVD de la matriz TF-IDF (`TruncatedSVD`): resume las 58 columnas en 4 números por nota. Es el `embedder` de tu proyecto, con 32 números en lugar de 4.

Las notas 4 y 5 («filtro lleno de polvo» y «polvo acumulado en la entrada») pasan de 0,36 a 0,81. LSA ha visto que «filtro», «polvo», «limpio» y «entrada» salen juntas en las notas de limpieza, y las acerca. Las notas 4 y 7 (limpieza y calibración) siguen lejos. Con solo 9 notas y 4 números se pierde más de la mitad de la varianza; en tu proyecto, 32 números conservan el 90 %.

### 4. Longitud 1, el coseno es un producto

Descomenta el **PASO 4** y ejecuta:

```
longitudes: [1. 1. 1.]
producto 0.342 · coseno 0.342
distancia de coseno 0.658 · euclídea² 1.316
```

`normalize` divide cada vector por su longitud. Con longitud 1, el coseno es el producto escalar (`a @ b`), que es más barato de calcular. La **distancia de coseno** es `1 - coseno`, y es lo que calcula el operador `<=>` de pgvector. La distancia euclídea al cuadrado es exactamente el doble: 2 − 2 × coseno. Por eso, con vectores de longitud 1, ordenar por distancia euclídea o por coseno da el mismo orden.

### 5. Un modelo preentrenado

Descomenta el **PASO 5** y ejecuta. Si hiciste el ejercicio 03 de la semana 36, el modelo ya está en tu caché; si no, la primera vez lo descarga (unos 470 MB):

```
vectores de 384 números
«se cortó la electricidad» y la nota 3: TF-IDF 0.27 · modelo 0.69
```

`paraphrase-multilingual-MiniLM-L12-v2` es un *encoder* (semana 36) entrenado con millones de pares de frases que dicen lo mismo. `embed` hace la media de los vectores de las piezas, como en la semana 36, y la normaliza. «se cortó la electricidad» y «La estación Este se apagó por un corte de energía» no comparten ninguna palabra con contenido, pero para el modelo están cerca (0,69). Para TF-IDF solo se parecen por «la» y «se».

Los mensajes de carga del modelo («Loading weights») salen por la salida de errores: no forman parte del resultado.

### 6. Buscar con los dos

Descomenta el **PASO 6** y ejecuta:

```
«el aparato no funciona»
   TF-IDF → El analizador de Sur no transmite datos desde ayer, hay que cambiar la pieza.
   modelo → El sensor de Norte dejó de enviar lecturas, queda fuera de servicio.
«se cortó la electricidad»
   TF-IDF → Se corrigió la deriva del cero en Norte.
   modelo → La estación Este se apagó por un corte de energía.
«había suciedad en la toma de aire»
   TF-IDF → En Centro se quitó el polvo acumulado en la entrada.
   modelo → En Centro se quitó el polvo acumulado en la entrada.
«se puso a punto el instrumento con una referencia»
   TF-IDF → El filtro de Sur estaba sucio y se lavó con agua.
   modelo → La calibración de Oeste dio un nuevo factor de escala.
TF-IDF acierta el tipo 2 de 4 · modelo acierta el tipo 4 de 4
```

Para cada consulta, la nota más parecida según cada método:

- **«el aparato no funciona»:** TF-IDF acierta, pero por «no», una palabra que no dice nada del tipo.
- **«se cortó la electricidad»:** TF-IDF elige una calibración por «se» y «la».
- **«se puso a punto el instrumento...»:** TF-IDF elige una limpieza.
- **El modelo** acierta las cuatro: compara significados, no palabras.

Es la diferencia entre la búsqueda **léxica** (las palabras) y la **semántica** (el sentido) de la teoría 01.

Entonces, ¿por qué tu proyecto usa TF-IDF y LSA?

- funciona sin descargar 470 MB ni ponerlos en la imagen Docker;
- es rápido en CPU, y no depende de nadie;
- con notas que repiten el vocabulario, como las tuyas, acierta tanto como `clasificar`.

Cuando las preguntas usen otras palabras que las notas, el modelo preentrenado gana.

Para terminar, añade al final de `QUERIES` dos consultas de **tu** dominio: una con las mismas palabras que una nota y otra con sinónimos. Mira cuál encuentra cada método.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `OSError: We couldn't connect to 'https://huggingface.co'` | Sin red no se descarga el modelo. Si ya está en la caché, ejecuta `HF_HUB_OFFLINE=1 uv run python main.py` |
| `ValueError: n_components(4) must be <= n_features` | Has quitado notas: LSA no puede sacar más números que palabras distintas haya |
| `NameError: name 'weights' is not defined` | Descomenta los pasos en orden: el 3 usa la matriz del 2 |
| La descarga se queda parada | Son 470 MB: la primera vez tarda. Puedes cambiar de carpeta de caché con `HF_HOME=...` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · RAG en tu Observatorio](../../1-teoria/05-rag-en-tu-observatorio.md) | **Ejercicio 01 · Embeddings** | [Ejercicio 02 · pgvector por dentro](../ejercicio-02-pgvector-por-dentro/README.md) |
