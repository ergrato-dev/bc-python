# Ejercicio 02 — Strings

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-strings-a-fondo.md)

## Objetivo

Recorrer con las manos lo que harás con texto en el proyecto: cortar con índices y slices, limpiar con métodos que devuelven un texto nuevo, partir campos y comparar texto que viene de fuera. Ejercicio **guiado**: descomentas cada paso de `strings_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-02-operadores_strings_io_y_match/2-practicas/ejercicio-02-strings/starter
uv run python strings_lab.py
```

Salida esperada: `Ejercicio 02 · Strings`. En cada paso: predice, descomenta (`Ctrl+K Ctrl+U`), ejecuta y compara. Abajo están las **líneas nuevas** de cada paso.

## Pasos

### 1. Índices y slicing

Descomenta el **PASO 1**:

```
Primero y último: O o
Slices: Obs torio oirotavresbO
Fuera de rango: ''
```

Con la imagen de la teoría 03 delante, cuenta las posiciones de `"Observatorio"` (12 caracteres) y comprueba cada slice. `repr` muestra las comillas, así se ve que `s[50:]` es un texto vacío y no un error. En el REPL, prueba `s[50]`: ese sí falla con `IndexError`.

### 2. Los `str` no cambian

Descomenta el **PASO 2**:

```
Sin guardar: '  ab 12 '
Guardado: 'AB-12'
```

La línea `code.strip()` calculó un texto limpio y lo tiró: `code` sigue igual. La segunda vez el resultado se guarda en `code`, después de encadenar tres métodos (cada uno recibe lo que devolvió el anterior).

### 3. `partition` y desempaquetar

Descomenta el **PASO 3**:

```
Correo: a***@correo.co
Extensiones: csv ''
```

| Línea | Qué pasa |
|---|---|
| `user, _, domain = ....partition("@")` | Las 3 partes van a 3 nombres; el separador va a `_` porque no se usa |
| `user[:1]` | La primera letra. Con un slice, un `user` vacío da `""` en vez de `IndexError` |
| `filename.rpartition(".")` | Parte por el **último** punto: `"datos.final.CSV"` da `("datos.final", ".", "CSV")` |
| `extension.lower() if dot else ""` | Si no había punto, `dot` es `""` (falso) y no hay extensión |

Prueba en el REPL `"LEEME".rpartition(".")` para ver por qué hace falta mirar `dot`.

### 4. `split` y `join`

Descomenta el **PASO 4**:

```
Campos: ['Norte', '12,5', '', 'µg/m³']
Palabras: 4
Unidas: PM2.5 / PM10 / O3
```

`split(";")` respeta el campo vacío entre los dos `;`: así se ve un dato faltante en una línea CSV. `split()` sin argumento se salta todos los espacios repetidos. `" / ".join(...)` hace lo contrario de `split`: une con el texto que va antes del punto.

### 5. Palíndromos

Descomenta el **PASO 5**:

```
Palíndromos: True False
```

Sigue `"Anita lava la tina"`: `casefold()` da `"anita lava la tina"`, `replace(" ", "")` da `"anitalavalatina"`, y al revés (`[::-1]`) es el mismo texto.

### 6. Comparar texto que viene de fuera

Descomenta el **PASO 6**:

```
Longitudes: 4 5
Con ==: False
Con same_text: True
```

`"Café"` normalizado en forma NFD tiene 5 caracteres: la `e` y la tilde van por separado. Se ve igual, pero `==` dice que no es igual. `normalize_text` hace los tres pasos de la teoría 03 (NFC, `strip`, `casefold`) y `same_text` compara los resultados. Es la función que usarás cada vez que compares etiquetas escritas por personas.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 's' is not defined` | Descomentaste una línea de un paso sin la que crea la variable |
| `ValueError: not enough values to unpack (expected 3, got 2)` | Cambiaste `partition` por `split`: `split` da tantas partes como haya |
| Tu predicción de los slices no coincide | Contaste desde 1: el primer índice es 0, y el `fin` del slice no se incluye |
| En la terminal, `µ` o `³` salen como `?` o símbolos raros | Tu terminal no usa UTF-8: en WSL2, `export LANG=C.UTF-8` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Operadores y condicionales](../ejercicio-01-operadores-y-condicionales/README.md) | **Ejercicio 02 · Strings** | [Ejercicio 03 · Formateo y t-strings](../ejercicio-03-formateo-y-t-strings/README.md) |
