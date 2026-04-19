# 🎵 Proyecto: Gestor de Playlist Musical

## 📋 Descripción

Desarrollarás un **sistema de gestión de playlists musicales** que permite crear, modificar y analizar colecciones de canciones usando listas, tuplas y estructuras de datos anidadas.

El sistema debe manejar canciones con múltiples atributos (título, artista, duración, género) y proporcionar funcionalidades de búsqueda, ordenamiento y estadísticas.

---

## 🎯 Objetivos de Aprendizaje

Al completar este proyecto serás capaz de:

- ✅ Usar Named Tuples para representar datos estructurados
- ✅ Manipular listas con métodos avanzados
- ✅ Aplicar slicing para extraer y modificar subconjuntos
- ✅ Trabajar con estructuras de datos anidadas
- ✅ Implementar funciones que retornan múltiples valores
- ✅ Usar tuple unpacking en diferentes contextos

---

## 📚 Requisitos Previos

- Métodos de listas (`append`, `extend`, `insert`, `remove`, `pop`, `sort`)
- Slicing avanzado `[start:stop:step]`
- Tuplas e inmutabilidad
- Named Tuples con `typing.NamedTuple`
- Tuple unpacking y extended unpacking

---

## 🎵 Modelo de Datos

### Canción (Song)

Cada canción se representa como una Named Tuple:

```python
from typing import NamedTuple

class Song(NamedTuple):
    title: str       # Título de la canción
    artist: str      # Nombre del artista
    duration: int    # Duración en segundos
    genre: str       # Género musical
    year: int        # Año de lanzamiento
```

### Playlist

Una playlist es una lista de canciones con un nombre:

```python
playlist_name: str = "Mi Playlist"
songs: list[Song] = [...]
```

---

## 📝 Funcionalidades Requeridas

### 1. Gestión de Canciones

| Función | Descripción |
|---------|-------------|
| `add_song()` | Agregar una canción al final de la playlist |
| `insert_song()` | Insertar una canción en una posición específica |
| `remove_song()` | Eliminar una canción por título |
| `move_song()` | Mover una canción a otra posición |

### 2. Consultas y Búsqueda

| Función | Descripción |
|---------|-------------|
| `find_by_artist()` | Buscar canciones de un artista |
| `find_by_genre()` | Filtrar canciones por género |
| `find_by_year_range()` | Canciones en un rango de años |
| `get_song_at()` | Obtener canción en posición específica |

### 3. Ordenamiento

| Función | Descripción |
|---------|-------------|
| `sort_by_title()` | Ordenar alfabéticamente por título |
| `sort_by_duration()` | Ordenar por duración (menor a mayor) |
| `sort_by_year()` | Ordenar por año de lanzamiento |

### 4. Estadísticas

| Función | Descripción |
|---------|-------------|
| `get_total_duration()` | Duración total de la playlist |
| `get_duration_stats()` | Retorna (min, max, promedio) de duración |
| `count_by_genre()` | Contar canciones por género |
| `get_oldest_newest()` | Retorna (canción más vieja, más nueva) |

### 5. Operaciones con Slicing

| Función | Descripción |
|---------|-------------|
| `get_first_n()` | Obtener las primeras N canciones |
| `get_last_n()` | Obtener las últimas N canciones |
| `get_range()` | Obtener canciones en un rango |
| `reverse_playlist()` | Invertir el orden de la playlist |

---

## 💻 Estructura del Código

```
3-proyecto/
├── README.md           # Este archivo
├── starter/
│   └── main.py         # Código inicial con TODOs
└── solution/           # ⚠️ Solo instructores
    └── main.py
```

---

## 🚀 Instrucciones

### Paso 1: Explorar el código inicial

Abre `starter/main.py` y familiarízate con:
- La definición de `Song` (NamedTuple)
- Las canciones de ejemplo
- La estructura de las funciones a implementar

### Paso 2: Implementar funciones de gestión

Completa las funciones:
- `add_song()`
- `insert_song()`
- `remove_song()`
- `move_song()`

