from pathlib import Path

import pyrrhic
import pyrrhic.cli.cat as cat
from pyrrhic.cli.state import state

import typer

app: typer.Typer = typer.Typer(add_completion=False)
app.add_typer(cat.app, name="cat")


@app.command()
def version():
    """Return version of pyrric application"""
    print(pyrrhic.__version__)


@app.callback()
def global_options(
    repo: Path = typer.Option(
        None, help="repository for subcommands ", envvar="RESTIC_REPOSITORY"
    ),
    password: str = typer.Option(
        None,
        help="repository password",
        prompt=True,
        hide_input=True,
        envvar="RESTIC_PASSWORD",
    ),
):
    state.repository = repo
    state.password = password


if __name__ == "__main__":
    app()
