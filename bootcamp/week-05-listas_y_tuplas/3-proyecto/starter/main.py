"""
🎵 Proyecto: Gestor de Playlist Musical
=======================================

Sistema de gestión de playlists usando listas, tuplas y estructuras anidadas.

Instrucciones:
1. Lee cada función y su docstring
2. Implementa la lógica donde dice TODO
3. Ejecuta para probar tu implementación
"""

from typing import NamedTuple


# ============================================
# MODELO DE DATOS
# ============================================

class Song(NamedTuple):
    """Representa una canción en la playlist."""
    title: str       # Título de la canción
    artist: str      # Nombre del artista
    duration: int    # Duración en segundos
    genre: str       # Género musical
    year: int        # Año de lanzamiento


# ============================================
# DATOS DE EJEMPLO
# ============================================

def get_sample_songs() -> list[Song]:
    """Retorna una lista de canciones de ejemplo."""
    return [
        Song("Bohemian Rhapsody", "Queen", 355, "Rock", 1975),
        Song("Stairway to Heaven", "Led Zeppelin", 482, "Rock", 1971),
        Song("Hotel California", "Eagles", 390, "Rock", 1977),
        Song("Sweet Child O' Mine", "Guns N' Roses", 356, "Rock", 1987),
        Song("Smells Like Teen Spirit", "Nirvana", 301, "Rock", 1991),
        Song("Billie Jean", "Michael Jackson", 294, "Pop", 1983),
        Song("Like a Prayer", "Madonna", 340, "Pop", 1989),
        Song("Purple Rain", "Prince", 520, "Pop", 1984),
        Song("Lose Yourself", "Eminem", 326, "Hip Hop", 2002),
        Song("Juicy", "The Notorious B.I.G.", 318, "Hip Hop", 1994),
    ]


# ============================================
# UTILIDADES
# ============================================

def format_duration(seconds: int) -> str:
    """
    Convierte segundos a formato mm:ss.

    Args:
        seconds: Duración en segundos

    Returns:
        str: Duración formateada (ej: "5:35")
    """
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"


def display_playlist(name: str, songs: list[Song]) -> None:
    """
    Muestra la playlist formateada.

    Args:
        name: Nombre de la playlist
        songs: Lista de canciones
    """
    print(f"\n📋 Playlist: {name} ({len(songs)} canciones)")
    print("-" * 50)

    if not songs:
        print("  (vacía)")
        return

    for i, song in enumerate(songs, 1):
        duration = format_duration(song.duration)
        print(f"  {i}. {song.title} - {song.artist} ({duration}) [{song.genre}, {song.year}]")


# ============================================
# 1. GESTIÓN DE CANCIONES
# ============================================

def add_song(songs: list[Song], song: Song) -> None:
    """
    Agrega una canción al final de la playlist.

    Args:
        songs: Lista de canciones (se modifica in-place)
        song: Canción a agregar
    """
    # TODO: Implementar
    # Usar el método apropiado de lista para agregar al final
    pass


def insert_song(songs: list[Song], position: int, song: Song) -> None:
    """
    Inserta una canción en una posición específica.

    Args:
        songs: Lista de canciones (se modifica in-place)
        position: Índice donde insertar (0-based)
        song: Canción a insertar
    """
    # TODO: Implementar
    # Usar el método apropiado de lista para insertar
    pass


def remove_song(songs: list[Song], title: str) -> Song | None:
    """
    Elimina una canción por su título.

    Args:
        songs: Lista de canciones (se modifica in-place)
        title: Título de la canción a eliminar

    Returns:
        Song | None: La canción eliminada o None si no se encontró
    """
    # TODO: Implementar
    # 1. Buscar la canción por título (ignorar mayúsculas/minúsculas)
    # 2. Si existe, eliminarla y retornarla
    # 3. Si no existe, retornar None
    pass


def move_song(songs: list[Song], from_pos: int, to_pos: int) -> bool:
    """
    Mueve una canción de una posición a otra.

    Args:
        songs: Lista de canciones (se modifica in-place)
        from_pos: Posición actual (0-based)
        to_pos: Nueva posición (0-based)

    Returns:
        bool: True si se movió, False si las posiciones son inválidas
    """
    # TODO: Implementar
    # 1. Validar que ambas posiciones estén dentro del rango
    # 2. Extraer la canción de from_pos (usar pop)
    # 3. Insertarla en to_pos
    # 4. Retornar True si tuvo éxito
    pass


# ============================================
# 2. CONSULTAS Y BÚSQUEDA
# ============================================

def find_by_artist(songs: list[Song], artist: str) -> list[Song]:
    """
    Busca todas las canciones de un artista.

    Args:
        songs: Lista de canciones
        artist: Nombre del artista (búsqueda parcial, case-insensitive)

    Returns:
        list[Song]: Canciones del artista
    """
    # TODO: Implementar
    # Usar list comprehension con búsqueda case-insensitive
    pass


