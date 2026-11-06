# Proyecto — Observatorio, capa 8: el modelo como clases

⏱️ 6 h 30 min · Capa 8 del [proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md). **Único entregable de la semana.**

## Qué construyes

Desde la semana 5, una medida es una tupla, `("Norte", 12.5)`, y la unidad y los umbrales viajan sueltos de función en función. Esta semana el Observatorio gana un **modelo**: tres *dataclasses* en un módulo nuevo, `core/model.py`.

| Clase | Qué es | Opciones | Qué aporta |
|---|---|---|---|
| `Scale(unit, low, high)` | La unidad y los dos umbrales | `frozen=True, slots=True` | Rechaza unos umbrales imposibles al crearse; `level(value)` y `row(measurement)` |
| `Measurement(label, value)` | Una medida | `frozen=True, slots=True` | `measurement.value` en lugar de `record[1]`; `Measurement.from_line(línea)`; `has_value` |
| `Series(measurements)` | Las medidas de una entrada, en orden | `slots=True` | `Series.from_lines(líneas)`, `add`, y los análisis como métodos: `values()`, `labels()`, `means()`, `most_common(n)` |

Las funciones de las capas 0 a 7 **no cambian**: los métodos las llaman. `main` pasa a usar `SCALE = Scale(UNIT, LOW, HIGH)` y una `Series` en lugar de la lista de tuplas, y la versión sube a `0.9.0`. El informe es **idéntico** al de la semana 8: los tests de `main` lo vigilan.

```
src/observatorio/core/
├── __init__.py      # + Measurement, Scale y Series en la API pública
├── model.py         # nuevo: las tres dataclasses
└── ...              # los siete módulos de siempre, sin cambios
```

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-09`. El `starter/` trae la capa 7 resuelta; **tú escribes `model.py`** y amplías tu `__main__.py`.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-08` está fusionado en `main`. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-09
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-09-clases_y_dataclasses/3-proyecto/starter
cp $STARTER/tests/test_model.py $STARTER/tests/test_my_model.py tests/
cp $STARTER/tests/test_package.py $STARTER/tests/test_main.py tests/
sed -i 's/week-08/week-09/' compose.yaml
git status --short
```

Nuevos: `tests/test_model.py` (29 tests) y `tests/test_my_model.py` (un ejemplo). Modificados: `test_package.py`, que ahora espera el módulo `model`, las tres clases en `__all__` y la versión `0.9.0`; `test_main.py`, que solo cambia la versión esperada; y `compose.yaml`.

### 3. Tests en rojo

```bash
uv run pytest
```

```
E   ImportError: cannot import name 'Measurement' from 'observatorio.core' (.../src/observatorio/core/__init__.py)
E   ImportError: cannot import name 'Measurement' from 'observatorio.core' (.../src/observatorio/core/__init__.py)
E   ImportError: cannot import name 'model' from 'observatorio.core' (.../src/observatorio/core/__init__.py)
!!!!!!!!!!!!!!!!!!! Interrupted: 3 errors during collection !!!!!!!!!!!!!!!!!!!
```

Como en la semana 8, tres archivos de tests no se pueden ni importar. Abre `tests/test_model.py` y léelo entero antes de escribir nada: es la especificación de las tres clases. Fíjate en `test_main_builds_its_scale_from_its_constants`, que usa `getattr(entry, "SCALE", None)` en lugar de `from observatorio.__main__ import SCALE`. Si importara `SCALE` y aún no existiera, fallaría la colección del archivo entero; así falla solo ese test.

### 4. El esqueleto del modelo

Crea `src/observatorio/core/model.py` solo con los campos:

```python
"""El modelo del Observatorio: la escala, la medida y la serie, como clases."""

from dataclasses import dataclass, field


@dataclass
class Scale:
    unit: str
    low: float
    high: float


@dataclass
class Measurement:
    label: str
    value: float | None


@dataclass
class Series:
    measurements: list[Measurement] = field(default_factory=list)
```

Y expónlas en la API pública: en `core/__init__.py`, añade `from observatorio.core.model import Measurement, Scale, Series` y los tres nombres a `__all__`. `uv run ruff check --fix` los coloca en su sitio (regla `RUF022`, semana 8).

```bash
uv run pytest -q
```

```
29 failed, 191 passed
```

Ya se importa todo. Fallan los que piden lo que aún no has escrito: validación, inmutabilidad, métodos y la versión. Los que pasan ya te dicen algo: `test_scale_repr_is_generated` y `test_measurement_fields_and_repr` pasan sin que hayas escrito ningún `__repr__`. Lo escribió `@dataclass`.

### 5. Inmutables y con `slots`

`Scale` y `Measurement` son **valores**: no cambian después de crearse. `Series` va acumulando medidas. Cambia los decoradores:

```python
@dataclass(frozen=True, slots=True)
class Scale: ...

@dataclass(frozen=True, slots=True)
class Measurement: ...

