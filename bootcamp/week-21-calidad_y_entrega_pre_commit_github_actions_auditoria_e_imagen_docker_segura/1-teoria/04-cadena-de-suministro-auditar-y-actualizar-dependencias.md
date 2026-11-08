# 04 · La cadena de suministro: auditar y actualizar dependencias

⏱️ 45 min

## 🎯 Objetivos

- Explicar qué es la cadena de suministro de tu programa y por qué sus fallos son tuyos.
- Leer un aviso de seguridad: CVE, GHSA y PYSEC, versión afectada y versión que lo arregla.
- Auditar el proyecto con `uv audit`, en tu máquina y en la CI.
- Actualizar una dependencia directa y una transitiva, una cada vez.
- Decidir cuándo se ignora un aviso, y dejarlo escrito.
- Configurar Dependabot para que las versiones fijadas no se queden viejas.

---

## 1. Tu cadena de suministro

Tu Observatorio tiene unas 1800 líneas de código. Lo que ejecuta es mucho más: en `uv.lock` hay 60 paquetes (FastAPI trae Starlette, SQLAlchemy trae typing-extensions, httpx trae certifi...), y por debajo, Python, Debian y las acciones de GitHub. Todo eso es tu **cadena de suministro**: el código de otros del que depende el tuyo. Si un eslabón tiene un fallo, tu programa lo tiene.

```bash
uv tree --depth 1
uv tree --invert --package certifi
```

Las dependencias que no pides tú, pero que pide algo que pediste, son **transitivas**. No están en tu `pyproject.toml`, pero sí en `uv.lock`, y se ejecutan igual.

---

## 2. Fijar, y el precio de fijar

Desde la semana 08, todo va fijado: `pydantic==2.14.2` en `pyproject.toml`, y cada paquete, con su versión y el **hash** de cada archivo, en `uv.lock`. Fijar da:

- **reproducibilidad**: hoy, mañana y en la CI se instala exactamente lo mismo;
- **integridad**: si alguien cambia el archivo de un paquete en PyPI, el hash no coincide y uv no lo instala.

El precio: una versión fijada **no se arregla sola**. Si mañana se descubre un fallo en `urllib3 2.7.0`, tu `uv.lock` seguirá instalando `2.7.0` hasta que alguien lo cambie. Fijar obliga a dos cosas más: **auditar** (saber cuándo una versión tiene fallos) y **actualizar** (cambiarla, con cuidado).

---

## 3. Leer un aviso

Una **vulnerabilidad** es un fallo que alguien puede aprovechar: leer lo que no debe, colgar tu programa, ejecutar su código. Cuando se descubre una, se publica un **aviso** (*advisory*) con un identificador:

| Identificador | Quién lo da | Ejemplo |
|---|---|---|
| **CVE** | El catálogo general, para cualquier software | `CVE-2024-56201` |
| **GHSA** | La base de datos de avisos de GitHub | `GHSA-cpwx-vrp4-4pq7` |
| **PYSEC** | La base de datos de avisos de Python (PyPA) | `PYSEC-2026-1472` |

Un mismo fallo suele tener los tres (*aliases*). **OSV** (Open Source Vulnerabilities) es la base de datos que los junta todos, con el formato que entienden las herramientas.

Lo que importa de un aviso:

- **qué versiones afecta** y cuál lo **arregla** (*Fixed in*);
- **en qué condiciones**: "sandbox breakout" en Jinja solo importa si ejecutas plantillas escritas por otros; un fallo en un servidor HTTP no importa si solo usas el cliente;
- **la gravedad**: CRITICAL, HIGH, MEDIUM, LOW, según lo fácil y dañino que sea aprovecharlo.

La regla práctica: si hay una versión que lo arregla, **actualiza**, aunque creas que no te afecta. Es más barato que estar seguro de que no te afecta.

---

## 4. `uv audit`

```bash
uv audit
```

```
warning: `uv audit` is experimental and may change without warning. Pass `--preview-features audit-command` to disable this warning.
...
Found no known vulnerabilities and no adverse project statuses in 61 packages
```

`uv audit` lee `uv.lock` y pregunta a OSV por cada paquete y versión. No instala nada ni necesita el entorno. Con avisos, los lista y **termina con código 1**:

```
jinja2 3.1.4 has 3 known vulnerabilities:

- PYSEC-2026-1472: Jinja has a sandbox breakout through malicious filenames

  Fixed in: 3.1.5

  Advisory information: https://nvd.nist.gov/vuln/detail/CVE-2024-56201
```

Opciones útiles:

| Opción | Qué hace |
|---|---|
| `--preview-features audit-command` | Quita el aviso de "experimental" (en la CI) |
| `--no-dev` | Solo las dependencias del programa, sin las de desarrollo |
| `--output-format json` | El informe para otro programa (también `sarif`) |
| `--ignore ID` | No cuenta ese aviso (sección 6) |
| `--ignore-until-fixed ID` | No lo cuenta **mientras no haya arreglo** |

`no adverse project statuses`: además de avisos, uv mira si algún paquete está marcado por su autor como **archivado**, **obsoleto** o en **cuarentena**. Un paquete archivado no tendrá más arreglos.

`uv audit` es **experimental** en uv 0.13: su salida puede cambiar en otra versión. Por eso tu uv está fijado, también en la CI.

¿Por qué en la CI y no una vez? Porque la base de datos **crece**: lo que hoy pasa limpio puede tener un aviso la semana que viene, sin que cambies nada. Tu CI lo audita en cada *push*. Un proyecto que se toca poco puede añadir un evento `schedule` para auditarlo cada semana (teoría 03).

---

## 5. Actualizar, una cosa cada vez

Qué hay más nuevo:

```bash
uv tree --outdated
```

```
└── requests v2.32.3 (latest: v2.34.2)
    ...
    └── urllib3 v2.2.3 (latest: v2.8.0)
```

| Qué | Cómo |
|---|---|
| Una **directa** | `uv add paquete==X.Y.Z` (cambia `pyproject.toml` y `uv.lock`) |
| Una **transitiva** | `uv lock --upgrade-package paquete` (solo `uv.lock`) |
| Todo, dentro de los rangos | `uv lock --upgrade` |

`uv lock` a secas **no actualiza**: si una versión de `uv.lock` sigue siendo válida, la deja. Así, añadir una dependencia no te cambia las demás por sorpresa. Para subir algo, hay que pedirlo.

Y antes de fijar una versión nueva, lo de siempre (`docs/stack-versions.md`): ¿cuándo salió?, ¿tiene avisos?, ¿qué cambia? Una versión de hace dos días puede venir con un fallo nuevo, o ser un paquete comprometido que aún nadie ha detectado. Una semana de espera filtra la mayoría.

Una actualización por *pull request*: si algo se rompe, sabes qué fue, y se deshace con un *revert*.

---

## 6. Ignorar, sabiendo lo que haces

A veces un aviso no tiene arreglo todavía, o no te afecta y actualizar rompe algo. Puedes ignorarlo:

```bash
uv audit --ignore PYSEC-2026-2275
```

Ignorar es una **decisión**, y se deja escrita donde la vea quien venga detrás: en la orden de la CI, con un comentario que diga qué es, por qué no te afecta y cuándo revisarlo. Mejor aún, `--ignore-until-fixed`: ignora el aviso solo hasta que salga un arreglo; ese día, la CI vuelve a fallar y te obliga a actualizar.

---

## 7. Dependabot: que alguien mire por ti

Con todo fijado, nadie actualiza si no lo pide alguien. **Dependabot**, de GitHub, lo pide por ti: revisa tus versiones y abre un *pull request* por cada actualización. La CI lo prueba, y tú decides si lo fusionas.

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: uv
    directory: /
    schedule:
      interval: weekly
    cooldown:
      default-days: 7
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
    cooldown:
      default-days: 7
  - package-ecosystem: docker
    directory: /
    schedule:
      interval: weekly
    cooldown:
      default-days: 7
    ignore:
      - dependency-name: python
        update-types:
          - version-update:semver-major
          - version-update:semver-minor
```

- **`uv`**: lee `pyproject.toml` y `uv.lock`, y actualiza los dos;
- **`github-actions`**: las acciones de tus workflows, con su SHA y su comentario;
- **`docker`**: las imágenes del `Dockerfile`, con su etiqueta y su digest;
- **`cooldown`**: no propone versiones con menos de 7 días, la misma regla que sigues tú.

Un caso real, el primer día de Dependabot en el Observatorio:

```
chore(deps): bump astral-sh/setup-uv from 10.3.2 to 10.3.3
chore(deps-dev): bump hypothesis from 6.170.8 to 6.170.14
chore(deps): bump pydantic-settings from 2.16.1 to 2.16.2
chore(deps-dev): bump types-pyyaml from 6.0.12.20260906 to 6.0.12.20261030
chore(deps): bump python from 3.14.10-slim-trixie to 3.15.0-slim-trixie
```

El último es un error: tu `pyproject.toml` dice `requires-python = ">=3.14,<3.15"`, pero Dependabot no lo lee en el `Dockerfile`. Por eso el `ignore`: para la imagen de Python, solo parches (`3.14.x`). El salto a 3.15 lo decides tú, cambiando `.python-version`, `requires-python` y el `Dockerfile` en el mismo *pull request*. Al añadir el `ignore`, Dependabot cerró solo el suyo.

Fíjate también en lo que **no** propuso: `types-pyyaml 6.0.12.20261103`, de 5 días. Es el `cooldown`.

---

## ⚠️ Errores comunes

| Error | Por qué está mal | Qué hacer |
|---|---|---|
| Auditar una vez y olvidarlo | Salen avisos nuevos para versiones viejas | `uv audit` en la CI |
| Mirar solo `pyproject.toml` | La mayoría de los paquetes son transitivos | `uv audit` lee `uv.lock` entero |
| `uv lock --upgrade` y un *pull request* con cuarenta cambios | Si algo se rompe, no sabes qué | Una actualización cada vez |
| Fijar la versión publicada ayer | Puede traer un fallo nuevo, o estar comprometida | Una semana de espera, y `cooldown` en Dependabot |
| `--ignore` sin explicación | Nadie sabrá por qué, ni cuándo quitarlo | Comentario con motivo y fecha, o `--ignore-until-fixed` |
| Fusionar a ciegas los *pull requests* de Dependabot | Un salto de versión puede cambiar el comportamiento | La CI en verde, y leer qué cambia |

---

## ✅ Qué debes saber al terminar

- [ ] Qué es tu cadena de suministro y qué son las dependencias transitivas.
- [ ] Qué da fijar versiones y qué obliga a hacer.
- [ ] Qué son CVE, GHSA, PYSEC y OSV, y qué leer de un aviso.
- [ ] `uv audit`, sus opciones, y por qué va en la CI.
- [ ] Cómo actualizar una directa, una transitiva o todo, y por qué una cada vez.
- [ ] Qué hace Dependabot, para qué sirven `cooldown` e `ignore`, y por qué no propuso Python 3.15.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [03 · Integración continua con GitHub Actions](03-integracion-continua-con-github-actions.md) | **04 · La cadena de suministro: auditar y actualizar dependencias** | [05 · Una imagen Docker segura](05-una-imagen-docker-segura.md) |
