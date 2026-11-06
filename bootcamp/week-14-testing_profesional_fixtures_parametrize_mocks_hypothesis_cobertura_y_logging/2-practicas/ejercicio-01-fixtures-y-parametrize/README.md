# Ejercicio 01 — Fixtures y parametrize

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-fixtures-y-conftest.md) y [02](../../1-teoria/02-parametrize-y-marcas.md)

## Objetivo

Preparar los datos de un test con **fixtures** y probar muchos casos con un solo test:

- una fixture que pides por el nombre del parámetro;
- fixtures que usan otras fixtures, y una nueva en cada test;
- una fixture con `yield`, que limpia al terminar;
- `conftest.py`, para compartir fixtures sin importarlas;
- `parametrize`, con nombres para los casos y un fallo conocido (`xfail`);
- una fixture con `scope="module"`, que se crea una sola vez.

Tu proyecto tendrá su propio `tests/conftest.py` con las fixtures `scale`, `lines`, `series` y `write_file`. Ejercicio **guiado**: descomentas cada paso de `tests/test_readings.py` (y uno de `tests/conftest.py`), ejecutas pytest y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-14-testing_profesional_fixtures_parametrize_mocks_hypothesis_cobertura_y_logging/2-practicas/ejercicio-01-fixtures-y-parametrize/starter
uv run pytest
```

```
============================ no tests ran in 0.05s =============================
```

`readings.py` trae el código que vas a probar: `parse` convierte un texto en lectura, `Station` guarda las lecturas de una estación y `load` lee una estación de un archivo. No lo cambies. En las salidas de abajo, los tiempos (`in 0.05s`) y los porcentajes pueden variar.

## Pasos

### 1. Una fixture

Descomenta el **PASO 1** y ejecuta con `-v`, que escribe un test por línea:

```bash
uv run pytest -v
```

```
tests/test_readings.py::test_mean PASSED                                 [ 50%]
tests/test_readings.py::test_add PASSED                                  [100%]
============================== 2 passed in 0.04s ===============================
```

`station` es una función con `@pytest.fixture`. Nadie la llama: pytest ve que `test_mean` tiene un parámetro llamado `station`, busca la fixture con ese nombre, la ejecuta y le pasa lo que devuelve. Los dos tests usan los mismos datos sin repetirlos.

### 2. Fixtures que usan fixtures

Descomenta el **PASO 2** y ejecuta con `--setup-show`, que enseña cuándo se crea y se destruye cada fixture:

```bash
uv run pytest --setup-show
```

```
        SETUP    F station
        tests/test_readings.py::test_mean (fixtures used: station) .
        TEARDOWN F station
        SETUP    F station
        tests/test_readings.py::test_add (fixtures used: station) .
        TEARDOWN F station
        SETUP    F station
        SETUP    F empty (fixtures used: station)
        tests/test_readings.py::test_empty_has_no_mean (fixtures used: empty, station) .
        TEARDOWN F empty
        TEARDOWN F station
        SETUP    F station
        tests/test_readings.py::test_station_is_new_in_each_test (fixtures used: station) .
        TEARDOWN F station
============================== 4 passed in 0.05s ===============================
```

Mira tres cosas:

- `empty` pide `station`, igual que lo pediría un test, y pytest crea antes `station`.
- La `F` significa *function*: cada test recibe una `station` **nueva**. Por eso `test_add`, que añade una lectura, no estropea `test_station_is_new_in_each_test`, que sigue viendo 3.
- Si los tests compartieran un solo objeto, el resultado dependería del orden en que se ejecutan.

### 3. Una fixture con `yield`

Descomenta el **PASO 3** y ejecuta con `-s`, que deja ver los `print`, y `-k`, que elige los tests cuyo nombre contiene ese texto:

```bash
uv run pytest -s -k first_line
```

```
tests/test_readings.py 
  abierto
.
  cerrado
