# 05 · Pipelines perezosos

⏱️ 45 min

## 🎯 Objetivos

- Encadenar generadores en una tubería que procesa un dato cada vez.
- Trabajar con entradas infinitas usando `itertools` (`islice`, `count`, `cycle`, `takewhile`, `chain`, `batched`).
- Decidir dónde una tubería debe dejar de ser perezosa y guardar una lista.
- Entender el diseño de la capa 10 del Observatorio y cómo probar generadores.

---

## 1. Perezoso frente a ansioso

Hasta ahora, el Observatorio es **ansioso** (*eager*): `read_lines` lee el archivo entero, `records_of` construye la lista de registros y `values_of` la de valores. Cada paso termina antes de que empiece el siguiente, y en cada momento todas las listas están en memoria.

Un generador es **perezoso** (*lazy*): no calcula nada hasta que alguien le pide un valor, y entonces calcula **solo ese**. Si encadenas generadores, cada valor atraviesa toda la tubería antes de que se lea el siguiente:

```python
values = (m.value for m in iter_measurements(iter_lines(path)) if m.value is not None)
for mean in running_mean(values):
    print(f"{mean:.1f}")
```

![Tubería perezosa: el for pide un valor a running_mean, que lo pide a la expresión de valores, que pide una medida a iter_measurements, que pide una línea a iter_lines, que la lee del archivo; el valor vuelve por la tubería y solo entonces se lee la línea siguiente](../0-assets/03-tuberia-perezosa.svg)

Lo que ganas:

- **Memoria constante**: con 10 líneas o con 10 millones, en cada momento hay una línea, una medida y una media.
- **Primer resultado inmediato**: la primera media sale en cuanto se lee la primera línea, sin esperar al final del archivo.
- **Entradas sin fin**: un sensor que manda lecturas sin parar, o una API que pagina (fase 3), se procesan igual que un archivo.

Lo que pierdes: no sabes cuántos datos hay (`len`), no puedes volver atrás y cada generador se recorre una vez.

---

## 2. `itertools` para tuberías

En la semana 6 usaste `pairwise` y `groupby`. Estas son las que más aparecen al trabajar con generadores:

| Función | Qué hace | Ejemplo |
|---|---|---|
| `islice(it, n)` | Los `n` primeros (o `islice(it, inicio, fin)`) | `islice(lecturas, 5)` |
| `count(inicio, paso)` | `inicio`, `inicio + paso`... sin fin | `count(1)`: 1, 2, 3, ... |
| `cycle(it)` | Repite los elementos sin fin | `cycle(["Norte", "Sur"])` |
| `repeat(x, n)` | `x` repetido `n` veces (sin `n`, sin fin) | `repeat(0.0, 3)` |
| `takewhile(pred, it)` | Mientras se cumpla `pred`; para en el primero que no | `takewhile(lambda v: v < 50, lecturas)` |
| `dropwhile(pred, it)` | Salta mientras se cumpla `pred`; da el resto | `dropwhile(es_cabecera, lineas)` |
| `chain(a, b, ...)` | Uno detrás de otro | `chain(lunes, martes)` |
| `batched(it, n)` | Tuplas de `n` (la última, más corta) | `batched(lecturas, 100)` para insertar por lotes |

Todas devuelven iteradores perezosos y aceptan iteradores perezosos: se encadenan sin construir listas.

```python
from itertools import count, islice

list(islice(running_mean(count(1)), 4))     # [1.0, 1.5, 2.0, 2.5]
```

`count(1)` no termina nunca, `running_mean` tampoco; `islice` pide cuatro valores y para. **Nunca** hagas `list()`, `sorted()`, `sum()` ni `max()` de algo infinito: no terminan y llenan la memoria.

---

## 3. Dónde se acaba la pereza

Hay operaciones que necesitan **todos** los datos a la vez: ordenar (`sorted`), la mediana (semana 6), contar por etiqueta (`Counter`), las medias por etiqueta o recorrer dos veces. Ahí la tubería se convierte en lista, y está bien:

```python
series = Series.from_lines(iter_lines(path))     # perezoso hasta aquí; la serie guarda la lista
print(median(series.values()))                   # la mediana necesita todos los valores
```

