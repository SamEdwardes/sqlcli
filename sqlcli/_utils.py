import importlib
import os
from textwrap import dedent
from typing import Dict, Optional, List

from rich.table import Table

from sqlmodel import SQLModel

from ._console import console


def get_db_url(database_url: Optional[str] = None):
    """A helper function to get the database url."""
    if not database_url:
        database_url = os.getenv("DATABASE_URL")
        
        if not database_url:
            msg = "Please ensure that an environment variable is set for `DATABASE_URL` or pass in the url to the database_url option."
            raise NameError(msg)
        
    return database_url


def get_tables(models_module) -> Dict[str, SQLModel]:
    """Find all of the SQLModel tables."""
    tables = {}
    for name, obj in models_module.__dict__.items():
        if isinstance(obj, type(SQLModel)) and name != "SQLModel":
            tables[name.lower()] = obj
    return tables


def get_models(module_path: Optional[str] = None):
    # Load the models provided by the user.
    if not module_path:
        module_path = os.getenv("MODELS_MODULE")
        if not module_path:
            raise NameError("No modules_path specific")
        
    module_path = os.path.normpath(module_path)
    path, filename = os.path.split(module_path)
    module_name, ext = os.path.split(filename)

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    models = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(models)
        
    return models


def create_rich_table(data: List[SQLModel]) -> Table:
    table = Table()
    for col_name in data[0].dict().keys():
        table.add_column(col_name)
    for row in data:
        table.add_row(*[str(i) for i in row.dict().values()])
    return table