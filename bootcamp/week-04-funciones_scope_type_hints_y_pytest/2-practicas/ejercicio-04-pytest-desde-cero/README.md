# Ejercicio 04 — `pytest` desde cero

⏱️ 2 h · Teoría previa: [05](../../1-teoria/05-tests-con-pytest.md)

## Objetivo

Hasta ahora usaste tests que venían escritos. Aquí los lees uno a uno, ves cómo pytest informa de un fallo y encuentras con ellos **dos errores** escondidos en `temperature.py`. Practicas `assert`, `pytest.approx`, `pytest.raises`, `parametrize` y las opciones `-v`, `-k`, `-x` y `--lf`. Ejercicio **guiado**: descomentas cada paso de `tests/test_temperature.py`. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-04-funciones_scope_type_hints_y_pytest/2-practicas/ejercicio-04-pytest-desde-cero/starter
cat temperature.py
uv run pytest; echo "código: $?"
```

```
============================ no tests ran in 0.04s =============================
código: 5
```

pytest encontró el archivo de tests, pero ninguna función `test_*`: todas están comentadas. El código `5` significa "no había tests", distinto de `0` (todo en verde) y de `1` (algún test falló). En el CI de la semana 21, un `5` también es un fallo.

## Pasos

### 1. El primer test

Descomenta el **PASO 1** en `tests/test_temperature.py` y ejecuta `uv run pytest`:

```
tests/test_temperature.py .                                              [100%]

============================== 1 passed in 0.01s ===============================
```

Cada `.` es un test que pasó. pytest busca archivos `test_*.py`, dentro de ellos funciones `test_*`, las llama y mira si algún `assert` falla. No hay que registrar nada.

### 2. Leer un fallo

Descomenta el **PASO 2** y ejecuta:

```
tests/test_temperature.py .F                                             [100%]
...
>       assert celsius_to_fahrenheit(36.6) == 97.88
E       assert 97.88000000000001 == 97.88
E        +  where 97.88000000000001 = celsius_to_fahrenheit(36.6)
...
FAILED tests/test_temperature.py::test_body_temperature - assert 97.880000000...
========================= 1 failed, 1 passed in 0.05s ==========================
```

| Parte | Qué dice |
|---|---|
| `F` | Ese test falló |
| `>` | La línea del `assert` que falló |
| `E       assert 97.88000000000001 == 97.88` | Los dos valores que comparó |
| `+  where ...` | De dónde salió el primero |

La función está bien: `36.6` no se puede guardar exacto en binario (semana 1) y el resultado arrastra un error diminuto. Para decimales, compara con tolerancia: cambia `== 97.88` por `== pytest.approx(97.88)` y ejecuta: `2 passed`.

### 3. Probar que algo falla

Descomenta el **PASO 3**:

```
4 passed
```

`pytest.raises(ValueError, match="vacía")` pasa solo si el bloque lanza `ValueError` y el mensaje contiene `"vacía"`. Comprueba que el test sirve: en `temperature.py`, comenta las dos líneas del `if len(values) == 0:` y ejecuta. Falla con `ZeroDivisionError`: pytest esperaba un `ValueError` y recibió otro error. Descomenta las dos líneas.

### 4. Los límites

Descomenta el **PASO 4** y ejecuta con `-v` para ver cada caso:

```bash
uv run pytest -v -k classify
```

```
tests/test_temperature.py::test_classify_temperature[14.9-fr\xedo] PASSED
tests/test_temperature.py::test_classify_temperature[15.0-templado] PASSED
tests/test_temperature.py::test_classify_temperature[24.9-templado] PASSED
tests/test_temperature.py::test_classify_temperature[25.0-calor] FAILED
tests/test_temperature.py::test_classify_temperature[-3.0-fr\xedo] PASSED
...
E       AssertionError: assert 'templado' == 'calor'
```

`-k classify` ejecuta solo los tests cuyo nombre contiene `classify`; `fr\xedo` es cómo escribe pytest la `í` en el nombre de un caso. **Primer error encontrado**: la docstring dice "calor" desde 25, y el código usa `celsius <= 25`. Arréglalo en `temperature.py` (`celsius < 25`) y ejecuta `uv run pytest`: todo en verde.

Sin el caso `25.0`, el error habría pasado: nadie prueba "25" si no piensa en el límite.

### 5. Preparar, actuar, comprobar

Descomenta el **PASO 5** y ejecuta:

```
E       ValueError: could not convert string to float: '21.5 °C'
temperature.py:30: ValueError
...
1 failed, 10 passed
```

**Segundo error**: `parse_celsius(" 21,5 °C ")` no funciona. El traceback baja hasta `temperature.py:30`: `removesuffix("°C")` se aplica antes de `strip()`, y con el espacio final el texto no termina en `"°C"`. Arréglalo: `text.strip().removesuffix("°C").strip()`.

Ahora prueba las opciones para cuando hay muchos tests:

```bash
uv run pytest --lf
uv run pytest -x
```

| Opción | Qué hace |
|---|---|
| `--lf` | *Last failed*: solo los tests que fallaron la última vez; si no falló ninguno, todos |
| `-x` | Para en el primer fallo |
| `-v` | Una línea por test, con su nombre |
| `-k texto` | Solo los tests cuyo nombre contiene `texto` |

Resultado final: `11 passed`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'temperature'` | Ejecuta desde la carpeta `starter`; `pythonpath = ["."]` del `pyproject.toml` lo resuelve desde ahí |
| `no tests ran` aunque descomentaste | El nombre de la función no empieza por `test_`, o quedó con sangría dentro de otra |
| `NameError: name 'pytest' is not defined` | Borraste el `import pytest` del principio |
| `Failed: DID NOT RAISE ValueError` | El bloque del `with pytest.raises` no lanzó el error: la función no valida lo que debería |
| `--lf` ejecuta todo | No había fallos guardados: es lo esperado |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Type hints](../ejercicio-03-type-hints/README.md) | **Ejercicio 04 · pytest desde cero** | [Proyecto · Observatorio, capa 3](../../3-proyecto/README.md) |
