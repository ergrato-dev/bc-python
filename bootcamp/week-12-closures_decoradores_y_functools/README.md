# Semana 12 — Closures, decoradores y `functools`

> Llevas once semanas escribiendo `@dataclass`, `@property` y `key=lambda ...` sin preguntarte qué son. Esta semana lo descubres: en Python una función es un valor más, que se guarda, se pasa y se devuelve. Una función creada dentro de otra recuerda las variables de fuera (*closure*), y una función que recibe otra y devuelve una versión ampliada es un **decorador**. `functools` trae los que más se usan: `partial`, `cache`, `wraps` y `singledispatch`. El proyecto le da a `Series` un filtro que recibe funciones, y estrena una closure, dos decoradores y una función que cambia según el tipo de lo que recibe.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Usar** funciones como valores: **guardarlas**, **pasarlas** como argumento y **devolverlas**, anotadas con `Callable`
- **Prever** con la regla LEGB qué variable usa cada nombre y **escribir** closures, con `nonlocal` cuando cambian su estado
- **Escribir** decoradores con `functools.wraps`, también genéricos con `[**P, R]`, y **prever** el orden de los apilados
- **Escribir** decoradores con argumentos (tres niveles) y **usarlos** para registrar funciones
- **Aplicar** `partial`, `cache`, `lru_cache`, `cached_property`, `reduce` y `singledispatch`, y **decidir** cuándo no hacerlo
- **Probar** closures y decoradores comprobando su resultado, sus llamadas y su identidad

---

## 📋 Prerrequisitos

- [Semana 11](../week-11-data_model_dunders_iteradores_y_generadores/README.md): data model, dunders, iteradores y generadores.
- El *pull request* `week-11` de tu proyecto fusionado en `main`.

---

## 🗂️ Estructura de la Semana

```
week-12-closures_decoradores_y_functools/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 11 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · Funciones como objetos](1-teoria/01-funciones-como-objetos.md) | Funciones en variables y diccionarios, `lambda`, funciones de orden superior, fábricas de funciones y `Callable` | 45 min |
| [02 · Closures y alcance](1-teoria/02-closures-y-alcance.md) | La regla LEGB, `UnboundLocalError`, closures y celdas, `nonlocal` frente a `global` y la trampa del bucle | 50 min |
| [03 · Decoradores](1-teoria/03-decoradores.md) | Un decorador a mano, la sintaxis `@`, `functools.wraps`, `*args`/`**kwargs`, `ParamSpec` y decoradores apilados | 50 min |
| [04 · Decoradores con argumentos](1-teoria/04-decoradores-con-argumentos.md) | Tres niveles, olvidar los paréntesis, registrar funciones, `@dataclass(...)` y un `retry` | 45 min |
| [05 · functools](1-teoria/05-functools.md) | `partial`, `cache` y `lru_cache`, `cached_property`, `reduce`, `singledispatch`, el diseño de la capa 11 y cómo probar decoradores | 50 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, lo ejecutas y comparas con la salida esperada. Preparan el proyecto.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · Funciones y closures](2-practicas/ejercicio-01-funciones-y-closures/README.md) | Funciones en un diccionario, `key=`, el alcance LEGB y su `UnboundLocalError`, closures con `nonlocal` y la trampa del bucle | 1 h 30 min |
| [02 · Decoradores](2-practicas/ejercicio-02-decoradores/README.md) | Un decorador a mano, `@` y el nombre perdido, `functools.wraps`, un contador para cualquier función y decoradores apilados | 1 h 30 min |
| [03 · Decoradores con argumentos](2-practicas/ejercicio-03-decoradores-con-argumentos/README.md) | `@repeat(3)`, `@repeat` sin paréntesis, un registro de lectores, `@dataclass(frozen=True)` a mano y un `retry` | 1 h 30 min |
| [04 · functools](2-practicas/ejercicio-04-functools/README.md) | `partial`, `cache` con `cache_info`, `lru_cache` que descarta, `reduce` y `singledispatch` | 1 h |

### Proyecto

El Observatorio gana funciones de orden superior: `Series.where(keep)` filtra con la función que le pases; `core/functional.py` trae `above` (una closure), `skip_missing` y `rounded` (decoradores) y `describe` (`singledispatch`). `main` no cambia, la versión sube a `0.12.0` y el informe no cambia ni un carácter. **Es el único entregable de la semana.**
→ [3-proyecto/README.md](3-proyecto/README.md)

---

## ⏱️ Distribución del Tiempo (18 horas)

| Actividad | Tiempo |
| --------- | ------ |
| Teoría (5 archivos) | 4 h |
| Ejercicio 01 | 1 h 30 min |
| Ejercicio 02 | 1 h 30 min |
| Ejercicio 03 | 1 h 30 min |
| Ejercicio 04 | 1 h |
| Proyecto | 6 h 30 min |
| Recursos y glosario | 1 h |
| Autoevaluación (cuestionario de la rúbrica) | 1 h |
| **Total** | **18 h** |

---

## 🎩 Trucos y atajos

| Truco | Cómo |
|---|---|
| Ver qué variables recuerda una closure | `f.__code__.co_freevars` y `[c.cell_contents for c in f.__closure__]` |
| Llamar a la función sin su decorador | `f.__wrapped__(...)`, si el decorador usa `functools.wraps` |
| Esqueleto de un decorador genérico | `def deco[**P, R]` que recibe `func: Callable[P, R]` y devuelve `Callable[P, R]`, con `@functools.wraps(func)` en el `wrapper` |
| Fijar un argumento sin escribir una `lambda` | `functools.partial(round, ndigits=1)` |
| Ver si una caché sirve de algo | `f.cache_info()`: muchos `misses` y pocos `hits` significa que no |
| Vaciar una caché entre tests | `f.cache_clear()` |
| Ver qué tipos tiene una función `singledispatch` | `list(f.registry)` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-12` de `python-<nombre>-<apellido>` con `Series.where`; `core/functional.py` (`above`, `skip_missing`, `rounded` y `describe`), los cuatro nombres en la API pública, la versión `0.12.0` y al menos 6 tests propios en `tests/test_my_functional.py`, todo en verde en tu máquina y en Docker, con `ruff check`, `ruff format --check` y `mypy` sin avisos
2. ✅ `README.md` del repositorio con `functional.py` en el árbol del paquete
3. ✅ Pull request `week-12` → `main` con tests, `mypy`, `ruff`, los dos fallos del `skip_missing` sin `wraps` y el orden de `skip_missing` y `rounded`

El cuestionario de la [rúbrica](rubrica-evaluacion.md) es tu autoevaluación: respóndelo antes de mirar las respuestas.

---

## ✅ Verificación

En tu proyecto:

```bash
uv run pytest
uv run ruff check && uv run ruff format --check
uv run mypy
uv run observatorio --version
docker compose run --build --rm app
```

Los tests terminan en `passed` sin `failed` (al menos 364), ruff dice `All checks passed!` y `N files already formatted`, `mypy` dice `Success: no issues found` y `--version` escribe `observatorio 0.12.0`. En los ejercicios, cada paso descomentado da la salida que muestra su README.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 11](../week-11-data_model_dunders_iteradores_y_generadores/README.md) | **Semana 12** | [Semana 13](../week-13-typing_estricto_mypy_y_pydantic/README.md) |

← [Volver al índice de semanas](../README.md)
