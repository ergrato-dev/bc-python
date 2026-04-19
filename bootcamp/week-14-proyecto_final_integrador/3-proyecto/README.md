# 🌤️ Proyecto Final: Weather Dashboard CLI

## 📋 Descripción

Desarrolla una **aplicación de línea de comandos** que consume la API de OpenWeatherMap para mostrar información meteorológica de cualquier ciudad del mundo.

Este proyecto integra todos los conceptos aprendidos durante el bootcamp:
- Programación orientada a objetos
- Consumo de APIs REST
- Manejo de archivos y persistencia
- Testing con pytest
- Logging y manejo de errores
- Documentación profesional

---

## 🎯 Objetivos

Al completar este proyecto serás capaz de:

- ✅ Diseñar y estructurar un proyecto Python profesional
- ✅ Consumir APIs REST con la librería `requests`
- ✅ Implementar persistencia de datos con JSON
- ✅ Escribir tests con mocking de servicios externos
- ✅ Crear una interfaz CLI amigable
- ✅ Documentar código siguiendo estándares

---

## 📦 Funcionalidades Requeridas

### 1. Clima Actual (Obligatorio)

```bash
# Consultar clima de una ciudad
weather-cli weather Madrid

# Output esperado:
🌤️ Clima actual en Madrid, ES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌡️  Temperatura: 22.5°C (sensación: 21.8°C)
💧 Humedad: 45%
💨 Viento: 3.5 m/s
☁️  Condición: Cielo despejado

Última actualización: 2026-01-02 15:30
```

### 2. Pronóstico 5 Días (Obligatorio)

```bash
weather-cli forecast Barcelona

# Output esperado:
📊 Pronóstico 5 días - Barcelona, ES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 Lunes 03/01
   🌡️ 18°C - 24°C | ☀️ Soleado

📅 Martes 04/01
   🌡️ 16°C - 22°C | ⛅ Parcialmente nublado

📅 Miércoles 05/01
   🌡️ 14°C - 19°C | 🌧️ Lluvia ligera

...
```

### 3. Ciudades Favoritas (Obligatorio)

```bash
# Añadir favorito
weather-cli favorites add Madrid
✅ Madrid añadida a favoritos

# Listar favoritos
weather-cli favorites list
⭐ Ciudades favoritas:
  1. Madrid
  2. Barcelona
  3. London,UK

# Eliminar favorito
weather-cli favorites remove Barcelona
🗑️ Barcelona eliminada de favoritos

# Ver clima de todos los favoritos
weather-cli favorites weather
```

### 4. Historial de Búsquedas (Obligatorio)

```bash
# Ver historial
weather-cli history
📈 Historial de búsquedas (últimas 10):

  1. Madrid       | 2026-01-02 15:30 | 22.5°C
  2. Barcelona    | 2026-01-02 14:15 | 24.0°C
  3. London,UK    | 2026-01-02 12:00 | 8.5°C

# Limpiar historial
weather-cli history clear
🗑️ Historial limpiado
```

### 5. Manejo de Errores (Obligatorio)

```bash
# Ciudad no encontrada
weather-cli weather CiudadInventada123
❌ Error: Ciudad "CiudadInventada123" no encontrada.
💡 Sugerencia: Verifica el nombre o usa formato "Ciudad,País"

# Sin conexión
weather-cli weather Madrid
❌ Error: No se pudo conectar al servicio de clima.
💡 Sugerencia: Verifica tu conexión a internet.

# API key inválida
weather-cli weather Madrid
❌ Error: API key inválida o no configurada.
💡 Sugerencia: Configura OPENWEATHER_API_KEY en tu archivo .env
```

---

## 🏗️ Arquitectura Requerida

