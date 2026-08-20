# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

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
