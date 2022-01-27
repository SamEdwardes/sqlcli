# Features

## Demo

Create a demo database to explore test *sqlcli* by using the `init-demo` command:

```bash
sqlcli init-demo
```

<div class="termy">

```console
$ sqlcli init-demo
───────────────────────── table: sport ──────────────────────────
┏━━━━━━━━┳━━━━┓
┃ name   ┃ id ┃
┡━━━━━━━━╇━━━━┩
│ Soccer │ 1  │
│ Hockey │ 2  │
└────────┴────┘
──────────────────────── table: athlete ─────────────────────────
┏━━━━┳━━━━━━━━━━┳━━━━━━━━━━┓
┃ id ┃ sport_id ┃ name     ┃
┡━━━━╇━━━━━━━━━━╇━━━━━━━━━━┩
│ 1  │ 1        │ Ronaldo  │
│ 2  │ 1        │ Messi    │
│ 3  │ 1        │ Beckham  │
│ 4  │ 2        │ Gretzky  │
│ 5  │ 2        │ Crosby   │
│ 6  │ 2        │ Ovechkin │
│ 7  │ 2        │ Sundin   │
│ 8  │ 2        │ Domi     │
└────┴──────────┴──────────┘
───────────────── how to use the demo database ──────────────────
A demo database has been created at:
/Users/samedwardes/git/sqlcli/demo_database.db

Demo models have been saved to:
/Users/samedwardes/git/sqlcli/demo_models.py

Here are some example commands to get you started:

sqlcli select athlete -d "sqlite:///demo_database.db" -m demo_models.py
sqlcli insert -d "sqlite:///demo_database.db" -m demo_models.py

To avoid passing in the `-d` and -`m` option everytime you can set the following environment 
variables:

export DATABASE_URL="sqlite:///demo_database.db"
export MODELS_PATH="demo_models.py"

For instructions on how to use the demo database visit 
https://samedwardes.github.io/sqlcli/tutorial/using-demo-db/.
```

</div>

## Select

Select data from your SQL database using the `select` command:

```bash
sqlcli select athlete -d "sqlite:///demo_database.db" -m "demo_models.py"
```

<div class="termy">

```console
$ sqlcli select athlete -d "sqlite:///demo_database.db" -m "demo_models.py"
┏━━━━┳━━━━━━━━━━┳━━━━━━━━━━┓
┃ id ┃ sport_id ┃ name     ┃
┡━━━━╇━━━━━━━━━━╇━━━━━━━━━━┩
│ 1  │ 1        │ Ronaldo  │
│ 2  │ 1        │ Messi    │
│ 3  │ 1        │ Beckham  │
│ 4  │ 2        │ Gretzky  │
│ 5  │ 2        │ Crosby   │
│ 6  │ 2        │ Ovechkin │
│ 7  │ 2        │ Sundin   │
│ 8  │ 2        │ Domi     │
└────┴──────────┴──────────┘
```

</div>

## Insert

Interactively insert new data using the `insert` command:

```bash
sqlcli insert athlete -d "sqlite:///demo_database.db" -m "demo_models.py"
```

<div class="termy">

```console
$ sqlcli insert athlete -d "sqlite:///demo_database.db" -m "demo_models.py"

───────────────────────── column: `id` ──────────────────────────
# <class 'int'> (optional):$ 
──────────────────────── column: `name` ─────────────────────────
# <class 'str'>:$ Carter 
────────────────────── column: `sport_id` ───────────────────────
The column `sport_id` is a foreign key related to the `sport` table. Please select from one of the 
options below from the `id` column:
     sport     
┏━━━━━━━━┳━━━━┓
┃ name   ┃ id ┃
┡━━━━━━━━╇━━━━┩
│ Soccer │ 1  │
│ Hockey │ 2  │
└────────┴────┘
# <class 'int'> (optional) [1/2]:$ 1
╭──────────────── New row successfully added 🎉 ────────────────╮
│ {'id': 9, 'sport_id': 1, 'name': 'Carter'}                    │
╰───────────────────────────────────────────────────────────────╯
```

</div>

## Set defaults

Type less by setting a default database url and models module:

```bash
export DATABASE_URL="sqlite:///demo_database.db"
export MODELS_PATH="demo_models.py"
```

```bash
sqlcli select athlete
```

<div class="termy">

```console
$ sqlcli select athlete
┏━━━━┳━━━━━━━━━━┳━━━━━━━━━━┓
┃ id ┃ sport_id ┃ name     ┃
┡━━━━╇━━━━━━━━━━╇━━━━━━━━━━┩
│ 1  │ 1        │ Ronaldo  │
│ 2  │ 1        │ Messi    │
│ 3  │ 1        │ Beckham  │
│ 4  │ 2        │ Gretzky  │
│ 5  │ 2        │ Crosby   │
│ 6  │ 2        │ Ovechkin │
│ 7  │ 2        │ Sundin   │
│ 8  │ 2        │ Domi     │
└────┴──────────┴──────────┘
```

<div>

