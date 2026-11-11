# 05 · Notebooks en un proyecto

⏱️ 45 min

## 🎯 Objetivos

- Repartir el trabajo entre `core/etl.py`, el comando `extraer` y `notebooks/eda.ipynb`.
- Instalar JupyterLab sin que llegue a la imagen ni a la CI de tests.
- Servir JupyterLab desde Docker, solo para tu máquina y con token.
- Mantener los notebooks limpios en Git con un gancho.
- Probar que un notebook se ejecuta de arriba abajo, sin Jupyter, y conocer los límites de esa prueba.

---

## 1. Dónde vive cada pieza

| Pieza | Qué hace | Por qué ahí |
|---|---|---|
| `core/etl.py` | `extract`, `transform`, `write_snapshot` | Código con tests: tipos, orden, niveles y bytes exactos |
| `extraer SALIDA [--carga N]` | Abre la base, ejecuta el ETL y escribe la huella | La única pieza que conoce `OBSERVATORIO_DATABASE_URL` |
| `notebooks/instantanea.csv` | Los datos del análisis | En Git: pequeña, con su huella |
| `notebooks/eda.ipynb` | Preguntas, tablas, gráficos, hallazgos | La historia, sin lógica que haya que reutilizar |

Como `frames.py` y `inference.py`, `etl.py` importa pandas y **no** se reexporta en `core/__init__.py`: la CLI lo importa dentro de `extraer`, y el resto de comandos arranca sin cargar pandas.

```
$ uv run observatorio extraer notebooks/instantanea.csv --carga 1
instantanea.csv: 2000 medidas · cargas: 1
sha256: 3193779438eecdede9910a3cbc922f05a883e69a8a92fd4ef9a33e482d636c65
```

`extraer` sale con código 1 si la carga no existe o no hay medidas (no escribe nada), y con código 2 si no puede escribir el archivo. Tarda unos 0,8 s, casi todo en importar pandas.

## 2. Un grupo para JupyterLab

JupyterLab no es parte del Observatorio: nadie lo necesita para ejecutar la CLI, la API o los tests. Por eso va en un **grupo de dependencias** propio:

```toml
[dependency-groups]
dev = [...]
notebook = [
    "jupyterlab==4.6.4",
]
```

`uv sync` instala el proyecto y el grupo `dev`, que es el grupo por defecto. `notebook` solo se instala cuando lo pides:

```bash
uv run --group notebook jupyter lab
```

La diferencia es grande. JupyterLab trae **78 paquetes** (el servidor, el kernel IPython, `nbconvert`, `tornado`, `pyzmq`...) y unos 380 MB en la imagen. Si fuera una dependencia del proyecto, la imagen `runtime` que sirve la API los llevaría todos, con cada aviso de seguridad que les salga. Si fuera de `dev`, cada ejecución de la CI los instalaría para nada.

Todos van fijados en `uv.lock`, con el resto: `uv lock --check` y `uv audit` de la CI también los revisan.

## 3. JupyterLab en Docker

El `Dockerfile` gana una etapa, `notebook`, entre `test` y `runtime`:

```dockerfile
FROM builder AS notebook

ENV PATH="/opt/venv/bin:$PATH"

RUN uv sync --locked --no-dev --no-editable --group notebook

RUN useradd --create-home --uid 1000 analyst
USER 1000:1000
WORKDIR /app/notebooks

EXPOSE 8888

CMD ["jupyter", "lab", "--ip", "0.0.0.0", "--port", "8888", "--no-browser"]
```

Parte de `builder`: el mismo Python y los mismos paquetes que la imagen que despliegas, más JupyterLab. `runtime` sigue siendo la última etapa (la de `docker build .`) y no sabe nada de Jupyter.

En `compose.yaml`, un servicio con **perfil**:

```yaml
  notebook:
    build:
      context: .
      target: notebook
    image: local/observatorio:week-29-notebook
    profiles:
      - notebook
    volumes:
      - ./notebooks:/app/notebooks
    ports:
      - "127.0.0.1:8888:8888"
```

- `profiles`: `docker compose up` no lo arranca; hace falta `docker compose --profile notebook up -d notebook`.
- `volumes`: tu carpeta `notebooks/` dentro del contenedor. Lo que guardas en JupyterLab aparece en tu repositorio, listo para `git add`.
- `127.0.0.1`: el puerto solo se abre a tu máquina, como el de PostgreSQL (semana 21).

**El usuario 1000.** Un volumen comparte la carpeta con sus permisos de tu máquina. Tu usuario de Linux o de WSL es casi siempre el 1000 (`id -u`); si el contenedor usara otro número, como el 10001 de `runtime`, JupyterLab no podría guardar nada en `notebooks/`. Si tu `id -u` no es 1000, cambia el número en las dos líneas del `Dockerfile`.

**El token.** Con `--ip 0.0.0.0`, JupyterLab escucha en todas las interfaces del contenedor. Sin token, cualquiera que llegue al puerto ejecuta código en tu máquina. Por eso la etapa **no** lo desactiva: JupyterLab inventa uno al arrancar y lo escribe en el registro:

```bash
docker compose logs notebook | grep 127.0.0.1
```

```
notebook-1  |         http://127.0.0.1:8888/lab?token=c2c8dead1c442d0dfdbee66100b1cbdcdce9e08870ab620e
```

Sin el token, la API de JupyterLab contesta `403`. Un test comprueba que nadie lo ha desactivado.

La imagen `week-29-notebook` mide unos 2,5 GB: todo lo de `builder` más JupyterLab. Solo vive en tu máquina.

## 4. Un gancho que limpia

