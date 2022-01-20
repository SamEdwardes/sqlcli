import os
from textwrap import dedent
from typing import Optional, Dict

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
