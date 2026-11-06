# Semana 03 — Bucles e iteración; depuración con `pdb` y VS Code

> Un dato suelto no dice mucho; mil datos, sí. Esta semana tu programa deja de procesar una línea y empieza a recorrer archivos enteros: repite, cuenta, acumula, busca y resume. Y como un bucle mal escrito falla en la vuelta 907 y no en la primera, aprendes también a detener un programa y mirar dentro de él.

Es la última semana sin funciones propias a fondo (semana 4) ni colecciones (semana 5): las listas aparecen solo lo justo para recorrerlas y añadir elementos.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Recorrer** textos, rangos, listas y la entrada estándar con `for`, `enumerate` y `zip`
- **Repetir** con `while` hasta que algo cambie, y **cortar** un bucle infinito
- **Controlar** las vueltas con `break`, `continue` y el `else` de los bucles
- **Aplicar** los patrones contador, acumulador, máximo, búsqueda, filtro y racha, y **comprobarlos** con una tabla de traza
- **Procesar** un archivo línea a línea con `<` y `|`, avisando de los errores sin detenerse
- **Depurar** con el traceback, `print(f"{x=}")`, `pdb` y el depurador de VS Code

---

## 📋 Prerrequisitos

- [Semana 02](../week-02-operadores_strings_io_y_match/README.md): operadores, strings, entrada/salida y `match`.
- El *pull request* `week-02` de tu proyecto fusionado en `main`.
- VS Code con la extensión **Python** de Microsoft (para el depurador).

---

## 🗂️ Estructura de la Semana

```
week-03-bucles_iteracion_y_depuracion/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 2 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · `for` e iterables](1-teoria/01-for-e-iterables.md) | Cuerpo y sangría, iterables, `range`, `enumerate`, `zip`, bucles anidados | 50 min |
| [02 · `while`, `break`, `continue` y `else`](1-teoria/02-while-break-continue.md) | Condición de parada, bucle infinito, centinela, `else` de los bucles | 45 min |
| [03 · Patrones de bucle](1-teoria/03-patrones-de-bucle.md) | Contador, acumulador, máximo, búsqueda, filtro, racha y tabla de traza | 50 min |
| [04 · Leer muchas líneas](1-teoria/04-leer-muchas-lineas.md) | `sys.stdin`, `<`, `\|`, `Ctrl+D`, números de línea, búferes, `-T` en Docker | 35 min |
| [05 · Depuración](1-teoria/05-depuracion.md) | Traceback, `print` con `=`, `pdb`, depurador de VS Code, método para depurar | 1 h |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, lo ejecutas y comparas con la salida esperada. Preparan el proyecto.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · `for` y `range`](2-practicas/ejercicio-01-for-y-range/README.md) | Vocales, rangos, suma y factorial, `enumerate`, `zip`, una tabla, el máximo a mano | 1 h 30 min |
| [02 · `while`, `break` y `continue`](2-practicas/ejercicio-02-while-break-y-continue/README.md) | Cuenta atrás, Collatz, promedio sin `None`, búsqueda, primos con `else`, centinela | 1 h 30 min |
| [03 · Depuración](2-practicas/ejercicio-03-depuracion/README.md) | Cuatro errores a propósito: traceback, `print`, `pdb` y VS Code | 2 h |
| [04 · Muchas líneas](2-practicas/ejercicio-04-muchas-lineas/README.md) | Leer un archivo por stdin, saltar comentarios, resumir y avisar de errores | 1 h 30 min |

### Proyecto

El Observatorio procesa un archivo entero de tu dominio: una fila por medida, errores con su número de línea y un resumen por niveles con la racha más larga. **Es el único entregable de la semana.**
→ [3-proyecto/README.md](3-proyecto/README.md)

---

## ⏱️ Distribución del Tiempo (18 horas)

| Actividad | Tiempo |
| --------- | ------ |
| Teoría (5 archivos) | 4 h |
| Ejercicio 01 | 1 h 30 min |
| Ejercicio 02 | 1 h 30 min |
| Ejercicio 03 | 2 h |
| Ejercicio 04 | 1 h 30 min |
| Proyecto | 5 h 30 min |
| Recursos y glosario | 1 h |
| Autoevaluación (cuestionario de la rúbrica) | 1 h |
| **Total** | **18 h** |

---

## 🎩 Trucos y atajos

| Truco | Cómo |
| ----- | ---- |
| Cortar un programa que no termina | `Ctrl+C` |
| Terminar la entrada desde el teclado | `Ctrl+D` al principio de una línea |
| Pasar un archivo como entrada | `uv run python programa.py < archivo.txt` |
| Ver solo los errores | `uv run python programa.py < archivo.txt > /dev/null` |
| Detener el programa en una línea | `breakpoint()`, o un punto rojo en VS Code y `F5` |
| Desactivar todos los `breakpoint()` | `PYTHONBREAKPOINT=0 uv run python programa.py` |
| Abrir `pdb` en el test que falla | `uv run pytest --pdb` |
| Depurar un test en VS Code | Vista Testing → clic derecho sobre el test → **Debug Test** |
| Parar solo en una vuelta concreta | Clic derecho sobre el punto rojo → **Edit Breakpoint** → `number == 907` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-03` de `python-<nombre>-<apellido>` con `report.py`, `__main__.py` con tus umbrales, tu `medidas.txt` y al menos 6 tests propios, todo en verde en tu máquina y en Docker
2. ✅ `README.md` del repositorio con el uso con archivo y un informe de ejemplo
3. ✅ Pull request `week-03` → `main` con tests, informe, código de salida y un error depurado explicado

El cuestionario de la [rúbrica](rubrica-evaluacion.md) es tu autoevaluación: respóndelo antes de mirar las respuestas.

---

## ✅ Verificación

En tu proyecto:

```bash
uv run pytest
uv run observatorio < medidas.txt; echo "código: $?"
docker compose run --build --rm app
```

Los tests deben terminar en `passed`, sin `failed`. El informe muestra una fila por medida, el resumen y la racha; el código es `1` si tu `medidas.txt` incluye la línea inválida que pide el paso 9. En los ejercicios, cada paso descomentado debe dar la salida que muestra su README.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 02](../week-02-operadores_strings_io_y_match/README.md) | **Semana 03** | Semana 04 (próximamente) |

← [Volver al índice de semanas](../README.md)
