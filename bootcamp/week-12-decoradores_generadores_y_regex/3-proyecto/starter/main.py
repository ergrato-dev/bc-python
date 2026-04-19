"""
Proyecto Semana 12: Sistema de Procesamiento de Logs
====================================================

Sistema que combina decoradores, generadores y regex para
analizar archivos de log de forma eficiente.

Instrucciones:
1. Completa cada sección marcada con TODO
2. Ejecuta para probar con datos de ejemplo
3. Verifica que todos los tests pasen
"""

import functools
import re
import time
import random
from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterator, Callable, ParamSpec, TypeVar, Any
from collections import Counter

P = ParamSpec("P")
R = TypeVar("R")


# ============================================
# SECCIÓN 1: DECORADORES
# ============================================

def timer(func: Callable[P, R]) -> Callable[P, R]:
    """
    Decorador que mide el tiempo de ejecución.

    Debe imprimir: ⏱️ {nombre_función} executed in {tiempo:.4f}s
    """
    # TODO: Implementar decorador timer
    # 1. Usar @functools.wraps(func)
    # 2. Medir tiempo con time.perf_counter()
    # 3. Imprimir tiempo de ejecución
    # 4. Retornar resultado de la función
    pass


def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """
    Decorador que reintenta la función si falla.

    Args:
        max_attempts: Número máximo de intentos
        delay: Segundos entre intentos
        exceptions: Tupla de excepciones a capturar
    """
    # TODO: Implementar decorador retry con argumentos
    # 1. Crear función decorator que recibe func
    # 2. Crear wrapper que intenta max_attempts veces
    # 3. Capturar solo las excepciones especificadas
    # 4. Esperar delay segundos entre intentos
    # 5. Si todos fallan, lanzar última excepción
    pass


def cache(func: Callable[P, R]) -> Callable[P, R]:
    """
    Decorador que cachea resultados por argumentos.

    Usa un diccionario para almacenar resultados.
    La clave debe ser una tupla de (args, kwargs items).
    """
    # TODO: Implementar decorador cache
    # 1. Crear diccionario _cache dentro del closure
    # 2. Generar clave única de args y kwargs
    # 3. Si existe en cache, retornar valor cacheado
    # 4. Si no, ejecutar función y guardar en cache
    pass


def log_calls(func: Callable[P, R]) -> Callable[P, R]:
    """
    Decorador que registra llamadas a funciones.

    Debe imprimir:
    - 📥 Calling {nombre}({args})
    - 📤 {nombre} returned {resultado}
    """
    # TODO: Implementar decorador log_calls
    # 1. Formatear argumentos como string
    # 2. Imprimir antes de llamar
    # 3. Imprimir después con resultado
    pass


# ============================================
# SECCIÓN 2: MODELOS DE DATOS
# ============================================

@dataclass
class LogEntry:
    """Representa una entrada de log parseada."""
    timestamp: datetime
    level: str
    message: str
    metadata: dict[str, str] = field(default_factory=dict)

    @property
    def hour(self) -> int:
        """Retorna la hora del timestamp."""
        return self.timestamp.hour

    def __str__(self) -> str:
        return f"[{self.timestamp}] {self.level}: {self.message}"


# ============================================
# SECCIÓN 3: PATRONES REGEX
# ============================================

# TODO: Definir patrón para parsear línea de log completa
# Formato: [YYYY-MM-DD HH:MM:SS] LEVEL: message
# Grupos nombrados: date, time, level, message
LOG_PATTERN = re.compile(
    r""  # TODO: Completar patrón regex
)

# TODO: Definir patrón para extraer pares key=value
# Formato: key=value (value puede tener letras, números, _, -)
KEY_VALUE_PATTERN = re.compile(
    r""  # TODO: Completar patrón regex
)

# Patrón para direcciones IP (ya implementado como referencia)
IP_PATTERN = re.compile(
    r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
)

# TODO: Patrón para códigos de error (formato: E1234 o ERR-123)
ERROR_CODE_PATTERN = re.compile(
    r""  # TODO: Completar patrón regex
)


# ============================================
# SECCIÓN 4: GENERADORES
# ============================================

def read_logs(filepath: str) -> Iterator[str]:
    """
    Lee archivo de log línea por línea.

    Usa generador para no cargar todo en memoria.
    Ignora líneas vacías.

    Args:
        filepath: Ruta al archivo de log

    Yields:
        Cada línea del archivo (sin newline)
    """
    # TODO: Implementar generador
    # 1. Abrir archivo con context manager
    # 2. Iterar líneas con yield
    # 3. Ignorar líneas vacías
    # 4. Hacer strip() a cada línea
    pass


