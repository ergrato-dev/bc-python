# 📖 Glosario - Semana 10

## Clases Abstractas, Módulos y Paquetes

### A

#### ABC (Abstract Base Class)
Clase que no puede ser instanciada directamente y sirve como plantilla para otras clases. En Python se usa el módulo `abc`.
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...
```

#### Abstract Method
Método decorado con `@abstractmethod` que debe ser implementado por todas las subclases concretas.

#### Absolute Import
Import que especifica la ruta completa desde la raíz del proyecto.
```python
from myproject.utils.helpers import format_date
```

---

### B

#### Build Backend
Sistema que construye paquetes distribuibles. Ejemplos: `hatchling`, `setuptools`, `flit`.

#### Build System
Configuración en `pyproject.toml` que indica cómo construir el paquete.
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

---

### C

#### Circular Import
Error que ocurre cuando dos módulos se importan mutuamente, creando una dependencia cíclica.

#### Concrete Class
Clase que implementa todos los métodos abstractos de su clase base y puede ser instanciada.

---

### D

#### Dependency
Paquete externo requerido por tu proyecto para funcionar.

#### Dependency Injection (DI)
Patrón donde las dependencias se pasan como parámetros en lugar de crearse internamente.
```python
class Service:
    def __init__(self, repository: Repository):  # Inyectada
        self.repository = repository
```

#### Distributable Package
Archivo `.whl` o `.tar.gz` que puede ser instalado con pip/uv.

#### Duck Typing
Filosofía donde el tipo de un objeto se determina por sus métodos, no por su clase.
> "Si camina como pato y grazna como pato, es un pato"

---

### E

#### Editable Install
Instalación que permite modificar código sin reinstalar (`pip install -e .`).

#### Entry Point
Configuración que crea comandos ejecutables desde un paquete.
```toml
[project.scripts]
my-cli = "mypackage.cli:main"
```

---

### F

#### Forward Reference
Referencia a una clase que aún no existe usando strings.
```python
def method(self) -> "FutureClass": ...
```

---

### I

#### `__init__.py`
Archivo que convierte un directorio en un paquete Python. Define qué se exporta.

#### Interface
Contrato que define qué métodos debe tener una clase. En Python: ABC o Protocol.

#### Interface Segregation
Principio SOLID: Interfaces pequeñas y específicas son mejores que una grande.

---

### L

#### Lock File
Archivo (`uv.lock`) que registra versiones exactas de todas las dependencias.

---

### M

#### Metaclass
Clase cuyas instancias son clases. `ABCMeta` es la metaclase de ABC.

#### Module
Archivo Python (`.py`) que contiene código reutilizable.

#### MRO (Method Resolution Order)
Orden en que Python busca métodos en herencia múltiple. Ver con `Class.__mro__`.

---

### N

#### Namespace
Contenedor que evita colisiones de nombres. Los módulos actúan como namespaces.

#### Namespace Package
Paquete sin `__init__.py` que permite dividir un paquete en múltiples directorios.

#### Nominal Typing
Tipado donde la compatibilidad se basa en herencia explícita (ABC).

---

### P

#### Package
Directorio con `__init__.py` que contiene módulos relacionados.

#### Protocol
Clase de `typing` que define una interfaz estructural (duck typing con tipos).
```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...
```

#### PyPI (Python Package Index)
Repositorio oficial de paquetes Python (https://pypi.org).

#### pyproject.toml
Archivo estándar para configurar proyectos Python (PEP 518, 621).

---

### R

#### Relative Import
Import relativo al módulo actual usando puntos.
```python
from .models import User      # Mismo directorio
from ..utils import helper    # Directorio padre
```

#### `runtime_checkable`
Decorador que permite usar `isinstance()` con Protocols.
```python
@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...
```

---

### S

#### Semantic Versioning (SemVer)
Sistema de versionado: MAJOR.MINOR.PATCH (ej: 1.2.3).

#### Site-packages
Directorio donde se instalan paquetes de terceros.

#### src Layout
Estructura de proyecto con código fuente en `src/paquete/`.
```
proyecto/
├── src/
│   └── mi_paquete/
└── pyproject.toml
```

#### Structural Typing
Tipado donde la compatibilidad se basa en los métodos presentes (Protocol).

---

### T

#### Template Method Pattern
Patrón donde una clase base define el algoritmo y subclases implementan pasos específicos.

#### TestPyPI
Versión de prueba de PyPI para testing de publicación.

#### Type Hint
Anotación que indica el tipo esperado de variables y funciones.

#### TYPE_CHECKING
Constante de `typing` que es `True` solo durante verificación de tipos.
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import User  # Solo para type hints
```

---

### U

#### uv
Gestor de paquetes moderno y rápido de Astral (reemplaza pip + venv).

---

### V

#### Virtual Environment (venv)
Entorno aislado con su propia instalación de Python y paquetes.

---

### W

#### Wheel (`.whl`)
Formato de distribución de paquetes Python (más rápido que `.tar.gz`).

---

### `__`

#### `__all__`
Lista que define qué nombres se exportan con `from module import *`.
```python
__all__ = ["User", "Product", "create_user"]
```

#### `__name__`
Variable especial con el nombre del módulo. Es `"__main__"` si se ejecuta directamente.

#### `__version__`
Convención para almacenar la versión del paquete.
```python
__version__ = "1.0.0"
```

---

## 📊 Tabla Comparativa: ABC vs Protocol

| Aspecto | ABC | Protocol |
|---------|-----|----------|
| Tipado | Nominal | Estructural |
| Herencia | Requerida | No requerida |
| Métodos compartidos | ✅ Sí | ❌ No |
| Verificación runtime | Al instanciar | Con @runtime_checkable |
| Clases externas | ❌ No | ✅ Sí |

---

## 🔗 Navegación

| ← Anterior | Actual | Siguiente → |
|------------|--------|-------------|
| [Webgrafía](../4-recursos/webgrafia/) | **Glosario** | [Week-11](../../week-11/) |
