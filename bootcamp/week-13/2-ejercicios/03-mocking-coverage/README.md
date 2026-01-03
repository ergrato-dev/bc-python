# 🎭 Ejercicio 03: Mocking y Coverage

## 🎯 Objetivos

- Usar `unittest.mock` para simular dependencias externas
- Aplicar `@patch` para reemplazar objetos temporalmente
- Verificar llamadas a mocks con asserts
- Medir cobertura de código con `pytest-cov`

---

## 📋 Instrucciones

Este ejercicio te enseñará a aislar tu código de dependencias externas usando mocking, y a medir qué porcentaje de tu código está cubierto por tests.

### Estructura del Ejercicio

```
03-mocking-coverage/
├── README.md          # Este archivo
└── starter/
    ├── src/
    │   ├── weather_service.py   # Servicio que llama a API externa
    │   └── notification.py      # Servicio de notificaciones
    ├── tests/
    │   ├── conftest.py
    │   ├── test_weather.py
    │   └── test_notification.py
    └── pyproject.toml
```

---

## Paso 1: Entender el Problema

**Abre `starter/src/weather_service.py`** para ver el código.

El servicio hace llamadas HTTP a una API externa. No queremos:
- Hacer llamadas reales en tests (lentas, pueden fallar)
- Depender de internet
- Gastar cuota de API

**Solución**: Mockear las llamadas HTTP.

---

## Paso 2: Mock Básico

**Abre `starter/tests/test_weather.py`** y descomenta la sección del Paso 2.

Usamos `@patch` para reemplazar `requests.get` temporalmente.

```python
from unittest.mock import patch, Mock

@patch("requests.get")
def test_get_weather(mock_get):
    # Configurar qué retorna el mock
    mock_get.return_value.json.return_value = {"temp": 25}
    mock_get.return_value.status_code = 200

    # Ejecutar código que usa requests.get
    result = get_weather("London")

    # Verificar resultado
    assert result["temp"] == 25
```

---

## Paso 3: Verificar Llamadas al Mock

Descomenta la sección del Paso 3.

Podemos verificar que el mock fue llamado correctamente:

```python
@patch("requests.get")
def test_api_called_correctly(mock_get):
    get_weather("Paris")

    # Verificar que se llamó
    mock_get.assert_called_once()

    # Verificar argumentos
    mock_get.assert_called_with(
        "https://api.weather.com/Paris",
        timeout=10
    )
```

---

## Paso 4: Simular Errores

Descomenta la sección del Paso 4.

Usar `side_effect` para simular errores:

```python
@patch("requests.get")
def test_handles_network_error(mock_get):
    mock_get.side_effect = ConnectionError("Network unavailable")

    with pytest.raises(WeatherServiceError):
        get_weather("London")
```

---

## Paso 5: Mockear Múltiples Dependencias

Descomenta la sección del Paso 5.

Puedes usar múltiples `@patch`:

```python
@patch("module.dependency_1")
@patch("module.dependency_2")
def test_multiple_mocks(mock_dep2, mock_dep1):
    # NOTA: El orden de los parámetros es inverso al de los decoradores
    pass
```

---

## Paso 6: Medir Cobertura

Ejecuta tests con cobertura:

```bash
cd starter

# Instalar dependencias
uv sync

# Ejecutar con cobertura
uv run pytest --cov=src --cov-report=term-missing

# Generar reporte HTML
uv run pytest --cov=src --cov-report=html
# Abrir htmlcov/index.html en el navegador
```

---

## Paso 7: Mejorar Cobertura

Descomenta la sección del Paso 7 en `test_notification.py`.

Identifica líneas no cubiertas y escribe tests para ellas.

---

## 🚀 Ejecutar los Tests

```bash
cd starter

# Todos los tests
uv run pytest -v

# Con cobertura detallada
uv run pytest --cov=src --cov-report=term-missing -v

# Solo tests de weather
uv run pytest tests/test_weather.py -v

# Ver líneas no cubiertas
uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```

---

## 📊 Interpretar Cobertura

```
Name                      Stmts   Miss  Cover   Missing
-------------------------------------------------------
src/weather_service.py       25      3    88%   45-47
src/notification.py          30      5    83%   22, 35-38
-------------------------------------------------------
TOTAL                        55      8    85%
```

- **Stmts**: Líneas de código ejecutables
- **Miss**: Líneas no ejecutadas por tests
- **Cover**: Porcentaje cubierto
- **Missing**: Números de línea sin cubrir

---

## ✅ Checklist de Verificación

- [ ] Tests mockean `requests.get` correctamente
- [ ] Verificas que los mocks fueron llamados
- [ ] Tests manejan errores de red simulados
- [ ] Cobertura de `weather_service.py` > 90%
- [ ] Cobertura de `notification.py` > 85%
- [ ] Reporte HTML generado y revisado
- [ ] Todos los tests pasan

---

## 📚 Recursos

- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Mocking Best Practices](https://realpython.com/python-mock-library/)
