#!/usr/bin/env bash

set -e

echo "=== Docker Entrypoint Debug ==="
echo "ENV_FILE: ${ENV_FILE:-<not set>}"
echo "Working directory: $(pwd)"
echo "Available .env files:"
ls -la .env* 2>/dev/null || echo "No .env files found"

if [[ -n "$ENV_FILE" ]]; then
    echo "Loading env file: $ENV_FILE"
    source bin/load-env "$ENV_FILE"
else
    echo "Loading default .env"
    source bin/load-env
fi

echo "Sample env vars after loading:"
echo "ENVIRONMENT: ${ENVIRONMENT:-<not set>}"
echo "HOST: ${HOST:-<not set>}"
echo "==============================="

exec "$@"
