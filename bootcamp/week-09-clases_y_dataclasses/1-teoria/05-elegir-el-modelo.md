# 05 · Elegir el modelo

⏱️ 50 min

## 🎯 Objetivos

- Comparar tupla, `NamedTuple`, diccionario, `TypedDict`, *dataclass* y clase normal para guardar un mismo dato.
- Elegir la estructura adecuada según el uso.
- Diseñar una clase que reutiliza funciones que ya existen, sin reescribirlas.
- Reconocer cuándo una clase sobra.
- Probar clases con pytest.

---

## 1. El mismo dato, seis formas

Una medida, `"Norte"` con `12.5`:

```python
from dataclasses import dataclass
from typing import NamedTuple, TypedDict

as_tuple = ("Norte", 12.5)

as_dict = {"label": "Norte", "value": 12.5}


class NamedMeasurement(NamedTuple):
    label: str
    value: float | None


class MeasurementDict(TypedDict):
    label: str
    value: float | None


@dataclass(frozen=True, slots=True)
class Measurement:
    label: str
    value: float | None
```

| | Acceso | ¿Cambia? | ¿Errata en un nombre? | Úsala para |
|---|---|---|---|---|
| Tupla | `m[1]` | No | — | Parejas cortas y obvias que se desempaquetan al momento: `for label, value in ...` |
| `NamedTuple` | `m.value` y `m[1]` | No | mypy la ve | Dar nombres a una tupla sin romper el código que la indexaba |
| Diccionario | `m["value"]` | Sí | Pasa: crea una clave nueva | Datos con claves variables: un JSON que llega de fuera, conteos |
| `TypedDict` | `m["value"]` | Sí | mypy la ve | Describir un JSON con forma fija sin convertirlo |
| *Dataclass* | `m.value` | Si quieres (`frozen`) | Con `slots`, falla al ejecutar; mypy la ve | El modelo de tu programa |
| Clase normal | `m.value` | Sí | Pasa, salvo `__slots__` | Objetos con comportamiento y estado interno, más que datos |

Un `TypedDict` es un diccionario normal en ejecución: solo le dice a mypy qué claves y tipos tiene. Una `NamedTuple` es una tupla de verdad: `NamedMeasurement("Norte", 12.5) == ("Norte", 12.5)` da `True`, y eso puede esconder errores. Una *dataclass* es un tipo propio: solo es igual a otra `Measurement`.

![Un árbol de decisión: si los datos llegan de fuera con forma variable, diccionario; si es una pareja que se desempaqueta en el momento, tupla; si necesitas nombres pero el código existente indexa la tupla, NamedTuple; si es el modelo de tu programa, dataclass, frozen si es un valor y sin frozen si acumula datos; si tiene más comportamiento que datos, clase normal](../0-assets/03-elegir-el-modelo.svg)

## 2. La regla práctica

- **Datos que entran o salen** (un JSON, un CSV, una respuesta de una API): diccionarios y listas, como los dejan `json` y `csv`. Conviértelos en tu modelo nada más leerlos y vuelve a diccionario (`asdict`) justo antes de escribir.
- **Datos que tu programa maneja por dentro**: *dataclasses*. Inmutables si son valores; mutables si acumulan.
- **Tuplas**: para parejas que se crean y se desempaquetan en dos líneas, como lo que devuelve `process_lines` o los `.items()` de un diccionario.

Esta separación tiene un nombre que verás en la fase 3: el **modelo** de dominio por dentro y los **datos** en la frontera. En la semana 13, Pydantic hace la conversión y la validación en un solo paso.

## 3. Una clase que reutiliza lo que ya tienes

Tu Observatorio tiene funciones probadas que trabajan con tuplas (`values_of`, `label_means`, `most_common_labels`...). Al crear `Series` no las reescribes: los métodos las **llaman**.

```python
@dataclass(slots=True)
class Series:
    measurements: list[Measurement] = field(default_factory=list)

    @property
    def records(self) -> list[Record]:
        return [(m.label, m.value) for m in self.measurements]

    def means(self) -> dict[str, float]:
        return label_means(values_by_label(self.records))
```

