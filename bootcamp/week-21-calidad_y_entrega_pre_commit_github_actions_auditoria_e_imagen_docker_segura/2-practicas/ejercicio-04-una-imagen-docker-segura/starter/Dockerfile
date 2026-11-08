# Cuatro imágenes en un solo Dockerfile, una por etapa. Cada una se construye con
# `docker build --target <etapa>` y se compara con las anteriores.

# Etapa `ingenua`: la imagen que sale si no piensas en la seguridad. Funciona.
FROM python:3.14.10-trixie AS ingenua
COPY --from=ghcr.io/astral-sh/uv:0.13.7 /uv /uvx /bin/
WORKDIR /app
COPY . .
RUN uv sync --locked
CMD ["uv", "run", "python", "main.py"]

# ============================================
# PASO 2: Dos etapas: construir y ejecutar
# ============================================
# `builder` instala las dependencias del programa, sin las de desarrollo, en /opt/venv.
# `slim` copia solo ese entorno y main.py sobre una imagen pequeña, sin uv.
# Descomenta las siguientes líneas:
# FROM python:3.14.10-slim-trixie AS builder
# COPY --from=ghcr.io/astral-sh/uv:0.13.7 /uv /bin/
# ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
#     UV_COMPILE_BYTECODE=1 \
#     UV_LINK_MODE=copy \
#     UV_PYTHON_DOWNLOADS=never
# WORKDIR /app
# COPY pyproject.toml uv.lock .python-version ./
# RUN uv sync --locked --no-dev
#
# FROM python:3.14.10-slim-trixie AS slim
# COPY --from=builder /opt/venv /opt/venv
# COPY main.py /app/main.py
# WORKDIR /app
# ENV PATH="/opt/venv/bin:$PATH"
# CMD ["python", "main.py"]

# ============================================
# PASO 3: Sin root
# ============================================
# La misma imagen `slim`, con un usuario sin privilegios.
# Descomenta las siguientes líneas:
# FROM slim AS sin-root
# RUN useradd --no-create-home --shell /usr/sbin/nologin --uid 10001 app
# USER 10001:10001

# ============================================
# PASO 4: Fijada, parcheada y sin pip
# ============================================
# La imagen base por su digest, los parches de Debian posteriores a ella, fuera pip,
# y sin root. Es la forma del Dockerfile de tu proyecto.
# Descomenta las siguientes líneas:
# FROM python:3.14.10-slim-trixie@sha256:9aaa474097d094040649f2162a627c0049b408f52138d980916788d80f04802f AS segura
# COPY --from=builder /opt/venv /opt/venv
# COPY main.py /app/main.py
# WORKDIR /app
# ENV PATH="/opt/venv/bin:$PATH"
# RUN apt-get update \
#     && apt-get upgrade --yes \
#     && rm -rf /var/lib/apt/lists/* \
#         /usr/local/bin/pip* \
#         /usr/local/lib/python3.14/site-packages/pip \
#         /usr/local/lib/python3.14/site-packages/pip-*.dist-info \
#     && useradd --no-create-home --shell /usr/sbin/nologin --uid 10001 app
# USER 10001:10001
# CMD ["python", "main.py"]
