# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Alembic migrations, run by `create_app` at boot; `create_all` is gone
- Stdout logging configured by `create_app`, with `LOG_JSON` for structured
  output and `X-Request-ID` on every request and log line
- `/health` checks the database and answers 503 when a check fails
- Release workflow: a `v*` tag builds the multi-arch image, pushes it to GHCR,
  and publishes a GitHub release
- Ruff hooks in pre-commit and a coverage floor of 80%

### Changed

- The engine is built inside `create_app` and stored on `app.state`; tests
  no longer reload modules
- The container runs as the unprivileged `app` user and copies a pinned uv
  from its multi-arch image
- `bin/template-eject persistence` removes the dependencies and settings
  itself; an ejected copy passes lint, types, tests, and `bin/verify`
- `uv.lock` is tracked and guarded with `merge=ours` instead of hidden in
  `.git/info/exclude`

### Removed

- `requirements.txt`; `uv.lock` is the only lockfile
- File-based log handlers and the `LOG_DIR`, `LOG_FILE`, `LOG_ROTATION_*`,
  `LOG_BACKUP_COUNT`, `LOG_FORMAT` settings

### Earlier

- `bin/template-eject` removes optional layers (`docker`, `persistence`, `ci`)
  and guards them in `.gitattributes` against later merges
- `bin/verify` boots the service and checks `/health`, via compose or uvicorn
- `docker-compose.yml` and `docker-compose.override.yml`, with a healthcheck
- CI workflow: lint, types, tests, service boot, image build, arm64 check
- Test suite covering the app with and without the persistence layer
- Root `README.md`, previously empty
- `CORS_ORIGINS` and `DATABASE_URL` settings

### Changed

- Dockerfile rebuilt on uv and `python:3.12-slim`; no more Rust or pipenv
- uv installed in-image so the binary matches the target architecture
- Python pinned to 3.12 across `pyproject.toml`, `.python-version`, and Docker
- `bin/setup` registers the `merge.ours` driver, without which every
  `merge=ours` entry was inert
- Dependabot configured for uv, github-actions, and docker

### Removed

- The ditloid application code from `router.py` and `models.py`, replaced with a
  minimal example
- The hardcoded `ditloid.org` CORS origin

## [0.2]

- Updated and stripped back `uv` based template
