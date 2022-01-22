# CLI

A command line interface (CLI) for interacting with SQLModel.

**Usage**:

```console
$ [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `create-all`: Create a database.
* `drop-all`: Drop a database.
* `init`
* `init-demo`: Create a demo database for exploring sqlcli.
* `insert`: Insert a new record into the database.
* `inspect`: Inspect a SQLModel with rich.inspect.
* `select`: Query the database.

## `create-all`

Create a database. The equivalent to calling
`SQLModel.metadata.create_all(engine)`.

**Usage**:

```console
$ create-all [OPTIONS]
```

**Options**:

* `-d, --database-url TEXT`: A database connection string. If no connection string is provided sqlcli willcheck for a connection string in the environment variable `DATABASE_URL`.
* `-m, --models-path TEXT`: The location of the python script(s) that contain the SQLModels. If no argumentis provided sqlcli will check for a path in the environment variable`MODELS_PATH`.
* `--help`: Show this message and exit.

## `drop-all`

Drop a database. The equivalent to calling
`SQLModel.metadata.drop_all(engine)`.

**Usage**:

```console
$ drop-all [OPTIONS]
```

**Options**:

* `-d, --database-url TEXT`: A database connection string. If no connection string is provided sqlcli willcheck for a connection string in the environment variable `DATABASE_URL`.
* `-m, --models-path TEXT`: The location of the python script(s) that contain the SQLModels. If no argumentis provided sqlcli will check for a path in the environment variable`MODELS_PATH`.
* `-y`: Danger! Skip the prompt and drop the database. This cannot be undone.  [default: False]
* `--help`: Show this message and exit.

## `init`

**Usage**:

```console
$ init [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `init-demo`

Create a demo database for exploring sqlcli.

Create a demo sqlite database to test with sqlcli.

**Usage**:

```console
$ init-demo [OPTIONS]
```

**Options**:

* `--path TEXT`: The path to save the demo database  [default: .]
* `--clear / --no-clear`: Remove all of the demo database related data including `demo_models.py` and `demo_database.db`.  [default: False]
* `--help`: Show this message and exit.

## `insert`

Insert a new record into the database.

**Usage**:

```console
$ insert [OPTIONS] [TABLE_NAME]
```

**Arguments**:

* `[TABLE_NAME]`: The name of the table to query.

**Options**:

* `-d, --database-url TEXT`: A database connection string. If no connection string is provided sqlcli willcheck for a connection string in the environment variable `DATABASE_URL`.
* `-m, --models-path TEXT`: The location of the python script(s) that contain the SQLModels. If no argumentis provided sqlcli will check for a path in the environment variable`MODELS_PATH`.
* `--help`: Show this message and exit.

## `inspect`

Inspect a SQLModel with rich.inspect.

**Usage**:

```console
$ inspect [OPTIONS] [TABLE_NAME]
```

**Arguments**:

* `[TABLE_NAME]`: The name of the table to query.

**Options**:

* `-d, --database-url TEXT`: A database connection string. If no connection string is provided sqlcli willcheck for a connection string in the environment variable `DATABASE_URL`.
* `-m, --models-path TEXT`: The location of the python script(s) that contain the SQLModels. If no argumentis provided sqlcli will check for a path in the environment variable`MODELS_PATH`.
* `--help`: Show this message and exit.

## `select`

Query the database.

Query the database to see the data inside a given table. Calling `sqlcli
select` is similar to calling `SELECT * FROM [table]`.

**Usage**:

```console
$ select [OPTIONS] [TABLE_NAME]
```

**Arguments**:

* `[TABLE_NAME]`: The name of the table to query.

**Options**:

* `-n, --number-rows INTEGER`: The number of database rows to query.  [default: 10]
* `-f, --format TEXT`: The format to output the data. Should be one of [None, 'json', 'dict', 'table']  [default: table]
* `-d, --database-url TEXT`: A database connection string. If no connection string is provided sqlcli willcheck for a connection string in the environment variable `DATABASE_URL`.
* `-m, --models-path TEXT`: The location of the python script(s) that contain the SQLModels. If no argumentis provided sqlcli will check for a path in the environment variable`MODELS_PATH`.
* `-v, --verbose`: Show a more verbose output.  [default: False]
* `--help`: Show this message and exit.
