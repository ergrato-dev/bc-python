# Semana 30 — Proyecto de fase: análisis de tu dominio

> Cierre de la fase 4. Has explorado tus datos en un notebook; esta semana **confirmas**. Haces una pregunta antes de ver la respuesta, escribes hallazgos con su tamaño y su incertidumbre, corriges por comparaciones múltiples y publicas un informe que sale de un comando, se lee en GitHub y la CI vigila. Tu Observatorio gana el comando `hallazgos` y la carpeta `informe/` con el análisis de tu dominio.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Convertir** una pregunta de tu dominio en una que los datos pueden responder, y **decidirla** antes de mirar
- **Escribir** hallazgos defendibles: diferencia, intervalo y tamaño del efecto, no solo un p-valor
- **Reconocer** la paradoja de Simpson y las variables de confusión
- **Corregir** por comparaciones múltiples con Bonferroni, Holm y Benjamini-Hochberg, y **elegir** entre FWER y FDR
- **Dibujar** un gráfico por afirmación y **generar** un informe en Markdown, byte a byte reproducible
- **Vigilar** con un test que el informe del repositorio sigue al día con sus datos

---

## 📋 Prerrequisitos

- [Semana 27](../week-27-visualizacion_con_matplotlib_seaborn_y_plotly/README.md): `Figure` sin `pyplot` y `charts.save`.
- [Semana 28](../week-28-estadistica_aplicada_con_scipy_y_statsmodels/README.md): intervalos, pruebas de hipótesis, d de Cohen e `inference.difference`.
- [Semana 29](../week-29-eda_notebooks_reproducibles_y_etl_desde_postgresql/README.md): la instantánea con su huella y tu notebook de exploración.
- El *pull request* `week-29` de tu proyecto fusionado en `main`, con la CI en verde.

---

## 🗂️ Estructura de la Semana

