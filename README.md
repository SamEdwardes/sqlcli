# sqlcli

A command line interface (CLI) for interacting with SQLModel.

<hr>

**Source code:** [https://github.com/SamEdwardes/sqlcli](https://github.com/SamEdwardes/sqlcli)

**Docs:** [https://samedwardes.github.io/sqlcli/](https://samedwardes.github.io/sqlcli/)

**PyPi:** [https://pypi.org/project/sqlcli/](https://pypi.org/project/sqlcli/)

<hr>

## Installation

You can install *sqlcli* using pip:

```bash
pip install sqlcli
```

This will make the `sqlcli` command available in your python environment.

## Usage

The quickest way to get started with *sqlcli* is to create a demo sqlite database:

```bash
sqlcli init-demo
```

This will create a small sqlite database on your computer. The you can use sqlcli to explore your database.

```bash
sqlcli select -d "sqlite:///demo_database.db" -m "demo_models.py"
```

<div class="termy">

```console
$ sqlcli select -d "sqlite:///demo_database.db" -m "demo_models.py"
# Please select a table [sport/athlete]:$ athlete
┏━━━━┳━━━━━━━━━━┳━━━━━━━━━━┓
┃ id ┃ name     ┃ sport_id ┃
┡━━━━╇━━━━━━━━━━╇━━━━━━━━━━┩
│ 1  │ Ronaldo  │ 1        │
│ 2  │ Messi    │ 1        │
│ 3  │ Beckham  │ 1        │
│ 4  │ Gretzky  │ 2        │
│ 5  │ Crosby   │ 2        │
│ 6  │ Ovechkin │ 2        │
│ 7  │ Sundin   │ 2        │
│ 8  │ Domi     │ 2        │
└────┴──────────┴──────────┘
```

</div>
