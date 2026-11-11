# Ejercicio 03 — ETL desde PostgreSQL

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-etl-desde-postgresql.md)

## Objetivo

Mover datos de PostgreSQL a pandas y de vuelta, como lo hará el comando `extraer` de tu proyecto:

- extraer con `pd.read_sql` y una consulta de SQLAlchemy;
- fijar los tipos;
- dejar que PostgreSQL agrupe;
- pasar valores como parámetros, y ver qué pasa si no;
- leer por partes, transformar y cargar de vuelta sin duplicar.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-29-eda_notebooks_reproducibles_y_etl_desde_postgresql/2-practicas/ejercicio-03-etl-desde-postgresql/starter
docker compose up -d --wait
uv run python main.py
```

```
Ejercicio 03 · ETL desde PostgreSQL
readings: 200000 filas
```

El PostgreSQL del ejercicio escucha en el puerto **5433** (el de tu proyecto usa el 5432). `main.py` crea la tabla `readings` y genera 200 000 medidas, una por hora de cinco estaciones, **dentro** de PostgreSQL, con `generate_series`: así no viajan por la red. `setseed` fija la secuencia de `random()`: siempre las mismas medidas. Al terminar el ejercicio, `docker compose down -v`.

## Pasos

### 1. Extraer con `read_sql`

Descomenta el **PASO 1** y ejecuta:

```
Norte: (40000, 2) · 0.6 MB en memoria
{'measured_at': dtype('<M8[us]'), 'value': dtype('float64')}
          measured_at  value
0 2026-01-01 00:00:00   24.2
1 2026-01-01 01:00:00   22.5
2 2026-01-01 02:00:00   23.1
```

- `pd.read_sql` recibe una consulta de SQLAlchemy y una conexión, y devuelve un `DataFrame`. El `WHERE` lo aplica PostgreSQL: llegan 40 000 filas, no 200 000.
- Los tipos salen de PostgreSQL: `timestamp` es `datetime64`, `double precision` es `float64`.

### 2. Fijar los tipos

Descomenta el **PASO 2** y ejecuta:

```
deducidos: {'station': <StringDtype(storage='python', na_value=nan)>, 'value': dtype('O')}
fijados:   {'station': <StringDtype(storage='python', na_value=nan)>, 'value': dtype('float64')}
valores: [None, None, None] → [nan, nan, nan]
```

- Tres filas sin valor. pandas deduce el tipo de lo que llega: solo `None`, así que `object`.
- Con `dtype=`, `value` es `float64` llegue lo que llegue, y los `None` son `NaN`. Así lo hace `extract` en tu proyecto (teoría 04, sección 3).

### 3. Que trabaje PostgreSQL

Descomenta el **PASO 3** y ejecuta:

```
pandas: 200000 filas traídas · 0.16 s
SQL:    5 filas traídas · 0.030 s
¿las mismas medias? True
```

Tus tiempos serán otros: son los de tu máquina.

- La media de cada estación, dos veces: trayendo las 200 000 filas y agrupando con pandas, y con `GROUP BY` en PostgreSQL, que devuelve 5 filas.
- Los mismos números, redondeados a tres decimales. Con una base en otro servidor, la diferencia de tiempo crece con cada fila que viaja.

### 4. Parámetros, nunca texto pegado

Descomenta el **PASO 4** y ejecuta:

```
pegado:    200000 filas
parámetro: 0 filas
Sur: 40000 filas
```

- El nombre de estación `Norte' OR '1'='1`, pegado con una f-string, se convierte en SQL: `WHERE station = 'Norte' OR '1'='1'`, verdad para todas las filas. Es una **inyección de SQL**.
- Como parámetro (`:station`), PostgreSQL lo recibe como un dato: ninguna estación se llama así.
- Con `read_sql`, los parámetros van en `params=`.

### 5. Por partes, sin traerlo todo

Descomenta el **PASO 5** y ejecuta:

```
4 partes · 193907 valores · media 20.0014 · PostgreSQL 20.0014
```

- `chunksize=50_000` convierte `read_sql` en un iterador de `DataFrame` de hasta 50 000 filas. `stream_results=True` hace que las filas lleguen del servidor por partes; sin él, el driver las traería todas antes de trocearlas.
- Sumas y recuentos se acumulan parte a parte, y con ellos la media. 193 907 valores: los 200 000 menos los `NULL`, que `count` no cuenta.

### 6. Transformar y cargar de vuelta

Descomenta el **PASO 6** y ejecuta:

```
transformado: 200000 medidas → 8335 días
to_sql(if_exists='replace'): daily tiene 8335 filas
to_sql(if_exists='replace'): daily tiene 8335 filas
to_sql(if_exists='append'): daily tiene 16670 filas
  station         day   mean  measurements
0  Centro  2026-01-01  20.74            24
1  Centro  2026-01-01  20.74            24
2    Este  2026-01-01  19.63            24
```

- La transformación: una media y un recuento por estación y día (1 667 días por estación).
- `to_sql` la carga en la tabla `daily`. Con `replace`, ejecutarlo dos veces deja lo mismo: es **idempotente**. Con `append`, cada ejecución duplica las filas: el Centro aparece dos veces el 1 de enero.
- `engine.begin()` abre una transacción que se confirma al salir del `with`: la carga entra entera o no entra.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `OperationalError: connection ... port 5433 failed: Connection refused` | El PostgreSQL del ejercicio no está arrancado: `docker compose up -d --wait` dentro de `starter/` |
| `Bind for 127.0.0.1:5433 failed: port is already allocated` | Otro contenedor usa el 5433, quizá el de la semana 19: `docker compose -p practicas-semana-19 down` |
| `ModuleNotFoundError: No module named 'psycopg'` | Ejecuta con `uv run python main.py` dentro de `starter/` |
| `¿las mismas medias? False` | Comparas sin redondear, o sin ordenar por estación: los dos lados necesitan `round(3)` y `sort_index()` |
| El paso 5 tarda y usa mucha memoria | Falta `execution_options(stream_results=True)` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Notebooks por dentro](../ejercicio-02-notebooks-por-dentro/README.md) | **Ejercicio 03 · ETL desde PostgreSQL** | [Ejercicio 04 · Reproducible o no](../ejercicio-04-reproducible-o-no/README.md) |
