# 🧬 Ejercicio 01: Herencia Simple

## 🎯 Objetivo

Practicar la creación de clases que heredan de una clase padre, entendiendo la relación "is-a" y el uso de `isinstance()` e `issubclass()`.

---

## 📋 Instrucciones

En este ejercicio crearás una jerarquía de vehículos donde diferentes tipos heredan de una clase base `Vehicle`.

### Paso 1: Clase Base Vehicle

Primero, define la clase padre con atributos comunes a todos los vehículos.

```python
class Vehicle:
    def __init__(self, brand: str, model: str, year: int) -> None:
        self.brand = brand
        self.model = model
        self.year = year

    def info(self) -> str:
        return f"{self.year} {self.brand} {self.model}"
```

**Abre `starter/main.py`** y descomenta la sección del Paso 1.

---

### Paso 2: Clase Car (Hereda de Vehicle)

Crea una clase `Car` que herede de `Vehicle` y añada atributos propios.

```python
class Car(Vehicle):
    def __init__(
        self,
        brand: str,
        model: str,
        year: int,
        num_doors: int
    ) -> None:
        super().__init__(brand, model, year)
        self.num_doors = num_doors

    def info(self) -> str:
        base = super().info()
        return f"{base} - {self.num_doors} doors"
```

**Descomenta** la sección del Paso 2 en `starter/main.py`.

---

### Paso 3: Clase Motorcycle (Hereda de Vehicle)

Crea otra subclase con sus propios atributos específicos.

```python
class Motorcycle(Vehicle):
    def __init__(
        self,
        brand: str,
        model: str,
        year: int,
        engine_cc: int
    ) -> None:
        super().__init__(brand, model, year)
        self.engine_cc = engine_cc

    def info(self) -> str:
        base = super().info()
        return f"{base} - {self.engine_cc}cc"
```

**Descomenta** la sección del Paso 3.

---

### Paso 4: Clase Truck (Hereda de Vehicle)

Una tercera subclase con capacidad de carga.

```python
class Truck(Vehicle):
    def __init__(
        self,
        brand: str,
        model: str,
        year: int,
        payload_kg: float
    ) -> None:
        super().__init__(brand, model, year)
        self.payload_kg = payload_kg

    def info(self) -> str:
        base = super().info()
        return f"{base} - {self.payload_kg}kg capacity"
```

**Descomenta** la sección del Paso 4.

---

### Paso 5: Crear Instancias

Crea objetos de cada tipo de vehículo.

```python
# Crear vehículos
car = Car("Toyota", "Corolla", 2023, 4)
moto = Motorcycle("Honda", "CBR600", 2022, 600)
truck = Truck("Ford", "F-150", 2024, 1000)

# Mostrar información
print(car.info())    # 2023 Toyota Corolla - 4 doors
print(moto.info())   # 2022 Honda CBR600 - 600cc
print(truck.info())  # 2024 Ford F-150 - 1000kg capacity
```

**Descomenta** la sección del Paso 5.

---

### Paso 6: Verificar Herencia con isinstance()

Usa `isinstance()` para verificar si un objeto es instancia de una clase.

```python
# isinstance verifica si un objeto es de un tipo específico
print(f"car is Vehicle: {isinstance(car, Vehicle)}")      # True
print(f"car is Car: {isinstance(car, Car)}")              # True
print(f"car is Motorcycle: {isinstance(car, Motorcycle)}")# False

# Todos son Vehicle
vehicles = [car, moto, truck]
for v in vehicles:
    print(f"{type(v).__name__} is Vehicle: {isinstance(v, Vehicle)}")
```

**Descomenta** la sección del Paso 6.

---

### Paso 7: Verificar Jerarquía con issubclass()

Usa `issubclass()` para verificar relaciones entre clases.

```python
# issubclass verifica la jerarquía de clases
print(f"Car is subclass of Vehicle: {issubclass(Car, Vehicle)}")          # True
print(f"Vehicle is subclass of Car: {issubclass(Vehicle, Car)}")          # False
print(f"Car is subclass of object: {issubclass(Car, object)}")            # True
print(f"Motorcycle is subclass of Car: {issubclass(Motorcycle, Car)}")    # False
```

**Descomenta** la sección del Paso 7.

---

### Paso 8: Función Polimórfica

Crea una función que trabaje con cualquier `Vehicle`.

```python
def print_vehicle_info(vehicle: Vehicle) -> None:
    """Imprime información de cualquier vehículo."""
    vehicle_type = type(vehicle).__name__
    print(f"[{vehicle_type}] {vehicle.info()}")


# Funciona con cualquier subclase de Vehicle
print_vehicle_info(car)
print_vehicle_info(moto)
print_vehicle_info(truck)
```

**Descomenta** la sección del Paso 8.

---

## ✅ Resultado Esperado

```
=== Paso 5: Crear Instancias ===
2023 Toyota Corolla - 4 doors
2022 Honda CBR600 - 600cc
2024 Ford F-150 - 1000kg capacity

=== Paso 6: isinstance() ===
car is Vehicle: True
car is Car: True
car is Motorcycle: False
Car is Vehicle: True
Motorcycle is Vehicle: True
Truck is Vehicle: True

=== Paso 7: issubclass() ===
Car is subclass of Vehicle: True
Vehicle is subclass of Car: False
Car is subclass of object: True
Motorcycle is subclass of Car: False

=== Paso 8: Función Polimórfica ===
[Car] 2023 Toyota Corolla - 4 doors
[Motorcycle] 2022 Honda CBR600 - 600cc
[Truck] 2024 Ford F-150 - 1000kg capacity
```

---

## 🔑 Conceptos Clave

| Concepto | Descripción |
|----------|-------------|
| `class Child(Parent)` | Sintaxis de herencia |
| `super().__init__()` | Llama al constructor del padre |
| `isinstance(obj, Class)` | Verifica si objeto es instancia de clase |
| `issubclass(Child, Parent)` | Verifica si clase hereda de otra |
| Relación "is-a" | Car IS-A Vehicle |

---

## 🔗 Siguiente

Continúa con [02-override-y-super](../02-override-y-super/) para practicar sobrescritura de métodos.
