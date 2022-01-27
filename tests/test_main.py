import os

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

DATABASE_URL = "sqlite:///demo_database.db"
MODEL_PATH = "demo_models.py"


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "0.1.0-alpha.0"
    

@pytest.mark.filterwarnings("ignore:Class SelectOfScalar will not")
def test_init_demo():
    result = runner.invoke(app, ["init-demo"])
    assert result.exit_code == 0
    assert os.path.isfile("demo_database.db")
    assert os.path.isfile("demo_models.py")   
    

@pytest.mark.filterwarnings("ignore:Class SelectOfScalar will not")
def test_select():
    result = runner.invoke(app, ["select", "sport", "-d", DATABASE_URL, "-m", MODEL_PATH])
    assert result.exit_code == 0
    assert result.stdout.strip() == SPORT_RICH_TABLE.strip()


@pytest.mark.filterwarnings("ignore:Class SelectOfScalar will not")
def test_select_with_input():
    result = runner.invoke(app, ["select", "-d", DATABASE_URL, "-m", MODEL_PATH], input="sport")
    assert result.exit_code == 0
    assert result.stdout.strip().endswith(SPORT_RICH_TABLE.strip())


# @pytest.mark.filterwarnings("ignore:Class SelectOfScalar will not")
# def test_insert():
#     result = runner.invoke(app, ["insert", "sport", "-d", DATABASE_URL, "-m", MODEL_PATH], input="MMA\n")
#     assert result.exit_code == 0


# Note this test should always run last!
@pytest.mark.filterwarnings("ignore:Class SelectOfScalar will not")
def test_init_demo_clear():
    # Rear down the db.
    result = runner.invoke(app, ["init-demo", "--clear"])
    assert result.exit_code == 0
    assert os.path.isfile("demo_database.db") == False 
    assert os.path.isfile("demo_models.py") == False