@dataclass(slots=True)
class Series: ...
```

```
25 failed, 195 passed
```

Pasan los cuatro tests de inmutabilidad, *hash* y `slots`. `test_measurements_are_hashable` mete tres medidas en un `set` y se queda con dos: dos medidas iguales tienen el mismo *hash* (teoría 04).

### 6. La escala se valida al crearse

Añade a `Scale` un `__post_init__` que lance `ValueError` si `low` no es menor que `high`, con un mensaje que empiece por `umbrales imposibles`:

```python
    def __post_init__(self) -> None:
        if self.low >= self.high:
            raise ValueError(
                f"umbrales imposibles: low ({self.low}) debe ser menor que high ({self.high})"
            )
```

```
23 failed, 197 passed
```

### 7. Los métodos de `Scale`

Dos métodos que **llaman** a funciones que ya tienes, sin copiar su lógica:

- `level(self, value: float | None) -> str`: el nivel de `value` con `classify` y los umbrales de la escala.
- `row(self, measurement: Measurement) -> str`: la fila de `format_row` con la etiqueta, el valor, la unidad y el nivel de la medida.

Importa `classify` y `format_row` de `observatorio.core.rules`. `row` recibe una `Measurement`, que se define **después** de `Scale` en el archivo: desde Python 3.14 puedes escribir el tipo sin comillas (teoría 02).

```
17 failed, 203 passed
```

### 8. Los métodos de `Measurement`

- `@classmethod from_line(cls, line: str) -> Measurement | None`: usa `parse_record` (de `observatorio.core.groups`); si da `None`, devuelve `None`; si no, `cls(*record)`.
- `@property has_value -> bool`: `True` si el valor no es `None`.

```
12 failed, 208 passed
```

`from_line` es un **constructor alternativo**, como `Thermometer.from_fahrenheit` del ejercicio 02. Las reglas de qué es una línea válida siguen en un solo sitio, `parse_record`, con sus tests de la semana 5.

### 9. Los métodos de `Series`

| Miembro | Qué hace | Reutiliza |
|---|---|---|
| `@classmethod from_lines(cls, lines)` | La serie de las líneas válidas | `records_of` |
| `add(self, measurement) -> None` | Añade al final | `list.append` |
| `@property records -> list[Record]` | Las medidas como tuplas `(etiqueta, valor)` | — |
| `values(self) -> list[float]` | Los valores que no son `None` | `values_of(self.records)` |
| `labels(self) -> set[str]` | Las etiquetas distintas | `distinct_labels` |
| `means(self) -> dict[str, float]` | La media de cada etiqueta | `label_means(values_by_label(...))` |
| `most_common(self, n) -> list[tuple[str, int]]` | Las `n` etiquetas más repetidas | `most_common_labels` |

`records` es el puente: traduce las medidas al formato de tuplas que esperan las funciones de las capas 4 a 6, y cada método queda en una línea. `from_lines` aplica `Measurement(label, value)` a cada tupla de `records_of`.

```
4 failed, 216 passed
```

`test_empty_series_do_not_share_their_list` pasa gracias a `field(default_factory=list)`. Prueba a cambiarlo por `= []`: la clase ni siquiera se crea (`ValueError: mutable default <class 'list'> for field measurements is not allowed: use default_factory`). Vuelve a dejarlo como estaba.

### 10. La versión

```bash
uv version --bump minor
```

```
observatorio 0.8.0 => 0.9.0
```

`uv version` cambia `pyproject.toml` y actualiza `uv.lock` a la vez (semana 8). Añadir clases sin romper nada sube el número **menor**.

```
1 failed, 219 passed
```

### 11. `main` usa el modelo

Queda `test_main_builds_its_scale_from_its_constants`. En tu `__main__.py`:

1. Debajo de `UNIT`, `LOW` y `HIGH`, crea `SCALE = Scale(UNIT, LOW, HIGH)`. **No** borres las tres constantes: los tests de `main` las importan.
2. Usa `SCALE.unit`, `SCALE.low` y `SCALE.high` donde usabas `UNIT`, `LOW` y `HIGH`.
3. Sustituye `records = records_of(lines)` por `series = Series.from_lines(lines)`, y cada función que recibía `records` por el método de la serie: `series.labels()`, `series.means()`, `series.most_common(TOP)`, `series.values()` y `summary_data(series.records)`.
4. Quita de los imports las funciones que ya no usa `main`. `uv run ruff check` te dice cuáles (`F401`).

```bash
uv run pytest -q
uv run observatorio -f medidas.csv
```

```
220 passed
```

El informe es el mismo de la semana 8, carácter a carácter. Ahora prueba la validación: cambia `LOW` a un valor mayor que `HIGH` y ejecuta `uv run observatorio --version`.

```
  File ".../src/observatorio/__main__.py", line 39, in <module>
    SCALE = Scale(UNIT, LOW, HIGH)
  File "<string>", line 6, in __init__
  File ".../src/observatorio/core/model.py", line 41, in __post_init__
    raise ValueError(
ValueError: umbrales imposibles: low (60.0) debe ser menor que high (50.0)
```

Falla **al arrancar**, antes de leer ninguna línea: `SCALE` se crea al importar `__main__.py`. Fíjate en `File "<string>", line 6, in __init__`: es el `__init__` que escribió `@dataclass`, que no tiene archivo. Tus números de línea pueden ser otros. Vuelve a dejar `LOW` como estaba.

### 12. Tus tests

En `tests/test_my_model.py`, sustituye el ejemplo por **al menos 6 tests tuyos** con datos de tu dominio, importando solo de `observatorio.core`:

| Qué pruebas | Ejemplo (calidad del aire) |
|---|---|
| Tu escala | `Scale` con tu unidad y tus umbrales clasifica bien un valor justo en cada umbral |
| Escala imposible | Tus umbrales al revés lanzan `ValueError` |
| Una línea de tu dominio | `Measurement.from_line` con coma decimal y con tu marca de dato faltante |
| Una serie | `Series.from_lines` con un archivo pequeño en `tmp_path`, leído con `read_data` |
| Medias | `series.means()` con dos estaciones calculadas a mano |
| `replace` | `dataclasses.replace(medida, value=...)` crea otra medida y deja igual la original |

```bash
uv run pytest
uv run ruff check && uv run ruff format --check && uv run mypy
```

Esperado: todo en verde, al menos `267 passed`. Son los 214 del bootcamp (12 + 17 + 19 + 20 + 26 + 27 + 28 + 24 + 12 + 29) más los 53 tuyos como mínimo (5 + 6 + 6 + 6 + 6 + 6 + 6 + 6 + 6, de las semanas 1 a 9).

### 13. En el contenedor

```bash
docker compose run --build --rm app
docker compose run --rm app observatorio --version
```

Los tests en verde y `observatorio 0.9.0`.

### 14. README, commit y pull request

En el `README.md` de tu repositorio, añade `model.py` al árbol del paquete y una frase sobre cada clase.

Commits sugeridos, en este orden: `feat: add model dataclasses`, `feat: freeze value classes and use slots`, `feat: validate scale thresholds`, `feat: add scale and measurement methods`, `feat: add series methods`, `chore: bump version to 0.9.0`, `refactor: use model in main` y `test: add model tests`. Al final:

```bash
git push -u origin week-09
```

En GitHub, abre un *pull request* de `week-09` hacia `main` con:

1. La salida de `uv run pytest`, `uv run mypy` y `uv run ruff check`.
2. Tu `Scale` con tu unidad y tus umbrales, y el error que da con los umbrales al revés.
3. Por qué `Measurement` es `frozen` y `Series` no.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ImportError: cannot import name 'Measurement' from 'observatorio.core'` | Falta el import de `model` en `core/__init__.py` (paso 4) |
| `test_every_module_lives_in_core` falla | `model.py` no está en `src/observatorio/core/` |
| `ValueError: mutable default <class 'list'> for field measurements is not allowed: use default_factory` | Escribiste `= []`: usa `field(default_factory=list)` |
| `TypeError: non-default argument ...` | En una *dataclass*, los campos sin valor por defecto van primero |
| `FrozenInstanceError` en tu código | Intentas cambiar una medida o la escala: crea otra con `dataclasses.replace` |
| `test_model_classes_use_slots` falla | Falta `slots=True` en `Measurement` o en `Series` |
| `NameError: name 'Measurement' is not defined` al importar | Python anterior a 3.14 en tu `.venv`: `uv run python --version` debe decir 3.14 |
| `test_main_builds_its_scale_from_its_constants` falla | `SCALE` no existe en `__main__.py`, o no se crea con `UNIT`, `LOW` y `HIGH` |
| `F401 ... imported but unused` en `__main__.py` | Quedan imports de funciones que ahora usa la serie: `uv run ruff check --fix` |
| Los tests de `main` fallan tras el paso 11 | El informe cambió: compara tu salida con la de antes (`git stash`, ejecuta, `git stash pop`) |
| `mypy`: `"Series" has no attribute ...` | El método tiene otro nombre en tu clase: usa los de la tabla del paso 9 |

## Entrega

- Rama `week-09` de `python-<nombre>-<apellido>` con `core/model.py` (`Scale`, `Measurement` y `Series`), las tres clases en la API pública, `main` usando `SCALE` y `Series`, la versión `0.9.0` y al menos 6 tests propios en `tests/test_my_model.py`. Todo en verde (también en Docker), con `ruff check`, `ruff format --check` y `mypy` sin avisos.
- `README.md` del repositorio con `model.py` en el árbol del paquete.
- *Pull request* `week-09` → `main` con la descripción del paso 14.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · Elegir el modelo](../2-practicas/ejercicio-04-elegir-el-modelo/README.md) | **Proyecto · Observatorio, capa 8** | [Webgrafía](../4-recursos/webgrafia/README.md) |
