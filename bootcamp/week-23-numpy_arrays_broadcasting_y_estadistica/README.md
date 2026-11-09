# Semana 23 — NumPy: arrays, broadcasting y estadística

> Empieza la fase 4, data science. En la semana 22 usaste NumPy solo para medir, y decidiste con números no meterlo en `informe`. Esta semana lo aprendes en serio: qué es un array por dentro (forma, tipo y `strides`), cómo se eligen partes sin copiar sin querer, cómo se opera con tablas enteras gracias al **broadcasting**, y cómo se tratan los datos que faltan, se resume una columna y se buscan atípicos. Tu Observatorio gana un comando, `estadisticas`, que hace todo eso con NumPy sin que los demás comandos paguen su importación. Es la base de pandas, Polars, scikit-learn y PyTorch.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Crear** arrays y **leer** su `shape`, su `dtype` y sus `strides`, y reconocer los límites de los enteros y de la coma flotante
- **Elegir** partes de un array con índices, cortes, listas y máscaras, sabiendo cuándo obtienes una **vista** y cuándo una **copia**
- **Resumir** tablas por filas o por columnas con `axis`, y **operar** arrays de formas distintas con la regla del broadcasting
- **Tratar** los datos que faltan con NaN, y **controlar** los avisos de NumPy
- **Resumir** una columna (media, desviación, cuartiles, histograma) y **encontrar** atípicos con puntuaciones z, conociendo su punto débil
- **Generar** datos aleatorios reproducibles con `default_rng`
- **Llevar** NumPy a un proyecto con tipos (`NDArray`), tests con tolerancia y una importación que solo paga quien la usa

---

## 📋 Prerrequisitos

- [Semana 22](../week-22-rendimiento_profiling_cprofile_py_spy_y_vectorizacion/README.md): rendimiento, sobre todo la teoría 05 y el ejercicio 04.
- El *pull request* `week-22` de tu proyecto fusionado en `main`, con la CI en verde.

---

## 🗂️ Estructura de la Semana

