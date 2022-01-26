
import json
import os
import pkgutil
from textwrap import dedent
from typing import Any, Dict, Optional

import sqlmodel
import typer
from rich import inspect
from rich.markdown import Markdown
from rich.panel import Panel
from rich.pretty import Pretty
from rich.prompt import Confirm, FloatPrompt, IntPrompt, Prompt
from rich.syntax import Syntax
from rich.table import Table
from sqlalchemy import sql
from sqlmodel import Session, SQLModel, col, create_engine, select

import sqlcli

from . import __version__
from ._console import console, error_console
from ._utils import (create_rich_table, get_db_url,
                     get_foreign_key_column_name, get_foreign_key_table_name,
                     get_models, get_primary_key, get_tables, is_foreign_key,
                     sqlmodel_setup, validate_table_name)

# SQLModel has known issue with an error message. Since this is a CLI application
# this error message is really annoying. For now the error will be filtered out.
# Note to self to monitor the GitHub issue for a resolution.
# https://github.com/tiangolo/sqlmodel/issues/189
import warnings
warnings.filterwarnings("ignore", ".*Class SelectOfScalar will not make use of SQL compilation caching.*")


app = typer.Typer(help="A command line interface (CLI) for interacting with SQLModel.")


def version_callback(value: bool):
    if value:
        console.print(f"{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(False, "--version", callback=version_callback, is_eager=True, help="Show the installed version."),
):
    return None



# Shared help strings.
database_url_help = """
A database connection string. If no connection string is provided sqlcli will
check for a connection string in the environment variable `DATABASE_URL`.
""".strip().replace("\n", "")

models_path_help = """
The location of the python script(s) that contain the SQLModels. If no argument
is provided sqlcli will check for a path in the environment variable
`MODELS_PATH`.
""".strip().replace("\n", "")

table_name_help = """
The name of the table to query.
""".strip().replace("\n", "")


@app.command()
def hello_world():
    console.print("hello world!")
    


@app.command()
def init_demo(
    path: str = typer.Option(".", help="The path to save the demo database"),
    clear: bool = typer.Option(False, help="Remove all of the demo database related data including `demo_models.py` and `demo_database.db`.")
):
    """Create a demo database for exploring sqlcli.
    
    Create a demo sqlite database to test with sqlcli.
    """
    db_filename = "demo_database.db"
    models_filename = "demo_models.py"
    
    if clear:
        if os.path.isfile(db_filename) and os.path.isfile(models_filename):
            os.remove(db_filename)
            os.remove(models_filename)
            console.print(f"[info]Removed files: `{db_filename}` and `{models_filename}`")
        else:
            console.print(f"[info]Files NOT found: `{db_filename}` and `{models_filename}`")
        raise typer.Exit()
     
    from ._demo.data import create_demo_data
    from ._demo.models import Athlete, Sport

    # Create a sqlite database.
    db_path = os.path.join(path, db_filename)
    sqlite_url = f"sqlite:///{db_path}"
    engine = create_engine(sqlite_url)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    
    # Insert demo data into the sqlite database.
    with Session(engine) as session:
        data = create_demo_data()
        session.add_all(data)
        session.commit()
    
    # Print the demo data to the console.
    with Session(engine) as engine:
        for obj in [Sport, Athlete]:
            console.rule(f"table: {obj.__table__}")
            data = session.exec(select(obj)).all()
            console.print(create_rich_table(data))
        
    # Create a model.py for the user to use with the demo.
    model_text = pkgutil.get_data(__name__, "_demo/models.py").decode("utf-8")
    with open("./demo_models.py", "w") as f:
        f.write(model_text)
    
    # How to use the demo database.
    model_text_path = os.path.join(os.getcwd(), models_filename)
    database_path = os.path.join(os.getcwd(), db_filename)
    
    console.rule("how to use the demo database", style="blue")
    console.print(f"A demo database has been created at:\n[u]{database_path}\n", style="info")
    console.print(f"[info]Demo models have been saved to:\n[u]{model_text_path}\n")
    
    console.print(f"[info]Here are some example commands to get you started:\n")
    console.print(f'sqlcli select athlete -d "sqlite:///{db_filename}" -m {models_filename}')
    console.print(f'sqlcli insert -d "sqlite:///{db_filename}" -m {models_filename}\n')
    
    console.print("[info]To avoid passing in the `-d` and -`m` option everytime you can set the following environment variables:\n")
    console.print('export DATABASE_URL="sqlite:///demo_database.db"')
    console.print('export MODELS_PATH="demo_models.py"\n')
    
    docs_url = "https://samedwardes.github.io/sqlcli/tutorial/using-demo-db/"
    text = f"[info]For instructions on how to use the demo database visit {docs_url}."
    console.print(text)
    
    

