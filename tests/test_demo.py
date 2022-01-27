import os

import pytest
from sqlcli.main import app
from typer.testing import CliRunner

runner = CliRunner()


# @pytest.mark.filterwarnings("ignore:Class SelectOfScalar will not")
# def test_init_demo():
#     result = runner.invoke(app, ["init-demo"])
#     assert result.exit_code == 0
#     assert os.path.isfile("demo_database.db")
#     assert os.path.isfile("demo_models.py")
    
    # tear down the db.
    # runner.invoke(app, ["init-demo", "--clear"])
    # assert os.path.isfile("demo_database.db") == False 
    # assert os.path.isfile("demo_models.py") == False
    
    