def parse_entries(lines: Iterator[str]) -> Iterator[LogEntry]:
    """
    Parsea líneas de log a objetos LogEntry.

    Usa LOG_PATTERN para extraer componentes.
    Extrae metadata con KEY_VALUE_PATTERN.

    Args:
        lines: Iterator de líneas de log

    Yields:
        LogEntry por cada línea válida
    """
    # TODO: Implementar generador
    # 1. Para cada línea, aplicar LOG_PATTERN
    # 2. Si no hace match, continuar (skip)
    # 3. Extraer date, time, level, message
    # 4. Parsear timestamp con datetime.strptime
    # 5. Extraer metadata con KEY_VALUE_PATTERN
    # 6. Yield LogEntry
    pass


def filter_by_level(
    entries: Iterator[LogEntry],
    min_level: str
) -> Iterator[LogEntry]:
    """
    Filtra entradas por nivel mínimo.

    Niveles en orden: DEBUG < INFO < WARNING < ERROR < CRITICAL

    Args:
        entries: Iterator de LogEntry
        min_level: Nivel mínimo a incluir

    Yields:
        LogEntry con nivel >= min_level
    """
    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    # TODO: Implementar filtro
    # 1. Obtener índice de min_level
    # 2. Para cada entry, comparar índices
    # 3. Yield si nivel >= min_level
    pass


def filter_by_date(
    entries: Iterator[LogEntry],
    start_date: datetime | None = None,
    end_date: datetime | None = None
) -> Iterator[LogEntry]:
    """
    Filtra entradas por rango de fechas.

    Args:
        entries: Iterator de LogEntry
        start_date: Fecha inicial (inclusive)
        end_date: Fecha final (inclusive)

    Yields:
        LogEntry dentro del rango
    """
    # TODO: Implementar filtro
    # 1. Si start_date, verificar entry.timestamp >= start_date
    # 2. Si end_date, verificar entry.timestamp <= end_date
    # 3. Yield si cumple ambas condiciones
    pass


def extract_errors(entries: Iterator[LogEntry]) -> Iterator[tuple[str, LogEntry]]:
    """
    Extrae mensajes de error categorizados.

    Yields:
        (error_type, LogEntry) para cada ERROR o CRITICAL
    """
    # TODO: Implementar extractor
    # 1. Filtrar solo ERROR y CRITICAL
    # 2. Intentar extraer código de error del mensaje
    # 3. Si no hay código, usar primeras palabras como tipo
    # 4. Yield (error_type, entry)
    pass


# ============================================
# SECCIÓN 5: ANALIZADOR DE LOGS
# ============================================

class LogAnalyzer:
    """Analizador de archivos de log."""

    def __init__(self, filepath: str | None = None):
        """
        Inicializa el analizador.

        Args:
            filepath: Ruta al archivo de log (opcional)
        """
        self.filepath = filepath
        self._entries_cache: list[LogEntry] = []

    def load_from_file(self, filepath: str) -> None:
        """Carga logs desde archivo."""
        self.filepath = filepath
        self._entries_cache = []

    def load_from_lines(self, lines: list[str]) -> None:
        """Carga logs desde lista de líneas."""
        self._entries_cache = list(parse_entries(iter(lines)))

    def create_pipeline(
        self,
        min_level: str = "DEBUG",
        start_date: datetime | None = None,
        end_date: datetime | None = None
    ) -> Iterator[LogEntry]:
        """
        Crea pipeline de procesamiento.

        Args:
            min_level: Nivel mínimo de log
            start_date: Fecha inicial
            end_date: Fecha final

        Returns:
            Iterator de LogEntry filtrados
        """
        # TODO: Implementar pipeline
        # 1. Si hay cache, usar cache
        # 2. Si hay filepath, usar read_logs
        # 3. Encadenar generadores: parse -> filter_level -> filter_date
        pass

    def count_by_level(self, entries: Iterator[LogEntry]) -> dict[str, int]:
        """
        Cuenta entradas por nivel.

        Returns:
            Dict {level: count}
        """
        # TODO: Implementar conteo
        # Usar Counter o dict para contar
        pass

    def errors_per_hour(self, entries: Iterator[LogEntry]) -> dict[int, int]:
        """
        Cuenta errores por hora del día.

        Returns:
            Dict {hour: error_count}
        """
        # TODO: Implementar conteo por hora
        # 1. Filtrar solo ERROR y CRITICAL
        # 2. Agrupar por entry.hour
        pass

    def top_errors(
        self,
        entries: Iterator[LogEntry],
        n: int = 5
    ) -> list[tuple[str, int]]:
        """
        Obtiene los N errores más frecuentes.

        Returns:
            Lista de (error_message, count) ordenada por count
        """
        # TODO: Implementar top errores
        # 1. Filtrar solo ERROR y CRITICAL
        # 2. Contar mensajes
        # 3. Retornar top N
        pass

    def generate_report(
        self,
        min_level: str = "WARNING",
        start_date: datetime | None = None,
        end_date: datetime | None = None
    ) -> str:
        """
        Genera reporte completo de análisis.

        Returns:
            String con reporte formateado
        """
        # TODO: Implementar generación de reporte
        # 1. Crear pipeline con filtros
        # 2. Recopilar estadísticas (count_by_level, errors_per_hour, top_errors)
        # 3. Formatear reporte con barras de progreso
        # 4. Incluir: período, total, por nivel, top errores, por hora
        pass


