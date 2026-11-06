# Ejercicio 04 — itertools

⏱️ 1 h · Teoría previa: [05](../../1-teoria/05-itertools.md)

## Objetivo

Recorrer datos de formas nuevas sin escribir el bucle a mano: encadenar, cortar, mirar vecinos, acumular, juntar rachas y hacer lotes. `pairwise` y `groupby` son las piezas de `jumps` y de la refactorización de `longest_streak` del proyecto. Ejercicio **guiado**: descomentas cada paso de `itertools_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-06-algoritmos_big_o_collections_e_itertools/2-practicas/ejercicio-04-itertools/starter
uv run python itertools_lab.py
```

```
Ejercicio 04 · itertools
```

## Pasos

### 1. `chain` e `islice`

Descomenta el **PASO 1** y ejecuta:

```
Seguidas: [12.5, 8.0, 55.1, 61.0, 48.9]
Primeros 4 ids: [1, 2, 3, 4]
Los 2 siguientes: [5, 6]
```

`chain` recorre un iterable y después el otro, sin crear una lista con los dos. `count` no termina nunca: `list(count())` llenaría la memoria. `islice` le pide solo los que quieres. Y como `ids` es un iterador, la segunda llamada **sigue** donde se quedó la primera: es la misma idea que el generador que se agotaba en la semana 5.

### 2. `pairwise` y `accumulate`

Descomenta el **PASO 2**:

```
Parejas: [(10.0, 15.0), (15.0, 12.0), (12.0, 30.0), (30.0, 28.0)]
Saltos: [5.0, -3.0, 18.0, -2.0]
Acumulado: [10.0, 25.0, 37.0, 67.0, 95.0]
Máximo hasta aquí: [10.0, 15.0, 15.0, 30.0, 30.0]
```

`pairwise` da cada pareja de vecinos: con 5 valores, 4 parejas. La comprehension de los saltos es la función `jumps` del proyecto, entera. `accumulate` da el resultado de ir aplicando una operación: la suma si no le dices otra, el máximo con `max`.

### 3. `groupby`

Descomenta el **PASO 3**:

```
  alto: racha de 2
  bajo: racha de 1
  alto: racha de 3
  medio: racha de 1
Racha más larga en alto: 3
Sin ordenar: ['alto', 'bajo', 'alto', 'medio']
Ordenados:   ['alto', 'bajo', 'medio']
```

`groupby` junta elementos **seguidos** con la misma clave: `alto` sale dos veces porque hay un `bajo` en medio. Eso lo hace perfecto para rachas (la línea de `streak` es la nueva `longest_streak` del proyecto) y engañoso para agrupar: si quieres un grupo por clave, ordena antes o usa un diccionario. Cada `group` es un iterador que se agota, y además deja de servir cuando `groupby` avanza al siguiente: por eso se consume enseguida con `len(list(group))`.

### 4. `batched` y `combinations`

Descomenta el **PASO 4**:

```
  lote (12.5, 8.0, 55.1) media 25.2
  lote (61.0, 48.9, 9.5) media 39.8
  lote (30.1,) media 30.1
6 parejas: [('Norte', 'Sur'), ('Norte', 'Este'), ('Norte', 'Oeste'), ('Sur', 'Este'), ('Sur', 'Oeste'), ('Este', 'Oeste')]
```

`batched` corta en lotes de `n`, como tuplas; el último puede ser más corto. Sirve para enviar datos de 100 en 100 a una API o a PostgreSQL. `combinations(stations, 2)` da cada pareja una sola vez: con 4 estaciones, 4 × 3 / 2 = 6. Es el O(n²) del ejercicio 01: con 1 000 estaciones serían casi medio millón de parejas.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ImportError: cannot import name 'batched'` | Tu Python es anterior a 3.12: comprueba `uv run python --version` y el `.python-version` |
| `ValueError: n must be at least one` | Llamaste a `batched` con `0` |
| `groupby` repite una clave | Es normal: junta solo los seguidos; ordena antes si quieres un grupo por clave |
| `len(list(group))` da 0 | Guardaste los `group` y los leíste después de avanzar: consúmelos dentro del mismo `for` |
| El programa no termina | Hiciste `list(count())`: `count` es infinito; córtalo con `islice` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · collections](../ejercicio-03-collections/README.md) | **Ejercicio 04 · itertools** | [Proyecto · Observatorio, capa 5](../../3-proyecto/README.md) |
