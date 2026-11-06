# Proyecto — Observatorio, capa 4: registros, conteos y grupos

⏱️ 6 h 30 min · Capa 4 del [proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md). **Único entregable de la semana.**

## Qué construyes

Hasta ahora cada medida se convertía enseguida en una fila de texto (`"Norte   12.5 µg/m³ | medio"`) y el número se perdía. Esta semana guardas cada medida como un **registro**, la tupla `("Norte", 12.5)`, y con listas, diccionarios y conjuntos respondes preguntas nuevas: cuántas etiquetas distintas hay y cuáles tienen la media más alta.

| Función | Recibe | Devuelve | Colección |
|---|---|---|---|
| `parse_record(line)` | `"Norte;12,5"` | `("Norte", 12.5)` o `None` | Tupla |
| `records_of(lines)` | Las líneas | La lista de registros válidos | List comprehension |
| `level_counts(rows)` | Las filas | `{"bajo": 2, "medio": 2, "alto": 2, "sin dato": 1}` | Dict comprehension y contador |
| `values_by_label(records)` | Los registros | `{"Norte": [12.5, 48.9], ...}` | Agrupar con `setdefault` |
| `label_means(groups)` | Los grupos | `{"Norte": 30.7, ...}` | Dict comprehension |
| `top(means, n)` | Las medias y cuántas | `[("Occidente", 61.0), ...]` | `sorted` con `key` y slicing |
| `distinct_labels(records)` | Los registros | `{"Norte", "Sur", ...}` | Set comprehension |

Todas van en `src/observatorio/groups.py`. El informe gana estas líneas al final (con el `medidas.txt` del starter):

