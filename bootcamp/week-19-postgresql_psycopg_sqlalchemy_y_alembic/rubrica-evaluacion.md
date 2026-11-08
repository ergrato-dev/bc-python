# Rúbrica de Evaluación — Semana 19: PostgreSQL con psycopg, SQLAlchemy y Alembic

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 18 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | Un compañero escribe `conn.execute(f"SELECT * FROM loads WHERE source = '{nombre}'")`. ¿Qué puede pasar si `nombre` lo escribe un usuario? ¿Cómo lo arreglas, y por qué el arreglo funciona? | 10 |
| 2 | Una carga tiene tres medidas: 10, `NULL` y 20. ¿Qué devuelven `count(*)`, `count(value)` y `avg(value)`? ¿Y `WHERE value = NULL`? | 10 |
| 3 | `save_series` hace `flush` y no `commit`. ¿Qué diferencia hay? ¿Por qué la decisión de confirmar es de la CLI y no de `database.py`? Piensa en `guardar` y en los tests | 10 |
| 4 | ¿Qué es el problema N+1? Escribe cómo sería `list_loads` si lo tuviera, cuántas consultas haría con 500 cargas y los dos arreglos posibles | 10 |
| 5 | En `guardar`, `load_id = save_series(...).id` va **antes** de `session.commit()`. ¿Qué pasaría si leyeras `load.id` después del commit? ¿Por qué? | 10 |
| 6 | Añades a `Reading` una columna `unit: Mapped[str]` y generas la migración. En tu máquina, con la base vacía, `upgrade head` funciona; en la de un compañero, con datos, falla. ¿Qué error ve y cómo lo arreglas? | 10 |
| 7 | Renombras `label` a `name` en `Reading` y generas la migración con `--autogenerate`. ¿Qué escribe Alembic, qué pasaría si la aplicaras, y qué escribes en su lugar? | 10 |
| 8 | ¿Por qué `alembic.ini` no lleva la URL de la base? ¿De dónde la saca tu `env.py`, y de dónde cuando la ejecutan los tests? | 10 |
| 9 | La fixture `session` deja la base limpia después de cada test aunque el código haga `session.commit()`. ¿Cómo? ¿Por qué los tests de la CLI necesitan otra cosa, y qué hace `db_env`? | 10 |
| 10 | ¿Por qué los tests usan un PostgreSQL de verdad y no SQLite en memoria? ¿Por qué la base de pruebas se crea con las migraciones y no con `create_all`? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. Es una **inyección de SQL**: con `nombre = "x' OR '1'='1"`, la comilla del usuario cierra la del SQL y lo que sigue se ejecuta como SQL; devuelve todas las filas, y con otro texto podría borrar o leer lo que quisiera. Se arregla con un **parámetro**: `conn.execute("SELECT * FROM loads WHERE source = %s", (nombre,))` con psycopg, o `select(Load).where(Load.source == nombre)` con SQLAlchemy. Funciona porque el SQL y los valores viajan **por separado**: PostgreSQL analiza el SQL sin el valor, y después lo coloca como dato. Un valor nunca puede convertirse en SQL.
2. `count(*)` = **3** (cuenta filas), `count(value)` = **2** (no cuenta los `NULL`) y `avg(value)` = **15** (ignora el `NULL`: (10 + 20) / 2). `WHERE value = NULL` no encuentra **ninguna** fila, ni siquiera la del `NULL`: comparar con `NULL` da "desconocido", nunca verdadero. Se pregunta con `IS NULL`.
3. `flush` **envía** los `INSERT` dentro de la transacción abierta: PostgreSQL asigna el `id`, pero nada es definitivo y un `rollback` lo deshace. `commit` **confirma** la transacción. Si `database.py` confirmara, nadie podría combinar dos funciones en una sola transacción (guardar una carga y algo más, todo o nada), y los tests no podrían deshacerlo todo al terminar: la fixture `session` depende de que el código no confirme por su cuenta. Quien abre la sesión sabe cuándo termina el trabajo: `guardar` confirma una vez por archivo.
4. Es hacer **una consulta para la lista y otra más por cada elemento**: `for load in session.scalars(select(Load)): len(load.readings)` hace 1 + 500 = **501** consultas con 500 cargas, porque cada `load.readings` se carga perezosamente con su propio `SELECT`. Arreglos: cargar las relaciones de golpe con `options(selectinload(Load.readings))` (2 consultas), o, si solo quieres contar, que **cuente PostgreSQL** con `JOIN` y `GROUP BY` (1 consulta), que es lo que hace `list_loads`.
5. Costaría **una consulta más**. Por defecto (`expire_on_commit=True`), el commit **caduca** los objetos de la sesión, y el siguiente acceso a cualquier atributo los vuelve a leer de la base, porque otro programa pudo cambiarlos. Con miles de archivos, sería una consulta extra por archivo. Apuntando el `id` antes, no hay ninguna.
6. Ve `column "unit" of relation "readings" contains null values` (un `NotNullViolation`): la columna nueva es `NOT NULL`, y las filas que ya existían no tienen valor. Con la base vacía no hay filas y funciona, por eso no lo viste. Se arregla dando un **`server_default`** en el modelo y en la migración (`server_default="unidad"`), o en tres pasos: añadir la columna con `NULL`, rellenarla con un `UPDATE` (`op.execute`) y después cambiarla a `NOT NULL`. La migración no se aplica a medias: PostgreSQL la deshace entera.
7. Alembic solo compara dos fotos: ve que falta `name` y sobra `label`, y escribe `add_column("readings", ... "name" ...)` y `drop_column("readings", "label")`. Aplicada, **borraría todas las etiquetas**. En su lugar: `op.alter_column("readings", "label", new_column_name="name")` en `upgrade`, y el renombrado contrario en `downgrade`. Por eso cada migración se lee antes de aplicarla.
8. Porque la URL lleva la **contraseña**, y `alembic.ini` va a Git, como todo el proyecto. `env.py` la lee de `Settings().database_url`, es decir, de `OBSERVATORIO_DATABASE_URL` en el entorno o en `.env`, la misma que usa la CLI. Los tests no la necesitan: la fixture `engine` abre una conexión con la base de pruebas y se la pasa en `config.attributes["connection"]`, y `env.py` usa esa conexión en lugar de leer la configuración.
9. La fixture abre una transacción en la conexión (`connection.begin()`) y crea la sesión sobre esa conexión con `join_transaction_mode="create_savepoint"`: el `commit` del código solo confirma un **SAVEPOINT** dentro de la transacción de fuera, que la fixture deshace con `rollback` al terminar. La CLI, en cambio, abre **su propio** motor con `OBSERVATORIO_DATABASE_URL` y confirma de verdad: no hay transacción de fuera. `db_env` apunta la CLI a la base de pruebas, vacía las tablas antes del test con `TRUNCATE ... RESTART IDENTITY` (así la primera carga es la 1) y deja la carpeta de trabajo sin `.env`.
10. Porque SQLite **no es PostgreSQL**: no comprueba la longitud de un `varchar(100)`, tiene otros tipos, otros errores y otras transacciones. Un test que pasa con SQLite no dice nada de tu programa con PostgreSQL, y el programa siempre usa PostgreSQL. Las migraciones crean la base de pruebas porque así **cada ejecución de los tests prueba también la cadena de Alembic** desde cero; con `create_all`, una migración rota pasaría los tests y fallaría en la base de verdad. Y `test_the_migrations_match_the_models` comprueba que modelos y migraciones dicen lo mismo.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños | El historial de `week-19` muestra un commit por paso (tests, dependencias, esqueleto, `make_engine`, Alembic, primera migración, cada función, `read_settings`, comandos, versión, tests propios), sin cambiar los tests del bootcamp | 8 |
| Migraciones con cuidado | La migración `0001` está revisada (nombres de la convención, `ondelete`, `server_default`); `alembic check` sin cambios; ningún commit con la URL ni la contraseña fuera de `.env` | 8 |
| Ejecución en vivo | Ante el instructor: `docker compose up -d --wait db`, `uv run pytest`, `ruff`, `mypy`, `coverage report`, `alembic upgrade head`, `guardar`, `cargas`, `consultar -c`, `borrar`, una mirada con `psql`, y lo mismo en Docker | 8 |
| Rompe y explica | Cambia `outerjoin` por `join` y explica qué test falla y por qué; quita el `flush` de `save_series` y explica el fallo; apaga la base y enseña que el error no lleva la contraseña | 8 |
| Explica sus medidas | Explica sus tiempos del paso 14, cuántas sentencias envía `guardar` con 10 000 medidas, y qué mutante sobrevivió y cómo lo mata su test | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 18

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| Modelos y migración | `Load` y `Reading` tipados con `Mapped`, `NULL` solo en `value`, clave foránea con `ondelete="CASCADE"`, `UniqueConstraint`, índice, `server_default` en `created_at`; `naming_convention` en `Base`; `alembic.ini` sin URL, `env.py` con `Settings` y con la conexión de los tests; migración `0001` revisada | 20 |
| Funciones de `database.py` | `make_engine` con `pool_pre_ping`; `save_series` con `flush` y sin commit; `load_series` en orden de `position`; `list_loads` y `label_stats` en **una** consulta con `GROUP BY`; `delete_load` con cascada; sin leer el entorno; pasan los tests de `test_database.py` | 15 |
| Comandos | `read_settings` compartido con `descargar`; `database()` con mensajes sin contraseña y código 2 para configuración, conexión y tablas que faltan, y `dispose` al terminar; `guardar` con un commit por archivo, `cargas`, `consultar -c` y `borrar` con código 1 si la carga no existe | 15 |
| Tests propios | Al menos 6 tests en `tests/test_my_database.py` con datos del dominio y las fixtures de `db_fixtures.py`: ida y vuelta, `list_loads`, `label_stats` con valores que faltan, `delete_load`, un comando; al menos uno mata el mutante que sobrevive a los tests del bootcamp | 20 |
| Calidad | `ruff check`, `ruff format --check`, `mypy` (también `migrations/`), `coverage report` y `alembic check` sin avisos; `database.py` al 100 %; `docker compose run --build --rm app` en verde; dependencias fijadas; versión `0.19.0` | 10 |
| Git y README | Rama `week-19` en `python-<nombre>-<apellido>`; README con los comandos y la sección "Base de datos"; `.env` fuera de Git | 5 |
| Pull request | Descripción con tests, `mypy`, `ruff`, cobertura y `alembic check`, las tablas de tiempos y de mutantes, y las dos preguntas del paso 18 | 15 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | [Semana 20](../week-20-fastapi_lo_justo_para_servir_tu_proyecto/README.md) |
