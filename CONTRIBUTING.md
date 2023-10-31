# Contributing

## Project Setup

Configure your virtual environment of choice with Python >=3.7.

Install the project and its dependencies to your virtual environment with pip:

```commandline
pip install -r requirements.txt'
pip install -e '.[dev]'
```

Run pre-commit install to enable the pre-commit configuration:

```commandline
pre-commit install
```

The pre-commit hooks will be run against all files during a `git commit`, or
you can run it explicitly with:

```commandline
pre-commit run --all-files
```

If for some reason, you wish to commit code that does not pass the
pre-commit checks, this can be done with:

```commandline
git commit -m "message" --no-verify
```

## Testing

Tests are run using `pytest`. Put pytest python modules and other test
resources in the `/tests` directory.

## Adding/updating dependencies

### Updating `requirements.txt` to latest versions

All dependencies should be specified in the project's `pyproject.toml`. The
frozen `requirements.txt` file is generated from that list using the
`pip-compile` utility (from the dev dependency `pip-tools`). Simply run:

```commandline
pip-compile
```

### Updating package pinning

To change a package minimum or maximum version, edit the pinning specified in
`pyproject.toml` then run `pip-compile` as above.

### Adding a new package

To add a new package as a project dependency, edit the `pyproject.toml` and add
it to the corresponding dependeny list. Run `pip-compile` as above to update
`requirements.txt` with the new package.
