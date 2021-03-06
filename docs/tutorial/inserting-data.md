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

Now you are ready to select data from the demo database ๐

## Create a new record

Creating a new record is as simple as calling:

```bash
sqlcli insert
```

<div class="termy">

```console
$ sqlcli insert

# Please select a table [sport/athlete]:$ athlete

โโโโโโโโโโโโโโโโโโโโโโโโโ column: `id` โโโโโโโโโโโโโโโโโโโโโโโโโโ
# <class 'int'> (optional):$ 
โโโโโโโโโโโโโโโโโโโโโโโโ column: `name` โโโโโโโโโโโโโโโโโโโโโโโโโ
# <class 'str'>:$ Carter 
โโโโโโโโโโโโโโโโโโโโโโ column: `sport_id` โโโโโโโโโโโโโโโโโโโโโโโ
The column `sport_id` is a foreign key related to the `sport` table. Please select from one of the 
options below from the `id` column:
     sport     
โโโโโโโโโโณโโโโโ
โ name   โ id โ
โกโโโโโโโโโโโโโโฉ
โ Soccer โ 1  โ
โ Hockey โ 2  โ
โโโโโโโโโโดโโโโโ
# <class 'int'> (optional) [1/2]:$ 1
โญโโโโโโโโโโโโโโโโ New row successfully added ๐ โโโโโโโโโโโโโโโโโฎ
โ {'id': 9, 'sport_id': 1, 'name': 'Carter'}                    โ
โฐโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโฏ
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

โโโโโโโโโโโโโโโโโโโโโโโโโ column: `id` โโโโโโโโโโโโโโโโโโโโโโโโโโ
# <class 'int'> (optional):$ 
โโโโโโโโโโโโโโโโโโโโโโโโ column: `name` โโโโโโโโโโโโโโโโโโโโโโโโโ
# <class 'str'>:$ Carter 
โโโโโโโโโโโโโโโโโโโโโโ column: `sport_id` โโโโโโโโโโโโโโโโโโโโโโโ
The column `sport_id` is a foreign key related to the `sport` table. Please select from one of the 
options below from the `id` column:
     sport     
โโโโโโโโโโณโโโโโ
โ name   โ id โ
โกโโโโโโโโโโโโโโฉ
โ Soccer โ 1  โ
โ Hockey โ 2  โ
โโโโโโโโโโดโโโโโ
# <class 'int'> (optional) [1/2]:$ 50
Please select one of the available options
# <class 'int'> (optional) [1/2]:$ Soccer
Please select one of the available options
# <class 'int'> (optional) [1/2]:$ 1
โญโโโโโโโโโโโโโโโโ New row successfully added ๐ โโโโโโโโโโโโโโโโโฎ
โ {'id': 9, 'sport_id': 1, 'name': 'Carter'}                    โ
โฐโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโโฏ
```

</div>
