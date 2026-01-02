"""
Ejercicio 1: Mi Primera Clase
=============================

Objetivo: Aprender a crear clases básicas en Python.

Instrucciones:
1. Lee cada sección
2. Descomenta el código
3. Ejecuta para verificar que funciona
4. Experimenta modificando valores
"""

# ============================================
# PASO 1: Clase Simple
# ============================================
print("--- Paso 1: Clase Simple ---")

# Una clase es una plantilla para crear objetos.
# __init__ es el constructor que inicializa los atributos.
# self hace referencia al objeto que se está creando.

# Descomenta las siguientes líneas:
# class Person:
#     """Representa una persona."""
#
#     def __init__(self, name: str, age: int) -> None:
#         """
#         Inicializa una nueva persona.
#
#         Args:
#             name: Nombre de la persona
#             age: Edad en años
#         """
#         self.name = name
#         self.age = age
#
#
# # Crear instancias (objetos)
# person1 = Person("Ana", 25)
# person2 = Person("Bob", 30)
#
# # Acceder a atributos
# print(f"Nombre: {person1.name}, Edad: {person1.age}")
# print(f"Nombre: {person2.name}, Edad: {person2.age}")


# ============================================
# PASO 2: Agregar Métodos
# ============================================
print("\n--- Paso 2: Agregar Métodos ---")

# Los métodos son funciones que pertenecen a una clase.
# Siempre reciben self como primer parámetro.

# Descomenta las siguientes líneas:
# class Person:
#     """Representa una persona con comportamientos."""
#
#     def __init__(self, name: str, age: int) -> None:
#         self.name = name
#         self.age = age
#
#     def greet(self) -> str:
#         """Retorna un saludo personalizado."""
#         return f"Hola, soy {self.name} y tengo {self.age} años"
#
#     def is_adult(self) -> bool:
#         """Verifica si la persona es mayor de edad."""
#         return self.age >= 18
#
#     def have_birthday(self) -> None:
#         """Incrementa la edad en 1."""
#         self.age += 1
#         print(f"¡Feliz cumpleaños {self.name}! Ahora tienes {self.age} años")
#
#
# # Usar los métodos
# ana = Person("Ana", 17)
# print(ana.greet())
# print(f"¿Es adulta? {ana.is_adult()}")
#
# ana.have_birthday()
# print(f"¿Es adulta ahora? {ana.is_adult()}")


# ============================================
# PASO 3: Valores por Defecto
# ============================================
print("\n--- Paso 3: Valores por Defecto ---")

# Puedes definir valores por defecto en __init__
# Los parámetros con default van al final

# Descomenta las siguientes líneas:
# class Product:
#     """Representa un producto en inventario."""
#
#     def __init__(
#         self,
#         name: str,
#         price: float,
#         quantity: int = 0,
#         category: str = "general"
#     ) -> None:
#         self.name = name
#         self.price = price
#         self.quantity = quantity
#         self.category = category
#
#     def total_value(self) -> float:
#         """Calcula el valor total del inventario de este producto."""
#         return self.price * self.quantity
#
#     def info(self) -> str:
#         """Retorna información del producto."""
#         return f"{self.name} ({self.category}): ${self.price:.2f} x {self.quantity}"
#
#
# # Crear productos con diferentes combinaciones de parámetros
# laptop = Product("Laptop", 999.99, 5, "electrónica")
# mouse = Product("Mouse", 29.99, quantity=20)
# cable = Product("Cable USB", 9.99)
#
# print(laptop.info())
# print(mouse.info())
# print(cable.info())
#
# print(f"\nValor total laptops: ${laptop.total_value():,.2f}")


# ============================================
# PASO 4: Clase BankAccount
# ============================================
print("\n--- Paso 4: Clase BankAccount ---")

# Crea una clase más completa con validaciones

