"""
Sistema de historial para la calculadora.
"""
import json
import csv
import io
from datetime import datetime
from typing import Any


class HistoryManager:
    """Gestiona el historial de operaciones de la calculadora."""

    def __init__(self) -> None:
        """Inicializa el historial vacío."""
        self._entries: list[dict[str, Any]] = []

    def record(
        self,
        operation: str,
        operands: dict[str, Any],
        result: Any,
    ) -> None:
        """
        Registra una operación en el historial.

        Args:
            operation: Nombre de la operación
            operands: Diccionario con los operandos
            result: Resultado de la operación
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "operands": operands,
            "result": result,
        }
        self._entries.append(entry)

    def get_all(self) -> list[dict[str, Any]]:
        """
        Obtiene todas las entradas del historial.

        Returns:
            Lista de entradas (copia)
        """
        return self._entries.copy()

    def get_last(self, n: int = 1) -> list[dict[str, Any]]:
        """
        Obtiene las últimas n entradas.

        Args:
            n: Número de entradas a obtener

        Returns:
            Lista con las últimas n entradas
        """
        return self._entries[-n:]

    def clear(self) -> None:
        """Limpia el historial."""
        self._entries.clear()

    def count(self) -> int:
        """
        Retorna el número de entradas en el historial.

        Returns:
            Número de operaciones registradas
        """
        return len(self._entries)

    def export(self, format: str = "json") -> str:
        """
        Exporta el historial en el formato especificado.

        Args:
            format: "json" o "csv"

        Returns:
            String con el historial formateado

        Raises:
            ValueError: Si el formato no es soportado
        """
        match format.lower():
            case "json":
                return self._export_json()
            case "csv":
                return self._export_csv()
            case _:
                raise ValueError(f"Unsupported format: {format}")

    def _export_json(self) -> str:
        """Exporta el historial como JSON."""
        return json.dumps(self._entries, indent=2)

    def _export_csv(self) -> str:
        """Exporta el historial como CSV."""
        if not self._entries:
            return "timestamp,operation,operands,result\n"

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["timestamp", "operation", "operands", "result"])

        for entry in self._entries:
            writer.writerow([
                entry["timestamp"],
                entry["operation"],
                json.dumps(entry["operands"]),
                entry["result"],
            ])

        return output.getvalue()

    def filter_by_operation(self, operation: str) -> list[dict[str, Any]]:
        """
        Filtra el historial por tipo de operación.

        Args:
            operation: Nombre de la operación a filtrar

        Returns:
            Lista de entradas que coinciden
        """
        return [e for e in self._entries if e["operation"] == operation]
