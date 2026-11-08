# 03 · SQLAlchemy 2: motor, Core y ORM

⏱️ 55 min

## 🎯 Objetivos

- Situar las capas de SQLAlchemy: motor, Core, ORM, y psycopg debajo.
- Crear un motor y explicar qué hace su **pool** de conexiones.
- Declarar modelos tipados con `Mapped`, `mapped_column` y `relationship`.
- Trabajar con una `Session`: `add`, `flush`, `commit`, `rollback`.
- Explicar el mapa de identidad, la unidad de trabajo y la caducidad tras el commit.
- Reconocer el problema N+1 y resolverlo con `selectinload` o con un `GROUP BY`.

---

## 1. Las capas

![Las capas de SQLAlchemy: tu código, el ORM, el Core, el motor y su pool, psycopg y PostgreSQL](../0-assets/01-de-python-a-postgresql.svg)

SQLAlchemy tiene dos pisos sobre el *driver*:

- el **Core**: tablas descritas en Python y consultas que se construyen por partes (`select(...).where(...)`), que él traduce al SQL de cada base. Es el ejercicio 02;
- el **ORM** (*Object Relational Mapper*): clases cuyas instancias son filas, y una **sesión** que decide qué SQL enviar según lo que cambias en los objetos. Es el ejercicio 03 y tu proyecto.

El ORM está construido **sobre** el Core, y los dos usan el mismo motor. En tu proyecto conviven: los modelos son ORM, y `list_loads` o `label_stats` son consultas que piden columnas sueltas, no objetos.

## 2. El motor

```python
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg://usuario:clave@127.0.0.1:5432/observatorio")
```

La URL dice el **dialecto** (`postgresql`), el **driver** (`psycopg`, la teoría 02) y dónde conectar. En SQLAlchemy 2.1, `postgresql://` sin *driver* ya usa psycopg 3; escribirlo deja claro cuál es.

`create_engine` **no conecta**. Prepara un **pool**: un almacén de conexiones abiertas que se prestan y se devuelven. Abrir una conexión cuesta (un proceso nuevo en el servidor, la autenticación); reutilizarla, casi nada. Por defecto guarda hasta 5, y puede abrir 10 más en un pico.

| Opción | Para qué |
|---|---|
| `pool_pre_ping=True` | Antes de prestar una conexión, comprueba que sigue viva; si PostgreSQL se reinició, abre otra |
| `echo=True` | Escribe en el registro cada SQL que envía |
| `engine.dispose()` | Cierra todas las conexiones del pool; la CLI lo hace al terminar cada comando |

Al imprimir el motor o su URL, la contraseña sale como `***`. Aun así, la URL completa es un secreto: en tu proyecto llega en un `SecretStr` (teoría 04 de la semana 18).

## 3. Conexiones y transacciones

```python
from sqlalchemy import text

with engine.connect() as conn:        # lee: al salir, rollback
    total = conn.execute(text("SELECT count(*) FROM readings")).scalar_one()

with engine.begin() as conn:          # escribe: al salir, commit; con excepción, rollback
    conn.execute(text("DELETE FROM loads WHERE id = :id"), {"id": 3})
```

`text()` envuelve SQL escrito a mano, con parámetros **con nombre** (`:id`). Igual que en psycopg, los valores nunca se pegan.

## 4. El Core en una página

```python
from sqlalchemy import Column, Integer, MetaData, String, Table, func, select

metadata = MetaData()
stations = Table(
    "stations", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
)

query = select(stations.c.name).where(stations.c.id > 10).order_by(stations.c.name)
```

`stations.c.id > 10` no compara nada: construye un trozo de SQL, con el `10` como parámetro. Una consulta se puede ir completando (`query = query.where(...)`), que es justo lo que hace `label_stats` con `--carga`. `print(query)` enseña el SQL.

## 5. Modelos del ORM

```python
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Load(Base):
    __tablename__ = "loads"

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(500))
    readings: Mapped[list[Reading]] = relationship(back_populates="load")


class Reading(Base):
    __tablename__ = "readings"

    id: Mapped[int] = mapped_column(primary_key=True)
    load_id: Mapped[int] = mapped_column(ForeignKey("loads.id"))
    label: Mapped[str] = mapped_column(String(100))
    value: Mapped[float | None]
    load: Mapped[Load] = relationship(back_populates="readings")
```

- `Mapped[T]` dice el tipo de Python, y de él salen el tipo de SQL y el `NULL`: `Mapped[float | None]` es una columna `double precision` que admite `NULL`; `Mapped[str]`, una `NOT NULL`. mypy entiende estas anotaciones sin *plugin*: `reading.value` es `float | None`.
- `mapped_column(...)` añade lo que el tipo no dice: clave primaria, longitud, clave foránea, valor por defecto.
- `relationship` no es una columna: es un atributo de Python que lleva de una carga a sus medidas y al revés. La columna de verdad es `load_id`. `back_populates` enlaza los dos lados.
- `Base.metadata` reúne todas las tablas: es lo que Alembic compara con la base (teoría 04).

En Python 3.14 las anotaciones se evalúan cuando alguien las pide, así que `Mapped[list[Reading]]` funciona aunque `Reading` se defina después, sin comillas.

## 6. La sesión

La **sesión** es tu espacio de trabajo con la base: recuerda los objetos que cargaste, apunta lo que cambias y lo envía cuando toca.

```python
from sqlalchemy.orm import Session

with Session(engine) as session:
    load = Load(source="medidas.txt", readings=[Reading(label="Norte", value=12.5)])
    session.add(load)
    session.flush()      # envía los INSERT; PostgreSQL asigna load.id
    print(load.id)
    session.commit()     # confirma la transacción
```

