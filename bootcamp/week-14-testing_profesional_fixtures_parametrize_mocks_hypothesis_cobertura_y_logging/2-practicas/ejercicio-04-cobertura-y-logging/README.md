# Ejercicio 04 — Cobertura y logging

⏱️ 1 h 30 min · Teoría previa: [05](../../1-teoria/05-cobertura-y-logging.md)

## Objetivo

Medir qué código ejecutan tus tests y dejar un registro de lo que hace el programa:

- `coverage run` y `coverage report`: qué líneas no ejecutó ningún test;
- la cobertura de **ramas**, que encuentra un `if` probado por un solo lado;
- `--fail-under`, que pone en rojo una cobertura baja;
- un logger por módulo, que nadie ha configurado;
- `logging.basicConfig` en el programa: nivel y formato;
- `caplog`, para probar lo que se registra.

Tu proyecto mide su cobertura con `fail_under = 95` y registra en DEBUG las líneas que descarta. Ejercicio **guiado**: descomentas cada paso de `tests/test_alerts.py` y de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-14-testing_profesional_fixtures_parametrize_mocks_hypothesis_cobertura_y_logging/2-practicas/ejercicio-04-cobertura-y-logging/starter
uv run python main.py
uv run pytest
```

```
Ejercicio 04 · Cobertura y logging
============================ no tests ran in 0.05s =============================
```

`alerts.py` clasifica valores por nivel (`level`), los cuenta (`summary`) y los describe en una línea (`describe`). Registra un WARNING por cada valor alto y un INFO al terminar `summary`.

## Pasos

### 1. El primer informe

Descomenta el **PASO 1** en `tests/test_alerts.py`. Esta vez no ejecutas pytest directamente: `coverage run` lo ejecuta y apunta cada línea que se ejecuta. Después, `coverage report` resume:

```bash
uv run coverage run -m pytest -q
uv run coverage report
```

```
1 passed in 0.01s
Name        Stmts   Miss  Cover   Missing
-----------------------------------------
alerts.py      23     14    39%   12, 14, 16-17, 23-28, 33-36
-----------------------------------------
TOTAL          23     14    39%
```

`Stmts` son las sentencias de `alerts.py`, y `Miss` las que no se ejecutaron. `Missing` dice **cuáles**: la 12 es el `return "sin dato"`, la 14 el `return "bajo"`... `summary` y `describe` no se ejecutaron nunca. Las líneas `def` y los `import` sí cuentan como ejecutadas: corren al importar el módulo.

`coverage run` guarda los datos en un archivo `.coverage`. En un proyecto va al `.gitignore`.

### 2. Cien por cien... de líneas

Descomenta el **PASO 2** y repite los dos comandos:

```
6 passed in 0.02s
Name        Stmts   Miss  Cover   Missing
-----------------------------------------
alerts.py      23      0   100%
-----------------------------------------
TOTAL          23      0   100%
```

Todas las líneas se ejecutaron. Pero mira `describe`: el único test que la llama tiene un valor `alto`. Nadie ha probado el caso sin `alto`, en el que el `if` no entra.

### 3. Ramas

En `pyproject.toml`, descomenta la línea `# branch = true` de `[tool.coverage.run]` y repite los comandos:

```
Name        Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------
alerts.py      23      0     10      1    97%   34->36
-------------------------------------------------------
TOTAL          23      0     10      1    97%
```

Con `branch = true`, coverage mira también las **ramas**: cada `if` puede seguir por dos caminos. `Branch` cuenta los caminos y `BrPart` las decisiones que solo tomaron uno. `34->36` dice qué camino falta: de la línea 34 (`if "alto" in counts:`) a la 36 (`return text`) sin pasar por la 35. Es el caso sin `alto`.

Pídele un mínimo:

```bash
uv run coverage report --fail-under=100
echo $?
```

```
...
Coverage failure: total of 97 is less than fail-under=100
2
```

El código de salida `2` pone en rojo un CI (lo verás en la semana 21). Descomenta el **PASO 3**, repite `coverage run` y `coverage report --fail-under=100`: `100%` y código `0`.

El 100 % no significa que el código esté bien: solo que cada línea y cada rama se ejecutó en algún test. Un test sin `assert` también cubre líneas.

### 4. Un logger sin configurar

Descomenta el **PASO 4** en `main.py` y ejecuta:

```bash
uv run python main.py
```

```
Ejercicio 04 · Cobertura y logging
valor alto: 61.0
alto: 1, bajo: 1, medio: 1, sin dato: 1 (¡atención!)
```

`alerts.py` escribe en su logger, `logging.getLogger(__name__)`, que se llama `alerts`. Nadie lo ha configurado, así que Python usa su **último recurso**: escribe en stderr los mensajes de WARNING o más, sin nivel ni nombre. El INFO de `summary` no sale. `valor alto` va a stderr, no a stdout: con `uv run python main.py 2> /dev/null` desaparece.

### 5. `basicConfig`

Descomenta el **PASO 5**, al principio de `main.py`, y ejecuta:

```
Ejercicio 04 · Cobertura y logging
WARNING alerts: valor alto: 61.0
INFO alerts: 4 valores clasificados
alto: 1, bajo: 1, medio: 1, sin dato: 1 (¡atención!)
```

`logging.basicConfig` configura el logger raíz, del que cuelgan todos: el nivel (`INFO` y más) y el formato (`%(levelname)s %(name)s: %(message)s`). Lo hace `main.py`, el **programa**, no `alerts.py`, la **biblioteca**: quien usa `alerts` decide qué quiere ver y dónde.

### 6. `caplog`

Descomenta el **PASO 6** en `tests/test_alerts.py` y ejecuta:

```bash
uv run pytest -v -k logs
```

```
tests/test_alerts.py::test_level_logs_a_warning_for_alto PASSED          [ 50%]
tests/test_alerts.py::test_summary_logs_info_only_when_asked PASSED      [100%]
```

`caplog` captura los registros del test: `caplog.messages` con el texto y `caplog.records` con todo, nivel y nombre del logger incluidos. El segundo test muestra que, por defecto, el INFO no se registra. `caplog.set_level(logging.INFO, logger="alerts")` lo activa solo para ese test, y pytest lo deshace al terminar.

Al final, `uv run pytest` da `9 passed`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `No data to report.` | Ejecuta antes `uv run coverage run -m pytest`: `report` lee el archivo `.coverage` que crea `run` |
| El informe no tiene las columnas `Branch` y `BrPart` | Falta descomentar `branch = true` en `pyproject.toml`, o no repetiste `coverage run` después |
| `alerts.py` sale con 0 % | Ejecutaste `uv run pytest` en vez de `uv run coverage run -m pytest` |
| No sale nada de registro con `basicConfig` | `basicConfig` debe ejecutarse antes del primer mensaje. Si ya hay un manejador configurado, no hace nada |
| `caplog.messages` vacío con un INFO | El nivel por defecto es WARNING: falta `caplog.set_level(logging.INFO, logger="alerts")` |
| Los mensajes de registro salen antes que el título | Rediriges la salida (a un archivo, a `less`): stdout se acumula en un búfer y stderr se escribe al momento. En la terminal salen en orden |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Mocks](../ejercicio-03-mocks/README.md) | **Ejercicio 04 · Cobertura y logging** | [Proyecto](../../3-proyecto/README.md) |
