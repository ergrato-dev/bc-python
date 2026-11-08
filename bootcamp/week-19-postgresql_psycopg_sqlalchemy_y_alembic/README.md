# Semana 19 — PostgreSQL con psycopg, SQLAlchemy y Alembic

> Tu Observatorio lee archivos, los resume y los olvida. Esta semana aprende a **guardar**: en una base de datos de verdad, **PostgreSQL**, que varios programas pueden compartir, que no deja guardar datos que rompen sus reglas, y que cuenta y promedia sin traer un millón de filas a Python. Hablas con ella primero sin nada en medio, con **psycopg**; después con **SQLAlchemy**, que convierte filas en objetos; y cambias sus tablas sin perder datos con las **migraciones** de **Alembic**. Lo aplicas en cuatro comandos nuevos, `guardar`, `cargas`, `consultar` y `borrar`, probados contra un PostgreSQL en Docker.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Explicar** qué gana un programa al guardar en una base de datos, y **leer y escribir** el SQL básico: claves, `JOIN`, `GROUP BY`, `NULL` y transacciones
- **Consultar** PostgreSQL con psycopg 3 usando **parámetros**, y **explicar** por qué evitan la inyección de SQL
- **Modelar** tablas con el ORM de SQLAlchemy 2 y **trabajar** con una sesión, sin caer en el problema N+1
- **Cambiar** el esquema con migraciones de Alembic, y **corregir** lo que `--autogenerate` no sabe hacer
- **Probar** contra un PostgreSQL de verdad, con una transacción por test y la base creada por las migraciones
- **Levantar** PostgreSQL con Docker Compose, con *healthcheck*, volumen y el puerto cerrado a la red

---

## 📋 Prerrequisitos

- [Semana 18](../week-18-http_con_httpx_reintentos_secretos_y_env/README.md): HTTP con httpx, reintentos, secretos y `.env`.
- El *pull request* `week-18` de tu proyecto fusionado en `main`.
- Docker funcionando: `docker compose version`.

---

## 🗂️ Estructura de la Semana

