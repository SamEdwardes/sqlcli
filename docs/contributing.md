# Contributing

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

## Credits

### Open source libraries

Like all great open source software *sqlcli* is built on the shoulders of giants. *sqlcli* relies heavily on:

- sqlmodel
- sqlalchemy
- typer
- rich
- mkdocs-material
- and many more!

See the [pyproject.toml](https://github.com/SamEdwardes/sqlcli/blob/main/pyproject.toml) for all requirements.

### Icons and logo

Icons are from [fontawesome.com](https://fontawesome.com/). 

The logo is the [terminal icon](https://fontawesome.com/v5.15/icons/terminal?style=solid).

![logo](static/img/terminal-solid.svg){width="100"}