- `records` traduce la serie al formato que esperan las funciones antiguas. Es el único sitio que conoce los dos mundos.
- Cada método es una línea. La lógica sigue en las funciones, con sus tests de las semanas 5 y 6, que siguen pasando.
- Quien usa la serie escribe `series.means()` y no necesita saber que debajo hay tres funciones.

Esto es **refactorizar sin romper**: el informe del Observatorio no cambia ni un carácter, y cada paso se puede comprobar con los tests. Un día quizá muevas la lógica dentro de los métodos; hoy no hace falta.

## 4. Cuándo una clase sobra

No todo tiene que ser una clase. Señales de que sobra:

- **Solo tiene `__init__` y un método.** Es una función con pasos de más. `Summarizer(rows).run()` es `summarize(rows)`.
- **Solo tiene métodos `@staticmethod`.** Es un módulo. En Python, los módulos ya agrupan funciones.
- **Guarda datos que no van juntos.** Si nunca usas `unit` y `readings` a la vez, quizá son dos cosas.
- **La creas "por si acaso" crece.** Cuando crezca, la creas: con los tests, cambiar una tupla por una *dataclass* es lo que haces esta semana.

Las funciones puras de tu Observatorio siguen siendo funciones: reciben datos y devuelven datos, y son lo más fácil de probar. La clase aporta cuando agrupa datos que siempre van juntos (`Scale`) o les da nombre (`Measurement`).

## 5. Probar clases

Las *dataclasses* se prueban como cualquier otro valor, porque `==` compara los campos:

```python
def test_measurement_from_line() -> None:
    assert Measurement.from_line(" Norte ;12,5") == Measurement("Norte", 12.5)


def test_scale_rejects_impossible_thresholds() -> None:
    with pytest.raises(ValueError, match="umbrales imposibles"):
        Scale("µg/m³", 50.0, 10.0)


def test_empty_series_do_not_share_their_list() -> None:
    first, second = Series(), Series()
    first.add(Measurement("Norte", 12.5))
    assert second.measurements == []
```

Qué merece un test:

- **La validación**: que lo imposible no se puede crear.
- **Los constructores alternativos**: entradas válidas e inválidas.
- **Lo que prometes con las opciones**: si es `frozen`, que no se puede asignar; si comparte listas, que no.
- **Los métodos**, con datos pequeños que puedas calcular a mano.

No pruebes lo que genera `@dataclass` campo a campo: es código de la biblioteca estándar. Un test del `repr` basta para saber que es una *dataclass* y que los campos son los que esperas.

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| `NamedTuple` igual a una tupla cualquiera | Una `NamedTuple` sigue siendo una tupla | Si no necesitas indexar, usa una *dataclass* |
| Una errata en una clave de diccionario no da error | Los diccionarios aceptan cualquier clave | Convierte los datos externos en tu modelo nada más leerlos |
| Has reescrito una función que ya existía dentro de un método | Al crear la clase, copiaste la lógica | Haz que el método llame a la función, que ya tiene tests |
| Una clase con un solo método además de `__init__` | Era una función | Vuelve a la función |
| Los tests de las semanas anteriores fallan tras crear la clase | Cambiaste las funciones antiguas en lugar de envolverlas | Las funciones no cambian; la clase las llama |

---

## ✅ Qué debes saber al terminar

- [ ] Qué ofrece cada estructura: tupla, `NamedTuple`, diccionario, `TypedDict`, *dataclass* y clase normal.
- [ ] Dónde van los diccionarios y dónde las *dataclasses* en un programa que lee y escribe archivos.
- [ ] Cómo una clase puede reutilizar funciones existentes en lugar de reescribirlas.
- [ ] Las señales de que una clase sobra.
- [ ] Qué tests merece una *dataclass* y cuáles no.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [04 · *Dataclasses* inmutables y con `slots`](04-dataclasses-inmutables-y-con-slots.md) | **05 · Elegir el modelo** | [Ejercicio 01 · Clases y objetos](../2-practicas/ejercicio-01-clases-y-objetos/README.md) |
