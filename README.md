# sqlcli

A command line interface (CLI) for interacting with SQLModel.

<hr>

**Source code:** [https://github.com/SamEdwardes/sqlcli](https://github.com/SamEdwardes/sqlcli)

**Docs:** [https://samedwardes.github.io/sqlcli/](https://samedwardes.github.io/sqlcli/)

**PyPi:** [https://pypi.org/project/sqlcli/](https://pypi.org/project/sqlcli/)

<hr>

<img src="https://i.imgur.com/MSFiWRS.gif"/>

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

This will create a small sqlite database on your computer. The you can use sqlcli to explore your database. View your table by using the `select` command.

```bash
sqlcli select athlete -d "sqlite:///demo_database.db" -m "demo_models.py"
```

```bash
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
│ 9  │ Carter   │ 1        │
└────┴──────────┴──────────┘
```