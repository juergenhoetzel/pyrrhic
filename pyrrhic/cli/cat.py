import os
import shutil
import sys
from pprint import pprint

import pyrrhic.cli.state
from pyrrhic.cli.util import catch_exception


import typer

app: typer.Typer = typer.Typer(add_completion=False)


@app.command()
@catch_exception(ValueError, exit_code=1)
@catch_exception(FileNotFoundError, exit_code=2)
def masterkey():
    """Return masterkey JSON to stdout"""
    state = pyrrhic.cli.state
    print(state.repository.masterkey.restic_json())


@app.command()
@catch_exception(ValueError, exit_code=1)
@catch_exception(FileNotFoundError, exit_code=2)
def config():
    """Return config JSON to stdout"""
    state = pyrrhic.cli.state
    config = state.repository.get_config()
    pprint(config)


@app.command()
@catch_exception(ValueError, exit_code=1)
@catch_exception(FileNotFoundError, exit_code=2)
def index(index_id: str):
    """Return index JSON to stdout"""
    state = pyrrhic.cli.state
    indexes = state.repository.get_index(index_id)
    if (index := next(indexes, None)) and next(indexes, None) is None:
        print(index.json(indent=2))
    else:
        raise ValueError(f"Invalid Index: {index_id}")


@app.command()
@catch_exception(ValueError, exit_code=1)
@catch_exception(FileNotFoundError, exit_code=2)
def snapshot(snapshot_id: str):
    """Return snapshot JSON to stdout"""
    state = pyrrhic.cli.state
    snapshot = state.repository.get_snapshot(snapshot_id)
    print(snapshot.json(indent=2, exclude_none=True))


@app.command()
@catch_exception(ValueError, exit_code=1)
@catch_exception(FileNotFoundError, exit_code=2)
def pack(pack_id: str, header: bool = typer.Option(False, "--header", help="Output parsed pack header")):
    """Return pack to stdout"""
    state = pyrrhic.cli.state
    pack = state.repository.get_pack(pack_id)
    if header:
        pprint(list(pack.get_blob_index()))
    else:
        with os.fdopen(sys.stdout.fileno(), "wb", closefd=False) as stdout, open(pack.path, "rb") as pack_fd:
            shutil.copyfileobj(pack_fd, stdout)