```
...
en alto: 28.6 %
etiquetas distintas: 5
medias más altas:
  Occidente: 61.0 unidad
  Oriente: 55.1 unidad
  Norte: 30.7 unidad
```

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-05`. El `starter/` trae las capas 0 a 3 resueltas; **tú usas las tuyas**. Esta semana no copias `__main__.py`: lo amplías tú, así conservas tu unidad y tus umbrales.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-04` está fusionado en `main`. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-05
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-05-colecciones_y_comprehensions/3-proyecto/starter
cp $STARTER/src/observatorio/groups.py src/observatorio/
cp $STARTER/tests/test_groups.py $STARTER/tests/test_main.py $STARTER/tests/test_my_groups.py tests/
sed -i 's/week-04/week-05/' compose.yaml
git status --short
```

Modificados: `tests/test_main.py` y `compose.yaml`. Nuevos: `groups.py`, `test_groups.py` y `test_my_groups.py`.

### 3. Datos con etiquetas repetidas

Las medias por etiqueta solo dicen algo si una etiqueta aparece varias veces. Abre tu `medidas.txt` y asegúrate de que tiene **al menos 10 líneas de datos**, con **al menos 3 etiquetas que se repiten** y una con un valor faltante (`NA`). Conserva la línea inválida de la semana 3. Por ejemplo, para calidad del aire:

```
Norte;12,5
Norte;48,9
Norte;30,1
Sur;8
Sur;9,5
```

### 4. Tests en rojo

```bash
uv run pytest
```

Salida esperada: `33 failed`, y en verde todo lo anterior. Fallan los 25 de `test_groups.py`, 7 de los 10 de `test_main.py` (los de ayuda y opción desconocida ya pasan con tu `main`) y el ejemplo de `test_my_groups.py`.

Abre `src/observatorio/groups.py` y lee las docstrings y el alias `Record = tuple[str, float | None]` (teoría 02). Después, `tests/test_groups.py`: fíjate en los tests que comprueban el **orden** de las claves y en los `..._does_not_change_...`, que vigilan que no cambies los argumentos (teoría 01).

### 5. `parse_record`

Es el `match` de `parse_line` en `rules.py` (semana 2), pero devuelve la tupla `(etiqueta, valor)` en lugar de la fila formateada. Usa `parse_value` para el valor.

```bash
uv run pytest -k parse_record
```

Esperado: `6 passed`.

### 6. `records_of`

Dos comprehensions, una detrás de otra (teoría 05):

1. Una lista con `parse_record(line.strip())` de cada línea que pasa `is_data_line(line)`. Algunos elementos serán `None`.
2. Otra lista con los elementos de la primera que no son `None`.

Las líneas solo se recorren una vez, en la primera comprehension: por eso `test_records_of_accepts_any_iterable` pasa aunque le des un iterador.

```bash
uv run pytest -k records_of
```

Esperado: `3 passed`.

### 7. `level_counts`

Empieza con todas las claves a 0, con una dict comprehension sobre `LEVELS`, y suma uno en un bucle con `level_of(row)` (teoría 03, sección 4).

```bash
uv run pytest -k level_counts
```

Esperado: `2 passed`. `test_level_counts_keeps_order_and_zeros` comprueba que las claves salen en el orden de `LEVELS` aunque no haya filas. Si las creas a medida que aparecen, con `get`, falla.

### 8. `values_by_label`

Agrupa con `setdefault` (teoría 03 y ejercicio 02, paso 4), saltando los `None`. Anota el diccionario vacío: `groups: dict[str, list[float]] = {}`.

```bash
uv run pytest -k values_by_label
```

Esperado: `3 passed`.

### 9. `label_means` y `top`

`label_means` es una dict comprehension de una línea sobre `groups.items()`. `top` es una línea con `sorted` sobre `means.items()`, un `key` que devuelve una tupla para desempatar (teoría 01, sección 3) y un trozo `[:n]`.

```bash
uv run pytest -k label_means
uv run pytest -k test_top
```

Esperado: `2 passed` y `7 passed`. Con `-k top` saldrían 8, porque también entra `test_main_invalid_line_does_not_stop_the_rest`: `-k` busca el texto dentro del nombre, y "s**top**" lo contiene.

### 10. `distinct_labels`

Una set comprehension de una línea (teoría 05).

```bash
uv run pytest -k distinct
```

Esperado: `3 passed` (el tercero es el ejemplo de `test_my_groups.py`). Con esto, `uv run pytest tests/test_groups.py` da `25 passed`.

### 11. Amplía tu `main`

En **tu** `src/observatorio/__main__.py`:

1. Importa lo nuevo:

   ```python
   from observatorio.groups import distinct_labels, label_means, records_of, top, values_by_label
   from observatorio.record import describe_record
   ```

2. Debajo de `HIGH`, una constante con cuántas medias se muestran: `TOP = 3`.
3. En el `case []:`, cambia `lines = sys.stdin` por `lines = list(sys.stdin)`. Ahora las líneas se recorren **dos** veces (`process_lines` y `records_of`), y `sys.stdin` se agota en la primera (ejercicio 03, paso 5).
4. Después de la línea `en alto`, calcula `records = records_of(lines)` y escribe:
   - `f"etiquetas distintas: {len(distinct_labels(records))}"`;
   - `"medias más altas:"`;
   - un `for label, mean in top(label_means(values_by_label(records)), TOP):` que escribe `f"  {describe_record(label, mean, UNIT)}"`.

```bash
uv run pytest tests/test_main.py
```

Esperado: `10 passed`. Si `test_main_reads_stdin` falla con `etiquetas distintas: 0`, falta el punto 3: `records_of` recibió un `sys.stdin` ya agotado.

### 12. Refactoriza `count_level`

`count_level` (semana 4) es un contador con un bucle. Ahora que tienes `level_counts`, puede ser una línea en `analysis.py`:

```python
from observatorio.groups import level_counts
...
    return level_counts(rows).get(level, 0)
