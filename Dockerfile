# Base Python image with specific version for reproducible builds
FROM python:3.12-slim AS builder

# Import UV from official repository
COPY --from=ghcr.io/astral-sh/uv:0.5.8 /uv /uvx /bin/

# Install system dependencies with cleanup in the same layer to reduce image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    awscli \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set Python environment variables for better Docker usage
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    UV_PROJECT_ENVIRONMENT=/usr/local/

WORKDIR /app

# Copy dependency files separately to leverage Docker caching
COPY pyproject.toml uv.lock ./
COPY libs ./libs

# Install dependencies
RUN uv sync --frozen --no-install-project

# Copy application code
COPY . ./
RUN uv sync --frozen

# Create a non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser \
    && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Document the port the application uses
EXPOSE 8080

# Add health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Set default command to run the application
CMD ["python", "-m", "smyth"]
