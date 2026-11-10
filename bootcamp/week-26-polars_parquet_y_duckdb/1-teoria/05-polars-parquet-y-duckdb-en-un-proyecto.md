# 05 · Polars, Parquet y DuckDB en un proyecto

⏱️ 55 min

## 🎯 Objetivos

- Repartir el código nuevo entre `core` y la CLI sin que la CLI cargue Polars ni DuckDB al arrancar.
- Pasar datos de Polars a DuckDB sin `pyarrow`, con un archivo Parquet en medio.
- Probar el mismo resumen hecho con tres bibliotecas, con tolerancia en los `float` y `None` donde pandas pone `NaN`.
- Ejecutar SQL que escribe otra persona sin darle acceso a tus archivos.
- Medir qué gana cada herramienta, y qué cuesta en la imagen Docker.
- Elegir entre pandas, Polars y DuckDB para cada trabajo.

---

## 1. Dónde vive cada pieza

| Archivo | Qué sabe hacer | Qué importa |
|---|---|---|
| `core/frames.py` y `core/summaries.py` | Tablas de pandas: filtrar, resumir, series de tiempo | pandas |
| `core/columnar.py` | La serie como tabla de Polars, su resumen perezoso, y SQL sobre un Parquet | Polars, DuckDB, `model` |
| `cli.py` | `exportar` y `sql`, y `rows_table` para escribir cualquier resultado | Polars y DuckDB **solo** dentro de los comandos |

`columnar.py` sigue la regla de `frames` y `summaries`: no se reexporta en `core/__init__.py`. Importar Polars cuesta unos 0,1 s y DuckDB unos 0,07 s; sumados a pandas, `uv run observatorio --help` tardaría un tercio de segundo más sin usar ninguno. `test_importing_the_cli_does_not_load_polars_or_duckdb` lo vigila en otro proceso, como el de pandas de la semana 24.

`core` habla inglés (`label`, `value`, `count`) y la terminal, español: `rows_table` traduce las columnas con el mismo `NAMES` de la semana 25.

---

## 2. Polars escribe, DuckDB lee

Polars y DuckDB se pueden pasar tablas en memoria, pero a través de Arrow, y eso necesita `pyarrow`: una dependencia más de 55 MB comprimidos, con sus propios avisos de seguridad que vigilar. Tu proyecto no la necesita, porque los dos hablan **Parquet**:

```
Series ──frame_of──▶ pl.DataFrame ──write_parquet──▶ medidas.parquet ──read_parquet──▶ DuckDB
                                                           │
                                                           └──scan_parquet──▶ summary ──▶ exportar
```

- `exportar` escribe el Parquet y **vuelve a leerlo** para resumirlo. Si al guardar se perdiera algo (un tipo, los `null`, una fila), el resumen lo enseñaría.
- `sql` no sabe nada de Polars: lee el Parquet que haya, lo escribiera quien lo escribiera.
- El archivo es el contrato entre los dos comandos, y otras herramientas (un notebook en la semana 29, una hoja de cálculo con un complemento, Spark) pueden leerlo igual.

---

## 3. Probar con tres bibliotecas

### Lo que falta

pandas pone `NaN`; Polars y DuckDB, `None`. Para comparar el resumen de Polars con el de `summaries.summary`, el test traduce:

```python
expected = [
    (label, *(None if isinstance(v, float) and math.isnan(v) else v for v in row))
    for label, row in zip(table.index, table.itertuples(index=False), strict=True)
]
```

### Los `float`

pandas, Polars y DuckDB suman en distinto orden (por bloques, en paralelo, con otra precisión intermedia), y una media puede cambiar en la última cifra. `same_rows` compara los `float` con `math.isclose` y lo demás con `==`:

```python
math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9) if isinstance(a, float) and isinstance(b, float) else a == b
```

`abs_tol` hace falta para los valores cerca de cero: `rel_tol` solo, con un cero, no admite ninguna diferencia.

### Archivos con Hypothesis

`tmp_path` es una *fixture* de una ejecución del test, y Hypothesis ejecuta el mismo test cien veces: se quejaría de reutilizarla. Dos salidas:

- `io.BytesIO()`: `write_parquet` y `read_parquet` aceptan un "archivo" en memoria (`test_parquet_round_trip`);
- `tempfile.TemporaryDirectory()`, cuando hace falta una ruta de verdad, como en `query` (`test_query_agrees_with_the_polars_summary`).

### El orden en SQL

SQL no promete ningún orden sin `ORDER BY`. Para comparar con el resumen de Polars, que va en orden de aparición, el test ordena por `min(rowid)`: `rowid` es la posición de cada fila en la tabla de DuckDB, y el mínimo de cada grupo es su primera aparición.

---

## 4. SQL que no escribes tú

`sql` ejecuta lo que escriba quien usa la CLI. En tu máquina, eres tú. Pero `query` vive en `core`, y la API de la semana 20 podría usarla mañana con el SQL de cualquiera. Por eso `query` lo trata como **entrada no confiable** desde ya:

1. abre una base **en memoria**, nueva en cada llamada;
2. **copia** el Parquet a la tabla `medidas`;
3. `SET enable_external_access = false`: sin archivos, sin red, sin extensiones;
4. ejecuta el SQL.

El SQL puede hacer lo que quiera con `medidas`, incluso borrarla: es una copia en memoria que desaparece al salir del `with`. No puede leer `.env`, ni escribir en tu carpeta, ni volver a abrir el disco (teoría 04, sección 6). Los tests intentan las tres cosas.

