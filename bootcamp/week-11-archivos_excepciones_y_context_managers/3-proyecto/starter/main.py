"""
Proyecto Semana 11: Sistema de Logs y Análisis de Archivos
==========================================================

Sistema completo para procesar logs, manejar errores y generar reportes.

Ejecutar:
    python main.py
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from contextlib import contextmanager
from typing import Iterator, Self
import json
import csv
import logging
import re
import tempfile

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# ============================================
# TAREA 1: Modelo de Datos
# ============================================

@dataclass
class LogEntry:
    """
    Representa una entrada de log.

    Attributes:
        timestamp: Fecha y hora del evento
        level: Nivel de log (INFO, DEBUG, WARNING, ERROR, CRITICAL)
        logger_name: Nombre del logger
        message: Mensaje del log
    """
    timestamp: datetime
    level: str
    logger_name: str
    message: str

    # TODO: Implementar método from_line que parsee una línea de log
    # Formato: "2024-01-15 10:30:45 - INFO - app.main - Message"
    @classmethod
    def from_line(cls, line: str) -> "LogEntry":
        """
        Parsea una línea de log y retorna LogEntry.

        Args:
            line: Línea de log en formato estándar

        Returns:
            LogEntry parseado

        Raises:
            LogParseError: Si el formato es inválido
        """
        # TODO: Implementar
        pass


@dataclass
class LogStatistics:
    """
    Estadísticas de un conjunto de logs.

    Attributes:
        total_entries: Número total de entradas
        by_level: Conteo por nivel
        date_range: Tupla (fecha_inicio, fecha_fin)
        error_count: Total de errores (ERROR + CRITICAL)
    """
    total_entries: int = 0
    by_level: dict[str, int] = field(default_factory=dict)
    date_range: tuple[datetime | None, datetime | None] = (None, None)
    error_count: int = 0

    # TODO: Implementar método para calcular porcentajes por nivel
    def get_level_percentages(self) -> dict[str, float]:
        """Retorna porcentaje de cada nivel."""
        # TODO: Implementar
        pass


# ============================================
# TAREA 2: Excepciones Personalizadas
# ============================================

class LogError(Exception):
    """Excepción base para errores de log."""
    pass


# TODO: Implementar LogParseError
# - Debe incluir: line_number, line_content, reason
class LogParseError(LogError):
    """Error al parsear línea de log."""

    def __init__(self, line_number: int, line_content: str, reason: str):
        # TODO: Implementar
        pass


# TODO: Implementar LogFileError
# - Debe incluir: file_path, operation (read/write)
class LogFileError(LogError):
    """Error de operación con archivo de log."""

    def __init__(self, file_path: str, operation: str, cause: Exception | None = None):
        # TODO: Implementar
        pass


# ============================================
# TAREA 3: LogProcessor
# ============================================

class LogProcessor:
    """
    Procesa archivos de log y extrae información.

    Attributes:
        entries: Lista de entradas procesadas
        errors: Lista de errores de parseo encontrados
    """

    def __init__(self):
        self.entries: list[LogEntry] = []
        self.errors: list[LogParseError] = []

    def process_file(self, path: str, encoding: str = "utf-8") -> int:
        """
        Procesa un archivo de log.

        Args:
            path: Ruta al archivo de log
            encoding: Encoding del archivo

        Returns:
            Número de entradas procesadas exitosamente

        Raises:
            LogFileError: Si no se puede leer el archivo
        """
        # TODO: Implementar
        # 1. Verificar que el archivo existe
        # 2. Leer línea por línea
        # 3. Parsear cada línea con LogEntry.from_line()
        # 4. Manejar errores de parseo (guardar en self.errors)
        # 5. Retornar número de entradas procesadas
        pass

    def filter_by_level(self, *levels: str) -> list[LogEntry]:
        """
        Filtra entradas por nivel(es) de log.

        Args:
            levels: Niveles a incluir (INFO, DEBUG, etc.)

        Returns:
            Lista de entradas que coinciden
        """
        # TODO: Implementar
        pass

    def filter_by_date_range(
        self,
        start: datetime | None = None,
        end: datetime | None = None
    ) -> list[LogEntry]:
        """
        Filtra entradas por rango de fechas.

        Args:
            start: Fecha inicio (inclusive)
            end: Fecha fin (inclusive)

        Returns:
            Lista de entradas en el rango
        """
        # TODO: Implementar
        pass

    def get_statistics(self) -> LogStatistics:
        """
        Calcula estadísticas de las entradas procesadas.

        Returns:
            LogStatistics con métricas calculadas
        """
        # TODO: Implementar
        # 1. Contar total de entradas
        # 2. Contar por nivel
        # 3. Determinar rango de fechas
        # 4. Contar errores (ERROR + CRITICAL)
        pass

    def clear(self) -> None:
        """Limpia entradas y errores."""
        self.entries.clear()
        self.errors.clear()


# ============================================
# TAREA 4: Context Managers
# ============================================

class LogSession:
    """
    Context manager para sesión de procesamiento de logs.

    Maneja:
    - Creación del processor
    - Logging de inicio/fin
    - Estadísticas de la sesión
    """

    def __init__(self, name: str = "LogSession"):
        self.name = name
        self.processor: LogProcessor | None = None
        self.start_time: datetime | None = None
        self.files_processed: int = 0

    def __enter__(self) -> Self:
        """Inicia sesión de procesamiento."""
        # TODO: Implementar
        # 1. Crear LogProcessor
        # 2. Registrar tiempo de inicio
        # 3. Loguear inicio de sesión
        # 4. Retornar self
        pass

    def __exit__(
        self,
        exc_type: type | None,
        exc_val: Exception | None,
        exc_tb: object
    ) -> bool:
        """Finaliza sesión de procesamiento."""
        # TODO: Implementar
        # 1. Calcular duración
        # 2. Loguear fin de sesión con estadísticas
        # 3. Si hubo error, loguear el error
        # 4. Retornar False (no suprimir excepciones)
        pass

    def process_file(self, path: str) -> int:
        """Procesa archivo usando el processor de la sesión."""
        if not self.processor:
            raise RuntimeError("Session not started")

        count = self.processor.process_file(path)
        self.files_processed += 1
        return count


# TODO: Implementar log_transaction como context manager
@contextmanager
def log_transaction(processor: LogProcessor) -> Iterator[LogProcessor]:
    """
    Context manager para transacción de procesamiento.

    Si hay error, hace rollback (limpia las entradas).

    Args:
        processor: LogProcessor a usar

    Yields:
        El processor para usar en el bloque
    """
    # TODO: Implementar
    # 1. Guardar estado inicial (número de entradas)
    # 2. yield processor
    # 3. En caso de error, hacer rollback al estado inicial
    # 4. Loguear resultado
    pass


# TODO: Implementar atomic_write como context manager
@contextmanager
def atomic_write(file_path: str, encoding: str = "utf-8") -> Iterator:
    """
    Context manager para escritura atómica.

    Escribe a archivo temporal y mueve al destino solo si es exitoso.

    Args:
        file_path: Ruta destino
        encoding: Encoding a usar

    Yields:
        File handle para escribir
    """
    # TODO: Implementar
    # 1. Crear archivo temporal
    # 2. yield file handle
    # 3. Si éxito, mover temporal a destino
    # 4. Si error, eliminar temporal
    pass


# ============================================
# TAREA 5: ReportGenerator
# ============================================

class ReportGenerator:
    """
    Genera reportes de análisis de logs.

    Soporta formatos: TXT, JSON, CSV
    """

    def __init__(self, statistics: LogStatistics, entries: list[LogEntry]):
        self.statistics = statistics
        self.entries = entries
        self.generated_at = datetime.now()

    def generate_text(self, path: str) -> None:
        """
        Genera reporte en formato texto.

        Args:
            path: Ruta del archivo de salida
        """
        # TODO: Implementar
        # Usar atomic_write para escritura segura
        pass

    def generate_json(self, path: str) -> None:
        """
        Genera reporte en formato JSON.

        Args:
            path: Ruta del archivo de salida
        """
        # TODO: Implementar
        # Usar atomic_write para escritura segura
        pass

    def generate_csv(self, path: str) -> None:
        """
        Genera CSV con todas las entradas.

        Args:
            path: Ruta del archivo de salida
        """
        # TODO: Implementar
        # Usar atomic_write para escritura segura
        pass


# ============================================
# TAREA 6: Integración
# ============================================

def create_sample_log(path: Path) -> None:
    """Crea archivo de log de ejemplo para testing."""
    sample_logs = """2024-01-15 10:30:45 - INFO - app.main - Application started