```

El `.get(level, 0)` mantiene el comportamiento con un nivel que no existe. Es una **refactorización**: los tests no cambian y deben seguir en verde.

```bash
uv run pytest
uv run --with mypy==2.4.1 mypy src tests
```

Esperado: ningún `failed` y `Success: no issues found`.

### 13. Tus tests

En `tests/test_my_groups.py`, sustituye el ejemplo por **al menos 6 tests tuyos** con datos de tu dominio, en preparar, actuar y comprobar:

| Qué pruebas | Ejemplo (calidad del aire) |
|---|---|
| `parse_record` con un formato real de tu dominio | `parametrize` con una línea con espacios, una con `NA` y una sin `;` |
| `values_by_label` con una etiqueta que solo tiene `None` | No aparece en el resultado |
| `label_means` con tus valores | `pytest.approx` con la media de tres lecturas del Norte |
| `top` con un empate de tu dominio | Dos estaciones con la misma media: la alfabética primero |
| `distinct_labels` con mayúsculas | `"norte"` y `"Norte"` cuentan como dos: ¿es lo que quieres? Escríbelo en el test |
| `level_counts` con tus umbrales | Las filas de tu `medidas.txt` dan los conteos que esperas |

```bash
uv run pytest
```

Esperado: todo en verde, al menos `132 passed`: los 103 del bootcamp (12 + 17 + 19 + 20 + 10 + 25) y los 29 tuyos como mínimo (5 + 6 + 6 + 6 + 6 de las semanas 1 a 5).

### 14. En la terminal y en el contenedor

```bash
uv run observatorio < medidas.txt; echo "código: $?"
docker compose run --build --rm app
docker compose run --rm -T app observatorio < medidas.txt
```

El informe, igual en tu máquina y en el contenedor, termina con las etiquetas distintas y las tres medias más altas de tu dominio.

### 15. README, commit y pull request

Añade al `README.md` de tu repositorio las líneas nuevas del informe y una frase sobre qué te dicen las medias más altas de tu dominio. Haz commits pequeños: uno por función en verde, uno para `main` y otro para la refactorización. Al final:

```bash
git push -u origin week-05
```

En GitHub, abre un *pull request* de `week-05` hacia `main` con:

1. La salida de `uv run pytest` y de `mypy`.
2. El informe de tu `medidas.txt`.
3. Por qué `main` necesita `list(sys.stdin)` y qué pasaba sin él.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ImportError: cannot import name 'records_of'` | `groups.py` no está en `src/observatorio/`: repite el paso 2 |
| `ImportError` circular al importar `level_counts` en `analysis.py` | Importaste `analysis` desde `groups.py`: `groups` solo importa de `record` y `report` |
| `test_level_counts_keeps_order_and_zeros` falla | Creas las claves con `get` a medida que aparecen: créalas todas a 0 antes del bucle |
| `test_values_by_label_groups_and_skips_none` da `'Centro': []` | Haces `setdefault` antes de comprobar el `None`: compruébalo primero |
| `test_top_ties_in_alphabetical_order` da `Sur` antes que `Este` | Con `reverse=True`, el desempate también se invierte o se queda en el orden de entrada: usa `key=lambda pair: (-pair[1], pair[0])` sin `reverse` |
| `test_top_does_not_change_means` falla | Usaste algo que cambia el diccionario; `sorted` crea una lista nueva |
| `etiquetas distintas: 0` al leer de stdin | Falta `list(sys.stdin)`: paso 11 |
| `mypy`: `Need type annotation for "groups"` | `groups: dict[str, list[float]] = {}` |

## Entrega

- Rama `week-05` de `python-<nombre>-<apellido>` con `groups.py`, tu `main` ampliado, `count_level` refactorizado, tu `medidas.txt` con etiquetas repetidas y al menos 6 tests propios en `tests/test_my_groups.py`, todo en verde (también en Docker) y `mypy` sin errores.
- `README.md` del repositorio con el informe nuevo.
- *Pull request* `week-05` → `main` con la descripción del paso 15.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · Estructuras anidadas](../2-practicas/ejercicio-04-estructuras-anidadas/README.md) | **Proyecto · Observatorio, capa 4** | [Webgrafía](../4-recursos/webgrafia/README.md) |
