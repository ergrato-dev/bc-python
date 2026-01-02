"""
Sistema de Biblioteca - Punto de Entrada
========================================

Este archivo demuestra el uso del sistema de biblioteca.
Ejecuta este archivo para probar tu implementación.
"""

from models import Book, User, Loan
from library import Library


def main() -> None:
    """Función principal que demuestra el sistema."""

    print("=" * 60)
    print("📚 SISTEMA DE BIBLIOTECA")
    print("=" * 60)

    # ================================================
    # 1. Crear la biblioteca
    # ================================================
    print("\n--- 1. Creando biblioteca ---")
    library = Library("Biblioteca Central")
    print(f"Biblioteca creada: {library.name}")

    # ================================================
    # 2. Agregar libros
    # ================================================
    print("\n--- 2. Agregando libros ---")

    # Crear libros directamente
    book1 = Book(
        title="1984",
        author="George Orwell",
        isbn="978-0451524935",
        year=1949
    )

    book2 = Book(
        title="El Quijote",
        author="Miguel de Cervantes",
        isbn="978-8420412146",
        year=1605
    )

    # Crear libro desde diccionario (factory method)
    book3 = Book.from_dict({
        "title": "Python Crash Course",
        "author": "Eric Matthes",
        "isbn": "978-1593279288",
        "year": 2019
    })

    # Agregar a la biblioteca
    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)

    print(f"Libros agregados: {Book.total_books}")
    for book in library.get_available_books():
        print(f"  📗 {book}")

    # ================================================
    # 3. Registrar usuarios
    # ================================================
    print("\n--- 3. Registrando usuarios ---")

    user1 = User(
        name="Ana García",
        email="ana@email.com"
    )

    user2 = User.from_dict({
        "name": "Bob Smith",
        "email": "bob@email.com"
    })

    library.register_user(user1)
    library.register_user(user2)

    print(f"Usuarios registrados: {User.total_users}")
    print(f"  👤 {user1}")
    print(f"  👤 {user2}")

    # ================================================
    # 4. Realizar préstamos
    # ================================================
    print("\n--- 4. Realizando préstamos ---")

    # Ana pide prestado "1984"
    loan1 = library.borrow_book(user1.user_id, book1.isbn)
    if loan1:
        print(f"✅ Préstamo exitoso: {loan1}")

    # Bob pide prestado "El Quijote"
    loan2 = library.borrow_book(user2.user_id, book2.isbn)
    if loan2:
        print(f"✅ Préstamo exitoso: {loan2}")

    # Intentar prestar un libro no disponible
    print("\nIntentando prestar '1984' (ya prestado)...")
    loan3 = library.borrow_book(user2.user_id, book1.isbn)
    if not loan3:
        print("❌ No se pudo realizar el préstamo")

    # ================================================
    # 5. Ver estado de libros
    # ================================================
    print("\n--- 5. Estado de libros ---")

    available = library.get_available_books()
    print(f"Libros disponibles ({len(available)}):")
    for book in available:
        print(f"  📗 {book}")

    # ================================================
    # 6. Buscar libros
    # ================================================
    print("\n--- 6. Búsqueda de libros ---")

    results = library.search_books("Python")
    print(f"Resultados para 'Python': {len(results)}")
    for book in results:
        print(f"  📘 {book}")

    results = library.search_books("Orwell")
    print(f"\nResultados para 'Orwell': {len(results)}")
    for book in results:
        status = "📗 Disponible" if book.is_available else "📕 Prestado"
        print(f"  {status} {book}")

    # ================================================
    # 7. Devolver libro
    # ================================================
    print("\n--- 7. Devolviendo libro ---")

    if loan1:
        success = library.return_book(loan1.loan_id)
        if success:
            print(f"✅ Libro devuelto: {book1.title}")
            print(f"   {book1.title} disponible: {book1.is_available}")

    # ================================================
    # 8. Estadísticas
    # ================================================
    print("\n--- 8. Estadísticas ---")

    stats = library.get_statistics()
    print(f"📊 Estadísticas de {library.name}:")
    print(f"   Total libros: {stats['total_books']}")
    print(f"   Disponibles: {stats['available_books']}")
    print(f"   Prestados: {stats['borrowed_books']}")
    print(f"   Total usuarios: {stats['total_users']}")
    print(f"   Préstamos activos: {stats['active_loans']}")

    # ================================================
    # 9. Información de usuario
    # ================================================
    print("\n--- 9. Información de usuarios ---")

    print(f"\n{user1}")
    print(f"   Préstamos activos: {len(user1.active_loans)}")
    print(f"   Historial: {len(user1.loan_history)} préstamos")
    print(f"   ¿Puede pedir más? {user1.can_borrow()}")

    print(f"\n{user2}")
    print(f"   Préstamos activos: {len(user2.active_loans)}")
    for loan in user2.active_loans:
        print(f"     📖 {loan.book.title} - Vence en {loan.days_until_due()} días")

    print("\n" + "=" * 60)
    print("✅ Demostración completada")
    print("=" * 60)


if __name__ == "__main__":
    main()
