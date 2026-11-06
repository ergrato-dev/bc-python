# 03 · Clases abstractas

⏱️ 50 min

## 🎯 Objetivos

- Explicar para qué sirve una clase que no se puede crear.
- Declarar una clase abstracta con `ABC` y `@abstractmethod`.
- Comparar `@abstractmethod` con el viejo `raise NotImplementedError`.
- Escribir métodos concretos en la base que usan los abstractos (método plantilla).
- Reconocer las clases abstractas de `collections.abc`.

---

## 1. Una base que no debería existir sola

Quieres varias clases de exportación: una escribe CSV, otra JSON. Todas comparten la ruta y la forma de usarse, y cada una escribe el archivo a su manera. Una clase base recoge lo común:

```python
from pathlib import Path


class Exporter:
    def __init__(self, path: Path) -> None:
        self.path = path

    def export(self, rows: list[str]) -> None:
        raise NotImplementedError


class CsvExporter(Exporter):
    def export(self, rows: list[str]) -> None:
        self.path.write_text("\n".join(rows), encoding="utf-8")
```

Funciona, pero tiene dos agujeros:

- `Exporter(Path("x"))` se puede crear, aunque no sirve para nada. El error llega más tarde, al llamar a `export()`.
- Si una subclase olvida `export` (o lo escribe mal: `exprot`), Python no dice nada hasta que alguien lo llama. Puede ser en producción, semanas después.

## 2. `ABC` y `@abstractmethod`

El módulo `abc` (*abstract base classes*) cierra los dos agujeros:

```python
from abc import ABC, abstractmethod


class Exporter(ABC):
    def __init__(self, path: Path) -> None:
        self.path = path

    @abstractmethod
    def export(self, rows: list[str]) -> None:
        """Escribe las filas en self.path."""
```

Dos cambios: la clase hereda de `ABC`, y el método lleva `@abstractmethod`. El cuerpo puede ser solo el *docstring*: nadie lo va a ejecutar. Ahora:

```python
Exporter(Path("x"))
```

```
TypeError: Can't instantiate abstract class Exporter without an implementation for abstract method 'export'
```

Y una subclase que no escribe `export` también es abstracta:

```python
class BrokenExporter(Exporter):
    def exprot(self, rows: list[str]) -> None:   # mal escrito
        ...


BrokenExporter(Path("x"))
# TypeError: Can't instantiate abstract class BrokenExporter without an implementation for abstract method 'export'
```

El error llega **al crear el objeto**, no al usarlo, y dice exactamente qué método falta. mypy lo ve antes aún, sin ejecutar: `Cannot instantiate abstract class "BrokenExporter" with abstract attribute "export"`.

Una clase con al menos un método abstracto es una **clase abstracta**. Las subclases que los implementan todos son **concretas**, y esas sí se pueden crear.

## 3. Lo que la base sí hace: el método plantilla

Una clase abstracta no es solo una lista de métodos obligatorios. También puede tener métodos **concretos**, escritos una sola vez, que usan los abstractos:

```python
class Exporter(ABC):
    def __init__(self, path: Path) -> None:
        self.path = path

    @abstractmethod
    def render(self, rows: list[str]) -> str:
        """El texto del archivo."""

    def export(self, rows: list[str]) -> int:
        """Escribe el archivo y devuelve el número de filas."""
        self.path.write_text(self.render(rows), encoding="utf-8")
        return len(rows)


class CsvExporter(Exporter):
    def render(self, rows: list[str]) -> str:
        return "etiqueta;valor\n" + "\n".join(rows) + "\n"


class JsonExporter(Exporter):
    def render(self, rows: list[str]) -> str:
        return json.dumps(rows, ensure_ascii=False, indent=2)
```

`export` es igual para todos: escribir, con UTF-8, y contar. Solo cambia **qué** se escribe, y eso lo decide cada subclase en `render`. A esto se le llama **método plantilla** (*template method*): la base fija los pasos y deja huecos que rellenan las hijas. Si mañana hay que comprobar que la carpeta existe antes de escribir, se cambia en un solo sitio.

