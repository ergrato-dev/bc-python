# Ejercicio 01 — Consultas con psycopg

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-bases-de-datos-relacionales-y-postgresql.md) y [02](../../1-teoria/02-psycopg-conexiones-parametros-y-transacciones.md)

## Objetivo

Hablar con PostgreSQL desde Python sin nada en medio, con **psycopg 3**, el *driver* que usará SQLAlchemy en los ejercicios siguientes y en tu proyecto:

- conectar y preguntarle cosas al servidor;
- crear una tabla, insertar filas con **parámetros** y leerlas;
- ver con tus ojos una **inyección de SQL**, y por qué los parámetros la impiden;
- usar transacciones: una que se deshace sola y otra que se queda rota;
- componer nombres de tabla con `psycopg.sql`;
- insertar 20 000 filas con `executemany` y con `COPY`.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

Arranca el PostgreSQL de las prácticas. Es el mismo para los cuatro ejercicios de la semana: `compose.yaml` le da el nombre `practicas-semana-19`.

```bash
cd bootcamp/week-19-postgresql_psycopg_sqlalchemy_y_alembic/2-practicas/ejercicio-01-consultas-con-psycopg/starter
docker compose up -d --wait
uv run python main.py
```

```
...
 ✔ Container practicas-semana-19-db-1  Healthy
Ejercicio 01 · Consultas con psycopg
```

`--wait` espera a que el *healthcheck* de `compose.yaml` (`pg_isready`) diga que PostgreSQL ya acepta conexiones. Sin él, el primer `uv run` puede llegar antes que la base.

Cada ejecución empieza con `DROP TABLE IF EXISTS stations`: puedes repetir los pasos tantas veces como quieras. Los pasos se acumulan: cada uno deja descomentados los anteriores.

## Pasos

### 1. Conectar y preguntar

Descomenta el **PASO 1** y ejecuta `uv run python main.py`:

```
servidor: PostgreSQL 18.6
base: practicas · usuario: practicas · puerto: 5433
```

`psycopg.connect(DSN)` abre **una** conexión: un proceso de PostgreSQL atiende solo a tu programa mientras dure. `conn.execute` envía el SQL y devuelve un cursor; `fetchone()` trae la primera fila como una **tupla**, aunque tenga una sola columna (`row[0]`).

`fetchone()` devuelve `None` si no hay filas: por eso el `assert`, que además le dice a mypy que `row` ya no es `None`.

### 2. Crear una tabla

Descomenta el **PASO 2** y ejecuta:

```
tabla creada
```

Tres columnas con su tipo: `serial` (un entero que PostgreSQL numera solo), `text` y `integer`. Las **restricciones** son reglas que la base comprueba siempre, venga el dato de donde venga: `PRIMARY KEY` (única y no nula), `NOT NULL` y `UNIQUE`.

`conn.commit()` confirma la transacción. psycopg abre una en cuanto envías el primer SQL, y lo que hay dentro no es definitivo hasta el `commit`.

Mírala desde fuera, con `psql`, el cliente de PostgreSQL que trae el contenedor:

```bash
docker compose exec db psql -U practicas -c '\d stations'
```

```
                             Table "public.stations"
  Column  |  Type   | Collation | Nullable |               Default
----------+---------+-----------+----------+--------------------------------------
 id       | integer |           | not null | nextval('stations_id_seq'::regclass)
 name     | text    |           | not null |
 altitude | integer |           |          |
Indexes:
    "stations_pkey" PRIMARY KEY, btree (id)
    "stations_name_key" UNIQUE CONSTRAINT, btree (name)
```

### 3. Insertar con parámetros

Descomenta el **PASO 3** y ejecuta:

```
id de Norte: 1
filas de executemany: 3
```

Los valores **nunca** van dentro del texto del SQL: van aparte, en una tupla, y en el SQL solo queda `%s`. psycopg los envía al servidor por separado (teoría 02). `RETURNING id` devuelve lo que PostgreSQL acaba de asignar. `executemany` repite el mismo `INSERT` con cada tupla de la lista; `None` se guarda como `NULL`.

### 4. Leer filas

Descomenta el **PASO 4** y ejecuta:

```
una: ('Norte', 2600)
el resto: [('Sur', 1500), ('Este', None), ('Oeste', 3100)]
por encima de 2000 m: ['Oeste', 'Norte']
como diccionario: [{'name': 'Este', 'altitude': None}]
```

Un cursor es una posición en el resultado: `fetchone()` avanza una fila, y `fetchall()` trae **las que quedan**, no todas. También se puede recorrer con `for`. Sin `ORDER BY`, PostgreSQL no promete ningún orden: pídelo siempre que te importe.

`row_factory=dict_row` cambia la forma de las filas: diccionarios con el nombre de cada columna. `NULL` llega como `None`.

### 5. Inyección de SQL

