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
* `init-demo`: Create a demo database for exploring sqlcli.
* `insert`: Insert a new record into the database.
* `select`: Query the database.

## `create-all`

Create a database.

**Usage**:

```console
$ create-all [OPTIONS]
```

**Options**:

* `--database-url TEXT`: A database connection string. If no connection string is provided sqlcli willcheck for a connection string in the environment variable `DATABASE_URL`.
* `--help`: Show this message and exit.

## `drop-all`

Drop a database.

**Usage**:

```console
$ drop-all [OPTIONS]
```

**Options**:

* `--database-url TEXT`: A database connection string. If no connection string is provided sqlcli willcheck for a connection string in the environment variable `DATABASE_URL`.
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
* `--instructions / --no-instructions`: Print the instructions on how to use the demo database.  [default: False]
* `--help`: Show this message and exit.

## `insert`

Insert a new record into the database.

**Usage**:

```console
$ insert [OPTIONS] [TABLE]
```

**Arguments**:

* `[TABLE]`

**Options**:

* `--database-url TEXT`: A database connection string. If no connection string is provided sqlcli willcheck for a connection string in the environment variable `DATABASE_URL`.
* `--help`: Show this message and exit.

## `select`

Query the database.

Query the database to see the data inside a given table. Calling `sqlcli
select` is similar to calling `SELECT * FROM [table]`.

**Usage**:

```console
$ select [OPTIONS] [TABLE]
```

**Arguments**:

* `[TABLE]`: The name of the table to query.

**Options**:

* `--n INTEGER`: The number of database rows to query.  [default: 10]
* `--format TEXT`: The format to output the data. Should be one of [None, 'json', 'dict', 'table']  [default: table]
* `--database-url TEXT`: A database connection string. If no connection string is provided sqlcli willcheck for a connection string in the environment variable `DATABASE_URL`.
* `--help`: Show this message and exit.
