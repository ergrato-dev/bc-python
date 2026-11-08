# Ejercicio 03 — Modelos y sesiones con el ORM

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-sqlalchemy-2-motor-core-y-orm.md)

## Objetivo

Trabajar con filas como si fueran objetos de Python, con el **ORM** de SQLAlchemy 2, el que usa tu proyecto:

- declarar dos **modelos** tipados con `Mapped` y `mapped_column`, unidos por una **relación**;
- guardar objetos con una `Session` y ver cuándo reciben su `id`;
- consultar con `select`, `scalars` y `get`;
- entender el **mapa de identidad** y la **unidad de trabajo**;
- descubrir el problema **N+1** y arreglarlo con `selectinload`, o con un `GROUP BY`;
- borrar en cascada, y ver qué pasa con un objeto fuera de su sesión.

Un contador apunta cada SQL que se envía (`sent`): en casi todos los pasos verás **cuántas consultas** cuesta lo que haces. Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

El mismo PostgreSQL de los ejercicios 01 y 02:

```bash
cd bootcamp/week-19-postgresql_psycopg_sqlalchemy_y_alembic/2-practicas/ejercicio-03-modelos-y-sesiones-con-el-orm/starter
docker compose up -d --wait
uv run python main.py
```

```
...
Ejercicio 03 · Modelos y sesiones con el ORM
```

## Pasos

### 1. Dos modelos

Descomenta el **PASO 1** (las dos clases, el bucle y las dos líneas de `metadata`) y ejecuta:

```
id: INTEGER · ¿admite NULL? False
name: VARCHAR(50) · ¿admite NULL? False
altitude: INTEGER · ¿admite NULL? True
```

Un **modelo** es una clase que hereda de `Base` y describe una tabla. Cada atributo con `Mapped[...]` es una columna, y su tipo de Python decide el de SQL **y** si admite `NULL`: `Mapped[int]` es `NOT NULL`; `Mapped[int | None]`, no. `mapped_column(...)` añade lo que el tipo no dice (la clave primaria, la longitud, `unique`). `altitude` ni siquiera lo necesita.

`relationship` no es una columna: es un atributo de Python que lleva de una estación a sus medidas (`station.readings`) y de una medida a su estación (`reading.station`). La columna de verdad es `station_id`, con su clave foránea. `back_populates` enlaza los dos lados.

`Reading` aparece en `Station` antes de estar definida: en Python 3.14 las anotaciones se evalúan tarde, cuando SQLAlchemy las necesita, y no hace falta escribirlas entre comillas.

### 2. Guardar objetos

Descomenta el **PASO 2** y ejecuta:

```
antes del commit, id de Norte: None
después del commit, id de Norte: 1
```

Creas objetos de Python normales y los metes en la sesión con `add_all`. Las medidas entran **con** su estación: están en `readings`, y la relación las lleva consigo. Hasta el `commit`, nada ha llegado a PostgreSQL, y por eso `id` es `None`. Al confirmar, la sesión envía los `INSERT` en el orden correcto (primero las estaciones, después las medidas, con su `station_id`) y apunta los `id` que PostgreSQL asignó.

`with Session(engine) as session:` cierra la sesión al salir y deshace lo que no se confirmó.

### 3. Consultar objetos

Descomenta el **PASO 3** y ejecuta:

```
todas: [Station('Este'), Station('Norte'), Station('Sur')]
la alta: Station('Norte') 2600
get(2): Station('Sur') · get(99): None
```

`select(Station)` pide objetos enteros. `session.scalars(...)` devuelve uno por fila; `.all()` los reúne en una lista y `.one()` exige exactamente uno. `session.get(Station, 2)` busca por clave primaria y devuelve `None` si no existe. El `Station('Norte')` lo escribe el `__repr__` del modelo.

### 4. El mapa de identidad

Descomenta el **PASO 4** y ejecuta:

```
¿el mismo objeto? True · consultas: 1
```

Dentro de una sesión, cada fila es **un solo objeto**. El segundo `get` ni siquiera pregunta a PostgreSQL: lo encuentra en el **mapa de identidad** de la sesión, por su clave primaria. Así, si cambias la estación 1 en un sitio, la ves cambiada en todos.

### 5. La unidad de trabajo

Descomenta el **PASO 5** y ejecuta:

```
pendiente de guardar: IdentitySet([Station('Norte')])
SQL del commit: ['UPDATE']
altitud: 2650 · consultas para leerla: 1
```

