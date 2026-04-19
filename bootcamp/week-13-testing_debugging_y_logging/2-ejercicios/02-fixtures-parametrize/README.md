# 🔧 Ejercicio 02: Fixtures y Parametrización

## 🎯 Objetivos

- Crear y usar fixtures para proveer datos de prueba
- Entender los diferentes scopes de fixtures
- Usar `@pytest.mark.parametrize` para múltiples casos
- Combinar fixtures con parametrización

---

## 📋 Instrucciones

Este ejercicio te enseñará a usar fixtures y parametrización para escribir tests más eficientes y mantenibles.

### Estructura del Ejercicio

```
02-fixtures-parametrize/
├── README.md          # Este archivo
└── starter/
    ├── src/
    │   └── user_manager.py   # Módulo a testear
    ├── tests/
    │   ├── conftest.py       # Fixtures compartidas
    │   └── test_user_manager.py
    └── pyproject.toml
```

---

## Paso 1: Fixtures Básicas

**Abre `starter/tests/conftest.py`** y descomenta la sección del Paso 1.

Las fixtures proveen datos o recursos reutilizables para los tests.

```python
@pytest.fixture
def sample_user():
    """Fixture que provee un usuario de prueba."""
    return {"name": "Alice", "email": "alice@example.com"}
```

---

## Paso 2: Usar Fixtures en Tests

**Abre `starter/tests/test_user_manager.py`** y descomenta la sección del Paso 2.

Para usar una fixture, simplemente agrégala como parámetro del test.

```python
def test_create_user(sample_user):
    # sample_user contiene los datos de la fixture
    user = UserManager().create(sample_user)
    assert user.name == "Alice"
```

---

## Paso 3: Fixtures con Setup y Teardown

Descomenta la sección del Paso 3 en `conftest.py`.

Usa `yield` para ejecutar código de limpieza después del test.

```python
@pytest.fixture
def temp_database():
    # Setup
    db = Database()
    db.connect()

    yield db  # El test recibe esto

    # Teardown (se ejecuta después del test)
    db.disconnect()
```

---

## Paso 4: Scopes de Fixtures

Descomenta la sección del Paso 4.

Los scopes controlan cuántas veces se ejecuta la fixture:
- `function`: Una vez por test (default)
- `class`: Una vez por clase de tests
- `module`: Una vez por archivo
- `session`: Una vez por sesión de pytest

```python
@pytest.fixture(scope="module")
def expensive_resource():
    """Se crea solo una vez para todo el módulo."""
    return create_expensive_resource()
```

---

## Paso 5: Parametrización Básica

Descomenta la sección del Paso 5 en `test_user_manager.py`.

`@pytest.mark.parametrize` ejecuta el mismo test con diferentes datos.

```python
@pytest.mark.parametrize("email, is_valid", [
    ("user@example.com", True),
    ("invalid-email", False),
    ("", False),
])
def test_email_validation(email, is_valid):
    assert validate_email(email) == is_valid
```

---

## Paso 6: Parametrización con IDs

Descomenta la sección del Paso 6.

Los IDs personalizados hacen la salida más legible.

```python
@pytest.mark.parametrize("input, expected", [
    pytest.param("hello", "HELLO", id="lowercase"),
    pytest.param("WORLD", "WORLD", id="uppercase"),
])
def test_uppercase(input, expected):
    assert input.upper() == expected
```

---

## Paso 7: Fixtures Parametrizadas

Descomenta la sección del Paso 7 en `conftest.py`.

Las fixtures también pueden parametrizarse.

```python
@pytest.fixture(params=["admin", "user", "guest"])
def user_role(request):
    """Fixture que provee diferentes roles."""
    return request.param
```

---

## 🚀 Ejecutar los Tests

```bash
cd starter

# Ejecutar todos los tests
uv run pytest -v

# Ver parametrizaciones expandidas
uv run pytest -v --collect-only

# Ejecutar solo tests parametrizados específicos
uv run pytest -v -k "valid_email"

# Ver fixtures disponibles
uv run pytest --fixtures
```

---

## ✅ Checklist de Verificación

- [ ] Fixture `sample_user` funciona correctamente
- [ ] Fixture `user_manager` provee instancia del manager
- [ ] Tests usan fixtures sin crear datos manualmente
- [ ] Parametrización ejecuta múltiples casos
- [ ] IDs personalizados aparecen en la salida
- [ ] Fixtures con `yield` ejecutan teardown
- [ ] Todos los tests pasan

---

## 📚 Recursos

- [pytest Fixtures](https://docs.pytest.org/en/latest/how-to/fixtures.html)
- [pytest Parametrize](https://docs.pytest.org/en/latest/how-to/parametrize.html)
