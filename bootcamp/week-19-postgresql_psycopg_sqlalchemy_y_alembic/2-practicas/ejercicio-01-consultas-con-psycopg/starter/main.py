"""Ejercicio 01 · Consultas con psycopg: conectar, crear, insertar, leer y transacciones.

Antes de ejecutar, arranca el PostgreSQL de las prácticas: `docker compose up -d --wait`.
Cada ejecución borra y vuelve a crear la tabla `stations`: puedes repetir sin miedo.
"""

import time

import psycopg
from psycopg import sql
from psycopg.rows import dict_row

# Usuario, contraseña, máquina, puerto y base: los de compose.yaml. En un programa de
# verdad esta URL sale de la configuración (semana 18), nunca del código.
DSN = "postgresql://practicas:practicas@127.0.0.1:5433/practicas"

print("Ejercicio 01 · Consultas con psycopg")

# `with` cierra la conexión al salir y, si no hubo excepción, hace commit.
with psycopg.connect(DSN) as conn:
    conn.execute("DROP TABLE IF EXISTS stations")
    conn.commit()

    # ============================================
    # PASO 1: Conectar y preguntar
    # ============================================
    # Descomenta las siguientes líneas:
    # row = conn.execute("SELECT version()").fetchone()
    # assert row is not None
    # print("servidor:", row[0].split(" on ")[0])
    # info = conn.info
    # print("base:", info.dbname, "· usuario:", info.user, "· puerto:", info.port)

    # ============================================
    # PASO 2: Crear una tabla
    # ============================================
    # Descomenta las siguientes líneas:
    # conn.execute(
    #     """
    #     CREATE TABLE stations (
    #         id serial PRIMARY KEY,
    #         name text NOT NULL UNIQUE,
    #         altitude integer
    #     )
    #     """
    # )
    # conn.commit()
    # print("tabla creada")

    # ============================================
    # PASO 3: Insertar con parámetros
    # ============================================
    # Descomenta las siguientes líneas:
    # with conn.cursor() as cur:
    #     cur.execute(
    #         "INSERT INTO stations (name, altitude) VALUES (%s, %s) RETURNING id",
    #         ("Norte", 2600),
    #     )
    #     row = cur.fetchone()
    #     assert row is not None
    #     print("id de Norte:", row[0])
    #     cur.executemany(
    #         "INSERT INTO stations (name, altitude) VALUES (%s, %s)",
    #         [("Sur", 1500), ("Este", None), ("Oeste", 3100)],
    #     )
    #     print("filas de executemany:", cur.rowcount)
    # conn.commit()

    # ============================================
    # PASO 4: Leer filas
    # ============================================
    # Descomenta las siguientes líneas:
    # cur = conn.execute("SELECT name, altitude FROM stations ORDER BY id")
    # print("una:", cur.fetchone())
    # print("el resto:", cur.fetchall())
    # high = conn.execute(
    #     "SELECT name FROM stations WHERE altitude > %s ORDER BY altitude DESC", (2000,)
    # )
    # print("por encima de 2000 m:", [name for (name,) in high])
    # with conn.cursor(row_factory=dict_row) as dict_cur:
    #     dict_cur.execute("SELECT name, altitude FROM stations WHERE altitude IS NULL")
    #     print("como diccionario:", dict_cur.fetchall())

    # ============================================
    # PASO 5: Inyección de SQL
    # ============================================
    # Descomenta las siguientes líneas:
    # typed = "nadie' OR '1'='1"
    # glued = f"SELECT count(*) FROM stations WHERE name = '{typed}'"
    # print("SQL pegado:", glued)
    # row = conn.execute(glued).fetchone()  # MAL: el texto del usuario es SQL.
    # assert row is not None
    # print("con f-string:", row[0], "filas")
    # safe = "SELECT count(*) FROM stations WHERE name = %s"
    # row = conn.execute(safe, (typed,)).fetchone()
    # assert row is not None
    # print("con parámetro:", row[0], "filas")

    # ============================================
    # PASO 6: Una transacción que se deshace
    # ============================================
    # Descomenta las siguientes líneas:
    # try:
    #     with conn.transaction():
    #         conn.execute("UPDATE stations SET altitude = altitude + 100")
    #         conn.execute("INSERT INTO stations (name) VALUES (%s)", ("Norte",))
    # except psycopg.errors.UniqueViolation as problem:
    #     print("UniqueViolation:", problem.diag.message_primary)
    # row = conn.execute("SELECT altitude FROM stations WHERE name = 'Norte'").fetchone()
    # assert row is not None
    # print("altitud de Norte:", row[0])

    # ============================================
    # PASO 7: Una transacción rota
    # ============================================
    # Descomenta las siguientes líneas:
    # try:
    #     conn.execute("INSERT INTO stations (name) VALUES (%s)", ("Sur",))
    # except psycopg.errors.UniqueViolation:
    #     print("primer error: UniqueViolation")
    # try:
    #     conn.execute("SELECT count(*) FROM stations")
    # except psycopg.errors.InFailedSqlTransaction as problem:
    #     print("segundo error:", problem)
    # conn.rollback()
    # row = conn.execute("SELECT count(*) FROM stations").fetchone()
    # assert row is not None
    # print("después de rollback:", row[0], "filas")

    # ============================================
    # PASO 8: Nombres de tabla con psycopg.sql
    # ============================================
    # Descomenta las siguientes líneas:
    # table = "stations"
    # query = sql.SQL("SELECT count(*) FROM {}").format(sql.Identifier(table))
    # print("SQL compuesto:", query.as_string(conn))
    # row = conn.execute(query).fetchone()
    # assert row is not None
    # print("filas:", row[0])
    # try:
    #     conn.execute("SELECT count(*) FROM %s", (table,))
    # except psycopg.errors.SyntaxError as problem:
    #     print("SyntaxError:", problem.diag.message_primary)
    # conn.rollback()

    # ============================================
    # PASO 9: Muchas filas: executemany y COPY
    # ============================================
    # Descomenta las siguientes líneas:
    # conn.execute("CREATE TEMPORARY TABLE readings (label text, value double precision)")
    # rows = [(f"S{i % 50}", i * 0.5) for i in range(20_000)]
    # start = time.perf_counter()
    # with conn.cursor() as cur:
    #     cur.executemany("INSERT INTO readings VALUES (%s, %s)", rows)
    # print(f"executemany: {time.perf_counter() - start:.2f} s")
    # conn.execute("TRUNCATE readings")
    # start = time.perf_counter()
    # copy_sql = "COPY readings (label, value) FROM STDIN"
    # with conn.cursor() as cur, cur.copy(copy_sql) as copy:
    #     for row in rows:
    #         copy.write_row(row)
    # print(f"COPY: {time.perf_counter() - start:.2f} s")
    # row = conn.execute("SELECT count(*), round(avg(value)) FROM readings").fetchone()
    # print("filas y media:", row)
