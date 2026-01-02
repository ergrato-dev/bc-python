"""
Ejercicio 3: Métodos Especiales (Dunder Methods)
================================================

Objetivo: Implementar métodos especiales para comportamiento nativo.

Instrucciones:
1. Lee cada sección
2. Descomenta el código
3. Ejecuta para verificar que funciona
4. Experimenta con variaciones
"""

# ============================================
# PASO 1: Representación (__str__ y __repr__)
# ============================================
print("--- Paso 1: Representación ---")

# __str__: Para usuarios (print, str())
# __repr__: Para developers (debug, REPL, en listas)

# Descomenta las siguientes líneas:
# class Product:
#     """Representa un producto."""
#
#     def __init__(self, name: str, price: float, sku: str) -> None:
#         self.name = name
#         self.price = price
#         self.sku = sku
#
#     def __str__(self) -> str:
#         """Representación legible para usuarios."""
#         return f"{self.name} - ${self.price:.2f}"
#
#     def __repr__(self) -> str:
#         """Representación técnica para developers."""
#         return f"Product(name='{self.name}', price={self.price}, sku='{self.sku}')"
#
#
# # Crear producto
# laptop = Product("MacBook Pro", 1999.99, "MBP-2024")
#
# # __str__ se usa con print() y str()
# print(laptop)        # MacBook Pro - $1999.99
# print(str(laptop))   # MacBook Pro - $1999.99
#
# # __repr__ se usa con repr() y en listas
# print(repr(laptop))  # Product(name='MacBook Pro', price=1999.99, sku='MBP-2024')
#
# # En una lista, Python usa __repr__
# products = [
#     Product("Mouse", 49.99, "MS-001"),
#     Product("Keyboard", 129.99, "KB-002"),
# ]
# print(f"\nLista de productos:\n{products}")


# ============================================
# PASO 2: Comparación (__eq__, __lt__)
# ============================================
print("\n--- Paso 2: Comparación ---")

# Sin __eq__, Python compara por identidad (misma posición en memoria)
# Con __eq__, podemos definir qué significa que dos objetos sean "iguales"

# Descomenta las siguientes líneas:
# from functools import total_ordering
#
#
# @total_ordering  # Genera __le__, __gt__, __ge__ automáticamente
# class Version:
#     """Representa una versión de software."""
#
#     def __init__(self, major: int, minor: int, patch: int) -> None:
#         self.major = major
#         self.minor = minor
#         self.patch = patch
#
#     def __str__(self) -> str:
#         return f"v{self.major}.{self.minor}.{self.patch}"
#
#     def __repr__(self) -> str:
#         return f"Version({self.major}, {self.minor}, {self.patch})"
#
#     def __eq__(self, other: object) -> bool:
#         """Compara si dos versiones son iguales."""
#         if not isinstance(other, Version):
#             return NotImplemented
#         return (self.major, self.minor, self.patch) == \
#                (other.major, other.minor, other.patch)
#
#     def __lt__(self, other: "Version") -> bool:
#         """Compara si esta versión es menor que otra."""
#         if not isinstance(other, Version):
#             return NotImplemented
#         return (self.major, self.minor, self.patch) < \
#                (other.major, other.minor, other.patch)
#
#     def __hash__(self) -> int:
#         """Permite usar Version en sets y como key de dict."""
#         return hash((self.major, self.minor, self.patch))
#
#
# # Crear versiones
# v1 = Version(1, 0, 0)
# v2 = Version(1, 0, 0)
# v3 = Version(2, 0, 0)
# v4 = Version(1, 5, 0)
#
# # Comparación de igualdad
# print(f"{v1} == {v2}: {v1 == v2}")  # True
# print(f"{v1} == {v3}: {v1 == v3}")  # False
#
# # Comparación de orden
# print(f"\n{v1} < {v3}: {v1 < v3}")   # True
# print(f"{v3} > {v4}: {v3 > v4}")     # True
# print(f"{v1} <= {v2}: {v1 <= v2}")   # True
#
# # Ordenar lista de versiones
# versions = [v3, v1, v4, v2]
# print(f"\nVersiones ordenadas: {sorted(versions)}")
#
# # Usar en set (requiere __hash__)
# unique_versions = {v1, v2, v3, v4}  # v1 y v2 son iguales
# print(f"Versiones únicas: {unique_versions}")


