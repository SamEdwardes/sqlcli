# Contributing

*sqlcli* welcomes all contributors. If you would like to make a contribution please create a fork of the repository and then submit a pull request.

## Pull request check list

When creating a pull request please ensure you have completed the following:

- [ ] Run the black code formatter (`black sqlcli`).
- [ ] Run pytest (`pytest --forked`).
- [ ] Re-build the docs api reference (`python scripts/docs.py build-typer-docs`).
- [ ] Preview the docs (`mkdocs serve`)

## Docs

The docs are hosted on GitHub pages at: [https://samedwardes.github.io/sqlcli/](https://samedwardes.github.io/sqlcli/). When making changes remember to do the following:

- [ ] Rebuild the API reference.

```bash
python scripts/docs.py build-typer-docs
```

- [ ] Check how the docs look locally.

```bash
mkdocs serve
```

- [ ] Publish to GitHub pages.

```bash
python scripts/docs.py publish-docs
```

## Testing

Testing is performed with pytest. When running make sure to pass the `--forked` so that pytest spins up a "fresh" environment for each test. The `--forked` option comes from [pytest-xdist](https://github.com/pytest-dev/pytest-xdist).

```bash
pytest --forked
```

## Credits

### Open source libraries

Like all great open source software *sqlcli* is built on the shoulders of giants. *sqlcli* relies heavily on:

- [sqlmodel](https://github.com/tiangolo/sqlmodel)
- [sqlalchemy](https://www.sqlalchemy.org/)
- [typer](https://github.com/tiangolo/typer)
- [rich](https://github.com/Textualize/rich)
- [mkdocs-material](https://squidfunk.github.io/mkdocs-material/)
- and many more!

See the [pyproject.toml](https://github.com/SamEdwardes/sqlcli/blob/main/pyproject.toml) for all requirements.

### Icons and logo

Icons are from [fontawesome.com](https://fontawesome.com/). 

The logo is the [terminal icon](https://fontawesome.com/v5.15/icons/terminal?style=solid).

![logo](static/img/terminal-solid.svg){width="100"}



