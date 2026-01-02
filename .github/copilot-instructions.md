# 🤖 Instrucciones para GitHub Copilot

## 📋 Contexto del Bootcamp

Este es un **Bootcamp de Python Zero to Hero** estructurado para llevar a estudiantes de cero a héroe en programación con Python moderno.

### 📊 Datos del Bootcamp

- **Duración**: 14 semanas (~3.5 meses)
- **Dedicación semanal**: 6 horas
- **Total de horas**: ~84 horas
- **Nivel de salida**: Desarrollador Python Junior
- **Enfoque**: Python moderno 3.13+
- **Stack**: Python 3.13+, pytest, uv (gestor de paquetes), Docker

---

## 🎯 Objetivos de Aprendizaje

Al finalizar el bootcamp, los estudiantes serán capaces de:

- ✅ Dominar los fundamentos de Python moderno (3.13+)
- ✅ Aplicar type hints y tipado estático correctamente
- ✅ Trabajar con estructuras de datos complejas
- ✅ Implementar Programación Orientada a Objetos (POO)
- ✅ Manejar archivos, excepciones y módulos
- ✅ Escribir código limpio y mantenible
- ✅ Crear tests automatizados con pytest
- ✅ Usar control de versiones con Git
- ✅ Trabajar con librerías populares del ecosistema Python
- ✅ Desarrollar proyectos completos desde cero

---

## 📚 Estructura del Bootcamp

### Distribución por Etapas

#### **Fundamentos (Semanas 1-4)** - 24 horas

- Introducción a Python y configuración del entorno
- Variables, tipos de datos y operadores
- Input/Output y formateo de strings
- Condicionales (if/elif/else)
- Bucles (for, while) y control de flujo
- Comprensiones de listas, diccionarios y sets
- Funciones: definición, parámetros y retorno

#### **Estructuras de Datos (Semanas 5-7)** - 18 horas

- Listas: métodos, slicing y operaciones
- Tuplas y su inmutabilidad
- Diccionarios: operaciones y métodos
- Sets y operaciones de conjuntos
- Estructuras anidadas y complejas
- Algoritmos básicos de búsqueda y ordenamiento

#### **POO y Modularidad (Semanas 8-10)** - 18 horas

- Clases y objetos
- Atributos y métodos
- Encapsulamiento y propiedades
- Herencia y polimorfismo
- Clases abstractas e interfaces
- Módulos y paquetes
- Manejo de dependencias con uv

#### **Temas Avanzados (Semanas 11-13)** - 18 horas

- Manejo de archivos (lectura/escritura)
- Excepciones: try/except/finally
- Context managers (with)
- Decoradores y generadores
- Expresiones regulares (regex)
- Testing con pytest
- Debugging y logging

#### **Proyecto Integrador (Semana 14)** - 6 horas

- Proyecto final que integra todos los conceptos
- Uso de librerías externas (requests, etc.)
- Documentación y buenas prácticas
- Presentación del proyecto

---

## 🗂️ Estructura de Carpetas

Cada semana sigue esta estructura estándar:

```
bootcamp/week-XX/
├── README.md                 # Descripción y objetivos de la semana
├── rubrica-evaluacion.md     # Criterios de evaluación detallados
├── 0-assets/                 # Imágenes, diagramas y recursos visuales
├── 1-teoria/                 # Material teórico (archivos .md)
├── 2-ejercicios/             # Ejercicios guiados paso a paso
├── 3-proyecto/               # Proyecto semanal integrador
│   ├── README.md             # Instrucciones del proyecto
│   ├── starter/              # Código inicial para el estudiante
│   └── solution/             # ⚠️ OCULTA - Solo para instructores
├── 4-recursos/               # Recursos adicionales
│   ├── ebooks-free/          # Libros electrónicos gratuitos
│   ├── videografia/          # Videos y tutoriales recomendados
│   └── webgrafia/            # Enlaces y documentación
└── 5-glosario/               # Términos clave de la semana (A-Z)
    └── README.md
```