# ============================================
# PASO 3: Longitud y Booleano (__len__, __bool__)
# ============================================
print("\n--- Paso 3: Longitud y Booleano ---")

# __len__: Define qué retorna len(objeto)
# __bool__: Define si el objeto es True o False en contextos booleanos

# Descomenta las siguientes líneas:
# class Playlist:
#     """Representa una playlist de música."""
#
#     def __init__(self, name: str) -> None:
#         self.name = name
#         self.songs: list[str] = []
#
#     def add(self, song: str) -> None:
#         """Agrega una canción."""
#         self.songs.append(song)
#
#     def remove(self, song: str) -> bool:
#         """Elimina una canción si existe."""
#         if song in self.songs:
#             self.songs.remove(song)
#             return True
#         return False
#
#     def __len__(self) -> int:
#         """Retorna el número de canciones."""
#         return len(self.songs)
#
#     def __bool__(self) -> bool:
#         """La playlist es True si tiene canciones."""
#         return len(self.songs) > 0
#
#     def __str__(self) -> str:
#         return f"Playlist '{self.name}' ({len(self)} canciones)"
#
#
# # Crear playlist
# rock = Playlist("Rock Classics")
#
# # Playlist vacía es False
# print(f"Playlist vacía: {rock}")
# print(f"bool(rock): {bool(rock)}")
# print(f"len(rock): {len(rock)}")
#
# if not rock:
#     print("La playlist está vacía")
#
# # Agregar canciones
# rock.add("Bohemian Rhapsody")
# rock.add("Stairway to Heaven")
# rock.add("Hotel California")
#
# print(f"\nPlaylist con canciones: {rock}")
# print(f"bool(rock): {bool(rock)}")
# print(f"len(rock): {len(rock)}")
#
# if rock:
#     print("La playlist tiene canciones")


# ============================================
# PASO 4: Acceso a Elementos (__getitem__, __iter__)
# ============================================
print("\n--- Paso 4: Acceso a Elementos ---")

# __getitem__: Permite obj[index] y obj[start:end]
# __iter__: Permite for item in obj

# Descomenta las siguientes líneas:
# class TodoList:
#     """Lista de tareas con acceso por índice."""
#
#     def __init__(self, name: str) -> None:
#         self.name = name
#         self._tasks: list[dict] = []
#
#     def add(self, task: str, priority: int = 1) -> None:
#         """Agrega una tarea."""
#         self._tasks.append({
#             "task": task,
#             "priority": priority,
#             "done": False
#         })
#
#     def __len__(self) -> int:
#         return len(self._tasks)
#
#     def __bool__(self) -> bool:
#         return len(self._tasks) > 0
#
#     def __getitem__(self, index: int) -> dict:
#         """Permite acceso por índice: todo[0], todo[-1], todo[1:3]"""
#         return self._tasks[index]
#
#     def __iter__(self):
#         """Permite iterar: for task in todo"""
#         return iter(self._tasks)
#
#     def __contains__(self, task_name: str) -> bool:
#         """Permite: 'task' in todo"""
#         return any(t["task"] == task_name for t in self._tasks)
#
#     def __str__(self) -> str:
#         return f"TodoList '{self.name}' ({len(self)} tareas)"
#
#
# # Crear lista de tareas
# todo = TodoList("Semana 08")
# todo.add("Estudiar POO", priority=5)
# todo.add("Hacer ejercicios", priority=4)
# todo.add("Revisar teoría", priority=3)
# todo.add("Descansar", priority=1)
#
# print(todo)
#
# # Acceso por índice
# print(f"\nPrimera tarea: {todo[0]}")
# print(f"Última tarea: {todo[-1]}")
#
# # Slicing
# print(f"\nTareas 1-2: {todo[1:3]}")
#
# # Iteración
# print("\nTodas las tareas:")
# for task in todo:
#     stars = "⭐" * task["priority"]
#     print(f"  [{stars}] {task['task']}")
#
# # Pertenencia
# print(f"\n'Estudiar POO' en lista: {'Estudiar POO' in todo}")
# print(f"'Otra tarea' en lista: {'Otra tarea' in todo}")


# ============================================
# PASO 5: Clase Completa - Money
# ============================================
print("\n--- Paso 5: Clase Completa ---")

# Combinamos todos los métodos especiales

