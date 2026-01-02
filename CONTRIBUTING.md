# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al **Bootcamp Python Zero to Hero**! Este documento proporciona las pautas para contribuir al proyecto.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [¿Cómo Puedo Contribuir?](#cómo-puedo-contribuir)
- [Configuración del Entorno](#configuración-del-entorno)
- [Estilo de Código](#estilo-de-código)
- [Commits y Pull Requests](#commits-y-pull-requests)
- [Estructura del Proyecto](#estructura-del-proyecto)

---

## 📜 Código de Conducta

Este proyecto adhiere al [Código de Conducta](CODE_OF_CONDUCT.md). Al participar, se espera que respetes este código. Por favor, reporta comportamientos inaceptables a los mantenedores del proyecto.

---

## 🎯 ¿Cómo Puedo Contribuir?

### 🐛 Reportar Bugs

Si encuentras un bug, por favor abre un [Issue](https://github.com/epti-dev/bc-python/issues/new?template=bug_report.md) con:

- Descripción clara del problema
- Pasos para reproducirlo
- Comportamiento esperado vs actual
- Screenshots si aplica
- Información del entorno (OS, versiones)

### 💡 Sugerir Mejoras

Para sugerir nuevas funcionalidades o mejoras:

1. Revisa los [Issues existentes](https://github.com/epti-dev/bc-python/issues) para evitar duplicados
2. Abre un nuevo Issue con la etiqueta `enhancement`
3. Describe claramente la mejora propuesta
4. Explica el caso de uso y beneficios

### 📚 Contribuir Contenido

Áreas donde puedes contribuir:

| Área                     | Descripción                 |
| ------------------------ | --------------------------- |
| ✨ **Ejercicios**        | Nuevos ejercicios prácticos |
| 📖 **Teoría**            | Mejoras en explicaciones    |
| 🎨 **Recursos visuales** | Diagramas SVG educativos    |
| 🐛 **Correcciones**      | Errores en código o texto   |
| 🌐 **Traducciones**      | Contenido en otros idiomas  |
| 📹 **Videos**            | Tutoriales complementarios  |

### 🔧 Contribuir Código

1. Fork del repositorio
2. Crea una rama para tu feature
3. Implementa los cambios
4. Escribe/actualiza tests si aplica
5. Asegura que pasan los tests
6. Envía un Pull Request

---

## ⚙️ Configuración del Entorno

### Prerrequisitos

- Docker y Docker Compose
- Git
- VS Code (recomendado)

### Pasos

```bash
# 1. Fork y clonar
git clone https://github.com/TU-USUARIO/bc-python.git
cd bc-python

# 2. Agregar upstream
git remote add upstream https://github.com/epti-dev/bc-python.git

# 3. Crear rama de trabajo
git checkout -b feature/mi-contribucion

# 4. Abrir en VS Code
code .
```

### Sincronizar con Upstream

```bash
git fetch upstream
git checkout main
git merge upstream/main
```

---

## 🎨 Estilo de Código

### Python

- **Versión**: Python 3.13+
- **Type hints**: Obligatorios
- **Formateo**: Seguir PEP 8
- **Nomenclatura**:
  - Variables/funciones: `snake_case`
  - Clases: `PascalCase`
  - Constantes: `UPPER_SNAKE_CASE`

```python
# ✅ Correcto
def calculate_average(numbers: list[float]) -> float:
    """Calculate the average of a list of numbers."""
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)

# ❌ Incorrecto
def calcularPromedio(nums):
    return sum(nums)/len(nums)
```

### Markdown

- Usar encabezados jerárquicos (`#`, `##`, `###`)
- Incluir emojis para mejorar legibilidad (con moderación)
- Código con syntax highlighting
- Enlaces relativos para archivos internos

### Recursos Visuales

- **Formato**: SVG preferido
- **Tema**: Dark mode
- **Sin degradados**: Solo colores sólidos
- **Paleta**: Azul Python (#306998, #FFD43B)

---

## 📝 Commits y Pull Requests

### Conventional Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/). Formato:

```
<tipo>[alcance opcional]: <descripción>

[cuerpo opcional]

[footer opcional]
```

#### Tipos de Commit

| Tipo       | Descripción                     |
| ---------- | ------------------------------- |
| `feat`     | Nueva funcionalidad             |
| `fix`      | Corrección de bug               |
| `docs`     | Cambios en documentación        |
| `style`    | Formateo, sin cambios de código |
| `refactor` | Refactorización de código       |
| `test`     | Agregar o modificar tests       |
| `chore`    | Tareas de mantenimiento         |

#### Ejemplos

```bash
# Nueva funcionalidad
git commit -m "feat(week-03): add dictionary comprehension exercises"

# Corrección
git commit -m "fix(week-01): correct typo in variables theory"

# Documentación
git commit -m "docs: update contributing guidelines"

# Refactorización
git commit -m "refactor(week-05): simplify sorting algorithm examples"
```

### Pull Requests

1. **Título**: Descriptivo y conciso
2. **Descripción**: Usa la plantilla proporcionada
3. **Referencias**: Vincula Issues relacionados (`Fixes #123`)
4. **Tests**: Asegura que el código funciona
5. **Revisión**: Espera feedback antes de merge

---

## 📁 Estructura del Proyecto

```
bc-python/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── copilot-instructions.md
├── _assets/                  # Assets globales
├── _docs/                    # Documentación general
├── _scripts/                 # Scripts de utilidad
├── bootcamp/
│   └── week-XX/
│       ├── README.md
│       ├── rubrica-evaluacion.md
│       ├── 0-assets/
│       ├── 1-teoria/
│       ├── 2-ejercicios/
│       ├── 3-proyecto/
│       ├── 4-recursos/
│       └── 5-glosario/
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── LICENSE
├── README.md
├── README-EN.md
└── SECURITY.md
```

### Convenciones de Archivos

- **Nombres**: `snake_case` para archivos Python
- **Carpetas de semanas**: `week-01`, `week-02`, etc.
- **Assets**: Nombres descriptivos (`for-loop-flow.svg`)

---

## ✅ Checklist antes de enviar PR

- [ ] El código sigue las guías de estilo
- [ ] Los commits siguen Conventional Commits
- [ ] La documentación está actualizada
- [ ] Los ejemplos de código funcionan
- [ ] No hay errores de sintaxis o typos
- [ ] Los assets SVG usan tema dark

---

## 🙏 Reconocimiento

Todos los contribuidores serán reconocidos en el README principal y en la sección de agradecimientos.

---

## ❓ ¿Preguntas?

- 💬 [GitHub Discussions](https://github.com/epti-dev/bc-python/discussions)
- 🐛 [GitHub Issues](https://github.com/epti-dev/bc-python/issues)

¡Gracias por contribuir! 🎉
