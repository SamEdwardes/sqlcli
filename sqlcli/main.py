
import os
from textwrap import dedent
from typing import Any, Dict, Optional

from rich.syntax import Syntax
import pkgutil

import sqlmodel
import typer
from rich import inspect
from rich.prompt import IntPrompt, Prompt, Confirm
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from sqlmodel import Session, SQLModel, create_engine, select, col

from ._utils import get_db_url, get_tables, get_models, create_rich_table
from ._console import console

# SQLModel has known issue with an error message. Since this is a CLI application
# this error message is really annoying. For now the error will be filtered out.
# Note to self to monitor the GitHub issue for a resolution.
# https://github.com/tiangolo/sqlmodel/issues/189
import warnings
warnings.filterwarnings("ignore", ".*Class SelectOfScalar will not make use of SQL compilation caching.*")

app = typer.Typer(help="A command line interface (CLI) for interacting with SQLModel.")

# Shared help strings.
database_url_help = """
A database connection string. If no connection string is provided sqlcli will
check for a connection string in the environment variable `DATABASE_URL`.
""".strip().replace("\n", "")


@app.command()
def init_demo(
    path: str = typer.Option(".", help="The path to save the demo database"),
    instructions: bool = typer.Option(False, help="Print the instructions on how to use the demo database.")
):
    """Create a demo database for exploring sqlcli.
    
    Create a demo sqlite database to test with sqlcli.
    """
    if instructions:
        data = pkgutil.get_data(__name__, "_demo/demo-instructions.md")
        console.print(Markdown(data.decode("utf-8")))
        console.print("[info]See the docs for more details:")
        console.print("https://samedwardes.github.io/sqlcli/")
        raise typer.Exit()
    
    from ._demo.models import Sport, Athlete
    from ._demo.data import create_demo_data
    
    # Create a sqlite database.
    sqlite_file_name = "demo_database.db"
    db_path = os.path.join(path, sqlite_file_name)
    sqlite_url = f"sqlite:///{db_path}"
    engine = create_engine(sqlite_url, echo=False)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    
    # Insert fake data into the sqlite database.
    with Session(engine) as session:
        data = create_demo_data()
        session.add_all(data)
        session.commit()
    console.print(f"Database created at {db_path}", style="info")
        
    
    with Session(engine) as engine:
        sports = session.exec(select(Sport)).all()
        athletes = session.exec(select(Athlete)).all()
        
    console.rule("sport")
    console.print(create_rich_table(sports))
    
    console.rule("athlete")
    console.print(create_rich_table(athletes))
    
    text = dedent("""
    [info]For instructions on how to use the demo database visit https://samedwardes.github.io/sqlcli/ or run the command:
    [italic]`sqlcli init-demo --instructions`
    """).strip()
    
    console.print(text)
    
    

@app.command('select')
def select_sqlcli(
    table: Optional[str] = typer.Argument(None, help="The name of the table to query."), 
    n: int = typer.Option(10, help="The number of database rows to query."),
    format: str = typer.Option('table', help="The format to output the data. Should be one of [None, 'json', 'dict', 'table']"),
    database_url: Optional[str] = typer.Option(None, help=database_url_help)
):
    """Query the database.
    
    Query the database to see the data inside a given table. Calling `sqlcli
    select` is similar to calling `SELECT * FROM [table]`.
    """
    models = get_models()
    url = get_db_url(database_url)
    engine = create_engine(url)
    tables = get_tables(models)
    
    if not table:
        table = Prompt.ask("Please select a table", choices=tables.keys())
        
    obj = tables[table]
        
    with Session(engine) as session:
        data = session.exec(select(obj).limit(n)).all()
    
    console.rule(f"{table}")
    
    if format == "json":
        for row in data:
            console.print(row.json()) 
    elif format == "dict":
        for row in data:
            console.print(row.dict())
    elif format == "table":
        console.print(create_rich_table(data))
    else:
        for row in data:
            console.print(row)


@app.command()
def insert(
    table: Optional[str] = typer.Argument(None), 
    database_url: Optional[str] = typer.Option(None, help=database_url_help), 
):
    """Insert a new record into the database."""
    models = get_models()
    url = get_db_url(database_url)
    engine = create_engine(url)
    tables = get_tables(models)
    
    if not table:
        table = Prompt.ask("Please select a table", choices=tables.keys())
        
    obj = tables[table]
    
    # Get input from the user:
    console.print(f"[cyan]Enter data for new {table}...")
    data = {}
    for name, field in obj.__fields__.items():
        txt = f"[blue]{name}[/] ({field.type_})"
        if str(field.type_) == "<class 'int'>":
            prompt = IntPrompt
        else:
            prompt = Prompt
        if field.allow_none:
            i = prompt.ask(f"{txt} [bold cyan](optional)", default=field.default,)
        else:
            i = prompt.ask(txt)
        data[name] = i
    
    with Session(engine) as session:
        new_row = obj(**data)
        console.print(new_row)
        session.add(new_row)
        session.commit()
        
    

@app.command()
def drop_all(database_url: Optional[str] = typer.Option(None, help=database_url_help)):
    """Drop a database."""
    text = dedent("[bold red]Are you sure you want to drop the database? This cannot be undone.")
    if Confirm.ask(text):
        console.print("Dropping the database...")
        models = get_models()
        database_url = get_db_url(database_url)
        engine = create_engine(database_url)
        console.print(":white_check_mark:​ Complete!")
    else:
        console.print("Aborting!")


@app.command()
def create_all(database_url: Optional[str] = typer.Option(None, help=database_url_help)):
    """Create a database."""
    console.print("Creating the database...")
    models = get_models()
    database_url = get_db_url(database_url)
    engine = create_engine(database_url)
    SQLModel.metadata.create_all(engine)
    console.print(":white_check_mark:​ Complete!")
