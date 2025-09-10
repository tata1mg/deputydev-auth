# syntax=docker/dockerfile:1.7
FROM python:3.13-slim AS builder

# Environment for reproducible, quiet Python
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps for installs and diagnostics
RUN apt-get update && apt-get install -y --no-install-recommends \
      git \
      curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast, reproducible installs
RUN pip install --no-cache-dir uv

WORKDIR /app

# Use Docker layer caching for dependencies
COPY pyproject.toml uv.lock ./

# Create and populate a local virtual environment under /app/.venv
RUN uv sync --frozen

# Copy the application source
COPY . .

# Optionally inject a config.json at build-time via BuildKit secret
# Provide with: --secret id=config_json,src=./config.json
RUN --mount=type=secret,id=config_json,required=false,dst=/tmp/config.json \
    if [ -f /tmp/config.json ]; then cp /tmp/config.json /app/config.json; fi

# ---------------- Runtime ----------------
FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/app/.venv/bin:$PATH

# Minimal runtime tools
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Bring app and virtualenv from builder
COPY --from=builder /app /app

# Expose service port
# Default command (same startup pattern)
CMD ["python", "-m", "app.service"]