# 🧪 Ejercicio 01: Primeros Tests con pytest

## 🎯 Objetivos

- Escribir tests unitarios básicos con pytest
- Usar assertions para verificar comportamiento
- Testear funciones con diferentes tipos de entrada
- Verificar manejo de excepciones

---

## 📋 Instrucciones

Este ejercicio te guiará paso a paso para escribir tus primeros tests con pytest.

### Estructura del Ejercicio

```
01-primeros-tests/
├── README.md          # Este archivo
└── starter/
    ├── src/
    │   └── calculator.py   # Módulo a testear
    └── tests/
        └── test_calculator.py  # Tus tests
```

---

## Paso 1: Explorar el Código a Testear

Primero, revisa el módulo `calculator.py` en `starter/src/`. Contiene funciones matemáticas básicas que vamos a testear.

```python
# Funciones disponibles en calculator.py:
# - add(a, b) -> suma dos números
# - subtract(a, b) -> resta b de a
# - multiply(a, b) -> multiplica dos números
# - divide(a, b) -> divide a entre b (lanza ValueError si b=0)
# - power(base, exp) -> calcula base^exp
# - is_even(n) -> retorna True si n es par
```

---

## Paso 2: Test Básico de Suma

**Abre `starter/tests/test_calculator.py`** y descomenta la sección del Paso 2.

Aprenderás:
- Estructura básica de un test
- Usar `assert` para verificar resultados
- Convención de nombres `test_*`

```python
# Ejemplo de test básico:
def test_add_two_positive_numbers():
    result = add(2, 3)
    assert result == 5
```

---

## Paso 3: Tests con Diferentes Casos

Descomenta la sección del Paso 3 para probar más casos:

- Números negativos
- Cero
- Números flotantes

```python
# Ejemplo: testear con negativos
def test_add_negative_numbers():
    result = add(-5, -3)
    assert result == -8
```

---

## Paso 4: Testear Excepciones

Descomenta la sección del Paso 4 para aprender a verificar excepciones.

```python
import pytest

# Verificar que se lanza una excepción
def test_divide_by_zero_raises_error():
    with pytest.raises(ValueError):
        divide(10, 0)
```

---

## Paso 5: Tests con Mensajes Descriptivos

Descomenta la sección del Paso 5 para agregar mensajes a tus assertions.

```python
# Mensaje personalizado en caso de fallo
def test_with_message():
    result = multiply(3, 4)
    assert result == 12, f"Expected 12 but got {result}"
```

---

## Paso 6: Testear Valores Booleanos

Descomenta la sección del Paso 6 para testear la función `is_even`.

```python
# Testear booleanos
def test_is_even_with_even_number():
    assert is_even(4)  # Equivalente a assert is_even(4) == True

def test_is_even_with_odd_number():
    assert not is_even(5)  # Equivalente a assert is_even(5) == False
```

---

## 🚀 Ejecutar los Tests

```bash
# Desde la carpeta starter/
cd starter

# Ejecutar todos los tests
uv run pytest

# Ejecutar con verbose
uv run pytest -v

# Ejecutar un test específico
uv run pytest tests/test_calculator.py::test_add_two_positive_numbers

# Ver tests que fallan primero
uv run pytest -x
```

---

## ✅ Checklist de Verificación

- [ ] Tests de `add` pasan con números positivos, negativos y cero
- [ ] Tests de `subtract` verifican diferentes casos
- [ ] Tests de `multiply` incluyen multiplicación por cero
- [ ] Tests de `divide` verifican división normal y excepción
- [ ] Tests de `power` verifican exponentes positivos y cero
- [ ] Tests de `is_even` verifican números pares e impares
- [ ] Todos los tests pasan (`pytest` muestra verde)

---

## 📚 Recursos

- [pytest - Getting Started](https://docs.pytest.org/en/latest/getting-started.html)
- [pytest - Assertions](https://docs.pytest.org/en/latest/how-to/assert.html)
