# Ejercicio 02 — Hypothesis

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-hypothesis.md)

## Objetivo

Escribir **tests de propiedades**: en vez de elegir tú los datos, describes qué datos valen y qué debe cumplirse siempre, y Hypothesis busca un contraejemplo.

- una propiedad de ida y vuelta: escribir y leer da lo mismo;
- leer un contraejemplo **encogido** al mínimo;
- decidir si el fallo es del código o de la estrategia;
- encontrar un error de *off-by-one*;
- descubrir los límites de los `float` y declarar el dominio real con `min_value` y `max_value`;
- `@example` y la base de datos de ejemplos.

En tu proyecto, Hypothesis encuentra dos bugs reales de las semanas anteriores. Ejercicio **guiado**: descomentas cada paso de `tests/test_codec.py`, ejecutas pytest y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-14-testing_profesional_fixtures_parametrize_mocks_hypothesis_cobertura_y_logging/2-practicas/ejercicio-02-hypothesis/starter
uv run pytest
```

```
plugins: hypothesis-6.170.8
collected 0 items

============================ no tests ran in 0.05s =============================
```

`plugins: hypothesis-6.170.8`: Hypothesis se instala como plugin de pytest. `codec.py` trae cuatro funciones pequeñas, alguna con un bug. Hypothesis genera datos al azar, así que algunos contraejemplos pueden salirte distintos de los de abajo: el README avisa dónde.

## Pasos

### 1. Una propiedad

Descomenta el **PASO 1** y ejecuta:

```
tests/test_codec.py .                                                    [100%]
============================== 1 passed in 0.72s ===============================
```

Un solo punto, pero `test_value_round_trips` se ha ejecutado **100 veces**, una con cada número que generó `FINITE`: ceros, negativos, decimales larguísimos, números diminutos y enormes. La propiedad es "`from_line` deshace lo que hace `to_line`", y vale para todos.

### 2. Un contraejemplo

Descomenta el **PASO 2** y ejecuta:

```
line = ';;0.0'
...
E       ValueError: too many values to unpack (expected 2, got 3)
E       Failing test case: test_any_label_round_trips(
E           label=';',
E           value=0.0,  # or any other generated value
E       )
codec.py:14: ValueError
...
FAILED tests/test_codec.py::test_any_label_round_trips - ValueError: too many...
========================= 1 failed, 1 passed in 2.20s ==========================
```

Hypothesis encontró una etiqueta que rompe la propiedad, seguramente larga y llena de caracteres raros. Después la **encogió**: probó versiones cada vez más simples que siguieran fallando, hasta `label=';'`. El valor no importa (`# or any other generated value`): con cualquiera falla. El mensaje es la mitad del diagnóstico: una etiqueta con `;` da tres trozos.

### 3. ¿Bug del código o de la estrategia?

Hay dos arreglos posibles: que `to_line` escape el `;`, o que la etiqueta no pueda llevarlo. En tu dominio, una etiqueta nunca lleva `;`: es el separador del formato. La propiedad era demasiado amplia, no el código.

Vuelve a comentar el **PASO 2**, descomenta el **PASO 3** y ejecuta:

```
tests/test_codec.py ..                                                   [100%]
============================== 2 passed in 0.95s ===============================
```

`st.text().filter(...)` descarta los textos con `;`. La estrategia es ahora la **especificación**: dice qué entradas son válidas.

### 4. Un *off-by-one*

Descomenta el **PASO 4** y ejecuta:

```
E         Right contains one more item: 0
...
E       Failing test case: test_chunks_keep_every_item(
E           items=[0],
E           size=1,  # or any other generated value
E       )
...
FAILED tests/test_codec.py::test_chunks_keep_every_item - assert [] == [0]
```

`chunks([0], 1)` debería dar `[[0]]` y da `[]`: pierde elementos. Hypothesis lo encoge a la lista más corta que falla. Mira la línea 20 de `codec.py`:

```python
    return [items[start : start + size] for start in range(0, len(items) - size, size)]
```

El `range` se para `size` posiciones antes de tiempo. Cambia `len(items) - size` por `len(items)` y vuelve a ejecutar: `3 passed`. El bug pierde siempre el último trozo, pero un test a mano que solo mirara el primero, como `chunks([1, 2, 3, 4], 2)[0] == [1, 2]`, no lo habría visto. La propiedad mira la lista entera, para cualquier lista.

### 5. Los límites de los `float`

Descomenta el **PASO 5** y ejecuta. Lo más probable es que veas esto:

```
E        +  where inf = mean([8.988465674311579e+307, 8.98846567431158e+307])
...
E       Failing test case: test_mean_is_between_min_and_max(
E           values=[8.988465674311579e+307, 8.98846567431158e+307],
E       )
```

Es un **desbordamiento**: la suma de dos números enormes pasa del máximo de un `float` (`1.8e308`) y da `inf`, que es mayor que el máximo de la lista. El contraejemplo puede cambiar de una ejecución a otra:

- dos números enormes y negativos, cuya suma da `-inf`;
- más rara vez, números como `5e16`, donde `sum(values) / len(values)` se pasa del máximo por **redondeo**.

Ninguno de los dos es un bug de `mean` para tus datos: ninguna estación mide `1e307`. Es un aviso de que la propiedad pide más de lo que los `float` garantizan.

### 6. El dominio real y `@example`

Vuelve a comentar el **PASO 5**, descomenta el **PASO 6** y ejecuta:

```
tests/test_codec.py ....                                                 [100%]
============================== 4 passed in 1.72s ===============================
```

`READINGS` describe tus datos de verdad: lecturas entre 0 y 1000. El margen de `1e-9` acepta el redondeo de la división. `@example([12.5])` añade un caso que se prueba **siempre**, además de los generados. Úsalo para un caso que un día falló o que quieres ver probado en cada ejecución.

Por último, descomenta otra vez el **PASO 2** y ejecuta dos veces. La segunda falla al instante con el mismo `label=';'`: Hypothesis guardó el contraejemplo en la carpeta `.hypothesis/` y lo prueba primero. En un proyecto, `.hypothesis/` va al `.gitignore`. Vuelve a comentar el PASO 2.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'hypothesis'` | Ejecuta con `uv run pytest` desde `starter/`: Hypothesis está en el grupo `dev` de su `pyproject.toml` |
| Tu contraejemplo no es el del README | En los pasos 2 y 4 debería coincidir. En el 5 puede cambiar de una ejecución a otra: lo que importa es la causa |
| `FailedHealthCheck` ... `filter` | El filtro descarta casi todo lo que genera la estrategia. Genera directamente lo que quieres (`min_size`, `alphabet`...) en vez de filtrar |
| `FailedHealthCheck` ... `function_scoped_fixture` | Un test con `@given` pide una fixture de función: se crearía una sola vez para los 100 ejemplos. Crea los datos dentro del test |
| Siguen fallando pasos ya resueltos | Comenta otra vez el PASO 2 (paso 3) y el PASO 5 (paso 6): muestran un fallo, no son para dejarlos |
| `Flaky` | El test dio resultados distintos con el mismo dato: depende de algo de fuera (la hora, el azar, un archivo) |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Fixtures y parametrize](../ejercicio-01-fixtures-y-parametrize/README.md) | **Ejercicio 02 · Hypothesis** | [Ejercicio 03 · Mocks](../ejercicio-03-mocks/README.md) |
