
import os
from textwrap import dedent
from typing import Any, Dict, Optional

import sqlmodel
import typer
from rich import inspect
from rich.prompt import IntPrompt, Prompt, Confirm
from sqlmodel import Session, SQLModel, create_engine, select, Field

from ._utils import get_db_url, get_tables, get_models
from ._console import console


app = typer.Typer(help="A command line interface (CLI) for interacting with SQLModel.")

# Shared help strings.
database_url_help = """
A database connection string. If no connection string is provided sqlcli will
check for a connection string in the environment variable `DATABASE_URL`.
""".strip().replace("\n", "")


@app.command()
def init_demo(path: str = typer.Option(".", help="The path to save the demo database")):
    """Create a demo database for exploring sqlcli.
    
    Create a demo sqlite database to test with sqlcli.
    """
    console.print("[blue]Creating a sqlite database[/]...")
    from ._demo_models import User, Book
    
    # Create a sqlite database.
    sqlite_file_name = "demo_database.db"
    db_path = os.path.join(path, sqlite_file_name)
    sqlite_url = f"sqlite:///{db_path}"
    engine = create_engine(sqlite_url, echo=False)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    
    # Insert fake data into the sqlite database.
    with Session(engine) as session:
        users = [
            User(email="sam@sqlcli.com", password="passw0rd"),
            User(email="jake@sqlcli.com", password="12345"),
            User(email="olivia@sqlcli.com", password="secret"),
        ]
        books = [
            Book(isbn="1234-5678", title="Harry Potter", author="JK Rowling"),
            Book(isbn="1112-5554", title="Harry Potter 2", author="JK Rowling"),
        ]
        session.add_all(users)
        session.add_all(books)
        session.commit()
        
    console.print(f"Datbase created at [yellow]{db_path}")
    
    with Session(engine) as engine:
        users = session.exec(select(User)).all()
        books = session.exec(select(Book)).all()
        
    console.print("[bold blue]user")
    for u in users:
        console.print(u)
    console.print("[bold blue]user")
    for b in books:
        console.print(b)
        
    console.print("To work with the demo database please copy and paste the two required environment variables into the terminal")
    console.print('export DATABASE_URL="sqlite:///demo_database.db"')
    console.print('export MODELS_MODULE="tests/models.py"')

@app.command('select')
def select_sqlcli(
    table: Optional[str] = typer.Argument(None, help="The name of the table to query."), 
    n: int = typer.Option(10, help="The number of database rows to query."),
    output: str = typer.Option(None, help="The format to output the data. Should be one of [None, 'json']"),
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
    
    console.print(f"[bold blue]{table}")
    for row in data:
        if output == "json":
            row = row.json()
        # TODO: add a rich table option
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
    console.print(f"[bold blue]Enter data for new {table}...")
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
