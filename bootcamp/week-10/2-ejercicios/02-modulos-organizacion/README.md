# 📂 Ejercicio 2: Organización en Módulos

## 🎯 Objetivo

Aprender a organizar código en múltiples módulos, usar imports correctamente y configurar `__init__.py` para exportar una API limpia.

---

## 📋 Descripción

Refactorizarás un archivo monolítico en una estructura modular:

1. **Separar responsabilidades** en archivos distintos
2. **Configurar imports** absolutos y relativos
3. **Usar `__init__.py`** para definir exports públicos
4. **Evitar imports circulares**

---

## 🔧 Conceptos Practicados

- Crear módulos Python
- Imports absolutos vs relativos
- Archivo `__init__.py` y `__all__`
- Organización de imports (PEP 8)
- Resolución de imports circulares

---

## 📁 Estructura Final

Después de completar el ejercicio, tendrás:

```
starter/
├── main.py                 # Punto de entrada
└── ecommerce/              # Paquete principal
    ├── __init__.py         # Exports públicos
    ├── models/
    │   ├── __init__.py
    │   ├── product.py
    │   └── user.py
    ├── services/
    │   ├── __init__.py
    │   ├── cart_service.py
    │   └── user_service.py
    └── utils/
        ├── __init__.py
        └── validators.py
```

---

## 🚀 Instrucciones

### Paso 1: Entender el Código Monolítico

Primero, revisa `main.py` que contiene todo el código en un solo archivo. Ejecuta para ver que funciona:

```bash
python main.py
```

---

### Paso 2: Crear la Estructura de Carpetas

```bash
cd starter
mkdir -p ecommerce/models ecommerce/services ecommerce/utils
touch ecommerce/__init__.py
touch ecommerce/models/__init__.py
touch ecommerce/services/__init__.py
touch ecommerce/utils/__init__.py
```

---

### Paso 3: Extraer Módulos

Sigue las instrucciones en `main.py` para:

1. Mover clases a sus archivos correspondientes
2. Configurar imports en cada archivo
3. Actualizar `__init__.py` con exports

---

### Paso 4: Verificar Imports

Después de modularizar, el `main.py` debe poder importar así:

```python
from ecommerce.models import User, Product
from ecommerce.services import CartService, UserService
from ecommerce.utils import validate_email
```

---

## ✅ Resultado Esperado

```
=== Sistema E-Commerce Modularizado ===

--- Paso 1: Código monolítico funcionando ---
Validando email: alice@example.com ✓
Usuario creado: User(id=1, name=Alice, email=alice@example.com)
Producto creado: Product(id=101, name=Laptop, price=999.99)

--- Paso 2: Estructura de módulos ---
ecommerce/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   └── product.py
├── services/
│   ├── __init__.py
│   ├── user_service.py
│   └── cart_service.py
└── utils/
    ├── __init__.py
    └── validators.py

--- Paso 3: Imports funcionando ---
✓ Imports desde ecommerce.models
✓ Imports desde ecommerce.services
✓ Imports desde ecommerce.utils

--- Paso 4: Sistema completo ---
Usuario: Alice (alice@example.com)
Carrito:
  - Laptop x1 = $999.99
  - Mouse x2 = $59.98
Total: $1059.97
```

---

## 💡 Tips

- Usa imports **relativos** dentro del paquete (`from .user import User`)
- Usa imports **absolutos** desde fuera (`from ecommerce.models import User`)
- `__all__` define qué se exporta con `from module import *`
- Si tienes import circular, considera usar `TYPE_CHECKING`

---

## 🔗 Navegación

| ← Anterior | Actual | Siguiente → |
|------------|--------|-------------|
| [Ejercicio 01](../01-clases-abstractas/) | **Ejercicio 02** | [Ejercicio 03](../03-paquete-completo/) |
