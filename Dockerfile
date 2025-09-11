ARG SERVICE_NAME

# ---------------- Builder Stage ----------------
FROM python:3.13-slim AS builder

# Environment for reproducible, quiet Python
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps for installs and diagnostics
RUN apt-get update && apt-get install -y --no-install-recommends \
      git \
      curl \
      build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast, reproducible installs
RUN pip install uv

WORKDIR /build

# Use Docker layer caching for dependencies
COPY uv.lock pyproject.toml ./

# Create and populate a local virtual environment
RUN uv sync


# Copy the application source
COPY . .

# Optionally inject a config.json at build-time via BuildKit secret
# Provide with: --secret id=config_json,src=./config.json
# Falls back gracefully when BuildKit is not available
RUN --mount=type=secret,id=config_json,required=false,dst=/tmp/config.json \
    if [ -f /tmp/config.json ]; then \
        cp /tmp/config.json /build/config.json && echo "Config injected via BuildKit secret"; \
    elif [ -f config.json ]; then \
        echo "Using config.json from build context"; \
    else \
        echo "No config.json found - will use config_template.json if available"; \
    fi

# ---------------- Runtime Stage ----------------
FROM python:3.13-slim AS runtime

ARG SERVICE_NAME

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Minimal runtime tools
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
    && rm -rf /var/lib/apt/lists/*

# Create home ubuntu service hydra
RUN mkdir -p /home/ubuntu/1mg/$SERVICE_NAME/logs

# switch to code folder
WORKDIR /home/ubuntu/1mg/$SERVICE_NAME

# Copy and install requirements
ENV PATH="/.venv/bin:$PATH"

# Bring app and virtualenv from builder
COPY --from=builder /build /home/ubuntu/1mg/$SERVICE_NAME