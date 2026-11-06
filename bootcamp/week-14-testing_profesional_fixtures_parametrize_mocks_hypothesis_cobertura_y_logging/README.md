# Semana 14 — Testing profesional: fixtures, parametrize, mocks, Hypothesis, cobertura y logging

> Tu Observatorio tiene más de 300 tests en verde y, aun así, tres bugs dentro. `"Norte;abc"` tumba el programa, `"nan"` pasa por una medida y un archivo sin permiso de lectura escapa como `PermissionError`. Ningún test los encontró, porque todos prueban los casos que se te ocurrieron a ti. Esta semana aprendes a escribir tests que buscan lo que no se te ocurrió. **Hypothesis** genera los datos y encoge el contraejemplo; los **mocks** provocan fallos imposibles de provocar de verdad; **coverage** enseña qué no ha probado nadie. Y por el camino, ordenas los tests con fixtures y `parametrize` y das al programa un registro con `logging`.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Compartir** la preparación de los tests con fixtures, `yield` y `conftest.py`, y **elegir** su `scope`
- **Probar** muchos casos con `parametrize` y **marcar** un fallo conocido con `xfail`
- **Escribir** propiedades con Hypothesis, **leer** un contraejemplo encogido y **declarar** el dominio real de los datos
- **Sustituir** la red, el reloj o un fallo del sistema por un doble con `Mock`, `patch` y `autospec`, en el sitio correcto
- **Medir** la cobertura de líneas y de ramas, y **explicar** qué no dice un 100 %
- **Registrar** con un logger por módulo, **configurar** el registro solo en el programa y **probarlo** con `caplog`

---

## 📋 Prerrequisitos

- [Semana 13](../week-13-typing_estricto_mypy_y_pydantic/README.md): typing estricto con mypy y Pydantic v2.
- El *pull request* `week-13` de tu proyecto fusionado en `main`.

---

## 🗂️ Estructura de la Semana

