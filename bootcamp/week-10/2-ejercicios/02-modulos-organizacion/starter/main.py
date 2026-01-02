#!/usr/bin/env python3
"""
Ejercicio 2: Organización en Módulos
=====================================
Aprende a separar código en módulos y usar imports correctamente.

Instrucciones:
1. Primero ejecuta este archivo para ver el código monolítico funcionando
2. Luego sigue los pasos para extraer cada parte a su propio módulo
3. Al final, los imports deben funcionar desde el paquete ecommerce/
"""

from dataclasses import dataclass, field
from datetime import datetime
import re


# ============================================
# CÓDIGO MONOLÍTICO (Todo en un archivo)
# ============================================
# Este código funciona, pero está todo mezclado.
# Tu tarea es organizarlo en módulos separados.

print("=== Sistema E-Commerce Modularizado ===\n")


# --------------------------------------------
# UTILIDADES - Mover a: ecommerce/utils/validators.py
# --------------------------------------------

def validate_email(email: str) -> bool:
    """Valida formato de email."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_price(price: float) -> bool:
    """Valida que el precio sea positivo."""
    return price > 0


def validate_quantity(quantity: int) -> bool:
    """Valida que la cantidad sea positiva."""
    return quantity > 0


# --------------------------------------------
# MODELOS - Mover a: ecommerce/models/
# --------------------------------------------

# Mover a: ecommerce/models/user.py
@dataclass
class User:
    """Modelo de usuario."""
    id: int
    name: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not validate_email(self.email):
            raise ValueError(f"Invalid email: {self.email}")


# Mover a: ecommerce/models/product.py
@dataclass
class Product:
    """Modelo de producto."""
    id: int
    name: str
    price: float
    stock: int = 0

    def __post_init__(self):
        if not validate_price(self.price):
            raise ValueError(f"Invalid price: {self.price}")


# Mover a: ecommerce/models/cart.py
@dataclass
class CartItem:
    """Item en el carrito."""
    product: Product
    quantity: int

    @property
    def subtotal(self) -> float:
        return self.product.price * self.quantity


# --------------------------------------------
# SERVICIOS - Mover a: ecommerce/services/
# --------------------------------------------

# Mover a: ecommerce/services/user_service.py
class UserService:
    """Servicio para gestionar usuarios."""

    def __init__(self):
        self._users: dict[int, User] = {}
        self._next_id = 1

    def create_user(self, name: str, email: str) -> User:
        """Crea un nuevo usuario."""
        user = User(id=self._next_id, name=name, email=email)
        self._users[user.id] = user
        self._next_id += 1
        return user

    def get_user(self, user_id: int) -> User | None:
        """Obtiene un usuario por ID."""
        return self._users.get(user_id)

    def list_users(self) -> list[User]:
        """Lista todos los usuarios."""
        return list(self._users.values())


# Mover a: ecommerce/services/cart_service.py
class CartService:
    """Servicio para gestionar el carrito de compras."""

    def __init__(self, user: User):
        self.user = user
        self._items: list[CartItem] = []

    def add_item(self, product: Product, quantity: int = 1) -> None:
        """Añade un producto al carrito."""
        if not validate_quantity(quantity):
            raise ValueError("Quantity must be positive")

        # Buscar si el producto ya está en el carrito
        for item in self._items:
            if item.product.id == product.id:
                item.quantity += quantity
                return

        self._items.append(CartItem(product=product, quantity=quantity))

    def remove_item(self, product_id: int) -> None:
        """Elimina un producto del carrito."""
        self._items = [item for item in self._items if item.product.id != product_id]

    def get_items(self) -> list[CartItem]:
        """Obtiene todos los items del carrito."""
        return self._items.copy()

    @property
    def total(self) -> float:
        """Calcula el total del carrito."""
        return sum(item.subtotal for item in self._items)

    def clear(self) -> None:
        """Vacía el carrito."""
        self._items.clear()


# ============================================
# PASO 1: Verificar que el código funciona
# ============================================
print("--- Paso 1: Código monolítico funcionando ---")

# Probar validadores
email = "alice@example.com"
print(f"Validando email: {email} {'✓' if validate_email(email) else '✗'}")

# Crear usuario
user = User(id=1, name="Alice", email=email)
print(f"Usuario creado: {user}")

# Crear producto
product = Product(id=101, name="Laptop", price=999.99, stock=10)
print(f"Producto creado: {product}")


# ============================================
# PASO 2: Crear estructura de módulos
# ============================================
print("\n--- Paso 2: Estructura de módulos ---")
print("""
Crea la siguiente estructura de carpetas:

ecommerce/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   └── product.py
├── services/
│   ├── __init__.py
│   ├── user_service.py
│   └── cart_service.py
└── utils/
    ├── __init__.py
    └── validators.py

Comandos:
  mkdir -p ecommerce/models ecommerce/services ecommerce/utils
  touch ecommerce/__init__.py
  touch ecommerce/models/__init__.py ecommerce/models/user.py ecommerce/models/product.py
  touch ecommerce/services/__init__.py ecommerce/services/user_service.py ecommerce/services/cart_service.py
  touch ecommerce/utils/__init__.py ecommerce/utils/validators.py