El informe de tu `main` es de este tipo: imprime las filas, luego las cuenta, luego busca la racha más larga, luego las medias... recorre los mismos datos muchas veces. Por eso `main` no cambia esta semana y sigue usando `source.lines()`, que devuelve una lista. Los generadores entran donde dan ventaja: al leer (`iter_lines`), al convertir (`iter_measurements`) y en los cálculos de una sola pasada (`running_mean`).

**Regla práctica**: perezoso en la entrada y en las transformaciones; una lista cuando el siguiente paso necesita recorrer más de una vez o necesita el total.

---

## 4. La capa 10 del Observatorio

| Pieza | Por qué así |
|---|---|
| `Measurement.__str__` | La medida se escribe en el mismo formato en que se lee: `from_line(str(m)) == m` |
| `Series.__len__`, `__iter__`, `__getitem__` | Una serie se usa como cualquier colección: `len`, `for`, `in`, `serie[0]`, `if serie:` |
| `__iter__` con `yield from` | Cada `for` crea un generador nuevo: la serie es un iterable, no un iterador |
| `Series.__add__` con `NotImplemented` | Juntar series es obvio; sumar con otra cosa da el `TypeError` normal |
| Sin `__contains__` | `in` funciona recorriendo con `__iter__` y el `__eq__` de la *dataclass* |
| Sin herencia de `Sequence` | Cuatro dunders bastan; `index` y `count` no significan nada para una serie |
| `streams.py` aparte | Los generadores dependen de `model`, nunca al revés: así no hay importaciones circulares |
| `iter_lines` con los errores de `read_lines` | Quien recorre recibe la misma `DataFileError`, solo que en el primer `next()` |

---

## 5. Probar generadores

Un generador se prueba como cualquier función, convirtiendo su salida en lista. Pero hay tres cosas que solo un test de generador comprueba:

```python
def test_iter_lines_fails_on_the_first_next_not_on_the_call(tmp_path: Path) -> None:
    lines = iter_lines(tmp_path / "no-existe.txt")         # no debe fallar aquí
    with pytest.raises(DataFileError, match="no existe el archivo"):
        next(lines)                                         # sino aquí


def test_iter_measurements_works_with_an_endless_input() -> None:
    endless = itertools.cycle(["Norte;12,5", "basura", "Sur;NA"])
    assert list(itertools.islice(iter_measurements(endless), 3)) == [NORTE, SUR, NORTE]


def test_a_generator_is_used_up_after_one_pass() -> None:
    means = running_mean([1.0, 3.0])
    assert list(means) == [1.0, 2.0]
    assert list(means) == []
```

1. **Cuándo falla**: crear el generador no debe fallar; el primer `next()`, sí.
2. **Que es perezoso de verdad**: una entrada infinita con `islice`. Una versión que construya una lista no termina, y el test se queda colgado en lugar de pasar.
3. **Que se gasta**: documenta para quien lea el test que el resultado se recorre una vez.

Y un test de tipo: `isinstance(iter_lines(ruta), Generator)` comprueba que la función es un generador y no una que devuelve `iter(lista)`.

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| El programa se queda colgado | `list`, `sorted`, `sum` o `max` sobre algo infinito | `islice` o `takewhile` antes |
| La tubería lee todo antes de dar el primer resultado | Una etapa usa una lista (`[...]` o `list(...)`) | Paréntesis en lugar de corchetes, o `yield` |
| Un cálculo sale vacío o a medias | Dos etapas recorren el mismo generador | Una lista donde haga falta recorrer dos veces |
| `ImportError: ... partially initialized module ... (most likely due to a circular import)` | Dos módulos se importan entre sí | Que la dependencia vaya en un solo sentido (`streams` importa `model`) |
| El test de la entrada infinita no termina | La función no es perezosa | Corta con `Ctrl+C`; reescríbela con `yield` |

---

## ✅ Qué debes saber al terminar

- [ ] Qué significa perezoso y ansioso, y qué gana y qué pierde cada uno.
- [ ] Cómo recorre un valor una tubería de generadores.
- [ ] Para qué sirven `islice`, `count`, `cycle`, `takewhile`, `chain` y `batched`.
- [ ] Dónde termina la pereza y por qué `main` sigue trabajando con listas.
- [ ] Las tres cosas que comprueba un test de generador.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [04 · Generadores](04-generadores.md) | **05 · Pipelines perezosos** | [Ejercicio 01 · Dunders](../2-practicas/ejercicio-01-dunders/README.md) |
