import os
from pprint import pprint

from pyrrhic.cli.state import state
from pyrrhic.cli.util import catch_exception, get_dir_masterkey
from pyrrhic.crypto.keys import get_config
from pyrrhic.repo.index import get_index
from pyrrhic.repo.snapshot import get_snapshot

import typer

app: typer.Typer = typer.Typer(add_completion=False)


@app.command()
@catch_exception(ValueError, exit_code=1)
@catch_exception(FileNotFoundError, exit_code=2)
def masterkey():
    """Return masterkey JSON to stdout"""
    valid_state = state.get_valid_state()
    keys_dir = os.path.join(valid_state.repository, "keys")
    key = get_dir_masterkey(keys_dir, valid_state.password)
    pprint(key.restic_json())


@app.command()
@catch_exception(ValueError, exit_code=1)
@catch_exception(FileNotFoundError, exit_code=2)
def config():
    """Return config JSON to stdout"""
    valid_state = state.get_valid_state()
    keys_dir = os.path.join(valid_state.repository, "keys")
    masterkey = get_dir_masterkey(keys_dir, valid_state.password)
    pprint(get_config(masterkey, os.path.join(valid_state.repository, "config")))


@app.command()
@catch_exception(ValueError, exit_code=1)
@catch_exception(FileNotFoundError, exit_code=2)
def index(index_id: str):
    """Return index JSON to stdout"""
    valid_state = state.get_valid_state()
    keys_dir = os.path.join(valid_state.repository, "keys")
    masterkey = get_dir_masterkey(keys_dir, valid_state.password)
    index = get_index(os.path.join(valid_state.repository, "index", index_id), masterkey)
    print(index.json(indent=2))


@app.command()
@catch_exception(ValueError, exit_code=1)
@catch_exception(FileNotFoundError, exit_code=2)
def snapshot(snapshot_id: str):
    """Return snapshot JSON to stdout"""
    valid_state = state.get_valid_state()
    keys_dir = os.path.join(valid_state.repository, "keys")
    masterkey = get_dir_masterkey(keys_dir, valid_state.password)
    snapshot = get_snapshot(os.path.join(valid_state.repository, "snapshots", snapshot_id), masterkey)
    print(snapshot.json(indent=2))
