# 📁 Patrones Avanzados de Manejo de Archivos

## 🎯 Objetivos de Aprendizaje

- Aplicar patrones robustos para operaciones con archivos
- Implementar procesamiento eficiente de archivos grandes
- Manejar archivos temporales correctamente
- Trabajar con diferentes formatos de archivo

---

## 1. Patrones de Lectura

### Lectura con Fallback de Encoding

```python
from pathlib import Path
from typing import Iterator


def read_with_fallback(
    file_path: str,
    encodings: list[str] | None = None
) -> str:
    """
    Intenta leer archivo con múltiples encodings.

    Args:
        file_path: Ruta al archivo
        encodings: Lista de encodings a intentar

    Returns:
        Contenido del archivo

    Raises:
        UnicodeDecodeError: Si ningún encoding funciona
    """
    encodings = encodings or ["utf-8", "latin-1", "cp1252", "utf-16"]

    for encoding in encodings:
        try:
            return Path(file_path).read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue

    raise UnicodeDecodeError(
        "all",
        b"",
        0,
        1,
        f"No encoding worked for {file_path}"
    )


# Uso
content = read_with_fallback("archivo_desconocido.txt")
```

### Lectura Perezosa (Lazy) de Líneas

```python
from typing import Iterator, Callable


def lazy_read_lines(
    file_path: str,
    predicate: Callable[[str], bool] | None = None,
    transform: Callable[[str], str] | None = None
) -> Iterator[str]:
    """
    Lee líneas de forma perezosa con filtro y transformación.

    Args:
        file_path: Ruta al archivo
        predicate: Función para filtrar líneas
        transform: Función para transformar líneas

    Yields:
        Líneas procesadas
    """
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n\r")

            if predicate and not predicate(line):
                continue

            if transform:
                line = transform(line)

            yield line


# Uso: Leer solo líneas no vacías, en mayúsculas
lines = lazy_read_lines(
    "data.txt",
    predicate=lambda x: x.strip(),
    transform=str.upper
)

for line in lines:
    print(line)
```

### Lectura por Chunks con Progreso

```python
from pathlib import Path
from typing import Iterator, Callable


def read_with_progress(
    file_path: str,
    chunk_size: int = 8192,
    progress_callback: Callable[[int, int], None] | None = None
) -> Iterator[str]:
    """
    Lee archivo en chunks reportando progreso.

    Args:
        file_path: Ruta al archivo
        chunk_size: Tamaño de cada chunk
        progress_callback: Función callback(bytes_read, total_bytes)
    """
    path = Path(file_path)
    total_size = path.stat().st_size
    bytes_read = 0

    with open(path, "r", encoding="utf-8") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break

            bytes_read += len(chunk.encode("utf-8"))

            if progress_callback:
                progress_callback(bytes_read, total_size)

            yield chunk


# Uso con barra de progreso simple
def show_progress(current: int, total: int) -> None:
    percent = (current / total) * 100
    print(f"\rProgreso: {percent:.1f}%", end="", flush=True)


for chunk in read_with_progress("large_file.txt", progress_callback=show_progress):
    process(chunk)
print()  # Nueva línea al final
```

---

## 2. Patrones de Escritura

### Escritura Atómica

```python
import os
import tempfile
from pathlib import Path
from contextlib import contextmanager
from typing import Iterator, TextIO


@contextmanager
def atomic_write(
    file_path: str,
    mode: str = "w",
    encoding: str = "utf-8"
) -> Iterator[TextIO]:
    """
    Escribe archivo de forma atómica.

    El archivo original solo se modifica si la escritura
    es completamente exitosa.
    """
    path = Path(file_path)

    # Crear archivo temporal en el mismo directorio
    fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp"
    )
    temp_file = None
    success = False

    try:
        temp_file = os.fdopen(fd, mode, encoding=encoding)
        yield temp_file
        temp_file.flush()
        os.fsync(temp_file.fileno())
        success = True

    finally:
        if temp_file:
            temp_file.close()

        if success:
            # Reemplazo atómico
            os.replace(temp_path, file_path)
        else:
            # Limpiar en caso de error
            try:
                os.unlink(temp_path)
            except OSError:
                pass


# Uso
with atomic_write("config.json") as f:
    f.write('{"key": "value"}')
# Si hay error, el archivo original no se modifica
```

