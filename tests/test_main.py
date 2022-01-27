import os

import pytest
from sqlcli.main import app
from typer.testing import CliRunner
# from sqlcli._demo.data import create_demo_data
# from sqlcli._demo.models import Sport, Athlete

# from sqlmodel import create_engine, Session, SQLModel
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
def test_select():

    # Run tests.
    result = runner.invoke(app, ["select", "sport", "-d", DATABASE_URL, "-m", MODEL_PATH])
    assert result.exit_code == 0
    assert result.stdout.strip() == SPORT_RICH_TABLE.strip()
    