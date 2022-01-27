import importlib
import os
from typing import Dict, List, Optional, Tuple

import typer
from rich import inspect
from rich.prompt import Prompt
from rich.table import Table
from sqlalchemy import Column
from sqlmodel import SQLModel, create_engine

from ._console import console, error_console


def get_db_url(database_url: Optional[str] = None):
    """A helper function to get the database url."""
    if not database_url:
        database_url = os.getenv("DATABASE_URL")
        
        if not database_url:
            msg = "Please ensure that an environment variable is set for `DATABASE_URL` or pass in the url to the database_url option."
            error_console.print(msg)
            raise typer.Exit(code=1)
            
        
    return database_url


def get_tables(models_module) -> Dict[str, SQLModel]:
    """Find all of the SQLModel tables."""
    tables = {}
    for name, obj in models_module.__dict__.items():
        if isinstance(obj, type(SQLModel)) and name != "SQLModel":
            tables[name.lower()] = obj
    return tables


def get_models(models_path: Optional[str] = None):
    # Load the models provided by the user.
    if not models_path:
        models_path = os.getenv("MODELS_PATH")
        if not models_path:
            msg = "No modules_path specified. You can set a modules_path by either passing in a value to the -m option or by setting an environment variable `export MODELS_PATH='demo_models.py'`"
            error_console.print(msg)
            raise typer.Exit(code=1)
        
        
    models_path = os.path.normpath(models_path)
    path, filename = os.path.split(models_path)
    module_name, ext = os.path.split(filename)

    spec = importlib.util.spec_from_file_location(module_name, models_path)
    models = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(models)
        
    return models


def is_foreign_key(obj, field_name: str) -> bool:
    foreign_keys = [i for i in obj.__table__.foreign_keys]
    for fk in foreign_keys:
        if fk.parent.name == field_name:
            return True
    return False


def get_foreign_key_column_name(obj: SQLModel, field_name: str) -> str:
    foreign_keys = [i for i in obj.__table__.foreign_keys]
    for fk in foreign_keys:
        if fk.parent.name == field_name:
            return fk.column.name


def get_foreign_key_table_name(obj: SQLModel, field_name: str) -> Optional[str]:
    foreign_keys = [i for i in obj.__table__.foreign_keys]
    for fk in foreign_keys:
        if fk.parent.name == field_name:
            return fk.column.table.name
    return None
        

def sqlmodel_setup(models_path: str, database_url: str):
    """Quickstart for getting required objects"""
    models = get_models(models_path)
    url = get_db_url(database_url)
    engine = create_engine(url)
    tables = get_tables(models)
    return models, url, engine, tables


def create_rich_table(data: List[SQLModel], **kwargs) -> Table:
    table = Table(**kwargs)
    for col_name in data[0].dict().keys():
        table.add_column(col_name)
    for row in data:
        table.add_row(*[str(i) for i in row.dict().values()])
    return table


def validate_table_name(table_name: Optional[str], tables: List[SQLModel]) -> Tuple[SQLModel, str]:
    if not table_name:
        table_name = Prompt.ask("Please select a table", choices=tables.keys())
    
    try:
        obj = tables[table_name]
    except KeyError:
        error_console.print(f"The provided table does not exist. Please select from one of:")
        error_console.print(f"{list(tables.keys())}")
        raise typer.Exit(code=1)
    
    return obj, table_name