### Paso 3: Implementar búsquedas

Completa las funciones de consulta:
- `find_by_artist()`
- `find_by_genre()`
- `find_by_year_range()`

### Paso 4: Implementar ordenamiento

Completa las funciones de ordenamiento:
- `sort_by_title()`
- `sort_by_duration()`
- `sort_by_year()`

### Paso 5: Implementar estadísticas

Completa las funciones que retornan múltiples valores:
- `get_duration_stats()`
- `get_oldest_newest()`
- `count_by_genre()`

### Paso 6: Implementar operaciones con slicing

Completa las funciones:
- `get_first_n()`
- `get_last_n()`
- `get_range()`
- `reverse_playlist()`

### Paso 7: Probar el sistema

Ejecuta el programa y verifica que todas las funcionalidades funcionen correctamente.

---

## ✅ Criterios de Evaluación

### Funcionalidad (40%)

| Criterio | Puntos |
|----------|--------|
| Gestión de canciones funciona correctamente | 10 |
| Búsquedas retornan resultados correctos | 10 |
| Ordenamiento funciona en todos los casos | 10 |
| Estadísticas calculadas correctamente | 10 |

### Código (40%)

| Criterio | Puntos |
|----------|--------|
| Uso correcto de Named Tuples | 10 |
| Uso apropiado de métodos de lista | 10 |
| Slicing aplicado correctamente | 10 |
| Tuple unpacking utilizado | 10 |

### Calidad (20%)

| Criterio | Puntos |
|----------|--------|
| Type hints en todas las funciones | 5 |
| Código limpio y legible | 5 |
| Manejo de casos edge (lista vacía, etc.) | 5 |
| Docstrings descriptivos | 5 |

---

## 📊 Ejemplo de Ejecución

```
🎵 GESTOR DE PLAYLIST MUSICAL
============================

📋 Playlist: Rock Classics (5 canciones)
  1. Bohemian Rhapsody - Queen (5:55) [Rock, 1975]
  2. Stairway to Heaven - Led Zeppelin (8:02) [Rock, 1971]
  3. Hotel California - Eagles (6:30) [Rock, 1977]
  4. Sweet Child O' Mine - Guns N' Roses (5:56) [Rock, 1987]
  5. Smells Like Teen Spirit - Nirvana (5:01) [Rock, 1991]

📊 Estadísticas:
  Duración total: 31:24
  Promedio por canción: 6:17
  Canción más corta: Smells Like Teen Spirit (5:01)
  Canción más larga: Stairway to Heaven (8:02)

🔍 Búsqueda por artista "Queen":
  - Bohemian Rhapsody (5:55)

📈 Ordenado por duración:
  1. Smells Like Teen Spirit (5:01)
  2. Bohemian Rhapsody (5:55)
  3. Sweet Child O' Mine (5:56)
  4. Hotel California (6:30)
  5. Stairway to Heaven (8:02)
```

---

## 🎯 Retos Adicionales (Opcional)

Si terminas antes, intenta implementar:

1. **Shuffle**: Función para mezclar aleatoriamente la playlist
2. **Merge playlists**: Combinar dos playlists eliminando duplicados
3. **Export**: Generar un string formateado para "exportar" la playlist
4. **Top N by duration**: Obtener las N canciones más largas/cortas

---

## ⏱️ Tiempo Estimado

- **Implementación básica**: 1.5 - 2 horas
- **Con retos adicionales**: 2.5 - 3 horas

---

## 📚 Recursos de Apoyo

- [Teoría: Métodos de Listas](../1-teoria/01-listas-metodos.md)
- [Teoría: Slicing](../1-teoria/02-listas-slicing.md)
- [Teoría: Tuplas](../1-teoria/03-tuplas.md)
- [Teoría: Estructuras Anidadas](../1-teoria/04-estructuras-anidadas.md)

---

## 🔗 Navegación

← [Ejercicios](../2-ejercicios/) | [Semana 05](../README.md) | [Recursos](../4-recursos/) →
