from distutils.command.build import build
import subprocess

import typer

app = typer.Typer()


def run_bash_command(bash_command: str):
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if output:
        typer.echo(output)
    if error:
        typer.echo(error)

@app.command()
def build_typer_docs():
    """Build the typer API docs."""
    run_bash_command("typer sqlcli.main utils docs --output docs/api/_typer-cli-auto-docs.md")
        

@app.command()
def publish_docs():
    """Build the typer API docs."""
    # Build the typer docs.
    build_typer_docs()
    # Publish to GitHub pages.
    run_bash_command("mkdocs gh-deploy --force")
        

if __name__ == "__main__":
    app()
