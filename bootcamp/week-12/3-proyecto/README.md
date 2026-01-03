# 🚀 Proyecto Semana 12: Sistema de Procesamiento de Logs

## 📋 Descripción

Desarrollarás un **Sistema de Procesamiento de Logs** que combina decoradores, generadores y expresiones regulares para analizar archivos de log de forma eficiente.

El sistema procesará logs de aplicaciones web, extrayendo métricas, detectando errores y generando reportes.

---

## 🎯 Objetivos de Aprendizaje

- ✅ Crear decoradores para timing, retry y caching
- ✅ Implementar generadores para procesar archivos grandes
- ✅ Usar regex para parsear entradas de log
- ✅ Construir pipelines de procesamiento eficientes
- ✅ Aplicar patrones de diseño con clases

---

## 📁 Estructura del Proyecto

```
3-proyecto/
├── README.md           # Este archivo
├── starter/
│   └── main.py         # Código inicial (implementar TODOs)
└── solution/
    └── main.py         # Solución completa (oculta)
```

---

## 📝 Formato de Logs

El sistema procesa logs con el siguiente formato:

```
[2024-01-15 10:30:45] INFO: User login successful - user_id=123
[2024-01-15 10:30:46] WARNING: High memory usage - 85%
[2024-01-15 10:30:47] ERROR: Database connection failed - timeout=30s
[2024-01-15 10:30:48] DEBUG: Cache hit for key=user_123
```

**Componentes:**
- `[YYYY-MM-DD HH:MM:SS]` - Timestamp
- `LEVEL` - Nivel: DEBUG, INFO, WARNING, ERROR, CRITICAL
- `message` - Mensaje con posibles key=value

---

## 🔧 Requisitos Funcionales

### 1. Decoradores (30 puntos)

| Decorador | Función |
|-----------|---------|
| `@timer` | Mide tiempo de ejecución |
| `@retry(n)` | Reintenta n veces si falla |
| `@cache` | Cachea resultados por argumentos |
| `@log_calls` | Registra llamadas a funciones |

### 2. Generadores (30 puntos)

| Generador | Función |
|-----------|---------|
| `read_logs(path)` | Lee archivo línea por línea |
| `parse_entries(lines)` | Parsea cada línea a LogEntry |
| `filter_by_level(entries, level)` | Filtra por nivel |
| `extract_metrics(entries)` | Extrae métricas numéricas |

### 3. Expresiones Regulares (20 puntos)

| Patrón | Uso |
|--------|-----|
| `LOG_PATTERN` | Parsear línea completa |
| `KEY_VALUE_PATTERN` | Extraer key=value |
| `IP_PATTERN` | Detectar direcciones IP |
| `ERROR_CODE_PATTERN` | Extraer códigos de error |

### 4. Análisis y Reportes (20 puntos)

| Función | Descripción |
|---------|-------------|
| `count_by_level()` | Cuenta logs por nivel |
| `errors_per_hour()` | Agrupa errores por hora |
| `top_errors()` | Top N errores más frecuentes |
| `generate_report()` | Genera reporte completo |

---

## 📊 Ejemplo de Uso

```python
# Procesar archivo de logs
analyzer = LogAnalyzer("server.log")

# Pipeline de procesamiento
pipeline = analyzer.create_pipeline(
    min_level="WARNING",
    start_date="2024-01-15",
    end_date="2024-01-16"
)

# Generar reporte
report = analyzer.generate_report(pipeline)
print(report)
```

**Salida esperada:**

```
================================================================================
                            LOG ANALYSIS REPORT
================================================================================

📅 Period: 2024-01-15 to 2024-01-16
📊 Total entries analyzed: 1,234

📈 ENTRIES BY LEVEL:
  WARNING  : ████████████████████ 456 (37.0%)
  ERROR    : ██████████████ 312 (25.3%)
  CRITICAL : ████ 89 (7.2%)

⚠️ TOP 5 ERRORS:
  1. Database connection failed (145 occurrences)
  2. Authentication timeout (87 occurrences)
  3. File not found (43 occurrences)
  4. Memory limit exceeded (25 occurrences)
  5. Invalid request format (12 occurrences)

⏰ ERRORS BY HOUR:
  10:00 - 11:00 : ████████████ 124
  11:00 - 12:00 : ████████ 89
  14:00 - 15:00 : ██████████████████ 178

================================================================================
```

---

## 🚀 Instrucciones

### Paso 1: Implementar Decoradores

Abre `starter/main.py` y completa los decoradores:

```python
def timer(func):
    # TODO: Implementar medición de tiempo
    pass

def retry(max_attempts=3, delay=1.0):
    # TODO: Implementar reintentos
    pass
```

### Paso 2: Implementar Generadores

Completa los generadores para procesamiento lazy:

```python
def read_logs(filepath: str) -> Iterator[str]:
    # TODO: Leer archivo línea por línea
    pass

def parse_entries(lines: Iterator[str]) -> Iterator[LogEntry]:
    # TODO: Parsear cada línea
    pass
```

### Paso 3: Implementar Patrones Regex

Define los patrones para parsear logs:

```python
LOG_PATTERN = re.compile(r"...")  # TODO: Definir patrón
KEY_VALUE_PATTERN = re.compile(r"...")  # TODO: Definir patrón
```

### Paso 4: Implementar LogAnalyzer

Completa la clase principal:

```python
class LogAnalyzer:
    def create_pipeline(self, ...):
        # TODO: Crear pipeline de generadores
        pass

    def generate_report(self, ...):
        # TODO: Generar reporte formateado
        pass
```

---

## ✅ Criterios de Evaluación

| Criterio | Puntos |
|----------|--------|
| Decoradores funcionan correctamente | 30 |
| Generadores procesan eficientemente | 30 |
| Regex parsean correctamente | 20 |
| Reportes completos y formateados | 20 |
| **Total** | **100** |

---

## 🧪 Testing

Ejecuta el archivo para probar con datos de ejemplo:

```bash
cd starter
python main.py
```

El archivo incluye datos de prueba generados automáticamente.

---

## 📚 Recursos

- [re — Regular expression operations](https://docs.python.org/3/library/re.html)
- [Generators - Python Wiki](https://wiki.python.org/moin/Generators)
- [PEP 318 – Decorators](https://peps.python.org/pep-0318/)

---

## 💡 Tips

1. **Decoradores**: Siempre usa `@functools.wraps` para preservar metadata
2. **Generadores**: Usa `yield from` para delegar a otros iteradores
3. **Regex**: Compila patrones con `re.compile()` para mejor rendimiento
4. **Testing**: Prueba cada componente por separado antes de integrar
