# FastAPI Template Overview

This template provides a production-ready FastAPI scaffold. Every piece is
designed to work together, but each optional layer can be ejected independently
with `bin/template eject`.

## Application Factory

The app is built through `app/factory.py:create_app()`. It wires up the router,
middleware, CORS, and health checks in one place. Settings come from
`pydantic-settings`, which reads `.env` files in precedence order and lets real
environment variables win.

`pyproject.toml` and `.env.example` carry `CHANGEME` markers. Both are guarded
with `merge=ours`, so your edits survive template merges.

## Health Check

`/health` reports liveness plus the state of each registered dependency. The
persistence layer registers a database ping. When any check fails the endpoint
returns 503, so compose health checks and load balancers see real readiness.

## Structured Logging

All output goes to stdout. `RequestIdMiddleware` assigns or propagates a
`X-Request-ID` header on every request and attaches it to log records via a
context variable. Set `LOG_JSON=true` for one JSON object per line, or leave it
off for human-readable text. Uvicorn's own handlers are stripped, so everything
flows through the shared format.

## Persistence (Ejectable)

SQLModel models live in `app/adapter/repository/sqlite/`. Alembic manages
migrations and runs `upgrade head` on every boot, so a fresh checkout, the test
suite, and a container all start with the current schema. The session dependency
is in `app/dependencies.py`.

## Docker (Ejectable)

The `Dockerfile` builds a multi-arch image (amd64 and arm64) that runs as an
unprivileged `app` user. `docker-compose.override.yml` is the dev layer: it
mounts source and runs with `--reload`. CI uses `docker-compose.yml` alone to
test the image as it would ship.

## CI (Ejectable)

`.github/workflows/ci.yml` runs linting (`bin/lint`) and tests (`pytest`).
Dependabot keeps Python, GitHub Actions, and Docker dependencies current.
Pre-commit hooks enforce the same checks locally.

## Release (Ejectable)

Commitizen manages versioning from the conventional commit history. Pushing a
`v*` tag triggers the release workflow, which builds and pushes a multi-arch
image to GHCR and creates a GitHub release with generated notes.

## Claude Code (Ejectable)

Two workflows: `claude.yml` responds to `@claude` mentions in issues and PR
comments, and `claude-code-review.yml` runs an automated code review on every
pull request. Both require `CLAUDE_CODE_OAUTH_TOKEN` in repo secrets.
