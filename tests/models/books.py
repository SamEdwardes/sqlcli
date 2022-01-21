from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    password: str
    

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    isbn: str
    title: str
    author: str
    url: Optional[str]