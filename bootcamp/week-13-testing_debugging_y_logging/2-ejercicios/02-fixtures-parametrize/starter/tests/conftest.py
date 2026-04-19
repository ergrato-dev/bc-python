"""
Fixtures compartidas para los tests de user_manager.

Las fixtures definidas aquí están disponibles para todos los tests
en este directorio y subdirectorios.
"""
import pytest
from src.user_manager import UserManager, User


# ============================================
# PASO 1: Fixtures Básicas
# ============================================
print("--- Paso 1: Fixtures básicas ---")

# Una fixture es una función decorada con @pytest.fixture
# que provee datos o recursos para los tests.

# Descomenta las siguientes líneas:
# @pytest.fixture
# def sample_user_data() -> dict:
#     """Fixture que provee datos de un usuario de prueba."""
#     return {
#         "name": "Alice",
#         "email": "alice@example.com",
#         "role": "user"
#     }


# @pytest.fixture
# def admin_user_data() -> dict:
#     """Fixture que provee datos de un admin."""
#     return {
#         "name": "Admin",
#         "email": "admin@example.com",
#         "role": "admin"
#     }


# @pytest.fixture
# def user_manager() -> UserManager:
#     """Fixture que provee una instancia limpia de UserManager."""
#     return UserManager()


# ============================================
# PASO 3: Fixtures con Setup y Teardown
# ============================================
print("--- Paso 3: Setup y Teardown ---")

# Usando yield, podemos ejecutar código de limpieza después del test.
# Todo lo que está antes de yield es "setup".
# Todo lo que está después de yield es "teardown".

# Descomenta las siguientes líneas:
# @pytest.fixture
# def manager_with_users(user_manager, sample_user_data, admin_user_data):
#     """Fixture que provee un manager con usuarios pre-cargados."""
#     # Setup: crear usuarios
#     user_manager.create(**sample_user_data)
#     user_manager.create(**admin_user_data)
#
#     yield user_manager  # El test recibe esto
#
#     # Teardown: limpiar (en este caso no es necesario porque
#     # user_manager es una fixture que se recrea para cada test)
#     print("\n[Teardown] Limpiando manager_with_users")


# ============================================
# PASO 4: Scopes de Fixtures
# ============================================
print("--- Paso 4: Scopes ---")

# scope="function" (default): Se ejecuta una vez por cada test
# scope="class": Se ejecuta una vez por clase de tests
# scope="module": Se ejecuta una vez por archivo .py
# scope="session": Se ejecuta una vez por toda la sesión de pytest

# Descomenta las siguientes líneas:
# @pytest.fixture(scope="module")
# def module_manager() -> UserManager:
#     """
#     Manager compartido para todo el módulo.
#
#     CUIDADO: Los tests que usen esta fixture compartirán estado.
#     Útil para recursos costosos de crear.
#     """
#     print("\n[Module Setup] Creando module_manager")
#     manager = UserManager()
#     yield manager
#     print("\n[Module Teardown] Destruyendo module_manager")


# ============================================
# PASO 7: Fixtures Parametrizadas
# ============================================
print("--- Paso 7: Fixtures parametrizadas ---")

# Las fixtures pueden parametrizarse para ejecutar tests
# con diferentes valores automáticamente.

# Descomenta las siguientes líneas:
# @pytest.fixture(params=["admin", "user", "guest"])
# def user_role(request) -> str:
#     """
#     Fixture parametrizada que provee diferentes roles.
#
#     Los tests que usen esta fixture se ejecutarán 3 veces,
#     una vez por cada rol.
#     """
#     return request.param


# @pytest.fixture(params=[
#     pytest.param({"name": "Alice", "email": "alice@test.com"}, id="alice"),
#     pytest.param({"name": "Bob", "email": "bob@test.com"}, id="bob"),
#     pytest.param({"name": "Charlie", "email": "charlie@test.com"}, id="charlie"),
# ])
# def user_data_set(request) -> dict:
#     """Fixture que provee diferentes conjuntos de datos de usuario."""
#     return request.param
