"""
Tests para el módulo user_manager usando fixtures y parametrización.

Ejercicio: Descomenta cada sección paso a paso.
"""
import pytest
from src.user_manager import UserManager, User


# ============================================
# PASO 2: Usar Fixtures en Tests
# ============================================
print("--- Paso 2: Usar fixtures ---")

# Para usar una fixture, simplemente agrégala como parámetro del test.
# pytest inyecta automáticamente el valor de la fixture.

# Descomenta las siguientes líneas:
# def test_create_user(user_manager, sample_user_data):
#     """Test que usa fixtures para datos y manager."""
#     user = user_manager.create(**sample_user_data)
#
#     assert user.name == sample_user_data["name"]
#     assert user.email == sample_user_data["email"]
#     assert user.id is not None


# def test_create_admin(user_manager, admin_user_data):
#     """Test creación de admin usando fixtures."""
#     user = user_manager.create(**admin_user_data)
#
#     assert user.is_admin()
#     assert user.get_display_name().startswith("[Admin]")


# def test_manager_starts_empty(user_manager):
#     """Test que el manager empieza vacío."""
#     assert user_manager.count() == 0
#     assert user_manager.list_all() == []


# def test_get_user_by_id(user_manager, sample_user_data):
#     """Test obtener usuario por ID."""
#     created = user_manager.create(**sample_user_data)
#
#     retrieved = user_manager.get(created.id)
#
#     assert retrieved is not None
#     assert retrieved.id == created.id
#     assert retrieved.email == created.email


# ============================================
# PASO 3: Tests con Fixtures de Setup/Teardown
# ============================================
print("--- Paso 3: Fixtures con setup/teardown ---")

# Las fixtures con yield permiten setup antes y teardown después.

# Descomenta las siguientes líneas:
# def test_manager_has_preloaded_users(manager_with_users):
#     """Test que usa fixture con usuarios pre-cargados."""
#     assert manager_with_users.count() == 2
#
#
# def test_find_preloaded_admin(manager_with_users):
#     """Test buscar admin en manager pre-cargado."""
#     admin = manager_with_users.find_by_email("admin@example.com")
#
#     assert admin is not None
#     assert admin.is_admin()


# ============================================
# PASO 5: Parametrización Básica
# ============================================
print("--- Paso 5: Parametrización básica ---")

# @pytest.mark.parametrize ejecuta el test múltiples veces
# con diferentes valores.

# Descomenta las siguientes líneas:
# @pytest.mark.parametrize("email, expected_valid", [
#     ("user@example.com", True),
#     ("test.email@domain.org", True),
#     ("name+tag@example.com", True),
#     ("invalid-email", False),
#     ("missing@domain", False),
#     ("@nodomain.com", False),
#     ("", False),
#     ("spaces in@email.com", False),
# ])
# def test_email_validation(email: str, expected_valid: bool):
#     """Test validación de email con múltiples casos."""
#     result = UserManager.validate_email(email)
#     assert result == expected_valid


# @pytest.mark.parametrize("name, expected_valid", [
#     ("Alice", True),
#     ("Bob Smith", True),
#     ("A", False),  # Muy corto
#     ("", False),  # Vacío
#     ("A" * 51, False),  # Muy largo
#     ("  ", False),  # Solo espacios
# ])
# def test_name_validation(name: str, expected_valid: bool):
#     """Test validación de nombre con múltiples casos."""
#     result = UserManager.validate_name(name)
#     assert result == expected_valid


# ============================================
# PASO 6: Parametrización con IDs
# ============================================
print("--- Paso 6: IDs personalizados ---")

# Los IDs personalizados hacen la salida más legible.

# Descomenta las siguientes líneas:
# @pytest.mark.parametrize("role, can_admin", [
#     pytest.param("admin", True, id="admin-can-administrate"),
#     pytest.param("user", False, id="regular-user-cannot"),
#     pytest.param("guest", False, id="guest-cannot"),
# ])
# def test_user_admin_permissions(user_manager, role: str, can_admin: bool):
#     """Test permisos de admin según rol."""
#     user = user_manager.create(
#         name="Test User",
#         email=f"{role}@example.com",
#         role=role
#     )
#
#     assert user.is_admin() == can_admin


# ============================================
# PASO 7: Usando Fixtures Parametrizadas
# ============================================
print("--- Paso 7: Fixtures parametrizadas ---")

# Los tests que usan fixtures parametrizadas se ejecutan
# múltiples veces, una por cada parámetro.

# Descomenta las siguientes líneas:
# def test_create_user_with_role(user_manager, user_role):
#     """
#     Test que se ejecuta 3 veces (admin, user, guest).
#
#     user_role es una fixture parametrizada definida en conftest.py
#     """
#     user = user_manager.create(
#         name="Test",
#         email=f"{user_role}@test.com",
#         role=user_role
#     )
#
#     assert user.role == user_role


# def test_create_from_data_set(user_manager, user_data_set):
#     """
#     Test que se ejecuta con diferentes conjuntos de datos.
#
#     user_data_set es una fixture parametrizada con IDs.
#     """
#     user = user_manager.create(**user_data_set, role="user")
#
#     assert user.name == user_data_set["name"]
#     assert user.email == user_data_set["email"]


# ============================================
# BONUS: Combinar Parametrize con Fixtures
# ============================================
print("--- Bonus: Combinaciones ---")

# Puedes combinar @parametrize con fixtures para más flexibilidad.

# Descomenta las siguientes líneas:
# @pytest.mark.parametrize("new_name", ["Updated", "Changed", "Modified"])
# def test_update_user_name(manager_with_users, new_name):
#     """Test actualizar nombre de usuario."""
#     # Obtener el primer usuario
#     users = manager_with_users.list_all()
#     user = users[0]
#
#     # Actualizar
#     updated = manager_with_users.update(user.id, name=new_name)
#
#     assert updated.name == new_name


# class TestUserManagerOperations:
#     """Clase que agrupa tests relacionados."""
#
#     def test_delete_existing_user(self, manager_with_users):
#         """Test eliminar usuario existente."""
#         users = manager_with_users.list_all()
#         user_id = users[0].id
#
#         result = manager_with_users.delete(user_id)
#
#         assert result is True
#         assert manager_with_users.get(user_id) is None
#
#     def test_delete_nonexistent_user(self, user_manager):
#         """Test eliminar usuario que no existe."""
#         result = user_manager.delete(999)
#
#         assert result is False
#
#     @pytest.mark.parametrize("invalid_email", [
#         "not-an-email",
#         "",
#         "@missing-local.com",
#     ])
#     def test_create_with_invalid_email_raises(self, user_manager, invalid_email):
#         """Test que crear con email inválido lanza excepción."""
#         with pytest.raises(ValueError, match="Invalid email"):
#             user_manager.create(name="Test", email=invalid_email)