def find_by_genre(songs: list[Song], genre: str) -> list[Song]:
    """
    Filtra canciones por género.

    Args:
        songs: Lista de canciones
        genre: Género a buscar (case-insensitive)

    Returns:
        list[Song]: Canciones del género especificado
    """
    # TODO: Implementar
    pass


def find_by_year_range(songs: list[Song], start_year: int, end_year: int) -> list[Song]:
    """
    Filtra canciones en un rango de años (inclusivo).

    Args:
        songs: Lista de canciones
        start_year: Año inicial
        end_year: Año final

    Returns:
        list[Song]: Canciones en el rango de años
    """
    # TODO: Implementar
    pass


def get_song_at(songs: list[Song], position: int) -> Song | None:
    """
    Obtiene la canción en una posición específica.

    Args:
        songs: Lista de canciones
        position: Índice (0-based, soporta negativos)

    Returns:
        Song | None: La canción o None si la posición es inválida
    """
    # TODO: Implementar
    # Manejar índices negativos y validar rango
    pass


# ============================================
# 3. ORDENAMIENTO
# ============================================

def sort_by_title(songs: list[Song]) -> list[Song]:
    """
    Retorna las canciones ordenadas alfabéticamente por título.

    Args:
        songs: Lista de canciones (no se modifica)

    Returns:
        list[Song]: Nueva lista ordenada
    """
    # TODO: Implementar
    # Usar sorted() con key apropiada
    pass


def sort_by_duration(songs: list[Song], descending: bool = False) -> list[Song]:
    """
    Retorna las canciones ordenadas por duración.

    Args:
        songs: Lista de canciones (no se modifica)
        descending: Si True, ordena de mayor a menor

    Returns:
        list[Song]: Nueva lista ordenada
    """
    # TODO: Implementar
    pass


def sort_by_year(songs: list[Song], descending: bool = False) -> list[Song]:
    """
    Retorna las canciones ordenadas por año.

    Args:
        songs: Lista de canciones (no se modifica)
        descending: Si True, ordena de más nuevo a más viejo

    Returns:
        list[Song]: Nueva lista ordenada
    """
    # TODO: Implementar
    pass


# ============================================
# 4. ESTADÍSTICAS
# ============================================

def get_total_duration(songs: list[Song]) -> int:
    """
    Calcula la duración total de la playlist.

    Args:
        songs: Lista de canciones

    Returns:
        int: Duración total en segundos
    """
    # TODO: Implementar
    # Usar sum() con expresión generadora
    pass


def get_duration_stats(songs: list[Song]) -> tuple[int, int, float]:
    """
    Calcula estadísticas de duración.

    Args:
        songs: Lista de canciones

    Returns:
        tuple: (duración_mínima, duración_máxima, promedio)
        Retorna (0, 0, 0.0) si la lista está vacía
    """
    # TODO: Implementar
    # Retornar tupla con (min, max, promedio)
    pass


def count_by_genre(songs: list[Song]) -> dict[str, int]:
    """
    Cuenta canciones por género.

    Args:
        songs: Lista de canciones

    Returns:
        dict: Diccionario {género: cantidad}
    """
    # TODO: Implementar
    # Contar ocurrencias de cada género
    pass


def get_oldest_newest(songs: list[Song]) -> tuple[Song | None, Song | None]:
    """
    Encuentra la canción más vieja y la más nueva.

    Args:
        songs: Lista de canciones

    Returns:
        tuple: (canción_más_vieja, canción_más_nueva)
        Retorna (None, None) si la lista está vacía
    """
    # TODO: Implementar
    # Usar min/max con key apropiada
    pass


# ============================================
# 5. OPERACIONES CON SLICING
# ============================================

def get_first_n(songs: list[Song], n: int) -> list[Song]:
    """
    Obtiene las primeras N canciones.

    Args:
        songs: Lista de canciones
        n: Cantidad de canciones

    Returns:
        list[Song]: Primeras N canciones
    """
    # TODO: Implementar usando slicing
    pass


def get_last_n(songs: list[Song], n: int) -> list[Song]:
    """
    Obtiene las últimas N canciones.

    Args:
        songs: Lista de canciones
        n: Cantidad de canciones

    Returns:
        list[Song]: Últimas N canciones
    """
    # TODO: Implementar usando slicing con índice negativo
    pass


def get_range(songs: list[Song], start: int, end: int) -> list[Song]:
    """
    Obtiene canciones en un rango de posiciones.

    Args:
        songs: Lista de canciones
        start: Posición inicial (inclusiva)
        end: Posición final (exclusiva)

    Returns:
        list[Song]: Canciones en el rango
    """
    # TODO: Implementar usando slicing
    pass


def reverse_playlist(songs: list[Song]) -> list[Song]:
    """
    Retorna la playlist en orden inverso.

    Args:
        songs: Lista de canciones (no se modifica)

    Returns:
        list[Song]: Nueva lista invertida
    """
    # TODO: Implementar usando slicing [::-1]
    pass


# ============================================
# PROGRAMA PRINCIPAL
# ============================================

