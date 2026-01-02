"""
Ejercicio 2: Atributos y Métodos Avanzados
==========================================

Objetivo: Dominar atributos de clase/instancia y tipos de métodos.

Instrucciones:
1. Lee cada sección
2. Descomenta el código
3. Ejecuta para verificar que funciona
4. Experimenta con variaciones
"""

# ============================================
# PASO 1: Atributos de Clase vs Instancia
# ============================================
print("--- Paso 1: Atributos de Clase vs Instancia ---")

# Atributos de CLASE: Compartidos entre TODAS las instancias
# Atributos de INSTANCIA: Únicos para CADA objeto

# Descomenta las siguientes líneas:
# class Employee:
#     """Representa un empleado de la empresa."""
#
#     # Atributos de clase (compartidos)
#     company_name: str = "TechCorp"
#     employee_count: int = 0
#     all_employees: list["Employee"] = []
#
#     def __init__(self, name: str, department: str, salary: float) -> None:
#         # Atributos de instancia (únicos por objeto)
#         self.name = name
#         self.department = department
#         self.salary = salary
#
#         # Actualizar atributos de clase
#         Employee.employee_count += 1
#         Employee.all_employees.append(self)
#
#     def info(self) -> str:
#         return f"{self.name} - {self.department} @ {Employee.company_name}"
#
#
# # Crear empleados
# emp1 = Employee("Ana", "Engineering", 75000)
# emp2 = Employee("Bob", "Marketing", 65000)
# emp3 = Employee("Carlos", "Engineering", 80000)
#
# # Acceso a atributos de clase
# print(f"Empresa: {Employee.company_name}")
# print(f"Total empleados: {Employee.employee_count}")
#
# # También accesible desde instancia
# print(f"Empresa (desde emp1): {emp1.company_name}")
#
# # Cada instancia tiene sus propios atributos de instancia
# print(f"\nEmpleado 1: {emp1.info()}")
# print(f"Empleado 2: {emp2.info()}")
#
# # Cambiar atributo de clase afecta a todos
# Employee.company_name = "TechCorp Inc."
# print(f"\nDespués de cambiar nombre de empresa:")
# print(f"Empleado 1: {emp1.info()}")
# print(f"Empleado 2: {emp2.info()}")


# ============================================
# PASO 2: Métodos de Clase (@classmethod)
# ============================================
print("\n--- Paso 2: Métodos de Clase ---")

# @classmethod recibe cls (la clase) como primer parámetro
# Útil para factory methods y modificar estado de clase

# Descomenta las siguientes líneas:
# class User:
#     """Representa un usuario del sistema."""
#
#     total_users: int = 0
#
#     def __init__(self, username: str, email: str, role: str = "user") -> None:
#         self.username = username
#         self.email = email
#         self.role = role
#         User.total_users += 1
#
#     # Factory method: crear desde string
#     @classmethod
#     def from_string(cls, user_string: str) -> "User":
#         """
#         Crea un User desde un string con formato 'username:email:role'.
#
#         Args:
#             user_string: String con datos del usuario
#
#         Returns:
#             Nueva instancia de User
#         """
#         parts = user_string.split(":")
#         username = parts[0]
#         email = parts[1]
#         role = parts[2] if len(parts) > 2 else "user"
#         return cls(username, email, role)
#
#     # Factory method: crear desde diccionario
#     @classmethod
#     def from_dict(cls, data: dict) -> "User":
#         """Crea un User desde un diccionario."""
#         return cls(
#             username=data["username"],
#             email=data["email"],
#             role=data.get("role", "user")
#         )
#
#     # Método de clase para acceder a estado de clase
#     @classmethod
#     def get_total_users(cls) -> int:
#         """Retorna el número total de usuarios."""
#         return cls.total_users
#
#     # Factory method: crear admin
#     @classmethod
#     def create_admin(cls, username: str, email: str) -> "User":
#         """Crea un usuario administrador."""
#         return cls(username, email, role="admin")
#
#     def __repr__(self) -> str:
#         return f"User({self.username}, {self.email}, {self.role})"
#
#
# # Diferentes formas de crear usuarios
# user1 = User("alice", "alice@email.com")
# user2 = User.from_string("bob:bob@email.com:moderator")
# user3 = User.from_dict({"username": "carlos", "email": "carlos@email.com"})
# admin = User.create_admin("admin", "admin@email.com")
#
# print(f"User 1: {user1}")
# print(f"User 2: {user2}")
# print(f"User 3: {user3}")
# print(f"Admin: {admin}")
# print(f"\nTotal usuarios: {User.get_total_users()}")


