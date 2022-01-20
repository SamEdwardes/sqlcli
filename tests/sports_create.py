import os

from sqlmodel import Field, Session, SQLModel, create_engine, select

from sports_models import Athlete, Sport

# Create a sqlite database.
path = "."
sqlite_file_name = "demo_database.db"
db_path = os.path.join(path, sqlite_file_name)
sqlite_url = f"sqlite:///{db_path}"
engine = create_engine(sqlite_url, echo=False)
SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)

data = [
    Sport(
        name="Soccer",
        athletes=[
            Athlete(name="Ronaldo"),
            Athlete(name="Messi"),
        ]
    ),
    Sport(
        name="Hockey",
        athletes=[
            Athlete(name="Gretzky"),
            Athlete(name="Crosby"),
        ]
    )
]

with Session(engine) as session:
    session.add_all(data)
    session.commit()
