from pprint import pprint

from pyrrhic.cli.state import repository
from pyrrhic.cli.util import catch_exception


import typer

app: typer.Typer = typer.Typer(add_completion=False)


@app.command()
@catch_exception(ValueError, exit_code=1)
@catch_exception(FileNotFoundError, exit_code=2)
def masterkey():
    """Return masterkey JSON to stdout"""
    print(repository.get_masterkey().restic_json())


@app.command()
@catch_exception(ValueError, exit_code=1)
@catch_exception(FileNotFoundError, exit_code=2)
def config():
    """Return config JSON to stdout"""
    config = repository.get_config()
    pprint(config)


@app.command()
@catch_exception(ValueError, exit_code=1)
@catch_exception(FileNotFoundError, exit_code=2)
def index(index_id: str):
    """Return index JSON to stdout"""
    index = repository.get_index(index_id)
    print(index.json(indent=2))


@app.command()
@catch_exception(ValueError, exit_code=1)
# @catch_exception(FileNotFoundError, exit_code=2)
def snapshot(snapshot_id: str):
    """Return snapshot JSON to stdout"""
    snapshot = repository.get_snapshot(snapshot_id)
    print(snapshot.json(indent=2))
