"""
Proyecto Semana 6: Gestor de Contactos
======================================
Sistema de gestión de contactos usando diccionarios.

Instrucciones:
1. Lee cada función y su docstring
2. Implementa el código donde dice TODO
3. Ejecuta el archivo para probar tu implementación
4. Los tests al final verifican tu código
"""

from datetime import date

# ============================================
# ESTRUCTURA DE DATOS GLOBAL
# ============================================

# Almacén de contactos: {id: {datos del contacto}}
contacts: dict[int, dict[str, str | int | list[str]]] = {}

# Contador para generar IDs únicos
next_id: int = 1


# ============================================
# FUNCIONES CRUD
# ============================================

def create_contact(
    name: str,
    email: str,
    phone: str = "",
    tags: list[str] | None = None,
    notes: str = ""
) -> dict[str, str | int | list[str]] | None:
    """
    Crea un nuevo contacto y lo agrega a la agenda.

    Args:
        name: Nombre completo del contacto
        email: Email del contacto (debe ser único)
        phone: Número de teléfono (opcional)
        tags: Lista de etiquetas (opcional)
        notes: Notas adicionales (opcional)

    Returns:
        dict: El contacto creado, o None si el email ya existe

    Example:
        >>> create_contact("Alice", "alice@example.com", tags=["work"])
        {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', ...}
    """
    global next_id, contacts

    # TODO: Implementar
    # 1. Verificar que el email no exista ya (usar search_by_email)
    # 2. Crear diccionario del contacto con todos los campos
    # 3. Usar next_id como ID y luego incrementarlo
    # 4. Agregar contacto al diccionario contacts
    # 5. Retornar el contacto creado
    pass


def get_contact(contact_id: int) -> dict[str, str | int | list[str]] | None:
    """
    Obtiene un contacto por su ID.

    Args:
        contact_id: ID del contacto a buscar

    Returns:
        dict: El contacto si existe, None si no existe
    """
    # TODO: Implementar
    # Usar .get() para retornar None si no existe
    pass


def update_contact(contact_id: int, **kwargs) -> dict[str, str | int | list[str]] | None:
    """
    Actualiza los campos de un contacto existente.

    Args:
        contact_id: ID del contacto a actualizar
        **kwargs: Campos a actualizar (name, email, phone, notes)

    Returns:
        dict: El contacto actualizado, o None si no existe

    Example:
        >>> update_contact(1, phone="+1-555-9999", notes="Updated")
        {'id': 1, 'name': 'Alice', 'phone': '+1-555-9999', ...}
    """
    # TODO: Implementar
    # 1. Verificar que el contacto existe
    # 2. Si se actualiza email, verificar que no esté duplicado
    # 3. Actualizar solo los campos proporcionados en kwargs
    # 4. No permitir actualizar 'id' ni 'created_at'
    # 5. Retornar el contacto actualizado
    pass


def delete_contact(contact_id: int) -> bool:
    """
    Elimina un contacto por su ID.

    Args:
        contact_id: ID del contacto a eliminar

    Returns:
        bool: True si se eliminó, False si no existía
    """
    # TODO: Implementar
    # Usar pop() con valor por defecto para manejar caso de no existencia
    pass


# ============================================
# FUNCIONES DE BÚSQUEDA
# ============================================

def search_by_name(name: str) -> list[dict[str, str | int | list[str]]]:
    """
    Busca contactos cuyo nombre contenga el texto dado (case-insensitive).

    Args:
        name: Texto a buscar en el nombre

    Returns:
        list: Lista de contactos que coinciden

    Example:
        >>> search_by_name("ali")
        [{'id': 1, 'name': 'Alice Johnson', ...}]
    """
    # TODO: Implementar
    # Usar list comprehension para filtrar
    # La búsqueda debe ser case-insensitive (usar .lower())
    pass


def search_by_email(email: str) -> dict[str, str | int | list[str]] | None:
    """
    Busca un contacto por email exacto.

    Args:
        email: Email a buscar

    Returns:
        dict: El contacto si existe, None si no existe
    """
    # TODO: Implementar
    # Recorrer contacts.values() y buscar coincidencia exacta
    pass


def search_by_tag(tag: str) -> list[dict[str, str | int | list[str]]]:
    """
    Busca contactos que tengan una etiqueta específica.

    Args:
        tag: Etiqueta a buscar

    Returns:
        list: Lista de contactos con esa etiqueta
    """
    # TODO: Implementar
    # Filtrar contactos donde tag esté en la lista de tags
    pass


# ============================================
# FUNCIONES DE ETIQUETAS
# ============================================

