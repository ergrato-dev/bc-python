# Ejercicio 02 — SQLAlchemy Core

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-sqlalchemy-2-motor-core-y-orm.md)

## Objetivo

Subir un piso por encima de psycopg, con el **Core** de SQLAlchemy, la capa sobre la que se construye el ORM del ejercicio 03:

- distinguir el **motor** (`Engine`) de una **conexión**;
- ejecutar SQL con `text()` y parámetros con nombre;
- ver la diferencia entre `engine.connect()` y `engine.begin()`;
- describir tablas con `MetaData` y `Table`, y crearlas con `create_all`;
- construir `insert`, `select`, `update` y `delete` en Python, con `JOIN` y `GROUP BY`;
- ver el SQL que SQLAlchemy envía, y el **pool** de conexiones.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

Usa el mismo PostgreSQL del ejercicio 01. Si lo apagaste, vuelve a arrancarlo: `compose.yaml` es el mismo.

```bash
cd bootcamp/week-19-postgresql_psycopg_sqlalchemy_y_alembic/2-practicas/ejercicio-02-sqlalchemy-core/starter
docker compose up -d --wait
uv run python main.py
```

```
...
Ejercicio 02 · SQLAlchemy Core
```

Fíjate en el principio de `main.py`: dos tablas, `stations` y `readings`, descritas como objetos `Table` dentro de un `MetaData`. Y una línea, `metadata.drop_all(engine)`, que las borra si existen: así cada ejecución empieza de cero, también si vienes del ejercicio 01, que dejó otra `stations`.

## Pasos

### 1. El motor no es una conexión

Descomenta el **PASO 1** y ejecuta:

```
motor: Engine(postgresql+psycopg://practicas:***@127.0.0.1:5433/practicas)
driver: postgresql + psycopg
pool: Pool size: 5  Connections in pool: 1 Current Overflow: -4 Current Checked out connections: 0
```

La URL dice tres cosas: el dialecto (`postgresql`), el *driver* (`psycopg`, el del ejercicio 01) y dónde conectar. Al imprimir el motor, la contraseña sale como `***`: un `print(engine)` en un registro no la filtra.

`create_engine` **no conecta**: prepara un **pool**, un almacén de conexiones que se abren cuando hacen falta y se reutilizan después. Hay una en el pool porque `drop_all` ya usó una y la devolvió. Por defecto caben 5 (`Pool size`), y `Overflow` cuenta las que se pueden abrir de más.

### 2. Una conexión y `text()`

Descomenta el **PASO 2** y ejecuta:

```
2 + 3 = 5
¿existe notes sin commit? False
pool: Pool size: 5  Connections in pool: 1 Current Overflow: -4 Current Checked out connections: 0
```

`text()` envuelve un SQL escrito a mano; los parámetros van con nombre (`:a`) y sus valores en un diccionario. `scalar_one()` devuelve el único valor de la única fila, y falla si hay más o ninguna.

El `CREATE TABLE` y el `INSERT` **desaparecen**: `engine.connect()` abre una transacción y, al salir del `with` sin `conn.commit()`, SQLAlchemy la deshace. En PostgreSQL, hasta un `CREATE TABLE` está dentro de la transacción. Y el pool sigue con una sola conexión: las dos del paso se pidieron y se devolvieron, una tras otra.

### 3. `begin()` confirma solo

Descomenta el **PASO 3** y ejecuta:

```
notas: 2
RuntimeError: algo falla a mitad
notas: 2
```

`engine.begin()` es una conexión con su transacción: si el bloque termina bien, **commit**; si sale una excepción, **rollback**. Por eso la nota `c` no llega. Es el patrón para escribir: `connect()` para leer, `begin()` para cambiar.

Una lista de diccionarios como parámetro ejecuta el mismo SQL una vez por diccionario, como el `executemany` del ejercicio 01.

### 4. Tablas como objetos de Python

Descomenta el **PASO 4** y ejecuta:

```

CREATE TABLE readings (
	id SERIAL NOT NULL, 
	station_id INTEGER NOT NULL, 
	value FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(station_id) REFERENCES stations (id)
)


tablas: ['readings', 'stations']
```

`CreateTable(...).compile(engine)` enseña el SQL que SQLAlchemy sacó del objeto `Table`, en el dialecto de PostgreSQL: `Integer` con `primary_key=True` es `SERIAL`, y `ForeignKey("stations.id")` es una **clave foránea**: PostgreSQL no dejará guardar una medida de una estación que no existe.

`create_all` crea, en el orden correcto, las tablas que faltan. Sirve para un ejercicio; en un proyecto, las tablas las crean las **migraciones** de Alembic (ejercicio 04), porque `create_all` no sabe cambiar una tabla que ya existe.

### 5. `insert()`

Descomenta el **PASO 5** y ejecuta:

```
ids: [1, 2, 3]
```

`insert(stations)` construye el `INSERT` a partir de la tabla: las columnas salen de las claves de los diccionarios. `.returning(...)` y `.scalars().all()` traen la columna `id` de las filas nuevas como una lista. Las cinco medidas se insertan sin `returning`.

### 6. `select()`

