# 🔌 Ejercicio 1: Sistema de Plugins con ABC

## 🎯 Objetivo

Crear un sistema de plugins extensible usando clases abstractas (ABC). Implementarás una arquitectura donde nuevos plugins pueden añadirse sin modificar el código existente.

---

## 📋 Descripción

Construirás un **sistema de procesamiento de texto** con plugins intercambiables:

1. **Clase abstracta `TextPlugin`**: Define la interfaz que todos los plugins deben implementar
2. **Plugins concretos**: `UppercasePlugin`, `ReversePlugin`, `CensorPlugin`
3. **PluginManager**: Gestiona el registro y ejecución de plugins

---

## 🔧 Conceptos Practicados

- Módulo `abc` y clase `ABC`
- Decorador `@abstractmethod`
- Métodos abstractos vs concretos
- Patrón Registry para plugins
- Type hints con clases abstractas

---

## 📁 Estructura

```
01-clases-abstractas/
├── README.md          # Este archivo
└── starter/
    └── main.py        # Código a descomentar
```

---

## 🚀 Instrucciones

### Paso 1: Crear la Clase Abstracta Base

La clase `TextPlugin` define el **contrato** que todos los plugins deben cumplir:

```python
from abc import ABC, abstractmethod

class TextPlugin(ABC):
    """Plugin abstracto para procesar texto."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Nombre único del plugin."""
        ...

    @abstractmethod
    def process(self, text: str) -> str:
        """Procesa el texto y retorna el resultado."""
        ...
```

**Abre `starter/main.py`** y descomenta la sección del Paso 1.

---

### Paso 2: Implementar Plugins Concretos

Cada plugin hereda de `TextPlugin` e implementa los métodos abstractos:

```python
class UppercasePlugin(TextPlugin):
    @property
    def name(self) -> str:
        return "uppercase"

    def process(self, text: str) -> str:
        return text.upper()
```

**Descomenta** las implementaciones de `UppercasePlugin`, `ReversePlugin` y `CensorPlugin`.

---

### Paso 3: Crear el PluginManager

El manager registra y ejecuta plugins:

```python
class PluginManager:
    def __init__(self):
        self._plugins: dict[str, TextPlugin] = {}

    def register(self, plugin: TextPlugin) -> None:
        self._plugins[plugin.name] = plugin

    def process(self, plugin_name: str, text: str) -> str:
        if plugin_name not in self._plugins:
            raise ValueError(f"Plugin '{plugin_name}' not found")
        return self._plugins[plugin_name].process(text)
```

**Descomenta** la clase `PluginManager` y los métodos adicionales.

---

### Paso 4: Probar el Sistema

Ejecuta el código y verifica que:

1. No puedes instanciar `TextPlugin` directamente
2. Cada plugin procesa texto correctamente
3. El manager puede ejecutar cualquier plugin registrado

```bash
cd bootcamp/week-10/2-ejercicios/01-clases-abstractas/starter
python main.py
```

---

## ✅ Resultado Esperado

```
=== Sistema de Plugins con ABC ===

--- Paso 1: Verificar que TextPlugin es abstracta ---
✓ No se puede instanciar TextPlugin directamente

--- Paso 2: Plugins concretos ---
Original: Hello World
uppercase: HELLO WORLD
reverse: dlroW olleH
censor: H***o W***d

--- Paso 3: PluginManager ---
Plugins registrados: ['uppercase', 'reverse', 'censor']
Procesando 'Python is awesome!' con uppercase: PYTHON IS AWESOME!
Procesando 'Python is awesome!' con reverse: !emosewa si nohtyP

--- Paso 4: Pipeline de plugins ---
Input: secret password here
Pipeline [censor -> uppercase]: S****T P******D H**E

--- Paso 5: Agregar nuevo plugin dinámicamente ---
Nuevo plugin 'spaces' registrado
spaces('Hello'): H e l l o
```

---

## 💡 Tips

- La propiedad `name` usa `@property` + `@abstractmethod` (decoradores apilados)
- `@abstractmethod` debe ser el decorador **más interno** (más cercano a la función)
- El manager usa un diccionario para O(1) en búsqueda de plugins

---

## 🔗 Navegación

| ← Anterior | Actual | Siguiente → |
|------------|--------|-------------|
| [Teoría 04](../../1-teoria/04-paquetes-dependencias.md) | **Ejercicio 01** | [Ejercicio 02](../02-modulos-organizacion/) |
