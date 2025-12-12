# Multi-stage Dockerfile for SemantIQ Phase 0
# Stage 1: builder installs dependencies and package
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install build tools
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml README.md
COPY src ./src
COPY examples ./examples

# Build wheel
RUN python -m pip install --upgrade pip && pip wheel . -w /dist --extra-index-url https://pypi.org/simple

# Stage 2: runtime with SemantIQ installed
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Create data volume
VOLUME ["/data"]

# Install runtime dependencies and built wheel
COPY --from=builder /dist /dist
RUN python -m pip install --upgrade pip && pip install /dist/*.whl && pip install "semantiq[all]" --no-cache-dir

EXPOSE 8000

# Default entrypoint: launch dashboard reading from /data
CMD ["semantiq", "dashboard", "--answers-dir", "/data/answers", "--evals-dir", "/data/evals"]