def main() -> None:
    """Función principal del programa."""
    print("🎵 GESTOR DE PLAYLIST MUSICAL")
    print("=" * 50)

    # Crear playlist con canciones de ejemplo
    playlist_name = "Mi Playlist"
    songs = get_sample_songs()

    # Mostrar playlist inicial
    display_playlist(playlist_name, songs)

    # --- TEST 1: Gestión de canciones ---
    print("\n" + "=" * 50)
    print("📝 TEST 1: Gestión de canciones")
    print("=" * 50)

    # Agregar una canción
    new_song = Song("Thriller", "Michael Jackson", 357, "Pop", 1982)
    add_song(songs, new_song)
    print(f"\n✅ Agregada: {new_song.title}")

    # Insertar en posición 0
    another_song = Song("Imagine", "John Lennon", 183, "Rock", 1971)
    insert_song(songs, 0, another_song)
    print(f"✅ Insertada al inicio: {another_song.title}")

    # Mostrar después de agregar
    display_playlist(playlist_name, songs)

    # Eliminar una canción
    removed = remove_song(songs, "Billie Jean")
    if removed:
        print(f"\n✅ Eliminada: {removed.title}")

    # Mover canción
    moved = move_song(songs, 0, 5)
    if moved:
        print("✅ Movida 'Imagine' de posición 0 a 5")

    # --- TEST 2: Búsquedas ---
    print("\n" + "=" * 50)
    print("🔍 TEST 2: Búsquedas")
    print("=" * 50)

    # Buscar por artista
    queen_songs = find_by_artist(songs, "Queen")
    print(f"\nCanciones de Queen: {len(queen_songs) if queen_songs else 0}")
    if queen_songs:
        for s in queen_songs:
            print(f"  - {s.title}")

    # Buscar por género
    pop_songs = find_by_genre(songs, "Pop")
    print(f"\nCanciones Pop: {len(pop_songs) if pop_songs else 0}")

    # Buscar por rango de años
    eighties = find_by_year_range(songs, 1980, 1989)
    print(f"\nCanciones de los 80s: {len(eighties) if eighties else 0}")
    if eighties:
        for s in eighties:
            print(f"  - {s.title} ({s.year})")

    # --- TEST 3: Ordenamiento ---
    print("\n" + "=" * 50)
    print("📊 TEST 3: Ordenamiento")
    print("=" * 50)

    # Ordenar por duración
    by_duration = sort_by_duration(songs)
    print("\nPor duración (cortas primero):")
    if by_duration:
        for s in by_duration[:3]:
            print(f"  - {s.title} ({format_duration(s.duration)})")

    # Ordenar por año
    by_year = sort_by_year(songs, descending=True)
    print("\nPor año (más nuevas primero):")
    if by_year:
        for s in by_year[:3]:
            print(f"  - {s.title} ({s.year})")

    # --- TEST 4: Estadísticas ---
    print("\n" + "=" * 50)
    print("📈 TEST 4: Estadísticas")
    print("=" * 50)

    # Duración total
    total = get_total_duration(songs)
    if total:
        print(f"\nDuración total: {format_duration(total)}")

    # Estadísticas de duración
    stats = get_duration_stats(songs)
    if stats and stats != (0, 0, 0.0):
        min_dur, max_dur, avg_dur = stats
        print(f"Duración mínima: {format_duration(min_dur)}")
        print(f"Duración máxima: {format_duration(max_dur)}")
        print(f"Duración promedio: {format_duration(int(avg_dur))}")

    # Conteo por género
    genre_count = count_by_genre(songs)
    if genre_count:
        print("\nCanciones por género:")
        for genre, count in genre_count.items():
            print(f"  {genre}: {count}")

    # Más vieja y más nueva
    oldest_newest = get_oldest_newest(songs)
    if oldest_newest and oldest_newest[0]:
        oldest, newest = oldest_newest
        print(f"\nMás antigua: {oldest.title} ({oldest.year})")
        print(f"Más nueva: {newest.title} ({newest.year})")

    # --- TEST 5: Slicing ---
    print("\n" + "=" * 50)
    print("✂️ TEST 5: Operaciones con Slicing")
    print("=" * 50)

    # Primeras 3
    first_three = get_first_n(songs, 3)
    print("\nPrimeras 3 canciones:")
    if first_three:
        for s in first_three:
            print(f"  - {s.title}")

    # Últimas 3
    last_three = get_last_n(songs, 3)
    print("\nÚltimas 3 canciones:")
    if last_three:
        for s in last_three:
            print(f"  - {s.title}")

    # Rango
    middle = get_range(songs, 2, 5)
    print("\nCanciones de posición 2 a 4:")
    if middle:
        for s in middle:
            print(f"  - {s.title}")

    # Invertida
    reversed_playlist = reverse_playlist(songs)
    print("\nPlaylist invertida (primeras 3):")
    if reversed_playlist:
        for s in reversed_playlist[:3]:
            print(f"  - {s.title}")

    # --- Resumen final ---
    print("\n" + "=" * 50)
    print("✅ ¡Proyecto completado!")
    print("=" * 50)
    display_playlist(playlist_name + " (Final)", songs)


if __name__ == "__main__":
    main()
