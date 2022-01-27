# Using the demo database

For *sqlcli* to be useful you need two things:

1. **database**
2. **SQLModel** object(s)

Luckily, *sqlcli* comes with a built in command to spin up a small SQLite database and a python file with SQLModel classes you can using for experimenting. 

## Set up

To get started, lets first create a new directory you can use to experiment with *sqlcli*.

```bash
mkdir demo
cd demo
```

Then, run the `init-demo` command to create the SQLite database and a python file that contains the SQLModel definitions.
    
```bash
sqlcli init-demo
```

This will create a new sqlite database on your computer and the related SQLModel classes that you can then use to test *sqlcli*. The command will output two new files in your working directory:

```bash
.
├── demo_database.db # A sqlite database with demo data.
└── demo_models.py   # SQLModel classes that map to the demo database.
```

With these two files you have everything you need to start working with *sqlcli* 🎉. The demo models are defined as follows:

```Python title="demo_models.py" linenums="1"
{!./sqlcli/_demo/models.py!}
```

## Explore the database

Now with your database in place and your models defined you will be able to
play with *sqlcli*! Lets try a few different commands and see what happens.

### `sqlcli select`

The `select` command is similar to `SELECT * FROM <TABLE>` in SQL. You can use it to view your data.

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

Because you defined your models in the *demo_models.py* file *sqlcli* knows the tables that are in your database and will automatically prompt you to choose of the tables.

Sometimes you may already know the name of your table. In that case, you can pass the name of the table to the `select` command as an argument.

```bash
sqlcli select sport -d "sqlite:///demo_database.db" -m "demo_models.py"
```

<div class="termy">

```console
$ sqlcli select sport -d "sqlite:///demo_database.db" -m "demo_models.py"
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

### `sqlcli insert`

The `insert` command is similar to `INSERT INTO <TABLE>` from SQL. You can use it to add new records to your database. Just like with the select command you can optionally specify the name of the table if you already know it. Try it out!

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

Because you defined your models using SQLModel sqlcli already knows a lot about your database. You will be prompted to enter a new value for each record attribute:

- Optional attributes are not required.
- Foreign keys will only accept valid options and will give your a preview of the possible options.
- Types are automatically enforced (e.g. integers must be integers).

## Setting up environment variables

It can be annoying to specify the database URL and SQLModel modules every time. To avoid this you can set two environment variables the *sqlcli* will default to:

```bash
export DATABASE_URL="sqlite:///demo_database.db"
export MODELS_PATH="tests/models/sports.py
```

Now you can call the same commands but without specifying the `-d` and `-m` options:

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
│ 9  │ 1        │ Carter   │
└────┴──────────┴──────────┘
```

</div>

```bash
sqlcli select sport
```

<div class="termy">

```console
$ sqlcli select sport
┏━━━━━━━━┳━━━━┓
┃ name   ┃ id ┃
┡━━━━━━━━╇━━━━┩
│ Soccer │ 1  │
│ Hockey │ 2  │
└────────┴────┘
```

</div>

```bash
sqlcli insert athlete
```

<div class="termy">

```console
$ sqlcli insert athlete

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