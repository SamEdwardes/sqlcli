from typer.testing import CliRunner
import os

from sqlcli.main import app

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "0.1.0-alpha.0"
    
    
def test_app():
    result = runner.invoke(app, ["hello-world"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "hello world!"
    

def test_init_demo():
    result = runner.invoke(app, ["init-demo"])
    assert result.exit_code == 0
    assert os.path.isfile("demo_database.db")
    assert os.path.isfile("demo_models.py")
    
    # tear down the db.
    runner.invoke(app, ["init-demo", "--clear"])
    assert os.path.isfile("demo_database.db") == False 
    assert os.path.isfile("demo_models.py") == False
    
