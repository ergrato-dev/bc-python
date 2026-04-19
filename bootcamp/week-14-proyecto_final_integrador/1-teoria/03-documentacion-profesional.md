# 📝 Documentación Profesional

## 🎯 Objetivos

- Escribir docstrings siguiendo estándares de la industria
- Crear READMEs efectivos y completos
- Usar type hints avanzados para documentar tipos
- Generar documentación automática

---

## 1. Docstrings: Documentando Código

### 1.1 ¿Por Qué Documentar?

```python
# ❌ Sin documentación: ¿Qué hace? ¿Qué parámetros acepta?
def process(d, t, m=False):
    if m:
        return d * t
    return d + t

# ✅ Con documentación: Claro y mantenible
def calculate_price(base_price: float, tax_rate: float, apply_discount: bool = False) -> float:
    """
    Calcula el precio final aplicando impuestos y descuentos.

    Args:
        base_price: Precio base del producto en euros
        tax_rate: Tasa de impuesto (ej: 0.21 para 21%)
        apply_discount: Si True, aplica 10% de descuento

    Returns:
        Precio final con impuestos y descuento aplicados

    Example:
        >>> calculate_price(100, 0.21)
        121.0
        >>> calculate_price(100, 0.21, apply_discount=True)
        108.9
    """
    price_with_tax = base_price * (1 + tax_rate)
    if apply_discount:
        return price_with_tax * 0.9
    return price_with_tax
```

### 1.2 Estilos de Docstrings

#### Google Style (Recomendado)

```python
def fetch_weather(city: str, units: str = "metric") -> dict:
    """
    Obtiene datos meteorológicos de una ciudad.

    Realiza una petición a la API de OpenWeatherMap y retorna
    los datos del clima actual.

    Args:
        city: Nombre de la ciudad (puede incluir país: "Madrid,ES")
        units: Sistema de unidades ("metric", "imperial", "kelvin")

    Returns:
        Diccionario con datos del clima incluyendo temperatura,
        humedad, viento y condición.

    Raises:
        CityNotFoundError: Si la ciudad no existe en la API
        APIError: Si hay problemas de conexión o autenticación

    Example:
        >>> client = WeatherClient(api_key="xxx")
        >>> weather = client.fetch_weather("Barcelona")
        >>> print(weather["temperature"])
        22.5

    Note:
        Requiere una API key válida de OpenWeatherMap.
        La API tiene límite de 60 requests por minuto en plan gratuito.
    """
    pass
```

#### NumPy Style

```python
def calculate_statistics(data: list[float]) -> dict[str, float]:
    """
    Calcula estadísticas descriptivas de una lista de números.

    Parameters
    ----------
    data : list[float]
        Lista de valores numéricos a analizar.
        Debe contener al menos un elemento.

    Returns
    -------
    dict[str, float]
        Diccionario con las siguientes claves:
        - mean: Media aritmética
        - std: Desviación estándar
        - min: Valor mínimo
        - max: Valor máximo

    Raises
    ------
    ValueError
        Si la lista está vacía.

    Examples
    --------
    >>> calculate_statistics([1, 2, 3, 4, 5])
    {'mean': 3.0, 'std': 1.41, 'min': 1, 'max': 5}
    """
    pass
```

### 1.3 Documentando Clases

```python
class WeatherService:
    """
    Servicio para gestionar consultas meteorológicas.

    Proporciona una interfaz de alto nivel para obtener información
    del clima, gestionar favoritos e historial de búsquedas.

    Attributes:
        client: Cliente HTTP para comunicación con API
        favorites: Servicio de gestión de favoritos
        history: Servicio de gestión de historial

    Example:
        >>> service = WeatherService.create_default()
        >>> weather = service.get_current_weather("Madrid")
        >>> print(f"Temperatura: {weather.temperature}°C")
        Temperatura: 22.5°C
    """

    def __init__(
        self,
        client: WeatherClient,
        favorites: FavoritesService,
        history: HistoryService,
    ) -> None:
        """
        Inicializa el servicio con sus dependencias.

        Args:
            client: Cliente para comunicación con API de clima
            favorites: Servicio de persistencia de favoritos
            history: Servicio de persistencia de historial
        """
        self.client = client
        self.favorites = favorites
        self.history = history

    @classmethod
    def create_default(cls, config: Config) -> "WeatherService":
        """
        Factory method para crear un servicio con configuración estándar.

        Args:
            config: Configuración de la aplicación

        Returns:
            Instancia de WeatherService completamente configurada
        """
        pass
```

### 1.4 Documentando Módulos

