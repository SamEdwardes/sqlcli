import os
import sqlite3
from textwrap import dedent

import pytest
from sqlcli.main import app
from typer.testing import CliRunner

runner = CliRunner()

SPORT_RICH_TABLE = """
┏━━━━┳━━━━━━━━┓
┃ id ┃ name   ┃
┡━━━━╇━━━━━━━━┩
│ 1  │ Soccer │
│ 2  │ Hockey │
└────┴────────┘
"""

DATABASE_NAME = "sqlcli_pytest.db"
DATABASE_URL = f"sqlite:///{DATABASE_NAME}"
MODEL_PATH = "tests/models.py"


@pytest.fixture
def create_test_database():
    con = sqlite3.connect(DATABASE_NAME)
    cur = con.cursor()
    
    # Create sport table.
    cur.execute('CREATE TABLE sport (id, name)')
    cur.execute("INSERT INTO sport VALUES (1, 'Soccer')")
    cur.execute("INSERT INTO sport VALUES (2, 'Hockey')")
    
    # Create athlete table.
    cur.execute('CREATE TABLE athlete (id, name, sport_id)')
    cur.execute("INSERT INTO athlete VALUES (1, 'Ronaldo', 1)")
    cur.execute("INSERT INTO athlete VALUES (2, 'Messi', 1)")
    cur.execute("INSERT INTO athlete VALUES (3, 'Beckham', 1)")
    cur.execute("INSERT INTO athlete VALUES (4, 'Gretzky', 2)")
    cur.execute("INSERT INTO athlete VALUES (5, 'Crosby', 2)")
    cur.execute("INSERT INTO athlete VALUES (6, 'Ovechkin', 2)")
    cur.execute("INSERT INTO athlete VALUES (7, 'Sundin', 2)")
    cur.execute("INSERT INTO athlete VALUES (8, 'Domi', 2)")
    
    # Save the data to the database and close connection.    
    con.commit()
    con.close()
    
    # Run the test.
    yield None

    # Teardown.
    os.remove(DATABASE_NAME)


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "0.1.0"
    

@pytest.mark.filterwarnings("ignore:Class SelectOfScalar will not")
def test_init_demo():
    # Create the demo database.
    result = runner.invoke(app, ["init-demo"])
    assert result.exit_code == 0
    assert os.path.isfile("sqlcli_demo/database.db")
    assert os.path.isfile("sqlcli_demo/models.py")
    
    # Tear down the demo database.
    result = runner.invoke(app, ["init-demo", "--clear"])
    assert result.exit_code == 0
    assert os.path.isdir("sqlcli_demo") == False 
    assert os.path.isfile("sqlcli_demo/models.py") == False 
    

@pytest.mark.filterwarnings("ignore:Class SelectOfScalar will not")
def test_select(create_test_database):
    result = runner.invoke(app, ["select", "sport", "-d", DATABASE_URL, "-m", MODEL_PATH])
    assert result.exit_code == 0
    assert result.stdout.strip() == SPORT_RICH_TABLE.strip()


@pytest.mark.filterwarnings("ignore:Class SelectOfScalar will not")
def test_select_with_input(create_test_database):
    result = runner.invoke(app, ["select", "-d", DATABASE_URL, "-m", MODEL_PATH], input="sport")
    assert result.exit_code == 0
    assert result.stdout.strip().endswith(SPORT_RICH_TABLE.strip())


@pytest.mark.filterwarnings("ignore:Class SelectOfScalar will not")
def test_insert(create_test_database):
    result = runner.invoke(app, ["insert", "sport", "-d", DATABASE_URL, "-m", MODEL_PATH], input="3\nMMA\n")
    
    assert result.exit_code == 0
    assert "'id': 3" in result.stdout
    assert "'name': 'MMA'" in result.stdout
    assert "New row successfully added 🎉" in result.stdout