2024-01-15 10:30:46 - DEBUG - app.db - Connecting to database
2024-01-15 10:30:47 - INFO - app.db - Database connected successfully
2024-01-15 10:30:48 - DEBUG - app.cache - Initializing cache
2024-01-15 10:31:00 - WARNING - app.cache - Cache miss for key: user_123
2024-01-15 10:31:15 - ERROR - app.api - Failed to fetch data: Connection timeout
2024-01-15 10:31:20 - INFO - app.api - Retrying request...
2024-01-15 10:31:25 - INFO - app.api - Request successful
2024-01-15 10:32:00 - DEBUG - app.main - Processing user request
2024-01-15 10:32:05 - WARNING - app.auth - Invalid token format
2024-01-15 10:32:10 - ERROR - app.auth - Authentication failed for user: guest
2024-01-15 10:33:00 - INFO - app.main - Application shutdown initiated
2024-01-15 10:33:05 - INFO - app.db - Database connection closed
2024-01-15 10:33:10 - INFO - app.main - Application stopped
INVALID LINE WITHOUT PROPER FORMAT
2024-01-15 10:34:00 - CRITICAL - app.main - System failure detected"""

    path.write_text(sample_logs, encoding="utf-8")


def main() -> None:
    """Función principal que demuestra el sistema."""

    print("=" * 60)
    print("SISTEMA DE LOGS Y ANÁLISIS DE ARCHIVOS")
    print("=" * 60)

    # Crear directorio temporal para el proyecto
    with tempfile.TemporaryDirectory() as temp_dir:
        work_dir = Path(temp_dir)
        log_file = work_dir / "app.log"

        # Crear log de ejemplo
        print("\n📝 Creando archivo de log de ejemplo...")
        create_sample_log(log_file)
        print(f"   Archivo creado: {log_file}")

        # TODO: Implementar demostración del sistema
        # 1. Crear LogSession
        # 2. Procesar archivo de log
        # 3. Mostrar estadísticas
        # 4. Filtrar por nivel
        # 5. Generar reportes en todos los formatos

        print("\n⚠️  TODO: Implementar el sistema completo")
        print("   Ver las tareas en el código fuente")

        # Ejemplo de cómo debería funcionar (descomentar cuando esté implementado):
        #
        # with LogSession("Demo") as session:
        #     # Procesar archivo
        #     count = session.process_file(str(log_file))
        #     print(f"\n📊 Entradas procesadas: {count}")
        #
        #     # Obtener estadísticas
        #     stats = session.processor.get_statistics()
        #     print(f"   Total: {stats.total_entries}")
        #     print(f"   Errores: {stats.error_count}")
        #     print(f"   Por nivel: {stats.by_level}")
        #
        #     # Filtrar errores
        #     errors = session.processor.filter_by_level("ERROR", "CRITICAL")
        #     print(f"\n🔴 Errores encontrados: {len(errors)}")
        #     for entry in errors:
        #         print(f"   [{entry.timestamp}] {entry.message}")
        #
        #     # Generar reportes
        #     generator = ReportGenerator(stats, session.processor.entries)
        #
        #     report_txt = work_dir / "report.txt"
        #     report_json = work_dir / "report.json"
        #     report_csv = work_dir / "entries.csv"
        #
        #     generator.generate_text(str(report_txt))
        #     generator.generate_json(str(report_json))
        #     generator.generate_csv(str(report_csv))
        #
        #     print(f"\n📄 Reportes generados:")
        #     print(f"   - {report_txt.name}")
        #     print(f"   - {report_json.name}")
        #     print(f"   - {report_csv.name}")

    print("\n" + "=" * 60)
    print("¡Proyecto completado!")
    print("=" * 60)


if __name__ == "__main__":
    main()