```python
# src/api/weather_client.py
"""
Cliente HTTP para la API de OpenWeatherMap.

Este módulo proporciona la clase WeatherClient para interactuar
con la API de OpenWeatherMap, incluyendo manejo de errores,
reintentos automáticos y logging.

Example:
    >>> from src.api import WeatherClient
    >>>
    >>> with WeatherClient(api_key="xxx") as client:
    ...     weather = client.get_current_weather("Madrid")
    ...     print(weather.temperature)

Attributes:
    DEFAULT_BASE_URL (str): URL base de la API
    DEFAULT_TIMEOUT (int): Timeout por defecto en segundos

Note:
    Requiere la librería `requests` instalada.
"""

DEFAULT_BASE_URL = "https://api.openweathermap.org/data/2.5"
DEFAULT_TIMEOUT = 10


class WeatherClient:
    ...
```

---

## 2. Type Hints Avanzados

### 2.1 Tipos Básicos y Genéricos

```python
from typing import Any
from collections.abc import Callable, Iterator, Sequence

# Tipos básicos
name: str = "Weather"
count: int = 42
price: float = 19.99
active: bool = True

# Colecciones (Python 3.9+)
cities: list[str] = ["Madrid", "Barcelona"]
temps: dict[str, float] = {"Madrid": 22.5, "Barcelona": 24.0}
coords: tuple[float, float] = (40.4168, -3.7038)
unique_cities: set[str] = {"Madrid", "Barcelona"}

# Opcionales y Uniones (Python 3.10+)
maybe_temp: float | None = None
id_or_name: int | str = "Madrid"

# Callable
processor: Callable[[str], dict] = process_city
handler: Callable[[int, int], float] = lambda x, y: x / y
```

### 2.2 TypedDict para Estructuras

```python
from typing import TypedDict, NotRequired


class WeatherData(TypedDict):
    """Estructura de datos del clima desde API."""
    city: str
    temperature: float
    humidity: int
    description: str
    wind_speed: NotRequired[float]  # Campo opcional


def process_weather(data: WeatherData) -> str:
    """Procesa datos con estructura conocida."""
    return f"{data['city']}: {data['temperature']}°C"


# El IDE autocompleta los campos
weather: WeatherData = {
    "city": "Madrid",
    "temperature": 22.5,
    "humidity": 45,
    "description": "Soleado",
}
```

### 2.3 Protocols para Duck Typing

```python
from typing import Protocol


class Storable(Protocol):
    """Protocolo para objetos que se pueden almacenar."""

    def to_dict(self) -> dict: ...

    @classmethod
    def from_dict(cls, data: dict) -> "Storable": ...


class JsonStorage:
    """Almacenamiento que acepta cualquier Storable."""

    def save(self, key: str, item: Storable) -> None:
        """Guarda un objeto que implemente Storable."""
        data = item.to_dict()
        self._write(key, data)


# Weather implementa el protocolo (sin heredar explícitamente)
@dataclass
class Weather:
    city: str
    temperature: float

    def to_dict(self) -> dict:
        return {"city": self.city, "temperature": self.temperature}

    @classmethod
    def from_dict(cls, data: dict) -> "Weather":
        return cls(city=data["city"], temperature=data["temperature"])


# Funciona porque Weather cumple el Protocol
storage = JsonStorage()
storage.save("madrid", Weather("Madrid", 22.5))  # ✅ OK
```

### 2.4 Type Aliases

```python
from typing import TypeAlias

# Alias simples
CityName: TypeAlias = str
Temperature: TypeAlias = float
Coordinates: TypeAlias = tuple[float, float]

# Alias complejos
WeatherCallback: TypeAlias = Callable[[Weather], None]
CityWeatherMap: TypeAlias = dict[CityName, Weather]
ForecastList: TypeAlias = list[Forecast]

# Uso
def get_temperatures(cities: list[CityName]) -> dict[CityName, Temperature]:
    """Obtiene temperaturas para múltiples ciudades."""
    pass

def on_weather_update(callback: WeatherCallback) -> None:
    """Registra callback para actualizaciones."""
    pass
```

---

## 3. README Profesional

### 3.1 Estructura Recomendada

```markdown
# 🌤️ Weather Dashboard CLI

[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://python.org)
[![Tests](https://img.shields.io/badge/tests-passing-green.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-92%25-green.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> Aplicación de línea de comandos para consultar el clima mundial.

![Demo](docs/demo.gif)

## ✨ Características

- 🌡️ Clima actual de cualquier ciudad del mundo
- 📊 Pronóstico de 5 días
- ⭐ Sistema de ciudades favoritas
- 📈 Historial de búsquedas
- 🎨 Interfaz colorida y amigable

## 🚀 Instalación

### Requisitos

- Python 3.13 o superior
- [uv](https://docs.astral.sh/uv/) (gestor de paquetes)

### Pasos

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/weather-dashboard.git
   cd weather-dashboard
   ```

2. Instala dependencias:
   ```bash
   uv sync
   ```

3. Configura tu API key:
   ```bash
   cp .env.example .env
   # Edita .env y añade tu OPENWEATHER_API_KEY
   ```

