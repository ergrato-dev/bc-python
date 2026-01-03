"""
Tests para el módulo calculator.

Ejercicio: Descomenta cada sección paso a paso y ejecuta los tests.
"""
import pytest
from src.calculator import add, subtract, multiply, divide, power, is_even


# ============================================
# PASO 2: Test Básico de Suma
# ============================================
print("--- Paso 2: Test básico ---")

# Un test es una función que verifica comportamiento.
# El nombre debe empezar con test_ para que pytest lo reconozca.
# Usamos assert para verificar que el resultado es el esperado.

# Descomenta las siguientes líneas:
# def test_add_two_positive_numbers():
#     """Test que verifica la suma de dos números positivos."""
#     result = add(2, 3)
#     assert result == 5


# def test_add_returns_correct_type():
#     """Test que verifica que add retorna un número."""
#     result = add(1, 1)
#     assert isinstance(result, (int, float))


# ============================================
# PASO 3: Tests con Diferentes Casos
# ============================================
print("--- Paso 3: Diferentes casos ---")

# Es importante testear diferentes escenarios:
# - Casos normales (happy path)
# - Casos límite (edge cases)
# - Casos especiales (cero, negativos, etc.)

# Descomenta las siguientes líneas:
# def test_add_negative_numbers():
#     """Test suma con números negativos."""
#     assert add(-5, -3) == -8


# def test_add_mixed_signs():
#     """Test suma con signos mixtos."""
#     assert add(-10, 5) == -5
#     assert add(10, -5) == 5


# def test_add_with_zero():
#     """Test suma con cero."""
#     assert add(5, 0) == 5
#     assert add(0, 5) == 5
#     assert add(0, 0) == 0


# def test_add_floats():
#     """Test suma con flotantes."""
#     result = add(2.5, 3.5)
#     assert result == 6.0


# def test_subtract_positive_result():
#     """Test resta con resultado positivo."""
#     assert subtract(10, 4) == 6


# def test_subtract_negative_result():
#     """Test resta con resultado negativo."""
#     assert subtract(4, 10) == -6


# def test_multiply_positive_numbers():
#     """Test multiplicación de positivos."""
#     assert multiply(3, 4) == 12


# def test_multiply_by_zero():
#     """Test multiplicación por cero."""
#     assert multiply(100, 0) == 0
#     assert multiply(0, 100) == 0


# def test_multiply_negative_numbers():
#     """Test multiplicación con negativos."""
#     assert multiply(-3, 4) == -12
#     assert multiply(-3, -4) == 12


# ============================================
# PASO 4: Testear Excepciones
# ============================================
print("--- Paso 4: Excepciones ---")

# pytest.raises() verifica que se lanza una excepción específica.
# Es crucial testear que el código maneja errores correctamente.

# Descomenta las siguientes líneas:
# def test_divide_normal():
#     """Test división normal."""
#     assert divide(10, 2) == 5.0


# def test_divide_with_remainder():
#     """Test división con resto."""
#     result = divide(10, 3)
#     # Usar pytest.approx para comparar flotantes
#     assert result == pytest.approx(3.333, rel=0.01)


# def test_divide_by_zero_raises_value_error():
#     """Test que dividir por cero lanza ValueError."""
#     with pytest.raises(ValueError):
#         divide(10, 0)


# def test_divide_by_zero_error_message():
#     """Test que el mensaje de error es correcto."""
#     with pytest.raises(ValueError) as exc_info:
#         divide(10, 0)
#     assert str(exc_info.value) == "Cannot divide by zero"


# ============================================
# PASO 5: Tests con Mensajes Descriptivos
# ============================================
print("--- Paso 5: Mensajes descriptivos ---")

# Puedes agregar mensajes a los asserts para debugging.
# El mensaje se muestra solo cuando el test falla.

# Descomenta las siguientes líneas:
# def test_power_positive_exponent():
#     """Test potencia con exponente positivo."""
#     result = power(2, 3)
#     assert result == 8, f"2^3 should be 8, but got {result}"


# def test_power_zero_exponent():
#     """Test potencia con exponente cero."""
#     result = power(5, 0)
#     assert result == 1, "Any number to the power of 0 should be 1"


# def test_power_negative_exponent():
#     """Test potencia con exponente negativo."""
#     result = power(2, -1)
#     assert result == 0.5, f"2^-1 should be 0.5, but got {result}"


# def test_power_with_zero_base():
#     """Test potencia con base cero."""
#     result = power(0, 5)
#     assert result == 0, "0 raised to any positive power should be 0"


# ============================================
# PASO 6: Testear Valores Booleanos
# ============================================
print("--- Paso 6: Booleanos ---")

# Para funciones que retornan booleanos, podemos usar
# assert directamente sin comparar con True/False.

# Descomenta las siguientes líneas:
# def test_is_even_with_even_number():
#     """Test is_even con número par."""
#     assert is_even(4)
#     assert is_even(0)
#     assert is_even(-2)
#     assert is_even(100)


# def test_is_even_with_odd_number():
#     """Test is_even con número impar."""
#     assert not is_even(5)
#     assert not is_even(1)
#     assert not is_even(-3)
#     assert not is_even(99)


# ============================================
# BONUS: Agrupa Tests Relacionados en Clases
# ============================================
print("--- Bonus: Clases de tests ---")

# Las clases ayudan a organizar tests relacionados.
# El nombre de la clase debe empezar con Test.

# Descomenta las siguientes líneas:
# class TestDivision:
#     """Grupo de tests para la función divide."""
#
#     def test_divide_integers(self):
#         assert divide(10, 2) == 5.0
#
#     def test_divide_floats(self):
#         result = divide(7.5, 2.5)
#         assert result == pytest.approx(3.0)
#
#     def test_divide_negative(self):
#         assert divide(-10, 2) == -5.0
#
#     def test_divide_by_zero(self):
#         with pytest.raises(ValueError):
#             divide(1, 0)
