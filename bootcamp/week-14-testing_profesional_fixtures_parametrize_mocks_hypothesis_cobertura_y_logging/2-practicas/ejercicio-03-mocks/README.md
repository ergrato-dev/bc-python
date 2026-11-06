# Ejercicio 03 — Mocks

⏱️ 1 h · Teoría previa: [04](../../1-teoria/04-mocks-y-dobles.md)

## Objetivo

Probar código que habla con algo que no controlas, como una red o el reloj, sustituyéndolo en el test por un **doble**:

- un `Mock`, que apunta cada llamada y devuelve lo que le digas;
- `patch`, que cambia un nombre mientras dura un `with`, y **dónde** hay que parchear;
- `side_effect`, para simular un fallo;
- congelar la hora;
- `create_autospec`, un doble que respeta la firma del original;
- `monkeypatch` con una función normal, la alternativa sin `Mock`.

En tu proyecto, un mock simula un archivo sin permiso de lectura y destapa un bug de la semana 7. Ejercicio **guiado**: descomentas cada paso de `tests/test_weather.py`, ejecutas pytest y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-14-testing_profesional_fixtures_parametrize_mocks_hypothesis_cobertura_y_logging/2-practicas/ejercicio-03-mocks/starter
uv run pytest
```

```
============================ no tests ran in 0.05s =============================
```

`weather.py` pide la última lectura de una estación a un servicio web (`fetch_reading`) y escribe la hora actual junto a un valor (`stamp`). El servicio, `observatorio.invalid`, no existe: los dominios `.invalid` están reservados y nunca resuelven. Un test no debe depender de la red ni de la hora: sería lento, frágil y distinto cada vez.

## Pasos

### 1. Un `Mock`

Descomenta el **PASO 1** y ejecuta `uv run pytest -v`:

```
tests/test_weather.py::test_a_mock_records_its_calls PASSED              [100%]
```

Un `Mock` acepta cualquier llamada y devuelve su `return_value`. Además apunta cómo lo llamaron: `assert_called_once_with("Norte")` falla si lo llamaron dos veces o con otros argumentos. Y se **inventa** cualquier atributo que le pidas: `fake.anything.at_all()` es otro `Mock`. Eso lo hace cómodo y peligroso a la vez: un `Mock` nunca se queja.

### 2. `patch`

Descomenta el **PASO 2** y ejecuta:

```
tests/test_weather.py::test_fetch_reading_with_a_fake_service PASSED     [100%]
```

Mientras dura el `with`, `weather.urlopen` es un `Mock` que devuelve `response(...)`, un `BytesIO` que se lee como la respuesta real. `fetch_reading` no sabe que no hay red. Al salir del `with`, `patch` deja el `urlopen` de verdad. Después, el test comprueba **cómo** se llamó: la URL y el `timeout`.

### 3. Dónde se parchea

Descomenta el **PASO 3** y ejecuta. Puede tardar unos segundos, hasta 20 en algunas redes:

```
tests/test_weather.py::test_patching_the_wrong_name_does_nothing PASSED  [100%]
```

Pasa, pero por la razón equivocada: este test **espera** el fallo. Parchea `urllib.request.urlopen`, y `weather.py` no usa ese nombre: hizo `from urllib.request import urlopen` y tiene su **propio** nombre `urlopen`, que sigue apuntando a la función real. La petición sale de verdad, el nombre no resuelve y llega `ReadingError`. Por eso tarda.

La regla: **parchea donde se usa, no donde se define**. Aquí, `"weather.urlopen"`. Vuelve a comentar el PASO 3: ningún test de verdad debe tocar la red.

### 4. `side_effect`

Descomenta el **PASO 4** y ejecuta:

```
tests/test_weather.py::test_fetch_reading_when_the_service_is_down PASSED [100%]
```

Con `side_effect=URLError("sin red")`, el doble **lanza** la excepción en lugar de devolver algo. Es la única forma razonable de probar el `except URLError` de `fetch_reading`: no puedes tumbar internet para un test. Además, el test comprueba que la excepción original queda en `__cause__` (`raise ... from error`).

### 5. Congelar la hora

Descomenta el **PASO 5** y ejecuta:

```
tests/test_weather.py::test_stamp_uses_the_current_time PASSED           [100%]
```

`datetime.now` no se puede parchear directamente, porque `datetime` es un tipo de C y no deja cambiar sus atributos. Por eso se parchea el nombre `datetime` **de `weather`** entero, y se le dice qué devuelve `now`. El test da lo mismo a las 3 de la tarde y a las 3 de la madrugada.

### 6. `autospec`

Descomenta el **PASO 6** y ejecuta:

```
tests/test_weather.py::test_autospec_checks_the_arguments PASSED         [100%]
```

`loose("Norte", "Sur", 3)` funciona aunque `fetch_reading` solo acepte un argumento: un `Mock` normal no sabe nada del original. `create_autospec(fetch_reading)` copia su firma y lanza `TypeError` con una llamada que la función real no aceptaría. Con `patch(..., autospec=True)` consigues lo mismo. Si mañana cambias la firma de la función, el test con `autospec` fallará; el `Mock` normal seguiría pasando.

### 7. `monkeypatch`

Descomenta el **PASO 7** y ejecuta:

```
tests/test_weather.py::test_fetch_reading_with_monkeypatch PASSED        [100%]
```

Lo mismo que el paso 2, sin `Mock`: una función normal con la firma de `urlopen`, que guarda las URLs en una lista. `monkeypatch.setattr` deshace el cambio al terminar el test, como `patch`. Para un doble sencillo es más fácil de leer; `Mock` compensa cuando necesitas `side_effect`, contar llamadas o `autospec`.

Al final, `uv run pytest` da `6 passed`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| Un test tarda segundos y da `ReadingError` | El parche no llega: parcheaste `urllib.request.urlopen`. Usa `"weather.urlopen"` |
| `TypeError: cannot set 'now' attribute of immutable type 'datetime.datetime'` | Intentaste parchear `datetime.now`. Parchea `"weather.datetime"` |
| `AttributeError: 'assert_called_once_wiht' is not a valid assertion` | Un error de tecleo en un `assert_*`. Python lo detecta porque empieza por `assert` |
| `json.decoder.JSONDecodeError` | El texto de `response(...)` no es JSON válido: revisa las comillas |
| `ModuleNotFoundError: No module named 'weather'` | Ejecuta pytest desde `starter/` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Hypothesis](../ejercicio-02-hypothesis/README.md) | **Ejercicio 03 · Mocks** | [Ejercicio 04 · Cobertura y logging](../ejercicio-04-cobertura-y-logging/README.md) |
