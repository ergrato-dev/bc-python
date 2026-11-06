# 02 · Parametrize y marcas

⏱️ 40 min

## 🎯 Objetivos

- Probar muchos casos con un solo test y `@pytest.mark.parametrize`.
- Dar nombres claros a los casos con `ids` y `pytest.param`.
- Marcar un fallo conocido con `xfail` y saltar tests con `skip` y `skipif`.
- Elegir qué tests ejecutar con `-k`, `-m`, `-x` y `--lf`.

---

## 1. Un test, muchos casos

`parse_value` tiene muchas entradas interesantes: coma, punto, espacios, `NA`, texto vacío. Un test por caso son cinco funciones casi iguales. Un bucle dentro de un solo test es peor: al primer fallo se para, y no sabes cuántos casos más fallan.

`parametrize` ejecuta el mismo test una vez por caso:

```python
@pytest.mark.parametrize(
    ("text", "expected"),
    [("12,5", 12.5), (" 8 ", 8.0), ("-3,25", -3.25), ("NA", None), ("", None)],
)
def test_parse_value_still_reads_good_values(text: str, expected: float | None) -> None:
    assert parse_value(text) == expected
```

El primer argumento son los nombres de los parámetros; el segundo, una lista con una tupla por caso. pytest los cuenta como **cinco tests**: cada uno pasa o falla por su cuenta y sale en el informe con su id:

```
tests/test_quality.py::test_parse_value_still_reads_good_values[12,5-12.5] PASSED
tests/test_quality.py::test_parse_value_still_reads_good_values[ 8 -8.0] PASSED
...
```

Con un solo parámetro basta su nombre y una lista de valores:

```python
@pytest.mark.parametrize("text", ["nan", "NaN", "inf", "-inf", "Infinity"])
def test_parse_value_rejects_non_finite_values(text: str) -> None:
    with pytest.raises(ValueError, match="valor no finito"):
        parse_value(text)
```

## 2. Nombres para los casos

pytest compone el id con los valores. Con textos cortos se lee bien; con un JSON entero, no. `ids` da un nombre a cada caso:

```python
@pytest.mark.parametrize(
    ("data", "error_type"),
    [
        ('{"label": "Norte", "value": NaN}', "finite_number"),
        ('{"label": "Norte", "value": "inf"}', "value_error"),
    ],
    ids=["json-nan", "text-inf"],
)
```

Y `pytest.param` da el id junto al caso, y le puede añadir marcas:

```python
@pytest.mark.parametrize(
    "text",
    [
        pytest.param("abc", id="letras"),
        pytest.param("nan", marks=pytest.mark.xfail(reason="float acepta nan")),
    ],
)
```

Con un buen id, `uv run pytest -k json-nan` ejecuta solo ese caso.

## 3. Varias listas: combinaciones

Dos `parametrize` en el mismo test multiplican: cada valor del primero con cada valor del segundo.

```python
@pytest.mark.parametrize("label", ["Norte", "Estación Sur"])
@pytest.mark.parametrize("text", ["12,5", "12.5"])
def test_any_label_with_any_decimal_mark(label: str, text: str) -> None:
    assert parse_record(f"{label};{text}") == (label, 12.5)
```

Son 2 × 2 = 4 tests. Úsalo con cuidado: tres listas de cinco son 125 tests.

## 4. Cuándo **no** parametrizar

`parametrize` es para el **mismo** comportamiento con distintos datos. Si cada caso necesita un `if` dentro del test, o un `assert` distinto, son tests distintos:

```python
# ❌ Un test que hace dos cosas según el caso
@pytest.mark.parametrize(("text", "ok"), [("12,5", True), ("abc", False)])
def test_parse(text: str, ok: bool) -> None:
    if ok:
        assert parse_value(text) == 12.5
    else:
        with pytest.raises(ValueError):
            parse_value(text)
```

Mejor dos tests, cada uno parametrizado: uno para los valores buenos y otro para los que se rechazan. Es lo que hace `test_quality.py`.

## 5. Marcas

