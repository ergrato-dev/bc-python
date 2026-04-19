# 🧪 Proyecto: Suite de Tests para Calculadora Científica

## 📋 Descripción

En este proyecto desarrollarás una **suite completa de tests** para una calculadora científica. Aplicarás todos los conceptos aprendidos: tests unitarios, fixtures, parametrización, mocking y medición de cobertura.

La calculadora ya está implementada. Tu trabajo es escribir tests que:
- Verifiquen todas las operaciones
- Cubran casos límite (edge cases)
- Manejen errores correctamente
- Alcancen **> 90% de cobertura**

---

## 🎯 Objetivos de Aprendizaje

Al completar este proyecto serás capaz de:

- ✅ Diseñar una estrategia de testing completa
- ✅ Escribir tests unitarios efectivos con pytest
- ✅ Usar fixtures para reducir duplicación
- ✅ Aplicar parametrización para múltiples casos
- ✅ Mockear dependencias externas
- ✅ Medir y mejorar cobertura de código
- ✅ Organizar tests de forma profesional

---

## 📁 Estructura del Proyecto

```
3-proyecto/
├── README.md                 # Este archivo
├── starter/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── calculator.py     # Calculadora científica
│   │   ├── memory.py         # Sistema de memoria
│   │   └── history.py        # Historial de operaciones
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py       # Fixtures (parcialmente completo)
│   │   ├── test_basic_ops.py # TODO: Completar
│   │   ├── test_scientific.py# TODO: Completar
│   │   ├── test_memory.py    # TODO: Completar
│   │   └── test_history.py   # TODO: Completar
│   └── pyproject.toml
└── solution/                 # ⚠️ Solo para instructores
```

---

## 🔬 La Calculadora Científica

### Operaciones Básicas
- `add(a, b)` - Suma
- `subtract(a, b)` - Resta
- `multiply(a, b)` - Multiplicación
- `divide(a, b)` - División (lanza `ZeroDivisionError`)

### Operaciones Científicas
- `power(base, exp)` - Potencia
- `sqrt(n)` - Raíz cuadrada (lanza `ValueError` si n < 0)
- `factorial(n)` - Factorial (lanza `ValueError` si n < 0 o no es entero)
- `sin(x)`, `cos(x)`, `tan(x)` - Funciones trigonométricas (en radianes)
- `log(x, base)` - Logaritmo (lanza `ValueError` si x <= 0)
- `ln(x)` - Logaritmo natural

### Sistema de Memoria
- `memory_store(value)` - Guardar en memoria
- `memory_recall()` - Recuperar de memoria
- `memory_clear()` - Limpiar memoria
- `memory_add(value)` - Sumar a memoria

### Historial
- `get_history()` - Obtener historial de operaciones
- `clear_history()` - Limpiar historial
- `export_history(format)` - Exportar (json, csv)

---

## 📝 Requisitos del Proyecto

### 1. Tests Básicos (25 puntos)
- [ ] Tests para `add`, `subtract`, `multiply`, `divide`
- [ ] Tests con números positivos, negativos, cero
- [ ] Tests con flotantes
- [ ] Test de división por cero

### 2. Tests Científicos (25 puntos)
- [ ] Tests para `sqrt`, `power`, `factorial`
- [ ] Tests para funciones trigonométricas
- [ ] Tests para logaritmos
- [ ] Tests de errores (ValueError para inputs inválidos)

### 3. Tests de Memoria (15 puntos)
- [ ] Tests para store/recall/clear
- [ ] Tests para memory_add
- [ ] Test de memoria vacía

### 4. Tests de Historial (15 puntos)
- [ ] Tests para registro de operaciones
- [ ] Tests para clear_history
- [ ] Tests para export (json, csv)

### 5. Calidad (20 puntos)
- [ ] Cobertura > 90%
- [ ] Uso de fixtures
- [ ] Uso de parametrización
- [ ] Tests bien organizados y documentados

---

## 🚀 Instrucciones

### Paso 1: Configurar el Proyecto

```bash
cd starter

# Instalar dependencias
uv sync

# Verificar que la calculadora funciona
uv run python -c "from src.calculator import ScientificCalculator; c = ScientificCalculator(); print(c.add(2, 3))"
```

### Paso 2: Explorar el Código

Revisa los archivos en `src/` para entender:
- Qué métodos existen
- Qué excepciones pueden lanzar
- Cómo interactúan los componentes

### Paso 3: Completar los Tests

Abre cada archivo de test y completa los TODOs:

1. **test_basic_ops.py**: Operaciones aritméticas básicas
2. **test_scientific.py**: Funciones científicas
3. **test_memory.py**: Sistema de memoria
4. **test_history.py**: Historial de operaciones

### Paso 4: Ejecutar y Verificar

```bash
# Ejecutar todos los tests
uv run pytest -v

# Ejecutar con cobertura
uv run pytest --cov=src --cov-report=term-missing

# Generar reporte HTML
uv run pytest --cov=src --cov-report=html
# Abrir htmlcov/index.html

# Verificar cobertura mínima
uv run pytest --cov=src --cov-fail-under=90
```

---

## 💡 Tips

### Usa Fixtures para la Calculadora

```python
@pytest.fixture
def calculator():
    return ScientificCalculator()

def test_add(calculator):
    assert calculator.add(2, 3) == 5
```

### Parametriza Casos Similares

```python
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
])
def test_add(calculator, a, b, expected):
    assert calculator.add(a, b) == expected
```

### Usa pytest.approx para Flotantes

```python
def test_sin_of_pi(calculator):
    import math
    result = calculator.sin(math.pi)
    assert result == pytest.approx(0, abs=1e-10)
```

### Agrupa Tests Relacionados

```python
class TestTrigonometry:
    def test_sin(self, calculator):
        ...

    def test_cos(self, calculator):
        ...
```

---

## 📊 Criterios de Evaluación

| Criterio | Puntos | Descripción |
|----------|--------|-------------|
| Tests básicos | 25 | Cobertura de operaciones aritméticas |
| Tests científicos | 25 | Cobertura de funciones científicas |
| Tests memoria | 15 | Tests del sistema de memoria |
| Tests historial | 15 | Tests del historial |
| Cobertura > 90% | 10 | Medido con pytest-cov |
| Calidad de tests | 10 | Fixtures, parametrización, organización |
| **Total** | **100** | |

### Escala de Cobertura
- 95-100%: 10 puntos
- 90-94%: 8 puntos
- 85-89%: 6 puntos
- 80-84%: 4 puntos
- < 80%: 2 puntos

---

## 📚 Recursos

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Python math Module](https://docs.python.org/3/library/math.html)

---

## ⏱️ Tiempo Estimado

- **Exploración del código**: 15 minutos
- **Tests básicos**: 30 minutos
- **Tests científicos**: 30 minutos
- **Tests memoria/historial**: 20 minutos
- **Mejorar cobertura**: 15 minutos
- **Total**: ~2 horas
