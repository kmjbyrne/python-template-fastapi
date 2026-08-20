# FastAPI Template

A FastAPI base template with a modular layout, so consumers keep only the parts
they want. Ships with SQLModel persistence, a portable Docker build, and CI that
proves the service actually boots.

## Getting started

```shell
bin/setup
uv run python main.py
```

The service listens on <http://localhost:8000>. Interactive docs are at `/docs`.
`/health` returns `{"status": true, "database": true}` and answers 503 when a
dependency check fails, so the compose healthcheck and load balancers see real
readiness rather than "the process is up".

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
| `docker`      | `Dockerfile`, both compose files, `.dockerignore`             |
| `persistence` | `alembic/`, `alembic.ini`, `app/db.py`, `app/dependencies.py`, `app/adapter/`, its tests; drops `sqlmodel` and `alembic` from `pyproject.toml` and cuts `DATABASE_URL` and the engine setup from `config.py`, `factory.py`, `.env.example` |
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
manifests, uv is copied from its multi-arch image so the binary matches the
target rather than the builder, and every dependency is a pure-Python wheel. Building on
an M-series Mac produces an arm64 image, and on an x86 host an amd64 image, with
no changes.

Nothing defaults to arm64. To build one or both explicitly:

```shell
docker buildx build --platform linux/arm64 -t app:arm64 .
docker buildx build --platform linux/amd64,linux/arm64 -t app:multi .
```

CI builds arm64 on every run purely as a portability check.

The container runs as the unprivileged `app` user. `instance/` is the only path
it can write to; the compose file mounts a volume there.

## CI

`.github/workflows/ci.yml` runs three jobs:

- **quality** — ruff check, ruff format, mypy, pytest
- **boot** — starts the service and hits `/health`
- **docker** — builds the image, waits for the compose healthcheck, then builds arm64

The docker job detects an ejected Docker layer and skips itself, so CI stays
green after `bin/template-eject docker`.

## Releasing

Versions live in `pyproject.toml` and are managed by commitizen from the
conventional commit history:

```shell
uv run cz bump          # bumps the version, updates CHANGELOG.md, tags vX.Y.Z
git push --follow-tags
```

Pushing a `v*` tag runs `.github/workflows/release.yml`, which builds the image
for every platform in `BUILD_PLATFORMS`, pushes it to
`ghcr.io/<owner>/<repo>` tagged `X.Y.Z`, `X.Y`, and `latest`, and publishes a
GitHub release with generated notes. Without the Docker layer it still creates
the release.

## Layout

```text
app/
  adapter/repository/sqlite/   models (optional, ejectable)
  config.py                    settings, env-driven
  db.py                        engine factory and migration runner (optional)
  dependencies.py              session dependency (optional)
  factory.py                   create_app
  router.py                    routes
bin/
  setup                        first-run setup
  lint                         ruff and mypy
  verify                       boot the service and check /health
  template-eject               remove an optional layer
tests/
alembic/                       migrations (optional, ejectable)
```

Any module placed in `app/adapter/repository/sqlite/` is imported at startup, so
new models need no registration.

## Database migrations

The schema is managed by Alembic. `create_app` runs `alembic upgrade head`
against the configured database on every boot, so a fresh checkout, the test
suite, and a container all start with the current schema and nothing else.

After changing a model:

```shell
uv run alembic revision --autogenerate -m "add item.price"
uv run alembic upgrade head
```

Review the generated file under `alembic/versions/` before committing it.
Autogenerate does not see every change (renames, server defaults, some
constraint edits) and SQLite needs batch mode for most `ALTER TABLE` work,
which `alembic/env.py` already enables.

## Configuration

Settings come from environment variables or a `.env` file; see `.env.example`.
`bin/setup` creates `.env` if it is missing. `ENVIRONMENT=production` loads
`.env.production`.

## Consuming this template

See [docs/template/fastapi/README.md](docs/template/fastapi/README.md).
