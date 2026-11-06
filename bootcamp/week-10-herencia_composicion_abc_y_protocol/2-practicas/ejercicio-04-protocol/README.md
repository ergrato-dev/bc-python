# Ejercicio 04 — `Protocol`

⏱️ 1 h · Teoría previa: [04](../../1-teoria/04-protocol.md)

## Objetivo

Ver el *duck typing* en acción, darle nombre con un `Protocol`, descubrir qué comprueba y qué no `@runtime_checkable`, y dejar que mypy encuentre sin ejecutar los errores que en ejecución pasan o llegan tarde. Es el `Source` de tu proyecto. Ejercicio **guiado**: descomentas cada paso de `protocol_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-10-herencia_composicion_abc_y_protocol/2-practicas/ejercicio-04-protocol/starter
uv run python protocol_lab.py
```

```
Ejercicio 04 · Protocol
```

Los pasos 2 y 3 usan las clases del paso 1: descomenta en orden.

## Pasos

### 1. *Duck typing*

Descomenta el **PASO 1** y ejecuta:

```
Fixed: Norte;12,5 · Shouting: ESTE;3
Error: 'PosixPath' object has no attribute 'lines'
```

`Fixed` y `Shouting` no tienen nada en común salvo un método `lines()`. `first_line` no tiene tipos y no pregunta de qué clase es su argumento: llama a `lines()` y funciona con las dos. Con un `Path` también "funciona" hasta la llamada, y ahí falla. Python no exige heredar de nada: si el objeto tiene el método, vale. El problema es que el error solo llega al ejecutar.

### 2. Un `Protocol` con nombre

Descomenta el **PASO 2** y ejecuta:

```
Líneas: 2 y 3
¿Fixed hereda de Source? False
Error: Instance and class checks can only be used with @runtime_checkable protocols
Error: 'PosixPath' object has no attribute 'lines'
```

`Source` describe lo que necesita `count_lines`: un método `lines()` que devuelve `list[str]`. `Fixed` y `Shouting` lo cumplen sin heredar de él (`Source` no está en su MRO). En ejecución, nada cambia: el `Path` sigue fallando igual, y `isinstance` con un `Protocol` normal ni siquiera se permite. El `Protocol` es para mypy, que lo verás en el paso 6.

### 3. `@runtime_checkable` y sus límites

Descomenta el **PASO 3** y ejecuta:

```
  Fixed: True
  PosixPath: False
  Liar: True
  WrongType: True
Líneas de WrongType: 10
```

Con `@runtime_checkable`, `isinstance` funciona. Pero mira lo que comprueba: solo que el objeto **tenga** un atributo llamado `lines`. `Liar` tiene `lines = 42`, que ni siquiera es un método, y pasa. `WrongType` tiene un `lines()` que devuelve un `str`, y también pasa. Y `count_lines(WrongType())` da 10, el número de **caracteres** de `"Norte;12,5"`, sin ningún error: el peor tipo de fallo, el silencioso. `isinstance` sirve para tests y comprobaciones rápidas; la comprobación de verdad es la de mypy.

### 4. Los protocolos de `collections.abc`

Descomenta el **PASO 4** y ejecuta:

```
len: 2 · ¿Sized? True · ¿Iterable? False
```

`Shelf` no hereda de nada. Como tiene `__len__`, `len()` funciona y es un `Sized`. No tiene `__iter__`, así que no es un `Iterable`: `for book in shelf` fallaría. En la semana 11 le darás `__iter__` y entrará en los `for`.

### 5. Un `Protocol` para las piezas de un objeto

Descomenta el **PASO 5** y ejecuta:

```
  AllReadings: [10.0, 20.0, 30.0]
  LastReading: [30.0]
```

Es el problema del paso 4 del ejercicio 02: dos clases de lecturas que no heredan una de otra. `ReadingStore` dice lo que necesita `record_all` (`add` y `values`), y las dos lo cumplen. Fíjate en `stores: list[ReadingStore]`: sin esa anotación, mypy deduciría que la lista es de `object` (lo único que tienen en común las dos clases) y se quejaría al pasar cada elemento a `record_all`.

### 6. Lo que ve mypy

```bash
uv run --with mypy==2.4.1 mypy protocol_lab.py
```

```
protocol_lab.py:56: error: Only @runtime_checkable protocols can be used with instance and class checks  [misc]
protocol_lab.py:60: error: Argument 1 to "count_lines" has incompatible type "Path"; expected "Source"  [arg-type]
protocol_lab.py:84: error: Argument 1 to "count_lines" has incompatible type "WrongType"; expected "Source"  [arg-type]
protocol_lab.py:84: note: Following member(s) of "WrongType" have conflicts:
protocol_lab.py:84: note:     Expected:
protocol_lab.py:84: note:         def lines(self) -> list[str]
protocol_lab.py:84: note:     Got:
protocol_lab.py:84: note:         def lines(self) -> str
Found 3 errors in 1 file (checked 1 source file)
```

- La línea 60 es el `Path` del paso 2: mypy lo ve sin ejecutar.
- La línea 84 es el fallo **silencioso** del paso 3, el que en ejecución dio 10 sin avisar. mypy no solo lo detecta: la nota compara la firma esperada (`Expected`) con la que tiene `WrongType` (`Got`).
- El `Path` del paso 1 **no** aparece: `first_line` no tiene tipos, y mypy no comprueba lo que no sabe. Es la razón para anotar con un `Protocol` en lugar de dejar el parámetro sin tipo.
- `Fixed`, `Shouting`, `AllReadings` y `LastReading` no dan ningún error: cumplen sus protocolos sin haberlos mencionado nunca.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'Fixed' is not defined` | Los pasos 2 y 3 usan las clases del paso 1: descoméntalo antes |
| `NameError: name 'count_lines' is not defined` en el paso 3 | Descomenta antes el paso 2 |
| En el paso 3 sale el error de `@runtime_checkable` | Falta el decorador encima de `class CheckedSource(Protocol)` |
| mypy da más errores o en otras líneas | Descomentaste algo distinto o añadiste líneas: compara los números de línea con los de tu archivo |
| mypy: `incompatible type "object"; expected "ReadingStore"` | Falta la anotación `stores: list[ReadingStore]` del paso 5 |
| mypy tarda la primera vez | Descarga mypy en un entorno temporal; la segunda vez va rápido |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Clases abstractas](../ejercicio-03-clases-abstractas/README.md) | **Ejercicio 04 · `Protocol`** | [Proyecto](../../3-proyecto/README.md) |