Descomenta el **PASO 6** y ejecuta:

```
SQL: SELECT stations.name, stations.altitude 
FROM stations 
WHERE stations.altitude > :altitude_1 ORDER BY stations.name
fila: ('Norte', 2600) · nombre: Norte · como dict: {'name': 'Norte', 'altitude': 2600}
solo nombres: ['Norte', 'Sur', 'Este']
```

`stations.c.altitude > 2000` no compara nada en Python: construye un trozo de SQL, y el `2000` va como **parámetro** (`:altitude_1`), nunca pegado. Lo de la inyección del ejercicio 01 no puede pasar aquí.

Cada fila es un `Row`: una tupla que además tiene atributos con el nombre de cada columna (`row.name`) y una vista de diccionario (`row._mapping`).

### 7. `JOIN` y `GROUP BY`

Descomenta el **PASO 7** y ejecuta:

```
SQL: SELECT stations.name, count(readings.id) AS measurements, count(readings.value) AS with_value, avg(readings.value) AS mean 
FROM stations LEFT OUTER JOIN readings ON stations.id = readings.station_id GROUP BY stations.name ORDER BY stations.name
Este: 0 medidas, 0 con valor, media None
Norte: 3 medidas, 3 con valor, media 13.333333333333334
Sur: 2 medidas, 1 con valor, media 30.0
```

Es la consulta de `label_stats` de tu proyecto. Fíjate en tres detalles:

- `outerjoin` (`LEFT OUTER JOIN`): Este sale aunque no tenga medidas. Con `join`, desaparecería;
- SQLAlchemy sabe **sobre qué** columnas unir: lo saca de la clave foránea;
- `count(columna)` no cuenta los `NULL`, y `avg` los ignora. Sur tiene dos medidas, una sin valor, y su media es 30, no 15.

PostgreSQL agrupa y cuenta; a Python solo llegan tres filas.

### 8. `update()` y `delete()`

Descomenta el **PASO 8** y ejecuta:

```
actualizadas: 1
borradas: 1
medidas que quedan: 4
```

`rowcount` dice cuántas filas tocó. Para comparar con `NULL` se usa `.is_(None)`, que es `IS NULL`: en SQL, `valor = NULL` nunca es verdadero, ni siquiera cuando el valor es `NULL`.

Un `update` o un `delete` **sin** `.where(...)` cambia o borra la tabla entera. Léelo dos veces antes de ejecutarlo.

### 9. Ver el SQL que se envía

Descomenta el **PASO 9** y ejecuta:

```
LOG BEGIN (implicit)
LOG SELECT stations.name 
FROM stations 
WHERE stations.id = %(id_1)s::INTEGER
LOG [generated in 0.00027s] {'id_1': 2}
LOG ROLLBACK
```

SQLAlchemy registra cada SQL en el *logger* `sqlalchemy.engine`. Con el nivel `INFO` lo ves todo: la transacción que abre (`BEGIN (implicit)`), el SQL con el formato de parámetros de psycopg (`%(id_1)s`), los valores aparte, y el `ROLLBACK` del final, porque era un `connect()` sin commit. Es lo mismo que `create_engine(URL, echo=True)`, y lo que hará `observatorio -v` si algún día lo necesitas.

### 10. El pool de conexiones

Descomenta el **PASO 10** y ejecuta:

```
pool: Pool size: 5  Connections in pool: 0 Current Overflow: -3 Current Checked out connections: 2
pool: Pool size: 5  Connections in pool: 2 Current Overflow: -3 Current Checked out connections: 0
después de dispose: Pool size: 5  Connections in pool: 0 Current Overflow: -5 Current Checked out connections: 0
```

Dos conexiones **prestadas** a la vez (`Checked out`). Al cerrarlas, no se cierran de verdad: vuelven al pool, listas para la siguiente. Abrir una conexión con PostgreSQL cuesta (un proceso nuevo en el servidor, autenticación); reutilizarla, casi nada. `engine.dispose()` cierra todas las del pool, que es lo que hace la CLI de tu proyecto al terminar cada comando.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `OperationalError: (psycopg.OperationalError) connection failed: ... Connection refused` | PostgreSQL no está arrancado: `docker compose up -d --wait` |
| `ModuleNotFoundError: No module named 'sqlalchemy'` | Ejecutaste `python main.py` sin `uv run` |
| `ProgrammingError: ... relation "stations" does not exist` | Descomentaste un paso sin el PASO 4, que crea las tablas |
| `IntegrityError: ... violates foreign key constraint` | Insertaste una medida con un `station_id` que no existe |
| `MultipleResultsFound` o `NoResultFound` | `scalar_one()` espera exactamente una fila; con varias, usa `.scalars().all()` |
| Cada línea `LOG` sale dos veces | Llamaste a `logging.basicConfig` y además pusiste `echo=True` en el motor: usa solo uno |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Consultas con psycopg](../ejercicio-01-consultas-con-psycopg/README.md) | **Ejercicio 02 · SQLAlchemy Core** | [Ejercicio 03 · Modelos y sesiones con el ORM](../ejercicio-03-modelos-y-sesiones-con-el-orm/README.md) |
