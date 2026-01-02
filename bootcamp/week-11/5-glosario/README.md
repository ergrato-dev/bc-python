# 📖 Glosario - Semana 11

## Archivos, Excepciones y Context Managers

---

### A

#### `append mode`
Modo de apertura de archivo (`"a"`) que añade contenido al final sin sobrescribir el existente.

#### `atomic write`
Operación de escritura que se completa totalmente o no se realiza, evitando estados intermedios corruptos.

---

### B

#### `binary mode`
Modo de apertura (`"b"`) para leer/escribir archivos como bytes en lugar de texto.

#### `buffering`
Técnica de almacenamiento temporal en memoria para optimizar operaciones de I/O.

---

### C

#### `chaining (exception)`
Capacidad de vincular excepciones usando `from` para mantener el traceback original.
```python
raise ValueError("Invalid") from original_error
```

#### `close()`
Método que libera recursos asociados a un archivo abierto.

#### `context manager`
Objeto que define `__enter__()` y `__exit__()` para gestionar recursos con `with`.

#### `contextlib`
Módulo estándar con utilidades para crear context managers.

#### `@contextmanager`
Decorador de `contextlib` que convierte un generador en context manager.

#### `CSV`
Comma-Separated Values. Formato de texto para datos tabulares.

---

### E

#### `encoding`
Sistema de codificación de caracteres (ej: UTF-8, ASCII, Latin-1).

#### `exception`
Evento que interrumpe el flujo normal del programa cuando ocurre un error.

#### `exception chaining`
Ver `chaining (exception)`.

#### `ExitStack`
Clase de `contextlib` para gestionar múltiples context managers dinámicamente.

---

### F

#### `file handle`
Objeto retornado por `open()` que representa la conexión a un archivo.

#### `file mode`
Cadena que especifica cómo abrir un archivo (`"r"`, `"w"`, `"a"`, `"x"`, `"b"`, `"t"`).

#### `file pointer`
Posición actual de lectura/escritura dentro de un archivo.

#### `finally`
Bloque que siempre se ejecuta, haya o no excepción.

---

### I

#### `IOError`
Excepción para errores de entrada/salida (alias de `OSError` en Python 3).

---

### J

#### `JSON`
JavaScript Object Notation. Formato ligero de intercambio de datos.

#### `json.dumps()`
Serializa objeto Python a string JSON.

#### `json.loads()`
Deserializa string JSON a objeto Python.

---

### O

#### `open()`
Función built-in para abrir archivos y retornar un file handle.

#### `OSError`
Excepción base para errores del sistema operativo (archivos, red, etc.).

---

### P

#### `pathlib`
Módulo moderno para manipulación de rutas de archivos como objetos.

#### `Path`
Clase principal de `pathlib` que representa una ruta de archivo.

---

### R

#### `raise`
Palabra clave para lanzar una excepción manualmente.

#### `read()`
Método que lee contenido de un archivo (todo o n bytes/caracteres).

#### `readline()`
Método que lee una línea de un archivo.

#### `readlines()`
Método que lee todas las líneas y retorna una lista.

---

### S

#### `seek()`
Método para mover el file pointer a una posición específica.

#### `suppress()`
Context manager de `contextlib` que suprime excepciones específicas.

---

### T

#### `tell()`
Método que retorna la posición actual del file pointer.

#### `text mode`
Modo por defecto (`"t"`) que lee/escribe como strings con encoding.

#### `traceback`
Información de la pila de llamadas cuando ocurre una excepción.

#### `try`
Palabra clave que inicia un bloque de manejo de excepciones.

---

### U

#### `UTF-8`
Encoding Unicode de longitud variable, compatible con ASCII. Estándar moderno.

---

### W

#### `with statement`
Construcción que garantiza limpieza de recursos usando context managers.
```python
with open("file.txt") as f:
    content = f.read()
```

#### `write()`
Método que escribe contenido a un archivo.

#### `writelines()`
Método que escribe una secuencia de strings a un archivo.

---

### Símbolos

#### `__enter__()`
Método mágico llamado al entrar en un bloque `with`. Retorna el recurso.

#### `__exit__()`
Método mágico llamado al salir de un bloque `with`. Maneja limpieza y excepciones.

---

## 📚 Referencias

- [Python Docs: Built-in Exceptions](https://docs.python.org/3/library/exceptions.html)
- [Python Docs: contextlib](https://docs.python.org/3/library/contextlib.html)
- [Python Docs: pathlib](https://docs.python.org/3/library/pathlib.html)
