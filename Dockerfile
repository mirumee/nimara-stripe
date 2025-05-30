FROM python:3.12

COPY --from=ghcr.io/astral-sh/uv:0.5.8 /uv /uvx /bin/

RUN apt-get update && apt-get install -y --no-install-recommends \
    awscli \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    UV_PROJECT_ENVIRONMENT=/usr/local/ \
    UV_CACHE_DIR=/tmp/uv-cache

WORKDIR /app

# Copy and install dependencies as root
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY . ./
RUN uv sync --frozen

# Create user with home directory and set permissions
RUN groupadd -r appuser && useradd -r -g appuser -m appuser \
    && chown -R appuser:appuser /app \
    && mkdir -p /tmp/uv-cache \
    && chown -R appuser:appuser /tmp/uv-cache

USER appuser

EXPOSE 8080

CMD ["python", "-m", "smyth"]