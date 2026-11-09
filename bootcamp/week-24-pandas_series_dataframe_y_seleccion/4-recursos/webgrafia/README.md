# Webgrafía — Semana 24

Todo en inglés, de la documentación oficial de pandas salvo donde se indica. Comprueba arriba de cada página que es la de la versión 3.

| Recurso | Para qué |
|---|---|
| [10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html) | El recorrido oficial por todo pandas en una página. Léelo después de la teoría 01: verás que ya conoces la mitad |
| [Intro to data structures](https://pandas.pydata.org/docs/user_guide/dsintro.html) | `Series` y `DataFrame` en detalle: cómo se crean, alineación por índice y operaciones. Amplía las teorías 01 y 02 |
| [Getting started tutorials](https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html) | Diez tutoriales cortos con dibujos: leer y escribir, elegir columnas y filas, crear columnas nuevas. Buen repaso antes del ejercicio 03 |
| [Essential basic functionality](https://pandas.pydata.org/docs/user_guide/basics.html) | `head`, `describe`, `sort_values`, `value_counts`, los `dtypes` y cómo se convierten |
| [Indexing and selecting data](https://pandas.pydata.org/docs/user_guide/indexing.html) | Todo sobre `.loc`, `.iloc`, máscaras, `isin`, `where` y `query`. La referencia de la teoría 03 |
| [Working with missing data](https://pandas.pydata.org/docs/user_guide/missing_data.html) | NaN, `pd.NA`, `isna`, `fillna`, `dropna` y los tipos que admiten datos que faltan, como `Int64` |
| [IO tools: CSV](https://pandas.pydata.org/docs/user_guide/io.html) | Todos los parámetros de `read_csv` y `to_csv`, con ejemplos. Busca `na_values` y `keep_default_na` |
| [`pandas.read_csv`](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html) | La lista completa de textos que `read_csv` trata como dato que falta, en la descripción de `na_values` |
| [`pandas.cut`](https://pandas.pydata.org/docs/reference/api/pandas.cut.html) | `bins`, `labels` y `right`, con ejemplos de los bordes |
| [Copy-on-Write](https://pandas.pydata.org/docs/user_guide/copy_on_write.html) | Por qué una selección se comporta como una copia, y cómo se migra código antiguo. La teoría 04, sección 4, en profundidad |
| [Migration guide for the new string data type](https://pandas.pydata.org/docs/user_guide/migration-3-strings.html) | El tipo `str` de pandas 3: qué cambia frente a `object` y qué código antiguo puede romperse |
| [What's new in 3.0.0](https://pandas.pydata.org/docs/whatsnew/v3.0.0.html) | Todos los cambios de pandas 3. Para cuando un tutorial antiguo no te funcione |
| [Testing](https://pandas.pydata.org/docs/reference/testing.html) | `assert_frame_equal`, `assert_series_equal` y sus opciones `check_*` |
| [pandas-stubs](https://github.com/pandas-dev/pandas-stubs) (GitHub) | El repositorio de los tipos de pandas para mypy: cómo se numeran las versiones y qué no cubren |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Proyecto](../../3-proyecto/README.md) | **Webgrafía** | [Ebooks gratuitos](../ebooks-free/README.md) |
