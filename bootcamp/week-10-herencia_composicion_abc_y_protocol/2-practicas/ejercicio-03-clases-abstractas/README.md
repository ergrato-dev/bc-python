# Ejercicio 03 — Clases abstractas

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-clases-abstractas.md) y [05](../../1-teoria/05-disenar-jerarquias.md)

## Objetivo

Pasar de una base que lanza `NotImplementedError` a una clase abstracta con `ABC` y `@abstractmethod`, escribir un método plantilla, una propiedad abstracta y una base abstracta que es una *dataclass*. El paso 5 es, casi línea a línea, el `FileSource` de tu proyecto. Ejercicio **guiado**: descomentas cada paso de `abc_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-10-herencia_composicion_abc_y_protocol/2-practicas/ejercicio-03-clases-abstractas/starter
uv run python abc_lab.py
```

```
Ejercicio 03 · clases abstractas
```

Cada paso define sus propias clases: puedes descomentarlos de uno en uno, en orden. Los pasos 3 y 5 escriben archivos en una carpeta temporal (`tempfile.TemporaryDirectory`) que se borra sola al salir del `with`.

## Pasos

### 1. Una base con `NotImplementedError`

Descomenta el **PASO 1** y ejecuta:

```
Creados sin problema: OldExporter y OldTypo
Error: NotImplementedError, pero solo al llamar a export
```

`OldExporter` "obliga" a sus hijas a escribir `export` lanzando un error si no lo hacen. Pero tiene dos agujeros: la base se puede crear aunque no sirva para nada, y `OldTypo`, que escribió `exprot` con una errata, también se crea. El fallo solo aparece cuando alguien llama a `export`, que puede ser mucho más tarde.

### 2. `ABC` y `@abstractmethod`

Descomenta el **PASO 2** y ejecuta:

```
Error: Can't instantiate abstract class Exporter without an implementation for abstract method 'export'
Error: Can't instantiate abstract class Typo without an implementation for abstract method 'export'
Abstractos de Exporter: ['export']
```

Dos cambios respecto al paso 1: `Exporter` hereda de `ABC` y `export` lleva `@abstractmethod`. Ahora ni la base ni la hija con la errata se pueden crear, y el error dice qué método falta. Llega **al crear el objeto**, no semanas después. El cuerpo de `export` es solo un *docstring*: nadie lo ejecuta. `__abstractmethods__` es la lista que Python consulta al crear un objeto: si no está vacía, no lo crea.

### 3. El método plantilla

Descomenta el **PASO 3** y ejecuta:

```
a.csv: 2 filas -> 'etiqueta;valor\nNorte;12,5\nSur;NA\n'
a.json: 2 filas -> '["Norte;12,5", "Sur;NA"]'
```

Una clase abstracta también tiene código **concreto**. `FileExporter.export` está escrito una sola vez: escribe el archivo en UTF-8 y devuelve el número de filas. Lo único que cambia entre CSV y JSON es el texto, y eso lo decide cada hija en `render`, el método abstracto. La base fija los pasos y las hijas rellenan el hueco: es el **método plantilla**. El `!r` del *f-string* (semana 9) muestra el texto con `repr`, para que veas los `\n`.

### 4. Una propiedad abstracta

Descomenta el **PASO 4** y ejecuta:

```
Extensión: .csv
Error: Can't instantiate abstract class NoSuffix without an implementation for abstract method 'suffix'
```

`@property` y `@abstractmethod` se combinan, con `@property` **encima**. Toda subclase de `Format` tiene que decir su extensión, y se lee sin paréntesis: `CsvFormat().suffix`. Prueba a invertir el orden de los dos decoradores en `Format`: la clase ni siquiera se crea (`AttributeError: attribute '__isabstractmethod__' of 'property' objects is not writable`). Vuelve a dejarlos como estaban.

### 5. Una base abstracta que es una *dataclass*

Descomenta el **PASO 5** y ejecuta:

```
TextSource(path=PosixPath('medidas'))
¿Iguales? True · False
Error: cannot assign to field 'path'
Texto: ['etiqueta;valor', 'Norte;12,5'] · CSV: ['Norte;12,5']
```

`Source` es a la vez una *dataclass* `frozen` y una clase abstracta. `TextSource` y `CsvSource` no llevan `@dataclass` ni `__init__` y aun así:

- se crean con `path`, porque heredan el `__init__` generado;
- tienen un `repr` con **su** nombre, no el de la base;
- se comparan por clase y campos: un `TextSource` y un `CsvSource` con la misma ruta **no** son iguales;
- son inmutables: `frozen` se hereda para los campos de la base.

Cada una solo escribe lo que la distingue, `lines()`. En tu proyecto, `FileSource`, `TextFile` y `CsvFile` son exactamente esto, con `read_lines` y `read_csv` en lugar de `read_text`. (En Windows, el `repr` diría `WindowsPath`: el `replace` de la línea lo iguala para que compares con esta salida.)

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| En el paso 2 los objetos se crean sin error | Falta `(ABC)` en la clase o `@abstractmethod` en el método |
| `NameError: name 'abstractmethod' is not defined` | Borraste algo del `from abc import ...` de arriba |
| `AttributeError: attribute '__isabstractmethod__' of 'property' objects is not writable` | `@abstractmethod` está encima de `@property`: invierte el orden |
| `TypeError: TextSource() takes no arguments` | Falta `@dataclass(frozen=True)` encima de `Source` |
| `TypeError: cannot inherit non-frozen dataclass from a frozen one` | Pusiste `@dataclass` en una subclase: las del paso 5 no llevan decorador |
| `FileNotFoundError` en el paso 5 | Llamaste a `lines()` fuera del `with`: la carpeta temporal ya se borró |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Composición](../ejercicio-02-composicion/README.md) | **Ejercicio 03 · Clases abstractas** | [Ejercicio 04 · `Protocol`](../ejercicio-04-protocol/README.md) |
