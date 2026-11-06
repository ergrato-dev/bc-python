# 05 · ruff

⏱️ 50 min

## 🎯 Objetivos

- Explicar la diferencia entre un *linter* y un *formatter*, y por qué un proyecto usa los dos.
- Ejecutar `ruff check`, leer sus avisos y arreglarlos con `--fix` o a mano.
- Distinguir un arreglo seguro de uno inseguro.
- Formatear con `ruff format` y comprobar con `--check`.
- Configurar ruff en `pyproject.toml`: longitud de línea, reglas y excepciones.

---

## 1. Un *linter* y un *formatter*

Los tests comprueban que el código hace lo que debe. Hay errores que no cambian ningún resultado y ningún test ve: un import que sobra, una variable que nadie usa, un valor por defecto que se comparte entre llamadas sin que nadie lo note hasta que falla en producción. Y hay discusiones que no aportan nada: comillas simples o dobles, dónde partir una línea larga.

| | *Linter*: `ruff check` | *Formatter*: `ruff format` |
|---|---|---|
| Busca | Errores probables y malas prácticas | Nada: reescribe la forma |
| Cambia lo que hace el código | Algunos arreglos podrían; por eso se revisan | Nunca |
| Ejemplos | Imports sin usar, `== None`, valores por defecto mutables, sintaxis antigua | Comillas, espacios, sangría, saltos de línea |
| Se ejecuta | `uv run ruff check` | `uv run ruff format` |

**ruff** hace las dos cosas. Está escrito en Rust y revisa un proyecto entero en milisegundos. Sustituye a varias herramientas que antes se usaban por separado: flake8 y sus *plugins* (*linter*), isort (orden de imports), pyupgrade (sintaxis moderna) y black (*formatter*), con las mismas reglas y casi el mismo formato.

## 2. `ruff check`

```bash
uv run ruff check                           # revisa la carpeta actual y las de dentro
uv run ruff check --output-format concise   # una línea por aviso
uv run ruff rule F401                       # explica una regla
```

```
src/observatorio/core/analysis.py:13:52: F401 [*] `observatorio.core.report.level_of` imported but unused
```

Cada aviso dice dónde (`archivo:línea:columna`), qué regla (`F401`) y qué pasa. El prefijo del código es la familia de la regla, que viene de la herramienta original:

| Prefijo | Familia | Qué busca |
|---|---|---|
| `F` | Pyflakes | Errores seguros: imports y variables sin usar, nombres no definidos |
| `E`, `W` | pycodestyle | El estilo de PEP 8: `== None`, varios imports en una línea |
| `I` | isort | El orden y el agrupado de los imports |
| `UP` | pyupgrade | Sintaxis antigua: `List[int]` en lugar de `list[int]`, `Optional[X]` en lugar de `X \| None` |
| `B` | flake8-bugbear | Trampas que suelen ser bugs: valores por defecto mutables, `except` demasiado amplios |
| `RUF` | ruff | Reglas propias, como `__all__` sin ordenar |

ruff 0.17 trae **407 reglas activas por defecto**, elegidas para que casi todos sus avisos sean problemas reales y casi ninguno de puro gusto. Por eso el proyecto no necesita elegir reglas: con los valores por defecto, ruff encontró en tu Observatorio un import sobrante que llevaba ahí desde la semana 6.

## 3. Arreglar: seguro, inseguro y a mano

Los avisos con `[*]` tienen un arreglo **seguro**: ruff está seguro de que no cambia lo que hace el programa.

```bash
uv run ruff check --fix
```

```
Found 11 errors (8 fixed, 3 remaining).
3 unsafe fixes available with `--fix --unsafe-fixes`.
```

Otros arreglos son **inseguros**: ruff sabe cómo hacerlos, pero podrían cambiar el comportamiento, y quiere que decidas tú. `--unsafe-fixes` los aplica sin preguntar; mejor léelos y arréglalos a mano. Un ejemplo, la regla `B006`:

```python
def add_reading(value: float, readings: list[float] = []) -> list[float]:
    readings.append(value)
    return readings
```

