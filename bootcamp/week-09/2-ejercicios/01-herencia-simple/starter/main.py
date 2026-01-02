"""
Ejercicio 01: Herencia Simple
=============================
Practica la creación de jerarquías de clases con herencia.

Instrucciones:
1. Lee cada sección comentada
2. Descomenta el código paso a paso
3. Ejecuta para ver los resultados
"""


# ============================================
# PASO 1: Clase Base Vehicle
# ============================================
print("=== Paso 1: Clase Base Vehicle ===")

# La clase Vehicle es la base de nuestra jerarquía
# Define atributos comunes: brand, model, year
# Descomenta las siguientes líneas:

# class Vehicle:
#     """Clase base para todos los vehículos."""
#
#     def __init__(self, brand: str, model: str, year: int) -> None:
#         self.brand = brand
#         self.model = model
#         self.year = year
#
#     def info(self) -> str:
#         """Retorna información básica del vehículo."""
#         return f"{self.year} {self.brand} {self.model}"
#
# # Probar la clase base
# vehicle = Vehicle("Generic", "Model", 2020)
# print(vehicle.info())

print()


# ============================================
# PASO 2: Clase Car (Hereda de Vehicle)
# ============================================
print("=== Paso 2: Clase Car ===")

# Car hereda de Vehicle y añade num_doors
# Usa super().__init__() para inicializar atributos del padre
# Descomenta las siguientes líneas:

# class Car(Vehicle):
#     """Auto - hereda de Vehicle, añade número de puertas."""
#
#     def __init__(
#         self,
#         brand: str,
#         model: str,
#         year: int,
#         num_doors: int
#     ) -> None:
#         # Llamar al constructor del padre
#         super().__init__(brand, model, year)
#         # Añadir atributo propio
#         self.num_doors = num_doors
#
#     def info(self) -> str:
#         """Extiende info() del padre con num_doors."""
#         base = super().info()
#         return f"{base} - {self.num_doors} doors"
#
# # Probar Car
# car = Car("Toyota", "Corolla", 2023, 4)
# print(car.info())

print()


# ============================================
# PASO 3: Clase Motorcycle (Hereda de Vehicle)
# ============================================
print("=== Paso 3: Clase Motorcycle ===")

# Motorcycle hereda de Vehicle y añade engine_cc
# Descomenta las siguientes líneas:

# class Motorcycle(Vehicle):
#     """Motocicleta - hereda de Vehicle, añade cilindrada."""
#
#     def __init__(
#         self,
#         brand: str,
#         model: str,
#         year: int,
#         engine_cc: int
#     ) -> None:
#         super().__init__(brand, model, year)
#         self.engine_cc = engine_cc
#
#     def info(self) -> str:
#         """Extiende info() con cilindrada del motor."""
#         base = super().info()
#         return f"{base} - {self.engine_cc}cc"
#
# # Probar Motorcycle
# moto = Motorcycle("Honda", "CBR600", 2022, 600)
# print(moto.info())

print()


# ============================================
# PASO 4: Clase Truck (Hereda de Vehicle)
# ============================================
print("=== Paso 4: Clase Truck ===")

# Truck hereda de Vehicle y añade payload_kg
# Descomenta las siguientes líneas:

# class Truck(Vehicle):
#     """Camión - hereda de Vehicle, añade capacidad de carga."""
#
#     def __init__(
#         self,
#         brand: str,
#         model: str,
#         year: int,
#         payload_kg: float
#     ) -> None:
#         super().__init__(brand, model, year)
#         self.payload_kg = payload_kg
#
#     def info(self) -> str:
#         """Extiende info() con capacidad de carga."""
#         base = super().info()
#         return f"{base} - {self.payload_kg}kg capacity"
#
# # Probar Truck
# truck = Truck("Ford", "F-150", 2024, 1000)
# print(truck.info())

print()


# ============================================
# PASO 5: Crear Instancias de Cada Tipo
# ============================================
print("=== Paso 5: Crear Instancias ===")

# Crea objetos de cada tipo de vehículo
# Nota: Necesitas haber descomentado los pasos 1-4
# Descomenta las siguientes líneas:

# # Crear vehículos de diferentes tipos
# car = Car("Toyota", "Corolla", 2023, 4)
# moto = Motorcycle("Honda", "CBR600", 2022, 600)
# truck = Truck("Ford", "F-150", 2024, 1000)
#
# # Mostrar información de cada uno
# print(car.info())
# print(moto.info())
# print(truck.info())

print()


# ============================================
# PASO 6: Verificar Herencia con isinstance()
# ============================================
print("=== Paso 6: isinstance() ===")

# isinstance() verifica si un objeto es instancia de una clase
# Retorna True también para clases padre
# Descomenta las siguientes líneas:

# # Verificar tipos específicos
# print(f"car is Vehicle: {isinstance(car, Vehicle)}")
# print(f"car is Car: {isinstance(car, Car)}")
# print(f"car is Motorcycle: {isinstance(car, Motorcycle)}")
#
# print()
#
# # Todos son Vehicle (polimorfismo)
# vehicles = [car, moto, truck]
# for v in vehicles:
#     class_name = type(v).__name__
#     print(f"{class_name} is Vehicle: {isinstance(v, Vehicle)}")

print()


# ============================================
# PASO 7: Verificar Jerarquía con issubclass()
# ============================================
print("=== Paso 7: issubclass() ===")

# issubclass() verifica relaciones entre CLASES (no objetos)
# Descomenta las siguientes líneas:

# # Verificar jerarquía de clases
# print(f"Car is subclass of Vehicle: {issubclass(Car, Vehicle)}")
# print(f"Vehicle is subclass of Car: {issubclass(Vehicle, Car)}")
# print(f"Car is subclass of object: {issubclass(Car, object)}")
# print(f"Motorcycle is subclass of Car: {issubclass(Motorcycle, Car)}")
#
# print()
#
# # Todas las clases heredan de object
# for cls in [Vehicle, Car, Motorcycle, Truck]:
#     print(f"{cls.__name__} -> object: {issubclass(cls, object)}")

print()


# ============================================
# PASO 8: Función Polimórfica
# ============================================
print("=== Paso 8: Función Polimórfica ===")

# Una función que acepta Vehicle funciona con CUALQUIER subclase
# Esto es polimorfismo en acción
# Descomenta las siguientes líneas:

# def print_vehicle_info(vehicle: Vehicle) -> None:
#     """Imprime información de cualquier vehículo."""
#     vehicle_type = type(vehicle).__name__
#     print(f"[{vehicle_type}] {vehicle.info()}")
#
#
# # Funciona con Car, Motorcycle y Truck
# print_vehicle_info(car)
# print_vehicle_info(moto)
# print_vehicle_info(truck)
#
# print()
#
# # También funciona con una lista mixta
# fleet = [
#     Car("BMW", "M3", 2024, 4),
#     Motorcycle("Yamaha", "R1", 2023, 998),
#     Truck("Volvo", "VNL", 2024, 20000),
#     Car("Tesla", "Model 3", 2024, 4)
# ]
#
# print("Fleet inventory:")
# for vehicle in fleet:
#     print_vehicle_info(vehicle)


print("\n✅ Ejercicio completado!")