```
week-23-numpy_arrays_broadcasting_y_estadistica/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 22 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · Arrays: forma, tipo y memoria](1-teoria/01-arrays-forma-tipo-y-memoria.md) | Crear arrays, `shape` y ejes, `reshape`, `dtype` y `object`, enteros que dan la vuelta, coma flotante, `strides` y vistas | 45 min |
| [02 · Índices, vistas y máscaras](1-teoria/02-indices-vistas-y-mascaras.md) | Índices y cortes en dos ejes, vistas y copias, listas de posiciones, máscaras con `&`, `\|` y `~`, `np.where`, `argsort` y `argmax` | 50 min |
| [03 · Operaciones, ejes y broadcasting](1-teoria/03-operaciones-ejes-y-broadcasting.md) | *Ufuncs*, resumir con `axis`, la regla del broadcasting, `keepdims`, normalizar columnas y tablas de dos ejes | 50 min |
| [04 · Datos que faltan, estadística y azar](1-teoria/04-datos-que-faltan-estadistica-y-azar.md) | `default_rng` y semillas, NaN y las funciones `nan*`, avisos y `errstate`, resumen de una columna, histograma, puntuaciones z y atípicos | 50 min |
| [05 · NumPy en un proyecto](1-teoria/05-numpy-en-un-proyecto.md) | `NDArray` y mypy, tipos de Python en la frontera, tests con tolerancia y sin avisos, importar solo donde hace falta, dónde gana y dónde no | 45 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, ejecutas y comparas con la salida esperada. Preparan el proyecto. Los datos aleatorios llevan semilla, así que tus números coinciden con los del README; los tiempos, no.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · Arrays y dtypes](2-practicas/ejercicio-01-arrays-y-dtypes/README.md) | Crear arrays, forma y memoria, mezclar tipos, desbordar un `int8`, coma flotante y vistas de `reshape` | 1 h 30 min |
| [02 · Índices, vistas y máscaras](2-practicas/ejercicio-02-indices-vistas-y-mascaras/README.md) | Elegir en una tabla, cambiar un corte y ver el original, listas de posiciones, máscaras, `np.where` y ordenar con `argsort` | 1 h 30 min |
| [03 · Broadcasting y ejes](2-practicas/ejercicio-03-broadcasting-y-ejes/README.md) | Resumir por día y por estación, el error de broadcasting y su arreglo, normalizar, tablas de tres ejes y bucles frente a broadcasting | 1 h 30 min |
| [04 · NaN, estadística y aleatoriedad](2-practicas/ejercicio-04-nan-estadistica-y-aleatoriedad/README.md) | Semillas, NaN, avisos, el resumen de una columna, un histograma en la terminal y atípicos que se esconden | 1 h 30 min |

### Proyecto

Añades a tu Observatorio:

- `numpy==2.5.4` como dependencia de producción;
- `core/arrays.py`: la serie como array con NaN, `stats_of`, `zscores`, `outliers`, `histogram` y `group_means`, un *group by* sin bucles;
- el comando `estadisticas RUTA [-u UMBRAL] [-i INTERVALOS]`: la tabla de estadísticas, un histograma, las atípicas y la media por etiqueta.

NumPy se importa **solo** en ese comando: `informe` tarda lo mismo que en la semana 22, y un test lo vigila. Mides dónde gana NumPy (por 30 y por 200) y dónde pierde (con las etiquetas). 40 tests nuevos, cuatro de ellos con Hypothesis, dos contra lo que ya tenías. La versión sube a `0.23.0`. **Es el único entregable de la semana.**
→ [3-proyecto/README.md](3-proyecto/README.md)

---

## ⏱️ Distribución del Tiempo (18 horas)

| Actividad | Tiempo |
| --------- | ------ |
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
| Probar algo de NumPy al vuelo | `uv run python` y `import numpy as np` (en el proyecto o en un ejercicio) |
| ¿Vista o copia? | `np.shares_memory(a, b)` |
| ¿Por qué no encaja el broadcasting? | `print(a.shape, b.shape)` y alinéalas por la derecha |
| Ver arrays sin notación científica | `np.set_printoptions(suppress=True, precision=2)` |
| Contar los `True` de una máscara | `np.count_nonzero(mascara)` o `mascara.sum()` |
| Datos aleatorios que se repiten | `rng = np.random.default_rng(23)` |
| Que un aviso de NumPy pare el programa | `with np.errstate(all="raise"):` |
| Comparar arrays en un test | `np.testing.assert_allclose(actual, esperado)` |
| ¿Importa NumPy este módulo? | `uv run python -c "import sys, observatorio.cli; print('numpy' in sys.modules)"` |
| Cuánto tarda importar NumPy | `uv run python -X importtime -c "import numpy" 2>&1 \| tail -1` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-23` de `python-<nombre>-<apellido>` con:
   - `core/arrays.py` sin reexportar en `core/__init__.py`, y el comando `estadisticas` con NumPy importado dentro;
   - `numpy==2.5.4` en las dependencias, las imágenes `week-23` en `compose.yaml`;
   - la versión `0.23.0` y al menos 6 tests propios en `tests/test_my_arrays.py`.

   Todo en verde en tu máquina, en Docker y en GitHub Actions.
2. ✅ `README.md` del repositorio con la sección "Estadísticas"
3. ✅ Pull request `week-23` → `main` con:
   - las salidas de los ganchos, la cobertura, `alembic check` y la CI en verde;
   - `estadisticas` con tus datos y el umbral que elegiste para tu dominio;
   - tu tabla de tiempos, el tamaño de la imagen y la tabla de mutantes con el equivalente explicado.

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
uv run observatorio estadisticas medidas.txt
uv run python -c "import sys, observatorio.cli; print('numpy' in sys.modules)"
docker compose build app api && docker compose run --rm app
gh pr checks
```

Lo que debes ver:

- todos los ganchos en `Passed` (o `Skipped`);
- los tests terminan en `passed` sin `failed`, al menos 779;
- `coverage report` termina sin `Coverage failure`;
- `alembic check` dice `No new upgrade operations detected.`;
- `--version` escribe `observatorio 0.23.0`;
- `estadisticas` escribe la tabla, el histograma, las atípicas y la media por etiqueta;
- la comprobación de `sys.modules` escribe `False`;
- `gh pr checks` con `quality`, `tests` e `image` en `pass`.

En los ejercicios, cada paso descomentado da la salida que muestra su README; los tiempos, los de tu máquina.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 22](../week-22-rendimiento_profiling_cprofile_py_spy_y_vectorizacion/README.md) | **Semana 23** | Semana 24 (próximamente) |
