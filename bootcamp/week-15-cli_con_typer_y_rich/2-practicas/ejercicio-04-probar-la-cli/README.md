# Ejercicio 04 — Probar la CLI

⏱️ 1 h 30 min · Teoría previa: [05](../../1-teoria/05-probar-la-cli-y-cerrar-la-fase.md)

## Objetivo

Probar una aplicación Typer desde pytest, sin lanzar otro proceso:

- `CliRunner.invoke` y lo que devuelve: `exit_code`, `stdout`, `stderr`;
- errores de uso (código 2) frente a resultados "no" (código 1);
- stdin con `input=`;
- archivos de verdad con `tmp_path`;
- un caso por nivel con `parametrize`;
- y la pregunta incómoda: ¿estos tests detectarían un bug? La respondes rompiendo `app.py` a propósito.

Tu proyecto cambia `tests/test_main.py` por `tests/test_cli.py`, que usa `CliRunner`. Ejercicio **guiado**: descomentas cada paso de `tests/test_app.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-15-cli_con_typer_y_rich/2-practicas/ejercicio-04-probar-la-cli/starter
uv run python main.py clasificar 12 61
uv run pytest
```

```
12 → medio
61 → alto
aviso: 1 valores altos
```

```
============================ no tests ran in 0.03s =============================
```

`app.py` es una CLI pequeña y completa. `clasificar` da el nivel de cada valor y termina con código `1` si alguno es alto. `contar` cuenta las líneas con datos de un archivo. Léela antes de seguir: los tests prueban lo que dice su ayuda.

## Pasos

### 1. Ejecutar un comando

Descomenta el **PASO 1** y ejecuta:

```bash
uv run pytest -v
```

```
tests/test_app.py::test_clasificar_one_value PASSED                      [100%]
```

`runner.invoke(app, ["clasificar", "30"])` hace lo mismo que `main.py clasificar 30` en la terminal, pero dentro del test. Typer analiza los argumentos, llama a la función, y el `Result` guarda lo que pasó. No hay otro proceso: es rápido, y coverage lo mide.

### 2. stderr y los códigos de salida

Descomenta el **PASO 2** y ejecuta `uv run pytest`:

```
3 passed in 0.09s
```

`result.stdout` y `result.stderr` llegan **separados**, así que puedes comprobar que el aviso va a stderr y las filas a stdout. El código `2` lo pone Typer cuando "doce" no es un `float`: tu función no llega a ejecutarse, y stdout queda vacío.

`result.output` tiene las dos salidas juntas, en orden. Úsalo solo si no te importa a cuál va cada cosa.

### 3. stdin con `input=`

Descomenta el **PASO 3** y ejecuta `uv run pytest`:

```
4 passed in 0.09s
```

`input="5\n\n30\n"` es lo que el comando lee de `sys.stdin`, como si llegara por una tubería. Sin `input=`, stdin está vacío: el test no se queda esperando.

### 4. Archivos de verdad

Descomenta el **PASO 4** y ejecuta `uv run pytest`:

```
6 passed in 0.10s
```

Como en la semana 7: el test escribe el archivo en `tmp_path` y pasa la ruta como texto. El segundo test comprueba el error de `exists=True`, que viene de Typer y termina con código `2`.

### 5. Un caso por nivel

Descomenta el **PASO 5** y ejecuta `uv run pytest`:

```
9 passed in 0.10s
```

Tres casos, uno por nivel. Parece completo: cada `return` de `level` se ejecuta.

### 6. ¿Detectan un bug?

Ahora rompe `app.py` a propósito. En `level`, cambia `if value > HIGH:` por `if value >= HIGH:`. Es un bug creíble: `50` pasaría a ser `alto`, y la ayuda dice que los umbrales son `medio`. Ejecuta `uv run pytest`:

```
9 passed in 0.09s
```

Todo verde con un bug dentro. Ningún test usa un valor **en** un umbral: `5`, `30` y `61` dan lo mismo con `>` que con `>=`.

Deja el bug y descomenta el **PASO 6**, que prueba los bordes:

```bash
uv run pytest
```

```
FAILED tests/test_app.py::test_the_thresholds_are_medio[50-medio] - Assertion...
1 failed, 12 passed in 0.12s
```

El test nuevo encuentra el bug. Vuelve a poner `>` en `app.py` y ejecuta otra vez: `13 passed`.

Lo que acabas de hacer es una **prueba de mutación** a mano: cambiar el código a propósito para ver si los tests lo notan. Si nada falla, esos tests no protegen esa línea, aunque la cobertura diga que se ejecuta. La cobertura dice qué se **ejecutó**, y la mutación, qué se **comprobó**.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'app'` | Ejecuta pytest desde `starter/`: `pythonpath = ["."]` en `pyproject.toml` busca `app.py` en la carpeta actual |
| `assert 2 == 0` en `exit_code` | Typer rechazó los argumentos: mira `result.stderr` para ver por qué (un `print(result.stderr)` en el test) |
| `result.stdout` está vacío y el test falla raro | Hubo una excepción dentro del comando: mira `result.exception`. `CliRunner` la captura y no la enseña |
| `61.0 → alto` en lugar de `61 → alto` | `app.py` escribe con `:g`, que quita el `.0`. Si cambiaste el formato, cambia también el texto esperado |
| El paso 6 no falla con el bug | Cambiaste otra línea, o no guardaste `app.py`. El cambio es `value > HIGH` por `value >= HIGH`, en `level` |
| Algunos tests fallan después del paso 6 | Te dejaste el bug: vuelve a escribir `>` en `level` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Rich](../ejercicio-03-rich/README.md) | **Ejercicio 04 · Probar la CLI** | [Proyecto](../../3-proyecto/README.md) |
