# Proyecto — Observatorio, capa 2: muchas líneas y un resumen

⏱️ 5 h 30 min · Capa 2 del [proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md). **Único entregable de la semana.**

## Qué construyes

Hasta ahora el Observatorio clasificaba **una** línea. Esta semana procesa un archivo entero de medidas de tu dominio: salta comentarios y líneas vacías, escribe la fila de cada medida, avisa de las líneas inválidas con su número sin detenerse, y termina con un resumen por niveles y la racha más larga en nivel alto.

```bash
uv run observatorio < medidas.txt
```

| Función | Archivo | Recibe | Devuelve |
|---|---|---|---|
| `is_data_line("# nota")` | `report.py` | Una línea | `False`: es un comentario |
| `level_of(row)` | `report.py` | Una fila de `format_row` | Su nivel, por ejemplo `"medio"` |
| `summarize(rows)` | `report.py` | Las filas | `"registros: 4 \| bajo: 1 \| medio: 2 \| alto: 1 \| sin dato: 0"` |
| `longest_streak(rows, "alto")` | `report.py` | Las filas y un nivel | La mayor cantidad de filas seguidas con ese nivel |
| `main([...])` | `__main__.py` | Los argumentos | El código de salida: `0`, `1` o `2` |

`parse_line`, de la semana 2, no cambia: `main` la llama una vez por línea.

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-03`. El `starter/` trae las capas 0 y 1 resueltas para funcionar solo; **tú usas las tuyas** y copias únicamente los archivos nuevos.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-02` está fusionado en `main`. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-03
```

### 2. Copia los archivos nuevos

Antes de copiar, **apunta** tus `UNIT`, `LOW` y `HIGH` de `src/observatorio/__main__.py`: el archivo nuevo los sustituye por los valores de partida.

```bash
grep -E '^(UNIT|LOW|HIGH)' src/observatorio/__main__.py
STARTER=<ruta-al-bootcamp>/bootcamp/week-03-bucles_iteracion_y_depuracion/3-proyecto/starter
cp $STARTER/src/observatorio/report.py $STARTER/src/observatorio/__main__.py src/observatorio/
cp $STARTER/tests/test_report.py $STARTER/tests/test_main.py $STARTER/tests/test_my_report.py tests/
cp $STARTER/medidas.txt .
sed -i 's/week-02/week-03/' compose.yaml
git status --short
```

Vuelve a escribir tus tres valores en el `__main__.py` nuevo. `git status` debe mostrar modificados `__main__.py`, `tests/test_main.py` y `compose.yaml`, y nuevos `report.py`, `test_report.py`, `test_my_report.py` y `medidas.txt`. `record.py`, `rules.py` y tus tests de las semanas 1 y 2 no se tocan.

### 3. Tests en rojo

```bash
uv run pytest
```

Salida esperada: `28 failed`, y en verde todo lo de las semanas anteriores (los 12 de `test_record.py`, los 17 de `test_rules.py` y tus tests propios). Fallan `test_report.py` (19), `test_main.py` (8) y el ejemplo de `test_my_report.py`, todos con `NotImplementedError`.

### 4. `is_data_line`

En `src/observatorio/report.py`: quita los espacios a los lados y devuelve si el resultado no está vacío **y** no empieza por `"#"` (semana 2: `strip`, `startswith`, `and`).

```bash
uv run pytest -k is_data_line
```

Esperado: `7 passed`. `"Norte # sin comentario;12,5"` es un dato: el `#` no está al principio.

### 5. `level_of`

Una línea: lo que va después del **último** `" | "` de la fila. `rpartition` (como `partition`, pero desde la derecha) te da las tres partes.

```bash
uv run pytest -k level_of
```

Esperado: `4 passed`.

### 6. `summarize`

Cuatro contadores creados **antes** del bucle, un `for` sobre las filas, un `if`/`elif` con `level_of(row)` y una f-string al final con el formato exacto de la docstring (teoría 03, contador). El total es `len(rows)`.

```bash
uv run pytest -k summarize
```

Esperado: `3 passed`. Si `test_summarize_mixed` da `bajo: 0 | medio: 1` cuando esperaba `bajo: 1 | medio: 2`, tus contadores se reinician dentro del bucle.

### 7. `longest_streak`

El patrón racha de la teoría 03: `current` y `best`. Antes de escribirlo, haz la tabla de traza para `["medio", "alto", "medio", "alto", "alto", "alto"]` con `"alto"`: `best` debe acabar en `3`.

```bash
uv run pytest -k longest_streak
```

Esperado: `5 passed`. Si `test_longest_streak[levels1-alto-3]` da `1`, actualizas `best` solo cuando la racha se corta. **Depúralo** antes de mirar la teoría: en VS Code, vista Testing → clic derecho sobre ese test → **Debug Test**, con un punto de parada en tu `for`. Es el mismo error del paso 3 del ejercicio 03.

### 8. `main`

La docstring describe cada caso. El esqueleto:

1. `args = sys.argv[1:] if argv is None else argv`.
2. `match args:` con cuatro `case`, en este orden: `["-h" | "--ayuda"]` (ayuda, `0`); `[option, *_] if option.startswith("-")` (`USAGE` a stderr, `2`); `[]` (`lines = sys.stdin`); `_` (`lines = args`).
3. `rows = []` y `errors = 0` antes del bucle.
4. `for number, line in enumerate(lines, start=1):` con `line = line.strip()`, `continue` si no es línea de datos, y `parse_line(line, UNIT, LOW, HIGH)`. Si da `None`, error a stderr, `errors += 1` y `continue`; si no, `print` y `rows.append(row)`.
5. Después del bucle: `print(summarize(rows))`, la racha con `f"racha más larga en alto: {longest_streak(rows, 'alto')}"` y `return 1 if errors > 0 else 0`.

