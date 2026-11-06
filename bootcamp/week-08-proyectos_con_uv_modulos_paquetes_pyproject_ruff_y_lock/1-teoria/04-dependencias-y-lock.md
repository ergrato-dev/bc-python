# 04 · Dependencias y lock

⏱️ 45 min

## 🎯 Objetivos

- Añadir, quitar y actualizar dependencias con `uv add`, `uv remove` y `uv lock --upgrade-package`.
- Leer los especificadores de versión (`==`, `>=`, `<`, `~=`) y elegir entre un rango y una versión fijada.
- Explicar qué guarda `uv.lock`, por qué se sube a Git y qué hacen `uv sync --locked` y `uv lock --check`.
- Distinguir dependencias directas y transitivas con `uv tree`.
- Elegir entre `uv add`, `uv run --with` y `uvx`.

---

## 1. Por qué fijar versiones

Tu Observatorio usa pytest 9.2.0. Si en `pyproject.toml` pusieras solo `"pytest"`, sin versión, cada máquina instalaría la última que hubiera ese día: tú la 9.2.0, una compañera el mes que viene la 9.3.0, y el CI dentro de un año la 10.0, que quizá cambie algo. El mismo código daría resultados distintos según **cuándo** se instaló. Fijar versiones hace que el proyecto se comporte igual en todas partes y en cualquier momento: es **reproducible**.

## 2. Especificadores de versión

| Especificador | Admite | Ejemplo |
|---|---|---|
| `==9.2.0` | Exactamente esa | `pytest==9.2.0` |
| `>=0.17` | Esa o cualquier posterior | Incluye una futura 1.0 que rompa cosas |
| `>=0.17,<0.18` | Un rango: la serie 0.17 | 0.17.3, 0.17.4... |
| `~=0.17.3` | Compatible: `>=0.17.3,<0.18` | Admite parches, no la siguiente menor |
| `!=0.17.2` | Todas menos esa | Para saltar una versión con un bug conocido |

Una biblioteca que otros instalan declara **rangos** amplios, para no chocar con lo que pidan los demás paquetes. Una aplicación, o un curso donde el README tiene que coincidir con lo que instalas, fija con `==`. El bootcamp fija siempre, y antes de fijar una versión comprueba que no tiene vulnerabilidades conocidas (`docs/stack-versions.md`).

## 3. `uv add`, `uv remove` y `uv tree`

```bash
uv add httpx==0.28.1              # dependencia del programa: va a [project] dependencies
uv add --dev ruff==0.17.3         # de desarrollo: va al grupo dev de [dependency-groups]
uv remove --dev ruff              # la quita de pyproject.toml, de uv.lock y de .venv
uv tree                           # el árbol de dependencias
```

`uv add` hace tres cosas de una vez: escribe la dependencia en `pyproject.toml`, **resuelve** (calcula una versión de cada paquete que sea compatible con todo lo demás) y apunta el resultado en `uv.lock`, y sincroniza `.venv`. Nunca edites `uv.lock` a mano.

Tú pides las dependencias **directas**; ellas traen las suyas, las **transitivas**. Al añadir mypy, el lock gana mypy y cinco paquetes más:

```
observatorio v0.8.0
├── mypy v2.4.1 (group: dev)
│   ├── ast-serialize v0.13.1
│   ├── librt v0.16.0
│   ├── mypy-extensions v1.2.0
│   ├── pathspec v1.1.1
│   └── typing-extensions v4.16.0
├── pytest v9.2.0 (group: dev)
...
```

Las transitivas también se fijan en el lock: no las controlas en `pyproject.toml`, pero una versión nueva de cualquiera de ellas podría romper tu proyecto igual que una directa.

## 4. `uv.lock`

`pyproject.toml` dice lo que **admites**; `uv.lock` dice lo que **usas**: la versión exacta de cada paquete, directo o transitivo, de dónde se descarga y el *hash* de cada archivo.

```toml
[[package]]
name = "pluggy"
version = "1.7.0"
source = { registry = "https://pypi.org/simple" }
wheels = [
    { url = "https://files.pythonhosted.org/.../pluggy-1.7.0-py3-none-any.whl", hash = "sha256:...", ... },
]
```

El *hash* es la huella del archivo: si alguien cambiara el *wheel* de pluggy 1.7.0 en el servidor, el *hash* no coincidiría y uv se negaría a instalarlo. El lock es además **universal**: un solo archivo con lo necesario para Linux, macOS y Windows. Por eso aparece `colorama`, que pytest solo usa en Windows, aunque en tu máquina no se instale.

