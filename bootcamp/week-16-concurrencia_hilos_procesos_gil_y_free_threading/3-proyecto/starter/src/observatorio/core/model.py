"""El modelo del Observatorio: la escala, la medida y la serie, como clases.

Qué: tres dataclasses que agrupan datos que hasta ahora viajaban sueltos: la unidad y
los umbrales, la etiqueta y el valor, y la lista de registros.
Para qué: una medida con nombres (measurement.value) se lee mejor que una tupla
(record[1]), y unos umbrales imposibles fallan al crear la escala, no a mitad del informe.
Impacto: los métodos reutilizan las funciones de las capas anteriores, que no cambian.
En la semana 13, Pydantic valida estos mismos modelos cuando llegan de un archivo o de
una API.
"""

from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass, field

from observatorio.core.groups import (
    Record,
    distinct_labels,
    label_means,
    parse_record,
    records_of,
    values_by_label,
)
from observatorio.core.rules import classify, format_row
from observatorio.core.trends import most_common_labels, values_of


@dataclass(frozen=True, slots=True)
class Scale:
    """La unidad y los dos umbrales con los que se clasifica cada medida.

    Inmutable: la escala se decide una vez, al arrancar, y no cambia mientras corre
    el programa. Si low no es menor que high, crearla lanza ValueError.
    """

    unit: str
    low: float
    high: float

    def __post_init__(self) -> None:
        if self.low >= self.high:
            raise ValueError(
                f"umbrales imposibles: low ({self.low}) debe ser menor que high ({self.high})"
            )

    def level(self, value: float | None) -> str:
        """El nivel de value con estos umbrales: "sin dato", "bajo", "medio" o "alto"."""
        return classify(value, self.low, self.high)

    def row(self, measurement: Measurement) -> str:
        """La fila de ancho fijo de format_row, con la unidad y el nivel de la escala."""
        value = measurement.value
        return format_row(measurement.label, value, self.unit, self.level(value))


@dataclass(frozen=True, slots=True)
class Measurement:
    """Una medida: su etiqueta y su valor, None si falta el dato.

    Inmutable y comparable: dos medidas con la misma etiqueta y el mismo valor son
    iguales, y se pueden guardar en un set o usar como clave de un diccionario.
    """

    label: str
    value: float | None

    @classmethod
    def from_line(cls, line: str) -> Measurement | None:
        """Crea la medida de una línea "etiqueta;valor", con las reglas de parse_record.

        Devuelve None si la línea no es válida. Ejemplo: Measurement.from_line("Sur;NA")
        da Measurement(label='Sur', value=None).
        """
        record = parse_record(line)
        if record is None:
            return None
        return cls(*record)

    def __str__(self) -> str:
        """La medida como línea "etiqueta;valor", con coma decimal y "NA" si falta el valor.

        Es la inversa de from_line: Measurement.from_line(str(medida)) == medida.
        """
        text = "NA" if self.value is None else str(self.value).replace(".", ",")
        return f"{self.label};{text}"

    @property
    def has_value(self) -> bool:
        """True si la medida tiene valor."""
        return self.value is not None


@dataclass(slots=True)
class Series:
    """Las medidas de un archivo o de una entrada, en el orden en que llegan.

    Mutable: add añade medidas. Cada serie tiene su propia lista (default_factory),
    así que dos series vacías no comparten nada.
    """

    measurements: list[Measurement] = field(default_factory=list)

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> Series:
        """Crea la serie con las medidas de las líneas válidas, con las reglas de records_of."""
        return cls([Measurement(label, value) for label, value in records_of(lines)])

    def __len__(self) -> int:
        """El número de medidas: len(serie). Una serie vacía es falsa en un if."""
        return len(self.measurements)

    def __iter__(self) -> Iterator[Measurement]:
        """Las medidas en orden: for medida in serie. También hace funcionar `in`."""
        yield from self.measurements

    def __getitem__(self, index: int) -> Measurement:
        """La medida en la posición index: serie[0], serie[-1]."""
        return self.measurements[index]

    def __add__(self, other: Series) -> Series:
        """Una serie nueva con las medidas de las dos: serie_a + serie_b."""
        if not isinstance(other, Series):
            return NotImplemented
        return Series(self.measurements + other.measurements)

    def where(self, keep: Callable[[Measurement], bool]) -> Series:
        """Una serie nueva con las medidas para las que keep devuelve True, en orden.

        keep es una función: serie.where(lambda m: m.label == "Norte") o serie.where(above(50)).
        """
        return Series([measurement for measurement in self.measurements if keep(measurement)])

    def add(self, measurement: Measurement) -> None:
        """Añade una medida al final de la serie."""
        self.measurements.append(measurement)

    @property
    def records(self) -> list[Record]:
        """Las medidas como tuplas (etiqueta, valor), para las funciones de las capas 4 a 6."""
        return [(measurement.label, measurement.value) for measurement in self.measurements]

    def values(self) -> list[float]:
        """Los valores que no son None, en orden."""
        return values_of(self.records)

    def labels(self) -> set[str]:
        """Las etiquetas distintas, también las que solo tienen None."""
        return distinct_labels(self.records)

    def means(self) -> dict[str, float]:
        """La media de cada etiqueta con algún valor."""
        return label_means(values_by_label(self.records))

    def most_common(self, n: int) -> list[tuple[str, int]]:
        """Las n etiquetas que más se repiten, con su número de medidas."""
        return most_common_labels(self.records, n)