```
week-30-proyecto_de_fase_analisis_de_tu_dominio/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 29 de tu Observatorio y tu informe: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
|---|---|---|
| [01 · De la exploración a la pregunta](1-teoria/01-de-la-exploracion-a-la-pregunta.md) | Explorar y confirmar, las cuatro piezas de una pregunta, decidir antes de mirar, el jardín de los senderos que se bifurcan | 45 min |
| [02 · Hallazgos defendibles](1-teoria/02-hallazgos-defendibles.md) | Tamaño e incertidumbre, significativo no es importante, la paradoja de Simpson, correlación y causa, robustez | 50 min |
| [03 · Muchas comparaciones](1-teoria/03-muchas-comparaciones.md) | 1 − (1 − α)^m, FWER y FDR, Bonferroni, Holm y Benjamini-Hochberg, `false_discovery_control` | 50 min |
| [04 · El informe, desde el código](1-teoria/04-el-informe-desde-el-codigo.md) | Las secciones de un informe, un gráfico por afirmación, Markdown sin plantillas, los mismos bytes, el test que lo vigila | 50 min |
| [05 · Cerrar la fase 4](1-teoria/05-cerrar-la-fase-4.md) | Del dato al informe, la fase semana a semana, mutantes en un informe, lo que llevas a la fase 5 | 45 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, ejecutas y comparas con la salida esperada. Preparan el proyecto. Las salidas coinciden con las del README salvo las huellas de los archivos que cambian a propósito en cada ejecución.

| Ejercicio | Qué haces | Duración |
|---|---|---|
| [01 · De la pregunta a la métrica](2-practicas/ejercicio-01-de-la-pregunta-a-la-metrica/README.md) | La misma tabla, tres respuestas: por medida, por sensor y por estación, con la paradoja de Simpson | 1 h 30 min |
| [02 · Muchas comparaciones](2-practicas/ejercicio-02-muchas-comparaciones/README.md) | Falsos positivos simulados, Bonferroni, Holm y BH, BH a mano, y mil análisis para medir cada corrección | 1 h 30 min |
| [03 · Un gráfico por afirmación](2-practicas/ejercicio-03-un-grafico-por-afirmacion/README.md) | De barras de medias a un *forest plot* con título-conclusión, SVG reproducible y con texto | 1 h 30 min |
| [04 · Un informe desde el código](2-practicas/ejercicio-04-un-informe-desde-el-codigo/README.md) | Una tabla Markdown con `join`, una barra que la rompe, formatos, los mismos bytes y un informe viejo detectado | 1 h 30 min |

### Proyecto

Añades a tu Observatorio:

- `core/findings.py`: `read_snapshot` (la instantánea con su huella), `compare_all` (cada par de etiquetas, con Benjamini-Hochberg), `differences_figure` (el *forest plot*) y `render` (el informe en Markdown);
- el comando `hallazgos INSTANTANEA CARPETA [--huella] [--confianza] [--alfa]`;
- `informe/`: `hallazgos.md` y `diferencias.svg`, generados, y tu `README.md`, con la pregunta, los datos, los hallazgos, las limitaciones y los siguientes pasos de tu dominio.

51 tests nuevos: 45 del módulo y el comando, y 6 que comprueban tu informe. Ninguna dependencia nueva. La versión sube a `0.30.0`. **Es el único entregable de la semana.**
→ [3-proyecto/README.md](3-proyecto/README.md)

---

## ⏱️ Distribución del Tiempo (18 horas)

| Actividad | Tiempo |
|---|---|
| Teoría (5 archivos) | 4 h |
| Ejercicio 01 | 1 h 30 min |
| Ejercicio 02 | 1 h 30 min |
| Ejercicio 03 | 1 h 30 min |
| Ejercicio 04 | 1 h 30 min |
| Proyecto | 6 h 30 min |
| Recursos y glosario | 30 min |
| Autoevaluación (cuestionario de la rúbrica) | 1 h |
| **Total** | **18 h** |

---

## 🎩 Trucos y atajos

| Truco | Cómo |
|---|---|
| Cuántos pares con k etiquetas | `k * (k - 1) // 2`, o `len(list(itertools.combinations(labels, 2)))` |
| Probabilidad de algún falso positivo | `1 - (1 - alpha) ** m` |
| Corregir con Benjamini-Hochberg | `scipy.stats.false_discovery_control(p_values, method="bh")` |
| Corregir con Bonferroni | `np.minimum(p * len(p), 1)` |
| Ver la paradoja de Simpson | `frame.pivot_table(index="estacion", columns="zona", values="valor")` |
| Un *forest plot* | `axes.errorbar(centros, filas, xerr=[abajo, arriba], fmt="o")` y `axes.axvline(0)` |
| Un SVG reproducible y con texto | `rc_context({"svg.hashsalt": "x", "svg.fonttype": "none"})` y `metadata={"Date": None}` |
| Regenerar el informe | `uv run observatorio hallazgos notebooks/instantanea.csv informe` |
| Ver qué cambió en el informe | `git diff informe/hallazgos.md` |
| Ver el informe como en GitHub | VS Code: *Markdown: Open Preview* sobre `informe/README.md` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-30` de `python-<nombre>-<apellido>` con:
   - `core/findings.py` sin reexportar en `core/__init__.py` y el comando `hallazgos`, con los imports dentro;
   - `informe/README.md` de tu dominio, con la pregunta en un commit anterior al de los hallazgos, y `informe/hallazgos.md` y `informe/diferencias.svg` al día;
   - las imágenes `week-30`, la versión `0.30.0` y al menos 6 tests propios en `tests/test_my_findings.py`.

   Todo en verde en tu máquina, en Docker y en GitHub Actions.
2. ✅ `README.md` del repositorio con la sección "Informe"
3. ✅ Pull request `week-30` → `main` con:
   - las salidas de los ganchos, la cobertura, `alembic check` y la CI en verde;
   - la salida de `hallazgos`, el enlace a tu informe y al commit de tu pregunta;
   - la tabla de mutantes con las dos respuestas del paso 9.

El cuestionario de la [rúbrica](rubrica-evaluacion.md) es tu autoevaluación: respóndelo antes de mirar las respuestas.

---

## ✅ Verificación

En tu proyecto:

```bash
docker compose up -d --wait db
uv run pre-commit run --all-files
uv run pytest
uv run coverage run -m pytest -q && uv run coverage report
uv run alembic check
uv run observatorio --version
uv run observatorio hallazgos notebooks/instantanea.csv informe --huella <tu huella>
git status --short informe/
uv run observatorio hallazgos notebooks/instantanea.csv /tmp/x --huella 0000
uv run python -c "import sys, observatorio.cli; print('scipy' in sys.modules)"
docker compose build app api && docker compose run --rm app
gh pr checks
```

Lo que debes ver:

- todos los ganchos en `Passed` (o `Skipped`);
- los tests terminan en `passed` sin `failed`, al menos 1260;
- `coverage report` termina sin `Coverage failure`;
- `alembic check` dice `No new upgrade operations detected.`;
- `--version` escribe `observatorio 0.30.0`;
- el primer `hallazgos` escribe tu número de medidas, tu huella y cuántos pares difieren;
- `git status` no muestra cambios en `informe/`: los mismos datos dieron los mismos bytes;
- el segundo `hallazgos`, `error: la huella de instantanea.csv es ..., no 0000` y código 1;
- la comprobación de `sys.modules` escribe `False`;
- `gh pr checks` con `quality`, `tests` e `image` en `pass`.

En los ejercicios, cada paso descomentado da la salida que muestra su README; las huellas que cambian en cada ejecución, las de tu máquina.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 29](../week-29-eda_notebooks_reproducibles_y_etl_desde_postgresql/README.md) | **Semana 30** | Semana 31 (próximamente) |
