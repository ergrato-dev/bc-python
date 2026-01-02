# 🔌 Proyecto: Sistema de Procesamiento de Datos

## 🎯 Objetivo

Crear un **framework de procesamiento de datos extensible** que combine todos los conceptos de la semana: clases abstractas, Protocols, módulos organizados y estructura de paquete distribuible.

---

## 📋 Descripción

Construirás un sistema que:

1. **Define abstracciones** con ABC y Protocols para procesadores y fuentes de datos
2. **Implementa plugins** concretos para diferentes formatos (CSV, JSON)
3. **Organiza código** en módulos bien estructurados
4. **Configura paquete** con pyproject.toml y entry points
5. **Usa inyección de dependencias** para flexibilidad y testing

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    DataPipeline                              │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │  Source  │───▶│  Processor   │───▶│    Output    │       │
│  │(Protocol)│    │    (ABC)     │    │  (Protocol)  │       │
│  └──────────┘    └──────────────┘    └──────────────┘       │
│       │                │                    │                │
│       ▼                ▼                    ▼                │
│  ┌─────────┐    ┌─────────────┐     ┌─────────────┐         │
│  │CSVSource│    │FilterProc   │     │ConsoleOutput│         │
│  │JSONSource│   │TransformProc│     │FileOutput   │         │
│  │APISource│    │AggregateProc│     │JSONOutput   │         │
│  └─────────┘    └─────────────┘     └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Estructura del Proyecto

```
data-processor/
├── pyproject.toml
├── README.md
├── src/
│   └── data_processor/
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── interfaces.py      # Protocols y ABC
│       │   ├── pipeline.py        # DataPipeline
│       │   └── registry.py        # PluginRegistry
│       ├── sources/
│       │   ├── __init__.py
│       │   ├── csv_source.py
│       │   ├── json_source.py
│       │   └── memory_source.py
│       ├── processors/
│       │   ├── __init__.py
│       │   ├── filter.py
│       │   ├── transform.py
│       │   └── aggregate.py
│       ├── outputs/
│       │   ├── __init__.py
│       │   ├── console.py
│       │   └── file.py
│       └── cli.py
└── tests/
    ├── __init__.py
    ├── test_pipeline.py
    ├── test_processors.py
    └── test_sources.py
```

---

## 🚀 Instrucciones

### Paso 1: Crear Estructura Base

```bash
cd starter
mkdir -p src/data_processor/{core,sources,processors,outputs}
mkdir -p tests
touch pyproject.toml README.md
```

### Paso 2: Implementar Interfaces (core/interfaces.py)

Define las abstracciones base:
- `DataSource` (Protocol): Fuente de datos
- `DataProcessor` (ABC): Procesador con lógica compartida
- `DataOutput` (Protocol): Salida de datos

### Paso 3: Implementar Sources

Crea fuentes de datos:
- `MemorySource`: Datos en memoria
- `CSVSource`: Lee archivos CSV
- `JSONSource`: Lee archivos JSON

### Paso 4: Implementar Processors

Crea procesadores:
- `FilterProcessor`: Filtra por condición
- `TransformProcessor`: Transforma campos
- `AggregateProcessor`: Agrega datos

### Paso 5: Implementar Outputs

Crea salidas:
- `ConsoleOutput`: Imprime en consola
- `FileOutput`: Escribe a archivo

### Paso 6: Crear Pipeline

Implementa `DataPipeline` que conecta source → processors → output.

### Paso 7: Configurar CLI

Crea comandos para ejecutar pipelines desde terminal.

---

## ✅ Requisitos de Entrega

### Funcionalidad (60 puntos)

| Requisito | Puntos |
|-----------|--------|
| `DataProcessor` ABC con al menos 1 método abstracto | 10 |
| `DataSource` y `DataOutput` como Protocols | 10 |
| Al menos 3 procesadores concretos funcionando | 15 |
| Al menos 2 fuentes de datos | 10 |
| Pipeline encadenando múltiples procesadores | 15 |

### Estructura (25 puntos)

| Requisito | Puntos |
|-----------|--------|
| Estructura src/ layout correcta | 5 |
| pyproject.toml con metadata completa | 5 |
| Imports organizados (relativos/absolutos) | 5 |
| `__init__.py` con exports públicos | 5 |
| Entry point CLI configurado | 5 |

### Calidad (15 puntos)

| Requisito | Puntos |
|-----------|--------|
| Type hints en todas las funciones públicas | 5 |
| Docstrings en clases y métodos | 5 |
| Tests con pytest (mínimo 5) | 5 |

---

## 💡 Ejemplo de Uso

```python
from data_processor import DataPipeline
from data_processor.sources import MemorySource
from data_processor.processors import FilterProcessor, TransformProcessor
from data_processor.outputs import ConsoleOutput

# Datos de ejemplo
data = [
    {"name": "Alice", "age": 30, "city": "NYC"},
    {"name": "Bob", "age": 25, "city": "LA"},
    {"name": "Charlie", "age": 35, "city": "NYC"},
]

# Crear pipeline
pipeline = DataPipeline(
    source=MemorySource(data),
    processors=[
        FilterProcessor(key="city", value="NYC"),
        TransformProcessor(key="name", fn=str.upper),
    ],
    output=ConsoleOutput(),
)

# Ejecutar
pipeline.run()
# Output:
# {'name': 'ALICE', 'age': 30, 'city': 'NYC'}
# {'name': 'CHARLIE', 'age': 35, 'city': 'NYC'}
```

---

## 🔧 CLI Esperado

```bash
# Procesar archivo CSV
data-processor run --source csv --input data.csv --filter "city=NYC"

# Procesar JSON con transformación
data-processor run --source json --input data.json --transform "name=upper"

# Ver plugins disponibles
data-processor plugins list
```

---

## 📊 Criterios de Evaluación

Ver [rubrica-evaluacion.md](../rubrica-evaluacion.md) para detalles completos.

| Nivel | Puntos | Descripción |
|-------|--------|-------------|
| Excelente | 90-100 | Todo implementado, extensible, bien documentado |
| Bueno | 70-89 | Funciona correctamente, estructura clara |
| Regular | 50-69 | Funciona parcialmente, faltan algunos componentes |
| Insuficiente | <50 | No cumple requisitos mínimos |

---

## 💡 Tips

1. **Empieza simple**: Implementa primero `MemorySource` y `ConsoleOutput`
2. **ABC para procesadores**: Te permite compartir lógica de validación
3. **Protocol para I/O**: Facilita testing con mocks
4. **Pipeline inmutable**: Cada ejecución no modifica el pipeline
5. **Tests primero**: Escribe tests antes de implementar

---

## 🔗 Recursos

- [Teoría: Clases Abstractas](../1-teoria/01-clases-abstractas.md)
- [Teoría: Protocols](../1-teoria/02-protocols-interfaces.md)
- [Teoría: Módulos](../1-teoria/03-modulos-imports.md)
- [Teoría: Paquetes](../1-teoria/04-paquetes-dependencias.md)

---

## 🔗 Navegación

| ← Anterior | Actual | Siguiente → |
|------------|--------|-------------|
| [Ejercicio 03](../2-ejercicios/03-paquete-completo/) | **Proyecto** | [Recursos](../4-recursos/) |