4. (Opcional) Obtén tu API key gratuita en:
   [OpenWeatherMap](https://openweathermap.org/api)

## 📖 Uso

### Clima actual

```bash
# Consultar clima de una ciudad
uv run python -m src.main weather Madrid

# Con código de país
uv run python -m src.main weather "London,UK"
```

### Pronóstico

```bash
# Pronóstico de 5 días
uv run python -m src.main forecast Barcelona
```

### Favoritos

```bash
# Añadir a favoritos
uv run python -m src.main favorites add Madrid

# Listar favoritos
uv run python -m src.main favorites list

# Ver clima de todos los favoritos
uv run python -m src.main favorites weather
```

### Historial

```bash
# Ver últimas búsquedas
uv run python -m src.main history

# Limpiar historial
uv run python -m src.main history clear
```

## 🏗️ Arquitectura

```
src/
├── api/           # Comunicación con API externa
├── models/        # Modelos de datos
├── services/      # Lógica de negocio
├── storage/       # Persistencia (JSON)
└── utils/         # Utilidades y configuración
```

## 🧪 Testing

```bash
# Ejecutar tests
uv run pytest

# Con cobertura
uv run pytest --cov=src --cov-report=html
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu rama (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- [OpenWeatherMap](https://openweathermap.org/) por la API gratuita
- Bootcamp Python Zero to Hero
```

### 3.2 Badges Útiles

```markdown
<!-- Estado del build -->
[![Build Status](https://github.com/user/repo/actions/workflows/ci.yml/badge.svg)]()

<!-- Cobertura -->
[![codecov](https://codecov.io/gh/user/repo/branch/main/graph/badge.svg)]()

<!-- Versión de Python -->
[![Python Version](https://img.shields.io/pypi/pyversions/package.svg)]()

<!-- Licencia -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

<!-- Estilo de código -->
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)]()
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)]()
```

---

## 4. Changelog y Versionado

### 4.1 Semantic Versioning

```
MAJOR.MINOR.PATCH

MAJOR: Cambios incompatibles con versiones anteriores
MINOR: Nueva funcionalidad compatible hacia atrás
PATCH: Corrección de bugs compatible hacia atrás

Ejemplos:
1.0.0 → Primera versión estable
1.1.0 → Nueva feature (agregar favoritos)
1.1.1 → Bug fix (corregir parsing de temperatura)
2.0.0 → Breaking change (nueva estructura de config)
```

### 4.2 Formato de CHANGELOG

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Soporte para múltiples idiomas

## [1.1.0] - 2026-01-15

### Added
- Sistema de ciudades favoritas
- Exportación de historial a CSV

### Changed
- Mejorado el formato de salida del pronóstico

### Fixed
- Corregido error al buscar ciudades con caracteres especiales

## [1.0.0] - 2026-01-01

### Added
- Consulta de clima actual
- Pronóstico de 5 días
- Historial de búsquedas
- Interfaz CLI con colores
```

---

## 5. Comentarios Efectivos

### 5.1 Cuándo Comentar

```python
# ✅ Comentar el "por qué", no el "qué"
# Usamos cache de 5 minutos porque la API tiene límite de 60 req/min
@lru_cache(maxsize=100, ttl=300)
def get_weather(city: str) -> Weather:
    return client.fetch(city)

# ✅ Explicar decisiones no obvias
# Redondeamos a 1 decimal porque la API a veces devuelve
# valores como 22.456789 que confunden al usuario
temperature = round(data["temp"], 1)

# ✅ Advertir sobre comportamiento especial
# IMPORTANTE: Esta función modifica el diccionario in-place
# para evitar copias innecesarias en datasets grandes
def normalize_temperatures(data: dict) -> None:
    pass

# ❌ NO comentar lo obvio
# Incrementa el contador  ← MALO
counter += 1

# Obtiene el usuario por ID  ← MALO
user = get_user_by_id(user_id)
```

### 5.2 TODOs y FIXMEs

```python
# TODO: Implementar cache con Redis para producción
# TODO(juan): Añadir soporte para coordenadas GPS
# FIXME: Este cálculo falla con temperaturas negativas
# HACK: Workaround temporal hasta que la API arregle el bug
# NOTE: Este endpoint requiere autenticación premium
# DEPRECATED: Usar get_weather_v2() en su lugar
```

---

## ✅ Checklist de Documentación

- [ ] Todas las funciones públicas tienen docstrings
- [ ] Docstrings siguen un estilo consistente (Google/NumPy)
- [ ] Type hints en todas las funciones y métodos
- [ ] README completo con instalación, uso y ejemplos
- [ ] CHANGELOG actualizado
- [ ] Comentarios explican el "por qué", no el "qué"
- [ ] Ejemplos de código son ejecutables
- [ ] .env.example documenta variables necesarias

---

## 📚 Recursos Adicionales

- [Google Python Style Guide - Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [Make a README](https://www.makeareadme.com/)
- [Keep a Changelog](https://keepachangelog.com/)
