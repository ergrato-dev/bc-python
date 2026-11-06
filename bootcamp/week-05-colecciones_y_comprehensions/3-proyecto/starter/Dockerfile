# Etapa 1: de esta imagen solo se toman los binarios de uv (versión fijada).
FROM ghcr.io/astral-sh/uv:0.13.7 AS uv

# Etapa 2: la imagen final, con el mismo Python que fija .python-version.
FROM python:3.14.10-slim-trixie

COPY --from=uv /uv /uvx /bin/

# UV_PYTHON_DOWNLOADS=never: usar el Python de la imagen, nunca descargar otro.
# UV_PROJECT_ENVIRONMENT: el entorno vive fuera de /app, así no lo pisa un volumen.
# UV_COMPILE_BYTECODE=1: compila a .pyc al instalar; el arranque es más rápido.
# PATH: los comandos del entorno (python, pytest, observatorio) se usan sin `uv run`.
# PYTEST_ADDOPTS: sin caché de pytest, que no podría escribirse en /app.
ENV UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/opt/venv/bin:$PATH" \
    PYTEST_ADDOPTS="-p no:cacheprovider"

WORKDIR /app

# Primero solo las dependencias, sin tu paquete: esta capa se reutiliza (caché)
# mientras pyproject.toml y uv.lock no cambien, aunque cambie tu código.
COPY pyproject.toml uv.lock .python-version README.md ./
RUN uv sync --locked --no-install-project

# Después el código, que cambia a menudo, y la instalación de tu paquete.
COPY . .
RUN uv sync --locked

# Usuario sin privilegios: si alguien explota tu programa, no es root.
RUN useradd --create-home --uid 10001 app
USER app

CMD ["pytest"]
