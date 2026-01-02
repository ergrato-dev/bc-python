"""
Ejercicio 02: Excepciones Robustas
==================================

Aprende a manejar errores de forma profesional en Python.

Instrucciones:
1. Lee cada sección y descomenta el código
2. Ejecuta el script después de cada paso
3. Observa cómo se manejan los diferentes errores

Ejecutar:
    python main.py
"""

from pathlib import Path
import tempfile
import logging

# Configurar logging básico
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Función principal del ejercicio."""

    print("=" * 60)
    print("EJERCICIO: Excepciones Robustas")
    print("=" * 60)

    # ============================================
    # PASO 1: Captura de Excepciones Específicas
    # ============================================
    print("\n--- Paso 1: Excepciones Específicas ---")

    # Descomenta las siguientes líneas:
    # def parse_number(value: str) -> int:
    #     """Convierte string a número con manejo de error."""
    #     try:
    #         return int(value)
    #     except ValueError:
    #         print(f"  Error: '{value}' no es un número válido")
    #         return 0
    #
    # # Probar con diferentes valores
    # test_values = ["42", "abc", "3.14", ""]
    # for val in test_values:
    #     result = parse_number(val)
    #     print(f"  parse_number('{val}') = {result}")

    # ============================================
    # PASO 2: Múltiples Excepciones
    # ============================================
    print("\n--- Paso 2: Múltiples Excepciones ---")

    # Descomenta las siguientes líneas:
    # def safe_divide(data: dict, key: str, divisor: float) -> float:
    #     """División segura con manejo de múltiples errores."""
    #     try:
    #         value = data[key]
    #         result = value / divisor
    #         return result
    #     except KeyError:
    #         print(f"  Error: Clave '{key}' no encontrada")
    #         return 0.0
    #     except ZeroDivisionError:
    #         print(f"  Error: División por cero")
    #         return float('inf')
    #     except TypeError:
    #         print(f"  Error: Tipo de dato inválido")
    #         return 0.0
    #
    # data = {"a": 100, "b": 50, "c": "texto"}
    #
    # print(f"  safe_divide(data, 'a', 5) = {safe_divide(data, 'a', 5)}")
    # print(f"  safe_divide(data, 'x', 5) = {safe_divide(data, 'x', 5)}")
    # print(f"  safe_divide(data, 'b', 0) = {safe_divide(data, 'b', 0)}")
    # print(f"  safe_divide(data, 'c', 5) = {safe_divide(data, 'c', 5)}")

    # ============================================
    # PASO 3: else y finally
    # ============================================
    print("\n--- Paso 3: else y finally ---")

    with tempfile.TemporaryDirectory() as temp_dir:
        work_dir = Path(temp_dir)

        # Crear archivo de prueba
        test_file = work_dir / "datos.txt"
        test_file.write_text("Contenido del archivo", encoding="utf-8")

        # Descomenta las siguientes líneas:
        # def read_file_safe(path: Path) -> str | None:
        #     """Lee archivo con manejo completo de excepciones."""
        #     content = None
        #     try:
        #         file = open(path, "r", encoding="utf-8")
        #     except FileNotFoundError:
        #         print(f"  Archivo no encontrado: {path.name}")
        #     except PermissionError:
        #         print(f"  Sin permisos: {path.name}")
        #     else:
        #         # Solo se ejecuta si NO hubo excepción
        #         content = file.read()
        #         file.close()
        #         print(f"  Lectura exitosa: {len(content)} caracteres")
        #     finally:
        #         # SIEMPRE se ejecuta
        #         print(f"  Operación completada para: {path.name}")
        #
        #     return content
        #
        # # Probar con archivo existente
        # read_file_safe(test_file)
        #
        # # Probar con archivo inexistente
        # read_file_safe(work_dir / "no_existe.txt")

    # ============================================
    # PASO 4: Excepciones Personalizadas
    # ============================================
    print("\n--- Paso 4: Excepciones Personalizadas ---")

    # Descomenta las siguientes líneas:
    # class ValidationError(Exception):
    #     """Error de validación de datos."""
    #
    #     def __init__(self, field: str, message: str):
    #         self.field = field
    #         self.message = message
    #         super().__init__(f"Campo '{field}': {message}")
    #
    #
    # class UserNotFoundError(Exception):
    #     """Usuario no encontrado."""
    #
    #     def __init__(self, user_id: int):
    #         self.user_id = user_id
    #         super().__init__(f"Usuario con ID {user_id} no encontrado")
    #
    #
    # def validate_email(email: str) -> None:
    #     """Valida formato de email."""
    #     if not email:
    #         raise ValidationError("email", "El email es requerido")
    #     if "@" not in email:
    #         raise ValidationError("email", "Formato inválido")
    #     if len(email) < 5:
    #         raise ValidationError("email", "Email muy corto")
    #
    #
    # # Probar validación
    # emails_test = ["user@example.com", "", "invalid", "a@b"]
    #
    # for email in emails_test:
    #     try:
    #         validate_email(email)
    #         print(f"  ✓ Email válido: {email}")
    #     except ValidationError as e:
    #         print(f"  ✗ {e}")

    # ============================================
    # PASO 5: Re-lanzar Excepciones con Logging
    # ============================================
    print("\n--- Paso 5: Re-lanzar con Logging ---")

    # Descomenta las siguientes líneas:
    # def process_data(data: list[int]) -> int:
    #     """Procesa datos con logging de errores."""
    #     try:
    #         result = sum(data) / len(data)
    #         logger.info(f"Procesamiento exitoso: promedio = {result}")
    #         return int(result)
    #     except ZeroDivisionError:
    #         logger.error("Lista vacía - no se puede calcular promedio")
    #         raise
    #     except TypeError as e:
    #         logger.error(f"Tipo de dato inválido: {e}")
    #         raise
    #
    # # Caso exitoso
    # try:
    #     result = process_data([10, 20, 30])
    #     print(f"  Resultado: {result}")
    # except Exception as e:
    #     print(f"  Error capturado: {e}")
    #
    # # Caso con error
    # try:
    #     result = process_data([])
    #     print(f"  Resultado: {result}")
    # except ZeroDivisionError:
    #     print("  Error manejado: lista vacía")

    # ============================================
    # PASO 6: Encadenamiento de Excepciones
    # ============================================
    print("\n--- Paso 6: Encadenamiento (from) ---")

    # Descomenta las siguientes líneas:
    # class ConfigError(Exception):
    #     """Error de configuración."""
    #     pass
    #
    #
    # def load_config(path: str) -> dict:
    #     """Carga configuración preservando causa original."""
    #     try:
    #         content = Path(path).read_text(encoding="utf-8")
    #         return {"content": content}
    #     except FileNotFoundError as e:
    #         # 'from e' preserva la excepción original
    #         raise ConfigError(f"Config no encontrada: {path}") from e
    #
    #
    # try:
    #     config = load_config("config_inexistente.json")
    # except ConfigError as e:
    #     print(f"  ConfigError: {e}")
    #     print(f"  Causa original: {e.__cause__}")

    # ============================================
    # PASO 7: Ejercicio Integrador
    # ============================================
    print("\n--- Paso 7: Ejercicio Integrador ---")

    # Crea un sistema de procesamiento de usuarios robusto

    # Descomenta las siguientes líneas:
    # class UserError(Exception):
    #     """Error base para usuarios."""
    #     pass
    #
    # class UserValidationError(UserError):
    #     """Error de validación de usuario."""
    #     def __init__(self, errors: list[str]):
    #         self.errors = errors
    #         super().__init__(f"Errores de validación: {errors}")
    #
    # class UserService:
    #     """Servicio de gestión de usuarios."""
    #
    #     def __init__(self):
    #         self._users: dict[int, dict] = {}
    #         self._next_id = 1
    #
    #     def create_user(self, name: str, email: str, age: int) -> dict:
    #         """Crea usuario con validación."""
    #         errors = []
    #
    #         if not name or len(name) < 2:
    #             errors.append("Nombre debe tener al menos 2 caracteres")
    #         if not email or "@" not in email:
    #             errors.append("Email inválido")
    #         if age < 0 or age > 150:
    #             errors.append("Edad debe estar entre 0 y 150")
    #
    #         if errors:
    #             raise UserValidationError(errors)
    #
    #         user = {
    #             "id": self._next_id,
    #             "name": name,
    #             "email": email,
    #             "age": age
    #         }
    #         self._users[self._next_id] = user
    #         self._next_id += 1
    #
    #         logger.info(f"Usuario creado: {user['name']}")
    #         return user
    #
    #     def get_user(self, user_id: int) -> dict:
    #         """Obtiene usuario por ID."""
    #         if user_id not in self._users:
    #             raise UserNotFoundError(user_id)
    #         return self._users[user_id]
    #
    #
    # # Probar el servicio
    # service = UserService()
    #
    # # Usuario válido
    # try:
    #     user = service.create_user("Ana García", "ana@example.com", 28)
    #     print(f"  ✓ Usuario creado: {user}")
    # except UserValidationError as e:
    #     print(f"  ✗ Validación: {e.errors}")
    #
    # # Usuario inválido
    # try:
    #     user = service.create_user("A", "invalid", 200)
    #     print(f"  ✓ Usuario creado: {user}")
    # except UserValidationError as e:
    #     print(f"  ✗ Validación fallida:")
    #     for error in e.errors:
    #         print(f"      - {error}")
    #
    # # Buscar usuario inexistente
    # try:
    #     user = service.get_user(999)
    #     print(f"  ✓ Usuario encontrado: {user}")
    # except UserNotFoundError as e:
    #     print(f"  ✗ {e}")

    print("\n" + "=" * 60)
    print("¡Ejercicio completado!")
    print("=" * 60)


if __name__ == "__main__":
    main()