======================= 1 passed, 4 deselected in 0.06s ========================
```

Lo que va antes del `yield` prepara el test (abre el archivo). Lo que el `yield` entrega es lo que recibe el test. Lo que va después **limpia**, y se ejecuta al terminar el test aunque falle. `tmp_path` es una fixture de pytest: una carpeta nueva y vacía para cada test.

### 4. `conftest.py`

Descomenta el **PASO 4** en `tests/conftest.py` **y** en `tests/test_readings.py`, y ejecuta:

```bash
uv run pytest -v -k load
```

```
tests/test_readings.py::test_load_skips_missing_values PASSED            [100%]
======================= 1 passed, 5 deselected in 0.06s ========================
```

`test_readings.py` usa `sample_file` sin importarla. pytest carga `conftest.py` antes que los tests de su carpeta, y sus fixtures valen en todos ellos. Prueba a ejecutar `uv run pytest --fixtures -q tests/` y busca `sample_file` y `station` en la lista, junto a las de pytest (`tmp_path`, `capsys`, `monkeypatch`, `caplog`...).

### 5. `parametrize`

Descomenta el **PASO 5** y ejecuta:

```bash
uv run pytest -v -k test_parse
```

```
tests/test_readings.py::test_parse[12,5-12.5] PASSED                     [ 20%]
tests/test_readings.py::test_parse[8-8.0] PASSED                         [ 40%]
tests/test_readings.py::test_parse[ 30.5 -30.5] PASSED                   [ 60%]
tests/test_readings.py::test_parse[NA-None] PASSED                       [ 80%]
tests/test_readings.py::test_parse[-None] PASSED                         [100%]
======================= 5 passed, 6 deselected in 0.06s ========================
```

Un test y cinco casos: pytest lo ejecuta una vez por tupla, y cada caso pasa o falla por separado. Entre corchetes va el **id** de cada caso, que pytest compone con los valores. El último, `-None`, es el texto vacío: se lee mal.

### 6. Nombres y un fallo conocido

Descomenta el **PASO 6** y ejecuta:

```bash
uv run pytest -v -k rejects
```

```
tests/test_readings.py::test_parse_rejects[letras] PASSED                [ 33%]
tests/test_readings.py::test_parse_rejects[punto-y-coma] PASSED          [ 66%]
tests/test_readings.py::test_parse_rejects[nan] XFAIL (float acepta nan) [100%]
================= 2 passed, 11 deselected, 1 xfailed in 0.07s ==================
```

`pytest.param(..., id="letras")` da un nombre claro al caso. El tercero lleva `marks=pytest.mark.xfail`: es un fallo **conocido**. `parse("nan")` no lanza `ValueError`, porque `float("nan")` es un número válido para Python, y el test lo apunta como `XFAIL` sin poner la ejecución en rojo. Si algún día `parse` rechaza `"nan"`, saldrá `XPASS`: es la señal de quitar la marca. En tu proyecto, ese bug se corrige esta semana.

### 7. `scope="module"`

Descomenta el **PASO 7** y ejecuta:

```bash
uv run pytest --setup-show -k known
```

```
    SETUP    M stations
        SETUP    F name['Norte']
        tests/test_readings.py::test_known_station[Norte] (fixtures used: name, stations) .
        TEARDOWN F name['Norte']
        SETUP    F name['Sur']
        tests/test_readings.py::test_known_station[Sur] (fixtures used: name, stations) .
        TEARDOWN F name['Sur']
        SETUP    F name['Este']
        tests/test_readings.py::test_known_station[Este] (fixtures used: name, stations) .
        TEARDOWN F name['Este']
    TEARDOWN M stations
======================= 3 passed, 14 deselected in 0.06s ========================
```

La `M` de `stations` es *module*: se crea **una vez** para los tres tests del archivo. Con `-s` verías `creando la lista (cara)` una sola vez. Úsalo para lo que es caro de crear y nadie cambia. Un objeto que los tests modifican, como `station`, debe seguir siendo de función.

Al final, `uv run pytest` da `16 passed, 1 xfailed`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `fixture 'station' not found` | El test pide una fixture que no está descomentada, o el nombre del parámetro no coincide con el de la función |
| `fixture 'sample_file' not found` | Falta descomentar el PASO 4 en `tests/conftest.py`, no solo en el archivo de tests |
| `Fixture "station" called directly` | Llamaste a `station()` dentro de un test. Pídela como parámetro: pytest la llama por ti |
| No salen `abierto` y `cerrado` | Falta `-s`: pytest captura los `print` de los tests que pasan |
| `XPASS(strict)` en rojo | Un test con `xfail(strict=True)` pasó: el fallo ya no existe y la marca sobra |
| `ModuleNotFoundError: No module named 'readings'` | Ejecuta pytest desde `starter/`: `pythonpath = ["."]` de `pyproject.toml` es relativo a esa carpeta |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Cobertura y logging](../../1-teoria/05-cobertura-y-logging.md) | **Ejercicio 01 · Fixtures y parametrize** | [Ejercicio 02 · Hypothesis](../ejercicio-02-hypothesis/README.md) |
