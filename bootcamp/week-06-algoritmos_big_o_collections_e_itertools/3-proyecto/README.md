# Proyecto — Observatorio, capa 5: tendencias y eficiencia

⏱️ 6 h 30 min · Capa 5 del [proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md). **Único entregable de la semana.**

## Qué construyes

Las medias por etiqueta de la semana 5 dicen dónde se mide más, pero no cómo **evolucionan** las medidas. Esta semana lees los valores en el orden en que llegaron y calculas la mediana, una media móvil que suaviza el ruido y el salto más brusco entre dos medidas seguidas. Cada función recorre los datos una sola vez, con las herramientas de `collections` e `itertools`.

| Función | Recibe | Devuelve | Herramienta | Orden |
|---|---|---|---|---|
| `values_of(records)` | Los registros | `[12.5, 8.0, 55.1, ...]`, sin `None` | List comprehension | O(n) |
| `most_common_labels(records, n)` | Registros y cuántas | `[("Norte", 2), ("Sur", 2), ...]` | `Counter.most_common` | O(n) |
| `median(values)` | Los valores | `30.7` | `sorted` | O(n log n) |
| `moving_average(values, window)` | Valores y ventana | `[25.2, 41.4, 55.0, 39.8]` | `deque` y total acumulado | O(n) |
| `jumps(values)` | Los valores | `[-4.5, 47.1, 5.9, ...]` | `pairwise` | O(n) |
| `largest_jump(values)` | Los valores | `47.1` | `max` con `key=abs` | O(n) |

Todas van en `src/observatorio/trends.py`. Además refactorizas dos funciones de semanas anteriores: `values_by_label` con `defaultdict` y `longest_streak` con `groupby`. El informe gana estas líneas al final (con el `medidas.txt` del starter):

```
...
medias más altas:
  Occidente: 61.0 unidad
  Oriente: 55.1 unidad
  Norte: 30.7 unidad
más frecuentes:
  Norte: 2
  Sur: 2
  Centro: 1
mediana: 30.7 unidad
media móvil (3): 25.2 · 41.4 · 55.0 · 39.8
mayor salto: +47.1 unidad
```

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-06`. El `starter/` trae las capas 0 a 4 resueltas; **tú usas las tuyas**. Como en la semana 5, no copias `__main__.py`: lo amplías tú.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-05` está fusionado en `main`. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-06
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-06-algoritmos_big_o_collections_e_itertools/3-proyecto/starter
cp $STARTER/src/observatorio/trends.py src/observatorio/
cp $STARTER/tests/test_trends.py $STARTER/tests/test_main.py $STARTER/tests/test_groups.py $STARTER/tests/test_my_trends.py tests/
sed -i 's/week-05/week-06/' compose.yaml
git status --short
```

Modificados: `tests/test_main.py`, `tests/test_groups.py` (un test nuevo al final) y `compose.yaml`. Nuevos: `trends.py`, `test_trends.py` y `test_my_trends.py`.

### 3. Datos en orden

La media móvil y los saltos leen los valores **en el orden del archivo**, como si fueran llegando en el tiempo. Abre tu `medidas.txt` y asegúrate de que tiene **al menos 12 líneas de datos**, ordenadas como se tomaron, con alguna subida o bajada brusca que se vea en el informe. Conserva las etiquetas repetidas, el `NA` y la línea inválida de semanas anteriores.

### 4. Tests en rojo

```bash
uv run pytest
```

Salida esperada: `35 failed`, y en verde todo lo anterior. Fallan los 27 de `test_trends.py`, 7 de los 12 de `test_main.py` (los de ayuda, opción desconocida y los dos de medias ya pasan con tu `main`) y el ejemplo de `test_my_trends.py`. El test nuevo de `test_groups.py` ya pasa: vigila la refactorización del paso 10.

Abre `src/observatorio/trends.py`: los `import` de arriba te dicen qué herramienta usa cada función. Después, `tests/test_trends.py`: fíjate en `test_moving_average_is_linear`, que pasa 200 000 valores con una ventana de 1 000.

### 5. `values_of` y `most_common_labels`

`values_of` es una list comprehension que salta los `None` (semana 5). `most_common_labels` es una línea: un `Counter` de las etiquetas, con una expresión generadora, y su `most_common(n)` (teoría 04).

```bash
uv run pytest -k "values_of or most_common"
```

Esperado: `7 passed`. `test_most_common_labels_ties_keep_first_seen_order` pasa solo: `most_common` ya deja los empates en el orden de aparición.

### 6. `median`

Ordena una **copia** con `sorted`, nunca con `.sort()` sobre `values` (teoría 03). Con un número impar de valores, la mediana es el del centro; con uno par, la media de los dos del centro. `len(ordered) // 2` es la posición del centro (o la de la derecha de los dos). Si `values` está vacía, lanza `ValueError` antes de nada.

