# 02 · psycopg: conexiones, parámetros y transacciones

⏱️ 45 min

## 🎯 Objetivos

- Explicar qué es un *driver* y por qué psycopg 3.
- Abrir una conexión, ejecutar SQL y leer filas con un cursor.
- Pasar valores como **parámetros**, y explicar por qué una f-string abre la puerta a una inyección de SQL.
- Controlar las transacciones: `commit`, `rollback` y `conn.transaction()`.
- Reconocer los errores de PostgreSQL en Python, incluida la transacción rota.
- Saber cuándo usar `COPY` en lugar de `INSERT`.

---

## 1. Un *driver*

Python no habla el protocolo de PostgreSQL. Un **driver** es la biblioteca que sí: abre la conexión de red, se autentica, envía el SQL y convierte las respuestas en objetos de Python. **psycopg 3** es el *driver* de PostgreSQL de referencia; SQLAlchemy lo usa por debajo cuando la URL dice `postgresql+psycopg://`.

```bash
uv add "psycopg[binary]==3.3.6"
```

El extra `[binary]` trae `libpq`, la biblioteca en C de PostgreSQL, ya compilada dentro de la rueda. Sin él, psycopg la buscaría en tu sistema, y la imagen `python:3.14.10-slim-trixie` no la tiene. El paquete se llama `psycopg`, sin número: `psycopg2` es la versión anterior, de otra generación.

## 2. Conexión y cursor

```python
import psycopg

DSN = "postgresql://practicas:practicas@127.0.0.1:5433/practicas"

with psycopg.connect(DSN) as conn:
    row = conn.execute("SELECT version()").fetchone()
    print(row)
```

- La **URL de conexión** (*DSN*) lleva el usuario, la contraseña, la máquina, el puerto y la base. Como lleva la contraseña, en un programa de verdad sale de la configuración (semana 18), nunca del código.
- `with psycopg.connect(...)` cierra la conexión al salir. Si el bloque termina bien, antes hace **commit**; si sale una excepción, **rollback**.
- `conn.execute` envía un SQL y devuelve un **cursor**, la posición en el resultado.

| Método del cursor | Devuelve |
|---|---|
| `fetchone()` | La fila siguiente, como tupla, o `None` si no quedan |
| `fetchall()` | Una lista con las filas **que quedan** |
| `for row in cursor` | Las filas una a una, sin cargarlas todas en memoria |
| `rowcount` | Cuántas filas tocó un `INSERT`, `UPDATE` o `DELETE` |

Por defecto cada fila es una tupla. `row_factory=dict_row` (de `psycopg.rows`) las da como diccionarios con el nombre de cada columna.

## 3. Parámetros, siempre

Los valores **nunca** se pegan en el texto del SQL. Van aparte, y en el SQL queda un hueco `%s`:

```python
conn.execute(
    "INSERT INTO stations (name, altitude) VALUES (%s, %s)",
    ("Norte", 2600),
)
```

psycopg envía el SQL y los valores **por separado**: PostgreSQL analiza el SQL sin los valores y después los coloca, ya como datos. Así, un valor nunca puede convertirse en SQL. Aunque se parezca, **no** es el `%` de las cadenas de Python: nunca escribas `"... %s" % valor`.

Lo que pasa si pegas:

```python
name = "nadie' OR '1'='1"          # lo que alguien escribió en un formulario
conn.execute(f"SELECT * FROM stations WHERE name = '{name}'")      # MAL
# SELECT * FROM stations WHERE name = 'nadie' OR '1'='1'    <- todas las filas
```

La comilla del usuario cierra la tuya, y lo que sigue es SQL que tú no escribiste. Es la **inyección de SQL**, uno de los fallos de seguridad más antiguos y más explotados. Con un parámetro, PostgreSQL busca una estación que se llame exactamente `nadie' OR '1'='1`. Lo ves en el ejercicio 01, paso 5.

Los parámetros sirven para **valores**. Un nombre de tabla o de columna no puede ir como `%s`; si de verdad tiene que ser variable, se compone con `psycopg.sql`:

```python
from psycopg import sql

query = sql.SQL("SELECT count(*) FROM {}").format(sql.Identifier(table))
```

`sql.Identifier` lo escribe entre comillas dobles y escapa lo que haga falta. Aun así, que ese nombre no salga nunca de lo que escribe un usuario.

## 4. Transacciones con psycopg

psycopg abre una transacción con el primer SQL que envías, y la deja abierta hasta que tú decides:

```python
conn.execute("INSERT ...")
conn.execute("INSERT ...")
conn.commit()        # las dos quedan guardadas
# o bien
conn.rollback()      # ninguna
```

Para un grupo de operaciones que van juntas, `conn.transaction()`:

```python
with conn.transaction():
    conn.execute("UPDATE stations SET altitude = altitude + 100")
    conn.execute("INSERT INTO stations (name) VALUES (%s)", ("Norte",))
```

