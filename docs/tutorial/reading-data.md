# Reading data with `select`

With *sqlcli* you can read data from your database in the command line. The `sqlcli select` command lets you select any table from your database. It is similar to the `SELECT` statement in SQL.

```bash
# using sqlcli
sqlcli select <TABLE>
```

```sql
-- using sql
SELECT * FROM <TABLE>
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

First, try selecting some data from the *athlete* table. The `select` command takes an optional argument for the name of the table.

```bash
sqlcli select athlete
```

```bash
โโโโโโณโโโโโโโโโโโณโโโโโโโโโโโ
โ id โ sport_id โ name     โ
โกโโโโโโโโโโโโโโโโโโโโโโโโโโโฉ
โ 1  โ 1        โ Ronaldo  โ
โ 2  โ 1        โ Messi    โ
โ 3  โ 1        โ Beckham  โ
โ 4  โ 2        โ Gretzky  โ
โ 5  โ 2        โ Crosby   โ
โ 6  โ 2        โ Ovechkin โ
โ 7  โ 2        โ Sundin   โ
โ 8  โ 2        โ Domi     โ
โโโโโโดโโโโโโโโโโโดโโโโโโโโโโโ
```

Nice! The table printed out to the console in an easy to read format.

## Formats

The `select` command also lets you specify different formats. The default format is `'table'` which looks like the output above. You can also specify `'json'`, or `'dict'`.

### json

```bash
sqlcli select athlete --format json -n 3
```

```json
{
    "athlete": [
        {
            "id": 1,
            "sport_id": 1,
            "name": "Ronaldo"
        },
        {
            "id": 2,
            "sport_id": 1,
            "name": "Messi"
        },
        {
            "id": 3,
            "sport_id": 1,
            "name": "Beckham"
        }
    ]
}
```

The json format can be useful if you want to pipe the results into another command. For example we can write the json data to a file named *data.json*.

```bash
sqlcli select athlete --format json -n 3 > data.json
cat data.json
```

```bash
{
    "athlete": [
        {
            "id": 1,
            "sport_id": 1,
            "name": "Ronaldo"
        },
        {
            "id": 2,
            "sport_id": 1,
            "name": "Messi"
        },
        {
            "id": 3,
            "sport_id": 1,
            "name": "Beckham"
        }
    ]
}
```