# ============================================
# PASO 3: Métodos Estáticos (@staticmethod)
# ============================================
print("\n--- Paso 3: Métodos Estáticos ---")

# @staticmethod no recibe self ni cls
# Son utilidades relacionadas con la clase pero independientes

# Descomenta las siguientes líneas:
# class Validator:
#     """Clase con métodos de validación."""
#
#     @staticmethod
#     def is_valid_email(email: str) -> bool:
#         """Valida formato básico de email."""
#         return "@" in email and "." in email.split("@")[-1]
#
#     @staticmethod
#     def is_valid_password(password: str) -> bool:
#         """
#         Valida que la contraseña tenga:
#         - Mínimo 8 caracteres
#         - Al menos una mayúscula
#         - Al menos un número
#         """
#         if len(password) < 8:
#             return False
#         has_upper = any(c.isupper() for c in password)
#         has_digit = any(c.isdigit() for c in password)
#         return has_upper and has_digit
#
#     @staticmethod
#     def is_valid_username(username: str) -> bool:
#         """Valida username (3-20 chars, alfanumérico + guión bajo)."""
#         if not 3 <= len(username) <= 20:
#             return False
#         return all(c.isalnum() or c == "_" for c in username)
#
#     @staticmethod
#     def sanitize_string(text: str) -> str:
#         """Limpia y normaliza un string."""
#         return text.strip().lower()
#
#
# # Usar sin crear instancia
# print(f"Email 'test@email.com': {Validator.is_valid_email('test@email.com')}")
# print(f"Email 'invalid': {Validator.is_valid_email('invalid')}")
# print()
# print(f"Password 'Abc12345': {Validator.is_valid_password('Abc12345')}")
# print(f"Password 'weak': {Validator.is_valid_password('weak')}")
# print()
# print(f"Username 'user_123': {Validator.is_valid_username('user_123')}")
# print(f"Username 'ab': {Validator.is_valid_username('ab')}")


# ============================================
# PASO 4: Combinando Todo
# ============================================
print("\n--- Paso 4: Combinando Todo ---")

# Clase completa con los tres tipos de métodos

# Descomenta las siguientes líneas:
# from datetime import date
#
#
# class Book:
#     """Representa un libro en la biblioteca."""
#
#     # Atributos de clase
#     library_name: str = "Biblioteca Central"
#     total_books: int = 0
#     all_books: list["Book"] = []
#
#     def __init__(self, title: str, author: str, year: int, isbn: str) -> None:
#         # Atributos de instancia
#         self.title = title
#         self.author = author
#         self.year = year
#         self.isbn = isbn
#         self.is_available = True
#
#         # Actualizar estado de clase
#         Book.total_books += 1
#         Book.all_books.append(self)
#
#     # Método de instancia
#     def borrow(self) -> bool:
#         """Presta el libro si está disponible."""
#         if self.is_available:
#             self.is_available = False
#             return True
#         return False
#
#     # Método de instancia
#     def return_book(self) -> None:
#         """Devuelve el libro."""
#         self.is_available = True
#
#     # Método de instancia
#     def get_age(self) -> int:
#         """Retorna la antigüedad del libro."""
#         return date.today().year - self.year
#
#     # Factory method
#     @classmethod
#     def from_dict(cls, data: dict) -> "Book":
#         """Crea un libro desde diccionario."""
#         return cls(
#             title=data["title"],
#             author=data["author"],
#             year=data["year"],
#             isbn=data["isbn"]
#         )
#
#     # Método de clase
#     @classmethod
#     def get_available_books(cls) -> list["Book"]:
#         """Retorna lista de libros disponibles."""
#         return [book for book in cls.all_books if book.is_available]
#
#     @classmethod
#     def get_statistics(cls) -> dict:
#         """Retorna estadísticas de la biblioteca."""
#         available = len(cls.get_available_books())
#         return {
#             "total": cls.total_books,
#             "available": available,
#             "borrowed": cls.total_books - available
#         }
#
#     # Método estático
#     @staticmethod
#     def is_valid_isbn(isbn: str) -> bool:
#         """Valida formato ISBN (simplificado)."""
#         # ISBN-10: 10 dígitos, ISBN-13: 13 dígitos
#         clean = isbn.replace("-", "").replace(" ", "")
#         return len(clean) in (10, 13) and clean.isdigit()
#
#     @staticmethod
#     def format_isbn(isbn: str) -> str:
#         """Formatea ISBN con guiones."""
#         clean = isbn.replace("-", "").replace(" ", "")
#         if len(clean) == 13:
#             return f"{clean[:3]}-{clean[3:4]}-{clean[4:9]}-{clean[9:12]}-{clean[12]}"
#         return isbn
#
#     def __repr__(self) -> str:
#         status = "📗" if self.is_available else "📕"
#         return f"{status} {self.title} by {self.author} ({self.year})"
#
#
# # Crear libros
# book1 = Book("1984", "George Orwell", 1949, "9780451524935")
# book2 = Book("El Quijote", "Cervantes", 1605, "9788420412146")
# book3 = Book.from_dict({
#     "title": "Python Crash Course",
#     "author": "Eric Matthes",
#     "year": 2019,
#     "isbn": "9781593279288"
# })
#
# # Mostrar libros
# print(f"Biblioteca: {Book.library_name}")
# print(f"Total libros: {Book.total_books}")
# print()
#
# for book in Book.all_books:
#     print(f"  {book}")
#
# # Prestar un libro
# print("\nPrestando '1984'...")
# book1.borrow()
#
# # Estadísticas
# stats = Book.get_statistics()
# print(f"\nEstadísticas: {stats}")
#
# # Validar ISBN
# print(f"\nISBN válido '9780451524935': {Book.is_valid_isbn('9780451524935')}")
# print(f"ISBN formateado: {Book.format_isbn('9780451524935')}")


