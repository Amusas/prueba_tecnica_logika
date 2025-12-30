############################
# 1️⃣ Builder
############################
FROM python:3.11.8-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install --prefix=/install --no-warn-script-location -r requirements.txt

############################
# 2️⃣ Runtime
############################
FROM python:3.11.8-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PATH="/usr/local/bin:$PATH"

# Usuario no root
RUN addgroup --system appgroup && \
    adduser --system --no-create-home --ingroup appgroup appuser

WORKDIR /app

# Dependencias runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    netcat-openbsd \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependencias Python
COPY --from=builder /install /usr/local

# Copiar aplicación
COPY --chown=appuser:appgroup . .

# Entrypoint
COPY --chown=appuser:appgroup entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER appuser

EXPOSE 8000

# Healthcheck opcional
# HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
#     CMD curl -f http://localhost:8000/health || exit 1

ENTRYPOINT ["/entrypoint.sh"]