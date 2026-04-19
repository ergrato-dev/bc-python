# Proyecto Semana 07: Analizador de Datos

## 🎯 Objetivo

Crear un **Analizador de Datos** que use sets para procesar y analizar colecciones de datos, aplicando operaciones de conjuntos y algoritmos de búsqueda y ordenamiento.

---

## 📋 Descripción

Desarrollarás un sistema que permita:

1. **Gestionar colecciones de datos** (usuarios, productos, tags)
2. **Analizar relaciones** entre conjuntos de datos
3. **Buscar elementos** eficientemente
4. **Ordenar y filtrar** datos con diferentes criterios
5. **Generar reportes** de análisis

---

## 🛠️ Funcionalidades Requeridas

### 1. Gestión de Conjuntos de Datos

```python
def create_dataset(name: str, items: list[str]) -> set[str]:
    """Crea un conjunto de datos eliminando duplicados."""
    pass

def add_items(dataset: set[str], items: list[str]) -> int:
    """Agrega items y retorna cantidad de nuevos agregados."""
    pass

def remove_items(dataset: set[str], items: list[str]) -> int:
    """Elimina items y retorna cantidad eliminados."""
    pass
```

### 2. Análisis de Conjuntos

```python
def analyze_datasets(
    dataset_a: set[str],
    dataset_b: set[str]
) -> dict[str, set[str] | int]:
    """
    Analiza dos conjuntos y retorna:
    - common: elementos en ambos
    - only_a: solo en A
    - only_b: solo en B
    - all_unique: todos los únicos
    - similarity: porcentaje de similitud (Jaccard)
    """
    pass
```

### 3. Sistema de Tags/Etiquetas

```python
def find_items_with_tags(
    items: dict[str, set[str]],
    required_tags: set[str],
    excluded_tags: set[str] | None = None
) -> list[str]:
    """Encuentra items que tienen todos los tags requeridos."""
    pass

def get_related_items(
    items: dict[str, set[str]],
    item_name: str,
    min_common_tags: int = 1
) -> list[tuple[str, int]]:
    """Encuentra items relacionados por tags comunes."""
    pass
```

### 4. Búsqueda y Ordenamiento

```python
def search_items(
    items: list[str],
    query: str,
    sorted_list: bool = False
) -> list[str]:
    """
    Busca items que contengan el query.
    Si sorted_list=True, usa búsqueda binaria optimizada.
    """
    pass

def sort_by_criteria(
    items: list[dict],
    criteria: list[tuple[str, bool]]
) -> list[dict]:
    """
    Ordena por múltiples criterios.
    criteria: lista de (campo, descendente)
    """
    pass
```

### 5. Reportes

```python
def generate_report(
    datasets: dict[str, set[str]]
) -> str:
    """Genera un reporte de análisis de todos los datasets."""
    pass
```

---

## 📁 Estructura del Proyecto

```
3-proyecto/
├── README.md
├── starter/
│   ├── main.py           # Punto de entrada
│   ├── analyzer.py       # Funciones de análisis
│   ├── search.py         # Búsqueda y ordenamiento
│   └── data/
│       └── sample.py     # Datos de ejemplo
└── solution/             # ⚠️ Solo instructores
```

---

## 🧪 Ejemplo de Uso

```python
# Crear datasets
users_premium = create_dataset("premium", ["alice", "bob", "carol", "alice"])
users_active = create_dataset("active", ["bob", "carol", "david", "eve"])

# Analizar
analysis = analyze_datasets(users_premium, users_active)
print(f"Usuarios premium Y activos: {analysis['common']}")
print(f"Solo premium: {analysis['only_a']}")
print(f"Similitud: {analysis['similarity']:.1%}")

# Sistema de tags
products = {
    "laptop": {"electronics", "computers", "portable"},
    "phone": {"electronics", "mobile", "portable"},
    "desk": {"furniture", "office"},
    "headphones": {"electronics", "audio", "portable"},
}

# Buscar productos electrónicos y portátiles
found = find_items_with_tags(
    products,
    required_tags={"electronics", "portable"}
)
print(f"Electrónicos portátiles: {found}")  # ['laptop', 'phone', 'headphones']

# Productos relacionados con laptop
related = get_related_items(products, "laptop", min_common_tags=2)
print(f"Relacionados con laptop: {related}")  # [('phone', 2), ('headphones', 2)]
```

---

## 📊 Salida Esperada

```
╔══════════════════════════════════════════════════════════════╗
║                    ANALIZADOR DE DATOS                       ║
╚══════════════════════════════════════════════════════════════╝

📊 ANÁLISIS DE USUARIOS
────────────────────────────────────────────────────────────────
  Dataset 'premium': 3 elementos
  Dataset 'active': 4 elementos

  ∩ Comunes: {'bob', 'carol'}
  ∪ Total únicos: {'alice', 'bob', 'carol', 'david', 'eve'}
  - Solo premium: {'alice'}
  - Solo active: {'david', 'eve'}
  📈 Similitud (Jaccard): 40.0%

🏷️ SISTEMA DE TAGS
────────────────────────────────────────────────────────────────
  Productos con tags {'electronics', 'portable'}:
    • laptop
    • phone
    • headphones

  Relacionados con 'laptop' (mín. 2 tags comunes):
    • phone (2 tags)
    • headphones (2 tags)

🔍 BÚSQUEDA Y ORDENAMIENTO
────────────────────────────────────────────────────────────────
  Búsqueda 'pro' en productos:
    • laptop_pro
    • headphones_pro

  Top 3 por ventas (descendente):
    1. phone: 150 ventas
    2. laptop: 120 ventas
    3. headphones: 80 ventas

📋 REPORTE GENERADO
────────────────────────────────────────────────────────────────
  Total datasets: 2
  Total elementos únicos: 5
  Elemento más común: bob (en 2 datasets)
```

---

## ✅ Criterios de Evaluación

| Criterio | Puntos | Descripción |
|----------|--------|-------------|
| Funcionalidad | 40% | Todas las funciones trabajan correctamente |
| Uso de Sets | 25% | Uso apropiado de operaciones de conjuntos |
| Algoritmos | 20% | Implementación correcta de búsqueda/ordenamiento |
| Código Limpio | 15% | Type hints, docstrings, nombres claros |

---

## 💡 Tips

- Usa `frozenset` cuando necesites sets como claves de diccionario
- El índice de Jaccard se calcula: `|A ∩ B| / |A ∪ B|`
- Para búsqueda binaria, la lista debe estar ordenada
- Usa `sorted()` con `key=lambda` para múltiples criterios

---

## 🚀 Extensiones Opcionales

1. **Persistencia**: Guardar/cargar datasets en JSON
2. **Visualización**: Mostrar diagramas de Venn en ASCII
3. **Caché**: Implementar caché de resultados con frozenset como clave
4. **CLI**: Interfaz de línea de comandos interactiva

---

## 🔗 Navegación

- ⬅️ **Ejercicios**: [03-algoritmos-basicos](../2-ejercicios/03-algoritmos-basicos/)
- 🏠 **Volver al índice**: [README](../README.md)