## 4. Propiedades abstractas

`@abstractmethod` se combina con `@property` (semana 9). El orden importa: `@property` va encima.

```python
class Exporter(ABC):
    @property
    @abstractmethod
    def suffix(self) -> str:
        """La extensión del archivo, con el punto."""


class CsvExporter(Exporter):
    @property
    def suffix(self) -> str:
        return ".csv"
```

Así la base obliga a que toda subclase diga su extensión, y quien la use escribe `exporter.suffix`, sin paréntesis.

## 5. Clases abstractas y *dataclasses*

Se combinan bien: la base guarda los campos comunes y las hijas heredan el `__init__` generado.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Exporter(ABC):
    path: Path

    @abstractmethod
    def render(self, rows: list[str]) -> str: ...


class CsvExporter(Exporter):
    def render(self, rows: list[str]) -> str:
        return "\n".join(rows)


CsvExporter(Path("salida.csv"))    # CsvExporter(path=PosixPath('salida.csv'))
```

`CsvExporter` no lleva `@dataclass` y aun así tiene `__init__`, `__repr__`, `__eq__` y la inmutabilidad de `frozen`: los hereda. Y `__repr__` usa el nombre de la clase real, `CsvExporter`. Es exactamente la forma de `FileSource`, `TextFile` y `CsvFile` en tu proyecto. (En Windows verás `WindowsPath` en lugar de `PosixPath`.)

## 6. Las clases abstractas que ya usas

`collections.abc` tiene las clases abstractas de los contenedores de Python. Las has visto en tipos desde la semana 8:

```python
from collections.abc import Iterable, Mapping, Sequence

isinstance([1, 2], Sequence)       # True
isinstance((1, 2), Sequence)       # True
isinstance({1, 2}, Sequence)       # False: un set no tiene orden ni índices
isinstance({"a": 1}, Mapping)      # True
isinstance("texto", Iterable)      # True
```

`Sequence` es una ABC con dos métodos abstractos (`__getitem__` y `__len__`) y varios concretos que se apoyan en ellos (`index`, `count`, `__contains__`, `__iter__`): el método plantilla otra vez. Cuando escribes `def records_of(lines: Iterable[str])`, dices "cualquier cosa que se pueda recorrer", no "una lista".

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| `TypeError: Can't instantiate abstract class Exporter without an implementation for abstract method 'export'` | Creas la base, o una subclase a la que le falta ese método | Crea una subclase concreta, o escribe el método con el nombre exacto |
| La base se puede crear aunque tenga `@abstractmethod` | La clase no hereda de `ABC` | `class Exporter(ABC):` |
| `AttributeError: attribute '__isabstractmethod__' of 'property' objects is not writable` | `@abstractmethod` encima de `@property` | `@property` arriba, `@abstractmethod` debajo |
| `mypy`: `Missing return statement  [empty-body]` | Un método con solo *docstring* sin `@abstractmethod` | Añade `@abstractmethod`, o escribe el cuerpo |
| `mypy`: `Cannot instantiate abstract class` en un test | El test crea la base a propósito | `# type: ignore[abstract]` en esa línea |

---

## ✅ Qué debes saber al terminar

- [ ] Qué dos problemas tiene `raise NotImplementedError` en la base.
- [ ] Cómo se declara una clase abstracta y cuándo falla crearla.
- [ ] Qué es el método plantilla y qué gana con él.
- [ ] En qué orden van `@property` y `@abstractmethod`.
- [ ] Qué hereda una subclase de una base que es una *dataclass*.
- [ ] Qué es `collections.abc.Sequence` y por qué `Iterable[str]` en un tipo.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [02 · Composición](02-composicion.md) | **03 · Clases abstractas** | [04 · `Protocol`](04-protocol.md) |
