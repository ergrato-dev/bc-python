# 🎭 Ejercicio 03: Polimorfismo

## 🎯 Objetivo

Practicar polimorfismo con herencia y Duck Typing, creando código flexible que trabaje con diferentes tipos de objetos de forma uniforme.

---

## 📋 Instrucciones

En este ejercicio crearás un sistema de formas geométricas que demuestra polimorfismo.

### Paso 1: Clase Base Shape

Define la clase padre con los métodos que serán implementados polimórficamente.

```python
class Shape:
    def area(self) -> float:
        raise NotImplementedError("Subclasses must implement area()")

    def perimeter(self) -> float:
        raise NotImplementedError("Subclasses must implement perimeter()")

    def describe(self) -> str:
        return f"{type(self).__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"
```

**Abre `starter/main.py`** y descomenta la sección del Paso 1.

---

### Paso 2: Circle

Implementa la primera forma geométrica.

```python
import math

class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self.radius
```

**Descomenta** la sección del Paso 2.

---

### Paso 3: Rectangle

Implementa la segunda forma geométrica.

```python
class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)
```

**Descomenta** la sección del Paso 3.

---

### Paso 4: Triangle

Implementa la tercera forma geométrica.

```python
class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float) -> None:
        self.a = a  # Lados del triángulo
        self.b = b
        self.c = c

    def area(self) -> float:
        # Fórmula de Herón
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self) -> float:
        return self.a + self.b + self.c
```

**Descomenta** la sección del Paso 4.

---

### Paso 5: Funciones Polimórficas

Crea funciones que trabajen con cualquier `Shape`.

```python
def print_shape_info(shape: Shape) -> None:
    """Imprime información de cualquier forma."""
    print(shape.describe())


def total_area(shapes: list[Shape]) -> float:
    """Calcula el área total de una lista de formas."""
    return sum(shape.area() for shape in shapes)


def largest_shape(shapes: list[Shape]) -> Shape:
    """Encuentra la forma con mayor área."""
    return max(shapes, key=lambda s: s.area())
```

**Descomenta** la sección del Paso 5.

---

### Paso 6: Usar Polimorfismo

Aplica las funciones polimórficas a diferentes formas.

```python
shapes = [
    Circle(5),
    Rectangle(4, 6),
    Triangle(3, 4, 5)
]

# Cada forma usa SU implementación
for shape in shapes:
    print_shape_info(shape)

print(f"\nTotal area: {total_area(shapes):.2f}")
print(f"Largest: {largest_shape(shapes).describe()}")
```

**Descomenta** la sección del Paso 6.

---

### Paso 7: Duck Typing

Demuestra que Python no requiere herencia para polimorfismo.

```python
# Clase SIN herencia de Shape
class Square:
    """Square no hereda de Shape pero tiene los mismos métodos."""

    def __init__(self, side: float) -> None:
        self.side = side

    def area(self) -> float:
        return self.side ** 2

    def perimeter(self) -> float:
        return 4 * self.side

    def describe(self) -> str:
        return f"Square: area={self.area():.2f}, perimeter={self.perimeter():.2f}"


# ¡Funciona con las mismas funciones!
square = Square(5)
print_shape_info(square)  # Duck typing en acción
```

**Descomenta** la sección del Paso 7.

---

### Paso 8: Protocol para Type Safety

Usa Protocol para combinar Duck Typing con type hints.

```python
from typing import Protocol

class ShapeLike(Protocol):
    """Protocolo que define qué es una 'forma'."""

    def area(self) -> float: ...
    def perimeter(self) -> float: ...
    def describe(self) -> str: ...


def print_shape_info_typed(shape: ShapeLike) -> None:
    """Versión con type hint de Protocol."""
    print(shape.describe())


# Funciona con Shape y Square (aunque Square no hereda de Shape)
print_shape_info_typed(Circle(3))
print_shape_info_typed(Square(4))
```

**Descomenta** la sección del Paso 8.

---

## ✅ Resultado Esperado

```
=== Paso 6: Polimorfismo ===
Circle: area=78.54, perimeter=31.42
Rectangle: area=24.00, perimeter=20.00
Triangle: area=6.00, perimeter=12.00

Total area: 108.54
Largest: Circle: area=78.54, perimeter=31.42

=== Paso 7: Duck Typing ===
Square: area=25.00, perimeter=20.00

=== Paso 8: Protocol ===
Circle: area=28.27, perimeter=18.85
Square: area=16.00, perimeter=16.00
```

---

## 🔑 Conceptos Clave

| Concepto | Descripción |
|----------|-------------|
| **Polimorfismo** | Mismo método, diferente comportamiento según la clase |
| **Duck Typing** | "Si hace cuac como pato, es un pato" - no requiere herencia |
| **Protocol** | Define interfaces sin herencia (Python 3.8+) |
| **Función polimórfica** | Trabaja con el tipo base pero acepta cualquier subclase |

---

## 🧠 Reflexión

1. ¿Por qué `print_shape_info()` funciona con `Square` aunque no hereda de `Shape`?
2. ¿Cuándo usarías herencia vs Duck Typing?
3. ¿Qué ventajas ofrece Protocol sobre Duck Typing puro?

---

## 🔗 Siguiente

Continúa con el [Proyecto de la Semana](../../3-proyecto/) para aplicar herencia y polimorfismo en un sistema completo.
