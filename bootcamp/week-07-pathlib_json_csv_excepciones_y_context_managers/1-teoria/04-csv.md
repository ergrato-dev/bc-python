# 04 · CSV

⏱️ 45 min

## 🎯 Objetivos

- Explicar qué es un CSV y por qué en español se separa con `;`.
- Leer con `csv.reader` y `csv.DictReader`, y escribir con `csv.writer`.
- Saber por qué se abre con `newline=""` y qué hacen las comillas.
- Validar la cabecera antes de confiar en las filas.

---

## 1. Qué es un CSV

Un **CSV** (*comma-separated values*, "valores separados por comas") es una tabla guardada como texto: una fila por línea y las columnas separadas por un carácter. La primera línea suele ser la **cabecera**, con el nombre de cada columna:

```
etiqueta;valor
Norte;12,5
Centro;NA
Sur;8
```

Es el formato que exportan Excel, LibreOffice, Google Sheets y casi cualquier portal de datos abiertos: si tus datos vienen de algún sitio, lo más probable es que lleguen en CSV.

En inglés el separador es la coma, y el punto es el decimal. En español, la coma es el decimal (`12,5`), así que Excel y LibreOffice en español separan con **punto y coma**. Por eso el CSV del Observatorio usa `;`, el mismo formato `etiqueta;valor` de tus líneas desde la semana 2.

## 2. ¿Por qué no un `split(";")`?

Para `Norte;12,5`, `line.split(";")` funciona. Pero un CSV permite meter el separador dentro de un campo, rodeándolo de **comillas**:

```
etiqueta;valor
"Sur; centro";8
"Dice ""hola""";1
```

Las comillas dicen "esto es un solo campo, aunque lleve `;`", y unas comillas dentro de un campo se escriben dobles (`""`). `split` no sabe nada de eso y parte mal. El módulo `csv` de la biblioteca estándar sí lo sabe, y funciona igual en lectura y en escritura.

## 3. Leer: `csv.reader`

```python
import csv

with path.open(encoding="utf-8", newline="") as file:
    rows = csv.reader(file, delimiter=";")
    header = next(rows)            # ['etiqueta', 'valor']
    for row in rows:
        print(row)                 # ['Norte', '12,5'], ['Sur; centro', '8'], ...
```

| Detalle | Por qué |
|---|---|
| `delimiter=";"` | Sin él, `csv` parte por comas y `Norte;12,5` da `['Norte;12', '5']` |
| `newline=""` | Deja los saltos de línea a `csv`, que así entiende un campo entre comillas con un salto de línea dentro |
| `next(rows)` | `csv.reader` es un iterador (semana 6): `next` saca la cabecera y el `for` sigue desde la segunda fila |
| Cada fila es `list[str]` | **Todo es texto**: `'12,5'` sigue siendo un string; convertirlo es tu trabajo |

`csv.reader` acepta cualquier iterable de strings, no solo un archivo abierto: una lista de líneas también vale. `read_csv` del proyecto lo aprovecha para reutilizar `read_lines`, que ya traduce los errores de archivo. El precio es que un campo con un salto de línea dentro se parte, y en el proyecto queda anotado.

## 4. Validar la cabecera

Un CSV no lleva tipos ni esquema: cualquiera puede mandarte `zona;medida`, `valor;etiqueta` o la exportación de otro sistema. Si lees las filas sin mirar la cabecera, procesas columnas equivocadas sin enterarte. La primera defensa es comprobarla y parar si no es la esperada:

```python
HEADER = ["etiqueta", "valor"]

header = next(rows, None)        # None si el archivo está vacío
if header is None:
    raise DataFileError(f"{path} está vacío")
if header != HEADER:
    raise DataFileError(f"cabecera inesperada en {path}: {';'.join(header)}")
```

`next(iterador, None)` devuelve `None` en lugar de lanzar `StopIteration` cuando no hay nada. Es la misma idea que `max(..., default=...)` de la semana 6.

## 5. Leer por nombre: `csv.DictReader`

`DictReader` usa la cabecera como claves y da cada fila como diccionario:

```python
with path.open(encoding="utf-8", newline="") as file:
    for row in csv.DictReader(file, delimiter=";"):
        print(row["etiqueta"], row["valor"])    # Norte 12,5
```

Se lee mejor cuando hay muchas columnas y no te importa su orden. Para el Observatorio, con dos columnas en un orden fijo, `csv.reader` y una cabecera comprobada son suficientes.

## 6. Escribir: `csv.writer`

```python
records = [["Norte", "12,5"], ["Sur; centro", "8"]]

with path.open("w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(["etiqueta", "valor"])
    writer.writerows(records)
```

El archivo resultante:

```
etiqueta;valor
Norte;12,5
"Sur; centro";8
```

`csv.writer` pone comillas **solo** donde hacen falta. `newline=""` también importa al escribir: `csv` termina cada fila con `\r\n`, el estándar de los CSV, y sin `newline=""` en Windows aparecería una línea en blanco entre fila y fila. Los números se escriben con `str()`, con punto decimal. Si el CSV es para un Excel en español, conviértelos tú: `f"{value:.1f}".replace(".", ",")`.

En la semana 25, pandas lee un CSV con `pd.read_csv("medidas.csv", sep=";", decimal=",")`. Debajo hace lo mismo, con los tipos ya convertidos.

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| Filas como `['Norte;12', '5']` | Falta `delimiter=";"` | Pásalo al reader y al writer |
| Comillas dentro de los campos (`'"Norte"'`) | Partiste con `split` | Usa `csv.reader` |
| Una línea en blanco entre filas (Windows) | Falta `newline=""` al escribir | `open(..., newline="")` |
| `StopIteration` en `next(rows)` | El archivo está vacío | `next(rows, None)` y comprueba |
| `ValueError: dict contains fields not in fieldnames: 'x'` | `DictWriter` recibió una clave que no está en `fieldnames` | Añádela a `fieldnames` o quítala del diccionario |
| `TypeError` o comparaciones raras con números | Los campos de un CSV son `str` | Convierte con `float`, como `parse_value` |

## ✅ Qué debes saber al terminar

- [ ] Qué es un CSV y por qué en español se separa con `;`.
- [ ] Por qué `csv.reader` y no `split`, y qué hacen las comillas.
- [ ] Para qué sirven `delimiter`, `newline=""` y `next(rows, None)`.
- [ ] Por qué hay que comprobar la cabecera.
- [ ] Cómo escribir un CSV con `csv.writer` y cuándo usar `DictReader`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [03 · Context managers](03-context-managers.md) | **04 · CSV** | [05 · JSON](05-json.md) |
