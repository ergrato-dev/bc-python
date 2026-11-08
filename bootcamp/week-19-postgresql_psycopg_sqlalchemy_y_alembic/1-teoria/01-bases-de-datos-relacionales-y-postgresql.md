# 01 · Bases de datos relacionales y PostgreSQL

⏱️ 45 min

## 🎯 Objetivos

- Explicar qué gana tu programa al guardar en una base de datos en lugar de en archivos.
- Describir una tabla: filas, columnas, tipos, clave primaria y clave foránea.
- Leer y escribir el SQL básico: `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `JOIN` y `GROUP BY`.
- Entender qué es `NULL` y por qué no se compara con `=`.
- Explicar qué es una transacción y qué promete.
- Arrancar PostgreSQL con Docker Compose y mirar dentro con `psql`.

---

## 1. Por qué una base de datos

Tu Observatorio guarda medidas en `.txt`, `.csv` y `.json`. Funciona mientras sea **un** programa en **una** máquina con archivos **pequeños**. Cuando no:

| Necesitas... | Con archivos | Con una base de datos |
|---|---|---|
| Que dos programas escriban a la vez | Uno pisa al otro | La base ordena las escrituras |
| La media de una etiqueta entre un millón de medidas | Lees el millón en Python | La base calcula y te manda una fila |
| Que no exista una medida sin estación | Lo compruebas tú, en cada programa | Una regla de la base, siempre |
| Que un fallo a mitad no deje la mitad guardada | Archivos temporales y renombrados | Una transacción |
| Que la API de la semana 20 lea lo mismo que la CLI | Compartir una carpeta | Los dos se conectan a la misma base |

Una **base de datos relacional** guarda los datos en tablas, los comprueba con reglas y responde preguntas en **SQL**. **PostgreSQL** es la que usa este bootcamp: libre, muy completa y la más extendida en proyectos nuevos de Python.

## 2. Tablas, filas y columnas

Una **tabla** es una lista de **filas** con las mismas **columnas**. Cada columna tiene un **tipo**, y PostgreSQL rechaza lo que no encaja:

```
 loads                                   readings
 id │ source       │ created_at          id │ load_id │ position │ label │ value
────┼──────────────┼─────────────────    ───┼─────────┼──────────┼───────┼──────
  1 │ medidas.txt  │ 2026-11-08 10:02     1 │       1 │        0 │ Norte │  12.5
  2 │ este.csv     │ 2026-11-08 10:05     2 │       1 │        1 │ Sur   │
                                          3 │       2 │        0 │ Este  │   3
```

Son las dos tablas de tu proyecto: una **carga** por archivo guardado, y una fila por **medida**. Los tipos que vas a usar:

| Tipo de PostgreSQL | Para qué | En Python |
|---|---|---|
| `integer`, `bigint` | Números enteros | `int` |
| `double precision` | Medidas con decimales | `float` |
| `numeric(10, 2)` | Dinero: decimales exactos | `Decimal` |
| `varchar(100)`, `text` | Texto, con o sin límite de longitud | `str` |
| `boolean` | Sí o no | `bool` |
| `timestamp with time zone` (`timestamptz`) | Un instante | `datetime` con zona |

## 3. Claves y restricciones

- La **clave primaria** (`PRIMARY KEY`) identifica cada fila: única y nunca vacía. Casi siempre es un `id` que numera la propia base.
- Una **clave foránea** (`FOREIGN KEY`) apunta a la clave primaria de otra tabla: `readings.load_id` apunta a `loads.id`. PostgreSQL no deja guardar una medida de una carga que no existe, ni borrar una carga con medidas, salvo que digas qué hacer con ellas (`ON DELETE CASCADE`: borrarlas también).
- `NOT NULL` obliga a dar un valor; `UNIQUE` prohíbe repetirlo; `CHECK` comprueba una condición (`value >= 0`).

Las **restricciones** son la última línea de defensa: da igual qué programa escriba, o si alguien escribe SQL a mano, la base no las deja romper.

Un **índice** es una estructura aparte que hace rápidas las búsquedas por una columna, como el índice de un libro. La clave primaria y `UNIQUE` llevan uno; `readings.load_id` tiene otro, porque casi todas las consultas buscan las medidas **de una carga**.

## 4. SQL en cinco minutos

SQL dice **qué** quieres, no cómo conseguirlo: la base decide cómo.

```sql
INSERT INTO loads (source) VALUES ('medidas.txt');

SELECT label, value FROM readings WHERE load_id = 1 ORDER BY position;

UPDATE readings SET value = 13.0 WHERE id = 1;

DELETE FROM loads WHERE id = 2;
```

`UPDATE` y `DELETE` sin `WHERE` cambian o borran **la tabla entera**. Y sin `ORDER BY`, las filas llegan en el orden que le venga bien a la base, que puede cambiar.

Dos operaciones más hacen casi todo el trabajo de un análisis:

```sql
-- JOIN: las filas de dos tablas, unidas por la clave foránea.
SELECT loads.source, readings.label, readings.value
FROM loads JOIN readings ON readings.load_id = loads.id;