# Descomenta las siguientes líneas:
# class BankAccount:
#     """Representa una cuenta bancaria."""
#
#     def __init__(self, owner: str, initial_balance: float = 0) -> None:
#         """
#         Crea una nueva cuenta bancaria.
#
#         Args:
#             owner: Nombre del titular
#             initial_balance: Balance inicial (default: 0)
#         """
#         self.owner = owner
#         self.balance = initial_balance
#
#     def deposit(self, amount: float) -> bool:
#         """
#         Deposita dinero en la cuenta.
#
#         Args:
#             amount: Cantidad a depositar
#
#         Returns:
#             True si el depósito fue exitoso
#         """
#         if amount <= 0:
#             print("Error: El monto debe ser positivo")
#             return False
#
#         self.balance += amount
#         print(f"Depósito exitoso: +${amount:.2f}")
#         return True
#
#     def withdraw(self, amount: float) -> bool:
#         """
#         Retira dinero de la cuenta.
#
#         Args:
#             amount: Cantidad a retirar
#
#         Returns:
#             True si el retiro fue exitoso
#         """
#         if amount <= 0:
#             print("Error: El monto debe ser positivo")
#             return False
#
#         if amount > self.balance:
#             print("Error: Fondos insuficientes")
#             return False
#
#         self.balance -= amount
#         print(f"Retiro exitoso: -${amount:.2f}")
#         return True
#
#     def get_balance(self) -> float:
#         """Retorna el balance actual."""
#         return self.balance
#
#     def transfer_to(self, other: "BankAccount", amount: float) -> bool:
#         """
#         Transfiere dinero a otra cuenta.
#
#         Args:
#             other: Cuenta destino
#             amount: Cantidad a transferir
#
#         Returns:
#             True si la transferencia fue exitosa
#         """
#         if self.withdraw(amount):
#             other.deposit(amount)
#             print(f"Transferencia de {self.owner} a {other.owner}: ${amount:.2f}")
#             return True
#         return False
#
#
# # Crear cuentas
# cuenta_ana = BankAccount("Ana", 1000)
# cuenta_bob = BankAccount("Bob", 500)
#
# # Operaciones
# print(f"Balance inicial Ana: ${cuenta_ana.get_balance():.2f}")
# cuenta_ana.deposit(200)
# cuenta_ana.withdraw(50)
# print(f"Balance Ana: ${cuenta_ana.get_balance():.2f}")
#
# # Transferencia
# print()
# cuenta_ana.transfer_to(cuenta_bob, 300)
# print(f"Balance final Ana: ${cuenta_ana.get_balance():.2f}")
# print(f"Balance final Bob: ${cuenta_bob.get_balance():.2f}")


# ============================================
# PASO 5: Múltiples Instancias
# ============================================
print("\n--- Paso 5: Múltiples Instancias ---")

# Trabaja con listas de objetos

# Descomenta las siguientes líneas:
# class Task:
#     """Representa una tarea por hacer."""
#
#     def __init__(self, title: str, priority: int = 1) -> None:
#         self.title = title
#         self.priority = priority
#         self.completed = False
#
#     def complete(self) -> None:
#         """Marca la tarea como completada."""
#         self.completed = True
#
#     def info(self) -> str:
#         """Retorna información de la tarea."""
#         status = "✅" if self.completed else "⏳"
#         stars = "⭐" * self.priority
#         return f"{status} [{stars}] {self.title}"
#
#
# # Crear lista de tareas
# tasks = [
#     Task("Aprender POO", 5),
#     Task("Hacer ejercicios", 4),
#     Task("Revisar teoría", 3),
#     Task("Tomar café", 1),
# ]
#
# # Mostrar todas las tareas
# print("=== Lista de Tareas ===")
# for task in tasks:
#     print(task.info())
#
# # Completar algunas tareas
# tasks[0].complete()
# tasks[3].complete()
#
# print("\n=== Después de completar ===")
# for task in tasks:
#     print(task.info())
#
# # Filtrar tareas pendientes de alta prioridad
# print("\n=== Pendientes de Alta Prioridad (≥3) ===")
# pending_high = [t for t in tasks if not t.completed and t.priority >= 3]
# for task in pending_high:
#     print(task.info())


# ============================================
# DESAFÍO EXTRA
# ============================================
print("\n--- Desafío Extra ---")

# Crea una clase Rectangle con:
# - Atributos: width, height
# - Métodos: area(), perimeter(), is_square()
# - Método: scale(factor) que modifica las dimensiones

# Descomenta y completa:
# class Rectangle:
#     """Representa un rectángulo."""
#
#     def __init__(self, width: float, height: float) -> None:
#         self.width = width
#         self.height = height
#
#     def area(self) -> float:
#         """Calcula el área."""
#         pass  # Implementa
#
#     def perimeter(self) -> float:
#         """Calcula el perímetro."""
#         pass  # Implementa
#
#     def is_square(self) -> bool:
#         """Verifica si es un cuadrado."""
#         pass  # Implementa
#
#     def scale(self, factor: float) -> None:
#         """Escala el rectángulo por un factor."""
#         pass  # Implementa
#
#
# # Test
# rect = Rectangle(10, 5)
# print(f"Área: {rect.area()}")           # 50
# print(f"Perímetro: {rect.perimeter()}")  # 30
# print(f"¿Es cuadrado? {rect.is_square()}")  # False
#
# rect.scale(2)
# print(f"Área después de escalar x2: {rect.area()}")  # 200


print("\n✅ Ejercicio completado!")
