# FastAPI Template

A FastAPI base template with a modular layout, so consumers keep only the parts
they want. Ships with SQLModel persistence, a portable Docker build, and CI that
proves the service actually boots.

## Getting started

```shell
bin/setup
uv run python main.py
```

The service listens on <http://localhost:8000>. Interactive docs are at `/docs`,
and `/health` returns `{"status": true}`.

## Removing what you do not need

Three layers are optional. Remove any of them with one command:

```shell
bin/template-eject                    # list layers and whether they are present
bin/template-eject --dry-run docker   # preview
bin/template-eject docker             # remove
bin/template-eject docker ci          # remove several
```

| Layer         | Removes                                                      |
| ------------- | ------------------------------------------------------------ |
| `docker`      | `Dockerfile`, `docker-entrypoint.sh`, both compose files, `.dockerignore` |
| `persistence` | `app/db.py`, `app/dependencies.py`, `app/adapter/`, its tests |
| `ci`          | `.github/workflows/`, `.github/dependabot.yml`, `.pre-commit-config.yaml` |

The app boots with any combination of these removed. Ejection also appends the
removed paths to `.gitattributes` with `merge=ours`, so a later
`git merge template/main` will not reinstate them.

Ejection is one-way. Recover a layer with `git revert` or by checking the paths
back out from the template remote.

## Verifying it runs

```shell
bin/verify           # docker compose when available, otherwise uvicorn
bin/verify --local   # always uvicorn
bin/verify --docker  # require docker compose
```

Either way it boots the service, polls `/health`, and exits non-zero if the
service never becomes healthy. In Docker mode it waits on the compose
healthcheck, so a container that starts but never serves traffic fails the run.

## Docker

```shell
docker compose up --build
```

`docker-compose.override.yml` is applied automatically and is the development
layer: it mounts your source and runs uvicorn with `--reload`. CI uses
`docker-compose.yml` alone to test the image as it would actually ship.

### Architectures

The build is architecture-neutral. `python:3.12-slim` publishes amd64 and arm64
manifests, uv is installed inside the image so the binary matches the target
rather than the builder, and every dependency is a pure-Python wheel. Building on
an M-series Mac produces an arm64 image, and on an x86 host an amd64 image, with
no changes.

Nothing defaults to arm64. To build one or both explicitly:

```shell
docker buildx build --platform linux/arm64 -t app:arm64 .
docker buildx build --platform linux/amd64,linux/arm64 -t app:multi .
```

CI builds arm64 on every run purely as a portability check.

## CI

`.github/workflows/ci.yml` runs three jobs:

- **quality** — ruff check, ruff format, mypy, pytest
- **boot** — starts the service and hits `/health`
- **docker** — builds the image, waits for the compose healthcheck, then builds arm64

The docker job detects an ejected Docker layer and skips itself, so CI stays
green after `bin/template-eject docker`.

## Layout

```text
app/
  adapter/repository/sqlite/   models (optional, ejectable)
  config.py                    settings, env-driven
  db.py                        engine and table creation (optional)
  dependencies.py              session dependency (optional)
  factory.py                   create_app
  router.py                    routes
bin/
  setup                        first-run setup
  lint                         ruff and mypy
  verify                       boot the service and check /health
  template-eject               remove an optional layer
tests/
```

Any module placed in `app/adapter/repository/sqlite/` is imported at startup, so
new models need no registration.

## Configuration

Settings come from environment variables or a `.env` file; see `.env.example`.
`bin/setup` creates `.env` if it is missing. `ENV_FILE=production` loads
`.env.production`.

## Consuming this template

See [docs/template/fastapi/README.md](docs/template/fastapi/README.md).