def add_tag(contact_id: int, tag: str) -> bool:
    """
    Agrega una etiqueta a un contacto.

    Args:
        contact_id: ID del contacto
        tag: Etiqueta a agregar

    Returns:
        bool: True si se agregó, False si no existe el contacto o ya tenía la etiqueta
    """
    # TODO: Implementar
    # 1. Verificar que el contacto existe
    # 2. Verificar que la etiqueta no esté ya en el contacto
    # 3. Agregar la etiqueta a la lista
    pass


def remove_tag(contact_id: int, tag: str) -> bool:
    """
    Elimina una etiqueta de un contacto.

    Args:
        contact_id: ID del contacto
        tag: Etiqueta a eliminar

    Returns:
        bool: True si se eliminó, False si no existe contacto o no tenía la etiqueta
    """
    # TODO: Implementar
    # 1. Verificar que el contacto existe
    # 2. Verificar que la etiqueta está en el contacto
    # 3. Eliminar la etiqueta de la lista
    pass


def get_all_tags() -> list[str]:
    """
    Obtiene todas las etiquetas únicas de todos los contactos.

    Returns:
        list: Lista ordenada de etiquetas únicas
    """
    # TODO: Implementar
    # 1. Recopilar todas las etiquetas de todos los contactos
    # 2. Usar set para eliminar duplicados
    # 3. Retornar como lista ordenada
    pass


def get_contacts_by_tag() -> dict[str, list[dict[str, str | int | list[str]]]]:
    """
    Agrupa todos los contactos por etiqueta.

    Returns:
        dict: Diccionario donde clave es etiqueta y valor es lista de contactos

    Example:
        >>> get_contacts_by_tag()
        {'work': [contact1, contact2], 'personal': [contact2, contact3], ...}
    """
    # TODO: Implementar
    # 1. Crear diccionario vacío para resultado
    # 2. Recorrer todos los contactos
    # 3. Para cada etiqueta del contacto, agregarlo a la lista correspondiente
    # Tip: usar setdefault() para inicializar listas
    pass


# ============================================
# FUNCIONES DE EXPORTACIÓN Y ESTADÍSTICAS
# ============================================

def export_summary() -> str:
    """
    Genera un resumen formateado de todos los contactos.

    Returns:
        str: Resumen en formato texto

    Example output:
        === AGENDA DE CONTACTOS ===
        Total: 2 contactos

        [1] Alice Johnson
            📧 alice@example.com
            📱 +1-555-0101
            🏷️ work, important
            📝 Project manager

        [2] Bob Smith
            📧 bob@example.com
            ...
    """
    # TODO: Implementar
    # 1. Crear header con total de contactos
    # 2. Para cada contacto, formatear sus datos
    # 3. Usar emojis para mejor visualización
    # 4. Retornar string completo
    pass


def get_statistics() -> dict[str, int | float | str]:
    """
    Calcula estadísticas de la agenda.

    Returns:
        dict: Estadísticas de la agenda
            - total_contacts: Número total de contactos
            - total_tags: Número de etiquetas únicas
            - contacts_with_phone: Contactos con teléfono
            - contacts_with_notes: Contactos con notas
            - most_common_tag: Etiqueta más usada
            - avg_tags_per_contact: Promedio de etiquetas por contacto
    """
    # TODO: Implementar
    # 1. Contar total de contactos
    # 2. Contar etiquetas únicas
    # 3. Contar contactos con teléfono (phone no vacío)
    # 4. Contar contactos con notas (notes no vacío)
    # 5. Encontrar etiqueta más común
    # 6. Calcular promedio de etiquetas por contacto
    pass


# ============================================
# FUNCIÓN AUXILIAR PARA LIMPIAR DATOS
# ============================================

def clear_all() -> None:
    """Limpia todos los contactos y reinicia el contador de IDs."""
    global contacts, next_id
    contacts = {}
    next_id = 1


# ============================================
# TESTS Y DEMOSTRACIÓN
# ============================================

