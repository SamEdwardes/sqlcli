# Installation and Getting Started

## Installation

The first step is to install *sqlcli*. To install *sqlcli* run the following command:

```
pip install sqlcli
```

## How to run *sqlcli*

*sqlcli* is a command a tool that is meant to be run through the command line. There are two primary ways you can run it:

**Option 1**

After install *sqlcli* you will have access to *sqlcli* command. You can run it in your terminal like any other command line program:

```
sqlcli --help
```

**Option 2**

You can also run *sqlcli* by invoking Python:

```
python -m sqlcli --help
```

Both ways produce the exact same result, so use which ever way you prefer. 

## Quick start

*sqlcli* comes with a demo database you can use to explore the program. Run the following commands to get started:

```bash
sqlcli init-demo
sqlcli select athlete -d "sqlite:///sqlcli_demo/database.db" -m "sqlcli_demo/models.py"
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

For more details please check out the next section [Using the demo database](./using-demo-db.md).
