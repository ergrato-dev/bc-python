# Etapa 1: de esta imagen solo se toman los binarios de uv (versión fijada).
FROM ghcr.io/astral-sh/uv:0.13.7 AS uv

# Etapa 2: la imagen final, con el mismo Python que fija .python-version.
FROM python:3.14.10-slim-trixie

COPY --from=uv /uv /uvx /bin/

# UV_PYTHON_DOWNLOADS=never: usar el Python de la imagen, nunca descargar otro.
# UV_PROJECT_ENVIRONMENT: el entorno vive fuera de /app, así no lo pisa un volumen.
# UV_COMPILE_BYTECODE=1: compila a .pyc al instalar; el arranque es más rápido.
# PATH: los comandos del entorno (python, pytest) se usan sin `uv run`; la imagen
# ya está sincronizada y así uv no intenta tocar /opt/venv al arrancar.
# PYTEST_ADDOPTS: sin caché de pytest, que no podría escribirse en /app.
ENV UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/opt/venv/bin:$PATH" \
    PYTEST_ADDOPTS="-p no:cacheprovider"

WORKDIR /app

# Primero solo los archivos de dependencias: esta capa se reutiliza (caché)
# mientras pyproject.toml y uv.lock no cambien, aunque cambie tu código.
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked

# Después el código: cambia a menudo, por eso va al final.
COPY . .

# Paso 6: aquí falta un usuario sin privilegios.

CMD ["pytest"]
