# Build stage with uv
FROM ghcr.io/astral-sh/uv:latest AS uv-bin
FROM python:3.12-slim AS builder

WORKDIR /app

COPY --from=uv-bin /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Install dependencies into virtual environment
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Runtime stage
FROM python:3.12-slim AS runner

# Create non-root system user
RUN groupadd -r appuser && useradd -r -g appuser -d /app appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy application source code
COPY --chown=appuser:appuser main.py ./
COPY --chown=appuser:appuser schedulebot/ ./schedulebot/

# Setup persistent data directory for SQLite
RUN mkdir -p /app/data && chown -R appuser:appuser /app/data

USER appuser

VOLUME ["/app/data"]

ENV SQLITE_DBFILE=/app/data/schedule.db

CMD ["python", "main.py"]
