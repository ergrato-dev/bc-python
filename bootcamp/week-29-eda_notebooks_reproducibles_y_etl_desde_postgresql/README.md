# Semana 29 — EDA, notebooks reproducibles y ETL desde PostgreSQL

> Tu Observatorio guarda medidas en PostgreSQL, las resume, las dibuja y las compara. Esta semana las **exploras**: aprendes a recorrer una tabla nueva sin dar nada por bueno, a trabajar en notebooks sin caer en el estado oculto, y a que tu análisis dé lo mismo hoy, dentro de un año y en la máquina de otra persona. Tu Observatorio gana el comando `extraer`, un ETL que saca las medidas de PostgreSQL a una instantánea con su huella, y un notebook de análisis de tu dominio que se ejecuta en JupyterLab, en Docker, en Colab y en tus tests.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Explorar** una tabla con un orden fijo, y **encontrar** huecos, centinelas, etiquetas mal escritas, repetidos y unidades mezcladas
- **Trabajar** en JupyterLab entendiendo el kernel, las salidas y el formato `.ipynb`, y **evitar** el estado oculto
- **Hacer** reproducible un análisis: datos con huella, código sin salidas, versiones fijadas también en Colab, semillas y el mismo entorno
- **Extraer** de PostgreSQL con pandas sin traer más de lo necesario, con parámetros y por partes, y **cargar** de vuelta sin duplicar
- **Servir** JupyterLab desde Docker, solo para tu máquina y con token
- **Probar** que un notebook se ejecuta de arriba abajo, en tu máquina y en la CI

---

## 📋 Prerrequisitos

- [Semana 19](../week-19-postgresql_psycopg_sqlalchemy_y_alembic/README.md): PostgreSQL, SQLAlchemy, sesiones y el comando `guardar`.
- [Semana 21](../week-21-calidad_y_entrega_pre_commit_github_actions_auditoria_e_imagen_docker_segura/README.md): ganchos de pre-commit, la CI y las etapas del `Dockerfile`.
- [Semana 28](../week-28-estadistica_aplicada_con_scipy_y_statsmodels/README.md): describir distribuciones y comparar grupos.
- El *pull request* `week-28` de tu proyecto fusionado en `main`, con la CI en verde.

---

## 🗂️ Estructura de la Semana