@app.command('select')
def select_sqlcli(
    table_name: Optional[str] = typer.Argument(None, help=table_name_help), 
    n: int = typer.Option(10, "--number-rows", "-n", help="The number of database rows to query."),
    format: str = typer.Option('table', "--format", "-f",  help="The format to output the data. Should be one of [None, 'json', 'dict', 'table']"),
    database_url: Optional[str] = typer.Option(None, "--database-url", "-d", help=database_url_help),
    models_path: Optional[str] = typer.Option(None, "--models-path", "-m", help=models_path_help),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show a more verbose output.")
):
    """Query the database.
    
    Query the database to see the data inside a given table. Calling `sqlcli
    select` is similar to calling `SELECT * FROM [table]`.
    """   
    models, url, engine, tables = sqlmodel_setup(models_path, database_url)
    obj, table_name = validate_table_name(table_name, tables)
        
    with Session(engine) as session:
        data = session.exec(select(obj).limit(n)).all()
    
    if verbose:
        console.rule(f"table: `{table_name}`")
    
    if format == "json":
        # json_rows = [row.json() for row in data]
        # json_data = {table_name: json_rows}
        dict_rows = [row.dict() for row in data]
        dict_data = {table_name: dict_rows}
        json_data = json.dumps(dict_data, indent=4)
        console.print(json_data) 
    elif format == "dict":
        dict_rows = [row.dict() for row in data]
        dict_data = {table_name: dict_rows}
        console.print(dict_data) 
    elif format == "table":
        console.print(create_rich_table(data))
    else:
        for row in data:
            console.print(row)
            
    if verbose:
        with Session(engine) as session:
            all_data = session.exec(select(obj)).all()
            nrows = len(all_data)
        
        console.rule("query details", style="blue")
        console.print(f"DATABASE_URL: {url}")
        console.print(f"Number of rows: {nrows}")


@app.command()
def insert(
    table_name: Optional[str] = typer.Argument(None, help=table_name_help), 
    database_url: Optional[str] = typer.Option(None, "--database-url", "-d", help=database_url_help),
    models_path: Optional[str] = typer.Option(None, "--models-path", "-m", help=models_path_help),
):
    """Insert a new record into the database."""
    models, url, engine, tables = sqlmodel_setup(models_path, database_url)        
    obj, table_name = validate_table_name(table_name, tables)
    
    # Get input from the user:
    data = {}
    
    for field in obj.__fields__.values():
        console.rule(f"column: `{field.name}`")
        
        # Figure out the right type of prompt to render.
        if isinstance(1, field.type_):
            prompt = IntPrompt
        elif isinstance(1.0, field.type_):
            prompt = FloatPrompt
        else:
            prompt = Prompt
            
        # Check if the column is a foreign key. If it is a foreign key identify
        # the list of possible values.
        if is_foreign_key(obj, field.name):
            foreign_table_name = get_foreign_key_table_name(obj, field.name)
            foreign_table = tables[foreign_table_name]
            foreign_key_col_name = get_foreign_key_column_name(obj, field.name)
            with Session(engine) as session:
                options_data = session.exec(select(foreign_table)).all()
                console.print(f"The column `[green]{field.name}[/]` is a foreign key related to the `[blue]{foreign_table_name}[/]` table. Please select from one of the options below from the `[blue]{foreign_key_col_name}[/]` column:")
                console.print(create_rich_table(options_data, title=foreign_table_name))
                prompt_choices = [str(i.dict()[foreign_key_col_name]) for i in options_data]
        else:
            prompt_choices = None      
                    
        # Determine if the field is optional or not.
        prompt_txt = f"{field.type_}"
        if field.allow_none:
            i = prompt.ask(f"{prompt_txt} [info](optional)", default=field.default, choices=prompt_choices)
        else:
            i = prompt.ask(prompt_txt, choices=prompt_choices)
            
        data[field.name] = i
    
    # Write the new data to the database.
    with Session(engine) as session:
        new_row = obj(**data)
        session.add(new_row)
        session.commit()
        session.refresh(new_row)
        console.print(Panel(
            Pretty(new_row.dict()),
            title="New row successfully added :party_popper:",
            border_style="green"
        ))
    

@app.command()
def drop_all(
    database_url: Optional[str] = typer.Option(None, "--database-url", "-d", help=database_url_help),
    models_path: Optional[str] = typer.Option(None, "--models-path", "-m", help=models_path_help),
    do_not_prompt: bool = typer.Option(False, "-y", help="Danger! Skip the prompt and drop the database. This cannot be undone.")
):
    """
    Drop a database. The equivalent to calling
    `SQLModel.metadata.drop_all(engine)`.
    """
    text = dedent("[bold red]Are you sure you want to drop the database? This cannot be undone.")
    if Confirm.ask(text):
        console.print("Dropping the database...")
        models, url, engine, tables = sqlmodel_setup(models_path, database_url)
        SQLModel.metadata.drop_all(engine)
        console.print(":white_check_mark:​ Complete!")
    else:
        console.print("Aborting!")


@app.command()
def create_all(
    database_url: Optional[str] = typer.Option(None, "--database-url", "-d", help=database_url_help),
    models_path: Optional[str] = typer.Option(None, "--models-path", "-m", help=models_path_help),
):
    """
    Create a database. The equivalent to calling
    `SQLModel.metadata.create_all(engine)`.
    """
    console.print("Creating the database...")
    models, url, engine, tables = sqlmodel_setup(models_path, database_url)
    SQLModel.metadata.create_all(engine)
    console.print(":white_check_mark:​ Complete!")


@app.command('inspect')
def inspect_sqlcli(
    table_name: Optional[str] = typer.Argument(None, help=table_name_help), 
    database_url: Optional[str] = typer.Option(None, "--database-url", "-d", help=database_url_help),
    models_path: Optional[str] = typer.Option(None, "--models-path", "-m", help=models_path_help), 
):
    """Inspect a SQLModel with rich.inspect."""
    models, url, engine, tables = sqlmodel_setup(models_path, database_url)
    obj, table_name = validate_table_name(table_name, tables)
    inspect(obj)


@app.command()
def docs():
    """Open the docs: https://samedwardes.github.io/sqlcli/"""
    url = "https://samedwardes.github.io/sqlcli/"
    console.print(f"[info]Opening the docs: {url}")
    typer.launch(url)
