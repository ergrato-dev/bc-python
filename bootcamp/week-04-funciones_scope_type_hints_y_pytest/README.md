# Semana 04 — Funciones, scope, type hints y primer `pytest`

> Llevas tres semanas usando funciones y tests escritos por otros. Esta semana los entiendes por dentro: cómo viajan los datos en una llamada, dónde vive cada variable, cómo los tipos te avisan de errores antes de ejecutar, y cómo escribir tus propios tests desde cero. Con eso reorganizas el Observatorio: la lógica, pura y probada; la terminal, en el borde.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Definir** funciones con parámetros por posición, por nombre, por defecto y solo por nombre, y **devolver** uno o varios valores
- **Explicar** la regla LEGB y **evitar** `UnboundLocalError` y el valor por defecto mutable
- **Separar** la lógica pura de los efectos (leer y escribir)
- **Pasar** funciones como argumentos y **ordenar** con `key=` y `lambda`; **escribir** una función recursiva
- **Anotar** tipos, incluidos `X | None`, `list[str]` e `Iterable[str]`, y **revisarlos** con `mypy`
- **Escribir** tests con `assert`, `pytest.approx`, `pytest.raises` y `parametrize`, siguiendo el ciclo rojo, verde, refactorizar

---

## 📋 Prerrequisitos

- [Semana 03](../week-03-bucles_iteracion_y_depuracion/README.md): bucles, patrones de bucle y depuración.
- El *pull request* `week-03` de tu proyecto fusionado en `main`.

---

## 🗂️ Estructura de la Semana

```
week-04-funciones_scope_type_hints_y_pytest/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 3 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · Definir y llamar funciones](1-teoria/01-definir-y-llamar-funciones.md) | `def`, docstring, `return` frente a `print`, formas de pasar argumentos, `*`, varios valores, guardas | 50 min |
| [02 · Scope y efectos](1-teoria/02-scope-y-efectos.md) | LEGB, `UnboundLocalError`, valor por defecto mutable, funciones puras | 40 min |
| [03 · Funciones como valores](1-teoria/03-funciones-como-valores.md) | Pasar funciones, `key=`, `lambda`, recursión | 40 min |
| [04 · Type hints](1-teoria/04-type-hints.md) | Anotaciones, `X \| None`, `list`, `tuple`, `Iterable`, `mypy` | 40 min |
| [05 · Tests con pytest](1-teoria/05-tests-con-pytest.md) | Descubrimiento, informe de fallos, `approx`, `raises`, `parametrize`, AAA, TDD | 1 h 10 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, lo ejecutas y comparas con la salida esperada. Preparan el proyecto.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · Definir funciones](2-practicas/ejercicio-01-definir-funciones/README.md) | `def`, `print` frente a `return`, argumentos por posición y nombre, `*`, tuplas, guardas | 1 h 30 min |
| [02 · Scope y funciones como valores](2-practicas/ejercicio-02-scope-y-funciones-como-valores/README.md) | Local y global, `UnboundLocalError`, `[]` por defecto, funciones como argumento, `key=`, recursión | 1 h 30 min |
| [03 · Type hints](2-practicas/ejercicio-03-type-hints/README.md) | Tres errores de tipo que Python no ve y `mypy` sí | 1 h |
| [04 · pytest desde cero](2-practicas/ejercicio-04-pytest-desde-cero/README.md) | Tests que encuentran dos errores escondidos; `approx`, `raises`, `parametrize`, `-k`, `-x`, `--lf` | 2 h |

### Proyecto

La lógica del Observatorio pasa a funciones puras (`process_lines`, `count_level`, `ratio`, `share`), `main` queda delgado, el informe gana el porcentaje en nivel alto y los tipos se revisan con `mypy`. **Es el único entregable de la semana.**
→ [3-proyecto/README.md](3-proyecto/README.md)

---

## ⏱️ Distribución del Tiempo (18 horas)

| Actividad | Tiempo |
| --------- | ------ |
| Teoría (5 archivos) | 4 h |
| Ejercicio 01 | 1 h 30 min |
| Ejercicio 02 | 1 h 30 min |
| Ejercicio 03 | 1 h |
| Ejercicio 04 | 2 h |
| Proyecto | 6 h |
| Recursos y glosario | 1 h |
| Autoevaluación (cuestionario de la rúbrica) | 1 h |
| **Total** | **18 h** |

---

## 🎩 Trucos y atajos

| Truco | Cómo |
| ----- | ---- |
| Ver la docstring y la firma de una función | `help(nombre)` en el REPL, o pasa el ratón por encima en VS Code |
| Ir a la definición de una función | `F12` en VS Code; volver, `Alt+←` |
| Renombrar una función en todo el proyecto | `F2` sobre el nombre en VS Code |
| Extraer código a una función | Selecciona las líneas, `Ctrl+.` → **Extract method** en VS Code |
| Revisar tipos sin instalar nada | `uv run --with mypy==2.4.1 mypy src tests` |
| Ejecutar un solo test | `uv run pytest tests/test_analysis.py::test_share_default_decimals` |
| Repetir solo lo que falló | `uv run pytest --lf` |
| Parar en el primer fallo | `uv run pytest -x` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-04` de `python-<nombre>-<apellido>` con `analysis.py`, el `main` delgado con tus umbrales y al menos 6 tests propios, todo en verde en tu máquina y en Docker, y `mypy` sin errores
2. ✅ `README.md` del repositorio con la organización del código y el informe nuevo
3. ✅ Pull request `week-04` → `main` con tests, `mypy`, informe y un límite del dominio justificado

El cuestionario de la [rúbrica](rubrica-evaluacion.md) es tu autoevaluación: respóndelo antes de mirar las respuestas.

---

## ✅ Verificación

En tu proyecto:

```bash
uv run pytest
uv run --with mypy==2.4.1 mypy src tests
uv run observatorio < medidas.txt; echo "código: $?"
docker compose run --build --rm app
```

Los tests terminan en `passed` sin `failed`, `mypy` dice `Success: no issues found` y el informe termina con la línea `en alto: ... %`. En los ejercicios, cada paso descomentado da la salida que muestra su README.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 03](../week-03-bucles_iteracion_y_depuracion/README.md) | **Semana 04** | Semana 05 (próximamente) |

← [Volver al índice de semanas](../README.md)
