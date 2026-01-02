"""
Módulo de Análisis de Datos
===========================
Funciones para crear y analizar conjuntos de datos.
"""


def create_dataset(name: str, items: list[str]) -> set[str]:
    """
    Crea un conjunto de datos eliminando duplicados.

    Args:
        name: Nombre del dataset (para referencia)
        items: Lista de items (puede tener duplicados)

    Returns:
        Set con items únicos
    """
    # TODO: Implementar
    # 1. Convertir la lista a set para eliminar duplicados
    # 2. Retornar el set
    pass


def add_items(dataset: set[str], items: list[str]) -> int:
    """
    Agrega items al dataset.

    Args:
        dataset: Set existente
        items: Items a agregar

    Returns:
        Cantidad de items nuevos agregados
    """
    # TODO: Implementar
    # 1. Guardar el tamaño inicial
    # 2. Usar update() para agregar los items
    # 3. Retornar la diferencia de tamaños
    pass


def remove_items(dataset: set[str], items: list[str]) -> int:
    """
    Elimina items del dataset.

    Args:
        dataset: Set existente
        items: Items a eliminar

    Returns:
        Cantidad de items eliminados
    """
    # TODO: Implementar
    # 1. Guardar el tamaño inicial
    # 2. Usar discard() para cada item (no lanza error si no existe)
    # 3. Retornar la diferencia de tamaños
    pass


def analyze_datasets(
    dataset_a: set[str],
    dataset_b: set[str]
) -> dict[str, set[str] | float]:
    """
    Analiza dos conjuntos y retorna estadísticas.

    Args:
        dataset_a: Primer conjunto
        dataset_b: Segundo conjunto

    Returns:
        dict con:
        - common: elementos en ambos (intersección)
        - only_a: solo en A (diferencia A - B)
        - only_b: solo en B (diferencia B - A)
        - all_unique: todos los únicos (unión)
        - similarity: índice de Jaccard (|A∩B| / |A∪B|)
    """
    # TODO: Implementar
    # 1. Calcular intersección (A & B)
    # 2. Calcular diferencia A - B
    # 3. Calcular diferencia B - A
    # 4. Calcular unión (A | B)
    # 5. Calcular similitud de Jaccard: len(intersección) / len(unión)
    #    Cuidado: si unión está vacía, similitud es 0
    # 6. Retornar diccionario con todos los valores
    pass


def find_items_with_tags(
    items: dict[str, set[str]],
    required_tags: set[str],
    excluded_tags: set[str] | None = None
) -> list[str]:
    """
    Encuentra items que tienen todos los tags requeridos
    y ninguno de los tags excluidos.

    Args:
        items: Diccionario {nombre_item: set de tags}
        required_tags: Tags que DEBE tener el item
        excluded_tags: Tags que NO debe tener el item

    Returns:
        Lista de nombres de items que cumplen los criterios
    """
    # TODO: Implementar
    # 1. Si excluded_tags es None, usar set vacío
    # 2. Para cada item, verificar:
    #    - required_tags es subconjunto de los tags del item
    #    - tags del item son disjuntos con excluded_tags
    # 3. Retornar lista de items que cumplen ambas condiciones
    pass


def get_related_items(
    items: dict[str, set[str]],
    item_name: str,
    min_common_tags: int = 1
) -> list[tuple[str, int]]:
    """
    Encuentra items relacionados por tags comunes.

    Args:
        items: Diccionario {nombre_item: set de tags}
        item_name: Nombre del item de referencia
        min_common_tags: Mínimo de tags en común requeridos

    Returns:
        Lista de tuplas (nombre_item, cantidad_tags_comunes)
        ordenada por cantidad descendente
    """
    # TODO: Implementar
    # 1. Obtener los tags del item de referencia
    # 2. Si no existe, retornar lista vacía
    # 3. Para cada otro item, calcular intersección de tags
    # 4. Filtrar los que tienen >= min_common_tags
    # 5. Ordenar por cantidad de tags comunes (descendente)
    # 6. Retornar lista de tuplas (nombre, cantidad)
    pass


def generate_report(datasets: dict[str, set[str]]) -> str:
    """
    Genera un reporte de análisis de todos los datasets.

    Args:
        datasets: Diccionario {nombre_dataset: set de items}

    Returns:
        String con el reporte formateado
    """
    # TODO: Implementar
    # 1. Contar total de datasets
    # 2. Calcular unión de todos para total de elementos únicos
    # 3. Encontrar elemento más común (en más datasets)
    # 4. Formatear y retornar el reporte como string
    #
    # Formato esperado:
    # """
    #   Total datasets: X
    #   Total elementos únicos: Y
    #   Elemento más común: Z (en N datasets)
    # """
    pass
