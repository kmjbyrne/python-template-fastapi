# syntax=docker/dockerfile:1

# Keep this in step with .python-version and requires-python in pyproject.toml.
# python:*-slim publishes amd64 and arm64 manifests, so the base resolves for
# both. Build other architectures with:
#   docker buildx build --platform linux/amd64,linux/arm64 -t app:local .
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    groupadd --system app && \
    useradd --system --gid app --home-dir /usr/src/app --no-create-home app

# The uv image is multi-arch, so this copies the binary for the target
# platform. Pinned so builds are reproducible and Dependabot can bump it.
COPY --from=ghcr.io/astral-sh/uv:0.9.9 /uv /usr/local/bin/uv

# Dependencies resolve in their own layer so app edits do not invalidate them.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

COPY . .
RUN uv sync --frozen --no-dev && \
    mkdir -p instance && \
    chown -R app:app /usr/src/app

USER app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