# ============================================
# PASO 5: Properties
# ============================================
print("\n--- Paso 5: Properties ---")

# @property permite controlar acceso a atributos
# con getters y setters que parecen atributos normales

# Descomenta las siguientes líneas:
# class Circle:
#     """Representa un círculo."""
#
#     PI: float = 3.14159
#
#     def __init__(self, radius: float) -> None:
#         self._radius = radius  # Atributo "privado"
#
#     @property
#     def radius(self) -> float:
#         """Getter para el radio."""
#         return self._radius
#
#     @radius.setter
#     def radius(self, value: float) -> None:
#         """Setter con validación."""
#         if value <= 0:
#             raise ValueError("Radius must be positive")
#         self._radius = value
#
#     @property
#     def diameter(self) -> float:
#         """Propiedad calculada: diámetro."""
#         return self._radius * 2
#
#     @diameter.setter
#     def diameter(self, value: float) -> None:
#         """Setter para diámetro (modifica radio)."""
#         self.radius = value / 2
#
#     @property
#     def area(self) -> float:
#         """Propiedad calculada: área."""
#         return Circle.PI * self._radius ** 2
#
#     @property
#     def circumference(self) -> float:
#         """Propiedad calculada: circunferencia."""
#         return 2 * Circle.PI * self._radius
#
#
# # Uso como atributos normales
# circle = Circle(5)
# print(f"Radio: {circle.radius}")
# print(f"Diámetro: {circle.diameter}")
# print(f"Área: {circle.area:.2f}")
# print(f"Circunferencia: {circle.circumference:.2f}")
#
# # Modificar radio
# circle.radius = 10
# print(f"\nNuevo radio: {circle.radius}")
# print(f"Nueva área: {circle.area:.2f}")
#
# # Modificar vía diámetro
# circle.diameter = 30
# print(f"\nDiámetro = 30 → Radio = {circle.radius}")
#
# # La validación funciona
# try:
#     circle.radius = -5
# except ValueError as e:
#     print(f"\nError esperado: {e}")


# ============================================
# DESAFÍO EXTRA
# ============================================
print("\n--- Desafío Extra ---")

# Crea una clase Temperature que:
# - Almacene temperatura en Celsius internamente
# - Tenga properties para acceder/modificar en Celsius y Fahrenheit
# - Tenga un @classmethod para crear desde Fahrenheit
# - Tenga un @staticmethod para convertir C a F y F a C
# - Valide que la temperatura no sea menor a -273.15°C

# Tu código aquí:
# class Temperature:
#     pass


print("\n✅ Ejercicio completado!")
