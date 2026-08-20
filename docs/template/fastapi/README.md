# Consuming the FastAPI template

## First use

Run this inside the new repository:

```shell
git remote add template git@github.com-kmjbyrne:kmjbyrne/python-template-fastapi.git
git fetch template
git merge template/main --allow-unrelated-histories
bin/setup
```

Then remove the layers you do not want:

```shell
bin/template-eject            # see what is optional
bin/template-eject docker
```

## Pulling later template updates

```shell
git fetch template
git merge template/main
```

To stop tracking the template entirely:

```shell
git remote remove template
```

## Keeping your own files

`bin/setup` runs `git config merge.ours.driver true`. This matters. `merge=ours`
in `.gitattributes` is inert without it: git ignores the attribute and you get a
conflict on every file the template also changed.

With the driver registered, these files stay yours on every merge:

- `README.md`
- `docs/template/README.md`
- `.env.example`
- `pyproject.toml`

Write your own README and it survives future merges. Everything else still
updates normally.

`bin/template-eject` adds the paths it removes to the same list, so ejected
layers do not reappear.

### Limits

`merge=ours` resolves a file both sides changed. It does not block a file that is
new to your repository. If a future template version adds a file you have never
had, the merge brings it in; delete it and it is guarded from then on.

To protect another path, add it to `.gitattributes`:

```gitattributes
path/to/file merge=ours
directory/** merge=ours
```

Directories need the `/**` glob. A bare directory path matches nothing.

## Renaming the project

`pyproject.toml` and `.env.example` both carry `CHANGEME`. Both are guarded, so
edit them once and merges will not revert your names.