```
week-29-eda_notebooks_reproducibles_y_etl_desde_postgresql/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 28 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
|---|---|---|
| [01 · Análisis exploratorio](1-teoria/01-analisis-exploratorio.md) | El recorrido: forma, tipos, huecos, centinelas, etiquetas, repetidos, distribuciones por grupo, atípicos, relaciones y hallazgos | 50 min |
| [02 · Notebooks y JupyterLab](1-teoria/02-notebooks-y-jupyterlab.md) | Celdas, kernel y salidas, JupyterLab, VS Code y Colab, el estado oculto, el formato `.ipynb`, salidas fuera de Git, magias, notebook o paquete | 50 min |
| [03 · Reproducibilidad](1-teoria/03-reproducibilidad.md) | Cinco ingredientes: datos con huella, código, versiones (también en Colab), azar y hora, entorno; cómo comprobarlo | 45 min |
| [04 · ETL desde PostgreSQL](1-teoria/04-etl-desde-postgresql.md) | `read_sql` con tipos fijados, `WHERE` y `GROUP BY` en la base, `ORDER BY`, parámetros e inyección de SQL, por partes, `to_sql` idempotente | 50 min |
| [05 · Notebooks en un proyecto](1-teoria/05-notebooks-en-un-proyecto.md) | `etl.py` y `extraer`, el grupo `notebook`, JupyterLab en Docker con token, el gancho que limpia, el test que ejecuta el notebook | 45 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, ejecutas y comparas con la salida esperada. Preparan el proyecto. Las salidas coinciden con las del README salvo los tiempos y los números al azar que el ejercicio 04 deja sin semilla a propósito.

| Ejercicio | Qué haces | Duración |
|---|---|---|
| [01 · EDA con pandas](2-practicas/ejercicio-01-eda-con-pandas/README.md) | Encontrar los cuatro problemas de una tabla de sensores: huecos, un centinela, etiquetas y repetidos, una estación en °F | 1 h 30 min |
| [02 · Notebooks por dentro](2-practicas/ejercicio-02-notebooks-por-dentro/README.md) | Escribir un notebook con `nbformat`, ejecutarlo con `nbclient`, provocar estado oculto, quitar las salidas | 1 h 30 min |
| [03 · ETL desde PostgreSQL](2-practicas/ejercicio-03-etl-desde-postgresql/README.md) | `read_sql`, tipos, `GROUP BY` frente a pandas, una inyección de SQL, por partes, `to_sql` con `replace` y `append` | 1 h 30 min |
| [04 · Reproducible o no](2-practicas/ejercicio-04-reproducible-o-no/README.md) | El mismo notebook dos veces: semillas, la hora, rutas, una huella que detecta un cambio, versiones | 1 h 30 min |

### Proyecto

Añades a tu Observatorio:

- `core/etl.py`: `extract` (las medidas de PostgreSQL, en su orden y con sus tipos), `transform` (el nivel y las columnas en español) y `write_snapshot` (el CSV y su huella SHA-256);
- el comando `extraer SALIDA [--carga N]`;
- `notebooks/eda.ipynb`, tu análisis exploratorio sobre `notebooks/instantanea.csv`, con botón de Colab;
- JupyterLab en el grupo `notebook`, una etapa del `Dockerfile` y un servicio de `compose.yaml` con perfil;
- un gancho de pre-commit que quita salidas, contadores y horas de los notebooks.

43 tests nuevos: 22 del ETL y 21 que ejecutan y revisan tu notebook sin Jupyter. La imagen `runtime` no cambia. La versión sube a `0.29.0`. **Es el único entregable de la semana.**
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
| Abrir JupyterLab con las versiones de tu proyecto | `uv run --group notebook jupyter lab` |
| Ejecutar un notebook de arriba abajo, en un kernel nuevo | *Kernel → Restart Kernel and Run All Cells*, o `jupyter execute eda.ipynb` |
| Encontrar un centinela | `frame["col"].value_counts().sort_index().tail()` |
| Normalizar etiquetas | `frame["estacion"].str.strip().str.title()` |
| Leer un CSV sin convertir "NA" en hueco | `pd.read_csv(path, keep_default_na=False, na_values={"valor": [""]})` |
| Leer de PostgreSQL con los tipos fijados | `pd.read_sql(query, connection, dtype={...})` |
| Un valor en una consulta | `text("... WHERE station = :station")` y `params={"station": ...}` |
| La huella de un archivo | `hashlib.sha256(path.read_bytes()).hexdigest()` |
| Quitar las salidas de un notebook | `uv run pre-commit run notebook-outputs --all-files` |
| El token de JupyterLab en Docker | `docker compose logs notebook \| grep 127.0.0.1` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-29` de `python-<nombre>-<apellido>` con:
   - `core/etl.py` sin reexportar en `core/__init__.py` y el comando `extraer`, con pandas importado dentro;
   - `notebooks/eda.ipynb` y `notebooks/instantanea.csv` de tu dominio, sin salidas;
   - `jupyterlab==4.6.4` en el grupo `notebook`, la etapa y el servicio `notebook`, el gancho `notebook-outputs` y las imágenes `week-29`;
   - la versión `0.29.0` y al menos 6 tests propios en `tests/test_my_etl.py`.

   Todo en verde en tu máquina, en Docker y en GitHub Actions.
2. ✅ `README.md` del repositorio con la sección "Explorar los datos"
3. ✅ Pull request `week-29` → `main` con:
   - las salidas de los ganchos, la cobertura, `alembic check` y la CI en verde;
   - la salida de `extraer` con tu huella y tus conclusiones;
   - el tamaño de tus imágenes, tus dos tiempos de ejecución del notebook y la tabla de mutantes con las dos respuestas del paso 11.

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
uv run observatorio extraer notebooks/instantanea.csv --carga <tu carga>
uv run observatorio extraer /tmp/x.csv --carga 999
git status --short notebooks/
uv run python -c "import sys, observatorio.cli; print('pandas' in sys.modules)"
docker compose build app api notebook && docker compose run --rm app
gh pr checks
```

Lo que debes ver:

- todos los ganchos en `Passed` (o `Skipped`), también `notebooks sin salidas`;
- los tests terminan en `passed` sin `failed`, al menos 1203;
- `coverage report` termina sin `Coverage failure`;
- `alembic check` dice `No new upgrade operations detected.`;
- `--version` escribe `observatorio 0.29.0`;
- el primer `extraer` escribe tu número de medidas y **la misma huella** que tiene `EXPECTED` en tu notebook;
- el segundo, `error: no existe la carga 999` y código 1;
- `git status` no muestra cambios en `notebooks/`: el `extraer` de antes reescribió los mismos bytes;
- la comprobación de `sys.modules` escribe `False`;
- `gh pr checks` con `quality`, `tests` e `image` en `pass`.

En los ejercicios, cada paso descomentado da la salida que muestra su README; los tiempos y los números sin semilla, los de tu máquina.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 28](../week-28-estadistica_aplicada_con_scipy_y_statsmodels/README.md) | **Semana 29** | Semana 30 (próximamente) |