### 📁 Carpetas Raíz

- **`_assets/`**: Recursos visuales globales (logos, headers, etc.)
- **`_docs/`**: Documentación general que aplica a todo el bootcamp
- **`_scripts/`**: Scripts de automatización y utilidades
- **`bootcamp/`**: Contenido semanal del bootcamp

---

## 🎓 Componentes de Cada Semana

### 1. **Teoría** (1-teoria/)

- Archivos markdown con explicaciones conceptuales
- Ejemplos de código con comentarios claros
- Diagramas y visualizaciones cuando sea necesario
- Referencias a documentación oficial de Python

### 2. **Ejercicios** (2-ejercicios/)

- Ejercicios guiados paso a paso
- Incremento progresivo de dificultad
- Soluciones comentadas
- Casos de uso del mundo real

#### 📋 Formato de Ejercicios

Los ejercicios son **tutoriales guiados**, NO tareas con TODOs. El estudiante aprende descomentando código:

**README.md del ejercicio:**

```markdown
### Paso 1: Crear una función básica

Explicación del concepto con ejemplo:

\`\`\`python

# Ejemplo explicativo

def greet(name: str) -> str:
return f"Hola, {name}!"
\`\`\`

**Abre `starter/main.py`** y descomenta la sección correspondiente.
```

**starter/main.py:**

```python
# ============================================
# PASO 1: Crear una función básica
# ============================================
print("--- Paso 1: Función básica ---")

# Las funciones encapsulan lógica reutilizable
# Descomenta las siguientes líneas:
# def greet(name: str) -> str:
#     return f"Hola, {name}!"
#
# print(greet("Python"))
```

> ⚠️ **IMPORTANTE**: Los ejercicios NO tienen carpeta `solution/`. El estudiante aprende descomentando el código y verificando que funcione correctamente.

#### ❌ NO usar este formato en ejercicios:

```python
# ❌ INCORRECTO - Este formato es para PROYECTOS, no ejercicios
def calculate_area(radius: float) -> float:
    result = None  # TODO: Implementar
    return result
```

#### ✅ Usar este formato en ejercicios:

```python
# ✅ CORRECTO - Código comentado para descomentar
# Descomenta las siguientes líneas:
# def calculate_area(radius: float) -> float:
#     return 3.14159 * radius ** 2
```

### 3. **Proyecto** (3-proyecto/)

- Proyecto integrador que consolida lo aprendido
- README.md con instrucciones claras
- Código inicial en `starter/`
- Carpeta `solution/` oculta (en `.gitignore`) solo para instructores
- Criterios de evaluación específicos

#### 📋 Formato de Proyecto (con TODOs)

A diferencia de los ejercicios, el proyecto SÍ usa TODOs para que el estudiante implemente desde cero:

**starter/main.py:**

```python
# ============================================
# FUNCIÓN: calculate_statistics
# Calcula estadísticas de una lista de números
# ============================================

def calculate_statistics(numbers: list[float]) -> dict[str, float]:
    """
    Calcula estadísticas básicas de una lista de números.

    Args:
        numbers: Lista de números a analizar

    Returns:
        dict: Diccionario con min, max, promedio y suma
    """
    # TODO: Implementar lógica
    # 1. Calcular el valor mínimo
    # 2. Calcular el valor máximo
    # 3. Calcular el promedio
    # 4. Calcular la suma total
    # 5. Retornar diccionario con resultados
    pass
```

> 📁 **Estructura del proyecto:**
>
> ```
> 3-proyecto/
> ├── README.md          # Instrucciones del proyecto
> ├── starter/           # Código inicial para el estudiante
> └── solution/          # ⚠️ OCULTA - Solo para instructores
> ```
>
> La carpeta `solution/` está en `.gitignore` y NO se sube al repositorio público.

### 4. **Recursos** (4-recursos/)