```
week-14-testing_profesional_fixtures_parametrize_mocks_hypothesis_cobertura_y_logging/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 13 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · Fixtures y `conftest.py`](1-teoria/01-fixtures-y-conftest.md) | Pedir una fixture por su nombre, fixtures que piden fixtures, `yield`, `conftest.py`, `scope`, las fixtures de pytest y las fábricas | 50 min |
| [02 · Parametrize y marcas](1-teoria/02-parametrize-y-marcas.md) | `parametrize`, `ids` y `pytest.param`, combinaciones, cuándo no parametrizar, `skip`, `xfail` y elegir qué ejecutar | 40 min |
| [03 · Hypothesis](1-teoria/03-hypothesis.md) | Ejemplos frente a propiedades, estrategias, el contraejemplo encogido, patrones de propiedades, el dominio real y `@example` | 55 min |
| [04 · Mocks y dobles](1-teoria/04-mocks-y-dobles.md) | Qué sustituir, `Mock`, `side_effect`, `patch` y dónde parchear, `autospec`, `monkeypatch` e inyectar la dependencia | 45 min |
| [05 · Cobertura y logging](1-teoria/05-cobertura-y-logging.md) | coverage de líneas y de ramas, `fail_under`, lo que no dice el 100 %, niveles, el árbol de loggers, quién configura y `caplog` | 50 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, lo ejecutas y comparas con la salida esperada. Preparan el proyecto.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · Fixtures y parametrize](2-practicas/ejercicio-01-fixtures-y-parametrize/README.md) | Fixtures encadenadas con `--setup-show`, `yield`, `conftest.py`, `parametrize` con ids y `xfail`, y `scope="module"` | 1 h 30 min |
| [02 · Hypothesis](2-practicas/ejercicio-02-hypothesis/README.md) | Una propiedad de ida y vuelta, un contraejemplo encogido, un *off-by-one*, los límites de los `float` y `@example` | 1 h 30 min |
| [03 · Mocks](2-practicas/ejercicio-03-mocks/README.md) | `Mock`, `patch` en el sitio correcto y en el equivocado, `side_effect`, congelar la hora, `autospec` y `monkeypatch` | 1 h |
| [04 · Cobertura y logging](2-practicas/ejercicio-04-cobertura-y-logging/README.md) | `coverage report`, ramas, `--fail-under`, un logger sin configurar, `basicConfig` y `caplog` | 1 h 30 min |

### Proyecto

Los tests nuevos del bootcamp destapan tres bugs de tu Observatorio, y tú los arreglas:

- `"Norte;abc"` ya no tumba el programa: `parse_record` lo rechaza, y `parse_line` se construye sobre `parse_record`;
- `"nan"` e `"inf"` dejan de ser medidas, también en JSON;
- un archivo sin permiso de lectura da un `DataFileError`.

Además, escribes `tests/conftest.py` con cuatro fixtures, registras en DEBUG las líneas leídas y las descartadas, añades la opción `-v` y configuras coverage con ramas y un mínimo del 95 %. La versión sube a `0.14.0`, y `hypothesis` y `coverage` entran en el grupo `dev`. **Es el único entregable de la semana.**
→ [3-proyecto/README.md](3-proyecto/README.md)

---

## ⏱️ Distribución del Tiempo (18 horas)

| Actividad | Tiempo |
| --------- | ------ |
| Teoría (5 archivos) | 4 h |
| Ejercicio 01 | 1 h 30 min |
| Ejercicio 02 | 1 h 30 min |
| Ejercicio 03 | 1 h |
| Ejercicio 04 | 1 h 30 min |
| Proyecto | 6 h 30 min |
| Recursos y glosario | 1 h |
| Autoevaluación (cuestionario de la rúbrica) | 1 h |
| **Total** | **18 h** |

---

## 🎩 Trucos y atajos

| Truco | Cómo |
|---|---|
| Ver cuándo se crea cada fixture | `uv run pytest --setup-show` |
| Listar las fixtures disponibles | `uv run pytest --fixtures` |
| Repetir solo lo que falló y parar en el primero | `uv run pytest -x --lf` |
| Ver qué estrategia genera qué | `uv run python -c "from hypothesis import strategies as st; print(st.floats().example())"` (solo para mirar, nunca en un test) |
| Buscar más contraejemplos con Hypothesis | `@settings(max_examples=1000)` en el test, mientras investigas |
| Ver la cobertura como página web | `uv run coverage html` y abre `htmlcov/index.html` |
| Ver el registro de tu programa | `uv run observatorio -v -f medidas.csv > /dev/null` |
| Ver el registro de un test que falla | pytest lo enseña solo, en la sección `Captured log call` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-14` de `python-<nombre>-<apellido>` con:
   - `hypothesis==6.170.8` y `coverage==7.17.0` en `dev`, y `[tool.coverage]`;
   - `tests/conftest.py` con sus cuatro fixtures;
   - los tres bugs arreglados;
   - los loggers de `storage.py` y `groups.py`, y la opción `-v`;
   - la versión `0.14.0` y al menos 6 tests propios en `tests/test_my_quality.py`.

   Todo en verde en tu máquina y en Docker, con `ruff check`, `ruff format --check`, `mypy` y `coverage report` sin avisos.
2. ✅ `README.md` del repositorio con `-v` y el comando de cobertura
3. ✅ Pull request `week-14` → `main` con:
   - tests, `mypy`, `ruff` y la cobertura;
   - el contraejemplo de Hypothesis;
   - por qué el bug de `"abc"` estaba en dos sitios y por qué el permiso se prueba con un mock.

El cuestionario de la [rúbrica](rubrica-evaluacion.md) es tu autoevaluación: respóndelo antes de mirar las respuestas.

---

## ✅ Verificación

En tu proyecto:

```bash
uv run pytest
uv run ruff check && uv run ruff format --check
uv run mypy
uv run coverage run -m pytest -q && uv run coverage report
uv run observatorio --version
docker compose run --build --rm app
```

Lo que debes ver:

- los tests terminan en `passed` sin `failed`, al menos 455;
- ruff dice `All checks passed!` y `N files already formatted`;
- `mypy` dice `Success: no issues found`;
- `coverage report` termina sin `Coverage failure`;
- `--version` escribe `observatorio 0.14.0`.

En los ejercicios, cada paso descomentado da la salida que muestra su README.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 13](../week-13-typing_estricto_mypy_y_pydantic/README.md) | **Semana 14** | Semana 15 (próximamente) |

← [Volver al índice de semanas](../README.md)
