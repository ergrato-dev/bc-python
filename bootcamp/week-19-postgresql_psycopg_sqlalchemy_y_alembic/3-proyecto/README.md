# Proyecto — Observatorio, capa 18: guardar y consultar en PostgreSQL

⏱️ 6 h 30 min · Capa 18 del [proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md). **Único entregable de la semana.**

## Qué construyes

Hasta ahora, cada comando leía archivos y los olvidaba al terminar. Esta semana tu Observatorio **guarda**: cada archivo es una **carga** en PostgreSQL, con sus medidas, y PostgreSQL cuenta, agrupa y promedia sin traerlas a Python.

```
$ uv run observatorio guardar medidas.txt medidas.csv
carga 1: medidas.txt, 7 medidas
carga 2: medidas.csv, 7 medidas
$ uv run observatorio cargas
                       Cargas
┏━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Carga ┃ Origen      ┃ Fecha            ┃ Medidas ┃
┡━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━┩
│     1 │ medidas.txt │ 2026-11-08 10:02 │       7 │
│     2 │ medidas.csv │ 2026-11-08 10:02 │       7 │
└───────┴─────────────┴──────────────────┴─────────┘
$ uv run observatorio consultar --carga 1
                  Etiquetas
┏━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Etiqueta  ┃ Medidas ┃ Con valor ┃       Media ┃
┡━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ Centro    │       1 │         0 │    sin dato │
│ Norte     │       2 │         2 │ 30.7 unidad │
│ Occidente │       1 │         1 │ 61.0 unidad │
│ Oriente   │       1 │         1 │ 55.1 unidad │
│ Sur       │       2 │         2 │  8.8 unidad │
└───────────┴─────────┴───────────┴─────────────┘
```

| Comando o variable | Qué hace |
|---|---|
| `guardar ARCHIVOS...` | Guarda cada `.txt` o `.csv` como una carga nueva, cada una en su transacción |
| `cargas` | Lista las cargas: número, origen, fecha y medidas |
| `consultar [--carga N]`, `-c N` | Medidas, medidas con valor y media por etiqueta, de una carga o de todas |
| `borrar CARGA` | Borra una carga y sus medidas |
| `OBSERVATORIO_DATABASE_URL` | La URL de PostgreSQL, en el entorno o en `.env` |

Las tablas no las crea el programa: las crean las **migraciones** de Alembic.

```
src/observatorio/
├── cli.py            # + read_settings, database() y los comandos guardar, cargas, consultar, borrar
├── settings.py       # + database_url
└── core/
    ├── __init__.py   # + la API de database
    └── database.py   # nuevo: Base, Load, Reading, LoadInfo, LabelStats y sus funciones
migrations/           # nuevo: env.py y versions/0001_create_loads_and_readings.py
alembic.ini           # nuevo: la configuración de Alembic, sin la URL
tests/
├── db_fixtures.py    # nuevo: las fixtures de PostgreSQL (engine, session, db_env)
├── test_database.py  # nuevo: los tests del bootcamp
├── test_my_database.py  # nuevo: los tuyos
├── conftest.py       # + importa las fixtures de db_fixtures.py
├── test_package.py   # modificado: el módulo database, las dependencias, migrations y 0.19.0
└── test_remote.py    # modificado: clean_env quita también OBSERVATORIO_DATABASE_URL
compose.yaml          # modificado: + el servicio db, PostgreSQL 18
.env.example          # + OBSERVATORIO_DATABASE_URL
```

`core/database.py` recibe la URL y la sesión como argumentos, como `remote.py` recibe el token: no lee el entorno. Y sus funciones **no hacen commit**: lo decide quien abre la sesión.

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-19`. El `starter/` trae la capa 17 resuelta. **Tú** escribes `core/database.py`, las migraciones y los cuatro comandos.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-18` está fusionado en `main`. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-19
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-19-postgresql_psycopg_sqlalchemy_y_alembic/3-proyecto/starter
cp $STARTER/tests/test_database.py $STARTER/tests/db_fixtures.py $STARTER/tests/test_my_database.py tests/
cp $STARTER/tests/test_package.py $STARTER/tests/test_remote.py tests/
cp $STARTER/compose.yaml .
cat $STARTER/.env.example
git status --short
```

Copias estos archivos:

- **Nuevos:**
  - `tests/test_database.py`, con 57 tests de `database.py`, de las migraciones, de `Settings` y de los comandos;
  - `tests/db_fixtures.py`, las fixtures de PostgreSQL (teoría 05);
  - `tests/test_my_database.py`, con un ejemplo.
- **Modificados:**
  - `test_package.py`, que espera el módulo `database`, su API en `core`, `alembic.ini` y `migrations/` en la raíz, las tres dependencias nuevas, `migrations` en mypy y la versión `0.19.0`;
  - `test_remote.py`, cuya `clean_env` quita también `OBSERVATORIO_DATABASE_URL`;
  - `compose.yaml`, con el servicio `db` y la imagen `week-19`. Léelo entero: cada línea tiene su comentario (teoría 01, sección 7).

`.env.example` **no** lo copies encima del tuyo: añade a tu `.env.example` y a tu `.env` las tres últimas líneas que acabas de ver con `cat`.

### 3. Dependencias, PostgreSQL y tests en rojo

```bash
uv run pytest
```

```
E   ModuleNotFoundError: No module named 'sqlalchemy'
...
!!!!!!!!!!!!!!!!!!! Interrupted: 3 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Añade las dependencias, con la versión fijada (`docs/stack-versions.md`, con su fecha y su revisión de avisos de seguridad):

