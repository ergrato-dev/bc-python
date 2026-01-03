# 📖 Glosario - Semana 13: Testing, Debugging y Logging

## A

### AAA Pattern (Arrange-Act-Assert)

Patrón para estructurar tests en tres fases: preparar datos (Arrange), ejecutar la acción (Act) y verificar resultados (Assert).

```python
def test_add():
    # Arrange
    calc = Calculator()
    # Act
    result = calc.add(2, 3)
    # Assert
    assert result == 5
```

### Assert

Declaración que verifica que una condición sea verdadera. Si falla, el test falla.

```python
assert result == expected
assert len(items) > 0
assert "error" in message.lower()
```

### Assertion Error

Excepción lanzada cuando una aserción falla.

---

## B

### Breakpoint

Punto en el código donde el debugger pausa la ejecución para inspección.

```python
def process_data(data):
    breakpoint()  # Pausa aquí
    return data.transform()
```

### Branch Coverage

Métrica que mide qué porcentaje de ramas (if/else) del código han sido ejecutadas por los tests.

---

## C

### Code Coverage

Métrica que indica qué porcentaje del código fuente es ejecutado durante los tests.

### conftest.py

Archivo especial de pytest que contiene fixtures compartidas entre múltiples archivos de test.

### Continuous Integration (CI)

Práctica de integrar y testear código frecuentemente de forma automática.

---

## D

### Debug

Proceso de identificar y corregir errores en el código.

### Debugger

Herramienta que permite ejecutar código paso a paso e inspeccionar su estado.

---

## E

### E2E Test (End-to-End)

Test que verifica el flujo completo de una aplicación, desde la interfaz hasta la base de datos.

### Exception

Error en tiempo de ejecución que interrumpe el flujo normal del programa.

---

## F

### Fixture

En pytest, función que provee datos o configuración para los tests.

```python
@pytest.fixture
def database():
    db = create_test_db()
    yield db
    db.cleanup()
```

### Fixture Scope

Alcance de una fixture: function, class, module, session.

### FIRST Principles

Principios para escribir buenos tests: Fast, Independent, Repeatable, Self-validating, Timely.

---

## G

### Green Test

Test que pasa exitosamente.

---

## H

### Handler (Logging)

Componente que determina dónde se envían los mensajes de log (archivo, consola, etc.).

---

## I

### Integration Test

Test que verifica la interacción entre múltiples componentes del sistema.

### Isolation

Principio de que cada test debe ser independiente de los demás.

---

## L

### Log Level

Nivel de severidad de un mensaje de log: DEBUG, INFO, WARNING, ERROR, CRITICAL.

### Logger

Objeto que genera y envía mensajes de log.

```python
import logging
logger = logging.getLogger(__name__)
logger.info("Operation completed")
```

---

## M

### Marker (pytest)

Decorador que etiqueta tests para filtrado o comportamiento especial.

```python
@pytest.mark.slow
def test_large_dataset():
    pass
```

### Mock

Objeto que simula el comportamiento de otro objeto para propósitos de testing.

```python
from unittest.mock import Mock
mock_api = Mock()
mock_api.get_data.return_value = {"key": "value"}
```

### MagicMock

Mock que implementa automáticamente métodos mágicos de Python.

### Monkey Patching

Técnica de reemplazar atributos o métodos en tiempo de ejecución.

---

## P

### Parametrize

Decorador de pytest que permite ejecutar un test con múltiples conjuntos de datos.

```python
@pytest.mark.parametrize("input,expected", [(1, 1), (2, 4), (3, 9)])
def test_square(input, expected):
    assert square(input) == expected
```

### Patch

Decorador o context manager para reemplazar temporalmente objetos durante tests.

```python
from unittest.mock import patch

@patch("module.function")
def test_something(mock_func):
    mock_func.return_value = "mocked"
```

### pdb (Python Debugger)

Debugger interactivo incluido en la biblioteca estándar de Python.

---

## R

### Red-Green-Refactor

Ciclo de TDD: escribir test que falla (Red), hacer que pase (Green), mejorar código (Refactor).

### Regression Test

Test que verifica que funcionalidad existente sigue funcionando después de cambios.

---

## S

### Setup/Teardown

Código que se ejecuta antes (setup) y después (teardown) de los tests.

### Side Effect

Efecto secundario de una función, como modificar estado global o hacer I/O.

```python
mock.side_effect = [1, 2, 3]  # Retorna valores diferentes cada llamada
mock.side_effect = ValueError  # Lanza excepción
```

### Smoke Test

Test básico que verifica que el sistema funciona en su nivel más fundamental.

### Spy

Mock que registra cómo fue llamado mientras delega al objeto real.

### Stub

Objeto que retorna respuestas predefinidas sin lógica real.

---

## T

### TDD (Test-Driven Development)

Metodología donde se escriben los tests antes del código de producción.

### Test Double

Término genérico para objetos que reemplazan componentes reales en tests (mocks, stubs, spies).

### Test Isolation

Principio de que cada test debe ejecutarse independientemente de otros.

### Test Pyramid

Modelo que sugiere tener muchos unit tests, menos integration tests, y pocos E2E tests.

### Test Suite

Colección de tests que se ejecutan juntos.

---

## U

### Unit Test

Test que verifica una unidad pequeña de código (función, método, clase) de forma aislada.

---

## Y

### Yield Fixture

Fixture que usa `yield` para separar setup de teardown.

```python
@pytest.fixture
def resource():
    setup()
    yield get_resource()
    cleanup()
```

---

## Símbolos y Comandos

### pytest Commands

| Comando                 | Descripción                     |
| ----------------------- | ------------------------------- |
| `pytest`                | Ejecutar todos los tests        |
| `pytest -v`             | Modo verbose                    |
| `pytest -x`             | Parar al primer fallo           |
| `pytest -k "name"`      | Filtrar por nombre              |
| `pytest -m marker`      | Filtrar por marker              |
| `pytest --cov=src`      | Medir cobertura                 |

### pdb Commands

| Comando | Descripción                   |
| ------- | ----------------------------- |
| `n`     | Next line                     |
| `s`     | Step into                     |
| `c`     | Continue                      |
| `p`     | Print expression              |
| `l`     | List source                   |
| `q`     | Quit                          |
| `b`     | Set breakpoint                |
| `w`     | Where (stack trace)           |

### Log Levels

| Nivel      | Valor | Uso                         |
| ---------- | ----- | --------------------------- |
| `DEBUG`    | 10    | Información de diagnóstico  |
| `INFO`     | 20    | Confirmación de operaciones |
| `WARNING`  | 30    | Situaciones inesperadas     |
| `ERROR`    | 40    | Errores que afectan función |
| `CRITICAL` | 50    | Errores graves del sistema  |

---

> 📚 Este glosario cubre los términos principales de la Semana 13. Consulta la documentación oficial para definiciones más detalladas.
