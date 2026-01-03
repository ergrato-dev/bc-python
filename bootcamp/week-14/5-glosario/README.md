# 📖 Glosario - Semana 14: Proyecto Final Integrador

## A

### API (Application Programming Interface)
Interfaz que permite la comunicación entre diferentes sistemas de software. En este proyecto, usamos la API REST de OpenWeatherMap.

```python
# Ejemplo de llamada a API
response = requests.get("https://api.example.com/data")
```

### API Key
Clave de autenticación única que identifica al usuario/aplicación ante un servicio de API.

### argparse
Módulo estándar de Python para crear interfaces de línea de comandos (CLI) con parsing de argumentos.

```python
import argparse
parser = argparse.ArgumentParser(description="Mi CLI")
parser.add_argument("--name", help="Tu nombre")
```

### Arquitectura en Capas
Patrón de diseño que organiza el código en capas con responsabilidades específicas (presentación, servicios, datos).

---

## C

### CLI (Command Line Interface)
Interfaz de usuario basada en texto donde los comandos se escriben en una terminal.

### Clean Code
Código que es fácil de leer, entender y mantener. Sigue principios como nombres descriptivos, funciones pequeñas y SRP.

### Coverage (Cobertura)
Métrica que indica qué porcentaje del código es ejecutado por los tests.

```bash
pytest --cov=src --cov-report=term-missing
```

---

## D

### Dataclass
Decorador de Python que genera automáticamente métodos especiales para clases de datos.

```python
from dataclasses import dataclass

@dataclass
class Weather:
    city: str
    temperature: float
```

### Dependency Injection (DI)
Patrón donde las dependencias se pasan a un objeto en lugar de crearlas internamente.

```python
class WeatherService:
    def __init__(self, client: WeatherClient):  # Inyección
        self.client = client
```

### Docstring
Cadena de documentación que describe el propósito de un módulo, clase o función.

```python
def greet(name: str) -> str:
    """
    Saluda al usuario por nombre.

    Args:
        name: Nombre del usuario.

    Returns:
        Saludo personalizado.
    """
    return f"Hola, {name}!"
```

---

## E

### Endpoint
URL específica de una API que representa un recurso o acción.

```
GET /weather?q=Madrid  → Endpoint para clima actual
GET /forecast?q=Madrid → Endpoint para pronóstico
```

### Exception Handling
Manejo de errores usando bloques try/except para controlar excepciones.

```python
try:
    response = client.get_weather("Madrid")
except CityNotFoundError:
    print("Ciudad no encontrada")
```

---

## F

### Factory Function
Función que crea y retorna objetos, encapsulando la lógica de creación.

```python
def create_weather_service() -> WeatherService:
    client = WeatherClient()
    return WeatherService(client)
```

### Fixture (pytest)
Función que proporciona datos o configuración reutilizable para tests.

```python
@pytest.fixture
def sample_weather():
    return Weather(city="Madrid", temperature=22.5)
```

---

## H

### HTTP (HyperText Transfer Protocol)
Protocolo de comunicación usado para transferir datos en la web.

### HTTP Methods
- **GET**: Obtener datos
- **POST**: Crear datos
- **PUT**: Actualizar datos
- **DELETE**: Eliminar datos

### HTTP Status Codes
Códigos numéricos que indican el resultado de una petición:
- **200**: OK
- **401**: No autorizado
- **404**: No encontrado
- **429**: Rate limit excedido
- **500**: Error del servidor

---

## J

### JSON (JavaScript Object Notation)
Formato de intercambio de datos ligero y legible.

```json
{
  "city": "Madrid",
  "temperature": 22.5,
  "humidity": 45
}
```

---

## L

### Logging
Sistema para registrar eventos y mensajes durante la ejecución del programa.

```python
import logging
logger = logging.getLogger(__name__)
logger.info("Operación completada")
```

---

## M

### Mock
Objeto simulado que reemplaza dependencias reales en tests.

```python
from unittest.mock import Mock

mock_client = Mock()
mock_client.get_weather.return_value = {"temp": 22.5}
```

### Model
Clase que representa una entidad del dominio con sus datos y comportamiento.

---

## P

### Persistencia
Almacenamiento de datos de forma que sobrevivan al cierre del programa.

### Protocol (typing)
Define una interfaz estructural para type hints sin herencia explícita.

```python
from typing import Protocol

class StorageProtocol(Protocol):
    def load(self) -> list: ...
    def save(self, data: list) -> None: ...
```

---

## R

### Rate Limiting
Restricción en el número de peticiones permitidas a una API en un período de tiempo.

### REST (Representational State Transfer)
Estilo arquitectónico para diseñar APIs web usando HTTP.

### Requests
Librería Python para hacer peticiones HTTP de forma simple.

```python
import requests
response = requests.get("https://api.example.com/data")
data = response.json()
```

---

## S

### Service Layer
Capa que contiene la lógica de negocio, separada de la presentación y los datos.

### Session (requests)
Objeto que persiste configuración entre múltiples peticiones HTTP.

```python
session = requests.Session()
session.headers.update({"Authorization": "Bearer token"})
```

### SOLID Principles
Cinco principios de diseño orientado a objetos:
- **S**ingle Responsibility
- **O**pen/Closed
- **L**iskov Substitution
- **I**nterface Segregation
- **D**ependency Inversion

### SRP (Single Responsibility Principle)
Cada clase o módulo debe tener una única razón para cambiar.

---

## T

### Timeout
Tiempo máximo de espera para una operación (ej: petición HTTP).

```python
response = requests.get(url, timeout=10)  # 10 segundos
```

### Type Hints
Anotaciones que indican los tipos esperados de variables, parámetros y retornos.

```python
def get_weather(city: str) -> Weather:
    ...
```

---

## U

### Unit Test
Test que verifica el comportamiento de una unidad pequeña de código de forma aislada.

### URL Parameters
Datos enviados en la URL de una petición HTTP.

```
https://api.weather.com/weather?q=Madrid&units=metric
                                ↑ query parameters
```

---

## V

### Validation
Proceso de verificar que los datos cumplen con criterios específicos.

---

## Símbolos y Abreviaturas

| Símbolo | Significado |
|---------|-------------|
| `->` | Indica tipo de retorno |
| `|` | Union de tipos (ej: `str | None`) |
| `...` | Ellipsis (en Protocol indica método abstracto) |
| `**` | Desempaquetado de diccionario |
| `*` | Desempaquetado de lista/tupla |

---

*Última actualización: Enero 2026*
