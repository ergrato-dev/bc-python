# Glosario — Semana 10

| Término | Definición |
|---|---|
| **`__abstractmethods__`** | Conjunto de métodos abstractos que le quedan por implementar a una clase; si no está vacío, la clase no se puede crear |
| **`__mro__`** | Tupla con las clases en las que Python busca un atributo, en orden: la propia clase, sus bases y, al final, `object` |
| **`@abstractmethod`** | Decorador de `abc` que marca un método como obligatorio para las subclases. Con `@property`, va debajo |
| **`@runtime_checkable`** | Decorador que permite `isinstance` con un `Protocol`. Solo comprueba que existan los nombres, no las firmas |
| **ABC** | *Abstract base class*: clase que hereda de `abc.ABC`, con métodos abstractos, que no se puede crear y sirve de base |
| **Clase abstracta** | Clase con al menos un método abstracto; no se puede crear, solo heredar de ella |
| **Clase base** | La clase de la que hereda otra; también "clase padre" o "superclase" |
| **Clase concreta** | Subclase que implementa todos los métodos abstractos de sus bases y, por tanto, se puede crear |
| **`collections.abc`** | Módulo con las clases abstractas de los contenedores: `Iterable`, `Sized`, `Sequence`, `Mapping`... |
| **Composición** | Construir un objeto a partir de otros que guarda en sus atributos y usa: "tiene un" |
| **Delegar** | Pasar el trabajo a un objeto interno: `add` valida y delega en `self._values.append` |
| ***Duck typing*** | Usar un objeto por los métodos que tiene, sin mirar su clase: "si grazna como un pato, es un pato" |
| **Herencia** | Crear una clase a partir de otra, que recibe sus atributos y métodos: "es un" |
| **Herencia múltiple** | Una clase con varias bases: `class D(B, C)`. La MRO decide el orden de búsqueda |
| **Jerarquía** | El árbol de clases que forman una base y sus subclases |
| **Método abstracto** | Método declarado en la base con `@abstractmethod`, sin implementación útil, que cada subclase concreta debe escribir |
| **Método plantilla** | Método concreto de la base que fija los pasos y llama a métodos abstractos que rellenan las subclases |
| ***Mixin*** | Clase pequeña, sin `__init__` ni campos, que solo aporta métodos para mezclar en otras: `JsonMixin` |
| **MRO** | *Method resolution order*: el orden en que Python busca un método en una jerarquía |
| **`NotImplementedError`** | Excepción que se lanzaba en la base para "obligar" a sustituir un método; con `@abstractmethod`, el aviso llega antes |
| ***Override*** | Sustituir en una subclase un método heredado, con el mismo nombre y una firma compatible |
| **Polimorfismo** | Llamar al mismo método en objetos de clases distintas y que cada uno responda con su versión |
| **`Protocol`** | Clase de `typing` que describe los métodos que debe tener un objeto; se cumple sin heredar de ella |
| **Subclase** | Clase que hereda de otra; también "clase hija" |
| **`super()`** | Da acceso al método de la siguiente clase en la MRO; con una sola base, el de la clase padre |
| **Tipado estructural** | Un tipo se cumple por tener los métodos adecuados (`Protocol`), sin importar la clase |
| **Tipado nominal** | Un tipo se cumple por heredar de la clase que lo define (ABC, herencia normal) |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