Si algo falla dentro del bloque, todo el bloque se deshace, también lo que ya se había ejecutado. Si termina bien, se confirma. Y se pueden anidar: un bloque dentro de otro es un **SAVEPOINT**, un punto al que volver sin deshacer lo de fuera.

Con `psycopg.connect(DSN, autocommit=True)`, cada SQL se confirma solo, sin transacción. Hace falta para algunas órdenes que no admiten transacción, como `CREATE DATABASE`.

## 5. Los errores de PostgreSQL

Cada error del servidor llega como una excepción de `psycopg.errors`, con una clase por código de error:

| Clase | Cuándo |
|---|---|
| `UniqueViolation` | Un valor repetido en una columna `UNIQUE` o en la clave primaria |
| `ForeignKeyViolation` | Una clave foránea que apunta a nada |
| `NotNullViolation` | Falta un valor en una columna `NOT NULL` |
| `StringDataRightTruncation` | Un texto más largo que su `varchar(n)` |
| `UndefinedTable` | La tabla no existe |
| `OperationalError` | No hay conexión: servidor apagado, contraseña mala |

Todas heredan de `psycopg.Error`, y `problem.diag.message_primary` es el mensaje del servidor.

Después de un error **dentro de una transacción**, la transacción queda rota, y cualquier SQL siguiente falla con:

```
current transaction is aborted, commands ignored until end of transaction block
```

Hay que terminarla con `rollback()`. Si ves este mensaje, el error de verdad es **el anterior**: búscalo más arriba en el registro.

## 6. Muchas filas: `COPY`

`executemany` repite un `INSERT` por cada fila; psycopg 3 los envía seguidos sin esperar cada respuesta, y es razonablemente rápido. Para cargas grandes, PostgreSQL tiene `COPY`, que recibe un chorro de filas en un solo comando:

```python
with conn.cursor() as cur, cur.copy("COPY readings (label, value) FROM STDIN") as copy:
    for row in rows:
        copy.write_row(row)
```

En el ejercicio 01, 20 000 filas: unos 0,3 s con `executemany` y 0,01 s con `COPY`. Tu proyecto no lo necesita (SQLAlchemy agrupa los `INSERT` de mil en mil, teoría 03), pero es la herramienta cuando importas un archivo de millones de líneas.

## 7. ¿Y por qué no psycopg a pelo en el proyecto?

Podrías escribir todo el Observatorio con psycopg y SQL a mano. Funciona, y para un script es lo más directo. En un proyecto que crece, SQLAlchemy añade:

- **tablas descritas en Python**, de las que Alembic saca las migraciones (teoría 04);
- consultas que se construyen por partes (un `where` solo si hay `--carga`), sin pegar textos;
- objetos con tipos para mypy en lugar de tuplas;
- un **pool** de conexiones y transacciones con `with`.

Por debajo sigue siendo psycopg: lo que aprendes aquí (parámetros, transacciones, errores) es lo que pasa cuando SQLAlchemy envía el SQL.

---

## ⚠️ Errores comunes

| Error | Causa | Solución |
|---|---|---|
| `ImportError: no pq wrapper available` | Instalaste `psycopg` sin `[binary]` y no tienes `libpq` | `uv add "psycopg[binary]==3.3.6"` |
| Un nombre con comilla (`O'Higgins`) rompe la consulta | Pegaste el valor con una f-string | Parámetro `%s` |
| `syntax error at or near "$1"` | Pusiste un nombre de tabla como parámetro | `sql.Identifier` |
| Los cambios no se ven desde `psql` | Falta el `commit` | `conn.commit()`, o `with conn.transaction():` |
| `current transaction is aborted...` | Un error anterior rompió la transacción | Busca el primer error; `rollback()` |
| `TypeError: query parameters should be a sequence or a mapping, got str` | Un solo parámetro sin coma: `("Norte")` es un texto | `("Norte",)`, con coma |

---

## ✅ Qué debes saber al terminar

- [ ] Qué hace un *driver* y qué trae el extra `[binary]`.
- [ ] Qué hace `with psycopg.connect(...)` al salir, bien y con error.
- [ ] Por qué un parámetro no puede convertirse en SQL y una f-string sí.
- [ ] Cómo agrupar operaciones en una transacción, y qué es un SAVEPOINT.
- [ ] Qué significa "current transaction is aborted" y qué hacer.
- [ ] Cuándo `COPY` y cuándo `INSERT`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [01 · Bases de datos relacionales y PostgreSQL](01-bases-de-datos-relacionales-y-postgresql.md) | **02 · psycopg: conexiones, parámetros y transacciones** | [03 · SQLAlchemy 2: motor, Core y ORM](03-sqlalchemy-2-motor-core-y-orm.md) |