### Escritura con Rotación de Archivos

```python
from pathlib import Path
from datetime import datetime
import gzip
import shutil


class RotatingFileWriter:
    """
    Escritor de archivos con rotación automática.
    """

    def __init__(
        self,
        base_path: str,
        max_size: int = 10 * 1024 * 1024,  # 10 MB
        max_files: int = 5,
        compress_old: bool = True
    ):
        self.base_path = Path(base_path)
        self.max_size = max_size
        self.max_files = max_files
        self.compress_old = compress_old
        self._file: TextIO | None = None
        self._current_size = 0

    def __enter__(self):
        self._open_file()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._file:
            self._file.close()
        return False

    def _open_file(self) -> None:
        """Abre archivo para escritura."""
        self._file = open(self.base_path, "a", encoding="utf-8")
        self._current_size = self.base_path.stat().st_size if self.base_path.exists() else 0

    def _rotate(self) -> None:
        """Rota archivos cuando se alcanza el tamaño máximo."""
        if self._file:
            self._file.close()

        # Rotar archivos existentes
        for i in range(self.max_files - 1, 0, -1):
            old_path = self._get_rotated_path(i)
            new_path = self._get_rotated_path(i + 1)

            if old_path.exists():
                if i + 1 >= self.max_files:
                    old_path.unlink()
                else:
                    old_path.rename(new_path)

        # Mover archivo actual
        if self.base_path.exists():
            rotated_path = self._get_rotated_path(1)
            self.base_path.rename(rotated_path)

            if self.compress_old:
                self._compress_file(rotated_path)

        self._open_file()

    def _get_rotated_path(self, index: int) -> Path:
        """Genera ruta para archivo rotado."""
        suffix = f".{index}" + (".gz" if self.compress_old and index > 0 else "")
        return self.base_path.with_suffix(self.base_path.suffix + suffix)

    def _compress_file(self, path: Path) -> None:
        """Comprime archivo con gzip."""
        compressed_path = path.with_suffix(path.suffix + ".gz")
        with open(path, "rb") as f_in:
            with gzip.open(compressed_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        path.unlink()

    def write(self, content: str) -> None:
        """Escribe contenido, rotando si es necesario."""
        content_bytes = len(content.encode("utf-8"))

        if self._current_size + content_bytes > self.max_size:
            self._rotate()

        if self._file:
            self._file.write(content)
            self._file.flush()
            self._current_size += content_bytes


# Uso
with RotatingFileWriter("app.log", max_size=1024*1024) as writer:
    for i in range(10000):
        writer.write(f"[{datetime.now()}] Log entry {i}\n")
```

---

## 3. Archivos Temporales

### Uso Correcto de tempfile

```python
import tempfile
from pathlib import Path
from contextlib import contextmanager
from typing import Iterator


# Archivo temporal que se elimina automáticamente
with tempfile.NamedTemporaryFile(
    mode="w",
    suffix=".txt",
    delete=True,
    encoding="utf-8"
) as f:
    f.write("Datos temporales")
    f.flush()

    # Usar f.name para obtener la ruta
    process_file(f.name)
# Archivo eliminado al salir del with


# Directorio temporal
with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)

    # Crear archivos en el directorio temporal
    (temp_path / "file1.txt").write_text("Contenido 1")
    (temp_path / "file2.txt").write_text("Contenido 2")

    process_directory(temp_dir)
# Directorio y contenido eliminados automáticamente


# Archivo temporal persistente (no se elimina automáticamente)
fd, temp_path = tempfile.mkstemp(suffix=".json")
try:
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump({"data": "value"}, f)

    # Usar el archivo...
    process_file(temp_path)
finally:
    os.unlink(temp_path)  # Limpieza manual
```

### Context Manager para Archivos Temporales