def run_tests() -> None:
    """Ejecuta tests para verificar la implementación."""
    print("=" * 50)
    print("🧪 EJECUTANDO TESTS")
    print("=" * 50)

    # Limpiar datos antes de tests
    clear_all()

    # Test 1: Crear contactos
    print("\n📝 Test 1: Crear contactos")
    c1 = create_contact("Alice Johnson", "alice@example.com", "+1-555-0101", ["work", "important"])
    c2 = create_contact("Bob Smith", "bob@example.com", "+1-555-0102", ["personal", "family"])
    c3 = create_contact("Carol White", "carol@example.com", tags=["work"])

    assert c1 is not None, "❌ Falló crear contacto 1"
    assert c1["id"] == 1, "❌ ID incorrecto para contacto 1"
    assert c2 is not None, "❌ Falló crear contacto 2"
    assert c3 is not None, "❌ Falló crear contacto 3"
    print("✅ Contactos creados correctamente")

    # Test 2: No permitir email duplicado
    print("\n📝 Test 2: Email duplicado")
    c_dup = create_contact("Alice Clone", "alice@example.com")
    assert c_dup is None, "❌ Permitió email duplicado"
    print("✅ Email duplicado rechazado correctamente")

    # Test 3: Obtener contacto
    print("\n📝 Test 3: Obtener contacto")
    contact = get_contact(1)
    assert contact is not None, "❌ No encontró contacto 1"
    assert contact["name"] == "Alice Johnson", "❌ Nombre incorrecto"
    assert get_contact(999) is None, "❌ Debería retornar None para ID inexistente"
    print("✅ Get contact funciona correctamente")

    # Test 4: Buscar por nombre
    print("\n📝 Test 4: Buscar por nombre")
    results = search_by_name("alice")
    assert len(results) == 1, "❌ Búsqueda por nombre falló"
    assert results[0]["name"] == "Alice Johnson", "❌ Resultado incorrecto"
    results_case = search_by_name("ALICE")
    assert len(results_case) == 1, "❌ Búsqueda case-insensitive falló"
    print("✅ Búsqueda por nombre funciona correctamente")

    # Test 5: Buscar por email
    print("\n📝 Test 5: Buscar por email")
    found = search_by_email("bob@example.com")
    assert found is not None, "❌ No encontró por email"
    assert found["name"] == "Bob Smith", "❌ Email incorrecto"
    print("✅ Búsqueda por email funciona correctamente")

    # Test 6: Buscar por etiqueta
    print("\n📝 Test 6: Buscar por etiqueta")
    work_contacts = search_by_tag("work")
    assert len(work_contacts) == 2, "❌ Búsqueda por tag falló"
    print("✅ Búsqueda por etiqueta funciona correctamente")

    # Test 7: Actualizar contacto
    print("\n📝 Test 7: Actualizar contacto")
    updated = update_contact(1, phone="+1-555-9999", notes="Updated contact")
    assert updated is not None, "❌ Actualización falló"
    assert updated["phone"] == "+1-555-9999", "❌ Teléfono no actualizado"
    assert updated["notes"] == "Updated contact", "❌ Notas no actualizadas"
    print("✅ Actualización funciona correctamente")

    # Test 8: Agregar/eliminar etiqueta
    print("\n📝 Test 8: Gestión de etiquetas")
    assert add_tag(1, "vip") is True, "❌ No agregó etiqueta"
    assert "vip" in get_contact(1)["tags"], "❌ Etiqueta no está en contacto"
    assert add_tag(1, "vip") is False, "❌ Permitió etiqueta duplicada"
    assert remove_tag(1, "vip") is True, "❌ No eliminó etiqueta"
    assert "vip" not in get_contact(1)["tags"], "❌ Etiqueta aún en contacto"
    print("✅ Gestión de etiquetas funciona correctamente")

    # Test 9: Obtener todas las etiquetas
    print("\n📝 Test 9: Obtener todas las etiquetas")
    all_tags = get_all_tags()
    assert "work" in all_tags, "❌ Falta etiqueta 'work'"
    assert "personal" in all_tags, "❌ Falta etiqueta 'personal'"
    print(f"✅ Etiquetas encontradas: {all_tags}")

    # Test 10: Agrupar por etiqueta
    print("\n📝 Test 10: Agrupar por etiqueta")
    by_tag = get_contacts_by_tag()
    assert "work" in by_tag, "❌ Falta grupo 'work'"
    assert len(by_tag["work"]) == 2, "❌ Cantidad incorrecta en 'work'"
    print("✅ Agrupación por etiqueta funciona correctamente")

    # Test 11: Eliminar contacto
    print("\n📝 Test 11: Eliminar contacto")
    assert delete_contact(3) is True, "❌ No eliminó contacto"
    assert get_contact(3) is None, "❌ Contacto aún existe"
    assert delete_contact(3) is False, "❌ Debería retornar False"
    print("✅ Eliminación funciona correctamente")

    # Test 12: Estadísticas
    print("\n📝 Test 12: Estadísticas")
    stats = get_statistics()
    assert stats is not None, "❌ Estadísticas retornó None"
    assert stats["total_contacts"] == 2, "❌ Total de contactos incorrecto"
    print(f"✅ Estadísticas: {stats}")

    # Test 13: Exportar resumen
    print("\n📝 Test 13: Exportar resumen")
    summary = export_summary()
    assert summary is not None, "❌ Export retornó None"
    assert "Alice Johnson" in summary, "❌ Falta Alice en resumen"
    print("✅ Exportación funciona correctamente")
    print("\n" + summary)

    print("\n" + "=" * 50)
    print("🎉 TODOS LOS TESTS PASARON")
    print("=" * 50)


if __name__ == "__main__":
    run_tests()
