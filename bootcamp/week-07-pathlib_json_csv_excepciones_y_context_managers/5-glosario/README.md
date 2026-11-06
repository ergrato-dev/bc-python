# Glosario — Semana 07

| Término | Definición |
|---|---|
| **Cabecera** | Primera fila de un CSV, con el nombre de cada columna; se comprueba antes de confiar en las filas |
| **Carpeta de trabajo** | La carpeta desde la que lanzaste el programa (`Path.cwd()`); las rutas relativas se resuelven desde ella |
| **Codificación** (*encoding*) | Tabla que convierte letras en bytes y bytes en letras; la de hoy es UTF-8 |
| **Context manager** | Objeto que sabe qué hacer al entrar en un bloque `with` (`__enter__`) y al salir de él (`__exit__`), salga como salga |
| **`@contextmanager`** | Decorador de `contextlib` que convierte una función con un `yield` en un context manager |
| **CSV** | Tabla guardada como texto: una fila por línea y columnas separadas por un carácter (`;` en español) |
| **`csv.reader` / `csv.writer`** | Leen y escriben CSV respetando separadores y comillas; cada fila es una lista de `str` |
| **`DictReader`** | Lector de CSV que da cada fila como diccionario, con la cabecera como claves |
| **EAFP** | "Es más fácil pedir perdón que permiso": intentar la operación y capturar el error, en lugar de comprobar antes (LBYL) |
| **Excepción** | Objeto que Python lanza cuando algo no puede seguir; sube por las llamadas hasta que alguien la captura |
| **Excepción propia** | Clase que hereda de `Exception` (`class DataFileError(Exception):`) para dar a tus errores un tipo y un mensaje con sentido |
| **`finally`** | Bloque de un `try` que se ejecuta siempre, haya error o no |
| **`glob`** | Buscar archivos con un patrón: `path.glob("*.csv")` |
| **JSON** | Formato de texto con tipos (números, textos, `true`/`false`, `null`, listas y objetos); el de las API web |
| **`JSONDecodeError`** | Excepción de `json` cuando el texto no es JSON válido; trae `lineno` y `colno` |
| **Modo de apertura** | Segundo argumento de `open`: `"r"` leer, `"w"` escribir desde cero, `"a"` añadir, `"x"` crear |
| **`newline=""`** | Argumento de `open` que deja los saltos de línea al módulo `csv` |
| **`OSError`** | Familia de los errores del sistema: `FileNotFoundError`, `IsADirectoryError`, `PermissionError`... |
| **`Path`** | Objeto de `pathlib` que representa una ruta y sabe partirse (`parent`, `name`, `suffix`) y unirse (`/`) |
| **`raise ... from`** | Lanza una excepción nueva guardando la original como causa (`__cause__`) |
| **Ruta absoluta / relativa** | Absoluta: desde la raíz del disco. Relativa: desde la carpeta de trabajo |
| **`suppress`** | Context manager de `contextlib` que ignora un tipo de excepción concreto |
| **`tmp_path`** | *Fixture* de pytest: una carpeta temporal nueva para cada test |
| ***Traceback*** | Informe de una excepción no capturada: el error en la última línea y, encima, el camino de llamadas |
| **`with`** | Sentencia que usa un context manager: abre un recurso y garantiza que se cierra |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
