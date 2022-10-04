import logging
import sys
from enum import Enum
from pathlib import Path

import pyrrhic
import pyrrhic.cli.cat as cat
import pyrrhic.cli.snapshots as snapshots
import pyrrhic.cli.state
from pyrrhic.cli.ls import ls
from pyrrhic.cli.restore import restore
from pyrrhic.cli.util import catch_exception
from pyrrhic.repo.repository import Repository, get_masterkey

from rich.logging import RichHandler

import typer

app: typer.Typer = typer.Typer(add_completion=False)
app.add_typer(cat.app, name="cat", help="🐈 Print internal objects to stdout")
app.command()(snapshots.snapshots)
app.command()(ls)
app.command()(restore)


class LogLevel(str, Enum):
    debug = "DEBUG"
    info = "INFO"
    warn = "WARN"
    error = "ERROR"

    def __str__(self):
        return self.value


@app.command()
def version():
    """Return version of pyrric application"""
    print(pyrrhic.__version__)


@app.callback()
@catch_exception(OSError, exit_code=2)
@catch_exception(ValueError, exit_code=1)
def global_options(
    loglevel: LogLevel = typer.Option(LogLevel.error, case_sensitive=False),
    repo: Path = typer.Option(None, "--repo", "-r", help="repository for subcommands ", envvar="RESTIC_REPOSITORY"),
    password: str = typer.Option(
        None,
        help="repository password",
        envvar="RESTIC_PASSWORD",
    ),
    password_file: Path = typer.Option(None, "--password-file", "-p", help="file to read the repository password from", envvar="RESTIC_PASSWORD_FILE"),
):
    logging.basicConfig(level=str(loglevel), format="%(name)s: %(message)s", datefmt="[%X]", handlers=[RichHandler()])
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