`sys.stdin` y una lista de argumentos son los dos iterables de líneas: el mismo `for` sirve para los dos.

```bash
uv run pytest tests/test_main.py
```

Esperado: `8 passed`.

### 9. Tus medidas, en la terminal

Sustituye las líneas de `medidas.txt` por **al menos 10** de tu dominio: con un comentario, una línea vacía, una medida que falte (`NA`), una línea inválida y valores en los tres niveles, incluida una racha de al menos 2 en alto. Después:

```bash
uv run observatorio < medidas.txt; echo "código: $?"
uv run observatorio "Norte;12,5" "Sur;80"; echo "código: $?"
uv run observatorio -x; echo "código: $?"
grep -v '^#' medidas.txt | uv run observatorio > informe.txt; cat informe.txt
```

Con el `medidas.txt` de partida y los umbrales de partida (`unidad`, 10 y 50), el primer comando da:

```
Norte              12.5 unidad | medio
Sur                 8.0 unidad | bajo
Centro                sin dato | sin dato
Oriente            55.1 unidad | alto
Occidente          61.0 unidad | alto
Norte              48.9 unidad | medio
error: línea 10: 'Sur 9,5'
Sur                 9.5 unidad | bajo
registros: 7 | bajo: 2 | medio: 2 | alto: 2 | sin dato: 1
racha más larga en alto: 2
código: 1
```

La línea del error puede salir en otro sitio (teoría 04): stdout y stderr tienen búferes distintos. En `informe.txt` solo quedan las filas y el resumen; el error salió en la pantalla. Borra `informe.txt` al terminar.

### 10. Tus tests, calculados a mano

En `tests/test_my_report.py`, sustituye el ejemplo por **al menos 6 tests tuyos** con filas de tu dominio. Construye las filas con `format_row` (o `parse_line`) y tu unidad, y calcula los resultados con una tabla de traza **antes** de ejecutar. Cubre al menos:

| Caso | Ejemplo (calidad del aire, umbrales 12 y 35) |
|---|---|
| Una línea de datos con espacios y un comentario con espacios delante | `is_data_line("  Centro;40,2  ") is True` y `is_data_line("   # 2026-11") is False` |
| `level_of` de una fila tuya con `"sin dato"` | `level_of(format_row("Centro", None, "µg/m³", "sin dato")) == "sin dato"` |
| `summarize` de 5 filas de tu dominio | Con 2 bajo, 2 alto y 1 sin dato, el texto exacto |
| Una racha que esté al **final** de la lista | `["bajo", "alto", "alto"]` da `2` |
| Una racha de un nivel que no sea `"alto"` | La de `"bajo"` |
| `main` con tus líneas | `main(["Centro;40,2", "malo"]) == 1` |

```bash
uv run pytest
```

Esperado: todo en verde, al menos `73 passed`: los 56 de los tests del bootcamp (12 + 17 + 19 + 8) y tus propios de las semanas 1, 2 y 3 (5 + 6 + 6 como mínimo).

### 11. En el contenedor

```bash
docker compose run --build --rm app
docker compose run --rm -T app observatorio < medidas.txt
```

Los mismos tests y el mismo informe que en tu máquina. `-T` conecta tu `medidas.txt` a la entrada del contenedor (teoría 04).

### 12. README, commit y pull request

Añade al `README.md` de tu repositorio cómo usar el Observatorio con un archivo y un ejemplo de informe con tus datos. Después:

```bash
git add .
git commit -m "feat: process many lines and summarize readings by level"
git push -u origin week-03
```

En GitHub, abre un *pull request* de `week-03` hacia `main` con:

1. La salida de `uv run pytest`.
2. El informe de tu `medidas.txt` y su código de salida.
3. Un error que hayas encontrado esta semana con el depurador o con `print`, explicado en dos frases: qué veías y cuál era la causa.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ImportError: cannot import name 'is_data_line'` | `report.py` no está en `src/observatorio/`: repite el paso 2 |
| Tus tests de la semana 2 fallan con otro nivel | Perdiste tus umbrales al copiar `__main__.py`: vuelve a escribirlos (paso 2) |
| `uv run observatorio` se queda esperando | Sin argumentos lee de stdin: `< medidas.txt`, o escribe líneas y `Ctrl+D` |
| `test_main_skips_comments...` da `línea 2` en vez de `línea 4` | Numeras solo las líneas de datos: usa `enumerate` sobre todas, antes del `continue` |
| `test_main_help[--ayuda]` da código `2` | El `case` de la opción desconocida está antes que el de la ayuda |
| El informe sale dos veces o el resumen dentro de las filas | El `print(summarize(rows))` quedó dentro del `for`: quítale la sangría |
| `ValueError: could not convert string to float` y se detiene todo | Una medida no numérica (`abc`): es el comportamiento esperado hasta la semana 7. Corrígela en `medidas.txt` |
| La terminal muestra `(Pdb)` | Quedó un `breakpoint()`: bórralo |

## Entrega

- Rama `week-03` de `python-<nombre>-<apellido>` con `report.py`, `__main__.py` con tus umbrales, tu `medidas.txt` y al menos 6 tests propios en `tests/test_my_report.py`, todo en verde, también en Docker.
- `README.md` del repositorio con el uso con archivo y un informe de ejemplo.
- *Pull request* `week-03` → `main` con la descripción del paso 12.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · Muchas líneas](../2-practicas/ejercicio-04-muchas-lineas/README.md) | **Proyecto · Observatorio, capa 2** | [Webgrafía](../4-recursos/webgrafia/README.md) |