El `[]` se crea **una vez**, al definir la función, y todas las llamadas que no pasan `readings` comparten la misma lista: `add_reading(8.0)` devuelve `[8.0]`, y la siguiente, `add_reading(12.5)`, devuelve `[8.0, 12.5]`. El arreglo es usar `None` y crear la lista dentro:

```python
def add_reading(value: float, readings: list[float] | None = None) -> list[float]:
    if readings is None:
        readings = []
    readings.append(value)
    return readings
```

A veces un aviso no aplica en un caso concreto. Un comentario `# noqa: CÓDIGO` lo silencia en esa línea, y solo esa regla:

```python
from observatorio.core import *  # noqa: F403
```

Úsalo poco, y siempre con el código: un `# noqa` sin código lo silencia todo, y ruff avisa si queda alguno que ya no hace falta (`RUF100`).

## 4. `ruff format`

```bash
uv run ruff format --diff     # enseña los cambios, sin hacerlos
uv run ruff format            # los aplica
uv run ruff format --check    # falla si algún archivo no está formateado (para el CI)
```

```diff
-    return total/len(values)
+    return total / len(values)
```

El formato es **determinista**: el mismo código da siempre la misma salida, escriba quien lo escriba. En un equipo, nadie discute comillas ni sangrías, y los *diffs* de los *pull requests* solo muestran cambios de verdad. La primera vez que formateas un proyecto cambian muchos archivos: haz ese commit **solo**, sin cambios de lógica, para que quien revise sepa que no hay nada que leer línea a línea.

`ruff format` respeta los textos largos: no parte un `"..."` de 120 caracteres. Las líneas que siguen largas después de formatear las decides tú.

## 5. Configurar en `pyproject.toml`

```toml
[tool.ruff]
line-length = 100                     # por defecto, 88

[tool.ruff.lint]
extend-select = ["E"]                 # añade reglas a las de por defecto
ignore = ["E501"]                     # quita reglas
per-file-ignores = { "tests/*" = ["B011"] }   # quita reglas solo en algunos archivos
```

| Opción | Hace |
|---|---|
| `line-length` | La longitud que usa `ruff format` para partir líneas, y la regla `E501` si está activa |
| `select` | Sustituye las reglas activas por las que digas |
| `extend-select` | Añade reglas a las que ya había |
| `ignore` | Quita reglas |
| `per-file-ignores` | Quita reglas solo en los archivos que coinciden con el patrón |

Tu Observatorio solo cambia `line-length`: las reglas por defecto bastan. La configuración vive en el repositorio, no en el editor de cada uno: todos revisan con las mismas reglas, y el CI de la semana 21 también.

En VS Code, la extensión **Ruff** (de Astral) usa esta misma configuración: subraya los avisos mientras escribes y puede formatear al guardar.

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| `error: Failed to spawn: ruff` | ruff no está en el grupo `dev` del proyecto | `uv add --dev ruff==0.17.3` |
| `--fix` no arregla un aviso | El arreglo es inseguro o no existe | Lee `uv run ruff rule CÓDIGO` y arréglalo a mano |
| Una opción de `[tool.ruff]` no hace efecto | Está bajo otra tabla, o es de lint y va en `[tool.ruff]` en lugar de `[tool.ruff.lint]` | `select`, `ignore` y compañía van en `[tool.ruff.lint]` |
| `ruff format` y tus tests cambian mucho de golpe | Es la primera vez | Un commit `style:` solo con eso |
| Un `# noqa` sin código | Silencia todas las reglas en esa línea | `# noqa: F401`, con el código |

---

## ✅ Qué debes saber al terminar

- [ ] La diferencia entre `ruff check` y `ruff format`, y por qué un proyecto usa los dos.
- [ ] Leer un aviso: archivo, línea, columna, código y familia.
- [ ] Qué es un arreglo seguro y uno inseguro, y por qué `B006` es un bug.
- [ ] Cuándo usar `# noqa: CÓDIGO`.
- [ ] Para qué sirven `ruff format --diff` y `ruff format --check`.
- [ ] Configurar `line-length`, `extend-select`, `ignore` y `per-file-ignores` en `pyproject.toml`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [04 · Dependencias y lock](04-dependencias-y-lock.md) | **05 · ruff** | [Ejercicio 01 · Módulos e imports](../2-practicas/ejercicio-01-modulos-e-imports/README.md) |
