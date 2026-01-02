"""
Ejercicio 03: Context Managers Personalizados
=============================================

Aprende a crear tus propios context managers.

Instrucciones:
1. Lee cada sección y descomenta el código
2. Ejecuta el script después de cada paso
3. Observa cómo funcionan los context managers

Ejecutar:
    python main.py
"""

from contextlib import contextmanager
from typing import Iterator, Self
from pathlib import Path
import time
import tempfile


def main() -> None:
    """Función principal del ejercicio."""

    print("=" * 60)
    print("EJERCICIO: Context Managers Personalizados")
    print("=" * 60)

    # ============================================
    # PASO 1: Context Manager con Clase
    # ============================================
    print("\n--- Paso 1: Context Manager con Clase ---")

    # Descomenta las siguientes líneas:
    # class Timer:
    #     """Context manager para medir tiempo de ejecución."""
    #
    #     def __init__(self, name: str = "Timer"):
    #         self.name = name
    #         self.start_time: float = 0
    #         self.elapsed: float = 0
    #
    #     def __enter__(self) -> Self:
    #         """Se ejecuta al entrar al bloque with."""
    #         self.start_time = time.perf_counter()
    #         print(f"  [{self.name}] Iniciando...")
    #         return self
    #
    #     def __exit__(
    #         self,
    #         exc_type: type | None,
    #         exc_val: Exception | None,
    #         exc_tb: object
    #     ) -> bool:
    #         """Se ejecuta al salir del bloque with."""
    #         self.elapsed = time.perf_counter() - self.start_time
    #         print(f"  [{self.name}] Completado en {self.elapsed:.4f}s")
    #
    #         if exc_type:
    #             print(f"  [{self.name}] Error detectado: {exc_val}")
    #
    #         return False  # No suprimir excepciones
    #
    #
    # # Uso básico
    # with Timer("Operación 1"):
    #     time.sleep(0.1)
    #     data = [x ** 2 for x in range(10000)]
    #
    # # Acceder al tiempo después
    # with Timer("Operación 2") as t:
    #     time.sleep(0.05)
    # print(f"  Tiempo guardado: {t.elapsed:.4f}s")

    # ============================================
    # PASO 2: @contextmanager Decorador
    # ============================================
    print("\n--- Paso 2: @contextmanager ---")

    # Descomenta las siguientes líneas:
    # @contextmanager
    # def simple_timer(name: str) -> Iterator[None]:
    #     """Context manager simple para timing."""
    #     print(f"  [{name}] Iniciando...")
    #     start = time.perf_counter()
    #
    #     try:
    #         yield  # Aquí se ejecuta el bloque with
    #     finally:
    #         elapsed = time.perf_counter() - start
    #         print(f"  [{name}] Completado en {elapsed:.4f}s")
    #
    #
    # # Uso
    # with simple_timer("Cálculo"):
    #     result = sum(range(100000))
    #     print(f"  Resultado: {result}")

    # ============================================
    # PASO 3: Context Manager con Recursos
    # ============================================
    print("\n--- Paso 3: Gestión de Recursos ---")

    # Descomenta las siguientes líneas:
    # class ManagedFile:
    #     """Context manager para archivos con logging."""
    #
    #     def __init__(self, path: str, mode: str = "r"):
    #         self.path = Path(path)
    #         self.mode = mode
    #         self._file = None
    #
    #     def __enter__(self):
    #         print(f"  Abriendo: {self.path.name} (modo: {self.mode})")
    #         self._file = open(self.path, self.mode, encoding="utf-8")
    #         return self._file
    #
    #     def __exit__(self, exc_type, exc_val, exc_tb):
    #         if self._file:
    #             self._file.close()
    #             print(f"  Cerrado: {self.path.name}")
    #         return False
    #
    #
    # # Probar con archivo temporal
    # with tempfile.NamedTemporaryFile(
    #     mode="w", suffix=".txt", delete=False, encoding="utf-8"
    # ) as tmp:
    #     tmp.write("Contenido de prueba")
    #     tmp_path = tmp.name
    #
    # with ManagedFile(tmp_path, "r") as f:
    #     content = f.read()
    #     print(f"  Contenido: {content}")
    #
    # Path(tmp_path).unlink()  # Limpiar

    # ============================================
    # PASO 4: Context Manager con @contextmanager
    # ============================================
    print("\n--- Paso 4: Recursos con @contextmanager ---")

    # Descomenta las siguientes líneas:
    # @contextmanager
    # def temporary_file(content: str) -> Iterator[Path]:
    #     """Crea archivo temporal que se elimina automáticamente."""
    #     # Setup
    #     tmp = tempfile.NamedTemporaryFile(
    #         mode="w", suffix=".txt", delete=False, encoding="utf-8"
    #     )
    #     tmp.write(content)
    #     tmp.close()
    #     path = Path(tmp.name)
    #     print(f"  Archivo temporal creado: {path.name}")
    #
    #     try:
    #         yield path
    #     finally:
    #         # Cleanup - siempre se ejecuta
    #         if path.exists():
    #             path.unlink()
    #             print(f"  Archivo temporal eliminado: {path.name}")
    #
    #
    # with temporary_file("Datos temporales") as tmp_path:
    #     print(f"  Usando archivo: {tmp_path}")
    #     print(f"  Contenido: {tmp_path.read_text()}")
    #
    # print(f"  ¿Existe después?: {tmp_path.exists()}")

    # ============================================
    # PASO 5: Context Managers Anidados
    # ============================================
    print("\n--- Paso 5: Context Managers Anidados ---")

    # Descomenta las siguientes líneas:
    # @contextmanager
    # def indented_print(prefix: str = "  ") -> Iterator[None]:
    #     """Context manager que indenta la salida."""
    #     import builtins
    #     original_print = builtins.print
    #
    #     def indented(*args, **kwargs):
    #         if args:
    #             args = (prefix + str(args[0]),) + args[1:]
    #         original_print(*args, **kwargs)
    #
    #     builtins.print = indented
    #     try:
    #         yield
    #     finally:
    #         builtins.print = original_print
    #
    #
    # # Múltiples context managers (Python 3.10+)
    # with (
    #     simple_timer("Total"),
    #     indented_print("    "),
    # ):
    #     print("Operación 1")
    #     time.sleep(0.05)
    #     print("Operación 2")
    #     time.sleep(0.05)

    # ============================================
    # PASO 6: Ejercicio Integrador
    # ============================================
    print("\n--- Paso 6: Ejercicio Integrador ---")

    # Crea un context manager para conexión simulada

    # Descomenta las siguientes líneas:
    # class DatabaseConnection:
    #     """Simulación de conexión a base de datos."""
    #
    #     def __init__(self, host: str, database: str):
    #         self.host = host
    #         self.database = database
    #         self._connected = False
    #         self._transaction_active = False
    #
    #     def __enter__(self) -> Self:
    #         self._connect()
    #         return self
    #
    #     def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
    #         if exc_type:
    #             print(f"  [DB] Error: {exc_val}")
    #             if self._transaction_active:
    #                 self.rollback()
    #         else:
    #             if self._transaction_active:
    #                 self.commit()
    #
    #         self._disconnect()
    #         return False
    #
    #     def _connect(self) -> None:
    #         print(f"  [DB] Conectando a {self.database}@{self.host}...")
    #         time.sleep(0.05)  # Simular conexión
    #         self._connected = True
    #         print(f"  [DB] Conectado")
    #
    #     def _disconnect(self) -> None:
    #         if self._connected:
    #             print(f"  [DB] Desconectando...")
    #             self._connected = False
    #
    #     def begin_transaction(self) -> None:
    #         print(f"  [DB] Iniciando transacción")
    #         self._transaction_active = True
    #
    #     def commit(self) -> None:
    #         print(f"  [DB] COMMIT")
    #         self._transaction_active = False
    #
    #     def rollback(self) -> None:
    #         print(f"  [DB] ROLLBACK")
    #         self._transaction_active = False
    #
    #     def execute(self, query: str) -> list[dict]:
    #         if not self._connected:
    #             raise RuntimeError("No hay conexión activa")
    #         print(f"  [DB] Ejecutando: {query}")
    #         return [{"result": "ok"}]
    #
    #
    # # Caso exitoso
    # print("\n  Caso exitoso:")
    # with DatabaseConnection("localhost", "mydb") as db:
    #     db.begin_transaction()
    #     db.execute("INSERT INTO users VALUES (...)")
    #     db.execute("UPDATE stats SET count = count + 1")
    #
    # # Caso con error
    # print("\n  Caso con error:")
    # try:
    #     with DatabaseConnection("localhost", "mydb") as db:
    #         db.begin_transaction()
    #         db.execute("INSERT INTO users VALUES (...)")
    #         raise ValueError("Error simulado!")
    # except ValueError:
    #     print("  Error capturado externamente")

    print("\n" + "=" * 60)
    print("¡Ejercicio completado!")
    print("=" * 60)


if __name__ == "__main__":
    main()