# Descomenta las siguientes líneas:
# from functools import total_ordering
#
#
# @total_ordering
# class Money:
#     """Representa una cantidad de dinero."""
#
#     def __init__(self, amount: float, currency: str = "USD") -> None:
#         self.amount = round(amount, 2)
#         self.currency = currency
#
#     # Representación
#     def __str__(self) -> str:
#         return f"${self.amount:,.2f} {self.currency}"
#
#     def __repr__(self) -> str:
#         return f"Money({self.amount}, '{self.currency}')"
#
#     # Comparación
#     def __eq__(self, other: object) -> bool:
#         if not isinstance(other, Money):
#             return NotImplemented
#         return self.amount == other.amount and self.currency == other.currency
#
#     def __lt__(self, other: "Money") -> bool:
#         if not isinstance(other, Money):
#             return NotImplemented
#         if self.currency != other.currency:
#             raise ValueError(f"Cannot compare {self.currency} with {other.currency}")
#         return self.amount < other.amount
#
#     def __hash__(self) -> int:
#         return hash((self.amount, self.currency))
#
#     # Operaciones aritméticas
#     def __add__(self, other: "Money") -> "Money":
#         if not isinstance(other, Money):
#             return NotImplemented
#         if self.currency != other.currency:
#             raise ValueError(f"Cannot add {self.currency} with {other.currency}")
#         return Money(self.amount + other.amount, self.currency)
#
#     def __sub__(self, other: "Money") -> "Money":
#         if not isinstance(other, Money):
#             return NotImplemented
#         if self.currency != other.currency:
#             raise ValueError(f"Cannot subtract {self.currency} from {other.currency}")
#         return Money(self.amount - other.amount, self.currency)
#
#     def __mul__(self, factor: float) -> "Money":
#         if not isinstance(factor, (int, float)):
#             return NotImplemented
#         return Money(self.amount * factor, self.currency)
#
#     def __rmul__(self, factor: float) -> "Money":
#         return self.__mul__(factor)
#
#     # Booleano
#     def __bool__(self) -> bool:
#         return self.amount != 0
#
#     # Negación
#     def __neg__(self) -> "Money":
#         return Money(-self.amount, self.currency)
#
#
# # Crear dinero
# price = Money(99.99)
# tax = Money(8.00)
# discount = Money(15.00)
#
# print(f"Precio: {price}")
# print(f"Impuesto: {tax}")
# print(f"Descuento: {discount}")
#
# # Operaciones
# subtotal = price + tax
# print(f"\nSubtotal: {subtotal}")
#
# total = subtotal - discount
# print(f"Total con descuento: {total}")
#
# # Multiplicación
# tip = total * 0.15
# print(f"Propina (15%): {tip}")
#
# # También funciona al revés
# double = 2 * price
# print(f"Doble del precio: {double}")
#
# # Comparación
# print(f"\n{price} > {tax}: {price > tax}")
#
# # Ordenar
# amounts = [Money(50), Money(100), Money(25), Money(75)]
# print(f"\nOrdenado: {sorted(amounts)}")
#
# # Booleano
# zero = Money(0)
# print(f"\nbool(Money(0)): {bool(zero)}")
# print(f"bool(Money(100)): {bool(price)}")


# ============================================
# DESAFÍO EXTRA
# ============================================
print("\n--- Desafío Extra ---")

# Crea una clase Vector2D que represente un vector en 2D con:
# - __init__(x, y)
# - __str__ y __repr__
# - __eq__ para comparar vectores
# - __add__ para sumar vectores
# - __sub__ para restar vectores
# - __mul__ para multiplicar por escalar
# - __abs__ para obtener la magnitud
# - __neg__ para negar el vector
# - __bool__ (False si es vector cero)

# Tu código aquí:
# class Vector2D:
#     pass
#
# # Tests
# v1 = Vector2D(3, 4)
# v2 = Vector2D(1, 2)
#
# print(f"v1 = {v1}")           # (3, 4)
# print(f"v2 = {v2}")           # (1, 2)
# print(f"v1 + v2 = {v1 + v2}") # (4, 6)
# print(f"v1 - v2 = {v1 - v2}") # (2, 2)
# print(f"v1 * 2 = {v1 * 2}")   # (6, 8)
# print(f"|v1| = {abs(v1)}")    # 5.0
# print(f"-v1 = {-v1}")         # (-3, -4)


print("\n✅ Ejercicio completado!")