Cambias un atributo y nada más: la sesión se da cuenta (`session.dirty`) y en el `commit` envía **un** `UPDATE` con solo lo que cambió. Es la **unidad de trabajo**: tú cambias objetos, la sesión decide el SQL.

Después del commit, leer `altitude` cuesta una consulta. Por defecto, el commit **caduca** los objetos (`expire_on_commit=True`), y el siguiente acceso los vuelve a leer: otro programa podría haber cambiado la fila entre medias.

### 6. Relaciones

Descomenta el **PASO 6** y ejecuta:

```
medidas de Sur: [30.0, None]
consultas al tocar .readings: 1
de la medida a su estación: Station('Sur') True
```

Las medidas no llegan con la estación: se cargan la primera vez que tocas `south.readings`, con su propia consulta. Es la carga **perezosa** (*lazy*), la de por defecto. Al revés, `reading.station` no pregunta nada: la estación ya está en el mapa de identidad, y es **el mismo** objeto.

### 7. El problema N+1

Descomenta el **PASO 7** y ejecuta:

```
Norte: 2 medidas
Sur: 2 medidas
Este: 0 medidas
consultas, sin selectinload: 4
consultas, con selectinload: 2
```

Una consulta para las estaciones, y **una más por cada estación** para sus medidas: 1 + N. Con 3 estaciones son 4; con 1000, 1001, y cada una es un viaje de ida y vuelta a PostgreSQL. Es el error de rendimiento más común con un ORM, y no se ve leyendo el código.

`options(selectinload(Station.readings))` pide las medidas de **todas** las estaciones en una segunda consulta (`... WHERE station_id IN (1, 2, 3)`): 2 consultas, sean 3 estaciones o 1000.

### 8. Que cuente PostgreSQL

Descomenta el **PASO 8** y ejecuta:

```
Este: 0 medidas, media None
Norte: 2 medidas, media 10.0
Sur: 2 medidas, media 30.0
consultas: 1
```

Si solo quieres **contar**, no traigas los objetos: pide a PostgreSQL el resultado. `select` también acepta columnas y funciones de los modelos, y `session.execute` devuelve filas, no objetos. Una consulta, y a Python solo llegan tres filas. Es lo que hacen `list_loads` y `label_stats` en tu proyecto.

### 9. Borrar en cascada

Descomenta el **PASO 9** y ejecuta:

```
SQL del borrado: ['DELETE', 'DELETE']
medidas que quedan: 2
```

`cascade="all, delete-orphan"` en la relación: al borrar la estación, la sesión borra **antes** sus medidas (el primer `DELETE`) y después la estación (el segundo). Sin la cascada, intentaría dejar las medidas con `station_id` a `NULL`, y la columna no lo admite. Quedan las 2 medidas de Norte.

En tu proyecto hay además `ondelete="CASCADE"` en la clave foránea: entonces lo hace también PostgreSQL, aunque alguien borre con SQL a mano.

### 10. Un objeto fuera de su sesión

Descomenta el **PASO 10** y ejecuta:

```
fuera del with, el nombre: Este
DetachedInstanceError: lazy load operation of attribute 'readings' cannot proceed
```

El objeto sigue existiendo cuando la sesión se cierra, con lo que ya tenía cargado: el nombre se lee. Pero `readings` no estaba cargado, y para cargarlo hace falta una sesión que ya no existe. Por eso las funciones de tu proyecto devuelven valores sencillos (`Series`, `LoadInfo`, `LabelStats`) y no modelos: lo que sale de la sesión no depende de ella.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'Reading' is not defined` | Ejecutaste con un Python anterior a 3.14: usa `uv run`, que respeta `.python-version` |
| `ArgumentError: Could not determine join condition between parent/child tables` | Falta `ForeignKey("stations.id")` en `station_id` |
| `null value in column "station_id" of relation "readings" violates not-null constraint` en el paso 9 | Quitaste `cascade="all, delete-orphan"` de la relación |
| `MultipleResultsFound` en `.one()` | La consulta devuelve más de una fila: añade un `where` o usa `.all()` |
| `relation "stations" does not exist` | Descomentaste un paso sin el PASO 1, que crea las tablas |
| `DetachedInstanceError` donde no la esperas | Usas un objeto fuera del `with Session(...)`: haz el trabajo dentro, o devuelve valores sencillos |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · SQLAlchemy Core](../ejercicio-02-sqlalchemy-core/README.md) | **Ejercicio 03 · Modelos y sesiones con el ORM** | [Ejercicio 04 · Migraciones con Alembic](../ejercicio-04-migraciones-con-alembic/README.md) |
