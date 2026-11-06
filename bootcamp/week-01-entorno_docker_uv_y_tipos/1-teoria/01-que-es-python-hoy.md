# 01 · Qué es Python hoy

⏱️ 40 min

## 🎯 Objetivos

- Saber qué es Python y qué es CPython.
- Saber para qué se usa Python hoy y por qué este bootcamp pone el peso en datos e IA.
- Entender por qué el curso fija Python 3.14.10 y no "la última".

---

## 1. Un lenguaje y un programa que lo ejecuta

**Python** es un lenguaje de programación: un conjunto de reglas para escribir instrucciones que un ordenador puede seguir. Esto es Python:

```python
print("Hola, mundo")
```

El ordenador no entiende ese texto por sí solo. Necesita un programa que lo lea y lo ejecute: el **intérprete**. El intérprete oficial se llama **CPython** (está escrito en C) y es el que instalas cuando dices "instalar Python". Hay otros (PyPy, MicroPython), pero en este bootcamp siempre usas CPython.

| Palabra | Qué es | Ejemplo |
|---|---|---|
| Lenguaje | Las reglas para escribir el programa | `print("Hola")` |
| Intérprete | El programa que lee y ejecuta tu código | `python3.14` |
| Script | Un archivo de texto con código Python | `main.py` |
| Biblioteca | Código ya escrito que reutilizas | `pandas`, `pytest` |

## 2. Para qué se usa Python

Python se usa en casi todo, pero hay tres áreas donde es el lenguaje dominante:

| Área | Qué se hace | Bibliotecas que verás |
|---|---|---|
| **Datos** | Leer, limpiar, analizar y graficar datos | NumPy, pandas, Polars, DuckDB, matplotlib |
| **Inteligencia artificial** | Entrenar modelos, usar LLMs, construir asistentes | scikit-learn, PyTorch, Transformers, SDK de LLM |
| **Automatización y backend** | Scripts, APIs, tareas programadas | httpx, FastAPI, SQLAlchemy |

Por eso las fases 4 y 5 del bootcamp (20 de 42 semanas) son data science e IA. Las fases 1 a 3 te dan lo que esas fases necesitan: Python bien escrito, tipado, probado y capaz de hablar con bases de datos y APIs.

## 3. Por qué Python 3.14.10 y no "la última"

Python publica una versión nueva cada octubre (3.13 en 2024, 3.14 en 2025, 3.15 en 2026). Cada versión recibe correcciones durante unos 5 años con números como `3.14.1`, `3.14.2`… El número tiene tres partes:

```
3   .   14   .   10
│       │        └── micro: correcciones de errores y de seguridad, sin cambios de comportamiento
│       └─────────── menor: funciones nuevas; puede romper bibliotecas antiguas
└─────────────────── mayor: cambia muy pocas veces (Python 2 → 3 fue en 2008)
```

El bootcamp fija **3.14.10** por dos motivos:

1. **Reproducibilidad.** Si cada persona usa una versión distinta, el mismo ejercicio funciona en una máquina y falla en otra. Con la versión fijada, tu resultado es el mismo que el del curso.
2. **Compatibilidad con las bibliotecas de datos e IA.** Una versión menor nueva (3.15) tarda meses en tener soporte de NumPy, PyTorch y compañía. 3.14 ya lo tiene.

Las versiones de todo el stack, con la fecha en que se revisaron, están en [`docs/stack-versions.md`](../../../docs/stack-versions.md).

## 4. Qué trae Python 3.14 que usarás

No necesitas entender esto todavía; es para que reconozcas los nombres cuando aparezcan:

| Novedad | Dónde la verás |
|---|---|
| REPL con colores y edición de varias líneas (desde 3.13) | Esta semana, en [02](02-del-codigo-a-la-ejecucion.md) |
| Mensajes de error más claros, con sugerencias | Todo el bootcamp |
| Build *free-threaded* (sin GIL) con soporte oficial | Semana 16, concurrencia |
| Anotaciones de tipo evaluadas de forma diferida | Semana 13, typing estricto |
| Plantillas de texto `t"..."` (*template strings*) | Semana 2, strings |

## 5. Errores frecuentes

| Error | Por qué pasa | Qué hacer |
|---|---|---|
| "Ya tengo Python, viene con el sistema" | Linux y macOS traen un Python que usa el propio sistema operativo | No lo toques ni lo actualices: uv instala el tuyo aparte ([03](03-uv-proyectos-y-entornos.md)) |
| Seguir un tutorial que usa Python 2 | Hay mucho material viejo en internet | Si ves `print "hola"` sin paréntesis, es Python 2: descártalo |
| Pensar que necesitas Anaconda para datos e IA | Durante años fue el camino habitual | Con uv y Docker no hace falta ([`docs/setup.md`](../../../docs/setup.md)) |

---

## ✅ Qué debes saber al terminar

- Python es el lenguaje; CPython es el intérprete que lo ejecuta.
- Datos, IA y automatización son las áreas donde Python domina.
- La versión del curso es 3.14.10 y está fijada para que todos obtengan el mismo resultado.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 01](../README.md) | **01 · Qué es Python hoy** | [02 · Del código a la ejecución](02-del-codigo-a-la-ejecucion.md) |
