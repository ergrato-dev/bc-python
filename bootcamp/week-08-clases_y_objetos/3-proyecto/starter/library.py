"""
Clase Library - Gestiona la biblioteca.

TODO: Implementa esta clase siguiendo las instrucciones del README.
"""

from models import Book, User, Loan


class Library:
    """Gestiona una biblioteca con libros, usuarios y préstamos."""

    def __init__(self, name: str) -> None:
        """
        Inicializa una nueva biblioteca.

        Args:
            name: Nombre de la biblioteca
        """
        # TODO: Asignar name
        # TODO: Inicializar books como dict vacío (isbn -> Book)
        # TODO: Inicializar users como dict vacío (user_id -> User)
        # TODO: Inicializar loans como lista vacía
        pass

    def add_book(self, book: Book) -> bool:
        """
        Agrega un libro a la biblioteca.

        Args:
            book: Libro a agregar

        Returns:
            True si se agregó, False si ya existía
        """
        # TODO: Verificar si el ISBN ya existe
        # TODO: Agregar al diccionario books
        pass

    def remove_book(self, isbn: str) -> bool:
        """
        Elimina un libro de la biblioteca.

        Solo se puede eliminar si está disponible (no prestado).

        Args:
            isbn: ISBN del libro a eliminar

        Returns:
            True si se eliminó, False si no existe o está prestado
        """
        # TODO: Verificar si existe y está disponible
        # TODO: Eliminar del diccionario
        pass

    def register_user(self, user: User) -> bool:
        """
        Registra un nuevo usuario.

        Args:
            user: Usuario a registrar

        Returns:
            True si se registró, False si ya existía
        """
        # TODO: Verificar si el user_id ya existe
        # TODO: Agregar al diccionario users
        pass

    def borrow_book(self, user_id: str, isbn: str) -> Loan | None:
        """
        Procesa un préstamo de libro.

        Args:
            user_id: ID del usuario
            isbn: ISBN del libro

        Returns:
            Loan si fue exitoso, None si falló
        """
        # TODO: Verificar que el usuario existe
        # TODO: Verificar que el libro existe
        # TODO: Verificar que el usuario puede pedir préstamos (can_borrow)
        # TODO: Verificar que el libro está disponible
        # TODO: Crear el préstamo (Loan)
        # TODO: Marcar libro como no disponible
        # TODO: Agregar préstamo al usuario
        # TODO: Agregar préstamo a la lista de préstamos
        # TODO: Retornar el préstamo
        pass

    def return_book(self, loan_id: str) -> bool:
        """
        Procesa la devolución de un libro.

        Args:
            loan_id: ID del préstamo

        Returns:
            True si fue exitoso, False si no se encontró
        """
        # TODO: Buscar el préstamo por loan_id
        # TODO: Marcar el préstamo como devuelto (complete_return)
        # TODO: Marcar el libro como disponible
        # TODO: Actualizar préstamos del usuario (return_loan)
        pass

    def search_books(self, query: str) -> list[Book]:
        """
        Busca libros por título o autor.

        Args:
            query: Texto a buscar (case-insensitive)

        Returns:
            Lista de libros que coinciden
        """
        # TODO: Buscar en título y autor
        # TODO: Búsqueda case-insensitive
        pass

    def get_available_books(self) -> list[Book]:
        """
        Obtiene lista de libros disponibles.

        Returns:
            Lista de libros con is_available=True
        """
        # TODO: Filtrar libros disponibles
        pass

    def get_overdue_loans(self) -> list[Loan]:
        """
        Obtiene lista de préstamos vencidos.

        Returns:
            Lista de préstamos que están vencidos
        """
        # TODO: Filtrar préstamos usando is_overdue()
        pass

    def get_statistics(self) -> dict:
        """
        Genera estadísticas de la biblioteca.

        Returns:
            Dict con:
            - total_books: Total de libros
            - available_books: Libros disponibles
            - borrowed_books: Libros prestados
            - total_users: Total de usuarios
            - active_loans: Préstamos activos (no devueltos)
            - overdue_loans: Préstamos vencidos
        """
        # TODO: Calcular todas las estadísticas
        pass
