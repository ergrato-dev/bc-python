# Cinco etapas: `uv` y `builder` preparan, `test` ejecuta los tests, `notebook` sirve
# JupyterLab y `runtime` es la imagen que se despliega. Cada imagen base, fijada por su
# digest (sha256): la etiqueta dice qué versión es, el digest garantiza que es
# exactamente esa imagen.

# Etapa 1: de esta imagen solo se toma el binario de uv.
FROM ghcr.io/astral-sh/uv:0.13.7@sha256:96f40d3904aad8d0bd010539001d36c8e2188b981e1334471a90c4a1d93bb490 AS uv

# Etapa 2: instala tu programa y sus dependencias, sin las de desarrollo, en /opt/venv.
FROM python:3.14.10-slim-trixie@sha256:9aaa474097d094040649f2162a627c0049b408f52138d980916788d80f04802f AS builder

COPY --from=uv /uv /bin/

# UV_PYTHON_DOWNLOADS=never: usar el Python de la imagen, nunca descargar otro.
# UV_PROJECT_ENVIRONMENT: el entorno vive en /opt/venv, que es lo que copia `runtime`.
# UV_COMPILE_BYTECODE=1: compila a .pyc al instalar; en `runtime` nadie podrá escribirlos.
# UV_LINK_MODE=copy: archivos copiados, no enlaces a la caché de uv, que no se copia.
ENV UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Primero solo las dependencias: esta capa se reutiliza mientras no cambie uv.lock.
COPY pyproject.toml uv.lock .python-version README.md ./
RUN uv sync --locked --no-dev --no-install-project

# Después tu paquete. --no-editable lo copia dentro de /opt/venv: el entorno ya no
# necesita la carpeta src.
COPY src ./src
RUN uv sync --locked --no-dev --no-editable

# Etapa 3: los tests, con las dependencias de desarrollo. `docker compose run app`.
FROM builder AS test

# PATH: python, pytest y observatorio se usan sin `uv run`.
# PYTEST_ADDOPTS y HYPOTHESIS_STORAGE_DIRECTORY: nada se escribe en /app.
ENV PATH="/opt/venv/bin:$PATH" \
    PYTEST_ADDOPTS="-p no:cacheprovider" \
    HYPOTHESIS_STORAGE_DIRECTORY=/tmp/hypothesis

COPY . .
RUN uv sync --locked

RUN useradd --create-home --uid 10001 app
USER 10001:10001

CMD ["pytest"]

# Etapa 4: JupyterLab, para explorar con los mismos paquetes y versiones que el proyecto.
# Solo con `docker compose --profile notebook up notebook`: nunca va a producción.
FROM builder AS notebook

ENV PATH="/opt/venv/bin:$PATH"

# --group notebook: JupyterLab y sus dependencias, encima de las del proyecto.
RUN uv sync --locked --no-dev --no-editable --group notebook

# UID 1000, el de tu usuario en casi cualquier Linux o WSL: los notebooks se guardan en tu
# carpeta notebooks/ (un volumen), y con otro UID no podría escribir en ella.
RUN useradd --create-home --uid 1000 analyst
USER 1000:1000
WORKDIR /app/notebooks

EXPOSE 8888

# 0.0.0.0 dentro del contenedor; compose.yaml solo abre el puerto a tu máquina. Sin
# --IdentityProvider.token, Jupyter crea un token al azar y lo escribe en el registro.
CMD ["jupyter", "lab", "--ip", "0.0.0.0", "--port", "8888", "--no-browser"]

# Etapa 5, la última: lo que se ejecuta en producción, y lo que construye
# `docker build .` sin --target. Solo Python y /opt/venv: ni uv, ni las herramientas de
# desarrollo, ni los tests, ni el código fuente.
FROM python:3.14.10-slim-trixie@sha256:9aaa474097d094040649f2162a627c0049b408f52138d980916788d80f04802f AS runtime

COPY --from=builder /opt/venv /opt/venv

# MPLCONFIGDIR: el usuario app no tiene carpeta personal, y matplotlib necesita una
# carpeta en la que pueda escribir su caché de fuentes. Sin ella, avisa en cada comando.
ENV PATH="/opt/venv/bin:$PATH" \
    MPLCONFIGDIR=/tmp/matplotlib

# Tres arreglos en una capa:
# - apt-get upgrade: los parches de seguridad de Debian publicados después de la imagen
#   base (el digest la congela, también con sus fallos);
# - fuera pip: en producción nadie instala nada, y pip trae sus propias dependencias
#   dentro (urllib3, msgpack...), cada una con sus avisos;
# - un usuario sin privilegios, por número: si alguien explota tu programa, no es root,
#   y quien ejecute la imagen puede comprobarlo sin buscar el nombre.
RUN apt-get update \
    && apt-get upgrade --yes \
    && rm -rf /var/lib/apt/lists/* \
        /usr/local/bin/pip* \
        /usr/local/lib/python3.14/site-packages/pip \
        /usr/local/lib/python3.14/site-packages/pip-*.dist-info \
    && useradd --no-create-home --shell /usr/sbin/nologin --uid 10001 app
USER 10001:10001

EXPOSE 8000

CMD ["observatorio", "servir", "--host", "0.0.0.0"]
