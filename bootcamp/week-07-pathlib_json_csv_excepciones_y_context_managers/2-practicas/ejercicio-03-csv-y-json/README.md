# Ejercicio 03 — CSV y JSON

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-csv.md) y [05](../../1-teoria/05-json.md)

## Objetivo

Escribir y leer un CSV con el módulo `csv`, ver por qué `split` no basta, y pasar datos de Python a JSON y de vuelta, con sus sorpresas de tipos. Los pasos 2 y 5 son `read_csv` y `write_json` del proyecto. Ejercicio **guiado**: descomentas cada paso de `formats_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-07-pathlib_json_csv_excepciones_y_context_managers/2-practicas/ejercicio-03-csv-y-json/starter
uv run python formats_lab.py
```

```
Ejercicio 03 · CSV y JSON
```

Los archivos van a `salida/`, junto a `formats_lab.py`.

## Pasos

### 1. Escribir un CSV con `csv.writer`

Descomenta el **PASO 1** y ejecuta:

```
etiqueta;valor
Norte;12,5
"Sur; centro";8
Centro;NA
```

`csv.writer` puso comillas **solo** en `"Sur; centro"`, el único campo que lleva el separador dentro. Abre `salida/medidas.csv` con LibreOffice Calc o Excel (separador `;`): verás dos columnas, con `Sur; centro` entero en la primera.

### 2. Leerlo con `csv.reader`

Descomenta el **PASO 2**:

```
Cabecera: ['etiqueta', 'valor']
  'Norte': '12,5' -> 12.5
  'Sur; centro': '8' -> 8.0
  'Centro': 'NA' -> None
Con split: ['"Sur', ' centro"', '8']
```

`next(reader)` saca la cabecera y el `for` sigue desde la segunda fila. Cada fila es una lista de **strings**: `'12,5'` hay que convertirlo, y `'NA'` es solo un texto hasta que tú decides que significa `None`. La última línea muestra por qué no basta un `split(";")`: parte el campo entre comillas y deja las comillas dentro.

Quita `delimiter=";"` del `csv.reader` y ejecuta:

```
ValueError: not enough values to unpack (expected 2, got 1)
```

Sin `delimiter`, `csv` parte por comas: la cabecera `etiqueta;valor` es un solo campo y el `for label, value` no puede desempaquetarla. Vuelve a ponerlo.

### 3. Leer por nombre con `csv.DictReader`

Descomenta el **PASO 3**:

```
  {'etiqueta': 'Norte', 'valor': '12,5'}
  {'etiqueta': 'Sur; centro', 'valor': '8'}
  {'etiqueta': 'Centro', 'valor': 'NA'}
```

`DictReader` usa la cabecera como claves: `row["valor"]` en lugar de `row[1]`. Con muchas columnas se lee mejor. Con dos columnas en un orden fijo, como el Observatorio, `csv.reader` basta.

### 4. Python ↔ texto JSON

Descomenta el **PASO 4**:

```
dumps: {"registros": 3, "mediana": 10.2, "falta": null, "ok": true, "rango": [8.0, 12.5], "2026": "año"}
loads: {'registros': 3, 'mediana': 10.2, 'falta': None, 'ok': True, 'rango': [8.0, 12.5], '2026': 'año'}
¿Igual? False
TypeError: Object of type set is not JSON serializable
```

Compara las dos primeras líneas: `None` se escribe `null` y `True`, `true`. La ida y la vuelta **no** dan lo mismo por dos razones: la tupla `(8.0, 12.5)` vuelve como lista, y la clave `2026` vuelve como el texto `"2026"`. Un `set` no cabe en JSON. Cambia `{"Norte", "Sur"}` por `sorted({"Norte", "Sur"})` y el error desaparece. Déjalo como estaba.

### 5. Archivos JSON con `dump` y `load`

Descomenta el **PASO 5**:

```
{
  "zona": "Peñalara",
  "registros": 3,
  "mediana": 10.2
}
load: {'zona': 'Peñalara', 'registros': 3, 'mediana': 10.2}
Sin ensure_ascii: {"zona": "Peñalara", "registros": 3, "mediana": 10.2}
JSONDecodeError en la línea 2: Illegal trailing comma before end of object
```

`indent=2` pone un elemento por línea y `ensure_ascii=False` deja la `ñ` tal cual. Sin él sale `ñ`, que es JSON válido pero ilegible. `json.dump` no escribe el salto de línea final: lo añade el `file.write("\n")`. La última línea es un JSON con una coma después del último elemento, algo que Python admite y JSON no: `JSONDecodeError` dice en qué línea está el problema.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ValueError: not enough values to unpack (expected 2, got 1)` | Falta `delimiter=";"`: es lo que muestra el paso 2 |
| Una línea en blanco entre filas del CSV (Windows) | Falta `newline=""` al abrir para escribir |
| `TypeError: Object of type set is not JSON serializable` | Convierte el conjunto a lista antes: `sorted(...)` |
| `ñ` en lugar de `ñ` | Falta `ensure_ascii=False` en `dump` o `dumps` |
| `¿Igual? False` | Es lo esperado: tuplas y claves numéricas no sobreviven a JSON |
| LibreOffice muestra una sola columna | Al abrir, elige `;` como separador |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Excepciones](../ejercicio-02-excepciones/README.md) | **Ejercicio 03 · CSV y JSON** | [Ejercicio 04 · Context managers](../ejercicio-04-context-managers/README.md) |