Descomenta el **PASO 5** y ejecuta:

```
SQL pegado: SELECT count(*) FROM stations WHERE name = 'nadie' OR '1'='1'
con f-string: 4 filas
con parámetro: 0 filas
```

Alguien escribe `nadie' OR '1'='1` en un formulario. Pegado con una f-string, su comilla **cierra** la tuya y lo que sigue pasa a ser SQL: `OR '1'='1'` es verdadero para todas las filas. Con un `DELETE`, borraría la tabla entera.

Con el parámetro, el mismo texto viaja como un **valor**: PostgreSQL busca una estación que se llame, literalmente, `nadie' OR '1'='1`, y no hay ninguna. Regla sin excepciones: un valor que no escribiste tú va como parámetro.

### 6. Una transacción que se deshace

Descomenta el **PASO 6** y ejecuta:

```
UniqueViolation: duplicate key value violates unique constraint "stations_name_key"
altitud de Norte: 2600
```

`with conn.transaction():` agrupa el `UPDATE` y el `INSERT`: o se confirman los dos, o ninguno. El `INSERT` repite `Norte`, que es `UNIQUE`; PostgreSQL lo rechaza, el bloque sale con una excepción y psycopg deshace **también** el `UPDATE`, que ya se había ejecutado. Norte sigue a 2600 m, no a 2700.

Los errores de PostgreSQL llegan como clases de `psycopg.errors`, una por código de error: `UniqueViolation`, `ForeignKeyViolation`, `NotNullViolation`... `diag.message_primary` es el mensaje del servidor, en inglés.

### 7. Una transacción rota

Descomenta el **PASO 7** y ejecuta:

```
primer error: UniqueViolation
segundo error: current transaction is aborted, commands ignored until end of transaction block
después de rollback: 4 filas
```

Esta vez el `INSERT` fallido no está en un bloque `transaction()`. La transacción que psycopg abrió sola queda **rota**: PostgreSQL rechaza cualquier SQL siguiente, hasta un `SELECT`, con `InFailedSqlTransaction`. Hay que terminarla con `conn.rollback()`.

Si ves ese mensaje en un programa, el error de verdad es **el anterior**: búscalo más arriba.

### 8. Nombres de tabla con `psycopg.sql`

Descomenta el **PASO 8** y ejecuta:

```
SQL compuesto: SELECT count(*) FROM "stations"
filas: 4
SyntaxError: syntax error at or near "$1"
```

Los parámetros son para **valores**, no para nombres de tablas o columnas: `FROM %s` llega al servidor como `FROM $1`, y no es SQL válido. Si un nombre tiene que ser variable, se compone con `sql.SQL` y `sql.Identifier`, que lo escribe entre comillas dobles y escapa lo que haga falta. `as_string` enseña el resultado.

### 9. Muchas filas: `executemany` y `COPY`

Descomenta el **PASO 9** y ejecuta:

```
executemany: 0.28 s
COPY: 0.01 s
filas y media: (20000, 5000.0)
```

Tus tiempos serán otros; la proporción, parecida. `executemany` envía 20 000 `INSERT` (psycopg 3 los manda seguidos, sin esperar cada respuesta). `COPY ... FROM STDIN` es el camino de PostgreSQL para cargar datos en bloque: un solo comando y un chorro de filas. Para cargar un archivo grande, `COPY`; para unas pocas filas, `INSERT`.

`CREATE TEMPORARY TABLE` crea una tabla que desaparece al cerrar la conexión: no ensucia la base.

Para terminar, apaga PostgreSQL **solo si no vas a seguir** con el ejercicio 02, que usa el mismo:

```bash
docker compose down
```

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `connection failed: ... port 5433 failed: Connection refused` | PostgreSQL no está arrancado: `docker compose up -d --wait` en `starter/` |
| `password authentication failed for user "practicas"` | Cambiaste `DSN` o `compose.yaml`: usuario y contraseña son `practicas` |
| `Bind for 127.0.0.1:5433 failed: port is already allocated` | Otro programa usa el 5433: `docker ps` y para el contenedor que lo ocupa |
| `ModuleNotFoundError: No module named 'psycopg'` | Ejecutaste `python main.py` sin `uv run` |
| `relation "stations" does not exist` | Descomentaste un paso sin el PASO 2, que crea la tabla |
| `current transaction is aborted...` en un paso tuyo | Un SQL anterior falló: arréglalo, o haz `conn.rollback()` después de capturarlo |
| `IndentationError` | Al descomentar, quitaste también los espacios del principio: los pasos van dentro del `with`, con 4 espacios |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Teoría 05 · Probar con una base de datos de verdad](../../1-teoria/05-probar-con-una-base-de-datos-de-verdad.md) | **Ejercicio 01 · Consultas con psycopg** | [Ejercicio 02 · SQLAlchemy Core](../ejercicio-02-sqlalchemy-core/README.md) |
