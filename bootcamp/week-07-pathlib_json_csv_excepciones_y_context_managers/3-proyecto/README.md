# Proyecto — Observatorio, capa 6: archivos, CSV, JSON y errores

⏱️ 6 h 30 min · Capa 6 del [proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md). **Único entregable de la semana.**

## Qué construyes

Hasta ahora el Observatorio recibía sus medidas por argumentos o por la entrada estándar, y todo lo que calculaba se perdía al cerrar la terminal. Esta semana abre él mismo sus archivos de texto y CSV, y guarda un resumen en JSON que otro programa (o tú, mañana) puede leer. Cualquier fallo de archivo, como uno que no existe, uno que no es UTF-8 o una cabecera inesperada, sale como **una sola excepción propia**, `DataFileError`, con un mensaje en español. `main` la captura en un solo sitio.

| Función | Recibe | Devuelve | Herramienta |
|---|---|---|---|
| `read_lines(path)` | Una ruta | `["Norte;12,5", "Sur;8", ...]` | `path.open`, `with`, `raise ... from` |
| `read_csv(path)` | La ruta de un CSV | Las filas como líneas `"etiqueta;valor"` | `csv.reader` con `delimiter=";"` |
| `read_data(path)` | Una ruta | Las líneas, por CSV o por texto | `path.suffix` |
| `summary_data(records)` | Los registros | `{"registros": 7, "con_valor": 6, ...}` | Un diccionario |
| `write_json(data, path)` | El resumen y una ruta | Nada: escribe el archivo | `json.dump` |
| `read_json(path)` | Una ruta | El diccionario guardado | `json.loads` |

Todas van en `src/observatorio/storage.py`, junto a la excepción `DataFileError` y la cabecera `HEADER`, que ya vienen escritas. `main` gana dos opciones:

```bash
uv run observatorio -f medidas.csv                    # las líneas salen del archivo
uv run observatorio -f medidas.csv -j resumen.json    # y además guarda el resumen
```

Con el `medidas.csv` del starter, el informe es el mismo que con `< medidas.txt`, con una línea más al final:

```
...
mayor salto: +47.1 unidad
resumen guardado en resumen.json
```

Y `resumen.json`:

```json
{
  "registros": 7,
  "con_valor": 6,
  "mediana": 30.7,
  "mayor_salto": 47.1
}
```

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-07`. El `starter/` trae las capas 0 a 5 resueltas; **tú usas las tuyas**. No copias `__main__.py`: lo amplías tú.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-06` está fusionado en `main`. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-07
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-07-pathlib_json_csv_excepciones_y_context_managers/3-proyecto/starter
cp $STARTER/src/observatorio/storage.py src/observatorio/
cp $STARTER/tests/test_storage.py $STARTER/tests/test_main.py $STARTER/tests/test_my_storage.py tests/
sed -i 's/week-06/week-07/' compose.yaml
echo "resumen.json" >> .gitignore
git status --short
```

Modificados: `tests/test_main.py`, `compose.yaml` y `.gitignore`. Nuevos: `storage.py`, `test_storage.py` y `test_my_storage.py`. `resumen.json` va al `.gitignore` porque lo genera el programa: se sube el código que lo crea, no el archivo.

### 3. Tu `medidas.csv`

Crea `medidas.csv` en la raíz del proyecto con las mismas medidas que tu `medidas.txt`, en el mismo orden, con esta primera línea de cabecera:

```
etiqueta;valor
Norte;12,5
Sur;8
Centro;NA
...
```

El separador es `;` y no `,` porque tus valores usan coma decimal: es el formato que exporta Excel o LibreOffice en español. Como en tu `medidas.txt`, deja **al menos 12 filas de datos**, alguna etiqueta repetida, un `NA` y una fila inválida (sin `;`). Lo que no lleva un CSV son comentarios ni líneas en blanco: la cabecera ya dice qué es cada columna.

### 4. Tests en rojo

```bash
uv run pytest
```

Salida esperada: `35 failed`, y en verde todo lo anterior. Fallan 27 de los 28 de `test_storage.py` (`test_data_file_error_is_an_exception` ya pasa: la clase viene escrita), 7 de los 20 de `test_main.py` y el ejemplo de `test_my_storage.py`.

Abre `tests/test_storage.py`. Casi todos los tests reciben `tmp_path`: una carpeta temporal **nueva para cada test**, que pytest crea y borra. Así cada test escribe sus propios archivos sin tocar tu proyecto ni pisar a los demás. Fíjate también en `caught.value.__cause__`: comprueba que guardaste la excepción original con `raise ... from` (teoría 02).

### 5. `read_lines`

Abre el archivo con `with path.open(encoding="utf-8") as file:` y devuelve `file.read().splitlines()`, que separa las líneas sin el `\n` (teoría 01). Rodea el `with` con un `try` y traduce cada error de Python a una `DataFileError` (teoría 02):

| Captura | Lanza |
|---|---|
| `FileNotFoundError` | `DataFileError(f"no existe el archivo {path}")` |
| `IsADirectoryError` | `DataFileError(f"{path} es una carpeta")` |
| `UnicodeDecodeError` | `DataFileError(f"{path} no es texto UTF-8")` |

Cada `raise` lleva `from error`. Sin él, el test de la causa falla y quien depure tu programa pierde el error original.

```bash
uv run pytest -k read_lines
```

Esperado: `8 passed` (el último es el ejemplo de `test_my_storage.py`). Si `test_read_lines_not_utf8` falla con un `UnicodeDecodeError` sin capturar, falta `encoding="utf-8"` o falta su `except`.

### 6. `read_csv`

No abras el archivo otra vez: `read_lines(path)` ya lo lee y ya traduce sus errores. `csv.reader` acepta cualquier lista de líneas (teoría 04):

1. `rows = csv.reader(read_lines(path), delimiter=";")`.
2. `header = next(rows, None)`: la primera fila. Si es `None`, el archivo está vacío: `DataFileError(f"{path} está vacío")`.
3. Si `header != HEADER`, lanza `DataFileError(f"cabecera inesperada en {path}: {';'.join(header)}")`.
4. Devuelve cada fila restante unida otra vez con `";".join(row)`.

Una fila con un campo de menos o de más sale tal cual (`"Norte"`, `"Sur;8;9"`): `process_lines` la marcará como error, igual que con stdin. Validar dos veces sería repetirse.

```bash
uv run pytest -k read_csv
```

Esperado: `7 passed`. `test_read_csv_understands_quotes` comprueba que el módulo `csv` quita las comillas de `"Norte";"12,5"`, algo que un `split(";")` no haría.

Leer por líneas tiene un límite: un campo entre comillas con un salto de línea dentro se parte en dos. Si tus datos lo traen, abre con `newline=""` y pasa el archivo a `csv.reader`; con medidas de una línea no hace falta.

### 7. `read_data` y `summary_data`

`read_data` elige: si `path.suffix.lower() == ".csv"`, `read_csv(path)`; si no, `read_lines(path)`. El `.lower()` hace que `MEDIDAS.CSV` también cuente como CSV.

`summary_data` arma el diccionario que irá al JSON, con `values_of`, `median` y `largest_jump` de la semana 6. Redondea la mediana y el salto con `round(..., 1)`. Sin valores, `median` lanza `ValueError`: en ese caso, las dos claves valen `None`, que en JSON se escribe `null`.

```bash
uv run pytest -k "read_data or summary_data"
```

Esperado: `6 passed`.

### 8. `write_json` y `read_json`

`write_json` abre en modo escritura, `path.open("w", encoding="utf-8")`, y dentro del `with` llama a `json.dump(data, file, ensure_ascii=False, indent=2)` y escribe un `"\n"` final (teoría 05). Captura `OSError`, la madre de todos los errores de archivo, y lanza `DataFileError(f"no se puede escribir {path}")`.

`read_json` lee el texto con `read_lines` (unido con `"\n".join(...)`), lo convierte con `json.loads` y traduce `json.JSONDecodeError` en `DataFileError(f"JSON no válido en {path}, línea {error.lineno}")`. Si el resultado no es un diccionario (`isinstance(data, dict)`), lanza `DataFileError(f"{path} no contiene un objeto JSON")`.

```bash
uv run pytest -k "write_json or read_json or round_trip"
```

Esperado: `7 passed`. Con esto, `uv run pytest tests/test_storage.py` da `28 passed`. `test_json_round_trip` es la prueba de fuego de un formato: lo que escribes y vuelves a leer es igual a lo que tenías.

### 9. Amplía tu `main`

En **tu** `src/observatorio/__main__.py`:

1. Importa lo nuevo:

   ```python
   from pathlib import Path

   from observatorio.storage import DataFileError, read_data, summary_data, write_json
   ```

2. Añade las opciones nuevas a `USAGE`: `'... o  observatorio -f archivo [-j resumen.json]'`.
3. Antes del `match`, `source: Path | None = None` y `output: Path | None = None`.
4. Dos `case` nuevos, **antes** del que rechaza las opciones desconocidas (el orden de los `case` importa, semana 2):

   ```python
   case ["-f" | "--archivo", name]:
       source = Path(name)
   case ["-f" | "--archivo", name, "-j" | "--json", summary]:
       source, output = Path(name), Path(summary)
   ```

5. Después del `match`, si `source is not None`, `lines = read_data(source)` dentro de un `try`. Con `except DataFileError as problem:` escribe `f"error: {problem}"` en stderr y devuelve `2`, sin informe.
6. Al final, antes del `return`, si `output is not None`, `write_json(summary_data(records), output)` en otro `try` igual, y después `f"resumen guardado en {output}"`.

```bash
uv run pytest tests/test_main.py
```

Esperado: `20 passed`. Llama a la excepción `problem` y no `error`: `error` ya es la variable del `for` que escribe los errores de línea, y `mypy` avisa de `Trying to read deleted variable "error"`, porque Python borra la variable del `except` al salir de él.

### 10. Rompe archivos a propósito

Las excepciones se entienden viéndolas. Prueba cada caso y comprueba el mensaje y el código de salida:

```bash
uv run observatorio -f no-existe.csv; echo "código: $?"
uv run observatorio -f src; echo "código: $?"
printf 'zona;medida\nNorte;1\n' > /tmp/raro.csv && uv run observatorio -f /tmp/raro.csv; echo "código: $?"
printf 'Pe\361a;1\n' > /tmp/latin1.txt && uv run observatorio -f /tmp/latin1.txt; echo "código: $?"
uv run observatorio -f medidas.csv -j /no-existe/resumen.json; echo "código: $?"
```

Esperado: una línea `error: ...` cada vez y `código: 2`, nunca un *traceback*. En el último, el informe sale entero y el error llega después, al intentar guardar. Fíjate en la línea de la fila inválida: con `-f medidas.csv` dice una posición distinta que con `< medidas.txt`, porque `process_lines` cuenta las líneas que recibe y `read_csv` no le pasa la cabecera.

### 11. Tus tests

En `tests/test_my_storage.py`, sustituye el ejemplo por **al menos 6 tests tuyos** con datos de tu dominio, cada uno con su `tmp_path`, en preparar, actuar y comprobar:

| Qué pruebas | Ejemplo (calidad del aire) |
|---|---|
| `read_csv` con un CSV de tu dominio | Tres estaciones con sus lecturas: salen tres líneas |
| `read_csv` con la cabecera de otro sistema | Una exportación con `estacion;pm25` da `DataFileError` |
| `read_data` con tu archivo real | `read_data(Path("medidas.csv"))` da tantas líneas como filas tiene |
| `summary_data` con tus valores | Con un `NA`, `con_valor` es uno menos que `registros` |
| Ida y vuelta por JSON | Un resumen con tildes en las claves vuelve igual |
| `pytest.raises` con un error tuyo | Un JSON cortado a la mitad da `DataFileError` con su línea |

```bash
uv run pytest
```

Esperado: todo en verde, al menos `210 passed`: los 169 del bootcamp (12 + 17 + 19 + 20 + 20 + 26 + 27 + 28) y los 41 tuyos como mínimo (5 + 6 + 6 + 6 + 6 + 6 + 6 de las semanas 1 a 7).

### 12. En la terminal y en el contenedor

```bash
uv run observatorio -f medidas.csv -j resumen.json; echo "código: $?"
cat resumen.json
uv run --with mypy==2.4.1 mypy src tests
docker compose run --build --rm app
docker compose run --rm app observatorio -f medidas.csv
docker compose run --rm app observatorio -f medidas.csv -j resumen.json; echo "código: $?"
```

El informe es igual en tu máquina y en el contenedor, y `mypy` dice `Success: no issues found`. El último comando termina con `error: no se puede escribir resumen.json` y `código: 2`, y está bien que sea así. En el contenedor eres el usuario `app`, sin permiso para escribir en `/app`, y tu `DataFileError` lo cuenta en una línea en lugar de un *traceback*. En la fase 3 montarás un volumen para guardar resultados fuera del contenedor.

### 13. README, commit y pull request

Añade al `README.md` de tu repositorio:

1. Los comandos nuevos (`-f` y `-j`) y un ejemplo de tu `resumen.json`.
2. Una tabla con los errores que tu programa reconoce, su mensaje y el código de salida.

Haz commits pequeños: uno por función en verde, uno para `medidas.csv` y uno para `main`. Al final:

```bash
git push -u origin week-07
```

En GitHub, abre un *pull request* de `week-07` hacia `main` con:

1. La salida de `uv run pytest` y de `mypy`.
2. Tu `resumen.json`.
3. La salida de dos casos del paso 10 y por qué `raise ... from` es mejor que dejar que salga el error de Python.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ImportError: cannot import name 'read_data'` | `storage.py` no está en `src/observatorio/`: repite el paso 2 |
| `test_read_lines_without_line_breaks` da `['Norte;12,5\n', ...]` | Usaste `file.readlines()` o `list(file)`, que conservan el `\n`: `file.read().splitlines()` |
| `assert None` en `isinstance(caught.value.__cause__, ...)` | Falta `from error` en el `raise` |
| `UnicodeDecodeError` en Windows con tildes | Falta `encoding="utf-8"`: sin él, Python usa la codificación del sistema |
| `test_read_csv_understands_quotes` da `'"Norte";"12,5"'` | Partiste con `split(";")`: usa `csv.reader` |
| `cabecera inesperada ... etiqueta,valor` con tu CSV | Lo guardaste con `,`: el separador es `;` |
| `test_write_json_writes_indented_utf8` da `Peñalara` | Falta `ensure_ascii=False` |
| `TypeError: Object of type ... is not JSON serializable` | Hay algo que JSON no conoce (un `set`, una `Path`): convierte antes a lista o a `str` |
| `Trying to read deleted variable "error"` en `mypy` | Llama `problem` a la excepción en `main`: paso 9 |
| `-f medidas.csv` da el mensaje de uso | Los `case` de `-f` van después del de opciones desconocidas: súbelos |

## Entrega

- Rama `week-07` de `python-<nombre>-<apellido>` con `storage.py`, tu `main` ampliado, tu `medidas.csv` con al menos 12 filas y al menos 6 tests propios en `tests/test_my_storage.py`, todo en verde (también en Docker) y `mypy` sin errores.
- `README.md` del repositorio con los comandos nuevos, un `resumen.json` de ejemplo y la tabla de errores.
- *Pull request* `week-07` → `main` con la descripción del paso 13.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · Context managers](../2-practicas/ejercicio-04-context-managers/README.md) | **Proyecto · Observatorio, capa 6** | [Webgrafía](../4-recursos/webgrafia/README.md) |