```
weather-dashboard/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Punto de entrada
│   ├── cli.py                  # Comandos CLI
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── client.py           # Cliente HTTP
│   │   └── exceptions.py       # Excepciones de API
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── weather.py          # Modelo Weather
│   │   └── forecast.py         # Modelo Forecast
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── weather_service.py  # Lógica de clima
│   │   ├── favorites_service.py
│   │   └── history_service.py
│   │
│   ├── storage/
│   │   ├── __init__.py
│   │   └── json_storage.py     # Persistencia JSON
│   │
│   └── utils/
│       ├── __init__.py
│       ├── config.py           # Configuración
│       └── display.py          # Formateo de salida
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Fixtures
│   ├── test_client.py
│   ├── test_services.py
│   ├── test_storage.py
│   └── test_models.py
│
├── data/
│   ├── favorites.json
│   └── history.json
│
├── pyproject.toml
├── README.md
├── .env.example
└── .gitignore
```

---

## 🔧 Requisitos Técnicos

### Dependencias

```toml
# pyproject.toml
[project]
requires-python = ">=3.13"
dependencies = [
    "requests>=2.31.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
]
```

### Configuración

```bash
# .env.example
OPENWEATHER_API_KEY=tu_api_key_aqui
API_TIMEOUT=10
LOG_LEVEL=INFO
DATA_DIR=data
```

### API de OpenWeatherMap

- **Registro**: https://openweathermap.org/api
- **Plan gratuito**: 60 requests/minuto, 1,000,000 requests/mes
- **Endpoints a usar**:
  - `/weather` - Clima actual
  - `/forecast` - Pronóstico 5 días (cada 3 horas)

---

## ✅ Criterios de Evaluación

### Funcionalidad (30 puntos)

| Criterio | Puntos |
|----------|--------|
| Clima actual funciona correctamente | 8 |
| Pronóstico 5 días funciona | 8 |
| CRUD de favoritos completo | 7 |
| Historial con persistencia | 7 |

### Calidad del Código (25 puntos)

| Criterio | Puntos |
|----------|--------|
| Type hints completos | 7 |
| Arquitectura en capas | 8 |
| Código limpio (DRY, SRP) | 5 |
| Manejo de errores robusto | 5 |

### Testing (20 puntos)

| Criterio | Puntos |
|----------|--------|
| Cobertura >85% | 8 |
| Tests unitarios con mocks | 7 |
| Calidad de tests (AAA, edge cases) | 5 |

### Documentación (15 puntos)

| Criterio | Puntos |
|----------|--------|
| README completo | 5 |
| Docstrings en funciones públicas | 5 |
| Comentarios útiles | 3 |
| .env.example documentado | 2 |

### Presentación (10 puntos)

| Criterio | Puntos |
|----------|--------|
| Demo funcional | 4 |
| Explicación técnica clara | 3 |
| Respuesta a preguntas | 3 |

**Total: 100 puntos**
**Mínimo para aprobar: 70 puntos**

---

## 🌟 Puntos Extra (hasta 20)

| Feature | Puntos |
|---------|--------|
| Cache de respuestas (TTL) | +5 |
| Exportación a CSV | +3 |
| Gráficos ASCII del pronóstico | +4 |
| Colores en terminal (colorama/rich) | +3 |
| Docker + docker-compose | +5 |

---

## 📝 Instrucciones de Entrega

1. **Fork** el repositorio del bootcamp
2. Desarrolla en la carpeta `bootcamp/week-14/3-proyecto/`
3. Asegúrate de que los tests pasen:
   ```bash
   uv run pytest --cov=src --cov-report=term-missing
   ```
4. Crea un **Pull Request** con tu solución
5. Prepara tu **presentación** (10 minutos)

---

## 💡 Consejos

1. **Empieza por los modelos**: Define `Weather` y `Forecast` primero
2. **Luego el cliente API**: Implementa la comunicación con OpenWeatherMap
3. **Después los servicios**: Construye la lógica sobre el cliente
4. **Storage en paralelo**: La persistencia JSON es independiente
5. **CLI al final**: Una vez que los servicios funcionan, crea la interfaz
6. **Tests durante el desarrollo**: No los dejes para el final

---

## 🔗 Recursos

- [OpenWeatherMap API Docs](https://openweathermap.org/api)
- [Requests Documentation](https://docs.python-requests.org/)
- [Click Documentation](https://click.palletsprojects.com/) (opcional para CLI)
- [Rich Library](https://rich.readthedocs.io/) (opcional para formato)

---

¡Buena suerte! 🍀🐍
