# Using the demo database

To work with the demo database first make sure you have run the command:
    
```bash
sqlcli init-demo
```

This will create a new sqlite database on your computer that you can then
use to test *sqlcli*.

Next you need to create a python module that contains the SQLModels. Create
a new file named *models.py*.

```bash
touch models.py
```

Then copy and paste the following code into *models.py*:

```python
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Sport(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    athletes: List["Athlete"] = Relationship(back_populates="sport")
    

class Athlete(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    sport_id: Optional[int] = Field(default=None, foreign_key="sport.id")
    sport: Optional[Sport] = Relationship(back_populates="athletes")
```

Now with your database in place and your models defined you will be able to
play with *sqlcli*!

```bash
sqlcli select sport
sqlcli select athlete
sqlcli insert
```