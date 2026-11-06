# Ejercicio 02 — Excepciones

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-excepciones.md)

## Objetivo

Capturar excepciones con `try` y `except`, ver en qué orden corren `else` y `finally`, seguir una excepción mientras sube por las llamadas, y traducir un error de bajo nivel en uno propio con `raise ... from`. El paso 4 es el patrón de `storage.py` del proyecto. Ejercicio **guiado**: descomentas cada paso de `errors_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-07-pathlib_json_csv_excepciones_y_context_managers/2-practicas/ejercicio-02-excepciones/starter
uv run python errors_lab.py
```

```
Ejercicio 02 · Excepciones
```

## Pasos

### 1. Capturar con `try` y `except`

Descomenta el **PASO 1** y ejecuta:

```
  '12,5' -> 12.5
  '8' -> 8.0
  'NA' -> None
  '' -> None
Mensaje: could not convert string to float: 'NA'
```

Para `"NA"` y `""`, `float` lanza `ValueError`, el `except` lo captura y la función devuelve `None`. Es `parse_value` de tu capa 0, escrito con una excepción en lugar de comprobar antes. Con `as error`, el `except` recibe la excepción y puede leer su mensaje.

Cambia `except ValueError:` por `except TypeError:` y ejecuta:

```
ValueError: could not convert string to float: 'NA'
```

El `except` solo captura el tipo que nombra: el `ValueError` pasa de largo y para el programa. Vuelve a `ValueError`.

### 2. `else` y `finally`

Descomenta el **PASO 2**:

```
divide(30, 3):
  else: media 10.0
  finally: siempre
divide(30, 0):
  except: no hay valores
  finally: siempre
```

Sin error, corren `else` y `finally`; con error, `except` y `finally`. `finally` corre en los dos casos, y también correría si la excepción no se capturara. El `try` tiene una sola línea, la división, y el `print` de la media va en el `else`: así el `except ZeroDivisionError` no puede capturar por accidente un error del `print`.

### 3. Una excepción sube por las llamadas

Descomenta el **PASO 3**:

```
  read_all: empieza
  read_value: empieza
  read_value: termina
  read_value: empieza
  capturado arriba: could not convert string to float: 'x'
```

Sigue las líneas: `read_value("1")` termina bien. `read_value("x")` empieza y se corta en `float`: no escribe "termina". La excepción sube a `read_all`, que tampoco la captura y no escribe "termina", y sigue hasta el `try` del final. El `"3"` nunca se lee.

Quita el `try` y el `except` del final (deja solo `read_all(["1", "x", "3"])`) y ejecuta. El *traceback* muestra el mismo camino, de abajo arriba: `float(text)` dentro de `read_value`, dentro de `read_all`, dentro del módulo. Vuelve a ponerlo.

### 4. Excepción propia y `raise ... from`

Descomenta el **PASO 4**:

```
Mensaje: no existe el archivo no-existe.csv
Tipo: DataFileError
Causa: FileNotFoundError(2, 'No such file or directory')
```

`read_lines` captura el `FileNotFoundError` de Python y lanza una `DataFileError` con un mensaje en español. Quien la llama solo tiene que capturar `DataFileError`, sin saber nada de errores de archivo. `from error` guarda el original en `__cause__`.

Ahora quita el `except DataFileError` (deja solo `read_lines(Path("no-existe.csv"))`, sin `try`) y ejecuta. El *traceback* muestra los dos errores unidos por:

```
The above exception was the direct cause of the following exception:
```

Quita también el `from error` y vuelve a ejecutar. La frase cambia a `During handling of the above exception, another exception occurred:`, que dice "hubo un segundo error mientras se trataba el primero": falso, y confuso para quien depura. Deja el `from error` y el `try` como estaban.

### 5. Familias de excepciones

Descomenta el **PASO 5**:

```
  'no-existe.txt': FileNotFoundError | ¿es OSError? True
  '.': IsADirectoryError | ¿es OSError? True
Familia de FileNotFoundError: ['FileNotFoundError', 'OSError', 'Exception', 'BaseException', 'object']
```

Un solo `except OSError` captura los dos errores, porque los dos son de la familia `OSError`. La última línea muestra la cadena completa: `FileNotFoundError` es un `OSError`, que es una `Exception`. Tu `DataFileError` cuelga directamente de `Exception`. `KeyboardInterrupt` (Ctrl+C) cuelga de `BaseException` y no de `Exception`. Por eso `except Exception` no la captura y `except:` a secas sí.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'error' is not defined` | Usaste la variable del `except` fuera de él: Python la borra al salir |
| El `except` no captura nada | El tipo no coincide: mira el tipo en la última línea del *traceback* |
| `IndentationError` al descomentar una función | Las líneas vacías dentro de un bloque comentado llevan `#`: quita también ese `#` |
| `Causa: None` | Falta `from error` en el `raise` |
| `'.': PermissionError` en Windows | Windows no deja abrir una carpeta y da otro error de la misma familia: sigue siendo `OSError` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Archivos y rutas](../ejercicio-01-archivos-y-rutas/README.md) | **Ejercicio 02 · Excepciones** | [Ejercicio 03 · CSV y JSON](../ejercicio-03-csv-y-json/README.md) |