El precio, medido con 100 000 medidas: conectar, 14 ms; copiar el Parquet, 8 ms; la consulta, 3 ms. Unos 30 ms en total, frente a 3 ms preguntando directamente al archivo. Para una consulta escrita a mano, 30 ms no se notan; si `query` estuviera detrás de una API con miles de llamadas por segundo, tocaría reutilizar la conexión.

---

## 5. Qué gana cada una

En la máquina del bootcamp, con las 100 000 medidas de `generar_medidas.py`:

| Operación | pandas | Polars | DuckDB |
|---|---|---|---|
| De `Series` a tabla | 8,9 ms | 6,6 ms | — |
| Resumen por etiqueta, en memoria | 7,9 ms | 2,1 ms | — |
| Resumen leyendo el Parquet | — | 3,7 ms | 30,7 ms (`query`, con la copia) |
| Escribir el archivo | 69 ms (CSV) | 3,9 ms (Parquet) | — |
| Tamaño del archivo | 1,04 MB (CSV) | 0,25 MB (Parquet) | — |

Y el comando entero:

| Comando | Tiempo | Dónde se va |
|---|---|---|
| `resumir perfil/grande.txt` | 1,25 s | Analizar el texto línea a línea con `Series.parse` |
| `exportar perfil/grande.txt ...` | 1,11 s | Lo mismo: lee el texto |
| `sql perfil/grande.parquet ...` | 0,68 s | Arrancar Python, importar y conectar; el Parquet se lee en milisegundos |

La lección de la semana 22 sigue en pie: mide antes de cambiar. Polars hace el resumen cuatro veces más rápido que pandas, pero el comando tarda lo mismo, porque casi todo el tiempo es leer el texto. Lo que de verdad cambia es **no volver a leer el texto**: una vez exportado, cada pregunta sale en menos de un segundo, y casi todo es arrancar.

---

## 6. Lo que cuesta

```
week-25   508 MB
week-26   850 MB
```

342 MB más en la imagen `runtime`. Los dos paquetes nuevos:

| Paquete | En disco |
|---|---|
| `_polars_runtime_32` (el motor de Polars, en Rust) | 170 MB |
| `_duckdb.abi3.so` (el motor de DuckDB, en C++) | 65 MB |

Más que pandas (83 MB) y NumPy (43 MB) juntos. Una imagen más grande tarda más en construirse, en subirse y en arrancar en un servidor nuevo, y tiene más código en el que puede aparecer una vulnerabilidad.

En un proyecto de verdad, raramente querrías las tres bibliotecas de tablas a la vez. Tu Observatorio las tiene porque es un proyecto para aprender; la decisión de cada equipo sería otra:

| Si tu trabajo es... | Elige | Por qué |
|---|---|---|
| Explorar, graficar, estadística, bibliotecas que esperan pandas | pandas | El ecosistema: matplotlib, seaborn, statsmodels, scikit-learn (semanas 27, 28 y 31) |
| Transformar tablas grandes en código, con tipos estrictos | Polars | Rápido, en paralelo, perezoso, y falla donde está el error |
| Preguntar con SQL a archivos, o compartir consultas con quien sabe SQL y no Python | DuckDB | SQL estándar, sin servidor, lee Parquet y CSV directamente |
| Muchos usuarios escribiendo a la vez | PostgreSQL | Ninguna de las tres es una base de datos para eso |

Polars `runtime-32` usa índices de 32 bits: hasta unos 4 300 millones de filas por tabla. Si alguna vez necesitas más, existe `polars[rt64]`. Para tu Observatorio, sobra.

---

## 7. Errores frecuentes

| Error | Por qué está mal | Qué hacer |
|---|---|---|
| Reexportar `columnar` en `core` | Todos los comandos cargarían Polars y DuckDB | Importa el módulo dentro de cada comando |
| Añadir `pyarrow` para pasar tablas de Polars a DuckDB | Otra dependencia grande que vigilar | Un archivo Parquet entre los dos |
| Comparar medias de dos bibliotecas con `==` | Suman en distinto orden | `math.isclose` con `rel_tol` y `abs_tol` |
| `tmp_path` en un test con Hypothesis | La *fixture* es de una sola ejecución | `io.BytesIO` o `tempfile.TemporaryDirectory` |
| Comparar el resultado de un SQL sin `ORDER BY` | El orden no está garantizado | `ORDER BY`, o compara conjuntos |
| Ejecutar SQL ajeno con acceso al disco | Lee y escribe tus archivos | Copiar y `SET enable_external_access = false` |
| Cambiar de pandas a Polars "porque es más rápido" sin medir | El tiempo puede estar en otro sitio | Mide el comando entero primero |

---

## ✅ Qué debes saber al terminar

- [ ] Por qué `columnar.py` no se reexporta, y cuánto cuesta importar Polars y DuckDB.
- [ ] Cómo pasan los datos de Polars a DuckDB sin `pyarrow`.
- [ ] Qué hay que traducir y qué tolerancia usar al comparar pandas, Polars y DuckDB en un test.
- [ ] Por qué `query` copia la tabla y cierra el disco, y cuánto cuesta.
- [ ] Dónde se va el tiempo de `exportar` y de `sql`.
- [ ] Cuánto crece la imagen, y qué herramienta elegirías para cada trabajo.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [04 · DuckDB: SQL sin servidor](04-duckdb-sql-sin-servidor.md) | **05 · Polars, Parquet y DuckDB en un proyecto** | [Ejercicio 01 · Polars: expresiones y contextos](../2-practicas/ejercicio-01-polars-expresiones-y-contextos/README.md) |
