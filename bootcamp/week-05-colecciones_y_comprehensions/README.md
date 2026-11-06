# Semana 05 — Colecciones: listas, tuplas, diccionarios, conjuntos y comprehensions

> Un programa de datos pasa la mayor parte del tiempo guardando, buscando, contando y agrupando. Esta semana conoces las cuatro colecciones de Python, cuándo usar cada una y las trampas de los objetos que cambian. Con ellas el Observatorio deja de ver filas de texto y empieza a ver registros: cuenta por nivel, agrupa por etiqueta y calcula medias, lo mismo que hará pandas en la fase 4.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Crear, leer, cambiar y ordenar** listas, y **explicar** por qué `b = a` no copia
- **Usar** tuplas como registros y **desempaquetarlas**, también en un `for`
- **Contar y agrupar** con diccionarios, y **elegir** entre `[clave]`, `.get` y `setdefault`
- **Quitar repetidos y comparar grupos** con conjuntos
- **Escribir** list, dict y set comprehensions y expresiones generadoras, y **saber** cuándo un bucle se lee mejor
- **Elegir** la colección adecuada para cada problema

---

## 📋 Prerrequisitos

- [Semana 04](../week-04-funciones_scope_type_hints_y_pytest/README.md): funciones, type hints y `pytest`.
- El *pull request* `week-04` de tu proyecto fusionado en `main`.

---

## 🗂️ Estructura de la Semana

```
week-05-colecciones_y_comprehensions/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 4 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · Listas](1-teoria/01-listas.md) | Índices, métodos que devuelven `None`, `sorted` frente a `sort`, `key` con dos criterios, alias y copias | 1 h |
| [02 · Tuplas y desempaquetado](1-teoria/02-tuplas-y-desempaquetado.md) | Inmutabilidad, tupla o lista, alias de tipo, `*rest`, comparar tuplas | 35 min |
| [03 · Diccionarios](1-teoria/03-diccionarios.md) | Leer sin fallar, recorrer, contar, agrupar con `setdefault`, claves hashables | 1 h |
| [04 · Conjuntos](1-teoria/04-conjuntos.md) | Sin repetidos ni orden, `\|`, `&`, `-`, set o lista | 30 min |
| [05 · Comprehensions](1-teoria/05-comprehensions.md) | List, dict y set comprehensions, filtrar o elegir, generadores, cuándo no | 55 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, lo ejecutas y comparas con la salida esperada. Preparan el proyecto.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · Listas y tuplas](2-practicas/ejercicio-01-listas-y-tuplas/README.md) | Leer, cambiar, ordenar, alias y copia, desempaquetar, ordenar tuplas por valor | 1 h 30 min |
| [02 · Diccionarios y conjuntos](2-practicas/ejercicio-02-diccionarios-y-conjuntos/README.md) | Leer por clave, contar, agrupar, tuplas como clave, operaciones de conjuntos | 1 h 30 min |
| [03 · Comprehensions](2-practicas/ejercicio-03-comprehensions/README.md) | Del bucle a la comprehension, filtrar o elegir, generadores que se agotan, anidadas | 1 h 30 min |
| [04 · Estructuras anidadas](2-practicas/ejercicio-04-estructuras-anidadas/README.md) | Tres trampas de la mutabilidad, datos como un JSON, buscar en lista o en set | 1 h |

### Proyecto

El Observatorio guarda cada medida como un registro `(etiqueta, valor)`, cuenta por nivel con un diccionario, agrupa por etiqueta, calcula medias y muestra las más altas y cuántas etiquetas distintas hay. **Es el único entregable de la semana.**
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
| Ver los métodos de una colección | `dir([])`, `dir({})` o `help(dict.setdefault)` en el REPL |
| Ver una estructura anidada legible | `from pprint import pprint` y `pprint(datos)` |
| Saber si dos nombres son el mismo objeto | `a is b`, o `id(a) == id(b)` |
| Ver el contenido de una colección al depurar | Panel **Variables** del depurador de VS Code: despliega listas y diccionarios |
| Contar cuántos distintos hay | `len(set(valores))` |
| Quitar repetidos sin perder el orden | `list(dict.fromkeys(valores))` |
| Pasar de bucle a comprehension | Escribe primero el bucle; cuando funcione, reordena sus tres piezas |
| Ejecutar solo los tests de una función | `uv run pytest -k test_top`, con el prefijo `test_` para no atrapar otros nombres |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-05` de `python-<nombre>-<apellido>` con `groups.py`, tu `main` ampliado, `count_level` refactorizado, tu `medidas.txt` con etiquetas repetidas y al menos 6 tests propios, todo en verde en tu máquina y en Docker, y `mypy` sin errores
2. ✅ `README.md` del repositorio con el informe nuevo
3. ✅ Pull request `week-05` → `main` con tests, `mypy`, informe y la explicación de `list(sys.stdin)`

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

Los tests terminan en `passed` sin `failed`, `mypy` dice `Success: no issues found` y el informe termina con `etiquetas distintas` y las tres medias más altas. En los ejercicios, cada paso descomentado da la salida que muestra su README.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 04](../week-04-funciones_scope_type_hints_y_pytest/README.md) | **Semana 05** | [Semana 06](../week-06-algoritmos_big_o_collections_e_itertools/README.md) |

← [Volver al índice de semanas](../README.md)
