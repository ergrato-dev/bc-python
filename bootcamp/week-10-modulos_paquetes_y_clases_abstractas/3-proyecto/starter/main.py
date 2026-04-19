#!/usr/bin/env python3
"""
Proyecto: Sistema de Procesamiento de Datos
===========================================
Framework extensible para procesar datos con plugins.

Este archivo contiene el código inicial con TODOs para implementar.
Sigue las instrucciones y completa cada sección.
"""

from abc import ABC, abstractmethod
from typing import Protocol, Callable, Any
from dataclasses import dataclass


# ============================================
# PARTE 1: INTERFACES (core/interfaces.py)
# ============================================

# Protocol para fuentes de datos
class DataSource(Protocol):
    """
    Protocol para fuentes de datos.

    Cualquier clase que implemente read() es una DataSource válida.
    """

    def read(self) -> list[dict[str, Any]]:
        """Lee datos de la fuente y retorna lista de diccionarios."""
        ...


# Clase abstracta para procesadores
class DataProcessor(ABC):
    """
    Clase abstracta base para procesadores de datos.

    Provee:
    - Validación común de datos
    - Método abstracto process() que subclases deben implementar
    - Logging básico de operaciones
    """

    def __init__(self, name: str | None = None):
        self.name = name or self.__class__.__name__
        self._processed_count = 0

    @abstractmethod
    def process(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Procesa los datos y retorna el resultado.

        Args:
            data: Lista de diccionarios a procesar

        Returns:
            Lista de diccionarios procesados
        """
        ...

    def validate(self, data: list[dict[str, Any]]) -> bool:
        """Valida que los datos sean válidos para procesar."""
        if not isinstance(data, list):
            return False
        return True

    def run(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Ejecuta validación y procesamiento."""
        if not self.validate(data):
            raise ValueError(f"[{self.name}] Invalid data format")

        result = self.process(data)
        self._processed_count += 1
        return result

    @property
    def stats(self) -> dict[str, Any]:
        """Estadísticas del procesador."""
        return {
            "name": self.name,
            "processed_count": self._processed_count,
        }


# Protocol para salidas de datos
class DataOutput(Protocol):
    """
    Protocol para salidas de datos.

    Cualquier clase que implemente write() es una DataOutput válida.
    """

    def write(self, data: list[dict[str, Any]]) -> None:
        """Escribe los datos a la salida."""
        ...


# ============================================
# PARTE 2: SOURCES (sources/)
# ============================================

class MemorySource:
    """
    Fuente de datos en memoria.

    TODO: Implementar completamente
    """

    def __init__(self, data: list[dict[str, Any]]):
        # TODO: Almacenar los datos
        # self._data = ...
        pass

    def read(self) -> list[dict[str, Any]]:
        """Lee datos de memoria."""
        # TODO: Retornar copia de los datos
        # return ...
        pass


class CSVSource:
    """
    Fuente de datos desde archivo CSV.

    TODO: Implementar completamente
    """

    def __init__(self, filepath: str):
        # TODO: Almacenar ruta del archivo
        # self.filepath = ...
        pass

    def read(self) -> list[dict[str, Any]]:
        """Lee datos desde CSV."""
        # TODO: Implementar lectura de CSV
        # Hint: Usa csv.DictReader
        # import csv
        # with open(self.filepath, 'r') as f:
        #     reader = csv.DictReader(f)
        #     return list(reader)
        pass


class JSONSource:
    """
    Fuente de datos desde archivo JSON.

    TODO: Implementar completamente
    """

    def __init__(self, filepath: str):
        # TODO: Almacenar ruta del archivo
        pass

    def read(self) -> list[dict[str, Any]]:
        """Lee datos desde JSON."""
        # TODO: Implementar lectura de JSON
        # import json
        # with open(self.filepath, 'r') as f:
        #     return json.load(f)
        pass


# ============================================
# PARTE 3: PROCESSORS (processors/)
# ============================================

class FilterProcessor(DataProcessor):
    """
    Procesador que filtra datos por condición.

    TODO: Implementar completamente
    """

    def __init__(self, key: str, value: Any):
        super().__init__(name=f"Filter[{key}={value}]")
        # TODO: Almacenar key y value
        # self.key = ...
        # self.value = ...
        pass

    def process(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Filtra items donde key == value."""
        # TODO: Implementar filtrado
        # return [item for item in data if item.get(self.key) == self.value]
        pass


class TransformProcessor(DataProcessor):
    """
    Procesador que transforma un campo usando una función.

    TODO: Implementar completamente
    """

    def __init__(self, key: str, fn: Callable[[Any], Any]):
        super().__init__(name=f"Transform[{key}]")
        # TODO: Almacenar key y función
        # self.key = ...
        # self.fn = ...
        pass

    def process(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Aplica función al campo especificado."""
        # TODO: Implementar transformación
        # result = []
        # for item in data:
        #     new_item = item.copy()
        #     if self.key in new_item:
        #         new_item[self.key] = self.fn(new_item[self.key])
        #     result.append(new_item)
        # return result
        pass


class AggregateProcessor(DataProcessor):
    """
    Procesador que agrega datos por un campo.

    TODO: Implementar completamente
    """

    def __init__(self, group_by: str, aggregate_key: str, operation: str = "sum"):
        super().__init__(name=f"Aggregate[{group_by}]")
        # TODO: Almacenar configuración
        # self.group_by = ...
        # self.aggregate_key = ...
        # self.operation = ...  # "sum", "count", "avg"
        pass

    def process(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Agrega datos por grupo."""
        # TODO: Implementar agregación
        # Hint: Usa defaultdict para agrupar
        # from collections import defaultdict
        # groups = defaultdict(list)
        # for item in data:
        #     key = item.get(self.group_by)
        #     groups[key].append(item.get(self.aggregate_key, 0))
        # ...
        pass


# ============================================
# PARTE 4: OUTPUTS (outputs/)
# ============================================

class ConsoleOutput:
    """
    Salida a consola.

    TODO: Implementar completamente
    """

    def __init__(self, pretty: bool = True):
        # TODO: Almacenar configuración
        # self.pretty = ...
        pass

    def write(self, data: list[dict[str, Any]]) -> None:
        """Imprime datos en consola."""
        # TODO: Implementar impresión
        # for item in data:
        #     if self.pretty:
        #         print(json.dumps(item, indent=2))
        #     else:
        #         print(item)
        pass


class FileOutput:
    """
    Salida a archivo JSON.

    TODO: Implementar completamente
    """

    def __init__(self, filepath: str):
        # TODO: Almacenar ruta
        pass

    def write(self, data: list[dict[str, Any]]) -> None:
        """Escribe datos a archivo JSON."""
        # TODO: Implementar escritura
        # import json
        # with open(self.filepath, 'w') as f:
        #     json.dump(data, f, indent=2)
        pass


# ============================================
# PARTE 5: PIPELINE (core/pipeline.py)
# ============================================

@dataclass
class DataPipeline:
    """
    Pipeline que conecta source -> processors -> output.

    TODO: Implementar completamente
    """

    source: DataSource
    processors: list[DataProcessor]
    output: DataOutput

    def run(self) -> list[dict[str, Any]]:
        """
        Ejecuta el pipeline completo.

        1. Lee datos de source
        2. Aplica cada processor en orden
        3. Escribe resultado a output
        4. Retorna datos procesados
        """
        # TODO: Implementar ejecución del pipeline
        # data = self.source.read()
        #
        # for processor in self.processors:
        #     data = processor.run(data)
        #
        # self.output.write(data)
        # return data
        pass

    def add_processor(self, processor: DataProcessor) -> "DataPipeline":
        """Añade un procesador al pipeline."""
        # TODO: Implementar
        # self.processors.append(processor)
        # return self
        pass


# ============================================
# PARTE 6: REGISTRY (core/registry.py)
# ============================================

class PluginRegistry:
    """
    Registro central de plugins.

    TODO: Implementar completamente
    """

    def __init__(self):
        # TODO: Inicializar registros
        # self._sources: dict[str, type] = {}
        # self._processors: dict[str, type] = {}
        # self._outputs: dict[str, type] = {}
        pass

    def register_source(self, name: str, source_class: type) -> None:
        """Registra una fuente de datos."""
        # TODO: Implementar
        pass

    def register_processor(self, name: str, processor_class: type) -> None:
        """Registra un procesador."""
        # TODO: Implementar
        pass

    def register_output(self, name: str, output_class: type) -> None:
        """Registra una salida."""
        # TODO: Implementar
        pass

    def get_source(self, name: str) -> type:
        """Obtiene una fuente por nombre."""
        # TODO: Implementar
        pass

    def list_plugins(self) -> dict[str, list[str]]:
        """Lista todos los plugins registrados."""
        # TODO: Implementar
        # return {
        #     "sources": list(self._sources.keys()),
        #     "processors": list(self._processors.keys()),
        #     "outputs": list(self._outputs.keys()),
        # }
        pass


# ============================================
# PARTE 7: DEMOSTRACIÓN
# ============================================

def main():
    """Demostración del sistema de procesamiento."""
    print("=" * 60)
    print("Sistema de Procesamiento de Datos")
    print("=" * 60)

    # Datos de ejemplo
    sample_data = [
        {"name": "Alice", "age": 30, "city": "NYC", "salary": 75000},
        {"name": "Bob", "age": 25, "city": "LA", "salary": 60000},
        {"name": "Charlie", "age": 35, "city": "NYC", "salary": 90000},
        {"name": "Diana", "age": 28, "city": "LA", "salary": 70000},
        {"name": "Eve", "age": 32, "city": "NYC", "salary": 85000},
    ]

    print("\n📊 Datos originales:")
    for item in sample_data:
        print(f"  {item}")

    # TODO: Descomentar cuando esté implementado
    #
    # print("\n🔧 Creando pipeline...")
    #
    # pipeline = DataPipeline(
    #     source=MemorySource(sample_data),
    #     processors=[
    #         FilterProcessor(key="city", value="NYC"),
    #         TransformProcessor(key="name", fn=str.upper),
    #     ],
    #     output=ConsoleOutput(pretty=False),
    # )
    #
    # print("\n📤 Resultado (filtrado NYC + nombres mayúsculas):")
    # result = pipeline.run()
    #
    # print(f"\n📈 Procesados: {len(result)} registros")

    print("\n" + "=" * 60)
    print("TODO: Implementa las clases para ver el resultado")
    print("=" * 60)


if __name__ == "__main__":
    main()