""")


# ============================================
# PASO 3: Contenido de cada archivo
# ============================================
print("--- Paso 3: Contenido de cada archivo ---")
print("""
# ecommerce/utils/validators.py
# ==============================
import re

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_price(price: float) -> bool:
    return price > 0

def validate_quantity(quantity: int) -> bool:
    return quantity > 0


# ecommerce/utils/__init__.py
# ============================
from .validators import validate_email, validate_price, validate_quantity

__all__ = ["validate_email", "validate_price", "validate_quantity"]


# ecommerce/models/user.py
# =========================
from dataclasses import dataclass, field
from datetime import datetime
from ..utils import validate_email  # Import relativo

@dataclass
class User:
    id: int
    name: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not validate_email(self.email):
            raise ValueError(f"Invalid email: {self.email}")


# ecommerce/models/product.py
# ============================
from dataclasses import dataclass
from ..utils import validate_price

@dataclass
class Product:
    id: int
    name: str
    price: float
    stock: int = 0

    def __post_init__(self):
        if not validate_price(self.price):
            raise ValueError(f"Invalid price: {self.price}")

@dataclass
class CartItem:
    product: Product
    quantity: int

    @property
    def subtotal(self) -> float:
        return self.product.price * self.quantity


# ecommerce/models/__init__.py
# =============================
from .user import User
from .product import Product, CartItem

__all__ = ["User", "Product", "CartItem"]


# ecommerce/services/user_service.py
# ====================================
from ..models import User

class UserService:
    def __init__(self):
        self._users: dict[int, User] = {}
        self._next_id = 1

    def create_user(self, name: str, email: str) -> User:
        user = User(id=self._next_id, name=name, email=email)
        self._users[user.id] = user
        self._next_id += 1
        return user

    def get_user(self, user_id: int) -> User | None:
        return self._users.get(user_id)


# ecommerce/services/cart_service.py
# ====================================
from ..models import User, Product, CartItem
from ..utils import validate_quantity

class CartService:
    def __init__(self, user: User):
        self.user = user
        self._items: list[CartItem] = []

    def add_item(self, product: Product, quantity: int = 1) -> None:
        if not validate_quantity(quantity):
            raise ValueError("Quantity must be positive")
        for item in self._items:
            if item.product.id == product.id:
                item.quantity += quantity
                return
        self._items.append(CartItem(product=product, quantity=quantity))

    def get_items(self) -> list[CartItem]:
        return self._items.copy()

    @property
    def total(self) -> float:
        return sum(item.subtotal for item in self._items)


# ecommerce/services/__init__.py
# ===============================
from .user_service import UserService
from .cart_service import CartService

__all__ = ["UserService", "CartService"]


# ecommerce/__init__.py
# ======================
from .models import User, Product, CartItem
from .services import UserService, CartService
from .utils import validate_email, validate_price

__all__ = [
    "User", "Product", "CartItem",
    "UserService", "CartService",
    "validate_email", "validate_price",
]
""")


# ============================================
# PASO 4: Probar imports (después de modularizar)
# ============================================
print("\n--- Paso 4: Probar imports ---")
print("""
Una vez creados los módulos, reemplaza este main.py con:

# main.py (versión modularizada)
from ecommerce.models import User, Product
from ecommerce.services import UserService, CartService
from ecommerce.utils import validate_email

def main():
    # Crear servicio de usuarios
    user_service = UserService()
    alice = user_service.create_user("Alice", "alice@example.com")
    print(f"Usuario: {alice.name} ({alice.email})")

    # Crear productos
    laptop = Product(id=101, name="Laptop", price=999.99, stock=10)
    mouse = Product(id=102, name="Mouse", price=29.99, stock=50)

    # Crear carrito
    cart = CartService(user=alice)
    cart.add_item(laptop, quantity=1)
    cart.add_item(mouse, quantity=2)

    # Mostrar carrito
    print("Carrito:")
    for item in cart.get_items():
        print(f"  - {item.product.name} x{item.quantity} = ${item.subtotal:.2f}")
    print(f"Total: ${cart.total:.2f}")

if __name__ == "__main__":
    main()
""")


# ============================================
# DEMOSTRACIÓN CON CÓDIGO ACTUAL
# ============================================
print("\n--- Demostración con código actual ---")

# Simular el resultado final
user_service = UserService()
alice = user_service.create_user("Alice", "alice@example.com")
print(f"Usuario: {alice.name} ({alice.email})")

laptop = Product(id=101, name="Laptop", price=999.99, stock=10)
mouse = Product(id=102, name="Mouse", price=29.99, stock=50)

cart = CartService(user=alice)
cart.add_item(laptop, quantity=1)
cart.add_item(mouse, quantity=2)

print("Carrito:")
for item in cart.get_items():
    print(f"  - {item.product.name} x{item.quantity} = ${item.subtotal:.2f}")
print(f"Total: ${cart.total:.2f}")


# ============================================
# RESUMEN
# ============================================
print("\n" + "=" * 50)
print("✅ Ejercicio completado!")
print("=" * 50)
print("""
Conceptos aprendidos:
1. Separar código en módulos por responsabilidad
2. Usar imports relativos dentro de paquetes (.module)
3. Configurar __init__.py para exports limpios
4. __all__ define la API pública del módulo
5. Imports absolutos desde fuera del paquete
""")
