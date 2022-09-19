import sys
from pathlib import Path

import pyrrhic
import pyrrhic.cli.cat as cat
import pyrrhic.cli.state
from pyrrhic.repo.repository import Repository, get_masterkey

import typer

app: typer.Typer = typer.Typer(add_completion=False)
app.add_typer(cat.app, name="cat")


@app.command()
def version():
    """Return version of pyrric application"""
    print(pyrrhic.__version__)


@app.callback()
def global_options(
    repo: Path = typer.Option(None, "--repo", "-r", help="repository for subcommands ", envvar="RESTIC_REPOSITORY"),
    password: str = typer.Option(
        None,
        help="repository password",
        envvar="RESTIC_PASSWORD",
    ),
    password_file: Path = typer.Option(None, "--password-file", "-p", help="file to read the repository password from", envvar="RESTIC_PASSWORD_FILE"),
):
    if password_file:
        if password:
            print("password and password-file are mutually exclusive", file=sys.stderr)
            raise typer.Exit(code=1)
        password = Path(password_file).read_text().strip()
    if not password:
        password = typer.prompt("repository password", hide_input=True)

    masterkey = get_masterkey(repo, password)
    pyrrhic.cli.state.repository = Repository(repo, masterkey)


if __name__ == "__main__":
    app()
