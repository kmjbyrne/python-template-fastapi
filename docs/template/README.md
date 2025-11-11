# Python Project Repository Template

Includes scaffolding for `ruff`, `black`, `mypy`, `commitizen` & `pre-commit`
for good standards for any development project.

## Usage

Let's take a brand new, virgin repository as an example.

```shell
mkdir new-project
cd new-project
git init
# this specifies the template repository as a remote, named template
git remote add template git@github.com-kmjbyrne:kmjbyrne/python.git
# then fetch all remotes
git fetch --all
# merge in the latest changes from the template main branch
git merge template/main
```

To remove the template and make the repository fully standalone:

```shell
git remote remove template
```

If you want to continue to leverage updates coming from the Python template,
then you have to do nothing else.

## Installing Dev Tools

```shell
pip install --user pipenv
pipenv install --dev
pipenv shell
# example ruff check
ruff check
```

## Installing Hooks

```shell
pre-commit install --hook-type pre-commit --hook-type pre-push
```