# ============================================
# SECCIÓN 6: DATOS DE PRUEBA
# ============================================

def generate_sample_logs(n: int = 100) -> list[str]:
    """Genera logs de prueba."""
    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    level_weights = [20, 40, 25, 12, 3]

    messages = {
        "DEBUG": [
            "Cache hit for key={key}",
            "Query executed in {time}ms",
            "Session {session_id} validated",
        ],
        "INFO": [
            "User login successful - user_id={user_id}",
            "Request processed - endpoint={endpoint}",
            "File uploaded - size={size}KB",
        ],
        "WARNING": [
            "High memory usage - {percent}%",
            "Slow query detected - {time}ms",
            "Rate limit approaching - {count}/1000",
        ],
        "ERROR": [
            "Database connection failed - timeout={timeout}s",
            "Authentication failed - user_id={user_id}",
            "File not found - path={path}",
        ],
        "CRITICAL": [
            "System overload - CPU at {percent}%",
            "Disk space critical - {percent}% used",
            "Service unavailable - {service}",
        ],
    }

    logs = []
    base_time = datetime(2024, 1, 15, 8, 0, 0)

    for i in range(n):
        # Timestamp incrementando
        timestamp = base_time.replace(
            hour=8 + (i // 20),
            minute=(i * 3) % 60,
            second=random.randint(0, 59)
        )

        # Nivel aleatorio con pesos
        level = random.choices(levels, weights=level_weights)[0]

        # Mensaje aleatorio
        template = random.choice(messages[level])
        message = template.format(
            key=f"user_{random.randint(100, 999)}",
            time=random.randint(10, 500),
            session_id=f"sess_{random.randint(1000, 9999)}",
            user_id=random.randint(1, 100),
            endpoint=random.choice(["/api/users", "/api/products", "/api/orders"]),
            size=random.randint(10, 5000),
            percent=random.randint(70, 99),
            count=random.randint(800, 990),
            timeout=random.randint(5, 30),
            path=f"/data/file_{random.randint(1, 100)}.txt",
            service=random.choice(["auth", "db", "cache", "api"]),
        )

        log_line = f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {level}: {message}"
        logs.append(log_line)

    return logs


# ============================================
# SECCIÓN 7: MAIN - PRUEBAS
# ============================================

def main():
    """Función principal para probar el sistema."""
    print("=" * 70)
    print("SISTEMA DE PROCESAMIENTO DE LOGS")
    print("=" * 70)
    print()

    # Generar datos de prueba
    print("📝 Generando logs de prueba...")
    sample_logs = generate_sample_logs(100)
    print(f"   Generados {len(sample_logs)} logs")
    print()

    # Mostrar algunos logs de ejemplo
    print("📋 Ejemplos de logs generados:")
    for log in sample_logs[:5]:
        print(f"   {log}")
    print("   ...")
    print()

    # TODO: Descomentar cuando implementes las funciones

    # # Crear analizador
    # print("🔍 Analizando logs...")
    # analyzer = LogAnalyzer()
    # analyzer.load_from_lines(sample_logs)
    #
    # # Generar reporte
    # report = analyzer.generate_report(
    #     min_level="WARNING",
    #     start_date=datetime(2024, 1, 15),
    #     end_date=datetime(2024, 1, 16)
    # )
    #
    # print(report)

    print()
    print("=" * 70)
    print("✅ Implementa las funciones TODO para ver el análisis completo")
    print("=" * 70)


if __name__ == "__main__":
    main()
