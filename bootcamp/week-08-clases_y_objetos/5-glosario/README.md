# 📖 Glosario - Semana 08: Clases y Objetos

Términos clave de Programación Orientada a Objetos en Python.

---

## A

### Abstracción
Proceso de ocultar los detalles de implementación y mostrar solo la funcionalidad esencial. Permite trabajar con conceptos de alto nivel sin preocuparse por los detalles internos.

### Atributo
Variable que pertenece a una clase o instancia. Almacena datos asociados al objeto.

```python
class Dog:
    species = "Canis familiaris"  # Atributo de clase

    def __init__(self, name: str) -> None:
        self.name = name  # Atributo de instancia
```

### Atributo de Clase (Class Attribute)
Variable definida directamente en el cuerpo de la clase, compartida por todas las instancias.

### Atributo de Instancia (Instance Attribute)
Variable definida en `__init__` con `self.`, única para cada instancia.

---

## C

### Clase (Class)
Plantilla o molde que define la estructura y comportamiento de los objetos. Define atributos y métodos.

```python
class Car:
    """Plantilla para crear coches."""

    def __init__(self, brand: str) -> None:
        self.brand = brand
```

### @classmethod
Decorador que define un método que recibe la clase (`cls`) como primer argumento en lugar de la instancia. Útil para factory methods.

```python
@classmethod
def from_string(cls, data: str) -> "MyClass":
    return cls(data.split(","))
```

### Constructor
Método especial que inicializa una nueva instancia. En Python, `__init__` es el inicializador (el verdadero constructor es `__new__`).

---

## D

### Decorador (Decorator)
Función que modifica el comportamiento de otra función o método. En POO: `@classmethod`, `@staticmethod`, `@property`.

### Dunder Method
Ver **Método Especial**.

---

## E

### Encapsulamiento (Encapsulation)
Principio de POO que agrupa datos y métodos relacionados, controlando el acceso a los detalles internos. En Python se usa convención de nombres (`_` y `__`).

### Estado (State)
Conjunto de valores de los atributos de un objeto en un momento dado.

---

## F

### Factory Method
Patrón de diseño donde un método de clase crea y retorna instancias. Comúnmente implementado con `@classmethod`.

```python
@classmethod
def from_dict(cls, data: dict) -> "User":
    return cls(name=data["name"], email=data["email"])
```

---

## H

### Herencia (Inheritance)
Mecanismo donde una clase (hija) hereda atributos y métodos de otra clase (padre). Se profundiza en la Semana 09.

---

## I

### Inicializador
Método `__init__` que configura el estado inicial de una instancia después de su creación.

### Instancia (Instance)
Objeto concreto creado a partir de una clase. Cada instancia tiene su propio estado.

```python
dog1 = Dog("Rex")   # dog1 es una instancia de Dog
dog2 = Dog("Luna")  # dog2 es otra instancia de Dog
```

### Instanciación
Proceso de crear una instancia a partir de una clase.

---

## M

### Método (Method)
Función definida dentro de una clase que opera sobre instancias u objetos.

### Método de Clase (Class Method)
Método decorado con `@classmethod` que recibe la clase como primer argumento (`cls`).

### Método de Instancia (Instance Method)
Método regular que recibe `self` como primer argumento. Opera sobre una instancia específica.

### Método Especial (Special Method / Magic Method / Dunder Method)
Métodos con doble guión bajo al inicio y final (`__nombre__`). Permiten definir comportamientos especiales.

| Método | Propósito |
|--------|-----------|
| `__init__` | Inicialización |
| `__str__` | Representación legible |
| `__repr__` | Representación técnica |
| `__eq__` | Comparación de igualdad |
| `__len__` | Longitud del objeto |
| `__getitem__` | Acceso por índice |

### Método Estático (Static Method)
Método decorado con `@staticmethod` que no recibe `self` ni `cls`. Es una función regular dentro de la clase.

---

## O

### Objeto (Object)
Entidad que combina estado (atributos) y comportamiento (métodos). En Python, todo es un objeto.

### Operador de Punto (Dot Operator)
Operador `.` usado para acceder a atributos y métodos de un objeto: `objeto.atributo`, `objeto.metodo()`.

---

## P

### Paradigma
Estilo o enfoque de programación. POO es un paradigma que organiza código en objetos.

### Polimorfismo
Capacidad de objetos de diferentes clases de responder al mismo método de formas distintas. Se profundiza en la Semana 09.

### Propiedad (Property)
Mecanismo que permite acceder a métodos como si fueran atributos, usando el decorador `@property`.

```python
@property
def full_name(self) -> str:
    return f"{self.first_name} {self.last_name}"
```

---

## S

### self
Referencia a la instancia actual dentro de un método. Primer parámetro de métodos de instancia.

```python
def greet(self) -> str:
    return f"Hola, soy {self.name}"
```

### Sobrecarga de Operadores (Operator Overloading)
Definir comportamiento personalizado para operadores (`+`, `-`, `==`, etc.) mediante métodos especiales.

### @staticmethod
Decorador que define un método que no recibe `self` ni `cls`. Útil para funciones utilitarias relacionadas con la clase.

---

## T

### Tipo (Type)
La clase de un objeto. `type(obj)` retorna la clase de un objeto.

### Type Hints
Anotaciones de tipos que indican el tipo esperado de variables, parámetros y retornos.

```python
def greet(self, name: str) -> str:
    return f"Hola, {name}"
```

---

## Referencias Cruzadas

| Término | Relacionado con |
|---------|-----------------|
| Clase | Objeto, Instancia |
| Método | Función, self |
| Atributo | Estado, Propiedad |
| @classmethod | Factory Method, cls |
| @staticmethod | Función utilitaria |
| Dunder | Método Especial |

---

## 🔗 Ver También

- **Semana 09**: Herencia y Composición
- **Semana 10**: Polimorfismo y Clases Abstractas
- [Python Data Model](https://docs.python.org/3/reference/datamodel.html)