-- GROUP BY: una fila por grupo, con funciones de agregado.
SELECT label, count(*), count(value), avg(value)
FROM readings
GROUP BY label
ORDER BY label;
```

`JOIN` solo deja las filas que tienen pareja; `LEFT JOIN` (o `LEFT OUTER JOIN`) deja también las de la izquierda que no la tienen, como una carga sin medidas.

## 5. `NULL`, el valor que falta

`NULL` no es cero ni texto vacío: es "no se sabe". Es el `None` de Python y el `NA` de tus archivos. Tres reglas que sorprenden:

- `value = NULL` **nunca** es verdadero, ni siquiera cuando `value` es `NULL`. Se pregunta con `value IS NULL`.
- `count(*)` cuenta filas; `count(value)` solo las que tienen valor.
- `avg(value)`, `sum`, `min` y `max` ignoran los `NULL`. La media de 10, `NULL` y 20 es 15, no 10.

Es justo lo que hace tu Observatorio con los "sin dato", así que la base calcula lo mismo que `label_means`.

## 6. Transacciones

Una **transacción** agrupa varias operaciones en una sola: o se aplican **todas** (`COMMIT`), o **ninguna** (`ROLLBACK`).

```sql
BEGIN;
INSERT INTO loads (source) VALUES ('medidas.txt');
INSERT INTO readings (load_id, position, label, value) VALUES (3, 0, 'Norte', 12.5);
COMMIT;
```

Si el segundo `INSERT` falla, el primero se deshace: nunca queda una carga a medias. Es lo que se conoce como **ACID**:

- **A**tomicidad: todo o nada;
- **C**onsistencia: al terminar, se cumplen todas las restricciones;
- a**I**slamiento: otra conexión no ve tus cambios hasta el `COMMIT`;
- **D**urabilidad: lo confirmado sobrevive a un apagón.

En PostgreSQL hasta `CREATE TABLE` y `ALTER TABLE` van dentro de la transacción. Lo aprovecharás en las migraciones (teoría 04) y en los tests (teoría 05).

## 7. PostgreSQL es un servidor

PostgreSQL no es un archivo que abres: es un **servidor**, un programa que escucha en un puerto (el 5432) y atiende a los **clientes** que se conectan. Cada conexión es un proceso del servidor, con un **usuario** (un *rol*) y una **base**: un mismo servidor guarda varias bases separadas.

En este bootcamp, PostgreSQL vive en un contenedor. El `compose.yaml` de tu proyecto lo describe:

```yaml
  db:
    image: postgres:18.6-alpine
    environment:
      POSTGRES_USER: observatorio
      POSTGRES_PASSWORD: observatorio
      POSTGRES_DB: observatorio
    ports:
      - "127.0.0.1:5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "observatorio", "-d", "observatorio"]
```

- La imagen va **fijada** (`18.6-alpine`), como todo en el bootcamp; las versiones y su revisión están en `docs/stack-versions.md`.
- Las variables `POSTGRES_*` crean el usuario y la base la primera vez que arranca. Son de desarrollo y solo para tu máquina.
- `127.0.0.1:5432:5432` abre el puerto **solo** a tu máquina, no a la red de la cafetería.
- El **volumen** `pgdata` guarda los datos fuera del contenedor: sobreviven a `docker compose down`. Con `down -v` se borran.
- El **healthcheck** pregunta con `pg_isready` si ya acepta conexiones. `docker compose up -d --wait db` espera a que diga que sí.

Para mirar dentro, el contenedor trae **`psql`**, el cliente de PostgreSQL en la terminal:

```bash
docker compose up -d --wait db
docker compose exec db psql -U observatorio
```

```
observatorio=# \dt
observatorio=# \d readings
observatorio=# SELECT count(*) FROM readings;
observatorio=# \q
```

`\dt` lista las tablas, `\d tabla` describe una, y `\q` sale. Lo que no empieza por `\` es SQL, y termina en `;`.

---

## ⚠️ Errores comunes

| Error | Causa | Solución |
|---|---|---|
| `connection refused` en el puerto 5432 | PostgreSQL no está arrancado, o aún no acepta conexiones | `docker compose up -d --wait db` |
| `port is already allocated` al arrancar | Ya tienes otro PostgreSQL en el 5432 | `docker ps` y para el otro, o cambia el puerto de tu máquina en `compose.yaml` |
| `WHERE value = NULL` no encuentra nada | `NULL` no es igual a nada | `WHERE value IS NULL` |
| La media sale distinta de la que esperabas | `avg` ignora los `NULL` | Es lo correcto; si quieres contar los vacíos, `count(*) - count(value)` |
| Has borrado todas las filas | `DELETE` sin `WHERE` | Escribe el `WHERE` antes que el `DELETE`, y prueba dentro de un `BEGIN` |
| Los datos desaparecen al reiniciar | Hiciste `docker compose down -v`, que borra el volumen | `down` a secas los conserva |

---

## ✅ Qué debes saber al terminar

- [ ] Tres cosas que una base de datos hace mejor que una carpeta de archivos.
- [ ] Qué son una clave primaria, una clave foránea y una restricción.
- [ ] Leer un `SELECT` con `JOIN`, `WHERE`, `GROUP BY` y `ORDER BY`.
- [ ] Las tres reglas de `NULL`.
- [ ] Qué promete una transacción.
- [ ] Qué hace cada línea del servicio `db` de `compose.yaml`, y cómo entrar con `psql`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 19 · README](../README.md) | **01 · Bases de datos relacionales y PostgreSQL** | [02 · psycopg: conexiones, parámetros y transacciones](02-psycopg-conexiones-parametros-y-transacciones.md) |