```python
from contextlib import contextmanager
import tempfile
import os
from pathlib import Path
from typing import Iterator


@contextmanager
def temp_copy(source_path: str) -> Iterator[Path]:
    """
    Crea copia temporal de un archivo.

    Útil para procesar archivos sin modificar el original.
    """
    source = Path(source_path)

    fd, temp_path = tempfile.mkstemp(suffix=source.suffix)
    temp = Path(temp_path)

    try:
        # Copiar contenido
        with os.fdopen(fd, "wb") as f:
            f.write(source.read_bytes())

        yield temp

    finally:
        if temp.exists():
            temp.unlink()


# Uso
with temp_copy("important_data.csv") as temp_file:
    # Modificar copia temporal
    content = temp_file.read_text()
    modified = content.replace("old", "new")
    temp_file.write_text(modified)

    # Procesar...
    if validate(temp_file):
        # Solo si es válido, guardar cambios
        shutil.copy(temp_file, "important_data.csv")
```

---

## 4. Procesamiento de Archivos Grandes

### Patrón Map-Reduce para Archivos

```python
from pathlib import Path
from typing import TypeVar, Callable, Iterator
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

T = TypeVar("T")
R = TypeVar("R")


def chunk_file(file_path: str, chunk_size: int = 1024 * 1024) -> Iterator[tuple[int, int]]:
    """
    Divide archivo en chunks para procesamiento paralelo.

    Yields:
        Tuplas (start_position, end_position)
    """
    path = Path(file_path)
    file_size = path.stat().st_size

    start = 0
    while start < file_size:
        end = min(start + chunk_size, file_size)

        # Ajustar a fin de línea
        if end < file_size:
            with open(path, "r", encoding="utf-8") as f:
                f.seek(end)
                f.readline()  # Completar línea actual
                end = f.tell()

        yield (start, end)
        start = end


def process_chunk(args: tuple[str, int, int, Callable]) -> list:
    """Procesa un chunk del archivo."""
    file_path, start, end, processor = args

    results = []
    with open(file_path, "r", encoding="utf-8") as f:
        f.seek(start)

        while f.tell() < end:
            line = f.readline()
            if not line:
                break

            result = processor(line.strip())
            if result is not None:
                results.append(result)

    return results


def parallel_process_file(
    file_path: str,
    processor: Callable[[str], T | None],
    reducer: Callable[[list[T], list[T]], list[T]] | None = None,
    workers: int | None = None
) -> list[T]:
    """
    Procesa archivo grande en paralelo.

    Args:
        file_path: Ruta al archivo
        processor: Función que procesa cada línea
        reducer: Función que combina resultados
        workers: Número de workers (default: CPU count)
    """
    workers = workers or multiprocessing.cpu_count()
    chunks = list(chunk_file(file_path))

    # Preparar argumentos
    args = [(file_path, start, end, processor) for start, end in chunks]

    # Procesar en paralelo
    with ProcessPoolExecutor(max_workers=workers) as executor:
        chunk_results = list(executor.map(process_chunk, args))

    # Reducir resultados
    if reducer:
        result = []
        for chunk in chunk_results:
            result = reducer(result, chunk)
        return result

    # Sin reducer, concatenar todo
    return [item for chunk in chunk_results for item in chunk]


# Uso: Contar palabras en archivo grande
def count_words(line: str) -> dict[str, int]:
    """Cuenta palabras en una línea."""
    counts: dict[str, int] = {}
    for word in line.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def merge_counts(a: list[dict], b: list[dict]) -> list[dict]:
    """Combina conteos de palabras."""
    merged: dict[str, int] = {}
    for d in a + b:
        for word, count in d.items():
            merged[word] = merged.get(word, 0) + count
    return [merged]


results = parallel_process_file(
    "huge_text_file.txt",
    processor=count_words,
    reducer=merge_counts
)
```

### Streaming de Archivos