Una **marca** es una etiqueta que cambia cómo pytest trata un test:

| Marca | Qué hace | Cuándo |
|---|---|---|
| `@pytest.mark.skip(reason="...")` | No lo ejecuta: `s` en el informe | Casi nunca: un test que no se ejecuta se olvida |
| `@pytest.mark.skipif(condición, reason="...")` | Lo salta si se cumple la condición | Un test que solo tiene sentido en un sistema: `sys.platform == "win32"` |
| `@pytest.mark.xfail(reason="...")` | Lo ejecuta y **espera** que falle: `x` si falla, `X` (`XPASS`) si pasa | Un bug conocido que aún no se ha arreglado |
| `@pytest.mark.xfail(strict=True)` | Como `xfail`, pero un `XPASS` cuenta como fallo | Para enterarte en cuanto alguien arregle el bug y quitar la marca |
| `@pytest.mark.parametrize` | También es una marca | Ya la conoces |

Un `xfail` no es un sitio para aparcar tests molestos: es un bug apuntado, con su `reason`. Si nadie va a arreglarlo, bórralo o arréglalo.

### Marcas propias

Puedes inventar marcas, como `@pytest.mark.slow` para los tests lentos, y ejecutar solo los rápidos con `uv run pytest -m "not slow"`. Regístralas en `pyproject.toml`, porque si no, pytest avisa y una errata (`@pytest.mark.slwo`) pasa desapercibida:

```toml
[tool.pytest.ini_options]
markers = ["slow: tests que tardan más de un segundo"]
addopts = ["--strict-markers"]
```

Con `--strict-markers`, una marca sin registrar es un error. Tu proyecto aún no necesita marcas propias.

## 6. Elegir qué ejecutar

| Opción | Qué hace |
|---|---|
| `-k texto` | Solo los tests cuyo nombre (o id) contiene `texto`. Admite `and`, `or` y `not`: `-k "parse and not json"` |
| `-m marca` | Solo los que tienen esa marca |
| `-x` | Para en el primer fallo |
| `--lf` | Solo los que fallaron la última vez (*last failed*) |
| `-v` | Un test por línea, con su id |
| `-q` | Lo mínimo: puntos y el resumen |
| `tests/test_quality.py::test_scale_fixture` | Un solo test, por su ruta |

Cuidado con `-k`: busca **subcadenas**. `-k top` también ejecuta `test_does_not_stop`. Para un nombre exacto, usa la ruta con `::`. Mientras arreglas un bug, `uv run pytest -x --lf` repite solo lo que falla y se para en el primero.

---

## ⚠️ Errores comunes

| Error | Causa | Solución |
|---|---|---|
| `In test_x: function uses no argument 'value'` | El nombre en `parametrize` no coincide con el parámetro | Usa el mismo nombre en los dos sitios |
| `in "parametrize" the number of names (2): ... must be equal to the number of values (3)` | Una tupla del caso tiene más o menos valores que nombres | Cuenta: `("text", "expected")` pide tuplas de dos |
| `PytestUnknownMarkWarning` | Una marca sin registrar, o con una errata | Corrígela o regístrala en `markers` |
| `XPASS(strict)` en rojo | El bug apuntado con `xfail(strict=True)` ya está arreglado | Quita la marca |
| `-k` ejecuta tests de más | Busca subcadenas | Afina el texto o usa la ruta con `::` |

---

## ✅ Qué debes saber al terminar

- [ ] Qué ventaja tiene `parametrize` sobre un bucle dentro del test.
- [ ] Cómo dar un nombre a un caso y añadirle una marca.
- [ ] Cuántos tests salen de dos `parametrize` apilados.
- [ ] Cuándo un caso merece su propio test en vez de un parámetro.
- [ ] Qué diferencia hay entre `skip` y `xfail`, y para qué sirve `strict=True`.
- [ ] Cómo repetir solo los tests que fallaron.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [01 · Fixtures y `conftest.py`](01-fixtures-y-conftest.md) | **02 · Parametrize y marcas** | [03 · Hypothesis](03-hypothesis.md) |
