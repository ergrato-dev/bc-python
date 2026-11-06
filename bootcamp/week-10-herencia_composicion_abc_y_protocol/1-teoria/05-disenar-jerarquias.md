# 05 · Diseñar jerarquías

⏱️ 50 min

## 🎯 Objetivos

- Heredar de una *dataclass* sin tropezar con el orden de los campos, `frozen` y `slots`.
- Leer la MRO de una clase con varias bases y usar un *mixin* pequeño.
- Mantener las jerarquías planas y saber cuándo basta una función.
- Entender el diseño de las fuentes de tu proyecto.
- Probar una jerarquía: cada clase concreta, la base y los objetos de prueba.

---

## 1. Heredar de una *dataclass*

Una subclase con `@dataclass` añade sus campos **detrás** de los de la base, y el `__init__` generado los pide en ese orden. Con valores por defecto, eso choca con la regla de la semana 9:

```python
@dataclass
class Sensor:
    name: str
    unit: str = "µg/m³"


@dataclass
class AirSensor(Sensor):
    pollutant: str           # sin valor por defecto, detrás de unit, que sí lo tiene
```

```
TypeError: non-default argument 'pollutant' follows default argument 'unit'
```

Dos arreglos:

- Darle valor por defecto al campo nuevo: `pollutant: str = "PM2.5"`.
- Hacer que los campos nuevos se pasen por nombre con `kw_only=True` (semana 9): `@dataclass(kw_only=True)` en la subclase, y se crea con `AirSensor("Centro", pollutant="PM2.5")`.

Otras dos reglas:

| Base | Subclase | Qué pasa |
|---|---|---|
| `@dataclass(frozen=True)` | `@dataclass` (sin `frozen`) | `TypeError: cannot inherit non-frozen dataclass from a frozen one` |
| `@dataclass(frozen=True)` | Sin `@dataclass` | Funciona: no puedes reasignar los campos de la base, pero sí crear atributos nuevos |
| `@dataclass(slots=True)` | Sin `@dataclass` | La subclase vuelve a tener `__dict__`: `slots` no se hereda |

Por eso en tu proyecto `FileSource` es `@dataclass(frozen=True)` sin `slots`, y `TextFile` y `CsvFile` no llevan decorador: no añaden campos, solo sustituyen `lines()`.

## 2. Varias bases y *mixins*

Una clase puede heredar de varias:

```python
class JsonMixin:
    """Añade to_json() a cualquier clase cuyos atributos se puedan pasar a JSON."""

    def to_json(self) -> str:
        return json.dumps(vars(self), ensure_ascii=False)


@dataclass
class Station(JsonMixin):
    name: str
    city: str


Station("Norte", "Lima").to_json()     # '{"name": "Norte", "city": "Lima"}'
```

Un ***mixin*** es una clase pequeña, sin `__init__` ni campos, que solo aporta métodos para "mezclar" en otras. Se reconoce por el nombre (`...Mixin`) y porque no tiene sentido crearla sola. Bien usado ahorra repetir un método en varias clases; mal usado, una clase con cinco *mixins* obliga a abrir cinco archivos para saber qué hace un método.

Con varias bases, la MRO deja de ser una línea recta. Python la calcula para que cada clase aparezca **una vez** y siempre antes que sus bases:

```python
class A:
    def hello(self) -> list[str]:
        return ["A"]

class B(A):
    def hello(self) -> list[str]:
        return ["B", *super().hello()]

class C(A):
    def hello(self) -> list[str]:
        return ["C", *super().hello()]

class D(B, C):
    def hello(self) -> list[str]:
        return ["D", *super().hello()]


[cls.__name__ for cls in D.__mro__]   # ['D', 'B', 'C', 'A', 'object']
D().hello()                           # ['D', 'B', 'C', 'A']
```

Fíjate en `B`: su `super()` no llama a `A`, sino a `C`, la **siguiente en la MRO de `D`**. Es lo que se anunció en la teoría 01: `super()` significa "el siguiente", no "mi padre". Gracias a eso, `A.hello` se ejecuta una sola vez. No necesitas dominar esto para el día a día; sí saber que existe cuando una jerarquía con varias bases hace algo raro, y que `Clase.__mro__` te dice el orden real.

## 3. Jerarquías planas

Una jerarquía profunda (`Sensor` → `EnvironmentalSensor` → `AirSensor` → `ParticleSensor` → `PM25Sensor`) obliga a recorrer cinco clases para saber qué hace un método, y cualquier cambio arriba se propaga a todos los de abajo. Algunas señales de que sobra herencia:

