"""
Proyecto Semana 07: Analizador de Datos
=======================================
Sistema de análisis de datos usando sets y algoritmos.

Instrucciones:
1. Completa las funciones marcadas con TODO
2. Sigue los type hints y docstrings
3. Ejecuta main.py para probar tu implementación
"""

from analyzer import (
    create_dataset,
    add_items,
    remove_items,
    analyze_datasets,
    find_items_with_tags,
    get_related_items,
    generate_report,
)
from search import (
    search_items,
    sort_by_criteria,
    binary_search,
)
from data.sample import SAMPLE_PRODUCTS, SAMPLE_SALES


def main() -> None:
    """Función principal del analizador."""
    print("╔" + "═" * 62 + "╗")
    print("║" + "ANALIZADOR DE DATOS".center(62) + "║")
    print("╚" + "═" * 62 + "╝")
    print()

    # ─────────────────────────────────────────────────────────────
    # 1. ANÁLISIS DE USUARIOS
    # ─────────────────────────────────────────────────────────────
    print("📊 ANÁLISIS DE USUARIOS")
    print("─" * 64)

    # Crear datasets de usuarios
    users_premium = create_dataset(
        "premium",
        ["alice", "bob", "carol", "alice", "bob"]  # Con duplicados
    )
    users_active = create_dataset(
        "active",
        ["bob", "carol", "david", "eve", "david"]
    )

    print(f"  Dataset 'premium': {len(users_premium)} elementos")
    print(f"  Dataset 'active': {len(users_active)} elementos")
    print()

    # Analizar relación entre datasets
    analysis = analyze_datasets(users_premium, users_active)

    print(f"  ∩ Comunes: {analysis['common']}")
    print(f"  ∪ Total únicos: {analysis['all_unique']}")
    print(f"  - Solo premium: {analysis['only_a']}")
    print(f"  - Solo active: {analysis['only_b']}")
    print(f"  📈 Similitud (Jaccard): {analysis['similarity']:.1%}")
    print()

    # ─────────────────────────────────────────────────────────────
    # 2. SISTEMA DE TAGS
    # ─────────────────────────────────────────────────────────────
    print("🏷️  SISTEMA DE TAGS")
    print("─" * 64)

    # Buscar productos con tags específicos
    required = {"electronics", "portable"}
    found = find_items_with_tags(
        SAMPLE_PRODUCTS,
        required_tags=required,
        excluded_tags={"audio"}
    )

    print(f"  Productos con tags {required} (sin 'audio'):")
    for item in found:
        print(f"    • {item}")
    print()

    # Encontrar productos relacionados
    related = get_related_items(SAMPLE_PRODUCTS, "laptop", min_common_tags=2)

    print("  Relacionados con 'laptop' (mín. 2 tags comunes):")
    for item, count in related:
        print(f"    • {item} ({count} tags)")
    print()

    # ─────────────────────────────────────────────────────────────
    # 3. BÚSQUEDA Y ORDENAMIENTO
    # ─────────────────────────────────────────────────────────────
    print("🔍 BÚSQUEDA Y ORDENAMIENTO")
    print("─" * 64)

    # Lista de productos para búsqueda
    product_names = [
        "laptop_basic", "laptop_pro", "phone_basic",
        "phone_pro", "headphones_basic", "headphones_pro",
        "tablet_mini", "tablet_pro"
    ]

    # Búsqueda de productos que contengan "pro"
    results = search_items(product_names, "pro")
    print("  Búsqueda 'pro' en productos:")
    for item in results:
        print(f"    • {item}")
    print()

    # Ordenar ventas por múltiples criterios
    sorted_sales = sort_by_criteria(
        SAMPLE_SALES,
        criteria=[("sales", True), ("name", False)]  # sales desc, name asc
    )

    print("  Top 3 por ventas (descendente):")
    for i, item in enumerate(sorted_sales[:3], 1):
        print(f"    {i}. {item['name']}: {item['sales']} ventas")
    print()

    # ─────────────────────────────────────────────────────────────
    # 4. REPORTE
    # ─────────────────────────────────────────────────────────────
    print("📋 REPORTE GENERADO")
    print("─" * 64)

    datasets = {
        "premium": users_premium,
        "active": users_active,
    }
    report = generate_report(datasets)
    print(report)


if __name__ == "__main__":
    main()
