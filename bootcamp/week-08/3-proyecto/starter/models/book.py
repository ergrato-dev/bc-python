"""
Clase Book - Representa un libro en la biblioteca.

TODO: Implementa esta clase siguiendo las instrucciones del README.
"""

from datetime import date


class Book:
    """Representa un libro en la biblioteca."""

    # Atributo de clase: contador de libros
    total_books: int = 0

    def __init__(
        self,
        title: str,
        author: str,
        isbn: str,
        year: int
    ) -> None:
        """
        Inicializa un nuevo libro.

        Args:
            title: Título del libro
            author: Nombre del autor
            isbn: Código ISBN
            year: Año de publicación

        Raises:
            ValueError: Si el ISBN no es válido
        """
        # TODO: Validar ISBN usando el método estático
        # TODO: Asignar atributos de instancia
        # TODO: Incrementar contador de clase
        pass

    def __str__(self) -> str:
        """
        Retorna representación legible.

        Formato: "Título por Autor (Año)"
        Ejemplo: "1984 por George Orwell (1949)"
        """
        # TODO: Implementar
        pass

    def __repr__(self) -> str:
        """
        Retorna representación técnica.

        Formato: Book(title='...', author='...', isbn='...', year=...)
        """
        # TODO: Implementar
        pass

    def __eq__(self, other: object) -> bool:
        """
        Compara igualdad por ISBN.

        Dos libros son iguales si tienen el mismo ISBN.
        """
        # TODO: Implementar
        # Recuerda verificar isinstance y retornar NotImplemented si no es Book
        pass

    def __hash__(self) -> int:
        """Permite usar Book en sets y como key de dict."""
        # TODO: Implementar usando el ISBN
        pass

    def get_age(self) -> int:
        """
        Calcula la antigüedad del libro en años.

        Returns:
            Años desde la publicación
        """
        # TODO: Implementar usando date.today().year
        pass

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        """
        Factory method: crea un Book desde un diccionario.

        Args:
            data: Dict con keys 'title', 'author', 'isbn', 'year'

        Returns:
            Nueva instancia de Book
        """
        # TODO: Implementar
        pass

    @staticmethod
    def is_valid_isbn(isbn: str) -> bool:
        """
        Valida el formato de un ISBN.

        Un ISBN válido tiene 10 o 13 dígitos (ignorando guiones).

        Args:
            isbn: Código ISBN a validar

        Returns:
            True si el formato es válido
        """
        # TODO: Implementar
        # 1. Remover guiones y espacios
        # 2. Verificar que tenga 10 o 13 caracteres
        # 3. Verificar que sean dígitos
        pass