- Una subclase que sustituye casi todo lo de la base: no "es una" base, solo se parece.
- Una subclase que existe para fijar un valor (`class PM25Sensor(AirSensor)` con `pollutant = "PM2.5"`): basta con un argumento.
- Una subclase por cada combinación de opciones: compón (teoría 02).
- Una base con un solo hijo "por si un día hay más": espera a que haya dos.

En Python, uno o dos niveles bastan casi siempre. Y a veces ni eso: si solo necesitas elegir entre dos comportamientos, una **función** que devuelve el objeto adecuado es más simple que una clase "fábrica". Es lo que hace `open_file` en tu proyecto.

## 4. El diseño de las fuentes

Cada pieza de `sources.py` responde a una pregunta:

| Pregunta | Respuesta | Herramienta |
|---|---|---|
| ¿Qué necesita `main` de una fuente? | Un método `lines()` | `Protocol` `Source` |
| ¿Y las líneas que ya están en memoria? | Un objeto con `lines()`; no tiene ruta, así que no es un archivo | `LinesSource`, sin herencia |
| ¿Qué comparten un `.txt` y un `.csv`? | La ruta, el `__init__`, `__eq__`, la inmutabilidad | Base abstracta `FileSource` |
| ¿Qué cambia entre ellos? | Cómo se leen | `lines()` en cada subclase, que llama a `read_lines` o `read_csv` |
| ¿Quién elige la clase? | Una regla de una línea sobre la extensión | Función `open_file` |

Y lo que **no** se hizo:

- `LinesSource` no hereda de `FileSource`: no tiene `path`, y heredarlo sería mentir ("es un archivo").
- `Source` no es una ABC: obligaría a `LinesSource` y a cada objeto de prueba a heredar de ella.
- `read_lines`, `read_csv` y `read_data` no cambian: las subclases las llaman. Las pruebas de la semana 7 siguen protegiendo la lectura.

## 5. Probar una jerarquía

| Qué | Cómo |
|---|---|
| Cada clase concreta | Un test por subclase con un archivo pequeño en `tmp_path` |
| La base abstracta | `pytest.raises(TypeError, match="abstract")` al crearla, con `# type: ignore[abstract]` para mypy |
| Una subclase incompleta | Una clase definida dentro del test sin el método: también lanza `TypeError` |
| Quién cumple el `Protocol` | `isinstance(objeto, Source)` si es `@runtime_checkable`; mypy comprueba las firmas |
| Código que usa la fuente | Un objeto de prueba con `lines()` en lugar de un archivo real |

El último punto es la gran ventaja del `Protocol`: para probar algo que necesita una fuente, no hace falta crear archivos. Basta con `LinesSource(["Norte;12,5"])`, o una clase de tres líneas dentro del test. `test_main_reads_files_through_open_file` va un paso más allá: con `monkeypatch.setattr` cambia `open_file` dentro de `__main__` por una función que devuelve una fuente en memoria. En la semana 14 verás `monkeypatch` y los *mocks* con calma.

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| `TypeError: non-default argument 'pollutant' follows default argument 'unit'` | La subclase añade un campo sin valor por defecto detrás de uno con valor | Valor por defecto, o `@dataclass(kw_only=True)` en la subclase |
| `TypeError: cannot inherit non-frozen dataclass from a frozen one` | Base `frozen` y subclase `@dataclass` sin `frozen` | `@dataclass(frozen=True)` también en la subclase, o sin decorador si no añade campos |
| Un objeto con `slots` acepta atributos inventados | Es una subclase sin `@dataclass(slots=True)` | Decora también la subclase |
| `super()` llama a un método inesperado | Varias bases: `super()` sigue la MRO de la clase del objeto | Mira `Clase.__mro__` |
| `TypeError: Cannot create a consistent method resolution order (MRO)` | Bases en un orden imposible (`class D(A, B)` con `B(A)`) | Pon la subclase antes que su base: `class D(B, A)` |

---

## ✅ Qué debes saber al terminar

- [ ] Las tres reglas de herencia de *dataclasses*: orden de campos, `frozen` y `slots`.
- [ ] Qué es un *mixin* y por qué `super()` sigue la MRO.
- [ ] Las señales de que una jerarquía sobra y cuándo basta una función.
- [ ] Por qué en tu proyecto `Source` es un `Protocol`, `FileSource` una ABC y `open_file` una función.
- [ ] Cómo se prueba una base abstracta y código que usa un `Protocol`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [04 · `Protocol`](04-protocol.md) | **05 · Diseñar jerarquías** | [Ejercicio 01 · Herencia](../2-practicas/ejercicio-01-herencia/README.md) |
