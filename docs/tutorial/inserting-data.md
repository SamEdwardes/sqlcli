# Writing data with `insert`

With *sqlcli* you can insert data into your database using the command line.. The `sqlcli insert` command helps you interactively create a new record.. It is similar to the `INSERT INTO` statement in SQL.

```bash
# using sqlcli
sqlcli insert <TABLE>
```

```sql
-- using sql
INSERT INTO <TABLE>
```

## Set up the demo database

To get started, first make sure you have set up the demo database.

```bash
sqlcli init-demo
```

To avoid having to specify the database and models with each command lets set our two optional environment variables:

```bash
export DATABASE_URL="sqlite:///sqlcli_demo/database.db"
export MODELS_PATH="sqlcli_demo/models.py"
```

Now you are ready to select data from the demo database 🙌

## Create a new record

Creating a new record is as simple as calling:

```bash
sqlcli insert
```

<div class="termy">

```console
$ sqlcli insert

# Please select a table [sport/athlete]:$ athlete

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

Alternatively, if you knew which table you wanted to insert a record into you could have also called:

```bash
sqlcli insert athlete
```

## Interactive prompt

One of the main features of *sqlcli* is the interactive prompt. *sqlcli* uses the information from your *sqlmodel* classes to generate a smart and interactive prompt. When inserting new data into the database *sqlcli* knows:

- What is the correct **type**. For example an integer is required, but a string is input by the user *sqlcli* will re-prompt you
- The **relationships** between tables. When a value is a foreign key to another table *sqlcli* will show you a preview of that table and only allow you to input valid options.

In the example below the user tries to enter an invalid input:

```bash
sqlcli insert athlete
```

<div class="termy">

```console
$ sqlcli insert

# Please select a table [sport/athlete]:$ athlete

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
# <class 'int'> (optional) [1/2]:$ 50
Please select one of the available options
# <class 'int'> (optional) [1/2]:$ Soccer
Please select one of the available options
# <class 'int'> (optional) [1/2]:$ 1
╭──────────────── New row successfully added 🎉 ────────────────╮
│ {'id': 9, 'sport_id': 1, 'name': 'Carter'}                    │
╰───────────────────────────────────────────────────────────────╯
```

</div>