```bash
uv add "psycopg[binary]==3.3.6" sqlalchemy==2.1.6 alembic==1.20.1
```

`uv add` trae también `psycopg-binary` (el *driver* con `libpq` dentro, teoría 02), `mako` y `markupsafe` (las plantillas de Alembic). Míralos en `uv.lock`.

Y arranca PostgreSQL:

```bash
docker compose up -d --wait db
docker compose ps
uv run pytest
```

```
NAME                              IMAGE                  ...   STATUS
python-<nombre>-<apellido>-db-1   postgres:18.6-alpine   ...   Up 5 seconds (healthy)
...
E   ImportError: cannot import name 'make_engine' from 'observatorio.core' (...)
...
!!!!!!!!!!!!!!!!!!! Interrupted: 3 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Lee `tests/db_fixtures.py` y `tests/test_database.py` antes de escribir nada. Fíjate en (teoría 05):

- la fixture `engine` **borra y crea** la base `observatorio_test` y le aplica tus migraciones, una vez por ejecución;
- la fixture `session` mete cada test en una transacción que se deshace al terminar;
- `db_env` apunta la CLI a la base de pruebas y vacía las tablas antes de cada test;
- `count_queries` cuenta el SQL que se envía: dos tests exigen **una** consulta.

### 4. El esqueleto: `database.py`, `Settings` y la API

Crea `src/observatorio/core/database.py` con un *docstring* de módulo (qué, para qué, impacto), y:

```python
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Engine,
    ForeignKey,
    String,
    UniqueConstraint,
    create_engine,
    func,
    select,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

from observatorio.core.model import Measurement, Series


class Base(DeclarativeBase):
    """La base de los modelos: su `metadata` reúne las tablas, y Alembic la compara."""


class Load(Base):
    """Una carga: las medidas de un archivo guardadas de una vez."""

    __tablename__ = "loads"

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(500))
    # server_default: la hora la pone PostgreSQL al insertar, con zona horaria.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    # cascade: las medidas viajan con su carga; al borrar la carga, se borran con ella.
    readings: Mapped[list[Reading]] = relationship(
        back_populates="load", cascade="all, delete-orphan", order_by="Reading.position"
    )


