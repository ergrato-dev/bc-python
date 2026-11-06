# Semana 02 — Operadores, strings, entrada/salida y `match`

> Un dato llega casi siempre como texto: una línea que escribe una persona, un argumento, un campo de un archivo. Esta semana aprendes a calcular y decidir con él, a cortarlo y limpiarlo, a mostrarlo bien formateado y a construir un programa de terminal que se comporta como los de verdad: lee, responde por el canal correcto y termina con un código que otros programas entienden.

Todavía no hay bucles: cada programa procesa **una** línea. La semana 3 añade la repetición.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Calcular** con `//`, `%` y `**` y **predecir** el resultado de expresiones con precedencia y cortocircuito
- **Decidir** con `if`/`elif`/`else` por rangos, probando los límites
- **Interpretar** órdenes de texto con `match`: literales, capturas, secuencias y guardas
- **Cortar**, **limpiar** y **comparar** texto con índices, slices y métodos de `str`, incluida la normalización Unicode
- **Formatear** números y tablas con el mini-lenguaje de formato
- **Explicar** qué es una t-string de Python 3.14 y por qué ayuda contra las inyecciones
- **Construir** un programa con `sys.argv`, `input`, stdout, stderr y código de salida

---

## 📋 Prerrequisitos

- [Semana 01](../week-01-entorno_docker_uv_y_tipos/README.md): entorno, uv, Docker y tipos básicos.
- El *pull request* `week-01` de tu proyecto fusionado en `main`.

---

## 🗂️ Estructura de la Semana

```
week-02-operadores_strings_io_y_match/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 4 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 1 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · Operadores y expresiones](1-teoria/01-operadores-y-expresiones.md) | Aritmética, `//` y `%` con negativos, comparaciones encadenadas, `and`/`or` y cortocircuito, precedencia | 45 min |
| [02 · Condicionales y `match`](1-teoria/02-condicionales-y-match.md) | `if`/`elif`/`else`, expresión condicional, `match` con literales, capturas, secuencias y guardas | 50 min |
| [03 · Strings a fondo](1-teoria/03-strings-a-fondo.md) | Índices, slicing, inmutabilidad, métodos, `partition`, `casefold` y normalización Unicode | 55 min |
| [04 · Formateo: f-strings y t-strings](1-teoria/04-formateo-f-strings-y-t-strings.md) | Mini-lenguaje de formato, `f"{x=}"`, t-strings y `Template` | 45 min |
| [05 · Entrada y salida](1-teoria/05-entrada-y-salida.md) | stdin, stdout, stderr, `input`, `sys.argv`, códigos de salida, lógica separada de `main` | 45 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, lo ejecutas y comparas con la salida esperada. Preparan el proyecto.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · Operadores y condicionales](2-practicas/ejercicio-01-operadores-y-condicionales/README.md) | `//` y `%`, bisiestos, `or` por defecto, rangos, expresión condicional, `match` con alternativas | 1 h 30 min |
| [02 · Strings](2-practicas/ejercicio-02-strings/README.md) | Slices, inmutabilidad, `partition`, `split`/`join`, palíndromos, texto Unicode | 1 h 30 min |
| [03 · Formateo y t-strings](2-practicas/ejercicio-03-formateo-y-t-strings/README.md) | Decimales, miles, dinero, columnas, `=`, un `Template` convertido en HTML seguro | 1 h 30 min |
| [04 · Entrada, salida y `match`](2-practicas/ejercicio-04-entrada-salida-y-match/README.md) | Un programa de órdenes con `sys.argv`, `input`, stderr y código de salida | 2 h |

### Proyecto

Las reglas de tu dominio (niveles por umbrales) y el comando `observatorio "etiqueta;valor"`, con tests calculados a mano. **Es el único entregable de la semana.**
→ [3-proyecto/README.md](3-proyecto/README.md)

---

## ⏱️ Distribución del Tiempo (18 horas)

| Actividad | Tiempo |
| --------- | ------ |
| Teoría (5 archivos) | 4 h |
| Ejercicio 01 | 1 h 30 min |
| Ejercicio 02 | 1 h 30 min |
| Ejercicio 03 | 1 h 30 min |
| Ejercicio 04 | 2 h |
| Proyecto | 5 h 30 min |
| Recursos y glosario | 1 h |
| Autoevaluación (cuestionario de la rúbrica) | 1 h |
| **Total** | **18 h** |

---

## 🎩 Trucos y atajos

| Truco | Cómo |
| ----- | ---- |
| Descomentar o comentar varias líneas | Selecciónalas en VS Code y `Ctrl+K Ctrl+U` (descomentar) o `Ctrl+K Ctrl+C` (comentar) |
| Ver el código de salida del último comando | `echo $?` |
| Separar resultados y errores | `programa > resultados.txt` guarda stdout; `2>/dev/null` descarta stderr |
| Ver un valor mientras pruebas | `print(f"{value=}")` |
| Ver espacios y comillas de un texto | `print(repr(text))` o `f"{text!r}"` |
| Ejecutar un archivo y quedarte en el REPL con sus variables | `uv run python -i archivo.py` |
| Ejecutar solo los tests de un archivo | `uv run pytest tests/test_main.py` |
| Ayuda de un método en el REPL | `help(str.partition)` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-02` de `python-<nombre>-<apellido>` con `rules.py`, `__main__.py` con tu unidad y tus umbrales, y al menos 6 tests propios, todo en verde en tu máquina y en Docker
2. ✅ `README.md` del repositorio con umbrales, justificación y ejemplo de uso
3. ✅ Pull request `week-02` → `main` con umbrales, salida de los tests y de los comandos del paso 8

El cuestionario de la [rúbrica](rubrica-evaluacion.md) es tu autoevaluación: respóndelo antes de mirar las respuestas.

---

## ✅ Verificación

En tu proyecto:

```bash
uv run pytest
uv run observatorio "Norte;12,5"; echo "código: $?"
docker compose run --build --rm app
```

Los tests deben terminar en `passed`, sin `failed`, y el comando con código `0`. En los ejercicios, cada paso descomentado debe dar la salida que muestra su README.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 01](../week-01-entorno_docker_uv_y_tipos/README.md) | **Semana 02** | [Semana 03](../week-03-bucles_iteracion_y_depuracion/README.md) |

← [Volver al índice de semanas](../README.md)
