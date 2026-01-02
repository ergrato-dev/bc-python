# 🎯 Proyecto Semana 11: Sistema de Logs y Análisis de Archivos

## 📋 Descripción

Desarrollarás un **sistema completo de procesamiento de logs** que demuestre dominio de:

- Lectura y escritura de archivos
- Manejo robusto de excepciones
- Context managers personalizados
- Generación de reportes

---

## 🎯 Objetivos

- Procesar archivos de log de diferentes formatos
- Implementar manejo robusto de errores
- Crear context managers para recursos
- Generar reportes en múltiples formatos (TXT, JSON, CSV)

---

## 📁 Estructura del Proyecto

```
3-proyecto/
├── README.md           ← Estás aquí
├── starter/
│   └── main.py         ← Código inicial con TODOs
└── solution/           ← ⚠️ Solo instructores
```

---

## 🔧 Requisitos Funcionales

### 1. Procesador de Logs

```python
class LogProcessor:
    """Procesa archivos de log y extrae información."""

    def process_file(self, path: str) -> list[LogEntry]
    def filter_by_level(self, level: str) -> list[LogEntry]
    def filter_by_date_range(self, start: datetime, end: datetime) -> list[LogEntry]
    def get_statistics(self) -> LogStatistics
```

### 2. Excepciones Personalizadas

```python
class LogError(Exception): ...
class LogParseError(LogError): ...
class LogFileError(LogError): ...
```

### 3. Context Managers

```python
class LogSession:
    """Context manager para sesión de procesamiento."""
    def __enter__(self) -> Self
    def __exit__(self, ...) -> bool

@contextmanager
def log_transaction(processor: LogProcessor) -> Iterator[None]
```

### 4. Generador de Reportes

```python
class ReportGenerator:
    """Genera reportes en diferentes formatos."""

    def generate_text(self, path: str) -> None
    def generate_json(self, path: str) -> None
    def generate_csv(self, path: str) -> None
```

---

## 📝 Tareas

### Tarea 1: Modelo de Datos (10 pts)

Implementa las dataclasses para representar logs:

- `LogEntry`: timestamp, level, logger, message
- `LogStatistics`: total, por nivel, errores

### Tarea 2: Excepciones (10 pts)

Crea jerarquía de excepciones:

- `LogError` (base)
- `LogParseError` (línea inválida)
- `LogFileError` (archivo no encontrado, permisos)

### Tarea 3: LogProcessor (25 pts)

Implementa el procesador principal:

- Lectura de archivos con encoding correcto
- Parseo de líneas de log
- Filtros por nivel y fecha
- Cálculo de estadísticas

### Tarea 4: Context Managers (25 pts)

Implementa:

- `LogSession`: gestiona sesión de procesamiento
- `log_transaction`: rollback en caso de error
- `atomic_write`: escritura atómica de reportes

### Tarea 5: ReportGenerator (20 pts)

Genera reportes en:

- Texto plano (.txt)
- JSON (.json)
- CSV (.csv)

### Tarea 6: Integración (10 pts)

- Función `main()` que demuestre todo el sistema
- Manejo de errores de línea de comandos
- Logging apropiado

---

## 📊 Formato de Log de Entrada

```
2024-01-15 10:30:45 - INFO - app.main - Application started
2024-01-15 10:30:46 - DEBUG - app.db - Connecting to database
2024-01-15 10:30:47 - ERROR - app.api - Failed to fetch data: timeout
2024-01-15 10:31:00 - WARNING - app.cache - Cache miss for key: user_123
```

---

## 📄 Formato de Reportes

### Texto (.txt)

```
=== LOG ANALYSIS REPORT ===
Generated: 2024-01-15 12:00:00

SUMMARY
-------
Total entries: 1,234
Date range: 2024-01-15 to 2024-01-15

BY LEVEL
--------
INFO: 800 (64.8%)
DEBUG: 300 (24.3%)
WARNING: 100 (8.1%)
ERROR: 34 (2.8%)
```

### JSON (.json)

```json
{
  "generated_at": "2024-01-15T12:00:00",
  "summary": {
    "total_entries": 1234,
    "date_range": {"start": "2024-01-15", "end": "2024-01-15"}
  },
  "by_level": {
    "INFO": 800,
    "DEBUG": 300,
    "WARNING": 100,
    "ERROR": 34
  }
}
```

---

## ✅ Criterios de Evaluación

| Criterio | Puntos |
|----------|--------|
| Modelo de datos correcto | 10 |
| Excepciones bien diseñadas | 10 |
| LogProcessor funcional | 25 |
| Context managers correctos | 25 |
| Reportes generados | 20 |
| Integración y código limpio | 10 |
| **Total** | **100** |

---

## 🚀 Ejecución

```bash
cd bootcamp/week-11/3-proyecto/starter
python main.py
```

---

## 💡 Consejos

1. **Empieza por las dataclasses** - Define bien tu modelo
2. **Usa type hints** en todo el código
3. **No silencies excepciones** - Al menos loguéalas
4. **Siempre usa `with`** para archivos
5. **Testea con archivos pequeños** primero
