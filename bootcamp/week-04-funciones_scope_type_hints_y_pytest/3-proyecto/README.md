# Proyecto — Observatorio, capa 3: lógica pura, proporciones y tipos

⏱️ 6 h · Capa 3 del [proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md). **Único entregable de la semana.**

## Qué construyes

En la semana 3, `main` hacía de todo: recorría las líneas, decidía y escribía. Esta semana separas la **lógica**, en funciones puras que devuelven, de la **entrada/salida**, que se queda en `main`. Además, el informe gana una línea nueva, el porcentaje de medidas en nivel alto, y revisas los tipos de todo el paquete con `mypy`.

| Función | Archivo | Recibe | Devuelve |
|---|---|---|---|
| `process_lines(lines, unit, low, high)` | `analysis.py` | Las líneas y las reglas | `(filas, errores)`, sin imprimir nada |
| `count_level(rows, "alto")` | `analysis.py` | Filas y un nivel | Cuántas filas tienen ese nivel |
| `ratio(2, 7)` | `analysis.py` | Parte y total | `0.2857…`; `ValueError` si es imposible |
| `share(2, 7, decimals=2)` | `analysis.py` | Parte, total y decimales solo por nombre | `"28.57 %"` |
| `main([...])` | `__main__.py` | Los argumentos | El código de salida; ahora solo lee y escribe |

El informe queda así (con los umbrales de partida):

