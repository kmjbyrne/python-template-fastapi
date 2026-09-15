# FastAPI Template

A modular FastAPI template. Ships with SQLModel persistence, Docker, CI, release
automation, and Claude Code workflows. Keep what you want, eject the rest.

## Using This Template

If starting from scratch, create the repository first:

```shell
git init my-project && cd my-project
git commit --allow-empty -m "init: empty repository"
```

From an existing repository, or after the step above:

```shell
git remote add template git@github.com-kmjbyrne:kmjbyrne/python-template-fastapi.git
git fetch template
git merge template/main --squash --allow-unrelated-histories
git commit -m "init: template scaffold"
bin/setup
```

Then remove what you do not need:

```shell
bin/template                  # list layers
bin/template eject docker     # remove one
```

See [docs/template/fastapi/README.md](docs/template/fastapi/README.md) for a
detailed overview of what the template provides.

## Template Updates

The initial squash merge means git has no shared history with the template. To
pull updates later, either merge with conflict resolution or inject specific
layers from the remote:

```shell
git fetch template
git merge template/main --allow-unrelated-histories

# or, for a single layer:
bin/template inject release
```

`bin/setup` registers the `merge=ours` driver so paths listed in
`.gitattributes` stay yours across merges. Ejected layers are automatically
guarded. To protect another path, add `path merge=ours` to `.gitattributes`.

## Getting Started

```shell
bin/setup
uv run python main.py
```

Listens on <http://localhost:8000>. Docs at `/docs`. `/health` returns readiness
status and answers 503 when a dependency check fails.

## Optional Layers

| Layer         | What it covers                                                             |
| ------------- | -------------------------------------------------------------------------- |
| `docker`      | `Dockerfile`, compose files, `.dockerignore`                               |
| `persistence` | Alembic, SQLModel, `app/adapter/`, `app/db.py`, `app/dependencies.py`      |
| `ci`          | `.github/workflows/ci.yml`, dependabot, pre-commit                         |
| `release`     | `.github/workflows/release.yml`                                            |
| `claude`      | `.github/workflows/claude.yml`, `.github/workflows/claude-code-review.yml` |

```shell
bin/template                              # list status
bin/template eject docker ci              # remove layers
bin/template inject release               # install from the template remote
```

The app boots with any combination removed. Ejected paths are guarded in
`.gitattributes` so `git merge template/main` does not reinstate them.

## Verify

```shell
bin/verify           # compose when available, otherwise uvicorn
bin/verify --local   # always uvicorn
bin/verify --docker  # require compose
```

Boots the service, polls `/health`, exits non-zero if it never becomes healthy.

## Docker

```shell
docker compose up --build
```

`docker-compose.override.yml` is the dev layer: mounts source, runs with
`--reload`. The build is architecture-neutral (amd64 and arm64). The container
runs as the unprivileged `app` user.

## Releasing

```shell
uv run cz bump          # bump version, tag vX.Y.Z
git push --follow-tags
```

The `v*` tag triggers the release workflow: builds and pushes a multi-arch image
to GHCR, creates a GitHub release with generated notes.

## Database Migrations

Alembic runs `upgrade head` on every boot. After changing a model:

```shell
uv run alembic revision --autogenerate -m "add item.price"
uv run alembic upgrade head
```

## Layout

```text
app/
  adapter/repository/sqlite/   models (ejectable)
  config.py                    settings, env-driven
  db.py                        engine factory (ejectable)
  dependencies.py              session dependency (ejectable)
  factory.py                   create_app
  router.py                    routes
bin/
  setup                        first-run setup
  lint                         ruff and mypy
  verify                       boot and check /health
  template                     manage optional layers
tests/
alembic/                       migrations (ejectable)
```

## Configuration

Settings come from environment variables or `.env`. `bin/setup` creates `.env`
if missing. `ENVIRONMENT=production` loads `.env.production`.
