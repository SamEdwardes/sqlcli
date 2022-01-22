# Using the demo database

To work with the demo database first make sure you have run the command:
    
```bash
sqlcli init-demo
```

This will create a new sqlite database on your computer and the related SQLModel classes that you can then use to test *sqlcli*. The command will output two new files in your working directory:

```bash
demo_database.db # A sqlite database with demo data.
demo_models.py   # SQLModel classes that map to the demo database.
```

The demo models are defined as follows:

```Python title="demo_models.py"
{!./sqlcli/_demo/models.py!}
```

Now with your database in place and your models defined you will be able to
play with *sqlcli*!

```bash
sqlcli select athlete -d "sqlite:///demo_database.db" -m "demo_models.py"
sqlcli select sport -d "sqlite:///demo_database.db" -m "demo_models.py"
sqlcli insert athlete -d "sqlite:///demo_database.db" -m "demo_models.py"
```

It can be annoying to specify the database URL and SQLModel modules everytime. To avoid this you can set two environment variables the *sqlcli* will default to:

```bash
export DATABASE_URL="sqlite:///demo_database.db"
export MODELS_PATH="tests/models/sports.py
```

Now you can call the same commands but without specifying the `-d` and `-m` options:

```bash
sqlcli select athlete
sqlcli select sport
sqlcli insert athlete
```