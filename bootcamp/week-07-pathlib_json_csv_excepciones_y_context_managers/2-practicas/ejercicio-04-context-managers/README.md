# Ejercicio 04 — Context managers

⏱️ 1 h · Teoría previa: [03](../../1-teoria/03-context-managers.md)

## Objetivo

Comprobar que `with` cierra un archivo también cuando hay un error, escribir tus propios context managers con `@contextmanager` y abrir dos archivos en un solo `with`. Ejercicio **guiado**: descomentas cada paso de `with_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-07-pathlib_json_csv_excepciones_y_context_managers/2-practicas/ejercicio-04-context-managers/starter
uv run python with_lab.py
```

```
Ejercicio 04 · Context managers
```

## Pasos

### 1. `with` cierra también cuando hay un error

Descomenta el **PASO 1** y ejecuta:

```
Dentro, ¿cerrado? False
Capturado: algo falló a mitad
Fuera, ¿cerrado? True
Se guardó: ['Norte;12,5']
```

El `ValueError` sale del `with` a mitad del bloque, y aun así el archivo se cerró: el `with` hizo su salida antes de que la excepción siguiera subiendo. Por eso lo escrito antes del error está en el disco. Sin `with`, el `close()` que iría detrás del `raise` nunca se habría ejecutado.

### 2. Un context manager propio

Descomenta el **PASO 2**:

```
  entra en lectura
  cuerpo con LECTURA
  sale de lectura
  entra en escritura
  sale de escritura
  capturado fuera: disco lleno
```

`@contextmanager` convierte la función en un context manager. Lo de antes del `yield` es la entrada; el valor del `yield` va a la variable de `as`; el cuerpo del `with` corre en el momento del `yield`; lo del `finally` es la salida. En el segundo `with`, el cuerpo lanza `OSError` y la salida se escribe igualmente, y después el error sigue subiendo hasta el `except`.

Quita el `try` y el `finally` de `announce` (deja `yield name.upper()` y el `print` de salida debajo, al mismo nivel) y ejecuta. Con el error, `sale de escritura` ya no aparece. Vuelve a ponerlos.

### 3. Un cronómetro

Descomenta el **PASO 3**:

```
  ordenar un millón: 48.4 ms
  sumar un millón: 12.4 ms
```

Tus milisegundos serán otros; la proporción, parecida. Es el mismo patrón con `perf_counter` de la semana 6, empaquetado: cualquier bloque se mide envolviéndolo en `with timer("..."):`, sin tocar su código.

### 4. Dos archivos en un `with`, y `suppress`

Descomenta el **PASO 4**:

```
Destino: ['Norte;12,5', 'Sur;8']
Siguió sin error
```

Un solo `with` abre los dos archivos, y al salir los cierra a los dos, en orden inverso. Los paréntesis permiten escribir uno por línea. `suppress(FileNotFoundError)` se traga el error de borrar un temporal que no existe. Fíjate en que el `print` de dentro **no** se escribe: el error corta el bloque, como en un `try`, y `suppress` solo evita que siga subiendo.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `TypeError: 'generator' object does not support the context manager protocol (missed __exit__ method)` | Falta `@contextmanager` encima de la función |
| `RuntimeError: generator didn't yield` | La función no llega al `yield`: revisa la sangría |
| La salida no se escribe cuando hay error | Falta `try` y `finally` alrededor del `yield` |
| `ValueError: I/O operation on closed file.` | Usaste el archivo fuera del `with` |
| `SyntaxError` en el `with (` | Cada recurso lleva su `as`, van separados por comas y el paréntesis se cierra con `):` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · CSV y JSON](../ejercicio-03-csv-y-json/README.md) | **Ejercicio 04 · Context managers** | [Proyecto · Observatorio, capa 6](../../3-proyecto/README.md) |
