# 📦 Ejercicio 3: Crear un Paquete Completo

## 🎯 Objetivo

Crear un paquete Python distribuible con estructura `src/`, configuración en `pyproject.toml`, y comandos CLI usando entry points.

---

## 📋 Descripción

Construirás un paquete llamado `text-tools` que incluye:

1. **Estructura src layout** correcta
2. **pyproject.toml** con metadata completa
3. **Entry points** para comandos CLI
4. **Tests** con pytest
5. **Instalación** en modo editable

---

## 🔧 Conceptos Practicados

- Estructura de paquete distribuible
- Configuración con pyproject.toml
- Entry points para CLI
- Gestión de dependencias con uv
- Instalación en modo desarrollo

---

## 📁 Estructura Final

```
text-tools/
├── pyproject.toml
├── README.md
├── src/
│   └── text_tools/
│       ├── __init__.py
│       ├── core.py
│       ├── transformers.py
│       └── cli.py
└── tests/
    ├── __init__.py
    ├── test_core.py
    └── test_transformers.py
```

---

## 🚀 Instrucciones

### Paso 1: Crear Estructura del Proyecto

Crea la estructura base:

```bash
cd starter
mkdir -p text-tools/src/text_tools text-tools/tests
cd text-tools
touch pyproject.toml README.md
touch src/text_tools/__init__.py
touch src/text_tools/core.py
touch src/text_tools/transformers.py
touch src/text_tools/cli.py
touch tests/__init__.py tests/test_core.py
```

---

### Paso 2: Configurar pyproject.toml

Descomenta y completa el contenido en el archivo de ejemplo.

---

### Paso 3: Implementar el Código

Sigue las instrucciones en `main.py` para implementar:

- `core.py`: Clase `TextProcessor` principal
- `transformers.py`: Funciones de transformación
- `cli.py`: Comandos de línea de comandos

---

### Paso 4: Instalar y Probar

```bash
# Instalar en modo editable
uv pip install -e .

# Probar CLI
text-tools --help
text-tools upper "hello world"
text-tools reverse "python"

# Ejecutar tests
uv run pytest
```

---

## ✅ Resultado Esperado

```
=== Paquete text-tools ===

--- Paso 1: Estructura creada ---
text-tools/
├── pyproject.toml
├── src/text_tools/
│   ├── __init__.py
│   ├── core.py
│   ├── transformers.py
│   └── cli.py
└── tests/

--- Paso 2: Instalación ---
$ uv pip install -e .
Successfully installed text-tools-0.1.0

--- Paso 3: CLI funcionando ---
$ text-tools upper "hello world"
HELLO WORLD

$ text-tools reverse "python"
nohtyp

$ text-tools count "hello world"
Characters: 11, Words: 2

--- Paso 4: Tests pasando ---
$ uv run pytest
===== 6 passed in 0.05s =====
```

---

## 💡 Tips

- El nombre del paquete en PyPI usa guiones (`text-tools`)
- El nombre del módulo Python usa guiones bajos (`text_tools`)
- Usa `hatchling` como build backend (simple y moderno)
- `uv pip install -e .` permite editar código sin reinstalar

---

## 🔗 Navegación

| ← Anterior | Actual | Siguiente → |
|------------|--------|-------------|
| [Ejercicio 02](../02-modulos-organizacion/) | **Ejercicio 03** | [Proyecto](../../3-proyecto/) |
