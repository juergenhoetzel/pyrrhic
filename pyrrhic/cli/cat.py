import operator
import os
import shutil
import sys

import pyrrhic.cli.state
from pyrrhic.cli.util import catch_exception

from rich import print

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
    print(config)


@app.command()
@catch_exception(ValueError, exit_code=1)
@catch_exception(FileNotFoundError, exit_code=2)
def index(index_id: str):
    """Return index JSON to stdout"""
    state = pyrrhic.cli.state
    indexes = state.repository.get_index(index_id)
    if len(indexes) == 1:
        print(indexes[0].json(indent=2))
    else:
        raise ValueError(f"Invalid Index: {index_id}")


@app.command()
@catch_exception(ValueError, exit_code=1)
@catch_exception(FileNotFoundError, exit_code=2)
def snapshot(snapshot_id: str):
    """Return snapshot JSON to stdout"""
    state = pyrrhic.cli.state
    if snapshot_id == "latest":
        snapshots = iter(sorted(pyrrhic.cli.state.repository.get_snapshot(), key=operator.attrgetter("time"), reverse=True)[:1])
    else:
        snapshots = state.repository.get_snapshot(snapshot_id)
    if (snapshot := next(snapshots, None)) and next(snapshots, None) is None:
        print(snapshot.json(indent=2, exclude_none=True))
    else:
        raise ValueError(f"Invalid Index: {snapshot_id}")


@app.command()
@catch_exception(ValueError, exit_code=1)
@catch_exception(FileNotFoundError, exit_code=2)
def pack(pack_id: str, header: bool = typer.Option(False, "--header", help="Output parsed pack header")):
    """Return pack to stdout"""
    state = pyrrhic.cli.state
    pack = state.repository.get_pack(pack_id)
    if header:
        print(list(pack.get_blob_index()))
    else:
        with os.fdopen(sys.stdout.fileno(), "wb", closefd=False) as stdout, open(pack.path, "rb") as pack_fd:
            shutil.copyfileobj(pack_fd, stdout)