```python
from typing import Iterator, TypeVar, Callable

T = TypeVar("T")


class FileStream:
    """
    Stream para procesamiento eficiente de archivos.
    """

    def __init__(self, file_path: str, encoding: str = "utf-8"):
        self.file_path = file_path
        self.encoding = encoding

    def lines(self) -> Iterator[str]:
        """Itera sobre líneas."""
        with open(self.file_path, "r", encoding=self.encoding) as f:
            for line in f:
                yield line.rstrip("\n\r")

    def filter(self, predicate: Callable[[str], bool]) -> "FilteredStream":
        """Filtra líneas."""
        return FilteredStream(self, predicate)

    def map(self, transform: Callable[[str], T]) -> "MappedStream[T]":
        """Transforma líneas."""
        return MappedStream(self, transform)

    def take(self, n: int) -> Iterator[str]:
        """Toma las primeras n líneas."""
        for i, line in enumerate(self.lines()):
            if i >= n:
                break
            yield line

    def skip(self, n: int) -> Iterator[str]:
        """Salta las primeras n líneas."""
        for i, line in enumerate(self.lines()):
            if i >= n:
                yield line

    def batch(self, size: int) -> Iterator[list[str]]:
        """Agrupa líneas en batches."""
        batch: list[str] = []
        for line in self.lines():
            batch.append(line)
            if len(batch) >= size:
                yield batch
                batch = []
        if batch:
            yield batch


class FilteredStream(FileStream):
    def __init__(self, source: FileStream, predicate: Callable[[str], bool]):
        self._source = source
        self._predicate = predicate

    def lines(self) -> Iterator[str]:
        for line in self._source.lines():
            if self._predicate(line):
                yield line


class MappedStream(FileStream):
    def __init__(self, source: FileStream, transform: Callable):
        self._source = source
        self._transform = transform

    def lines(self) -> Iterator:
        for line in self._source.lines():
            yield self._transform(line)


# Uso fluent
stream = FileStream("data.txt")

# Filtrar, transformar, tomar 100
results = list(
    stream
    .filter(lambda x: x.startswith("ERROR"))
    .map(lambda x: x.split(": ", 1)[1])
    .take(100)
)

# Procesar en batches
for batch in stream.filter(bool).batch(1000):
    process_batch(batch)
```

---

## 5. Formatos Específicos

### Procesador de Logs

```python
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Iterator
from pathlib import Path


@dataclass
class LogEntry:
    """Entrada de log parseada."""
    timestamp: datetime
    level: str
    logger: str
    message: str

    @classmethod
    def from_line(cls, line: str) -> "LogEntry | None":
        """Parsea línea de log."""
        # Formato: 2024-01-15 10:30:45 - INFO - myapp - Message
        pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (\w+) - (\w+) - (.+)"
        match = re.match(pattern, line)

        if not match:
            return None

        return cls(
            timestamp=datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S"),
            level=match.group(2),
            logger=match.group(3),
            message=match.group(4)
        )


class LogReader:
    """Lector de archivos de log."""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def entries(self) -> Iterator[LogEntry]:
        """Itera sobre entradas de log."""
        with open(self.file_path, "r", encoding="utf-8") as f:
            for line in f:
                entry = LogEntry.from_line(line.strip())
                if entry:
                    yield entry

    def filter_by_level(self, *levels: str) -> Iterator[LogEntry]:
        """Filtra por nivel de log."""
        levels_set = set(levels)
        for entry in self.entries():
            if entry.level in levels_set:
                yield entry

    def filter_by_time(
        self,
        start: datetime | None = None,
        end: datetime | None = None
    ) -> Iterator[LogEntry]:
        """Filtra por rango de tiempo."""
        for entry in self.entries():
            if start and entry.timestamp < start:
                continue
            if end and entry.timestamp > end:
                continue
            yield entry

    def errors(self) -> Iterator[LogEntry]:
        """Obtiene solo errores."""
        return self.filter_by_level("ERROR", "CRITICAL")


# Uso
reader = LogReader("app.log")

# Errores de las últimas 24 horas
from datetime import timedelta
yesterday = datetime.now() - timedelta(days=1)

for entry in reader.filter_by_time(start=yesterday):
    if entry.level in ("ERROR", "CRITICAL"):
        print(f"[{entry.timestamp}] {entry.message}")
```

### Procesador de CSV con Validación