Un gancho de pre-commit nuevo, con la misma idea que los de la semana 21 (las herramientas de tu `uv.lock`):

```yaml
      - id: notebook-outputs
        name: notebooks sin salidas
        entry: >-
          uv run --locked --group notebook jupyter nbconvert --clear-output --inplace
          --ClearMetadataPreprocessor.enabled=True
          --ClearMetadataPreprocessor.preserve_nb_metadata_mask=kernelspec
        language: unsupported
        files: \.ipynb$
```

`nbconvert`, que llega con JupyterLab, reescribe cada notebook del commit:

- `--clear-output`: sin salidas y con los contadores a `null`;
- `ClearMetadataPreprocessor`: sin los metadatos de cada celda, donde Jupyter guarda la hora a la que se ejecutó;
- `preserve_nb_metadata_mask=kernelspec`: conserva el kernel del notebook, para que JupyterLab sepa con cuál abrirlo.

Si el gancho cambia algo, el commit se para (`files were modified by this hook`): vuelve a añadir el notebook y repite. No hace falta un paquete más (como `nbstripout`): todo lo que necesita ya está en el grupo `notebook`.

## 5. Probar un notebook sin Jupyter

`tests/test_notebook.py` lee `eda.ipynb` como lo que es, un JSON, y comprueba:

| Test | Qué comprueba |
|---|---|
| Sin salidas, contadores ni horas | Que el gancho pasó |
| El botón de Colab | La primera celda enlaza a `colab.research.google.com/github/.../notebooks/eda.ipynb` |
| La celda de Colab | Instala versiones fijadas, y son las de tu `pyproject.toml` |
| Python normal | Ni `%`, ni `!`, ni `display(` |
| La huella | Compara `hashlib.sha256` de `instantanea.csv` con un `EXPECTED` de 64 caracteres |
| Las conclusiones | Una celda de Markdown con `## Conclusiones` |
| **De arriba abajo** | Ejecuta cada celda de código, en orden, en un espacio de nombres vacío |

El último es el importante:

```python
monkeypatch.chdir(FOLDER)
namespace: dict[str, Any] = {"__name__": "__main__"}
for index, cell in enumerate(cells("code")):
    exec(compile(source(cell), f"celda {index}", "exec"), namespace)
```

`exec` ejecuta texto como código de Python, con `namespace` como variables globales: lo mismo que hace el kernel de Jupyter, sin el kernel. Si una celda usa algo de una celda borrada o posterior, falla con su número (`File "celda 4"`). En la carpeta del notebook, como JupyterLab, para que funcionen las rutas relativas. `exec` con texto que no controlas es peligroso; aquí es tu propio notebook, el mismo código que ejecutas en JupyterLab.

Tarda unos 0,7 s, frente a los 3,8 s de `jupyter execute` con un kernel de verdad, y no necesita JupyterLab: corre con el resto de tests en tu máquina, en `docker compose run --rm app` y en la CI.

**Sus límites.** No es un kernel de IPython: no entiende magias (por eso el notebook no las usa), no muestra salidas y no prueba que JupyterLab abra el archivo. Comprueba lo que más se rompe, que el notebook funcione de arriba abajo con sus datos; lo demás lo ves al abrirlo.

## 6. Colab

La primera celda de Markdown lleva el botón:

```markdown
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/<usuario>/python-<nombre>-<apellido>/blob/main/notebooks/eda.ipynb)
```

Colab abre el notebook directamente desde GitHub (si tu repositorio es privado, te pide permiso para leerlo). La instantánea no viaja con él: súbela con el panel de archivos de Colab y la huella comprueba que es la buena. Solo datos sintéticos o anonimizados (`docs/setup.md`). Lo que cambies en Colab no vuelve a tu repositorio: descárgalo, pásalo por el gancho y haz commit desde tu máquina.

## 7. Lo que cuesta

| Pieza | Coste |
|---|---|
| `core/etl.py` y `extraer` | Nada nuevo: pandas y SQLAlchemy ya estaban |
| Grupo `notebook` | 78 paquetes; solo si lo pides |
| Imagen `runtime` | Sin cambios: 1,18 GB, como la semana 28 |
| Imagen `notebook` | Unos 2,5 GB, solo en tu máquina |
| Tests | 1 s más, sin JupyterLab |

## 8. Errores frecuentes

| Error | Consecuencia | Mejor |
|---|---|---|
| `jupyterlab` en las dependencias del proyecto | 78 paquetes en la imagen que despliegas | Un grupo propio |
| JupyterLab con `--IdentityProvider.token=''` | Cualquiera que llegue al puerto ejecuta código | El token al azar, del registro |
| El puerto sin `127.0.0.1:` | JupyterLab abierto a tu red | `127.0.0.1:8888:8888` |
| El contenedor con otro UID | `Permission denied` al guardar en `notebooks/` | El UID de `id -u` |
| Commit sin el gancho | Salidas y horas en cada diff | `uv run pre-commit install` (semana 21) |
| Lógica en el notebook | Código sin tests | `core/etl.py` |

## ✅ Qué debes saber al terminar

- Qué hace cada pieza: `etl.py`, `extraer`, la instantánea y el notebook.
- Por qué JupyterLab va en un grupo propio y en una etapa propia del `Dockerfile`.
- Cómo arrancas JupyterLab en Docker, de dónde sale el token y por qué el UID 1000.
- Qué limpia el gancho y por qué.
- Qué comprueba el test que ejecuta el notebook, y qué no.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [04 · ETL desde PostgreSQL](04-etl-desde-postgresql.md) | **05 · Notebooks en un proyecto** | [Ejercicio 01 · EDA con pandas](../2-practicas/ejercicio-01-eda-con-pandas/README.md) |