```bash
uv run pytest -k median
```

Esperado: `6 passed`. Es la función más cara del archivo, O(n log n), por culpa de ordenar. La biblioteca estándar tiene `statistics.median`; aquí la escribes para ver qué hace por dentro.

### 7. `moving_average`

Es la ventana del ejercicio 03, paso 4, con una mejora: no sumes la ventana entera en cada vuelta. Guarda el `total` de la ventana y, en cada valor:

1. Si la ventana ya está llena, resta a `total` el más antiguo, `recent[0]`, que va a salir.
2. Añade el valor al `deque(maxlen=window)` y súmalo a `total`.
3. Si la ventana está llena, añade `total / window` al resultado.

Anota el deque: `recent: deque[float] = deque(maxlen=window)`. Lanza `ValueError` si `window` es menor que 1.

```bash
uv run pytest -k moving_average --durations=1
```

Esperado: `7 passed`, y `test_moving_average_is_linear` en unas centésimas. Con `sum(recent)` en cada vuelta también pasa, pero son 200 millones de sumas: tarda alrededor de un segundo. La versión del bucle a mano, unos 10. Esa es la diferencia entre O(n) y O(n · k).

### 8. `jumps` y `largest_jump`

`jumps` es una comprehension sobre `pairwise(values)` (ejercicio 04, paso 2). `largest_jump` es un `max` sobre los saltos con `key=abs`, para comparar por tamaño sin perder el signo, y `default=0.0` para cuando no hay saltos (teoría 05).

```bash
uv run pytest -k "jumps or largest_jump"
```

Esperado: `8 passed` (el último es el ejemplo de `test_my_trends.py`). Con esto, `uv run pytest tests/test_trends.py` da `27 passed`.

### 9. Amplía tu `main`

En **tu** `src/observatorio/__main__.py`:

1. Importa lo nuevo:

   ```python
   from observatorio.trends import largest_jump, median, most_common_labels, moving_average, values_of
   ```

2. Debajo de `TOP`, el tamaño de la ventana: `WINDOW = 3`.
3. Después de las medias más altas, escribe `"más frecuentes:"` y un `for label, count in most_common_labels(records, TOP):` que escribe `f"  {label}: {count}"`.
4. Calcula `values = values_of(records)` y, **solo si hay valores** (`if values:`), escribe:
   - `f"mediana: {median(values):.1f} {UNIT}"`;
   - `f"media móvil ({WINDOW}): {averages}"`, donde `averages` son las medias con un decimal unidas por `" · "` (`" · ".join(...)` con una expresión generadora);
   - `f"mayor salto: {largest_jump(values):+.1f} {UNIT}"`. El `+` del formato escribe el signo también cuando es positivo.

```bash
uv run pytest tests/test_main.py
```

Esperado: `12 passed`. Si `test_main_without_values_skips_trends` falla con `ValueError`, falta el `if values:`: `median` no acepta una lista vacía.

### 10. Refactoriza `values_by_label` con `defaultdict`

En `groups.py` (semana 5), cambia el agrupado con `setdefault` por un `defaultdict(list)` (teoría 04, sección 2):

```python
from collections import defaultdict
...
    groups: defaultdict[str, list[float]] = defaultdict(list)
    for label, value in records:
        if value is not None:
            groups[label].append(value)
    return dict(groups)
```

El `dict(groups)` del final importa: sin él, quien lea una etiqueta que no está recibe una lista vacía y la crea sin querer. Lo vigila `test_values_by_label_returns_a_plain_dict`; quita el `dict(...)` y míralo fallar. Vuelve a ponerlo.

```bash
uv run pytest tests/test_groups.py
```

Esperado: `26 passed`, sin cambiar ningún test.

### 11. Refactoriza `longest_streak` con `groupby`

En `report.py` (semana 3), el bucle con `best` y `current` es una racha: exactamente lo que `groupby` encuentra (ejercicio 04, paso 3).

```python
from itertools import groupby
...
    return max(
        (len(list(group)) for key, group in groupby(rows, key=level_of) if key == level),
        default=0,
    )
```

`key=level_of` agrupa las filas seguidas que tienen el mismo nivel, y la expresión generadora mide solo las del nivel pedido. `default=0` cubre el caso en que ningún grupo es de ese nivel.

