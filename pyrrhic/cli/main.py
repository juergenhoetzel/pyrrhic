import typer
from pathlib import Path
import pyrrhic
from pyrrhic.cli import state
import pyrrhic.cli.cat as cat

app = typer.Typer(add_completion=False)
app.add_typer(cat.app, name="cat")


@app.command()
def version():
    """Return version of pyrric application"""
    print(pyrrhic.__version__)


@app.callback()
def repository(
    repo: Path = typer.Option(
        None, help="repository for subcommands ", envvar="RESTIC_REPOSITORY"
    )
):
    state["repository"] = repo


if __name__ == "__main__":
    app()
