# Multi-stage build for optimized image size

# Builder stage
FROM python:3.12-slim AS builder

WORKDIR /app

# Install uv for fast dependency management
RUN pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install dependencies with increased timeout
ENV UV_HTTP_TIMEOUT=120
RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install -e .

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

# Install curl for health checks
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY src/ /app/src/

# Create non-root user
RUN useradd --create-home --shell /bin/bash fmgmcp && \
    chown -R fmgmcp:fmgmcp /app

# Create logs directory
RUN mkdir -p /app/logs && chown fmgmcp:fmgmcp /app/logs

# Switch to non-root user
USER fmgmcp

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src" \
    PYTHONUNBUFFERED=1

# Expose MCP server port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run server
CMD ["python", "-m", "fortimanager_mcp"]

