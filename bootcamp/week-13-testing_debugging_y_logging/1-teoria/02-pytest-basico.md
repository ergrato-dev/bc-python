# 🔬 pytest Básico

## 📋 Contenido

1. [¿Qué es pytest?](#1-qué-es-pytest)
2. [Instalación y configuración](#2-instalación-y-configuración)
3. [Escribir tu primer test](#3-escribir-tu-primer-test)
4. [Assertions en pytest](#4-assertions-en-pytest)
5. [Organización de tests](#5-organización-de-tests)
6. [Ejecutar tests](#6-ejecutar-tests)

---

## 1. ¿Qué es pytest?

pytest es el framework de testing más popular de Python. Es simple, poderoso y extensible.

### ¿Por qué pytest?

| Característica | Descripción |
|----------------|-------------|
| **Simple** | Solo usa `assert`, sin API compleja |
| **Poderoso** | Fixtures, parametrización, plugins |
| **Informativo** | Mensajes de error detallados |
| **Compatible** | Funciona con unittest existente |
| **Extensible** | Miles de plugins disponibles |

### pytest vs unittest

```python
# unittest - Verboso
import unittest

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_negative(self):
        self.assertEqual(add(-1, -1), -2)

if __name__ == "__main__":
    unittest.main()

# pytest - Simple y limpio
def test_add():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, -1) == -2
```

---

## 2. Instalación y Configuración

### Instalación con uv

```bash
# Crear proyecto
uv init my_project
cd my_project

# Agregar pytest como dependencia de desarrollo
uv add --dev pytest pytest-cov
```

### Estructura del Proyecto

```
my_project/
├── src/
│   ├── __init__.py
│   └── calculator.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py        # Fixtures compartidas
│   └── test_calculator.py
├── pyproject.toml
└── pytest.ini             # Configuración (opcional)
```

### Configuración en pyproject.toml

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_functions = ["test_*"]
python_classes = ["Test*"]
addopts = "-v --tb=short"
```

### Configuración Alternativa: pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = -v
```

---

## 3. Escribir tu Primer Test

### Código a Testear

```python
# src/calculator.py
def add(a: float, b: float) -> float:
    """Suma dos números."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Resta b de a."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiplica dos números."""
    return a * b

def divide(a: float, b: float) -> float:
    """Divide a entre b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

### Tests Básicos

```python
# tests/test_calculator.py
from src.calculator import add, subtract, multiply, divide
import pytest


def test_add_integers():
    """Test suma de enteros."""
    result = add(2, 3)
    assert result == 5


def test_add_floats():
    """Test suma de flotantes."""
    result = add(2.5, 3.5)
    assert result == 6.0


def test_subtract_positive():
    """Test resta con resultado positivo."""
    result = subtract(10, 4)
    assert result == 6


def test_subtract_negative_result():
    """Test resta con resultado negativo."""
    result = subtract(4, 10)
    assert result == -6


def test_multiply():
    """Test multiplicación."""
    result = multiply(3, 4)
    assert result == 12


def test_divide():
    """Test división normal."""
    result = divide(10, 2)
    assert result == 5.0


def test_divide_by_zero_raises_error():
    """Test que divide por cero lanza ValueError."""
    with pytest.raises(ValueError) as exc_info:
        divide(10, 0)

    assert str(exc_info.value) == "Cannot divide by zero"
```

### Ejecutar los Tests

```bash
# Ejecutar todos los tests
pytest

# Salida esperada:
# tests/test_calculator.py::test_add_integers PASSED
# tests/test_calculator.py::test_add_floats PASSED
# tests/test_calculator.py::test_subtract_positive PASSED
# ...
# ==================== 7 passed in 0.03s ====================
```

---

## 4. Assertions en pytest

### Assertions Básicas

```python
# Igualdad
assert result == expected
assert result != unexpected

# Comparaciones
assert value > 0
assert value >= minimum
assert value < maximum
assert value <= limit

# Booleanos
assert is_valid
assert not is_invalid

# Identidad
assert obj is None
assert obj is not None

# Contenido
assert item in collection
assert item not in collection
```

### Assertions con Mensajes

```python
def test_with_message():
    result = calculate_discount(100, 20)
    assert result == 80, f"Expected 80 but got {result}"
```

### Comparar Flotantes

```python
# ❌ Puede fallar por precisión de flotantes
def test_float_bad():
    assert 0.1 + 0.2 == 0.3  # ¡Falla!

# ✅ Usar pytest.approx
def test_float_good():
    assert 0.1 + 0.2 == pytest.approx(0.3)

# Con tolerancia personalizada
def test_float_tolerance():
    assert 0.1 + 0.2 == pytest.approx(0.3, rel=1e-9)
```

### Testear Excepciones

```python
import pytest

def test_raises_value_error():
    """Test básico de excepción."""
    with pytest.raises(ValueError):
        int("not a number")


def test_raises_with_message():
    """Test excepción con mensaje específico."""
    with pytest.raises(ValueError, match="invalid literal"):
        int("not a number")


def test_raises_and_check_details():
    """Test excepción con acceso a detalles."""
    with pytest.raises(ValueError) as exc_info:
        int("abc")

    assert "invalid literal" in str(exc_info.value)
    assert exc_info.type == ValueError


def test_raises_type_error():
    """Test TypeError."""
    with pytest.raises(TypeError):
        len(42)  # int no tiene len
```

### Testear Warnings

```python
import warnings
import pytest

def deprecated_function():
    warnings.warn("This function is deprecated", DeprecationWarning)
    return 42

def test_deprecation_warning():
    with pytest.warns(DeprecationWarning):
        deprecated_function()

def test_warning_message():
    with pytest.warns(DeprecationWarning, match="deprecated"):
        deprecated_function()
```

---

## 5. Organización de Tests

### Convenciones de Nombres

```python
# Archivos: test_*.py o *_test.py
test_calculator.py
calculator_test.py

# Funciones: test_*
def test_add():
    pass

# Clases: Test*
class TestCalculator:
    def test_add(self):
        pass
```

### Agrupar con Clases

```python
# tests/test_calculator.py

class TestAddition:
    """Tests para la función add."""

    def test_add_positive_integers(self):
        assert add(2, 3) == 5

    def test_add_negative_integers(self):
        assert add(-2, -3) == -5

    def test_add_mixed_signs(self):
        assert add(-2, 5) == 3


class TestDivision:
    """Tests para la función divide."""

    def test_divide_evenly(self):
        assert divide(10, 2) == 5

    def test_divide_with_remainder(self):
        assert divide(10, 3) == pytest.approx(3.333, rel=0.01)

    def test_divide_by_zero(self):
        with pytest.raises(ValueError):
            divide(10, 0)
```

### Estructura Recomendada

```
tests/
├── __init__.py
├── conftest.py              # Fixtures globales
├── unit/                    # Tests unitarios
│   ├── __init__.py
│   ├── test_calculator.py
│   └── test_user.py
├── integration/             # Tests de integración
│   ├── __init__.py
│   └── test_user_service.py
└── e2e/                     # Tests end-to-end
    ├── __init__.py
    └── test_api.py
```

---

## 6. Ejecutar Tests

### Comandos Básicos

```bash
# Ejecutar todos los tests
pytest

# Ejecutar con verbose
pytest -v

# Ejecutar archivo específico
pytest tests/test_calculator.py

# Ejecutar test específico
pytest tests/test_calculator.py::test_add_integers

# Ejecutar clase de tests
pytest tests/test_calculator.py::TestAddition

# Ejecutar método de clase
pytest tests/test_calculator.py::TestAddition::test_add_positive
```

### Filtrar Tests

```bash
# Por nombre (substring match)
pytest -k "add"                    # Tests con "add" en el nombre
pytest -k "add or subtract"        # Tests con "add" o "subtract"
pytest -k "not divide"             # Tests sin "divide"
pytest -k "add and not negative"   # Combinaciones

# Por marcador (ver pytest avanzado)
pytest -m "slow"
pytest -m "not slow"
```

### Opciones Útiles

```bash
# Mostrar prints (no capturar stdout)
pytest -s

# Detener en primer fallo
pytest -x

# Detener después de N fallos
pytest --maxfail=3

# Ejecutar últimos tests fallidos
pytest --lf

# Ejecutar tests fallidos primero
pytest --ff

# Mostrar tests más lentos
pytest --durations=10

# Modo watch (requiere pytest-watch)
ptw
```

### Salida y Reportes

```bash
# Verbose con traceback corto
pytest -v --tb=short

# Solo nombres de tests
pytest --collect-only

# Output en formato JUnit (para CI)
pytest --junitxml=report.xml

# Coverage (requiere pytest-cov)
pytest --cov=src --cov-report=html
```

---

## 📝 Ejemplo Completo

### Estructura

```
calculator_project/
├── src/
│   ├── __init__.py
│   └── calculator.py
├── tests/
│   ├── __init__.py
│   └── test_calculator.py
└── pyproject.toml
```

### src/calculator.py

```python
"""Módulo de calculadora simple."""

def add(a: float, b: float) -> float:
    """Suma dos números."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Resta b de a."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiplica dos números."""
    return a * b

def divide(a: float, b: float) -> float:
    """Divide a entre b.

    Raises:
        ValueError: Si b es cero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def power(base: float, exponent: int) -> float:
    """Calcula base elevado a exponent."""
    return base ** exponent
```

### tests/test_calculator.py

```python
"""Tests para el módulo calculator."""
import pytest
from src.calculator import add, subtract, multiply, divide, power


class TestAdd:
    """Tests para la función add."""

    def test_add_positive_integers(self):
        assert add(2, 3) == 5

    def test_add_negative_integers(self):
        assert add(-2, -3) == -5

    def test_add_floats(self):
        assert add(2.5, 3.5) == 6.0

    def test_add_zero(self):
        assert add(5, 0) == 5


class TestSubtract:
    """Tests para la función subtract."""

    def test_subtract_larger_from_smaller(self):
        assert subtract(3, 5) == -2

    def test_subtract_same_numbers(self):
        assert subtract(5, 5) == 0


class TestMultiply:
    """Tests para la función multiply."""

    def test_multiply_positive(self):
        assert multiply(3, 4) == 12

    def test_multiply_by_zero(self):
        assert multiply(5, 0) == 0

    def test_multiply_negative(self):
        assert multiply(-3, 4) == -12


class TestDivide:
    """Tests para la función divide."""

    def test_divide_evenly(self):
        assert divide(10, 2) == 5.0

    def test_divide_with_remainder(self):
        assert divide(10, 3) == pytest.approx(3.333, rel=0.01)

    def test_divide_by_zero_raises_value_error(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)


class TestPower:
    """Tests para la función power."""

    def test_power_positive_exponent(self):
        assert power(2, 3) == 8

    def test_power_zero_exponent(self):
        assert power(5, 0) == 1

    def test_power_negative_exponent(self):
        assert power(2, -1) == 0.5
```

### Ejecutar

```bash
# Instalar dependencias
uv add --dev pytest

# Ejecutar tests
uv run pytest -v

# Salida:
# tests/test_calculator.py::TestAdd::test_add_positive_integers PASSED
# tests/test_calculator.py::TestAdd::test_add_negative_integers PASSED
# ...
# ==================== 14 passed in 0.05s ====================
```

---

## 📚 Resumen

| Concepto | Descripción |
|----------|-------------|
| `assert` | Verificar condiciones |
| `pytest.raises` | Verificar excepciones |
| `pytest.approx` | Comparar flotantes |
| `pytest.warns` | Verificar warnings |
| `-v` | Output verbose |
| `-k` | Filtrar por nombre |
| `-x` | Parar en primer fallo |
| `--cov` | Medir cobertura |

---

## 🔗 Referencias

- [pytest Documentation](https://docs.pytest.org/)
- [pytest Quick Start](https://docs.pytest.org/en/latest/getting-started.html)
- [pytest Assertions](https://docs.pytest.org/en/latest/how-to/assert.html)