```
week-19-postgresql_psycopg_sqlalchemy_y_alembic/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 18 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · Bases de datos relacionales y PostgreSQL](1-teoria/01-bases-de-datos-relacionales-y-postgresql.md) | Por qué una base de datos, tablas y tipos, claves y restricciones, SQL en cinco minutos, `NULL`, transacciones, PostgreSQL en Compose y `psql` | 45 min |
| [02 · psycopg: conexiones, parámetros y transacciones](1-teoria/02-psycopg-conexiones-parametros-y-transacciones.md) | El *driver*, conexión y cursor, parámetros e inyección de SQL, `psycopg.sql`, transacciones, errores y `COPY` | 45 min |
| [03 · SQLAlchemy 2: motor, Core y ORM](1-teoria/03-sqlalchemy-2-motor-core-y-orm.md) | Las capas, el motor y su pool, el Core, modelos con `Mapped`, la sesión, el mapa de identidad, N+1 y lo que sale de la sesión | 55 min |
| [04 · Alembic: migraciones del esquema](1-teoria/04-alembic-migraciones-del-esquema.md) | La cadena de migraciones, `env.py`, `--autogenerate` y sus límites, nombres de restricciones, `upgrade`/`downgrade` y migraciones en equipo | 45 min |
| [05 · Probar con una base de datos de verdad](1-teoria/05-probar-con-una-base-de-datos-de-verdad.md) | PostgreSQL y no SQLite, la base de pruebas, migraciones en la fixture, una transacción por test, la CLI, contar consultas y Docker | 50 min |

### Prácticas

Guiadas y sin entrega: el código viene comentado por pasos, lo descomentas, lo ejecutas y comparas con la salida esperada. Preparan el proyecto. Los cuatro comparten un PostgreSQL (`docker compose up -d --wait` en cualquiera de ellos), en el puerto 5433 para no chocar con el de tu proyecto.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · Consultas con psycopg](2-practicas/ejercicio-01-consultas-con-psycopg/README.md) | Conectar, crear una tabla, insertar con parámetros, una inyección de SQL de verdad, transacciones que se deshacen y que se rompen, `psycopg.sql` y `COPY` | 1 h 30 min |
| [02 · SQLAlchemy Core](2-practicas/ejercicio-02-sqlalchemy-core/README.md) | El motor y el pool, `text()`, `connect()` y `begin()`, `Table`, `insert`, `select`, `JOIN` y `GROUP BY`, `update`, `delete` y el SQL que se envía | 1 h 30 min |
| [03 · Modelos y sesiones con el ORM](2-practicas/ejercicio-03-modelos-y-sesiones-con-el-orm/README.md) | Dos modelos con relación, la sesión, el mapa de identidad, la unidad de trabajo, el problema N+1, cascada y `DetachedInstanceError` | 1 h 30 min |
| [04 · Migraciones con Alembic](2-practicas/ejercicio-04-migraciones-con-alembic/README.md) | `alembic init`, `--autogenerate`, una columna `NOT NULL` en una tabla con datos, un renombrado sin perder datos, `downgrade`, `--sql` y `check` | 1 h 30 min |

### Proyecto

Añades a tu Observatorio el módulo `core/database.py`, las migraciones y cuatro comandos:

- los modelos `Load` y `Reading`, con su clave foránea, su cascada y una convención de nombres;
- `save_series`, `load_series`, `list_loads`, `label_stats` y `delete_load`, sin commit, y las dos consultas de resumen en **una** consulta cada una;
- Alembic, con la URL fuera de `alembic.ini`, y la migración `0001`;
- `observatorio guardar`, `cargas`, `consultar [-c N]` y `borrar`, con errores que no enseñan la contraseña;
- un servicio `db` con PostgreSQL 18 en `compose.yaml`.

Por el camino, un refactor (`read_settings`). Después guardas 10 000 medidas, mides, y haces una prueba de mutación. La versión sube a `0.19.0`. **Es el único entregable de la semana.**
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
| Entrar en PostgreSQL | `docker compose exec db psql -U observatorio`; `\dt`, `\d tabla`, `\q` |
| Una consulta rápida sin entrar | `docker compose exec db psql -U observatorio -c 'SELECT count(*) FROM readings'` |
| Ver el SQL que genera una consulta | `print(query)`, o `make_engine(url, echo=True)` |
| Ver el SQL de las migraciones sin aplicarlas | `uv run alembic upgrade head --sql` |
| ¿Modelos y migraciones de acuerdo? | `uv run alembic check` |
| Empezar con la base vacía | `docker compose down -v` y `docker compose up -d --wait db` (borra **todos** tus datos) |
| Solo los tests de la base | `uv run pytest tests/test_database.py -q` |
| ¿Qué ocupa el puerto 5432? | `docker ps --format '{{.Names}} {{.Ports}}'` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-19` de `python-<nombre>-<apellido>` con:
   - `core/database.py` con los modelos, `LoadInfo`, `LabelStats` y las seis funciones, exportados desde `core`;
   - `alembic.ini` sin URL, `migrations/env.py` y la migración `0001_create_loads_and_readings.py`;
   - `database_url` en `Settings`, y `OBSERVATORIO_DATABASE_URL` en `.env.example`;
   - los comandos `guardar`, `cargas`, `consultar` y `borrar`, y la función `read_settings`;
   - `compose.yaml` con el servicio `db`, las dependencias `psycopg[binary]==3.3.6`, `sqlalchemy==2.1.6` y `alembic==1.20.1`, la versión `0.19.0` y al menos 6 tests propios en `tests/test_my_database.py`.

   Todo en verde en tu máquina y en Docker, con `ruff check`, `ruff format --check`, `mypy`, `coverage report` y `alembic check` sin avisos.
2. ✅ `README.md` del repositorio con los comandos nuevos y la sección "Base de datos"
3. ✅ Pull request `week-19` → `main` con:
   - tests, `mypy`, `ruff`, la cobertura y `alembic check`;
   - la tabla de tiempos del paso 14;
   - la tabla de mutantes y el test que mata al superviviente;
   - por qué las funciones de `database.py` no hacen commit, y por qué `list_loads` es una sola consulta.

El cuestionario de la [rúbrica](rubrica-evaluacion.md) es tu autoevaluación: respóndelo antes de mirar las respuestas.

---

## ✅ Verificación

En tu proyecto:

```bash
docker compose up -d --wait db
uv run pytest
uv run ruff check && uv run ruff format --check
uv run mypy
uv run coverage run -m pytest -q && uv run coverage report
uv run alembic upgrade head && uv run alembic check
uv run observatorio --version
uv run observatorio guardar medidas.txt && uv run observatorio consultar
docker compose run --build --rm app
```

Lo que debes ver:

- `db` sale `Healthy`;
- los tests terminan en `passed` sin `failed`, al menos 695;
- ruff dice `All checks passed!` y `N files already formatted`;
- `mypy` dice `Success: no issues found`;
- `coverage report` termina sin `Coverage failure`;
- `alembic check` dice `No new upgrade operations detected.`;
- `--version` escribe `observatorio 0.19.0`;
- `guardar` escribe `carga N: medidas.txt, ...` y `consultar`, la tabla `Etiquetas`.

En los ejercicios, cada paso descomentado da la salida que muestra su README, con los tiempos y los identificadores de tu máquina.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 18](../week-18-http_con_httpx_reintentos_secretos_y_env/README.md) | **Semana 19** | Semana 20 (próximamente) |
