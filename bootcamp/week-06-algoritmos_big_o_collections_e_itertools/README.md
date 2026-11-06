# Semana 06 — Algoritmos y Big-O con `collections` e `itertools`

> Dos programas correctos pueden tardar un segundo o tres horas con los mismos datos. Esta semana aprendes a ver la diferencia antes de ejecutar: cuentas cuánto trabajo hace un algoritmo cuando crecen los datos (Big-O), buscas y ordenas sabiendo lo que cuesta, y usas las herramientas de `collections` e `itertools` que resuelven en una línea los patrones de la semana 5. El Observatorio gana tendencias: mediana, media móvil y el salto más brusco, cada una en una sola pasada.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Estimar** el orden (Big-O) de un trozo de código y **reconocer** O(1), O(log n), O(n), O(n log n) y O(n²)
- **Medir** tiempos con `perf_counter` y `timeit` y **comparar** tamaños en lugar de números sueltos
- **Explicar** la búsqueda binaria y **usar** `bisect` para contar y clasificar en una lista ordenada
- **Ordenar** sin cambiar los datos de quien llama, **aprovechar** la estabilidad y **calcular** la mediana
- **Contar**, **agrupar** y **mantener ventanas** con `Counter`, `defaultdict` y `deque`
- **Recorrer** con `pairwise`, `groupby`, `accumulate`, `islice` y `batched`, y **refactorizar** bucles con ellas sin romper los tests

---

## 📋 Prerrequisitos

- [Semana 05](../week-05-colecciones_y_comprehensions/README.md): listas, tuplas, diccionarios, conjuntos y comprehensions.
- El *pull request* `week-05` de tu proyecto fusionado en `main`.

---

## 🗂️ Estructura de la Semana

```
week-06-algoritmos_big_o_collections_e_itertools/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 5 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · Algoritmos y Big-O](1-teoria/01-algoritmos-y-big-o.md) | Contar pasos, los cinco órdenes, coste de las operaciones de Python, medir con `perf_counter` y `timeit` | 1 h |
| [02 · Buscar](1-teoria/02-buscar.md) | Búsqueda lineal y binaria, `bisect`, clasificar por tramos, cuándo ordenar y cuándo un set | 45 min |
| [03 · Ordenar](1-teoria/03-ordenar.md) | Por qué O(n log n), `sorted` frente a `sort`, estabilidad, la mediana, `heapq` | 40 min |
| [04 · collections](1-teoria/04-collections.md) | `Counter`, `defaultdict` y su trampa, `deque` y la media móvil en O(n), `namedtuple` | 45 min |
| [05 · itertools](1-teoria/05-itertools.md) | Iteradores, `pairwise`, `accumulate`, `groupby` para rachas, `islice`, `batched`, `max` con `key` y `default` | 50 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, lo ejecutas y comparas con la salida esperada. Preparan el proyecto.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · Contar pasos y medir](2-practicas/ejercicio-01-contar-pasos-y-medir/README.md) | Contar comparaciones, `perf_counter`, `timeit` con lista y set, el mismo problema en O(n²) y en O(n) | 1 h 30 min |
| [02 · Buscar y ordenar](2-practicas/ejercicio-02-buscar-y-ordenar/README.md) | Búsqueda lineal, binaria a mano, `bisect`, ordenación estable, `heapq.nlargest` | 1 h 30 min |
| [03 · collections](2-practicas/ejercicio-03-collections/README.md) | `Counter`, `defaultdict`, `deque` frente a `pop(0)`, ventana con `maxlen`, `namedtuple` | 1 h 30 min |
| [04 · itertools](2-practicas/ejercicio-04-itertools/README.md) | `chain`, `islice`, `pairwise`, `accumulate`, `groupby`, `batched`, `combinations` | 1 h |

### Proyecto

El Observatorio lee los valores en el orden en que llegaron y calcula las etiquetas más frecuentes, la mediana, la media móvil y el mayor salto, todo en O(n) salvo la mediana. Además refactorizas `values_by_label` con `defaultdict` y `longest_streak` con `groupby`. **Es el único entregable de la semana.**
→ [3-proyecto/README.md](3-proyecto/README.md)

---

## ⏱️ Distribución del Tiempo (18 horas)

| Actividad | Tiempo |
| --------- | ------ |
| Teoría (5 archivos) | 4 h |
| Ejercicio 01 | 1 h 30 min |
| Ejercicio 02 | 1 h 30 min |
| Ejercicio 03 | 1 h 30 min |
| Ejercicio 04 | 1 h |
| Proyecto | 6 h 30 min |
| Recursos y glosario | 1 h |
| Autoevaluación (cuestionario de la rúbrica) | 1 h |
| **Total** | **18 h** |

---

## 🎩 Trucos y atajos

| Truco | Cómo |
|---|---|
| Medir una línea sin escribir un archivo | `uv run python -m timeit -s "data = list(range(100_000))" "99_999 in data"` |
| Ver qué tests tardan más | `uv run pytest --durations=5` |
| Saber si un `in` es O(n) | Mira sobre qué colección se hace: lista o tupla, O(n); set o diccionario, O(1) |
| Contar en una línea | `Counter(iterable).most_common(n)` |
| Ver lo que da un iterador en el REPL | Envuélvelo en `list(...)`, con un `islice` si es infinito |
| Comparar con el anterior | `pairwise(values)`, sin índices |
| Rachas sin contadores a mano | `groupby(datos, key=...)` y `len(list(group))` |
| Refactorizar sin miedo | Tests en verde antes y después; si cambias un test, no es una refactorización |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-06` de `python-<nombre>-<apellido>` con `trends.py`, tu `main` ampliado, las refactorizaciones de `values_by_label` y `longest_streak`, tu `medidas.txt` con al menos 12 líneas en orden y al menos 6 tests propios, todo en verde en tu máquina y en Docker, y `mypy` sin errores
2. ✅ `README.md` del repositorio con el informe nuevo y la tabla con el orden de cada función
3. ✅ Pull request `week-06` → `main` con tests, `mypy`, informe y la explicación de por qué tu media móvil es O(n)

El cuestionario de la [rúbrica](rubrica-evaluacion.md) es tu autoevaluación: respóndelo antes de mirar las respuestas.

---

## ✅ Verificación

En tu proyecto:

```bash
uv run pytest
uv run --with mypy==2.4.1 mypy src tests
uv run observatorio < medidas.txt; echo "código: $?"
docker compose run --build --rm app
```

Los tests terminan en `passed` sin `failed`, `mypy` dice `Success: no issues found` y el informe termina con `mediana`, `media móvil (3)` y `mayor salto`. En los ejercicios, cada paso descomentado da la salida que muestra su README (en los tiempos, la misma proporción entre filas).

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 05](../week-05-colecciones_y_comprehensions/README.md) | **Semana 06** | Semana 07 (próximamente) |

← [Volver al índice de semanas](../README.md)
