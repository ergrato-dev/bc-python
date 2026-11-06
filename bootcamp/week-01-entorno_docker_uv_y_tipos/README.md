# Semana 01 — Entorno: Docker, uv, Python 3.14 y tipos

> Antes de escribir programas hay que saber qué pasa entre tu `.py` y un programa funcionando, quién instala Python y las bibliotecas, y por qué un dato que falta no es un `0`. Esta semana montas el entorno que usarás las 41 siguientes y das tus primeros pasos con los tipos.

No hay bucles, ni listas, ni clases. Hay un intérprete, un proyecto uv, un contenedor, los tipos básicos y las primeras funciones de tu Observatorio.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Describir** qué hace CPython con un `.py` y **leer** un traceback
- **Usar** el REPL para probar expresiones
- **Crear** y **ejecutar** un proyecto con `uv init`, `uv add`, `uv sync` y `uv run`
- **Explicar** qué guardan `pyproject.toml`, `uv.lock`, `.python-version` y `.venv/`
- **Ejecutar** tests en un contenedor con `docker compose run` y **corregir** una imagen que corre como root
- **Elegir** el tipo correcto (`int`, `float`, `bool`, `str`, `None`) y **convertir** entre tipos de forma explícita
- **Comparar** `float` con `math.isclose` y **distinguir** `None` de `0` y `""`

---

## 📋 Prerrequisitos

- Ninguna semana anterior: esta es la primera.
- Docker, uv, Git y VS Code según [`docs/setup.md`](../../docs/setup.md).
- Terminal básica y Git (`bc-linux-commandline`, `bc-github`).
- **No hace falta saber programar.**

---

## 🗂️ Estructura de la Semana

```
week-01-entorno_docker_uv_y_tipos/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 4 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 3 ejercicios con starter/ y tests
├── 3-proyecto/                  # la capa 0 de tu Observatorio
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · Qué es Python hoy](1-teoria/01-que-es-python-hoy.md) | Lenguaje e intérprete, usos, versiones fijadas | 40 min |
| [02 · Del código a la ejecución](1-teoria/02-del-codigo-a-la-ejecucion.md) | Bytecode, PVM, REPL, `SyntaxError` frente a errores en ejecución, traceback | 45 min |
| [03 · uv: proyectos y entornos](1-teoria/03-uv-proyectos-y-entornos.md) | Entorno virtual, `pyproject.toml`, `uv.lock`, `uv init/add/sync/run` | 55 min |
| [04 · Docker para Python](1-teoria/04-docker-para-python.md) | Imagen, capa, contenedor, el `Dockerfile` del curso, `docker compose run` | 55 min |
| [05 · Variables y tipos](1-teoria/05-variables-y-tipos.md) | Nombres y objetos, tipos básicos, conversiones, f-strings, primeras funciones | 45 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, lo ejecutas y comparas con la salida esperada. Preparan el proyecto.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · Hola, entorno](2-practicas/ejercicio-01-hola-entorno/README.md) | Toolchain, primera función, REPL, bytecode, los dos tipos de error | 2 h |
| [02 · Python en Docker](2-practicas/ejercicio-02-python-en-docker/README.md) | El programa en el contenedor, caché de capas, usuario sin privilegios, lock roto | 2 h 30 min |
| [03 · Tipos y conversiones](2-practicas/ejercicio-03-tipos-y-conversiones/README.md) | Conversiones que fallan, `float` inexactos, `int` sin límite, `None` | 2 h 30 min |

### Proyecto

Con el dominio que te asignó tu instructor, creas tu repositorio y escribes la capa 0 del Observatorio: leer, validar y mostrar una medida, con tests calculados a mano.
→ [3-proyecto/README.md](3-proyecto/README.md)

---

## ⏱️ Distribución del Tiempo (18 horas)

| Actividad | Tiempo |
| --------- | ------ |
| Teoría (5 archivos) | 4 h |
| Ejercicio 01 | 2 h |
| Ejercicio 02 | 2 h 30 min |
| Ejercicio 03 | 2 h 30 min |
| Proyecto | 5 h |
| Recursos y glosario | 1 h |
| Autoevaluación (cuestionario de la rúbrica) | 1 h |
| **Total** | **18 h** |

---

## 🎩 Trucos y atajos

| Truco | Cómo |
| ----- | ---- |
| Probar una línea sin crear archivo | `uv run python` y escribe en el REPL |
| Ejecutar solo algunos tests | `uv run pytest -k parse_value` |
| Ver más detalle de un test que falla | `uv run pytest -vv` |
| Parar en el primer fallo | `uv run pytest -x` |
| Ver el árbol de dependencias | `uv tree` |
| Comprobar que el lock está al día | `uv lock --check` |
| Abrir el REPL dentro del contenedor | `docker compose run --rm app python` |
| Ver el bytecode de un archivo | `uv run python -m dis main.py` |
| Ayuda de cualquier función en el REPL | `help(round)` |

---

## 📌 Entregables

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Repositorio `python-<nombre>-<apellido>` con tu dominio en su README
2. ✅ Rama `week-01` con al menos 5 tests propios, todo en verde en tu máquina y en Docker
3. ✅ Pull request `week-01` → `main` con dominio, versiones y salidas

El cuestionario de la [rúbrica](rubrica-evaluacion.md) es tu autoevaluación: respóndelo antes de mirar las respuestas.

---

## ✅ Verificación

En tu proyecto:

```bash
uv run pytest
docker compose run --build --rm app
```

Los dos deben terminar en `passed`, sin `failed`. En los ejercicios, cada paso descomentado debe dar la salida que muestra su README. Si algo falla antes de llegar a los tests (uv, Docker), las tablas de errores frecuentes de [03 · uv](1-teoria/03-uv-proyectos-y-entornos.md) y [04 · Docker](1-teoria/04-docker-para-python.md) cubren los casos habituales.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Índice de semanas](../README.md) | **Semana 01** | [Semana 02](../week-02-operadores_strings_io_y_match/README.md) |

← [Volver al inicio del bootcamp](../../README.md)