```python
import csv
from dataclasses import dataclass, field
from typing import Iterator, TypeVar, Type, get_type_hints
from pathlib import Path

T = TypeVar("T")


@dataclass
class ValidationError:
    """Error de validación."""
    row: int
    field: str
    value: str
    message: str


@dataclass
class CSVResult:
    """Resultado del procesamiento de CSV."""
    records: list
    errors: list[ValidationError] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0


def parse_csv_to_dataclass(
    file_path: str,
    dataclass_type: Type[T],
    strict: bool = False
) -> CSVResult:
    """
    Parsea CSV a lista de dataclasses con validación.

    Args:
        file_path: Ruta al CSV
        dataclass_type: Tipo de dataclass destino
        strict: Si True, falla en el primer error
    """
    records: list[T] = []
    errors: list[ValidationError] = []
    type_hints = get_type_hints(dataclass_type)

    with open(file_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        for row_num, row in enumerate(reader, start=2):  # +2 por header y 1-index
            try:
                # Convertir tipos
                converted = {}
                for field_name, field_type in type_hints.items():
                    value = row.get(field_name, "")

                    try:
                        if field_type == int:
                            converted[field_name] = int(value) if value else 0
                        elif field_type == float:
                            converted[field_name] = float(value) if value else 0.0
                        elif field_type == bool:
                            converted[field_name] = value.lower() in ("true", "1", "yes")
                        else:
                            converted[field_name] = value
                    except ValueError as e:
                        error = ValidationError(
                            row=row_num,
                            field=field_name,
                            value=value,
                            message=f"Cannot convert to {field_type.__name__}: {e}"
                        )
                        errors.append(error)
                        if strict:
                            return CSVResult(records, errors)
                        continue

                # Crear instancia
                record = dataclass_type(**converted)
                records.append(record)

            except Exception as e:
                error = ValidationError(
                    row=row_num,
                    field="*",
                    value=str(row),
                    message=str(e)
                )
                errors.append(error)
                if strict:
                    break

    return CSVResult(records, errors)


# Uso
@dataclass
class User:
    name: str
    email: str
    age: int
    active: bool


result = parse_csv_to_dataclass("users.csv", User)

if result.is_valid:
    for user in result.records:
        print(f"{user.name} ({user.age})")
else:
    for error in result.errors:
        print(f"Row {error.row}, {error.field}: {error.message}")
```

---

## 6. Buenas Prácticas Resumen

### ✅ Hacer

```python
# 1. Siempre usar pathlib para rutas
from pathlib import Path
data_file = Path("data") / "input.txt"

# 2. Especificar encoding explícitamente
content = data_file.read_text(encoding="utf-8")

# 3. Usar context managers para recursos
with open(file_path, encoding="utf-8") as f:
    process(f)

# 4. Procesar archivos grandes línea por línea
for line in open("large.txt", encoding="utf-8"):
    process_line(line)

# 5. Usar escritura atómica para archivos críticos
with atomic_write("config.json") as f:
    json.dump(config, f)

# 6. Manejar errores específicos
try:
    content = Path("file.txt").read_text()
except FileNotFoundError:
    content = default_content
except PermissionError:
    raise ConfigError("Cannot read config file")
```

### ❌ Evitar

```python
# 1. NO concatenar strings para rutas
path = "data" + "/" + "file.txt"  # ❌

# 2. NO olvidar encoding
content = open("file.txt").read()  # ❌

# 3. NO cargar archivos grandes completamente en memoria
all_lines = open("huge.txt").readlines()  # ❌

# 4. NO ignorar errores de archivo
try:
    content = Path("file.txt").read_text()
except:  # ❌
    pass
```

---

## 📚 Resumen de Patrones

| Patrón | Uso |
|--------|-----|
| Escritura atómica | Archivos críticos (configs) |
| Rotación de archivos | Logs, datos temporales |
| Lectura lazy | Archivos grandes |
| Procesamiento paralelo | Archivos muy grandes |
| Streaming | Procesamiento continuo |
| Archivos temporales | Datos intermedios |

---

## ✅ Checklist de Verificación

- [ ] Uso `pathlib.Path` para manejo de rutas
- [ ] Especifico encoding en todas las operaciones
- [ ] Proceso archivos grandes línea por línea
- [ ] Uso escritura atómica para archivos críticos
- [ ] Implemento rotación para archivos de log
- [ ] Uso archivos temporales para datos intermedios
- [ ] Manejo errores específicos de archivo
- [ ] Limpio archivos temporales correctamente