- **ebooks-free/**: Libros gratuitos relevantes
- **videografia/**: Videos tutoriales complementarios
- **webgrafia/**: Enlaces a documentación y artículos

### 5. **Glosario** (5-glosario/)

- Términos técnicos ordenados alfabéticamente
- Definiciones claras y concisas
- Ejemplos de código cuando aplique

---

## 📝 Convenciones de Código

### Estilo Python Moderno

```python
# ✅ BIEN - usar type hints siempre
def get_item(item_id: int) -> dict | None:
    return items.get(item_id)

# ✅ BIEN - usar f-strings para formateo
def greet(name: str) -> str:
    return f"Hola, {name}!"

# ✅ BIEN - usar comprehensions
squares = [x ** 2 for x in range(10)]
even_squares = {x: x ** 2 for x in range(10) if x % 2 == 0}

# ✅ BIEN - usar match statements (Python 3.10+)
def handle_command(command: str) -> str:
    match command:
        case "start":
            return "Iniciando..."
        case "stop":
            return "Deteniendo..."
        case _:
            return "Comando desconocido"

# ✅ BIEN - usar walrus operator cuando simplifique
if (n := len(data)) > 10:
    print(f"Lista con {n} elementos")

# ❌ MAL - sin type hints
def get_item(item_id):
    return items.get(item_id)

# ❌ MAL - usar format() o %
def greet(name):
    return "Hola, {}!".format(name)
```

### Nomenclatura

- **Variables y funciones**: snake_case
- **Constantes globales**: UPPER_SNAKE_CASE
- **Clases**: PascalCase
- **Archivos**: snake_case.py
- **Módulos/Paquetes**: snake_case
- **Idioma**: Inglés para código, español para documentación

### Estructura de Proyecto Python

```
proyecto/
├── src/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada
│   ├── config.py            # Configuración
│   ├── models/              # Modelos de datos
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/            # Lógica de negocio
│   │   ├── __init__.py
│   │   └── user_service.py
│   └── utils/               # Utilidades
│       ├── __init__.py
│       └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_services/
├── pyproject.toml           # Configuración del proyecto
├── uv.lock                  # Lock de dependencias
└── README.md
```

---

## 🧪 Testing

El bootcamp enseña testing con **pytest**.

### Estructura de Tests

```python
# tests/test_calculator.py
import pytest
from src.calculator import add, divide

def test_add_positive_numbers():
    """Test suma de números positivos."""
    result = add(2, 3)
    assert result == 5

def test_add_negative_numbers():
    """Test suma con números negativos."""
    result = add(-1, -1)
    assert result == -2

def test_divide_by_zero():
    """Test división por cero lanza excepción."""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

@pytest.mark.parametrize("a,b,expected", [
    (1, 1, 2),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_add_parametrized(a: int, b: int, expected: int):
    """Test suma con múltiples casos."""
    assert add(a, b) == expected
```

### Fixtures

```python
# tests/conftest.py
import pytest

@pytest.fixture
def sample_users() -> list[dict]:
    """Fixture que provee usuarios de prueba."""
    return [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
    ]

@pytest.fixture
def temp_file(tmp_path):
    """Fixture que crea un archivo temporal."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("contenido de prueba")
    return file_path
```

---

## 📖 Documentación

### README.md de Semana

Debe incluir:

1. **Título y descripción**
2. **🎯 Objetivos de aprendizaje**
3. **📚 Requisitos previos**
4. **🗂️ Estructura de la semana**
5. **📝 Contenidos** (con enlaces a teoría/ejercicios)
6. **⏱️ Distribución del tiempo** (6 horas)
7. **📌 Entregables**
8. **🔗 Navegación** (anterior/siguiente semana)

### Archivos de Teoría

```markdown
# Título del Tema

## 🎯 Objetivos

- Objetivo 1
- Objetivo 2

## 📋 Contenido

### 1. Introducción

### 2. Conceptos Clave

### 3. Ejemplos Prácticos

### 4. Ejercicios

## 📚 Recursos Adicionales

## ✅ Checklist de Verificación
```

---

## 🎨 Recursos Visuales y Estándares de Diseño

### Formato de Assets

- ✅ **Preferir SVG** para todos los diagramas, iconos y gráficos
- ❌ **NO usar ASCII art** para diagramas o visualizaciones
- ✅ Usar PNG/JPG solo para screenshots o fotografías
- ✅ Optimizar imágenes antes de incluirlas

### Criterio para Assets SVG por Semana

Los assets SVG en `0-assets/` de cada semana tienen un propósito educativo específico:

- ✅ **Apoyo visual para comprensión de conceptos teóricos**
- ✅ **Diagramas de arquitectura** (flujo de datos, capas, etc.)
- ✅ **Visualización de procesos** (loops, condicionales, etc.)
- ✅ **Headers de semana** para identificación visual

**Reglas de vinculación:**

1. Todo SVG debe estar **vinculado en al menos un archivo** de teoría o ejercicio
2. Usar sintaxis markdown: `![Descripción](../0-assets/nombre.svg)`
3. Incluir texto alternativo descriptivo para accesibilidad
4. Nombrar archivos descriptivamente: `for-loop-flow.svg`, `list-methods.svg`

```markdown
<!-- Ejemplo de vinculación correcta en teoría -->

## Flujo de un Bucle For

![Diagrama del flujo de un bucle for](../0-assets/for-loop-flow.svg)

Como se observa en el diagrama, el bucle itera...
```

### Tema Visual

- 🌙 **Tema dark** para todos los assets visuales
- ❌ **Sin degradés** (gradients) en diseños
- ✅ Colores sólidos y contrastes claros
- ✅ Paleta consistente basada en azul Python (#306998, #FFD43B)

### Tipografía

- ✅ **Fuentes sans-serif** exclusivamente
- ✅ Recomendadas: Inter, Roboto, Open Sans, System UI
- ❌ **NO usar fuentes serif** (Times, Georgia, etc.)
- ✅ Mantener jerarquía visual clara

### Otros

- ✅ Incluir screenshots con anotaciones claras
- ✅ Mantener consistencia visual entre semanas
- ✅ Usar emojis para mejorar legibilidad (con moderación)

---

## 🌐 Idioma y Nomenclatura

### Código y Comentarios Técnicos

- ✅ **Nomenclatura en inglés** (variables, funciones, clases)
- ✅ **Comentarios de código en inglés**
- ✅ Usar términos técnicos estándar de la industria

```python
# ✅ CORRECTO - inglés
def get_user_by_email(email: str) -> User | None:
    # Fetch user from database by email
    return db.query(User).filter(User.email == email).first()

# ❌ INCORRECTO - español en código
def obtener_usuario_por_email(correo: str) -> Usuario | None:
    # Obtener usuario de la base de datos por correo
    return db.query(Usuario).filter(Usuario.correo == correo).first()
```

### Documentación

- ✅ **Documentación en español** (READMEs, teoría, guías)
- ✅ Explicaciones y tutoriales en español
- ✅ Comentarios educativos en español cuando expliquen conceptos

```python
# ✅ CORRECTO - código en inglés, explicación en español
def calculate_discount(price: float, percentage: float) -> float:
    # En Python, los porcentajes se manejan como decimales
    # Por ejemplo: 20% = 0.20
    return price * (1 - percentage / 100)
```

---

## 🔐 Mejores Prácticas

### Código Limpio

- Nombres descriptivos y significativos
- Funciones pequeñas con una sola responsabilidad
- Comentarios solo cuando sea necesario explicar el "por qué"
- Evitar anidamiento profundo
- Usar early returns

### Seguridad

- Validar TODOS los inputs del usuario
- No hardcodear contraseñas o secrets
- Usar variables de entorno para configuración sensible
- Sanitizar datos antes de operaciones con archivos
- Usar hashing seguro para contraseñas (bcrypt/argon2)

### Rendimiento

- Usar generadores para grandes volúmenes de datos
- Evitar operaciones innecesarias dentro de bucles
- Usar estructuras de datos apropiadas (dict para búsquedas O(1))
- Lazy loading cuando sea apropiado
- Cachear resultados costosos de calcular

---

## 📊 Evaluación

Cada semana incluye **tres tipos de evidencias**:

1. **Conocimiento 🧠** (30%): Evaluaciones teóricas, cuestionarios
2. **Desempeño 💪** (40%): Ejercicios prácticos en clase
3. **Producto 📦** (30%): Proyecto entregable funcional

### Criterios de Aprobación

- Mínimo **70%** en cada tipo de evidencia
- Entrega puntual de proyectos
- Código funcional y bien documentado
- Tests pasando (cuando aplique)

---

## 🚀 Metodología de Aprendizaje

### Estrategias Didácticas

- **Aprendizaje Basado en Proyectos (ABP)**: Proyectos semanales integradores
- **Práctica Deliberada**: Ejercicios incrementales
- **Coding Challenges**: Problemas del mundo real
- **Code Review**: Revisión de código entre estudiantes
- **Live Coding**: Sesiones en vivo de programación

### Distribución del Tiempo (6h/semana)

- **Teoría**: 1.5-2 horas
- **Ejercicios**: 2.5-3 horas
- **Proyecto**: 1.5-2 horas

---

## 🤖 Instrucciones para Copilot

Cuando trabajes en este proyecto:

### Límites de Respuesta

1. **Divide respuestas largas**

   - ❌ **NUNCA generar respuestas que superen los límites de tokens**
   - ✅ **SIEMPRE dividir contenido extenso en múltiples entregas**
   - ✅ Crear contenido por secciones, esperar confirmación del usuario
   - ✅ Priorizar calidad sobre cantidad en cada entrega
   - Razón: Evitar pérdida de contenido y garantizar completitud

2. **Estrategia de División**
   - Para semanas completas: dividir por carpetas (teoria → ejercicios → proyecto)
   - Para archivos grandes: dividir por secciones lógicas
   - Siempre indicar claramente qué parte se entrega y qué falta
   - Esperar confirmación del usuario antes de continuar

### Generación de Código

1. **Usa siempre sintaxis Python moderna (3.13+)**

   - Type hints obligatorios
   - Match statements cuando aplique
   - f-strings para formateo
   - Walrus operator cuando simplifique
   - Union types con `|` en lugar de `Union[]`
   - Genéricos nativos (`list[str]` en lugar de `List[str]`)

2. **Entorno de Desarrollo con Docker**

   - ✅ **USAR Docker** para evitar problemas con múltiples versiones de Python
   - ✅ **docker compose** para orquestar servicios
   - ✅ Crear archivos `.env` para configuración de entorno
   - Razón: Entorno consistente, reproducible y aislado para todos los estudiantes
   - Estructura recomendada:

     ```
     proyecto/
     ├── docker-compose.yml    # Orquestación de servicios
     ├── Dockerfile            # Imagen de la aplicación
     ├── .env.example          # Variables de entorno (template)
     ├── .env                  # Variables de entorno (ignorado en git)
     └── src/                  # Código fuente
     ```

   - Comandos esenciales:

     ```bash
     # Construir y levantar servicios
     docker compose up --build

     # Levantar en background
     docker compose up -d

     # Ver logs
     docker compose logs -f app

     # Ejecutar comandos dentro del contenedor
     docker compose exec app bash

     # Detener servicios
     docker compose down

     # Limpiar todo (incluye volúmenes)
     docker compose down -v
     ```

3. **Gestión de Paquetes (dentro de Docker)**

   - ❌ **NUNCA usar `pip`** directamente
   - ✅ **SOLO usar `uv`** como gestor de paquetes (rápido y moderno)
   - Razón: Mejor resolución de dependencias, compatibilidad con Docker
   - En Dockerfile:

     ```dockerfile
     FROM python:3.13-slim

     ENV PYTHONDONTWRITEBYTECODE=1 \
         PYTHONUNBUFFERED=1 \
         UV_SYSTEM_PYTHON=1

     RUN pip install --no-cache-dir uv

     WORKDIR /app
     COPY pyproject.toml uv.lock* ./
     RUN uv sync --frozen --no-dev

     COPY . .
     CMD ["uv", "run", "python", "src/main.py"]
     ```

   - Comandos uv (dentro del contenedor):

     ```bash
     # Crear proyecto
     uv init

     # Instalar dependencias
     uv sync

     # Agregar paquete
     uv add requests

     # Agregar paquete de desarrollo
     uv add --dev pytest
     ```

4. **Comenta el código de manera educativa**

   - Explica conceptos para principiantes
   - Incluye referencias a documentación cuando sea útil
   - Usa comentarios que enseñen, no solo describan

5. **Proporciona ejemplos completos y funcionales**
   - Código que se pueda copiar y ejecutar
   - Incluye casos de uso realistas
   - Muestra tanto lo que se debe hacer como lo que se debe evitar

### Creación de Contenido

1. **Estructura clara y progresiva**

   - De lo simple a lo complejo
   - Conceptos construidos sobre conocimientos previos
   - Repetición espaciada de conceptos clave

2. **Ejemplos del mundo real**

   - Casos de uso prácticos y relevantes
   - Proyectos que los estudiantes puedan mostrar en portfolios
   - Problemas que encontrarán en el desarrollo real

3. **Enfoque moderno**
   - No mencionar características obsoletas
   - Enfocarse en mejores prácticas actuales
   - Usar herramientas y patrones modernos

### Respuestas y Ayuda

1. **Explicaciones claras**

   - Lenguaje simple y directo
   - Evitar jerga innecesaria
   - Proporcionar analogías cuando sea útil

2. **Código comentado**

   - Explicar cada paso importante
   - Destacar conceptos clave
   - Señalar posibles errores comunes

3. **Recursos adicionales**
   - Referencias a documentación oficial de Python
   - Artículos relevantes de calidad

---

## 📚 Referencias Oficiales

- **Python Documentation**: https://docs.python.org/3/
- **pytest Documentation**: https://docs.pytest.org/
- **uv Documentation**: https://docs.astral.sh/uv/
- **Docker Documentation**: https://docs.docker.com/
- **Real Python**: https://realpython.com/

---

## 🔗 Enlaces Importantes

- **Repositorio**: https://github.com/epti-dev/bc-python
- **Documentación general**: [\_docs/README.md](_docs/README.md)
- **Primera semana**: [bootcamp/week-01/README.md](bootcamp/week-01/README.md)

---

## ✅ Checklist para Nuevas Semanas

Cuando crees contenido para una nueva semana:

- [ ] Crear estructura de carpetas completa
- [ ] README.md con objetivos y estructura
- [ ] Material teórico en 1-teoria/
- [ ] Ejercicios guiados en 2-ejercicios/
- [ ] Proyecto integrador en 3-proyecto/
- [ ] Recursos adicionales en 4-recursos/
- [ ] Glosario de términos en 5-glosario/
- [ ] Rúbrica de evaluación
- [ ] Verificar coherencia con semanas anteriores
- [ ] Revisar progresión de dificultad
- [ ] Probar código de ejemplos

---

## 💡 Notas Finales

- **Prioridad**: Claridad sobre brevedad
- **Enfoque**: Aprendizaje práctico sobre teoría abstracta
- **Objetivo**: Preparar desarrolladores Python listos para trabajar
- **Filosofía**: Python moderno desde el día 1

---

_Última actualización: Enero 2026_
_Versión: 1.0_
