# 📖 Glosario - Semana 09: Herencia y Polimorfismo

## A

### Abstract Base Class (ABC)
Clase que no puede instanciarse directamente y define métodos abstractos que las subclases deben implementar.
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass
```

### Ancestor (Ancestro)
Cualquier clase en la cadena de herencia por encima de una clase dada. Si `C` hereda de `B` y `B` hereda de `A`, entonces `A` y `B` son ancestros de `C`.

---

## B

### Base Class (Clase Base)
La clase de la cual otras clases heredan atributos y métodos. También llamada "clase padre" o "superclase".
```python
class Animal:  # Base class
    pass

class Dog(Animal):  # Dog hereda de Animal
    pass
```

---

## C

### C3 Linearization
Algoritmo que Python usa para determinar el Method Resolution Order (MRO) en herencia múltiple. Garantiza un orden consistente y predecible.

### Child Class (Clase Hija)
Clase que hereda de otra clase. También llamada "subclase" o "clase derivada".
```python
class Vehicle:  # Parent
    pass

class Car(Vehicle):  # Child
    pass
```

### Composition (Composición)
Patrón de diseño alternativo a la herencia donde una clase contiene instancias de otras clases en lugar de heredar de ellas.
```python
class Engine:
    def start(self): pass

class Car:
    def __init__(self):
        self.engine = Engine()  # Composición
```

---

## D

### Derived Class
Ver **Child Class**.

### Diamond Problem (Problema del Diamante)
Situación en herencia múltiple donde una clase hereda de dos clases que comparten un ancestro común. Python lo resuelve con MRO.
```
     A
    / \
   B   C
    \ /
     D   # D hereda de B y C, ambos heredan de A
```

### Duck Typing
Filosofía de tipado donde el tipo de un objeto se determina por sus métodos y atributos, no por su herencia.
> "Si camina como pato y hace cuac como pato, es un pato."
```python
# No importa el tipo, solo que tenga speak()
def make_sound(animal):
    animal.speak()
```

---

## E

### Encapsulation (Encapsulamiento)
Principio de POO que oculta los detalles internos de una clase. Relacionado con herencia para controlar acceso a atributos.

### Extend (Extender)
Agregar funcionalidad a un método heredado sin reemplazarlo completamente, usando `super()`.
```python
def save(self):
    super().save()  # Llama al padre
    self.log("Saved")  # Añade funcionalidad
```

---

## H

### Hierarchy (Jerarquía)
Estructura de clases organizadas por relaciones de herencia.

---

## I

### Inheritance (Herencia)
Mecanismo por el cual una clase puede heredar atributos y métodos de otra clase.
```python
class Parent:
    def greet(self):
        return "Hello"

class Child(Parent):  # Hereda greet()
    pass
```

### Interface
Contrato que define métodos que una clase debe implementar. En Python se logra con ABCs o Protocols.

### `isinstance()`
Función que verifica si un objeto es instancia de una clase o sus ancestros.
```python
isinstance(dog, Animal)  # True si dog es Animal o subclase
```

### `issubclass()`
Función que verifica si una clase es subclase de otra.
```python
issubclass(Dog, Animal)  # True
```

### "is-a" Relationship
Relación de herencia: "Un perro ES UN animal".
```python
class Dog(Animal):  # Dog is-a Animal
    pass
```

---

## M

### Method Resolution Order (MRO)
Orden en que Python busca métodos en la jerarquía de clases. Se calcula con C3 Linearization.
```python
print(ClassName.__mro__)  # Ver el MRO
print(ClassName.mro())    # Alternativa
```

### Mixin
Clase diseñada para añadir funcionalidad específica a otras clases mediante herencia múltiple.
```python
class LoggingMixin:
    def log(self, msg):
        print(f"[LOG] {msg}")

class Service(LoggingMixin, BaseService):
    pass
```

### Multiple Inheritance (Herencia Múltiple)
Capacidad de una clase de heredar de múltiples clases padre.
```python
class Child(Parent1, Parent2):
    pass
```

---

## O

### Override (Sobrescribir)
Redefinir un método heredado en la clase hija.
```python
class Animal:
    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):  # Override
        return "Woof!"
```

---

## P

### Parent Class (Clase Padre)
Ver **Base Class**.

### Polymorphism (Polimorfismo)
Capacidad de objetos de diferentes clases de responder al mismo método de formas distintas.
```python
for shape in [Circle(), Rectangle()]:
    print(shape.area())  # Cada uno calcula diferente
```

### Protocol
Forma de definir interfaces sin herencia (Python 3.8+). Permite duck typing con type hints.
```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...
```

---

## S

### Single Inheritance (Herencia Simple)
Herencia de una sola clase padre.
```python
class Child(Parent):  # Solo un padre
    pass
```

### Subclass (Subclase)
Ver **Child Class**.

### `super()`
Función que retorna un objeto proxy que permite acceder a métodos de la clase padre.
```python
class Child(Parent):
    def __init__(self):
        super().__init__()  # Llama a Parent.__init__()
```

### Superclass (Superclase)
Ver **Base Class**.

---

## T

### Type Hint
Anotación que indica el tipo esperado. Útil con herencia y polimorfismo.
```python
def process(item: BaseClass) -> None:
    pass  # Acepta BaseClass y subclases
```

---

## V

### Virtual Method
En otros lenguajes, método que puede ser sobrescrito. En Python, todos los métodos son virtuales por defecto.

---

## Símbolos y Sintaxis

| Sintaxis | Significado |
|----------|-------------|
| `class Child(Parent)` | Child hereda de Parent |
| `class C(A, B)` | Herencia múltiple |
| `super()` | Acceso al padre en MRO |
| `__mro__` | Atributo con MRO |
| `isinstance(obj, cls)` | Verificar instancia |
| `issubclass(cls1, cls2)` | Verificar subclase |

---

## 📚 Referencias

- [Documentación oficial de Python - Clases](https://docs.python.org/3/tutorial/classes.html)
- [Real Python - Inheritance](https://realpython.com/inheritance-composition-python/)
- [PEP 3119 - Abstract Base Classes](https://peps.python.org/pep-3119/)