![El flujo de las dependencias: pyproject.toml con lo que admites, uv lock resuelve y escribe uv.lock con versiones exactas y hashes, uv sync instala exactamente eso en .venv; uv add cambia los dos archivos a la vez y uv lock --check comprueba que siguen de acuerdo](../0-assets/03-de-pyproject-al-entorno.svg)

**`uv.lock` se sube a Git**, siempre junto a `pyproject.toml`: son una pareja. Quien clona tu repositorio ejecuta `uv sync` y obtiene **exactamente** tu entorno.

## 5. Cuando `pyproject.toml` y el lock no están de acuerdo

Si alguien edita `pyproject.toml` a mano y no ejecuta `uv lock`, los dos archivos se desincronizan. Tres comandos según lo que quieras:

| Comando | Si están desincronizados | Úsalo en |
|---|---|---|
| `uv sync` | Actualiza el lock y después instala | Tu máquina, mientras desarrollas |
| `uv sync --locked` | Falla con un error | Docker y CI: nunca construir con algo distinto de lo probado |
| `uv lock --check` | Falla, sin instalar nada | Una comprobación rápida, por ejemplo antes de un commit |

```
error: The lockfile at `uv.lock` needs to be updated, but `--locked` was provided.

hint: To update the lockfile, run `uv lock`.
```

Tu `Dockerfile` usa `uv sync --locked` desde la semana 1: si el lock no coincide, la imagen no se construye.

## 6. Actualizar

Las versiones fijadas no se actualizan solas. Para ver qué hay nuevo y subir una:

```bash
uv tree --outdated --depth 1                # marca las que tienen versión nueva
uv add --dev ruff==0.17.4                   # una fijada con ==: cambias el número
uv lock --upgrade-package pluggy            # una transitiva: la más nueva que admita el rango
uv lock --upgrade                           # todas: con cuidado, y con los tests después
```

```
└── ruff v0.17.3 (group: dev) (latest: v0.17.4)
```

Actualiza de una en una, ejecuta los tests después de cada una y haz un commit por actualización: si algo se rompe, sabes qué fue.

## 7. `uv add`, `uv run --with` o `uvx`

| Comando | Qué hace | Cuándo |
|---|---|---|
| `uv add --dev mypy==2.4.1` | La herramienta pasa a ser parte del proyecto, fijada en el lock | Lo que usa todo el equipo, siempre: pytest, ruff, mypy |
| `uv run --with mypy==2.4.1 mypy src` | La añade solo para ese comando, en un entorno temporal | Probar algo una vez, sin tocar `pyproject.toml` |
| `uvx ruff@0.17.3 check` | Ejecuta una herramienta en su propio entorno, fuera de cualquier proyecto | Herramientas que no dependen de tu código, o fuera de un proyecto |

Hasta la semana 7, mypy llegaba con `--with`: cada uno tenía que acordarse de la versión. Desde esta semana está en el grupo `dev`, y `uv run mypy` usa la del lock.

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| `The lockfile at uv.lock needs to be updated, but --locked was provided` | `pyproject.toml` cambió sin `uv lock` | `uv lock` y commit de los dos archivos |
| `No solution found when resolving dependencies` | Dos paquetes piden versiones incompatibles de un tercero, o la versión no existe para tu Python | Lee el mensaje: dice quién pide qué. Relaja un rango o cambia una versión |
| En otra máquina se instalan versiones distintas | No subiste `uv.lock` | Súbelo siempre |
| Conflictos de Git en `uv.lock` | Dos ramas añadieron dependencias | Quédate con un `pyproject.toml` correcto y ejecuta `uv lock`: no lo arregles a mano |
| Instalaste un paquete con pip dentro del proyecto | El paquete queda en `.venv` pero no en `pyproject.toml` ni en el lock | `uv add`, siempre |

---

## ✅ Qué debes saber al terminar

- [ ] Por qué un proyecto sin versiones fijadas no es reproducible.
- [ ] Qué admite cada especificador: `==`, `>=`, `<`, `~=` y `!=`.
- [ ] Las tres cosas que hace `uv add`, y la diferencia entre una dependencia directa y una transitiva.
- [ ] Qué guarda `uv.lock`, por qué es universal y por qué se sube a Git.
- [ ] La diferencia entre `uv sync`, `uv sync --locked` y `uv lock --check`.
- [ ] Cómo actualizar una dependencia de forma segura.
- [ ] Cuándo usar `uv add --dev`, `uv run --with` y `uvx`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [03 · `pyproject.toml`](03-pyproject-toml.md) | **04 · Dependencias y lock** | [05 · ruff](05-ruff.md) |
