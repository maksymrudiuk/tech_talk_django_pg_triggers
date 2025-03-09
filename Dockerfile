FROM python:3.12.1 AS base

# Assure UTF-8 encoding is used.
ENV LC_CTYPE=C.utf8
ENV DEBIAN_FRONTEND=noninteractive

# Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONBREAKPOINT=ipdb.set_trace

# UV
ENV UV_PYTHON=python3.12.1
ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
ENV UV_PROJECT_ENVIRONMENT="/opt/.venv"
ENV UV_PYTHON_INSTALL_DIR="/python"
ENV PATH="$UV_PROJECT_ENVIRONMENT/bin:$PATH"

# Install system dependencies
RUN set -ex; \
  if ! command -v gpg > /dev/null; then \
  apt-get update; \
  apt-get install -y --no-install-recommends \
  gnupg \
  dirmngr \
  ; \
  rm -rf /var/lib/apt/lists/*; \
  fi

RUN set -xe; \
  apt-get update; \
  apt-get install -y --no-install-recommends \
  curl \
  make \
  apt-transport-https \
  ca-certificates \
  lzma \
  gettext \
  libc6-dev \
  gcc \
  libevent-dev \
  libffi-dev \
  libpng-dev \
  libjpeg-dev \
  zlib1g-dev \
  libtiff-dev \
  libfreetype6 \
  libwebp-dev \
  libpq-dev; \
  find /var/lib/apt/lists \
  /usr/share/man \
  /usr/share/doc \
  /var/log \
  -type f -exec rm -f {} +

# Create application directory
RUN mkdir -p /app
WORKDIR /app

###############################################################################
FROM base AS boot

# Install supervisor
RUN mkdir -p /init && mkdir -p /init/boot
COPY conf/supervisord.conf /init/supervisord.conf
RUN set -xe; \
  pip install "supervisor>=4,<5"; \
  ln -s /init/supervisord.conf /usr/local/supervisord.conf

CMD ["supervisord", "-c", "/init/supervisord.conf", "--"]

###############################################################################
FROM boot AS deps

# Upgrade pip and install uv package manager
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir uv

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --no-install-project


FROM deps AS develop

# Install additional development dependencies
RUN set -xe; \
  apt-get update; \
  apt-get install -y --no-install-recommends \
  nano \
  lsof