```bash
uv run pytest
uv run --with mypy==2.4.1 mypy src tests
```

Esperado: ningún `failed` y `Success: no issues found`. Si `mypy` dice `Need type annotation for "groups"`, falta `defaultdict[str, list[float]]` en el paso 10.

### 12. Tus tests

En `tests/test_my_trends.py`, sustituye el ejemplo por **al menos 6 tests tuyos** con datos de tu dominio, en preparar, actuar y comprobar:

| Qué pruebas | Ejemplo (calidad del aire) |
|---|---|
| `median` con tus valores | Las lecturas de un día con un pico: la mediana apenas se mueve y la media sí |
| `moving_average` con una ventana de tu dominio | Ventana de 24 lecturas horarias: con 30 lecturas salen 7 medias |
| `largest_jump` con una bajada | La lectura cae de 80 a 20 µg/m³: el salto es `-60.0`, con signo |
| `most_common_labels` con tus etiquetas | La estación que más mide va primero |
| `values_of` con tus `NA` | Los `None` desaparecen y el orden se conserva |
| `jumps` con datos de tu `medidas.txt` | `parametrize` con dos o tres tramos de tu archivo |

```bash
uv run pytest
```

Esperado: todo en verde, al menos `168 passed`: los 133 del bootcamp (12 + 17 + 19 + 20 + 12 + 26 + 27) y los 35 tuyos como mínimo (5 + 6 + 6 + 6 + 6 + 6 de las semanas 1 a 6).

### 13. En la terminal y en el contenedor

```bash
uv run observatorio < medidas.txt; echo "código: $?"
docker compose run --build --rm app
docker compose run --rm -T app observatorio < medidas.txt
```

El informe, igual en tu máquina y en el contenedor, termina con las más frecuentes, la mediana, la media móvil y el mayor salto de tu dominio.

### 14. README, commit y pull request

Añade al `README.md` de tu repositorio:

1. Las líneas nuevas del informe y una frase sobre qué dice la media móvil de tu dominio que no dijera la media.
2. Una tabla con el orden (Big-O) de cada función de `trends.py` y por qué.

Haz commits pequeños: uno por función en verde, uno para `main` y uno por cada refactorización (`refactor: ...`). Al final:

```bash
git push -u origin week-06
```

En GitHub, abre un *pull request* de `week-06` hacia `main` con:

1. La salida de `uv run pytest` y de `mypy`.
2. El informe de tu `medidas.txt`.
3. El tiempo de `test_moving_average_is_linear` (`--durations=1`) y por qué tu `moving_average` es O(n) y no O(n · k).

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ImportError: cannot import name 'largest_jump'` | `trends.py` no está en `src/observatorio/`: repite el paso 2 |
| `ImportError` circular con `trends` | `trends.py` solo importa de `groups` (el alias `Record`); no importes `analysis` ni `__main__` |
| `test_median_does_not_change_values` falla | Usaste `values.sort()`: ordena una copia con `sorted(values)` |
| `test_moving_average_window_three` da valores de más | Añades una media antes de que la ventana esté llena: compruébalo con `len(recent) == window` |
| La media móvil da números que no cuadran | Restas `recent[0]` **después** de añadir el nuevo: con `maxlen` el más antiguo ya se ha caído y restas otro; réstalo antes |
| `test_largest_jump_keeps_the_sign` da `8.0` | Hiciste `max(abs(j) for j in ...)`: eso pierde el signo; usa `key=abs` |
| `ValueError: max() iterable argument is empty` | Falta `default=0.0` en `largest_jump` o `default=0` en `longest_streak` |
| `test_main_without_values_skips_trends` da `ValueError` | Falta el `if values:` antes de la mediana: paso 9 |
| `test_values_by_label_returns_a_plain_dict` falla | Devuelves el `defaultdict`: `return dict(groups)` |

## Entrega

- Rama `week-06` de `python-<nombre>-<apellido>` con `trends.py`, tu `main` ampliado, las dos refactorizaciones, tu `medidas.txt` con al menos 12 líneas en orden y al menos 6 tests propios en `tests/test_my_trends.py`, todo en verde (también en Docker) y `mypy` sin errores.
- `README.md` del repositorio con el informe nuevo y la tabla de órdenes.
- *Pull request* `week-06` → `main` con la descripción del paso 14.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · itertools](../2-practicas/ejercicio-04-itertools/README.md) | **Proyecto · Observatorio, capa 5** | [Webgrafía](../4-recursos/webgrafia/README.md) |
