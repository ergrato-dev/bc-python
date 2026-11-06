# Glosario — Semana 09

| Término | Definición |
|---|---|
| **`__dict__`** | Diccionario donde un objeto guarda sus atributos; lo enseña `vars(objeto)`. Las clases con `slots` no lo tienen |
| **`__eq__`** | Método especial que llama `==`. Definirlo quita a la clase su `__hash__` |
| **`__hash__`** | Método especial que da el *hash* de un objeto; sin él, el objeto no puede ir en un `set` ni ser clave de un diccionario |
| **`__init__`** | Método especial que prepara cada objeto nuevo: recibe el objeto en `self` y le pone sus atributos |
| **`__post_init__`** | Método que el `__init__` generado por `@dataclass` llama al terminar: para validar y calcular campos |
| **`__repr__`** | Método especial con el texto de un objeto para quien programa: `repr()`, `!r`, listas, depurador |
| **`__str__`** | Método especial con el texto de un objeto para quien lee el resultado: `print()` y los f-strings |
| **Atributo** | Un nombre guardado en un objeto (`north.name`) o en su clase |
| **Atributo de clase** | Atributo escrito en la clase, fuera de los métodos; lo comparten todos sus objetos |
| **Atributo de instancia** | Atributo de un objeto concreto, normalmente creado en `__init__` con `self.nombre = valor` |
| **Campo** (*field*) | En una *dataclass*, cada atributo declarado con `nombre: tipo`; `@dataclass` lo usa para generar los métodos |
| **Clase** | Un tipo nuevo, definido con `class`, que junta datos y las funciones que trabajan con ellos |
| **`@classmethod`** | Método que recibe la clase en `cls` en lugar del objeto; se usa sobre todo para constructores alternativos |
| **`ClassVar`** | Marca de tipo que dice a `@dataclass` que un atributo es de clase y no un campo |
| **Constructor alternativo** | `@classmethod` que crea un objeto de otra forma: `Measurement.from_line(...)`, `dict.fromkeys(...)` |
| ***Dataclass*** | Clase decorada con `@dataclass`, que genera `__init__`, `__repr__` y `__eq__` a partir de sus campos |
| **`default_factory`** | Argumento de `field()` con una función que crea el valor por defecto de cada objeto: `field(default_factory=list)` |
| **`FrozenInstanceError`** | Excepción al asignar un campo de una *dataclass* `frozen` |
| **`frozen`** | Opción de `@dataclass` que hace los objetos inmutables y les da `__hash__` |
| **Inmutable** | Que no cambia después de crearse: tuplas, textos, *dataclasses* `frozen` |
| **Instancia** | Un objeto de una clase: `north` es una instancia de `Sensor` |
| **`kw_only`** | Opción de `@dataclass` que obliga a pasar todos los campos por nombre |
| **Método** | Función escrita dentro de una clase; recibe el objeto en `self` |
| **Método especial** (*dunder method*) | Método con dos guiones bajos a cada lado que llama Python, no tú: `__init__`, `__repr__`, `__eq__`... |
| **Modelo** | Las clases que representan los datos con los que trabaja un programa por dentro: `Scale`, `Measurement`, `Series` |
| **`NamedTuple`** | Tupla con nombres para cada posición; sigue siendo una tupla y es igual a una tupla con los mismos datos |
| **`NotImplemented`** | Valor que devuelve `__eq__` cuando no sabe compararse con el otro objeto, para que Python pruebe al revés |
| **Objeto** | Cualquier valor de Python; en esta semana, lo que se crea al llamar a una clase |
| **`order`** | Opción de `@dataclass` que genera `<`, `<=`, `>` y `>=`, comparando los campos en orden |
| **`@property`** | Decorador que convierte un método en algo que se lee como un atributo; con un *setter*, puede validar lo que se asigna |
| **`replace`** | Función de `dataclasses` (o `copy.replace`) que crea una copia de un objeto con algunos campos cambiados |
| **`self`** | Primer parámetro de cada método: el objeto con el que se llamó |
| ***Setter*** | La parte de una propiedad que se ejecuta al asignarle un valor: `@celsius.setter` |
| **`slots`** | Opción de `@dataclass` que quita el `__dict__`: menos memoria y ningún atributo fuera de los campos |
| **`@staticmethod`** | Método que no recibe ni objeto ni clase: una función que vive en la clase |
| **`TypedDict`** | Descripción para mypy de un diccionario con claves y tipos fijos; en ejecución es un diccionario normal |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