class Reading(Base):
    """Una medida de una carga, en su posición dentro del archivo."""

    __tablename__ = "readings"
    # Dos medidas de una misma carga no pueden ocupar la misma posición.
    __table_args__ = (UniqueConstraint("load_id", "position"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    # ondelete="CASCADE": PostgreSQL borra las medidas aunque se borre la carga con SQL a mano.
    load_id: Mapped[int] = mapped_column(ForeignKey("loads.id", ondelete="CASCADE"), index=True)
    position: Mapped[int]
    label: Mapped[str] = mapped_column(String(100))
    # `float | None`: la columna admite NULL, que es "sin dato".
    value: Mapped[float | None]

    load: Mapped[Load] = relationship(back_populates="readings")


@dataclass(frozen=True, slots=True)
class LoadInfo:
    """Una fila de la lista de cargas: número, origen, fecha y cuántas medidas tiene."""

    id: int
    source: str
    created_at: datetime
    measurements: int


@dataclass(frozen=True, slots=True)
class LabelStats:
    """El resumen de una etiqueta: medidas, medidas con valor y media de los valores."""

    label: str
    measurements: int
    with_value: int
    mean: float | None


def make_engine(url: str, *, echo: bool = False) -> Engine:
    """El motor de una URL como postgresql+psycopg://usuario:clave@host:5432/base."""
    raise NotImplementedError


def save_series(session: Session, source: str, series: Series) -> Load:
    """Añade una carga con las medidas de `series` y la devuelve con su `id` ya asignado."""
    raise NotImplementedError


def load_series(session: Session, load_id: int) -> Series | None:
    """Las medidas de una carga, en su orden, o None si no existe."""
    raise NotImplementedError


def list_loads(session: Session) -> list[LoadInfo]:
    """Todas las cargas, de la más antigua a la más nueva, con cuántas medidas tiene cada una."""
    raise NotImplementedError


def label_stats(session: Session, load_id: int | None = None) -> list[LabelStats]:
    """Medidas, medidas con valor y media por etiqueta, de una carga o de todas."""
    raise NotImplementedError


def delete_load(session: Session, load_id: int) -> bool:
    """Borra una carga y sus medidas; False si no existía."""
    raise NotImplementedError
```

Los modelos ya están completos: describen las tablas y no hay nada que "implementar". Repásalos con la teoría 03: qué columna admite `NULL`, qué hace cada argumento de `relationship`, por qué `position`. Y fíjate en lo que devuelven las funciones que consultan: `LoadInfo` y `LabelStats`, valores inmutables, no modelos (teoría 03, sección 9).

En `settings.py`, un campo más:

```python
    # SecretStr: la URL lleva la contraseña, y no debe salir en un registro ni en un error.
    database_url: SecretStr | None = None
```

En `core/__init__.py`, importa `Base`, `LabelStats`, `Load`, `LoadInfo`, `Reading`, `delete_load`, `label_stats`, `list_loads`, `load_series`, `make_engine` y `save_series` de `observatorio.core.database`, y añádelos a `__all__`.

Y en `tests/conftest.py`, que es tuyo, importa las fixtures de PostgreSQL para que lleguen a todos los tests (teoría 05, sección 6), debajo de los otros imports:

```python
# Las fixtures de PostgreSQL (semana 19): importarlas aquí las ofrece a todos los tests.
from db_fixtures import db_env, engine, session

__all__ = ["db_env", "engine", "session"]
```

```bash
uv run ruff check --fix
uv run pytest
```

```
13 failed, 544 passed, 41 errors
```

Los 41 errores son los tests que piden una base: la fixture `engine` llama a `make_engine`.

### 5. `make_engine`

```python
    return create_engine(url, echo=echo, pool_pre_ping=True)
```

`pool_pre_ping` comprueba cada conexión antes de prestarla: si PostgreSQL se reinició, el pool abre otra en lugar de darte una muerta (teoría 03, sección 2). Añade al *docstring* qué hacen `pool_pre_ping` y `echo`.

```
9 failed, 548 passed, 41 errors
```

Los errores siguen: ahora la fixture llega a `command.upgrade(...)` y Alembic no existe todavía.

```
E   alembic.util.exc.CommandError: No 'script_location' key found in configuration.
```

### 6. Alembic

```bash
uv run alembic init migrations
```

```
...
Please edit configuration/connection/logging settings in /.../alembic.ini before proceeding.
```

**En `alembic.ini`**, tres cambios (teoría 04, sección 3):

1. Borra la línea `sqlalchemy.url = driver://user:pass@localhost/dbname` y pon en su lugar:

   ```ini
   # Sin sqlalchemy.url: la URL lleva una contraseña y este archivo va a Git. migrations/env.py
   # la lee de OBSERVATORIO_DATABASE_URL, del entorno o de .env.
   ```

2. Debajo de las líneas `# file_template = ...` comentadas, añade:

   ```ini
   # Nombres como 0001_create_loads_and_readings.py: el número de la revisión y lo que hace.
   file_template = %%(rev)s_%%(slug)s
   ```

3. En `[post_write_hooks]`, debajo de los ejemplos comentados de ruff, añade:

   ```ini
   # Cada migración nueva sale ya corregida y formateada por ruff, como el resto del código.
   hooks = ruff_check, ruff_format
   ruff_check.type = module
   ruff_check.module = ruff
   ruff_check.options = check --fix REVISION_SCRIPT_FILENAME
   ruff_format.type = module
   ruff_format.module = ruff
   ruff_format.options = format REVISION_SCRIPT_FILENAME
   ```

**`migrations/env.py`**: sustituye el que generó `alembic init` por este, que lee la URL de `Settings` y acepta la conexión que le pasan los tests:

```python
"""Alembic: con qué base de datos y con qué modelos se ejecutan las migraciones.

Qué: lee la URL de Settings (OBSERVATORIO_DATABASE_URL) y compara con Base.metadata.
Para qué: `alembic revision --autogenerate` saca de los modelos lo que falta en la base,
y `alembic upgrade head` lo aplica, siempre con la misma URL que usa la CLI.
Impacto: los tests pasan su propia conexión en config.attributes["connection"]; así
migran la base de pruebas sin tocar tu .env ni el registro de pytest.
"""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import Connection

from observatorio.core.database import Base, make_engine
from observatorio.settings import Settings

config = context.config
connection: Connection | None = config.attributes.get("connection")

# El registro de alembic.ini, solo desde la terminal: en los tests lo configura pytest.
if config.config_file_name is not None and connection is None:
    fileConfig(config.config_file_name, disable_existing_loggers=False)


def database_url() -> str:
    """La URL de OBSERVATORIO_DATABASE_URL; sin ella no hay nada que migrar."""
    url = Settings().database_url
    if url is None:
        raise SystemExit("error: falta OBSERVATORIO_DATABASE_URL (en el entorno o en .env)")
    return url.get_secret_value()


def run_migrations(connection: Connection) -> None:
    """Aplica las migraciones pendientes en una transacción de esa conexión."""
    context.configure(connection=connection, target_metadata=Base.metadata)
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    # `alembic upgrade head --sql`: escribe el SQL en pantalla en lugar de ejecutarlo.
    context.configure(url=database_url(), target_metadata=Base.metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
elif connection is not None:
    run_migrations(connection)
else:
    with make_engine(database_url()).connect() as new_connection:
        run_migrations(new_connection)
```

Por último, que mypy revise también `env.py` y las migraciones. En `pyproject.toml`:

```toml
files = ["src", "tests", "migrations"]
```

```bash
uv run mypy
uv run pytest
```

```
Success: no issues found in 59 source files
...
36 failed, 551 passed, 11 errors
```

Ya no hay errores de configuración: Alembic aplica... ninguna migración, porque no hay. Los tests fallan con `relation "loads" does not exist`.

### 7. Nombres fijos y la primera migración

Antes de la primera migración, la convención de nombres de las restricciones (teoría 04, sección 5). En `database.py`, importa `MetaData` y dale a `Base` su `metadata`:

```python
class Base(DeclarativeBase):
    """La base de los modelos: su `metadata` reúne las tablas, y Alembic la compara."""

    # Nombres fijos para índices y restricciones (pk_loads, fk_readings_load_id_loads...).
    # Sin ellos, PostgreSQL inventa uno, y una migración futura no sabría cuál borrar.
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )
```

Ahora genera la migración contra tu base de desarrollo, la de `.env`:

```bash
uv run alembic revision --autogenerate --rev-id 0001 -m "create loads and readings"
```

```
...
INFO  [alembic.autogenerate.compare.tables] Detected added table 'loads'
INFO  [alembic.autogenerate.compare.tables] Detected added table 'readings'
INFO  [alembic.autogenerate.compare.constraints] Detected added index 'ix_readings_load_id' on '('load_id',)'
Generating .../migrations/versions/0001_create_loads_and_readings.py ...  done
Running post write hook 'ruff_check' ...
...
```

**Léela** antes de aplicar nada. Busca en ella: las dos tablas, `nullable=True` solo en `value`, `server_default=sa.text("now()")`, la clave foránea con `ondelete="CASCADE"`, la restricción única, el índice, y los nombres (`pk_loads`, `fk_readings_load_id_loads`, `uq_readings_load_id_position`). Y el `downgrade()`, que lo deshace en el orden contrario. Si algo no cuadra con los modelos, se arregla en los modelos y se vuelve a generar.

```bash
uv run alembic upgrade head
uv run alembic current
docker compose exec db psql -U observatorio -c '\d readings'
uv run pytest
```

```
INFO  [alembic.runtime.migration] Running upgrade  -> 0001, create loads and readings
...
0001 (head)
...
Indexes:
    "pk_readings" PRIMARY KEY, btree (id)
    "ix_readings_load_id" btree (load_id)
    "uq_readings_load_id_position" UNIQUE CONSTRAINT, btree (load_id, "position")
Foreign-key constraints:
    "fk_readings_load_id_loads" FOREIGN KEY (load_id) REFERENCES loads(id) ON DELETE CASCADE
...
40 failed, 558 passed
```

Los cinco tests de migraciones ya pasan: la de pruebas se crea con **tu** migración en cada ejecución.

### 8. `save_series` y `load_series`

`save_series` crea la carga con sus medidas, la añade a la sesión y hace `flush`, **no** `commit`:

```python
    load = Load(
        source=source,
        readings=[
            Reading(position=position, label=measurement.label, value=measurement.value)
            for position, measurement in enumerate(series)
        ],
    )
    session.add(load)
    # flush envía los INSERT sin confirmar la transacción: así PostgreSQL asigna el id.
    session.flush()
    return load
```

`load_series` busca la carga por su clave primaria con `session.get(Load, load_id)`; si es `None`, devuelve `None`; si no, una `Series` con un `Measurement(reading.label, reading.value)` por cada medida de `load.readings`, que ya llegan en orden gracias al `order_by` de la relación.

```
27 failed, 571 passed
```

Fíjate en `test_save_series_does_not_commit`: cambia `session.commit` por una función que falla. Si haces commit dentro, la CLI no podría combinar varias funciones en una transacción, y los tests no podrían deshacerlo todo al final.

### 9. `list_loads`

Una sola consulta, con `JOIN` y `GROUP BY` (teoría 03, sección 7):

```python
    # Una sola consulta con JOIN y GROUP BY: sin traer las medidas a Python (N+1).
    query = (
        select(Load.id, Load.source, Load.created_at, func.count(Reading.id))
        .outerjoin(Load.readings)
        .group_by(Load.id)
        .order_by(Load.id)
    )
    return [LoadInfo(*row) for row in session.execute(query)]
```

`outerjoin` y no `join`: una carga vacía sale con 0 medidas, en lugar de desaparecer. `group_by(Load.id)` basta para poder pedir también `source` y `created_at`: PostgreSQL sabe que dependen de la clave primaria.

```
24 failed, 574 passed
```

### 10. `label_stats`

La consulta de `consultar`:

```python
    # count(value) no cuenta los NULL, y avg los ignora: lo mismo que hace el Observatorio
    # con los "sin dato".
    query = (
        select(
            Reading.label,
            func.count(Reading.id),
            func.count(Reading.value),
            func.avg(Reading.value),
        )
        .group_by(Reading.label)
        .order_by(Reading.label)
    )
```

Si `load_id` no es `None`, añade `.where(Reading.load_id == load_id)` a `query`, y devuelve un `LabelStats(*row)` por fila, como en el paso 9. Una consulta que se completa por partes, sin pegar textos (teoría 03, sección 4).

```
19 failed, 579 passed
```

### 11. `delete_load`

Busca la carga con `session.get`; si no existe, `False`. Si existe, `session.delete(load)`, `session.flush()` y `True`. La relación, con `cascade="all, delete-orphan"`, borra antes sus medidas.

```
17 failed, 581 passed
```

Los 17 que quedan son de la CLI, y uno de la versión.

### 12. La CLI

**Un refactor primero.** `descargar` lee `Settings` y convierte un `ValidationError` en un mensaje con código 2. Los comandos nuevos necesitan lo mismo: saca esas líneas a una función, y que `descargar` la use.

```python
def read_settings() -> Settings:
    """La configuración de OBSERVATORIO_* y .env; si no es válida, sale con código 2."""
    try:
        return Settings()
    except ValidationError as problem:
        first = problem.errors()[0]
        name = f"OBSERVATORIO_{str(first['loc'][0]).upper()}"
        raise fail(f"configuración no válida: {name}: {first['msg']}", 2) from None
```

**Una sesión para cada comando.** Un gestor de contexto que abre el motor y la sesión, traduce los problemas de conexión a mensajes sin contraseña y lo cierra todo al terminar:

```python
@contextmanager
def database() -> Iterator[Session]:
    """Una sesión con la base de OBSERVATORIO_DATABASE_URL, que se cierra al salir.

    Los problemas de configuración o de conexión salen con código 2 y un mensaje sin la
    contraseña; los demás errores de la base de datos llegan como siempre.
    """
    settings = read_settings()
    if settings.database_url is None:
        raise fail("falta OBSERVATORIO_DATABASE_URL (en el entorno o en .env)", 2)
    url = settings.database_url.get_secret_value()
    try:
        engine = make_engine(url)
    except ArgumentError:
        raise fail("OBSERVATORIO_DATABASE_URL no es una URL de base de datos válida", 2) from None
    try:
        with Session(engine) as session:
            yield session
    except OperationalError:
        # Solo el servidor y el puerto: el texto del error podría llevar el usuario.
        where = make_url(url)
        raise fail(f"no se pudo conectar con PostgreSQL en {where.host}:{where.port}", 2) from None
    except ProgrammingError as problem:
        if isinstance(problem.orig, UndefinedTable):
            raise fail("faltan las tablas: ejecuta `uv run alembic upgrade head`", 2) from None
        raise
    finally:
        # Cierra las conexiones del pool: la CLI termina enseguida y no las reutiliza.
        engine.dispose()
```

Necesitas `Iterator` (de `collections.abc`), `contextmanager` (de `contextlib`), `make_url` (de `sqlalchemy`), `ArgumentError`, `OperationalError` y `ProgrammingError` (de `sqlalchemy.exc`), `Session` (de `sqlalchemy.orm`) y `UndefinedTable` (de `psycopg.errors`). `from None` corta la traza encadenada: el usuario ve el mensaje, no veinte líneas de psycopg.

**Los cuatro comandos**, cada uno dentro de `with database() as session:`:

- `guardar(archivos)`: `typer.Argument(metavar="ARCHIVOS", ...)`. Para cada ruta, `Series.from_lines(open_file(path).lines())`; con `DataFileError`, `error: ...` a stderr, cuenta el fallo y sigue con la siguiente. Si se leyó, `load_id = save_series(session, str(path), series).id`, **después** `session.commit()` (un commit por archivo: si el siguiente falla, este ya está guardado) y escribe `carga {load_id}: {path}, {len(series)} medidas`. Apunta el `id` **antes** del commit: después, leerlo costaría una consulta (teoría 03, sección 6). Al final, `typer.Exit(1)` si falló alguno.
- `cargas()`: `list_loads`. Sin cargas, escribe `no hay cargas: guarda una con \`observatorio guardar\``. Con cargas, una tabla `Cargas` con las columnas `Carga` (derecha), `Origen`, `Fecha` (`f"{load.created_at:%Y-%m-%d %H:%M}"`) y `Medidas` (derecha).
- `consultar(carga)`: opción `--carga`/`-c`, `int | None`. Si hay `carga` y `session.get(Load, carga)` es `None`, `fail(f"no existe la carga {carga}", 1)`. Si no, una tabla `Etiquetas` con `Etiqueta`, `Medidas`, `Con valor` y `Media` (las tres a la derecha), con la media como en `files_table`: `"sin dato"` o `f"{mean:.1f} {UNIT}"`.
- `borrar(carga)`: `typer.Argument(metavar="CARGA", ...)`. Si `delete_load` devuelve `False`, `fail(f"no existe la carga {carga}", 1)`; si no, `session.commit()` y `carga {carga} borrada`.

Escribe en el *docstring* de `guardar` de qué variable lee la configuración, como en `descargar`, y añade los comandos al *docstring* del módulo.

```bash
uv run observatorio --help
uv run pytest
```

```
...
│ guardar    Guarda cada archivo en PostgreSQL como una carga nueva, en su     │
│            propia transacción.                                               │
│ cargas     Lista las cargas guardadas: número, origen, fecha y medidas.      │
│ consultar  Resume por etiqueta las medidas guardadas: PostgreSQL agrupa,     │
│            cuenta y promedia.                                                │
│ borrar     Borra una carga y todas sus medidas.                              │
...
1 failed, 597 passed
```

### 13. La versión

```bash
uv version --bump minor
uv run observatorio --version
uv run pytest
```

```
observatorio 0.19.0
...
598 passed
```

### 14. Usar de verdad, y medir

Guarda tus archivos en la base de desarrollo y mira qué hay dentro:

```bash
uv run observatorio guardar medidas.txt medidas.csv
uv run observatorio cargas
uv run observatorio consultar
docker compose exec db psql -U observatorio -c 'SELECT load_id, count(*), count(value) FROM readings GROUP BY load_id'
uv run observatorio borrar 2
uv run observatorio consultar -c 2; echo $?
```

```
...
error: no existe la carga 2
1
```

Prueba tres fallos, y comprueba que ninguno enseña la contraseña:

```bash
OBSERVATORIO_DATABASE_URL=nada uv run observatorio cargas; echo $?
OBSERVATORIO_DATABASE_URL=postgresql+psycopg://observatorio:observatorio@127.0.0.1:5999/observatorio uv run observatorio cargas; echo $?
uv run alembic downgrade base && uv run observatorio cargas; uv run alembic upgrade head
```

```
error: OBSERVATORIO_DATABASE_URL no es una URL de base de datos válida
2
error: no se pudo conectar con PostgreSQL en 127.0.0.1:5999
2
...
error: faltan las tablas: ejecuta `uv run alembic upgrade head`
...
```

Una variable del entorno gana a `.env` (semana 18): así pruebas otra URL sin tocar tu `.env`. Y el `downgrade base` borró tus cargas con las tablas: vuelve a guardarlas.

Ahora mide. Crea un archivo de 10 000 medidas con tu dominio:

```bash
uv run python -c "
import random
random.seed(1)
labels = ['Norte', 'Sur', 'Este']
lines = [f'{random.choice(labels)};{random.uniform(0, 60):.1f}'.replace('.', ',') for _ in range(10_000)]
open('grande.txt', 'w').write('\n'.join(lines) + '\n')
"
time uv run observatorio --version
time uv run observatorio guardar grande.txt
time uv run observatorio consultar
```

Rellena la tabla con tus tiempos (`real`):

| Orden | Tiempo | Menos el arranque |
|---|---|---|
| `--version` (el arranque) | | — |
| `guardar grande.txt` (10 000 medidas) | | |
| `consultar` (todas las cargas) | | |

En mi máquina, dentro de Docker: arranque 1,2 s, `guardar` 2,4 s (1,2 s para las 10 000 medidas) y `consultar` 1,3 s (casi solo el arranque). Las 10 000 medidas viajan en **11** sentencias SQL (una para la carga y diez `INSERT` de mil medidas, teoría 03, sección 8), y `consultar` hace que PostgreSQL agrupe todo sin mandar ninguna medida a Python.

Antes de seguir, `rm grande.txt`: no va a Git.

### 15. Calidad y cobertura

```bash
uv run ruff check && uv run ruff format --check
uv run mypy
uv run coverage run -m pytest -q && uv run coverage report
uv run alembic check
```

`database.py`, `settings.py` y `cli.py` deben salir al 100 %. `alembic check` debe decir `No new upgrade operations detected.`

### 16. Una prueba de mutación

Haz cada cambio, **uno cada vez**, ejecuta `uv run pytest -x -q` y deshazlo con `git checkout <archivo>`:

| Archivo | Mutante | ¿Lo detectan? |
|---|---|---|
| `database.py` | `enumerate(series)` por `enumerate(series, 1)` | |
| `database.py` | `.outerjoin(Load.readings)` por `.join(Load.readings)` | |
| `database.py` | `func.count(Reading.value)` por `func.count(Reading.id)` | |
| `database.py` | quita el `session.flush()` de `save_series` | |
| `database.py` | quita `ondelete="CASCADE"` | |
| `database.py` | `order_by="Reading.position"` por `order_by="Reading.id"` | |
| `cli.py` | quita el `session.commit()` de `guardar` | |
| `cli.py` | `{where.host}:{where.port}` por `{url}` en `database()` | |

Siete mueren. Uno **sobrevive**: ¿cuál, y por qué ningún test del bootcamp lo ve? Pista: ¿en qué orden asigna PostgreSQL los `id` de las medidas que guarda `save_series`? Lo vas a matar en el paso siguiente.

### 17. Tus tests

En `tests/test_my_database.py`, sustituye el ejemplo por **al menos 6 tests** con medidas de **tu dominio** y las fixtures `session`, `engine` y `db_env`:

- `save_series` y `load_series` de ida y vuelta, con un valor que falta;
- `list_loads` con dos cargas, una de ellas vacía;
- `label_stats` con una etiqueta que solo tiene valores que faltan: `mean` es `None`;
- `delete_load`, y que las medidas de la otra carga siguen ahí;
- un comando de la CLI con `CliRunner` y `db_env`;
- el mutante que sobrevivió en el paso 16.

Para el último, guarda una carga cuyas medidas tengan los `id` en un orden **distinto** de sus `position`: crea tú el `Load` con `Reading(position=2, ...)`, `Reading(position=0, ...)` y `Reading(position=1, ...)`, en ese orden, `session.add` y `session.flush()`. Después, `session.expire_all()` (para que la relación se vuelva a leer de la base) y comprueba que `load_series` las devuelve por `position`.

Al final, al menos 695 tests en verde.

### 18. Contenedor, README y pull request

```bash
docker compose run --build --rm app
docker compose run --rm app alembic upgrade head
docker compose run --rm app observatorio guardar medidas.txt
docker compose run --rm app observatorio cargas
```

`app` espera a que `db` esté sano y usa las URLs de `compose.yaml`, con el servidor `db`: los tests van contra `observatorio_test` y los comandos contra `observatorio`, la misma base que usas desde tu máquina.

En el `README.md` de tu repositorio, añade los cuatro comandos y una sección "Base de datos": `docker compose up -d --wait db`, `uv run alembic upgrade head`, y la variable `OBSERVATORIO_DATABASE_URL` en `.env`.

Commits sugeridos, en este orden:

1. `test: add database tests and fixtures`
2. `build: add psycopg, sqlalchemy and alembic, and a postgres service`
3. `feat: add the database models and api skeleton`
4. `feat: add make_engine`
5. `build: set up alembic`
6. `feat: add naming convention and first migration`
7. `feat: save and load series`
8. `feat: list loads with one query`
9. `feat: add label stats`
10. `feat: delete loads`
11. `refactor: extract read_settings`
12. `feat: add guardar, cargas, consultar and borrar commands`
13. `chore: bump version to 0.19.0`
14. `test: add my database tests`

Antes de cada `git add`, un `git status --short`: ni `.env` ni `grande.txt`. Al final:

```bash
git push -u origin week-19
```

En GitHub, abre un *pull request* de `week-19` hacia `main` con:

1. La salida de `uv run pytest`, `uv run mypy`, `uv run ruff check`, `uv run coverage report` y `uv run alembic check`.
2. La tabla de tiempos del paso 14.
3. La tabla de mutantes del paso 16, y el test con el que mataste al superviviente.
4. Por qué las funciones de `database.py` no hacen commit, y por qué `list_loads` es una sola consulta.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `no hay PostgreSQL en 127.0.0.1:5432: arráncalo con ...` | `docker compose up -d --wait db` |
| `Bind for 127.0.0.1:5432 failed: port is already allocated` | Tienes otro PostgreSQL en el 5432 (¿el de otro proyecto?): `docker ps` y páralo |
| `fixture 'session' not found` | Falta el import de `db_fixtures` en tu `conftest.py` (paso 4) |
| `No 'script_location' key found in configuration` | Falta el paso 6: `alembic init migrations` |
| `error: falta OBSERVATORIO_DATABASE_URL` al usar `alembic` | No la añadiste a tu `.env` (paso 2) |
| `relation "loads" does not exist` en los tests | No hay migración en `migrations/versions/`, o está vacía: paso 7 |
| La migración sale vacía (`pass`) | Ya aplicaste las tablas en tu base de desarrollo, o `env.py` no usa `Base.metadata` |
| `Can't locate revision identified by '0001'` | Tu base de desarrollo tiene una revisión que no está en tu `versions/` (otra rama, otro proyecto): `docker compose down -v` y `up -d --wait db` la dejan vacía |
| `test_there_is_one_head_and_it_is_0001` falla | Generaste la migración sin `--rev-id 0001`, o hay dos: borra `versions/`, `docker compose down -v`, y repite el paso 7 |
| `test_list_loads_counts_measurements` pierde la carga vacía | `join` en lugar de `outerjoin` |
| `test_save_series_assigns_an_id` da `assert False` | Falta el `session.flush()` |
| `A transaction is already begun on this Session` | Usas `session.begin()` en un comando: con `session.commit()` al final de cada bloque basta |
| `guardar` da `carga 3` en lugar de `carga 1` en tus tests | Usa la fixture `db_env`, que reinicia los números |
| `docker compose run` da `dependency failed to start: container ... db-1 is unhealthy` | PostgreSQL no arrancó: `docker compose logs db` |

## Entrega

- Rama `week-19` de `python-<nombre>-<apellido>` con:
  - `core/database.py` con `Base`, `Load`, `Reading`, `LoadInfo`, `LabelStats`, `make_engine`, `save_series`, `load_series`, `list_loads`, `label_stats` y `delete_load`, exportados desde `core`;
  - `alembic.ini` sin URL, `migrations/env.py` y la migración `0001_create_loads_and_readings.py`;
  - `database_url` en `Settings`, y `OBSERVATORIO_DATABASE_URL` en `.env.example`;
  - los comandos `guardar`, `cargas`, `consultar` y `borrar`, y la función `read_settings`;
  - `compose.yaml` con el servicio `db`, la versión `0.19.0` y al menos 6 tests propios en `tests/test_my_database.py`.

  Todo en verde, también en Docker, con `ruff check`, `ruff format --check`, `mypy`, `coverage report` y `alembic check` sin avisos.
- `README.md` del repositorio con los comandos nuevos y la sección "Base de datos".
- *Pull request* `week-19` → `main` con la descripción del paso 18.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · Migraciones con Alembic](../2-practicas/ejercicio-04-migraciones-con-alembic/README.md) | **Proyecto · Observatorio, capa 18** | [Webgrafía](../4-recursos/webgrafia/README.md) |