| Método | Qué hace |
|---|---|
| `add(objeto)` | Lo mete en la sesión; con él, lo que cuelga de sus relaciones |
| `flush()` | Envía los cambios pendientes **sin** confirmar: los `id` ya existen, pero un `rollback` los deshace |
| `commit()` | `flush` y confirma la transacción |
| `rollback()` | Deshace todo lo no confirmado |
| `get(Load, 3)` | El objeto con esa clave primaria, o `None` |
| `scalars(select(Load))` | Un objeto por fila |
| `execute(select(Load.id, func.count(...)))` | Filas con columnas sueltas, no objetos |
| `delete(objeto)` | Lo borra en el siguiente `flush` |

Las funciones de tu `core/database.py` reciben la sesión y **no** hacen commit: hacen `flush` cuando necesitan el `id`. Quien abre la sesión (la CLI, la API, un test) decide cuándo se confirma. Así una función se puede combinar con otras dentro de la misma transacción, y un test puede deshacerlo todo al final (teoría 05).

Tres comportamientos que conviene conocer:

- **Mapa de identidad.** Dentro de una sesión, cada fila es un solo objeto: `session.get(Load, 1) is session.get(Load, 1)`, y el segundo `get` ni pregunta a PostgreSQL.
- **Unidad de trabajo.** Cambias atributos (`load.source = "otro.txt"`) y la sesión decide el SQL: un `UPDATE` con lo que cambió, en el siguiente `flush`.
- **Caducidad tras el commit.** Por defecto (`expire_on_commit=True`), el commit marca los objetos como caducados, y el siguiente acceso a un atributo los vuelve a leer: otro programa pudo cambiarlos. Por eso `guardar` apunta `load.id` **antes** del commit.

## 7. Cargar relaciones: el problema N+1

Por defecto, una relación se carga la primera vez que la tocas, con su propia consulta (carga **perezosa**). En un bucle, eso es una consulta por vuelta:

```python
for load in session.scalars(select(Load)):   # 1 consulta
    print(len(load.readings))                # +1 por cada carga
```

Con 1000 cargas, 1001 consultas. Es el error de rendimiento más habitual con un ORM, y no se ve leyendo el código: se ve contando el SQL (`echo=True`, o el contador del ejercicio 03). Dos arreglos:

- si necesitas los objetos, cárgalos de golpe: `select(Load).options(selectinload(Load.readings))` hace **2** consultas, sean 3 cargas o 1000;
- si solo quieres **contar**, que cuente PostgreSQL:

```python
select(Load.id, Load.source, func.count(Reading.id)).outerjoin(Load.readings).group_by(Load.id)
```

Es `list_loads`: una consulta, y a Python solo llega una fila por carga. `outerjoin` para que salgan también las cargas sin medidas, con 0. Un test de tu proyecto, `test_list_loads_is_one_query`, comprueba que es **una** consulta.

## 8. Insertar muchas filas

Con 10 000 medidas en una carga, la sesión no envía 10 000 `INSERT`. SQLAlchemy 2 agrupa las filas en `INSERT ... VALUES (...), (...), ...` de mil en mil: medido con tu proyecto, `save_series` con 10 000 medidas envía **11** sentencias, una para la carga y diez para las medidas. Por eso guardar 10 000 medidas tarda alrededor de un segundo y no un minuto.

## 9. Lo que sale de la sesión

Al cerrar la sesión, los objetos siguen existiendo con lo que ya tenían cargado, pero sin sesión no pueden cargar nada más:

```
DetachedInstanceError: Parent instance <Load at 0x...> is not bound to a Session; lazy load operation of attribute 'readings' cannot proceed
```

Por eso las funciones de tu proyecto que **consultan** devuelven valores sencillos e inmutables (`Series`, `LoadInfo`, `LabelStats`) y no modelos: lo que llega a la CLI no depende de que la sesión siga abierta.

---

## ⚠️ Errores comunes

| Error | Causa | Solución |
|---|---|---|
| El programa tarda más con cada fila nueva | N+1: una consulta por objeto en un bucle | `selectinload`, o un `GROUP BY` que cuente en PostgreSQL |
| `load.id` es `None` | Aún no se envió nada | `session.flush()` antes de leerlo |
| Leer `load.id` después del commit lanza otra consulta | Caducidad tras el commit | Apúntalo antes del commit |
| `DetachedInstanceError` | Usas un objeto con la sesión cerrada | Haz el trabajo dentro del `with`, o devuelve valores sencillos |
| `A transaction is already begun on this Session` | `session.begin()` después de haber consultado (la sesión ya abrió una sola) | `session.commit()` al terminar cada bloque, sin `begin()` |
| Una columna `str` admite `NULL` sin quererlo | `Mapped[str | None]` | `Mapped[str]` |

---

## ✅ Qué debes saber al terminar

- [ ] Qué hace cada capa: ORM, Core, motor y pool, psycopg.
- [ ] Qué significan `Mapped[float | None]`, `mapped_column(...)` y `relationship(...)`.
- [ ] La diferencia entre `flush` y `commit`, y por qué tus funciones no hacen commit.
- [ ] El mapa de identidad, la unidad de trabajo y la caducidad tras el commit.
- [ ] Qué es el problema N+1 y sus dos arreglos.
- [ ] Por qué las consultas del proyecto devuelven `LoadInfo` y no objetos `Load`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [02 · psycopg: conexiones, parámetros y transacciones](02-psycopg-conexiones-parametros-y-transacciones.md) | **03 · SQLAlchemy 2: motor, Core y ORM** | [04 · Alembic: migraciones del esquema](04-alembic-migraciones-del-esquema.md) |