```
...
registros: 7 | bajo: 2 | medio: 2 | alto: 2 | sin dato: 1
racha más larga en alto: 2
en alto: 28.6 %
```

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-04`. El `starter/` trae las capas 0, 1 y 2 resueltas; **tú usas las tuyas** y copias solo los archivos nuevos.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-03` está fusionado en `main`. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-04
```

### 2. Copia los archivos nuevos

Como la semana pasada, **apunta** tus `UNIT`, `LOW` y `HIGH` antes de copiar, y vuelve a escribirlos después en el `__main__.py` nuevo:

```bash
grep -E '^(UNIT|LOW|HIGH)' src/observatorio/__main__.py
STARTER=<ruta-al-bootcamp>/bootcamp/week-04-funciones_scope_type_hints_y_pytest/3-proyecto/starter
cp $STARTER/src/observatorio/analysis.py $STARTER/src/observatorio/__main__.py src/observatorio/
cp $STARTER/tests/test_analysis.py $STARTER/tests/test_main.py $STARTER/tests/test_my_analysis.py tests/
sed -i 's/week-03/week-04/' compose.yaml
git status --short
```

Modificados: `__main__.py`, `tests/test_main.py` y `compose.yaml`. Nuevos: `analysis.py`, `test_analysis.py` y `test_my_analysis.py`.

### 3. Tests en rojo

```bash
uv run pytest
```

Salida esperada: `29 failed`, y en verde todo lo anterior (12 + 17 + 19 del bootcamp y tus tests propios de las semanas 1 a 3). Fallan `test_analysis.py` (20), `test_main.py` (8) y el ejemplo de `test_my_analysis.py`.

Abre `tests/test_analysis.py` y léelo entero antes de seguir: ahora sabes qué hace cada pieza (teoría 05). Fíjate en `test_process_lines_does_not_print`: comprueba con `capsys` que `process_lines` **no** escribe nada.

### 4. `process_lines`

Es el bucle de tu `main` de la semana 3, movido a una función que **devuelve** en lugar de imprimir:

- Antes del bucle: `rows: list[str] = []` y `errors: list[str] = []` (la anotación hace falta en las listas vacías, teoría 04).
- En el bucle, lo mismo que en la semana 3, pero `rows.append(row)` en lugar de `print(row)` y `errors.append(f"línea {number}: {line!r}")` en lugar de escribir en stderr.
- Al final: `return rows, errors`.

Usa los parámetros `unit`, `low` y `high`, no las constantes de `__main__.py`: así la función sirve para cualquier dominio y los tests le pasan los suyos.

```bash
uv run pytest -k process_lines
```

Esperado: `4 passed`. `test_process_lines_accepts_any_iterable` le pasa un iterable que solo se puede recorrer una vez: si recorres `lines` dos veces, la segunda vuelta no encuentra nada.

### 5. `count_level`

Un contador (semana 3) con `level_of`, que importas de `report.py`:

```bash
uv run pytest -k count_level
```

Esperado: `4 passed`.

### 6. `ratio`

Tres partes, con cláusulas de guarda (teoría 01):

1. Si `part` o `total` son negativos, o `part > total`: `raise ValueError(...)` con un mensaje que diga qué valores llegaron.
2. Si `total == 0`: `return 0.0`.
3. `return part / total`.

```bash
uv run pytest -k ratio
```

Esperado: `8 passed, 1 failed`. Los 8 son los de `ratio`: 5 de valores (con `pytest.approx`) y 3 de errores (con `pytest.raises`). El que falla es `test_share_propagates_ratio_errors`, que también lleva `ratio` en el nombre: se pondrá en verde en el paso 7.

### 7. `share`

Una línea: `ratio(part, total) * 100`, formateado con `decimals` decimales y `" %"`. Para un número de decimales que está en una variable, el formato admite otra llave dentro: `f"{x:.{decimals}f}"`.

```bash
uv run pytest -k share
```

Esperado: `5 passed` (el quinto es el ejemplo de `test_my_analysis.py`). `share(8, 7)` lanza el `ValueError` de `ratio` sin que `share` haga nada: un error sube por las llamadas hasta que alguien lo trata.

### 8. `main`, delgado

Conserva la parte de `match` de la semana 3 (ayuda, opción desconocida, stdin o argumentos). Después:

1. `rows, errors = process_lines(lines, UNIT, LOW, HIGH)`.
2. Un `for` que imprime cada fila y otro que escribe cada error en stderr con el prefijo `"error: "`.
3. El resumen, la racha y la línea nueva: `f"en alto: {share(count_level(rows, 'alto'), len(rows))}"`.
4. `return 1 if errors else 0`.

```bash
uv run pytest tests/test_main.py
```

Esperado: `8 passed`. Ahora `main` no tiene ninguna decisión sobre los datos: si mañana las líneas llegan de una API, solo cambia `main`.

### 9. Revisa los tipos con `mypy`

```bash
uv run --with mypy==2.4.1 mypy src tests
```

Objetivo: `Success: no issues found`. Errores típicos en tu código de semanas anteriores:

| Error de `mypy` | Arreglo |
|---|---|
| `Need type annotation for "rows"` | `rows: list[str] = []` |
| `Unsupported operand types ... "None"` | Comprueba `is None` antes de usar el valor (teoría 04) |
| `Function is missing a return type annotation` | No aparece por defecto; si lo ves, añade `-> None` a tus tests |
| `Incompatible types in assignment (expression has type "float \| None", variable has type "float")` | La variable puede recibir `None`: anótala `float \| None` |

Arreglar tipos es **refactorizar**: el comportamiento no cambia, así que `uv run pytest` debe seguir igual de verde después de cada cambio.

### 10. Tus tests, con las herramientas nuevas

En `tests/test_my_analysis.py`, sustituye el ejemplo por **al menos 6 tests tuyos** con datos de tu dominio, organizados en preparar, actuar y comprobar. Deben usar al menos una vez cada herramienta de la teoría 05:

| Herramienta | Ejemplo (calidad del aire, umbrales 12 y 35) |
|---|---|
| `parametrize` con los límites de **tus** umbrales | `count_level` con filas justo en `LOW` y en `HIGH` |
| `pytest.approx` | `ratio(1, 3) == pytest.approx(0.3333333)` |
| `pytest.raises` | `share(-1, 5)` lanza `ValueError` |
| `process_lines` con tus líneas | Una línea válida, un comentario y una inválida: comprueba filas y errores |
| `decimals=` | `share(1, 3, decimals=0) == "33 %"` |
| Un iterable que no es lista | `process_lines(iter([...]), ...)` |

```bash
uv run pytest
```

Esperado: todo en verde, al menos `99 passed`: los 76 del bootcamp (12 + 17 + 19 + 20 + 8) y los 23 tuyos como mínimo (5 + 6 + 6 + 6 de las semanas 1 a 4).

### 11. En la terminal y en el contenedor

```bash
uv run observatorio < medidas.txt; echo "código: $?"
docker compose run --build --rm app
docker compose run --rm -T app observatorio < medidas.txt
```

Las filas, los errores, el resumen, la racha y el porcentaje, igual en tu máquina y en el contenedor.

### 12. README, commit y pull request

Añade al `README.md` de tu repositorio la línea nueva del informe y una frase sobre cómo está organizado el código: qué hace `analysis.py` y qué hace `__main__.py`. Haz commits pequeños mientras avanzas (uno por función en verde, otro para los tipos). Al final:

```bash
git push -u origin week-04
```

En GitHub, abre un *pull request* de `week-04` hacia `main` con:

1. La salida de `uv run pytest` y de `mypy`.
2. El informe de tu `medidas.txt`.
3. Un ejemplo de un límite de tu dominio que pruebas con `parametrize` y por qué lo elegiste.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ImportError: cannot import name 'process_lines'` | `analysis.py` no está en `src/observatorio/`: repite el paso 2 |
| `test_process_lines_does_not_print` falla | Quedó un `print` dentro de `process_lines`: mueve la escritura a `main` |
| `test_process_lines_accepts_any_iterable` da 0 filas | Recorres `lines` dos veces, o lo conviertes antes con algo que lo agota |
| `assert 0.2857142857142857 == 0.2857142857` | Comparaste con `==`; el test usa `pytest.approx`: no lo cambies, revisa `ratio` |
| `Failed: DID NOT RAISE ValueError` | `ratio` no valida `part > total` o los negativos |
| `share(1, 3, decimals=0)` da `"33.0 %"` | Escribiste `.1f` fijo; usa `.{decimals}f` |
| Tus tests de semanas anteriores fallan con otro nivel | Perdiste tus umbrales al copiar `__main__.py`: paso 2 |
| `error: Failed to spawn: mypy` | `uv run --with mypy==2.4.1 mypy src tests`, con `mypy` dos veces |

## Entrega

- Rama `week-04` de `python-<nombre>-<apellido>` con `analysis.py`, el `main` delgado con tus umbrales, al menos 6 tests propios en `tests/test_my_analysis.py`, todo en verde (también en Docker) y `mypy` sin errores.
- `README.md` del repositorio con la organización del código y el informe nuevo.
- *Pull request* `week-04` → `main` con la descripción del paso 12.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · pytest desde cero](../2-practicas/ejercicio-04-pytest-desde-cero/README.md) | **Proyecto · Observatorio, capa 3** | [Webgrafía](../4-recursos/webgrafia/README.md) |
